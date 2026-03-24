import os

root_path = os.path.expanduser("~")
extensions = ('.jpg', '.jpeg', '.png', '.mp4', '.pdf', '.docx', '.txt')

print("-" * 30)
print("⚡ AL-RAAD SCANNER ACTIVE ⚡")
print("-" * 30)

count = 0
for root, dirs, files in os.walk(root_path):
    for file in files:
        if file.lower().endswith(extensions):
            print(f"[+] FOUND: {file}")
            count += 1

print("-" * 30)
print(f"⚡ DONE! TOTAL FILES: {count} ⚡")
