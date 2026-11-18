# Autonomous Due Diligence Multi-Agent Pipeline

## Overview
An automated, multi-agent intelligence pipeline designed to execute 15-point startup due diligence with zero manual intervention. Built to compress the research cycle for Founder's Office and strategic operations roles, this system synthesizes financial health, unit economics, brand sentiment (Kapferer’s Prism), and operational bottlenecks into executive-ready markdown reports.

## Architecture: Master-Sub Routing Protocol
Standard single-agent LLM prompts fail at complex diligence due to context dilution and API serialization limits. This architecture solves that bottleneck via a Master-Sub routing model.

1. **Master Orchestrator:** Ingests the target company and industry, acting as the central router.
2. **Financial Intelligence Agent:** Scrapes and extracts hard numeric metrics (Gross Margins, AOV, Payback Periods, CapEx).
3. **Brand Sentiment Agent:** Executes targeted Reddit scrapes and maps verbatim consumer quotes directly into a Kapferer Brand Identity Prism.
4. **Career Fit Agent:** Cross-references the target company's scaling challenges against specific operator backgrounds (e.g., 0-to-1 food venture execution, CRM retention mechanics) to evaluate direct role viability.

*(View the n8n node architecture in the `/architecture` folder).*

## Engineering Constraints & Solutions
* **API Quota Management:** Transitioned from speed-optimized free-tier models to strict Pro-tier execution to maintain complex markdown table formatting and prevent structural fracturing.
* **Hallucination Suppression:** Implemented strict negative constraints to prevent data fabrication. If the Career Agent cannot scrape a live job description, it is hard-coded to state the deficit rather than hallucinate generalized salary brackets.
* **Spatial Formatting:** Forced the LLM to embed verbatim quotes and URLs directly into table matrices rather than generating unstructured lists.

## Output
Review the generated intelligence payload in the `/reports` folder:
* [Swish (Food Delivery) - Due Diligence Report](./reports/sample_report_swish.md)
