 Realty Q3 Sales Data Cleaning & Dashboard

Project Overview
Built an automated data cleaning pipeline and interactive Tableau dashboard for a real estate company's Q3 sales data.

#### What I Did
1. Data Generation: Created a Python script to generate 500 rows of realistic messy data with multiple formatting issues
2. Data Cleaning: Built an automated pipeline using pandas to:
   - Standardize 5 different date formats
   - Convert text-values ("Three", "450k") to numeric
   - Flag impossible values (negative sq.ft) without deleting data
   - Fix email typos
3. Quality Audit: Generated an Excel file with a "Problem IDs" sheet for business review
4. Tableau Dashboard: Built an interactive dashboard showing:
   - Monthly commission trends
   - Agent performance rankings
   - Filterable by date

Key Insight
Identified that while total Q3 revenue grew, per-agent productivity declined during the merger transition.

## Tools Used
- Python (pandas, numpy)
- Tableau
- Excel

Development Workflow
This project was built using an AI-assisted development workflow. 
- I designed the data architecture, business logic, and cleaning strategy.
- I used AI (LLMs) to accelerate syntax generation and debug edge cases.
- I manually verified every output, caught data anomalies (like the 2-digit year issue), and extracted the final business insights.

This reflects my actual working style: leveraging modern tools to deliver high-quality results faster, while maintaining strict quality control and business logic oversight.
