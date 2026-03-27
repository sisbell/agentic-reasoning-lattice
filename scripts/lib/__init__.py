import sys
from pathlib import Path

# Ensure scripts/ is on path so `from lib.shared.paths import ...` works
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
