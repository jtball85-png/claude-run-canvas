"""
test_connection.py
------------------
Quick sanity check — confirms your Canvas API token and base URL are working.
Pulls basic account info and prints it to the terminal.
Run with: python scripts/test_connection.py
"""

import os
import requests
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

TOKEN = os.getenv("CANVAS_API_TOKEN")
BASE_URL = os.getenv("CANVAS_BASE_URL")

if not TOKEN:
    print("ERROR: CANVAS_API_TOKEN is missing from your .env file.")
    exit(1)

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "User-Agent": "claude-run-canvas/1.0 (Ventura Adult and Continuing Education)"
}

def test_connection():
    url = f"{BASE_URL}/accounts"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        accounts = response.json()
        print("SUCCESS: Connection working!\n")
        for account in accounts:
            print(f"  Account ID : {account.get('id')}")
            print(f"  Name       : {account.get('name')}")
            print(f"  Workflow   : {account.get('workflow_state')}")
            print()
    elif response.status_code == 401:
        print("ERROR: Unauthorized -- check your CANVAS_API_TOKEN in .env")
    elif response.status_code == 404:
        print("ERROR: Not found -- check your CANVAS_BASE_URL in .env")
    else:
        print(f"ERROR: Unexpected response: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_connection()
