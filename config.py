"""Configuration helpers for local API keys and scraper settings."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Runtime configuration loaded from environment variables."""

    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    anthropic_api_key: str | None = os.getenv("ANTHROPIC_API_KEY")
    llm_model: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
    output_csv: str = os.getenv("OUTPUT_CSV", "output/listings.csv")


settings = Settings()
