# Implementation Issues Summary

**Created:** 2025-11-04
**Total Issues:** 16
**GitHub Repository:** https://github.com/vanderbilt-data-science/grant-match

## Overview

This document summarizes all GitHub issues created for the faculty research profile generation project. Issues are organized by category and execution phase.

---

## Phase 1: Setup & Infrastructure (Issues #1-2)

### Issue #1: Install and configure MCP server for web navigation
**Priority:** High
**Dependencies:** None

Install and configure a Model Context Protocol (MCP) server (Puppeteer or Playwright) to enable automated web navigation and data extraction from Vanderbilt University websites.

**Key Tasks:**
- Research and select appropriate MCP server
- Install and configure for Vanderbilt websites
- Test basic navigation and content extraction
- Document setup process

---

### Issue #2: Configure development environment and API access
**Priority:** High
**Dependencies:** None

Set up Python environment with all necessary dependencies and obtain API credentials for data collection and AI processing.

**Key Tasks:**
- Create requirements.txt
- Configure .env template
- Obtain and test Anthropic API key
- Research ORCID, arXiv, Semantic Scholar APIs
- Document rate limits and best practices

---

## Phase 2: Research & Discovery (Issues #3, #16)

### Issue #3: Map Vanderbilt Engineering department structure and faculty pages
**Priority:** High
**Dependencies:** Issue #1 (MCP setup)

Document the organizational structure of Vanderbilt School of Engineering and identify all department faculty listing pages.

**Key Tasks:**
- Identify all engineering departments
- Document URL structure for faculty pages
- Identify HTML patterns and page variations
- Create department inventory (JSON)

**Deliverable:** `data/department_inventory.json`

---

### Issue #16: Extract and analyze FIS faculty data
**Priority:** High
**Dependencies:** Issue #2 (Environment setup)

Analyze the existing `FIS_All_Tenured_TT.xlsx` file to extract Engineering faculty information and assess data coverage, especially ORCID IDs.

**Key Tasks:**
- Load and analyze Excel structure
- Filter for School of Engineering
- Extract names, departments, ORCID IDs, emails
- Assess data quality and completeness
- Export cleaned faculty list

**Deliverable:** `data/faculty_from_fis.json`

---

## Phase 3: Data Collection (Issues #4-7)

### Issue #4: Scrape faculty listings from department pages
**Priority:** High
**Dependencies:** Issues #1, #3

Automatically extract faculty information from all School of Engineering department websites.

**Key Tasks:**
- Design faculty data structure
- Write scraper for department pages
- Handle different page layouts
- Extract: name, title, department, email, website URL
- Implement error handling and rate limiting

**Deliverable:** `data/faculty_roster.json`

---

### Issue #5: Extract research information from faculty websites
**Priority:** Medium
**Dependencies:** Issues #1, #4

Scrape individual faculty websites to collect research descriptions, interests, publications, and lab information.

**Key Tasks:**
- Navigate to each faculty website
- Extract research descriptions and keywords
- Find publication lists and CV links
- Handle various website formats
- Parse PDF CVs if found

**Deliverable:** `data/faculty_websites/{faculty_id}.json`

---

### Issue #6: Search preprint repositories for faculty publications
**Priority:** Medium
**Dependencies:** Issues #2, #4

Search arXiv, bioRxiv, and other preprint repositories to find recent publications by Engineering faculty.

**Key Tasks:**
- Implement arXiv and bioRxiv search
- Search by author name and affiliation
- Filter for last 3-5 years
- Handle name disambiguation
- Deduplicate across repositories

**Deliverable:** `data/preprints/{faculty_id}.json`

---

### Issue #7: Retrieve publication data via ORCID and scholarly APIs
**Priority:** High
**Dependencies:** Issues #2, #4

Collect comprehensive publication records using ORCID (if available) and scholarly APIs like Semantic Scholar, CrossRef, or OpenAlex.

**Key Tasks:**
- Query ORCID API for faculty with IDs
- Search Semantic Scholar/OpenAlex for others
- Fetch full publication metadata and abstracts
- Deduplicate publications across sources
- Prioritize recent publications (last 5 years)

**Deliverable:** `data/publications/{faculty_id}.json`

---

## Phase 4: Profile Generation (Issues #8-10)

### Issue #8: Define research profile data structure and schema
**Priority:** High
**Dependencies:** None (can start early)

Design a standardized data structure for faculty research profiles that supports both AI generation and grant matching.

**Key Tasks:**
- Define profile schema (JSON)
- Identify required vs. optional fields
- Create validation rules
- Design versioning strategy
- Document schema comprehensively

**Deliverable:** `docs/profile_schema.md` and JSON schema file

---

### Issue #9: Design and test profile generation prompts
**Priority:** High
**Dependencies:** Issues #2, #7, #8

Create high-quality prompts for generating faculty research profiles using Claude API, with emphasis on specificity and accuracy.

**Key Tasks:**
- Design initial prompt template
- Test on 5 diverse faculty examples
- Evaluate: specificity, accuracy, comprehensiveness
- Iterate based on test results
- Create prompt variants for different data scenarios
- Document examples of good vs. bad outputs

**Deliverable:** `src/prompts/profile_generation.py`

---

### Issue #10: Build automated profile generation pipeline
**Priority:** High
**Dependencies:** Issues #2, #7, #8, #9 (+ #5 recommended)

Implement an automated pipeline that generates research profiles for all Engineering faculty using AI and collected data.

**Key Tasks:**
- Create profile generation script
- Aggregate all data sources per faculty
- Call Claude API with generation prompt
- Validate and score output quality
- Implement batch processing with progress tracking
- Handle errors and rate limits
- Generate summary report

**Deliverable:** `data/profiles/{faculty_id}.json` for all faculty

---

## Phase 5: Validation & Refinement (Issues #11-12)

### Issue #11: Manual review and quality assessment of generated profiles
**Priority:** High
**Dependencies:** Issue #10

Conduct thorough manual review of generated profiles to ensure accuracy, quality, and fitness for grant matching.

**Key Tasks:**
- Select 10-15 representative profiles
- Verify accuracy against websites and CVs
- Create quality rubric (1-5 scale)
- Document issues by type and severity
- Generate validation report
- Identify patterns for improvement

**Deliverable:** Validation report with quality ratings

---

### Issue #12: Improve profiles based on validation feedback
**Priority:** High
**Dependencies:** Issues #9, #10, #11

Refine the profile generation process based on validation findings to improve quality and accuracy.

**Key Tasks:**
- Review validation report
- Categorize issues by root cause
- Update prompts and data processing
- Regenerate poor/adequate profiles
- Re-validate improvements
- Iterate until quality targets met (avg ≥4.0/5)

**Success Metric:** Average quality score ≥4.0/5, ≥80% rated Good or Excellent

---

## Phase 6: Documentation & Demo (Issues #13-14)

### Issue #13: Create comprehensive profile dataset documentation
**Priority:** Medium
**Dependencies:** Issues #10, #11

Document the faculty research profile dataset thoroughly for future use, maintenance, and demo presentations.

**Key Tasks:**
- Document data collection methodology
- Create data dictionary
- Generate dataset statistics
- Document data provenance
- Define ethical guidelines
- Create changelog for updates

**Deliverable:** `docs/data_documentation.md`

---

### Issue #14: Create profile showcase interface
**Priority:** Medium
**Dependencies:** Issues #10, #12 (recommended)

Build a simple interface (likely Streamlit) to showcase generated faculty research profiles for demo purposes.

**Key Tasks:**
- Design demo interface (Streamlit recommended)
- Implement profile viewer with navigation
- Add search and filtering
- Create statistics dashboard
- Make presentable for stakeholders
- Prepare demo script

**Deliverable:** `src/demo/profile_viewer.py`

---

## Project Management

### Issue #15: Create implementation roadmap and milestones
**Priority:** High
**Dependencies:** All issues (organizational)

Organize all issues into a clear implementation roadmap with milestones and dependencies.

**Proposed Milestones:**
1. **Development Environment Ready** (Week 1) - Issues #1-2
2. **Data Collection Complete** (Weeks 1-2) - Issues #3-7, #16
3. **Profile Generation Working** (Week 2) - Issues #8-10
4. **Validation & Refinement** (Week 3) - Issues #11-12
5. **Demo Ready** (Week 3) - Issues #13-14

**Estimated Timeline:** ~3 weeks

---

## Quick Reference

### Critical Path (Must be Sequential)
1. MCP/API Setup (#1, #2)
2. Department Mapping (#3)
3. Faculty Roster (#4, #16)
4. Data Collection (#5, #6, #7)
5. Profile Generation (#8, #9, #10)
6. Validation (#11)
7. Refinement (#12)
8. Documentation & Demo (#13, #14)

### Can Be Done in Parallel
- Schema design (#8) while collecting data
- Prompt design (#9) with sample data
- Website (#5), Preprint (#6), Publication (#7) collection
- Documentation (#13) and Demo (#14) at the end

### High Priority (Blocking)
- #1 - MCP setup
- #2 - Environment setup
- #4 - Faculty scraping
- #7 - Publication data
- #8 - Profile schema
- #9 - Prompt design
- #10 - Profile generation
- #11 - Validation
- #12 - Refinement
- #16 - FIS data analysis

### Medium Priority (Valuable)
- #3 - Department mapping
- #5 - Website scraping
- #6 - Preprint search
- #13 - Documentation
- #14 - Demo interface

---

## Success Criteria

**Data Collection:**
- Faculty data for 80%+ of Engineering faculty
- Publication data for 80%+ with abstracts
- ORCID coverage documented

**Profile Generation:**
- Profiles generated for all faculty with sufficient data
- Average quality score ≥4.0/5
- ≥80% rated Good (4) or Excellent (5)
- 0 hallucinated content
- Specific citations to real publications

**Demo Readiness:**
- 80+ high-quality profiles
- Demo interface functional
- Documentation complete
- Ready to present to stakeholders

---

## Next Steps

1. **Review Issues:** Read through all issue details on GitHub
2. **Organize Milestones:** Implement the roadmap from Issue #15
3. **Start Execution:** Begin with Issues #1 and #2 (setup)
4. **Track Progress:** Update issues as work progresses
5. **Iterate:** Refine approach based on learnings

**Repository:** https://github.com/vanderbilt-data-science/grant-match/issues

---

**Document Status:** Ready for implementation
**Last Updated:** 2025-11-04
