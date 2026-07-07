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

Open `config.py` and update `TARGET_SITES`.

Start with public pages that already list inventory in a readable page, then validate each site's terms of use and robots guidance before running repeated scrapes.

Current starter targets:

- **KO Supply**: `https://kosupply.com/inventory/`
  - Visible data: OD, weight, grade, end finish, length, manufacturer, status, joints, quantity in feet, comments, and MTR availability.
  - Structure: static WordPress/wpDataTables inventory table. Rows are present in the HTML, so this should be the easiest first scraper target.
  - Selector hints: `#table_4 tbody tr[data-row-index]`; columns map directly to the table headers. No row-level price is shown publicly.
- **Surplus & Prime Worldwide**: `https://surplusandprime.com/product-category/oilfield-equipment/octg/`
  - Visible data: product title with size/grade/spec/quantity details, product category, starting bid, image, and product detail URL.
  - Structure: static WordPress/WooCommerce archive with paginated product cards. Detail pages may be needed for location and contact context.
  - Selector hints: `ul.products li.product`; links are under `a.woocommerce-LoopProduct-link` or `a.ast-loop-product__link`; pagination is `nav.woocommerce-pagination a.page-numbers`.
- **Salvex Pipe Trading**: `https://www.salvex.com/pipe/`
  - Visible data after rendering: asset title, category, region/location, quantity, condition, asking price or bid state, and seller/contact workflow.
  - Structure: Next.js/React app. Initial HTML contains the app shell and loading skeletons, so use browser-use or Playwright before extraction.
  - Selector hints: start broad with rendered nodes such as `[class*='product']`, `[class*='asset']`, or `[class*='listing']`, then tighten after a browser inspection run.

For each site:

1. Add or edit a `TargetSite` entry in `config.py`.
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

## Notes on target difficulty

Run KO Supply first because the table rows are available in page source. Surplus & Prime is also static, but the best extraction may combine archive cards with product detail pages. Salvex needs a rendered-browser pass before ScrapeGraphAI can see the listings.

## Next step: outreach email agent

Once scraping produces reliable rows, add an outreach stage:

1. Filter rows with useful inventory and a public `contact_email`.
2. Deduplicate by company, grade, size, and source URL.
3. Generate a short supplier inquiry email asking for availability, MTRs, condition, location, price, and photos.
4. Save drafts first, then send only after manual review.
5. Consider using Composio or Gmail API auth so the agent can create drafts without storing email credentials in this repo.

Keep scraping and outreach separate at first. It will make testing, compliance, and supplier follow-up much easier.
