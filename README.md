# OCTG Surplus Scraper

Python starter project for finding surplus OCTG (oil country tubular goods) pipe listings from public marketplace and broker websites.

The scaffold combines:

- `browser-use` for browser-based page inspection and navigation.
- `ScrapeGraphAI` for LLM-assisted extraction from marketplace pages.
- `Pydantic` for normalized listing records.
- A CSV writer for local lead and inventory review.

## What it captures

Each parsed listing is normalized into:

- `company_name`
- `pipe_grade`
- `diameter`
- `wall_thickness`
- `length`
- `quantity`
- `price`
- `location`
- `contact_email`
- `source_url`

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install
cp .env.example .env
```

Edit `.env` and add either an OpenAI key or a Claude/Anthropic key:

```bash
OPENAI_API_KEY=replace-with-your-openai-key
ANTHROPIC_API_KEY=replace-with-your-claude-key
```

No real API keys are committed to this repository.

## Run the scraper

```bash
python main.py
```

Results are written to:

```text
output/listings.csv
```

## How to add target sites

Open `main.py` and update `TARGET_URLS`.

Start with public pages that already list inventory in a readable page, then validate each site's terms of use and robots guidance before running repeated scrapes.

Good future targets to evaluate:

- Rigzone marketplace or classifieds pages.
- Public pipe surplus broker inventory pages.
- Industrial surplus marketplace pages with OCTG, casing, tubing, drill pipe, or line pipe categories.

For each site:

1. Add the inventory page URL to `TARGET_URLS`.
2. Run once and inspect the browser-use summary.
3. Tighten `EXTRACTION_PROMPT` with site-specific hints if needed.
4. Confirm the CSV rows preserve critical fields like grade, OD, wall, quantity, yard location, and contact info.

## Starter architecture

```text
config.py      Loads API key placeholders and output settings.
models.py      Defines the Pydantic OCTGListing schema.
writer.py      Saves normalized listings to CSV.
main.py        Coordinates browser-use inspection, ScrapeGraphAI extraction, and CSV output.
```

## Notes on the sample URL

The starter uses a generic placeholder URL:

```text
https://example.com/industrial-surplus/octg-pipe
```

Swap this for a real target page before expecting meaningful results. The flow is intentionally structured so the browser step can help you understand page layout before the extraction step normalizes listings.

## Next step: outreach email agent

Once scraping produces reliable rows, add an outreach stage:

1. Filter rows with useful inventory and a public `contact_email`.
2. Deduplicate by company, grade, size, and source URL.
3. Generate a short supplier inquiry email asking for availability, MTRs, condition, location, price, and photos.
4. Save drafts first, then send only after manual review.
5. Consider using Composio or Gmail API auth so the agent can create drafts without storing email credentials in this repo.

Keep scraping and outreach separate at first. It will make testing, compliance, and supplier follow-up much easier.
