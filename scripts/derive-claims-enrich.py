"""Enrich claim YAMLs — add type, dependencies, signature.

Usage:
    python scripts/derive-claims-enrich.py <ASN>
    python scripts/derive-claims-enrich.py 36
"""

from lib.claim_derivation.enrich import main

if __name__ == "__main__":
    main()
