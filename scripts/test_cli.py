import os
import subprocess

username = os.environ.get("PHASE6_USERNAME")
password = os.environ.get("PHASE6_PASSWORD")

print("--- Running Login ---")
proc = subprocess.run(
    ["uv", "run", "pyphase6", "login", "--username", username, "--password", password],
    text=True,
    capture_output=True
)
print(proc.stdout)
if proc.stderr: print("STDERR:", proc.stderr)

print("--- Running Subjects ---")
proc = subprocess.run(
    ["uv", "run", "pyphase6", "subjects"],
    text=True,
    capture_output=True
)
print(proc.stdout)
if proc.stderr: print("STDERR:", proc.stderr)

print("--- Running Vocab ---")
# Using the ID for the HSK subject we saw earlier
subject_id = "615cc841-91fa-458d-a1d0-ea4ccaeb2c3e" 
proc = subprocess.run(
    ["uv", "run", "pyphase6", "vocab", subject_id, "--limit", "10"],
    text=True,
    capture_output=True
)
print(proc.stdout)
if proc.stderr: print("STDERR:", proc.stderr)
