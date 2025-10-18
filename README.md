# 🇮🇳 ProspectSearchAgent

A Python-based intelligent prospecting agent that automatically identifies potential **Indian customers** by querying multiple data sources and matching them against your **Ideal Customer Profile (ICP)**.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Async](https://img.shields.io/badge/Async-Await-orange.svg)
![India Focus](https://img.shields.io/badge/Focus-India%20Market-saffron.svg)

---

## 🚀 Features

- **Multi-source Data Collection:** Fetches company data from Apollo.io, Crunchbase, and SerpApi
- **India-Focused:** Optimized for Indian company classifications and market patterns
- **ICP-based Filtering:** Matches companies against configurable criteria
- **Simple Heuristic Scoring:** Clear, interpretable confidence scores (0.0–1.0)
- **Signal Detection:** Identifies buying signals like **funding** and **hiring activity**
- **Async Processing:** Efficient parallel API calls for faster results
- **Smart Deduplication:** Merges duplicate records from different data sources

---

## 📊 Latest Results (Production Ready)

### 📈 Prospecting Summary
| Confidence Level | Prospect Count | Percentage |
| :--- | :--- | :--- |
| **High Confidence (≥0.7)** | 3 | 6.5% |
| Medium Confidence (0.4–0.7) | 14 | 30.4% |
| Low Confidence (<0.4) | 29 | 63.0% |
| **Total Prospects** | **46 Indian Companies** | **100%** |

### 🏆 Top Prospects
| Company Name | Confidence Score | Primary Signals |
| :--- | :--- | :--- |
| **Infosys** | **0.7** | Industry Match, Funding Signal |
| **HCLTech** | **0.7** | Industry Match, Funding Signal |
| **Tech Mahindra** | **0.7** | Industry Match, Funding Signal |
| Tata Consultancy Services | 0.4 | Industry Match |
| Wipro | 0.4 | Industry Match |

---

## 🛠 Quick Start

### Installation

Clone the repository and install dependencies:
```bash
git clone [https://github.com/surabhi-chandrakant/prospect-search-agent.git](https://github.com/surabhi-chandrakant/prospect-search-agent.git)
cd prospect-search-agent
pip install -r requirements.txt
Configuration
Add your necessary API keys to the .env file:

Ini, TOML

APOLLO_API_KEY=your_key_here
CRUNCHBASE_API_KEY=your_key_here
SERPAPI_API_KEY=your_key_here
Modify icp_config.yaml to define your Ideal Customer Profile for the Indian market:

YAML

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
Run the Agent
Execute the main script to start prospecting:

Bash

python main.py
🎯 How It Works
🔄 Data Flow
Data Collection: Queries Apollo.io (returns 46 companies) and Crunchbase (mock data for funding).

Signal Detection: Checks for active hiring activity via Google Jobs using SerpApi.

Processing: Deduplicates and merges company data from all sources into a unified record.

Scoring: Applies the heuristic algorithm against the ICP to calculate a confidence score.

Output: Generates ranked prospects in JSON format.

🧮 Scoring Algorithm
The Confidence Score is a simple weighted heuristic, with a maximum possible score of 1.0:

$$\text{Score} = 0.4 \times \text{industry\_match} + 0.3 \times \text{funding\_signal} + 0.2 \times \text{hiring\_signal} + 0.1 \times \text{tech\_match} $$| Criterion | Weight | Value (0 or 1) | | :--- | :--- | :--- | | **Industry Match** | 0.4 | 1 if industry is in ICP list, 0 otherwise. | | **Funding Signal** | 0.3 | 1 if new funding is detected (e.g., from Crunchbase), 0 otherwise. | | **Hiring Signal** | 0.2 | 1 if recent hiring for data/tech roles is found (via SerpApi), 0 otherwise. | | **Tech Match** | 0.1 | 1 if tech stack is a match (planned future integration), 0 otherwise. | ----- ## 📁 Project Structure ``` prospect-search-agent/ ├── main.py                 # Main agent script with async orchestration ├── icp_config.yaml         # ICP configuration (India-optimized) ├── prospects_output.json   # Generated results with confidence scores ├── requirements.txt        # Python dependencies ├── .env.example            # Environment variables template └── README.md               # Project documentation ``` ### 🔧 API Integrations | Source | Purpose | Status | Notes | | :--- | :--- | :--- | :--- | | **Apollo.io** | Company discovery & filtering | ✅ Working (46 companies) | Core prospect data source. | | **Crunchbase** | Funding stage data | ✅ Mock Data | Simulating successful funding signal detection. | | **SerpApi** | Hiring signal detection | ⚠️ Rate Limited | Functional but requires careful rate management. | ### 📈 Sample Output ```json [ { "company_name": "Infosys", "domain": "infosys.com", "industry": "information technology & services", "location": "Bengaluru, Karnataka, India", "confidence": 0.7, "signals": { "new_funding": true, "recent_hiring": false }, "source": ["Apollo", "Crunchbase"] } ] ``` ----- ## 🚀 Performance Metrics | Metric | Result | | :--- | :--- | | **Execution Time** | \~15 seconds | | **Companies Found** | 46 real Indian companies | | **Data Sources** | 2 operational + 1 mock | | **Success Rate** | 100% execution success | | **Output Quality** | Professional scoring and ranking | ----- ## 🎯 Ideal Use Cases | Usecase | Benefit | | :--- | :--- | | 💼 **Sales Teams** | Automated lead generation and qualification for the Indian market. | | 🚀 **Startups** | Investor and strategic partnership prospecting based on growth signals. | | 📣 **Marketing** | Account-Based Marketing (ABM) targeting high-confidence accounts. | | 🧑‍💼 **Recruitment** | Company research for talent acquisition and competitive analysis. | ----- ## 🔮 Future Enhancements We are continuously improving the agent. Future focus areas include: - **Real Crunchbase API** integration for up-to-date funding data. - Enhanced **SerpApi rate limit handling** with backoff and retry logic. - **Email contact enrichment** via a third-party service. - **CSV/Excel export** capabilities for easy workflow integration. - **Dashboard** for interactive results visualization. ----- ## 🤝 Contributing Contributions are welcome\! If you have any ideas for new features, bug fixes, or integrations, please open an issue or submit a pull request. Focus areas for contribution: - Additional data source integrations (e.g., LinkedIn, proprietary data). - Enhanced scoring algorithms (e.g., incorporating employee growth rate). - Improved rate limit handling and error logging. - Export functionality (CSV/Excel). ``` ```$$
