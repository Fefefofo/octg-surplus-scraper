"""Starter scrape flow for surplus OCTG pipe listings.

This demo combines browser-use for browser navigation with ScrapeGraphAI for
LLM-assisted extraction. The included target is a generic placeholder page
shape so the project is safe to run while you swap in real public target URLs.
"""

from __future__ import annotations

import asyncio
from typing import Any

from browser_use import Agent
from scrapegraphai.graphs import SmartScraperGraph

from config import settings
from models import OCTGListing
from writer import write_listings_csv


TARGET_URLS = [
    # Replace this with real public inventory pages once you confirm terms of use.
    # Examples to evaluate later: Rigzone marketplace pages, pipe surplus brokers,
    # or industrial surplus sites that publish OCTG inventory pages.
    "https://example.com/industrial-surplus/octg-pipe",
]


EXTRACTION_PROMPT = """
Extract surplus OCTG pipe inventory listings from this page.
Return every listing you can find with these fields:
company_name, pipe_grade, diameter, wall_thickness, length, quantity, price,
location, contact_email, source_url.

If a field is missing, use null. Keep measurements and prices as written.
"""


def build_scrapegraph_config() -> dict[str, Any]:
    """Build ScrapeGraphAI configuration using a local LLM API key placeholder."""

    if settings.openai_api_key:
        return {
            "llm": {
                "api_key": settings.openai_api_key,
                "model": settings.llm_model,
            },
            "verbose": True,
            "headless": True,
        }

    if settings.anthropic_api_key:
        return {
            "llm": {
                "api_key": settings.anthropic_api_key,
                "model": "claude-3-5-sonnet-latest",
            },
            "verbose": True,
            "headless": True,
        }

    raise RuntimeError(
        "Add OPENAI_API_KEY or ANTHROPIC_API_KEY to .env before running extraction."
    )


async def inspect_target_with_browser_use(url: str) -> str:
    """Use browser-use to open the page and summarize the relevant DOM content."""

    agent = Agent(
        task=(
            "Open this public industrial surplus marketplace page and identify "
            f"where OCTG pipe inventory listings appear: {url}. "
            "Summarize the page sections and useful listing selectors."
        )
    )
    result = await agent.run()
    return str(result)


def extract_listings_with_scrapegraph(url: str) -> list[OCTGListing]:
    """Run ScrapeGraphAI against a target page and normalize results."""

    graph = SmartScraperGraph(
        prompt=EXTRACTION_PROMPT,
        source=url,
        config=build_scrapegraph_config(),
    )
    raw_result = graph.run()

    listings = raw_result.get("listings", raw_result)
    if isinstance(listings, dict):
        listings = [listings]

    normalized: list[OCTGListing] = []
    for item in listings or []:
        if isinstance(item, dict):
            item.setdefault("source_url", url)
            normalized.append(OCTGListing.model_validate(item))

    return normalized


async def scrape_targets(urls: list[str]) -> list[OCTGListing]:
    """Coordinate browser inspection and structured listing extraction."""

    all_listings: list[OCTGListing] = []
    for url in urls:
        print(f"Inspecting target with browser-use: {url}")
        browser_notes = await inspect_target_with_browser_use(url)
        print(browser_notes)

        print(f"Extracting listings with ScrapeGraphAI: {url}")
        all_listings.extend(extract_listings_with_scrapegraph(url))

    return all_listings


async def main() -> None:
    listings = await scrape_targets(TARGET_URLS)
    output_path = write_listings_csv(listings, settings.output_csv)
    print(f"Saved {len(listings)} listing(s) to {output_path}")


if __name__ == "__main__":
    asyncio.run(main())
