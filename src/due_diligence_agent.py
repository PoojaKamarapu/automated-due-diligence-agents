import os
import google.generativeai as genai
from duckduckgo_search import DDGS

# --- CONFIGURATION ---
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY" # Insert your key here
genai.configure(api_key=GEMINI_API_KEY)

# Use the Pro model for complex reasoning and formatting
MODEL_NAME = 'gemini-1.5-pro-latest' 

def perform_search(query, max_results=4):
    """Replaces Tavily: Uses DuckDuckGo to scrape the web for free."""
    try:
        results = DDGS().text(query, max_results=max_results)
        return "\n".join([f"Source: {res['href']}\nContent: {res['body']}" for res in results])
    except Exception as e:
        return f"Search failed: {e}"

def get_financials(company_name, industry, model):
    print(f"[*] Running Sub-Agent 1: Financials for {company_name}...")
    search_data = perform_search(f"{company_name} {industry} business model unit economics funding valuation")
    
    prompt = f"""
    Role: Financial Intelligence Agent.
    Target: {company_name} in the {industry} sector.
    
    Raw Web Data:
    {search_data}
    
    Task: Extract the founders' names, background, business model, unit economics, revenue drivers, cost/P&L metrics, and funding details.
    Constraint: You must extract hard numeric metrics. Return a highly detailed, multi-paragraph text analysis. Do not format as a final report; return raw, categorized intelligence.
    For Section 1 and 2, every strategic claim must be accompanied by a hard operational metric (e.g., margins, payback periods, SLA percentages, or order density numbers). Generalized summaries without numbers are prohibited.
    """
    response = model.generate_content(prompt)
    return response.text

def get_sentiment(company_name, industry, model):
    print(f"[*] Running Sub-Agent 2: Brand Sentiment for {company_name}...")
    search_data = perform_search(f"site:reddit.com {company_name} {industry} reviews complaints")
    
    prompt = f"""
    Role: Brand & Sentiment Agent.
    Target: {company_name} in the {industry} sector.
    
    Raw Reddit Data:
    {search_data}
    
    Task: Analyze the target's intended positioning versus the actual customer view using Kapferer's Brand Identity Prism.
    Constraint: Extract exact quotes and URLs. Exclude any data outside the target industry. Return detailed text analysis.
    Format the Kapferer analysis exclusively as a Markdown table with three columns: | Prism Facet | Intended Brand Identity | Actual Consumer Sentiment |. You MUST embed verbatim user quotes and URLs directly inside the Actual Consumer Sentiment column. You are strictly forbidden from placing quotes in an external list.
    """
    response = model.generate_content(prompt)
    return response.text

def get_career_fit(company_name, industry, model):
    print(f"[*] Running Sub-Agent 3: Career Fit for {company_name}...")
    search_data = perform_search(f"{company_name} {industry} Founder's Office Chief of Staff job operations")
    
    prompt = f"""
    Role: Executive Career Agent.
    Target: {company_name} in the {industry} sector.
    
    Raw Job/Operations Data:
    {search_data}
    
    Task: Evaluate the role requirements against the candidate's specific background: an Engineering degree, an MBA in General Management from Masters' Union, 0-to-1 operational execution (AAVIRI food truck), CRM management (Brooks Kitchen), and technical proficiency in n8n/Python AI agent pipelines.
    Constraint: Identify the candidate's exact strengths and weaknesses for this specific application. Return detailed text analysis.
    If you cannot find an active Founder's Office job posting for the target company, do not invent generalized industry salary benchmarks or use conversational hedging. You must state definitively: "Zero active Founder's Office listings currently detected via web crawl; analysis is modeled on cold-outreach positioning."
    """
    response = model.generate_content(prompt)
    return response.text

def master_orchestrator(company_name, industry):
    print(f"=== Initiating Due Diligence Pipeline for {company_name} ===\n")
    model = genai.GenerativeModel(MODEL_NAME)
    
    # Execute the three sub-agents sequentially
    financial_data = get_financials(company_name, industry, model)
    sentiment_data = get_sentiment(company_name, industry, model)
    career_data = get_career_fit(company_name, industry, model)
    
    print("[*] Sub-Agents completed. Master Orchestrator synthesizing final report...\n")
    
    master_prompt = f"""
    Role: Master Due Diligence Orchestrator.
    
    Payloads from Sub-Agents:
    --- FINANCIAL INTELLIGENCE ---
    {financial_data}
    
    --- BRAND SENTIMENT ---
    {sentiment_data}
    
    --- CAREER FIT ---
    {career_data}
    
    Task: Synthesize the combined data into a comprehensive, highly structured markdown report. Do not truncate, summarize away, or compress the findings. Render all sub-agent tables exactly as formatted without turning them into bullet points or altering their columns.
    
    Use the following exact structure:
    # Due Diligence & Career Fit Report: {company_name} ({industry})

    ## 1. Executive & Financial Summary
    ## 2. Competitive Landscape & Positioning
    ## 3. Consumer Sentiment (Reddit Quotes & Kapferer Prism)
    ## 4. Career Analysis (Founder's Office JD, Salary, and Profile Fit)
    """
    
    final_report = model.generate_content(master_prompt)
    
    # Save the report to a markdown file
    filename = f"{company_name.lower().replace(' ', '_')}_diligence_report.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(final_report.text)
        
    print(f"=== Pipeline Complete! Report saved to {filename} ===")
    return final_report.text

# --- EXECUTION ---
if __name__ == "__main__":
    target_company = "AI Accountant"
    target_industry = "B2B SaaS (Accounting Automation)"
    
    master_orchestrator(target_company, target_industry)
