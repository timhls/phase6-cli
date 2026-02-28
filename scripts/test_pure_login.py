import os
import httpx
import json

username = os.environ.get("PHASE6_USERNAME")
password = os.environ.get("PHASE6_PASSWORD")

client = httpx.Client(base_url="https://lernen.phase-6.de")

response = client.post(
    "/server.integration/login",
    json={"username": username, "password": password, "jossoSessionId": "", "remember": True},
)

print(f"Login Response Status: {response.status_code}")
try:
    print(f"Login JSON: {response.json()}")
except:
    print(f"Login Content: {response.text}")

print(f"Cookies: {client.cookies}")

# Try to get subjects
subjects_resp = client.post("/server.integration/subjectsCombined", json={"filterMode": "LIBRARY"})
print(f"Subjects Response Status: {subjects_resp.status_code}")
try:
    print(f"Subjects JSON: {json.dumps(subjects_resp.json())[:300]}")
except:
    print(f"Subjects Content: {subjects_resp.text}")
