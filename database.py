import os
from dotenv import load_dotenv

load_dotenv()

RAGIE_API_KEY = os.getenv("RAGIE_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
NEON_DATABASE_URL = os.getenv("NEON_DATABASE_URL", "")


def validate_config():
    missing = []
    if not RAGIE_API_KEY:
        missing.append("RAGIE_API_KEY")
    if not OPENAI_API_KEY:
        missing.append("OPENAI_API_KEY")
    if not NEON_DATABASE_URL:
        missing.append("NEON_DATABASE_URL")

    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}"
        )


validate_config()
