import subprocess

print(subprocess.run(['nslookup', 'google.com'], capture_output=True, text=True).stdout)
