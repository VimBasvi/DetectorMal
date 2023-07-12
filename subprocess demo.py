import subprocess
link = "google.com"
print(subprocess.run(['nslookup', link], capture_output=True, text=True).stdout)
