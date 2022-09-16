import subprocess
result = subprocess.run(
    ["git", "describe", "--abbrev=0", "--tags"], stdout=subprocess.PIPE, check=True)
VERSION = result.stdout.decode('utf-8').strip()
