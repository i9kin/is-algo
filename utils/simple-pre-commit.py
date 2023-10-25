import subprocess
from pathlib import Path

base_dir = Path(".")
assert (base_dir / "book.toml").exists()
subprocess.Popen("python3 -m black .".split()).wait()
subprocess.Popen("python3 utils/task-manager.py d".split()).wait()
subprocess.Popen("python3 utils/format.py".split()).wait()
# subprocess.Popen("yaspeller --config utils/.yaspeller.json .".split()).wait()
