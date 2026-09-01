# Video RAG System

A multimodal **Video Question-Answering (Video RAG)** system built with **Ragie, MCP, LangChain, and Neon PostgreSQL**.

## Tech Stack

* **Ragie** — Video visual/audio parsing and indexing
* **MCP** — Tool exposure
* **LangChain** — RAG orchestration
* **Neon PostgreSQL** — Metadata storage

## Setup

### 1. Clone and configure environment

```bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_REPOSITORY_DIRECTORY>

cp .env.example .env
```

Add the required API keys and database URL to `.env`.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Initialize the database

```bash
python database.py
```

### 4. Upload and index a video

```bash
python ragie_ingest.py /path/to/your_video.mp4
```

Example:

```bash
python ragie_ingest.py ./videos/sample.mp4
```

### 5. Query the video

```bash
python orchestrator.py "What actions happen around the 3 minute mark?"
```

## Workflow

```text
Video
  ↓
Ragie
  ↓
Video Index
  ↓
MCP + LangChain
  ↓
Relevant Context
  ↓
Question Answering
```

## Project Structure

```text
├── README.md
├── requirements.txt
├── .env.example
├── database.py
├── ragie_ingest.py
└── orchestrator.py
```
