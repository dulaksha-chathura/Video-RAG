from fastmcp import FastMCP
from ragie import Ragie
from config import RAGIE_API_KEY

mcp = FastMCP("Video-RAG-MCP-Server")
ragie_client = Ragie(auth=RAGIE_API_KEY)


@mcp.tool()
def search_video_content(query: str, top_k: int = 5) -> str:
    """Search indexed video documents for timestamped transcript text, visual scene descriptions, and audio content."""
    results = ragie_client.retrievals.retrieve(
        request={"query": query, "top_k": top_k, "rerank": True}
    )

    if not results.scored_chunks:
        return "No matching video content found."

    chunks_formatted = []
    for chunk in results.scored_chunks:
        start_t = chunk.metadata.get("timestamp_start", "N/A")
        end_t = chunk.metadata.get("timestamp_end", "N/A")

        chunks_formatted.append(
            f"[Timestamp: {start_t}s - {end_t}s | Confidence:"
            f" {chunk.score:.2f}]\nContent: {chunk.text}"
        )

    return "\n---\n".join(chunks_formatted)


if __name__ == "__main__":
    mcp.run()
