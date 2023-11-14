import utils
from pathlib import Path
import os

base_dir = Path(os.path.dirname(__file__)).parent
assert (base_dir / "book.toml").exists()
utils.shell_command("python3 -m black .")
utils.shell_command("python3 utils/task-manager.py d")
utils.shell_command("python3 utils/format.py")
# utils.shell_command("yaspeller --config utils/.yaspeller.json .")
