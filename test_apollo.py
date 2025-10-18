# test_apollo.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_apollo_connection():
    APOLLO_API_KEY = os.getenv("APOLLO_API_KEY")
    
    if not APOLLO_API_KEY:
        print("❌ No Apollo API key found")
        return
        
    headers = {
        "X-Api-Key": APOLLO_API_KEY,
        "Content-Type": "application/json"
    }
    
    # Test with very simple query
    payload = {
        "q_organization_keywords": "tech",
        "page": 1,
        "per_page": 5
    }
    
    try:
        response = requests.post(
            "https://api.apollo.io/v1/organizations/search",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_apollo_connection()