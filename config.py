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


@dataclass(frozen=True)
class TargetSite:
    """Public inventory page and scraping notes for one source."""

    name: str
    slug: str
    url: str
    structure: str
    visible_fields: tuple[str, ...]
    listing_selector: str
    detail_link_selector: str | None
    pagination_selector: str | None
    notes: str


TARGET_SITES: tuple[TargetSite, ...] = (
    TargetSite(
        name="KO Supply",
        slug="ko-supply",
        url="https://kosupply.com/inventory/",
        structure="Static WordPress/wpDataTables HTML table rendered in the page source.",
        visible_fields=(
            "OD",
            "weight",
            "grade",
            "end finish",
            "length",
            "manufacturer",
            "status",
            "joints",
            "quantity in feet",
            "comments",
            "MTR availability",
        ),
        listing_selector="#table_4 tbody tr[data-row-index]",
        detail_link_selector=None,
        pagination_selector=".dataTables_paginate a",
        notes=(
            "Best first target because the inventory rows are present in HTML. "
            "No public row-level price is shown; use the contact page for outreach."
        ),
    ),
    TargetSite(
        name="Surplus & Prime Worldwide",
        slug="surplus-and-prime",
        url="https://surplusandprime.com/product-category/oilfield-equipment/octg/",
        structure="Static WordPress/WooCommerce category pages with auction product cards.",
        visible_fields=(
            "pipe type",
            "diameter",
            "weight",
            "grade",
            "connection or spec",
            "length",
            "manufacturer",
            "joint or metric-ton quantity",
            "starting bid",
            "product detail URL",
        ),
        listing_selector="ul.products li.product",
        detail_link_selector="a.woocommerce-LoopProduct-link, a.ast-loop-product__link",
        pagination_selector="nav.woocommerce-pagination a.page-numbers",
        notes=(
            "Category pages expose useful title, price, category, and link fields. "
            "Follow each detail URL for richer location/contact data when present."
        ),
    ),
    TargetSite(
        name="Salvex Pipe Trading",
        slug="salvex-pipe",
        url="https://www.salvex.com/pipe/",
        structure="Next.js/React application; listings hydrate client-side after the initial HTML shell.",
        visible_fields=(
            "asset title",
            "category",
            "region or location",
            "quantity",
            "condition",
            "asking price or bid status",
            "seller/contact workflow",
        ),
        listing_selector="[class*='product'], [class*='asset'], [class*='listing']",
        detail_link_selector="a[href*='/listings/'], a[href*='/pipe/']",
        pagination_selector="button[aria-label*='Next'], a[aria-label*='Next']",
        notes=(
            "Use browser-use or Playwright for this source; curl only returns the app shell "
            "and loading skeletons. ScrapeGraphAI should run after browser rendering."
        ),
    ),
)


settings = Settings()
