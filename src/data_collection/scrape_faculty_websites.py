"""
Faculty Website Scraper
Issue #5: Extract research information from faculty websites

This script visits individual faculty websites to extract research descriptions,
interests, publications, and lab information.

Dependencies:
    pip install playwright beautifulsoup4 lxml requests trafilatura
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import re


def load_faculty_roster() -> Dict:
    """Load the faculty roster created in Issue #4."""
    try:
        with open('data/faculty_roster.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback to FIS data if roster not yet created
        with open('data/faculty_from_fis.json', 'r') as f:
            return json.load(f)


def extract_research_info_playwright(url: str, faculty_name: str) -> Dict:
    """
    Extract research information from a faculty website using Playwright MCP.

    Args:
        url: URL of faculty personal/lab website
        faculty_name: Name of faculty member (for validation)

    Returns:
        Dictionary with extracted research information

    Note:
        In a Claude Code session with Playwright MCP, you would use:
        "Navigate to {url} and extract research description, interests, publications, and lab info"
    """

    print(f"[PLAYWRIGHT MCP] Navigating to: {url}")
    print(f"[PLAYWRIGHT MCP] Extracting research content for: {faculty_name}")

    # Placeholder for Playwright MCP interaction
    research_data = {
        'website_url': url,
        'research_description': None,
        'research_keywords': [],
        'research_areas': [],
        'lab_name': None,
        'lab_website': None,
        'cv_url': None,
        'publications_listed': [],
        'courses_taught': [],
        'graduate_students': [],
        'funding_sources': [],
        'last_updated': None,
        'extraction_success': False,
        'extraction_method': 'playwright_mcp',
        'extraction_date': datetime.now().isoformat()
    }

    # Expected extraction tasks:
    # 1. Find main research description (usually in <p> tags, specific divs)
    # 2. Extract research interests/keywords (often bullet lists)
    # 3. Look for lab/group name
    # 4. Find CV/resume links (PDFs)
    # 5. Extract publication lists if present
    # 6. Note any course listings
    # 7. Identify funding sources (NIH, NSF grants mentioned)

    return research_data


def extract_text_with_trafilatura(html_content: str) -> str:
    """
    Extract main content from HTML using trafilatura library.

    This is a backup method for pages that don't require JavaScript.
    """
    try:
        import trafilatura
        text = trafilatura.extract(html_content)
        return text if text else ""
    except ImportError:
        print("Warning: trafilatura not installed. Install with: pip install trafilatura")
        return ""


def extract_keywords_from_text(text: str) -> List[str]:
    """Extract research keywords from text using pattern matching."""
    keywords = []

    # Common patterns for research interests sections
    patterns = [
        r'research interests?:?\s*(.+?)(?:\n\n|\.|$)',
        r'interests?:?\s*(.+?)(?:\n\n|\.|$)',
        r'keywords?:?\s*(.+?)(?:\n\n|\.|$)',
        r'areas?:?\s*(.+?)(?:\n\n|\.|$)',
    ]

    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            content = match.group(1)
            # Split by common delimiters
            items = re.split(r'[,;•·\n]', content)
            keywords.extend([item.strip() for item in items if item.strip()])

    # Remove duplicates while preserving order
    seen = set()
    unique_keywords = []
    for kw in keywords:
        kw_lower = kw.lower()
        if kw_lower not in seen and len(kw) > 2:
            seen.add(kw_lower)
            unique_keywords.append(kw)

    return unique_keywords[:20]  # Limit to top 20


def extract_cv_links(html_content: str, base_url: str) -> Optional[str]:
    """Find CV/resume PDF links in HTML."""
    cv_patterns = [
        r'href="([^"]*(?:cv|resume|vitae)[^"]*\.pdf)"',
        r'href="([^"]*CV[^"]*\.pdf)"',
    ]

    for pattern in cv_patterns:
        matches = re.finditer(pattern, html_content, re.IGNORECASE)
        for match in matches:
            cv_url = match.group(1)
            # Make absolute URL if relative
            if not cv_url.startswith('http'):
                from urllib.parse import urljoin
                cv_url = urljoin(base_url, cv_url)
            return cv_url

    return None


def process_faculty_website(faculty: Dict) -> Dict:
    """
    Process a single faculty member's website.

    Args:
        faculty: Faculty dictionary with at least 'website' and 'name'

    Returns:
        Enriched faculty dictionary with research information
    """
    if not faculty.get('website'):
        return {
            **faculty,
            'website_data': {
                'extraction_success': False,
                'reason': 'no_website_url'
            }
        }

    try:
        # Use Playwright MCP to extract research info
        research_info = extract_research_info_playwright(
            faculty['website'],
            faculty['name']
        )

        # Merge research info into faculty record
        enriched = {
            **faculty,
            'website_data': research_info
        }

        return enriched

    except Exception as e:
        print(f"Error processing {faculty['name']}: {str(e)}")
        return {
            **faculty,
            'website_data': {
                'extraction_success': False,
                'error': str(e)
            }
        }


def categorize_research_areas(keywords: List[str]) -> List[str]:
    """Categorize research keywords into broad areas."""
    categories = {
        'machine_learning': ['machine learning', 'deep learning', 'neural network', 'ai', 'artificial intelligence'],
        'biomedical': ['biomedical', 'medical', 'clinical', 'health', 'disease'],
        'robotics': ['robot', 'robotic', 'automation', 'autonomous'],
        'materials': ['material', 'polymer', 'composite', 'nanomaterial'],
        'energy': ['energy', 'renewable', 'solar', 'battery', 'fuel cell'],
        'computing': ['computing', 'software', 'algorithm', 'data'],
        'imaging': ['imaging', 'vision', 'image processing', 'visualization'],
        'control': ['control', 'optimization', 'system'],
    }

    identified = []
    kw_lower = [k.lower() for k in keywords]

    for category, terms in categories.items():
        if any(term in ' '.join(kw_lower) for term in terms):
            identified.append(category)

    return identified


def generate_website_scraping_report(faculty_data: List[Dict]) -> str:
    """Generate summary report of website scraping."""
    total = len(faculty_data)
    with_websites = len([f for f in faculty_data if f.get('website')])
    successful = len([f for f in faculty_data if f.get('website_data', {}).get('extraction_success')])

    with_descriptions = len([f for f in faculty_data
                            if f.get('website_data', {}).get('research_description')])
    with_keywords = len([f for f in faculty_data
                        if f.get('website_data', {}).get('research_keywords')])
    with_cv = len([f for f in faculty_data
                  if f.get('website_data', {}).get('cv_url')])

    report = f"""
=== Faculty Website Scraping Summary (Issue #5) ===

Total Faculty: {total}
With Website URLs: {with_websites} ({with_websites/total*100:.1f}%)
Successful Extractions: {successful} ({successful/with_websites*100:.1f}% of those with websites)

Content Extracted:
  Research Descriptions: {with_descriptions}
  Research Keywords: {with_keywords}
  CV/Resume Links: {with_cv}

Extraction Rate by Department:
"""

    # Count by department
    dept_stats = {}
    for f in faculty_data:
        dept = f.get('department_code', 'unknown')
        if dept not in dept_stats:
            dept_stats[dept] = {'total': 0, 'with_website': 0, 'extracted': 0}

        dept_stats[dept]['total'] += 1
        if f.get('website'):
            dept_stats[dept]['with_website'] += 1
        if f.get('website_data', {}).get('extraction_success'):
            dept_stats[dept]['extracted'] += 1

    for dept, stats in sorted(dept_stats.items()):
        rate = (stats['extracted'] / stats['with_website'] * 100) if stats['with_website'] > 0 else 0
        report += f"  {dept}: {stats['extracted']}/{stats['with_website']} ({rate:.1f}%)\n"

    return report


def save_enriched_roster(faculty_data: List[Dict], output_path: str):
    """Save the enriched faculty roster with website data."""
    output = {
        'metadata': {
            'created_date': datetime.now().isoformat(),
            'data_sources': [
                'FIS_All_Tenured_TT.xlsx',
                'web_scraping_faculty_listings',
                'web_scraping_faculty_websites'
            ],
            'total_faculty': len(faculty_data),
            'issues': ['#16 - FIS Data', '#4 - Faculty Listings', '#5 - Faculty Websites']
        },
        'faculty': faculty_data
    }

    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nSaved enriched roster to: {output_path}")


def main():
    """Main workflow for Issue #5."""
    print("=== Faculty Website Scraper (Issue #5) ===\n")

    # Load faculty roster
    roster = load_faculty_roster()
    faculty_list = roster['faculty']

    print(f"Loaded {len(faculty_list)} faculty members\n")

    # Filter for faculty with websites
    with_websites = [f for f in faculty_list if f.get('website')]
    print(f"Faculty with website URLs: {len(with_websites)}\n")

    # Process each faculty website
    enriched_faculty = []
    for i, faculty in enumerate(faculty_list, 1):
        print(f"[{i}/{len(faculty_list)}] Processing: {faculty['name']}")

        if faculty.get('website'):
            enriched = process_faculty_website(faculty)
            enriched_faculty.append(enriched)

            # Rate limiting - be respectful
            time.sleep(3)
        else:
            print(f"  → No website URL, skipping")
            enriched_faculty.append(faculty)

    # Save enriched data
    save_enriched_roster(enriched_faculty, 'data/faculty_enriched.json')

    # Generate report
    report = generate_website_scraping_report(enriched_faculty)
    print(report)

    # Save report
    with open('data/website_scraping_report.txt', 'w') as f:
        f.write(report)

    print("\n=== Website Scraping Complete ===")


if __name__ == '__main__':
    main()


# PLAYWRIGHT MCP USAGE NOTES:
# ============================
#
# To actually run this script with Playwright MCP:
#
# 1. Ensure Issue #4 is complete (faculty roster with website URLs)
# 2. Start Claude Code session with Playwright MCP active
# 3. Modify extract_research_info_playwright() to use natural language:
#
#    "Navigate to {url} using Playwright and:
#     1. Extract the main research description text
#     2. Find research interests/keywords (often in bullet lists)
#     3. Look for lab or group name
#     4. Find any CV/resume PDF links
#     5. Extract publication lists if present
#     6. Note courses taught if listed
#     7. Identify funding sources mentioned (NSF, NIH grants)
#     Return as a structured dictionary"
#
# 4. The script will handle:
#    - Rate limiting (3 second delays)
#    - Error handling
#    - Progress tracking
#    - Data merging with existing faculty records
#
# 5. Output: data/faculty_enriched.json with full research information
