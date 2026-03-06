import sys
from pathlib import Path

# Ensure scripts/ is on path so `from paths import ...` works in lib/ modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
