"""Disassemble — section YAMLs to per-claim file pairs.

Usage:
    python scripts/disassemble.py <ASN>
    python scripts/disassemble.py 36
    python scripts/disassemble.py 36 --dry-run
"""

from lib.blueprinting.disassemble import main

if __name__ == "__main__":
    main()
