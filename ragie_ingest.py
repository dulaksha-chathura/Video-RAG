import sys
import time
from database import get_db_connection
from ragie import Ragie
from config import RAGIE_API_KEY


class VideoIngestor:

    def __init__(self):
        self.client = Ragie(auth=RAGIE_API_KEY)

    def upload_and_register_video(self, file_path: str, name: str) -> str:
        print(f"Uploading '{name}' to Ragie for multimodal processing...")
        with open(file_path, "rb") as f:
            document = self.client.documents.create(
                request={
                    "file": {"file_name": name, "content": f},
                    "metadata": {"type": "video", "source_name": name},
                }
            )

        doc_id = document.id
        print(f"Document created in Ragie (ID: {doc_id}). Syncing to Neon...")

        # Record metadata in Neon DB
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO video_documents (ragie_doc_id, file_name, status)
            VALUES (%s, %s, %s)
            ON CONFLICT (ragie_doc_id) DO UPDATE SET status = EXCLUDED.status;
            """,
            (doc_id, name, "processing"),
        )
        conn.commit()
        cursor.close()
        conn.close()

        self._wait_for_indexing(doc_id)
        return doc_id

    def _wait_for_indexing(self, doc_id: str):
        print("Waiting for Ragie VLM keyframe and transcription indexing...")
        while True:
            doc = self.client.documents.get(document_id=doc_id)
            status = doc.status
            print(f"Ragie status: {status}")

            if status in ["ready", "summary_indexed"]:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE video_documents SET status = 'ready' WHERE"
                    " ragie_doc_id = %s;",
                    (doc_id,),
                )
                conn.commit()
                cursor.close()
                conn.close()
                print("✓ Video indexing completed successfully!")
                break
            elif status == "failed":
                raise RuntimeError(
                    f"Video indexing failed in Ragie for ID: {doc_id}"
                )

            time.sleep(5)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ragie_ingest.py <path_to_video.mp4>")
        sys.exit(1)

    file_path = sys.argv[1]
    file_name = file_path.split("/")[-1]
    ingestor = VideoIngestor()
    ingestor.upload_and_register_video(file_path, file_name)
