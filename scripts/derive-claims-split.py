"""Decompose ASN — split by section headers, analyze structure.

Usage:
    python scripts/derive-claims-split.py <ASN>
    python scripts/derive-claims-split.py 36
"""

from lib.claim_derivation.decompose import main

if __name__ == "__main__":
    main()
