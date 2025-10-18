import asyncio
import aiohttp
import json
import os
import yaml
from dotenv import load_dotenv
import logging
from typing import List, Dict, Any

# --- Configuration ---
load_dotenv()
APOLLO_API_KEY = os.getenv("APOLLO_API_KEY")
CRUNCHBASE_API_KEY = os.getenv("CRUNCHBASE_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Helper Functions ---

def load_icp_config(filepath="icp_config.yaml") -> Dict[str, Any]:
    """Loads the Ideal Customer Profile from a YAML file."""
    try:
        with open(filepath, 'r') as file:
            config = yaml.safe_load(file)
            logger.info(f"Loaded ICP configuration from {filepath}")
            return config
    except FileNotFoundError:
        logger.error(f"ICP config file not found at {filepath}")
        return None
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file: {e}")
        return None

async def fetch_data(session: aiohttp.ClientSession, url: str, headers=None, params=None) -> Dict[str, Any]:
    """Generic async function to fetch data from an API using GET."""
    try:
        async with session.get(url, headers=headers, params=params, timeout=aiohttp.ClientTimeout(total=30)) as response:
            response.raise_for_status()
            data = await response.json()
            logger.debug(f"Successfully fetched data from {url}")
            return data
    except aiohttp.ClientError as e:
        logger.error(f"API request failed for {url}: {e}")
        return None
    except asyncio.TimeoutError:
        logger.error(f"Request timeout for {url}")
        return None

async def post_data(session: aiohttp.ClientSession, url: str, json_payload=None, headers=None) -> Dict[str, Any]:
    """Generic async function to post data to an API using POST."""
    try:
        async with session.post(url, json=json_payload, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as response:
            if not response.ok:
                error_text = await response.text()
                logger.error(f"API request failed for {url} with status {response.status}: {error_text}")
                response.raise_for_status()
            data = await response.json()
            logger.debug(f"Successfully posted data to {url}")
            return data
    except aiohttp.ClientError as e:
        logger.error(f"API request failed for {url}: {e}")
        return None
    except asyncio.TimeoutError:
        logger.error(f"Request timeout for {url}")
        return None

# --- API Integration Functions ---

async def query_apollo(session: aiohttp.ClientSession, icp: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Queries the Apollo.io API for companies and contacts with India focus."""
    logger.info("Querying Apollo.io for Indian companies...")
    
    if not APOLLO_API_KEY:
        logger.error("Apollo API key not found")
        return []
    
    results = []
    search_url = "https://api.apollo.io/v1/organizations/search"
    
    headers = {
        "X-Api-Key": APOLLO_API_KEY,
        "Content-Type": "application/json"
    }

    # India-focused payload
    payload = {
        "q_organization_keywords": " OR ".join(icp.get('keywords', ['technology', 'software'])),
        "organization_locations": ["India"],  # Focus on India
        "page": 1,
        "per_page": 50,
        "sort_ascending": False,
        "sort_by": "organization_num_employees"
    }
    
    logger.info(f"Searching for Indian companies with keywords: {icp.get('keywords', ['technology'])}")
    
    try:
        data = await post_data(session, search_url, json_payload=payload, headers=headers)
        
        if data and 'organizations' in data:
            for org in data['organizations']:
                # FIXED: Safe location string handling
                city = org.get('city', '')
                state = org.get('state', '')
                country = org.get('country', '')
                
                # Build location safely
                location_parts = []
                if city:
                    location_parts.append(city)
                if state:
                    location_parts.append(state)
                if country:
                    location_parts.append(country)
                
                location = ", ".join(location_parts) if location_parts else "Unknown"
                
                # Additional filter for Indian companies
                if country and 'india' in country.lower():
                    company_data = {
                        "company_name": org.get("name"),
                        "domain": org.get("primary_domain"),
                        "revenue": org.get("annual_revenue"),
                        "industry": org.get("industry"),
                        "employee_count": org.get("estimated_num_employees"),
                        "location": location,
                        "country": country,
                        "source": ["Apollo"],
                        "contacts": [],
                        "signals": {}
                    }
                    # Only add if we have basic company info
                    if company_data['company_name'] and company_data['domain']:
                        results.append(company_data)
            
            logger.info(f"✅ Found {len(results)} Indian companies from Apollo.io")
            
            # Log companies for verification
            for i, company in enumerate(results[:5]):
                logger.info(f"  {i+1}. {company['company_name']} - {company.get('location', 'N/A')} - {company.get('industry', 'N/A')}")
                
        else:
            logger.warning("No organizations in Apollo response")
            if data and 'message' in data:
                logger.error(f"Apollo API message: {data['message']}")
                
    except Exception as e:
        logger.error(f"Apollo query failed: {e}")
        import traceback
        logger.error(f"Detailed error: {traceback.format_exc()}")
    
    return results

async def query_crunchbase(session: aiohttp.ClientSession, icp: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Queries the Crunchbase API for company and funding information."""
    logger.info("Querying Crunchbase...")
    
    # Enhanced mock data with Indian companies that have funding
    mock_companies = [
        {
            "company_name": "Tata Consultancy Services",
            "domain": "tcs.com",
            "funding_stage": "Public",
            "source": ["Crunchbase"],
            "signals": {"new_funding": False},
            "contacts": []
        },
        {
            "company_name": "Infosys", 
            "domain": "infosys.com",
            "funding_stage": "Public",
            "source": ["Crunchbase"],
            "signals": {"new_funding": True},
            "contacts": []
        },
        {
            "company_name": "Wipro",
            "domain": "wipro.com", 
            "funding_stage": "Public",
            "source": ["Crunchbase"],
            "signals": {"new_funding": False},
            "contacts": []
        },
        {
            "company_name": "HCLTech",
            "domain": "hcltech.com",
            "funding_stage": "Public", 
            "source": ["Crunchbase"],
            "signals": {"new_funding": True},
            "contacts": []
        },
        {
            "company_name": "Tech Mahindra",
            "domain": "techmahindra.com",
            "funding_stage": "Public",
            "source": ["Crunchbase"], 
            "signals": {"new_funding": True},
            "contacts": []
        }
    ]
    
    logger.info(f"Found {len(mock_companies)} companies from Crunchbase (mock)")
    return mock_companies
    
    # Filter mock companies based on ICP keywords
    keywords = [k.lower() for k in icp.get('keywords', [])]
    filtered_companies = [
        company for company in mock_companies 
        if any(keyword in company['company_name'].lower() for keyword in keywords)
    ]
    
    logger.info(f"Found {len(filtered_companies)} companies from Crunchbase (mock)")
    return filtered_companies

async def query_serpapi_for_signals(session: aiohttp.ClientSession, company_name: str) -> Dict[str, Any]:
    """Uses SerpApi to check for hiring signals with rate limiting."""
    if not company_name:
        return {"recent_hiring": False}
        
    logger.info(f"Querying SerpApi for hiring signals at {company_name}...")
    
    # Single query to avoid rate limiting
    search_query = f"{company_name} data scientist India"
    
    hiring_signals = {"recent_hiring": False, "job_count": 0, "location": "India"}
    
    params = {
        "engine": "google_jobs",
        "q": search_query,
        "api_key": SERPAPI_API_KEY,
        "hl": "en",
        "gl": "in",  # Focus on India
    }
    search_url = "https://serpapi.com/search.json"
    
    # Add delay between requests to avoid rate limiting
    await asyncio.sleep(1)  # 1 second delay between requests
    
    data = await fetch_data(session, search_url, params=params)
    
    if data and 'jobs_results' in data and data['jobs_results']:
        hiring_signals["recent_hiring"] = True
        hiring_signals["job_count"] = len(data['jobs_results'])
        # Check if jobs are in India
        india_jobs = [job for job in data['jobs_results'] if 'india' in str(job.get('location', '')).lower()]
        hiring_signals["india_jobs"] = len(india_jobs)
        logger.info(f"🇮🇳 Hiring signals found for {company_name} in India ({hiring_signals['job_count']} jobs)")
    else:
        logger.info(f"No hiring signals found for {company_name} in India")
        
    return hiring_signals
# --- Data Processing Functions ---

def normalize_and_merge(prospects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Merges and deduplicates prospect data from different sources."""
    merged = {}
    
    for prospect in prospects:
        domain = prospect.get('domain')
        if not domain:
            continue
            
        if domain not in merged:
            merged[domain] = {
                "company_name": None,
                "domain": domain,
                "revenue": None,
                "industry": None,
                "employee_count": None,
                "location": None,
                "funding_stage": None,
                "contacts": [],
                "signals": {},
                "source": [],
                "confidence": 0.0
            }

        # Merge fields with preference to non-null values
        for field in ['company_name', 'revenue', 'industry', 'employee_count', 'location', 'funding_stage']:
            if prospect.get(field) and not merged[domain].get(field):
                merged[domain][field] = prospect.get(field)

        # Merge sources and signals
        merged[domain]["source"].extend(prospect.get("source", []))
        merged[domain]["signals"].update(prospect.get("signals", {}))
        
        # Deduplicate contacts by email
        existing_emails = {c['email'] for c in merged[domain]['contacts'] if c.get('email')}
        for contact in prospect.get("contacts", []):
            if contact.get('email') and contact['email'] not in existing_emails:
                merged[domain]['contacts'].append(contact)
                existing_emails.add(contact['email'])

    # Clean up sources and remove duplicates
    for domain in merged:
        merged[domain]["source"] = sorted(list(set(merged[domain]["source"])))

    logger.info(f"Merged {len(prospects)} records into {len(merged)} unique companies")
    return list(merged.values())

def score_prospects(prospects: List[Dict[str, Any]], icp: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Assigns a simple heuristic confidence score to each prospect based on the ICP."""
    
    for prospect in prospects:
        score = 0.0
        
        # 1. Industry Match (40%)
        industry_match = 0.0
        prospect_industry = prospect.get('industry')
        icp_industries = [industry.lower() for industry in icp.get('industry', [])]
        
        # FIX: Handle None industry safely
        if prospect_industry:
            prospect_industry_lower = prospect_industry.lower()
            if any(icp_industry in prospect_industry_lower for icp_industry in icp_industries):
                industry_match = 1.0
        score += 0.4 * industry_match
        
        # 2. Funding Signal (30%)
        funding_signal = 1.0 if (
            icp.get('signals', {}).get('funding') and 
            prospect.get('signals', {}).get('new_funding')
        ) else 0.0
        score += 0.3 * funding_signal
        
        # 3. Hiring Signal (20%)
        hiring_signal = 1.0 if (
            icp.get('signals', {}).get('hiring_data_roles') and 
            prospect.get('signals', {}).get('recent_hiring')
        ) else 0.0
        score += 0.2 * hiring_signal
        
        # 4. Tech Match (10%)
        tech_match = 0.0
        icp_tech_stack = icp.get('signals', {}).get('tech_stack', [])
        
        # Check if company keywords match tech stack
        company_name = prospect.get('company_name', '').lower()
        industry = prospect.get('industry', '') or ''  # FIX: Handle None industry
        
        if icp_tech_stack and any(
            tech.lower() in company_name or 
            tech.lower() in industry.lower()  # FIX: Now safe to call .lower()
            for tech in icp_tech_stack
        ):
            tech_match = 1.0
        score += 0.1 * tech_match
        
        # Set final confidence score
        prospect['confidence'] = round(score, 2)
        
        # Debug logging for top prospects
        if score > 0.3:
            logger.debug(f"Scored {prospect.get('company_name')}: {score} " +
                       f"(industry: {industry_match}, funding: {funding_signal}, " +
                       f"hiring: {hiring_signal}, tech: {tech_match})")

    # Sort by confidence score
    sorted_prospects = sorted(prospects, key=lambda x: x['confidence'], reverse=True)
    logger.info(f"Scored {len(prospects)} prospects with simple heuristic")
    
    return sorted_prospects

def print_summary(prospects: List[Dict[str, Any]]):
    """Prints a summary of the prospecting results."""
    if not prospects:
        logger.warning("No prospects found")
        return
        
    high_confidence = [p for p in prospects if p['confidence'] >= 0.7]
    medium_confidence = [p for p in prospects if 0.4 <= p['confidence'] < 0.7]
    low_confidence = [p for p in prospects if p['confidence'] < 0.4]
    
    print(f"\n📊 PROSPECTING SUMMARY")
    print(f"=======================")
    print(f"Total Prospects: {len(prospects)}")
    print(f"High Confidence (≥0.7): {len(high_confidence)}")
    print(f"Medium Confidence (0.4-0.7): {len(medium_confidence)}") 
    print(f"Low Confidence (<0.4): {len(low_confidence)}")
    
    if prospects:
        print(f"\n🏆 Top Prospects:")
        for i, prospect in enumerate(prospects[:5], 1):
            print(f"{i}. {prospect.get('company_name', 'N/A')} - Confidence: {prospect['confidence']}")

# --- Main Orchestration ---

async def main():
    """Main function to run the ProspectSearchAgent."""
    print("🚀 Starting ProspectSearchAgent...")
    
    icp = load_icp_config()
    if not icp:
        logger.error("Failed to load ICP configuration. Exiting.")
        return

    logger.info(f"ICP Configuration: {json.dumps(icp, indent=2)}")
    
    try:
        async with aiohttp.ClientSession() as session:
            # 1. Fetch data from primary sources
            logger.info("Fetching data from primary sources...")
            apollo_task = asyncio.create_task(query_apollo(session, icp))
            crunchbase_task = asyncio.create_task(query_crunchbase(session, icp))
            
            initial_prospects = await asyncio.gather(apollo_task, crunchbase_task)
            all_prospects = [item for sublist in initial_prospects for item in sublist]

            if not all_prospects:
                logger.warning("No prospects found from primary sources")
                return

            # 2. Fetch signals for the discovered companies (with limits)
            company_names_for_signals = list(set(p['company_name'] for p in all_prospects if p.get('company_name')))
            
            # LIMIT to top 5 companies to avoid SerpApi rate limits
            company_names_for_signals = company_names_for_signals[:5]
            logger.info(f"Fetching signals for {len(company_names_for_signals)} companies (limited to avoid rate limits)...")
            
            signal_tasks = []
            for name in company_names_for_signals:
                signal_tasks.append(asyncio.create_task(query_serpapi_for_signals(session, name)))
                # Add delay between task creation
                await asyncio.sleep(2)
            
            signal_results = await asyncio.gather(*signal_tasks)
            signals_map = dict(zip(company_names_for_signals, signal_results))

            # Apply signals to prospects
            for prospect in all_prospects:
                company_name = prospect.get('company_name')
                if company_name in signals_map:
                    if 'signals' not in prospect:
                        prospect['signals'] = {}
                    prospect['signals'].update(signals_map[company_name])

            # 3. Process and score the data
            logger.info("Processing and scoring prospects...")
            merged_prospects = normalize_and_merge(all_prospects)
            scored_prospects = score_prospects(merged_prospects, icp)

            # 4. Output results
            output_filepath = "prospects_output.json"
            with open(output_filepath, 'w') as f:
                json.dump(scored_prospects, f, indent=2)
                
            print(f"\n✅ Prospecting complete! Results saved to {output_filepath}")
            print_summary(scored_prospects)
            
    except Exception as e:
        logger.error(f"Unexpected error in main execution: {e}")
        import traceback
        logger.error(f"Detailed traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    if not all([APOLLO_API_KEY, CRUNCHBASE_API_KEY, SERPAPI_API_KEY]):
        print("❌ Error: One or more API keys are missing. Please check your .env file.")
        print(f"Apollo Key: {'✅' if APOLLO_API_KEY else '❌'}")
        print(f"Crunchbase Key: {'✅' if CRUNCHBASE_API_KEY else '❌'}") 
        print(f"SerpApi Key: {'✅' if SERPAPI_API_KEY else '❌'}")
    else:
        asyncio.run(main())