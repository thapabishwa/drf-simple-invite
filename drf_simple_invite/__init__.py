import subprocess
result = subprocess.run(
    ["git", "describe", "--abbrev=0", "--tags"], stdout=subprocess.PIPE)
VERSION = result.stdout.decode('utf-8').strip()
