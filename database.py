import psycopg2
from config import NEON_DATABASE_URL


def get_db_connection():
    return psycopg2.connect(NEON_DATABASE_URL)


def init_db():
    """Creates the tracking table in Neon PostgreSQL if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS video_documents (
            id SERIAL PRIMARY KEY,
            ragie_doc_id VARCHAR(255) UNIQUE NOT NULL,
            file_name VARCHAR(255) NOT NULL,
            status VARCHAR(50) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("✓ Neon PostgreSQL database tables initialized.")


if __name__ == "__main__":
    init_db()
