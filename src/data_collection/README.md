# Data Collection Scripts

Scripts for collecting faculty information from Vanderbilt Engineering websites.

---

## Overview

These scripts implement the data collection pipeline for Issues #4 and #5:
- **Issue #4:** Scrape faculty listings from department pages
- **Issue #5:** Extract research information from individual faculty websites

Both scripts are designed to work with the Playwright MCP server installed in Issue #1.

---

## Scripts

### 1. `scrape_faculty_listings.py` (Issue #4)

**Purpose:** Extract faculty directory information from department listing pages.

**Inputs:**
- `data/department_inventory.json` (from Issue #3)
- `data/faculty_from_fis.json` (from Issue #16)

**Outputs:**
- `data/faculty_roster.json` - Enriched faculty roster
- `data/faculty_scraping_report.txt` - Summary report

**What it extracts:**
- Faculty names
- Titles and ranks
- Email addresses
- Phone numbers
- Office locations
- Personal/lab website URLs
- Profile page URLs
- Research interests (if listed)
- Faculty category (tenure-track, research, etc.)

**Workflow:**
1. Loads department inventory and FIS data
2. For each department's faculty page:
   - Uses Playwright MCP to navigate to the page
   - Waits for JavaScript content to load
   - Extracts all faculty information
   - Rate limits between requests
3. Matches scraped data with FIS data
4. Creates enriched faculty roster
5. Generates summary report

### 2. `scrape_faculty_websites.py` (Issue #5)

**Purpose:** Extract detailed research information from individual faculty websites.

**Inputs:**
- `data/faculty_roster.json` (from Issue #4) OR
- `data/faculty_from_fis.json` (fallback if #4 not complete)

**Outputs:**
- `data/faculty_enriched.json` - Fully enriched faculty data
- `data/website_scraping_report.txt` - Summary report

**What it extracts:**
- Research descriptions (main content)
- Research keywords and interests
- Lab/group names
- Lab website URLs
- CV/resume PDF links
- Publication lists (if on website)
- Courses taught
- Graduate students
- Funding sources (grants mentioned)
- Last updated dates

**Workflow:**
1. Loads faculty roster
2. For each faculty with a website URL:
   - Uses Playwright MCP to navigate to the site
   - Extracts research content
   - Parses and structures the information
   - Rate limits (3 seconds between requests)
3. Merges research data with faculty records
4. Generates enriched roster with all data
5. Creates summary report

---

## Usage with Playwright MCP

### Prerequisites

1. **Playwright MCP installed** (Issue #1 complete)
   ```bash
   claude mcp add npx @playwright/mcp@latest
   ```

2. **Python dependencies** (Issue #2)
   ```bash
   pip install beautifulsoup4 lxml trafilatura
   ```

3. **Data files** (Issues #3, #16)
   - `data/department_inventory.json`
   - `data/faculty_from_fis.json`

### Running the Scripts

**Option A: Via Claude Code (Recommended)**

Start a Claude Code session in this directory and use natural language:

```
"Run the faculty listing scraper (scrape_faculty_listings.py) using Playwright MCP
to extract faculty information from all department pages"
```

Claude Code will:
1. Execute the Python script
2. Use Playwright MCP for JavaScript-rendered pages
3. Handle browser automation automatically
4. Save results to `data/` directory

**Option B: Manual Execution with MCP Integration**

The scripts are structured to work with Claude Code's Playwright MCP. In the actual execution:

1. The `scrape_faculty_page_playwright()` and `extract_research_info_playwright()` functions will be replaced with Claude Code natural language commands
2. Claude Code will use the MCP to navigate and extract content
3. The rest of the script (matching, saving) will work as-is

### Example Session Flow

```
User: "Work on Issue #4 - scrape faculty listings"

Claude: I'll use the Playwright MCP to navigate to each department's faculty page
        and extract the faculty information.

        [Executes scrape_faculty_listings.py with Playwright MCP integration]

        Results:
        - Scraped 110 faculty from 6 departments
        - 98 matched with FIS data
        - 12 new faculty found on web not in FIS
        - 95% have personal website URLs
        - Saved to: data/faculty_roster.json
```

---

## Data Flow

```
Issue #16 (FIS Data)
    ↓
    data/faculty_from_fis.json (110 faculty, basic info)
    ↓
Issue #4 (Faculty Listings) ← data/department_inventory.json
    ↓
    data/faculty_roster.json (enriched with website URLs)
    ↓
Issue #5 (Faculty Websites)
    ↓
    data/faculty_enriched.json (fully enriched with research info)
    ↓
Issues #7-10 (Publication data, Profile generation)
```

---

## Script Structure

Both scripts follow a similar pattern:

```python
# 1. Load existing data
def load_department_inventory() -> Dict:
def load_fis_faculty() -> Dict:
def load_faculty_roster() -> Dict:

# 2. Scraping functions (use Playwright MCP)
def scrape_faculty_page_playwright(url, dept) -> List[Dict]:
def extract_research_info_playwright(url, name) -> Dict:

# 3. Data processing
def match_with_fis_data(scraped, fis) -> List[Dict]:
def process_faculty_website(faculty) -> Dict:

# 4. Output generation
def save_faculty_roster(data, path):
def generate_summary_report(data) -> str:

# 5. Main workflow
def main():
    # Load data
    # Scrape each source
    # Process and merge
    # Save results
    # Generate reports
```

---

## Rate Limiting

Both scripts implement rate limiting to be respectful of Vanderbilt's servers:

- **Faculty Listings:** 2 seconds between department pages
- **Faculty Websites:** 3 seconds between individual sites

Adjust these values in the `time.sleep()` calls if needed.

---

## Error Handling

The scripts handle common errors:

- Missing website URLs (skip gracefully)
- Network timeouts (log and continue)
- Parsing errors (save partial data)
- JavaScript loading failures (retry or mark as failed)

All errors are logged for manual review.

---

## Output Data Structures

### faculty_roster.json (Issue #4)

```json
{
  "metadata": {
    "created_date": "2025-11-04T...",
    "data_sources": ["FIS_All_Tenured_TT.xlsx", "web_scraping"],
    "total_faculty": 110,
    "issues": ["#16 - FIS Data", "#4 - Web Scraping"]
  },
  "faculty": [
    {
      "id": "faculty_123456",
      "name": "Dr. Jane Smith",
      "title": "Associate Professor",
      "department_code": "bme",
      "email": "jane.smith@vanderbilt.edu",
      "phone": "615-xxx-xxxx",
      "office": "FGH 123",
      "website": "https://engineering.vanderbilt.edu/~jsmith/",
      "profile_url": "https://engineering.vanderbilt.edu/people/...",
      "photo_url": "https://.../photo.jpg",
      "category": "Tenure / Tenure Track",
      "source_url": "https://engineering.vanderbilt.edu/people/biomedical-engineering/",
      "data_sources": ["FIS_All_Tenured_TT.xlsx", "web_scraping"]
    }
  ]
}
```

### faculty_enriched.json (Issue #5)

```json
{
  "metadata": {
    "created_date": "2025-11-04T...",
    "data_sources": [
      "FIS_All_Tenured_TT.xlsx",
      "web_scraping_faculty_listings",
      "web_scraping_faculty_websites"
    ],
    "total_faculty": 110
  },
  "faculty": [
    {
      "id": "faculty_123456",
      "name": "Dr. Jane Smith",
      ...
      "website_data": {
        "website_url": "https://...",
        "research_description": "Dr. Smith's research focuses on...",
        "research_keywords": ["neural interfaces", "brain-computer systems"],
        "research_areas": ["biomedical_engineering", "machine_learning"],
        "lab_name": "Neural Engineering Lab",
        "lab_website": "https://.../nel/",
        "cv_url": "https://.../cv.pdf",
        "publications_listed": [...],
        "funding_sources": ["NSF CAREER Award", "NIH R01"],
        "extraction_success": true,
        "extraction_date": "2025-11-04T..."
      }
    }
  ]
}
```

---

## Next Steps

After Issues #4 and #5 are complete:

1. **Issue #6:** Search preprint repositories (arXiv, bioRxiv)
2. **Issue #7:** Query ORCID and scholarly APIs for publications
3. **Issue #8:** Define research profile schema
4. **Issue #9:** Design AI profile generation prompts
5. **Issue #10:** Generate profiles using collected data

---

## Troubleshooting

### Playwright MCP not working

```bash
# Verify MCP installation
claude mcp list

# Reinstall if needed
claude mcp remove npx
claude mcp add npx @playwright/mcp@latest
```

### JavaScript content not loading

- Increase wait times in Playwright commands
- Check if page requires authentication
- Verify network connectivity

### No data extracted

- Check if URL structure has changed
- Verify CSS selectors are still valid
- Look at raw HTML to confirm content exists

### High failure rate

- Check robots.txt compliance
- Reduce rate limiting delays if too aggressive
- Verify website hasn't blocked automated access

---

## Notes

- Scripts are designed to resume from partial completion
- All intermediate data is saved for debugging
- Reports track success rates per department
- Failed extractions are logged for manual review
- Scripts can be run multiple times (idempotent where possible)

---

**Status:** Scripts created, ready for execution with Playwright MCP
**Last Updated:** 2025-11-04
**Issues:** #4, #5
