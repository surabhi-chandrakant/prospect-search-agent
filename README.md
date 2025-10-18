🚀 ProspectSearchAgent

A Python-based intelligent prospecting agent that automatically identifies potential Indian customers by querying multiple data sources and matching them against your Ideal Customer Profile (ICP).






🌟 Features

Multi-source Data Collection: Fetches company data from Apollo.io, Crunchbase, and SerpApi

India-Focused: Optimized for Indian company classifications and market patterns

ICP-based Filtering: Matches companies against configurable criteria

Simple Heuristic Scoring: Clear, interpretable confidence scores (0.0–1.0)

Signal Detection: Identifies buying signals like funding and hiring activity

Async Processing: Efficient parallel API calls for faster results

Smart Deduplication: Merges duplicate records from different data sources

📊 Latest Results (Production Ready)
📈 Prospecting Summary
Confidence Level	Range	Companies
High	≥ 0.7	3
Medium	0.4–0.7	14
Low	< 0.4	29

Total Prospects: 46 Indian Companies

🏆 Top Prospects
Company	Confidence	Description
Infosys	0.7	IT Services Leader
HCLTech	0.7	Technology Solutions
Tech Mahindra	0.7	Digital Transformation
Tata Consultancy Services	0.4	IT Giant
Wipro	0.4	Global IT Services
⚙️ Quick Start
🧩 Installation
git clone https://github.com/surabhi-chandrakant/prospect-search-agent.git
cd prospect-search-agent
pip install -r requirements.txt

⚙️ Configuration

Add your API keys to .env:

APOLLO_API_KEY=your_key_here
CRUNCHBASE_API_KEY=your_key_here
SERPAPI_API_KEY=your_key_here


Modify icp_config.yaml for your target market:

revenue_min: 1000000
revenue_max: 100000000
employee_count_min: 20
industry: ["Information Technology & Services", "IT Services", "Software"]
geography: ["INDIA"]
keywords: ["AI", "data analytics", "automation", "machine learning", "cloud"]
signals:
  funding: true
  hiring_data_roles: true
  tech_stack: ["Snowflake", "AWS", "Google Cloud", "Azure"]


Run the Agent:

python main.py

🎯 How It Works
🔄 Data Flow

Data Collection: Queries Apollo.io (46 companies) + Crunchbase (mock data)

Signal Detection: Checks hiring activity via SerpApi

Processing: Deduplicates and merges company data

Scoring: Applies heuristic scoring algorithm

Output: Generates ranked prospects in JSON format

🧮 Scoring Algorithm
score = 0.4*industry_match + 0.3*funding_signal + 0.2*hiring_signal + 0.1*tech_match

📁 Project Structure
prospect-search-agent/
├── main.py                 # Main agent script with async orchestration
├── icp_config.yaml         # ICP configuration (India-optimized)
├── prospects_output.json   # Generated results with confidence scores
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # Project documentation

🔧 API Integrations
Source	Purpose	Status
Apollo.io	Company discovery & filtering	✅ Working (46 companies)
Crunchbase	Funding stage data	✅ Mock Data
SerpApi	Hiring signal detection	⚠️ Rate Limited
📈 Sample Output
[
  {
    "company_name": "Infosys",
    "domain": "infosys.com",
    "industry": "information technology & services",
    "location": "Bengaluru, Karnataka, India",
    "confidence": 0.7,
    "signals": {
      "new_funding": true,
      "recent_hiring": false
    },
    "source": ["Apollo", "Crunchbase"]
  }
]

⚡ Performance Metrics
Metric	Result
Execution Time	~15 seconds
Companies Found	46 real Indian companies
Data Sources	2 operational + 1 mock
Success Rate	100% execution success
Output Quality	Professional scoring and ranking
💼 Ideal Use Cases

Sales Teams: Automated lead generation for Indian market

Startups: Investor and partnership prospecting

Marketing: Account-based targeting

Recruitment: Company research for talent acquisition

🔮 Future Enhancements

Real Crunchbase API integration

Enhanced SerpApi rate limit handling

Email contact enrichment

CSV/Excel export capabilities

Dashboard for results visualization

🤝 Contributing

Contributions are welcome! 💡

Areas for Improvement:

Additional data source integrations

Enhanced scoring algorithms

Better rate limit handling
