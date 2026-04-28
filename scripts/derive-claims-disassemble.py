"""Disassemble — section YAMLs to per-claim file pairs.

Usage:
    python scripts/derive-claims-disassemble.py <ASN>
    python scripts/derive-claims-disassemble.py 36
    python scripts/derive-claims-disassemble.py 36 --dry-run
"""

from lib.claim_derivation.disassemble import main

if __name__ == "__main__":
    main()
