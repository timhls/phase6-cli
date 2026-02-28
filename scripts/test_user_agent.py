import json
import os
from pathlib import Path
import httpx
from playwright.sync_api import sync_playwright

username = os.environ.get("PHASE6_USERNAME")
password = os.environ.get("PHASE6_PASSWORD")

print("Logging in with Playwright...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    page = context.new_page()

    page.goto("https://lernen.phase-6.de/v2/#/login", wait_until="networkidle")
    page.fill('input[type="e-mail"]', username)
    page.fill('input[type="password"]', password)
    page.get_by_role("button", name="Login").click()
    page.wait_for_url("**/home**", timeout=15000)
    
    # Grab the whole state so we can see all headers/cookies
    state = context.storage_state()
    
    # Let's try the request *inside* Playwright to prove it works
    resp = context.request.post(
        "https://lernen.phase-6.de/server.integration/subjectsCombined",
        data=json.dumps({"filterMode": "LIBRARY"}),
        headers={"Content-Type": "application/json"}
    )
    print(f"Playwright request status: {resp.status}")
    if resp.status == 200:
        print("Playwright request worked!")

    cookies = {c["name"]: c["value"] for c in state["cookies"]}
    browser.close()

# Now try with HTTPX using the exact same cookies
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Origin": "https://lernen.phase-6.de",
    "Referer": "https://lernen.phase-6.de/v2/",
    "X-Requested-With": "XMLHttpRequest"
}

print("Trying HTTPX...")
client = httpx.Client(base_url="https://lernen.phase-6.de", cookies=cookies, headers=headers)
response = client.post("/server.integration/subjectsCombined", json={"filterMode": "LIBRARY"})
print(f"Status: {response.status_code}")
if response.status_code == 200:
    print(f"Success! {json.dumps(response.json())[:200]}")
else:
    print(response.text)
