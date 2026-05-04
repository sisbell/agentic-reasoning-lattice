"""Annotate claim YAMLs — add type, dependencies, signature.

Usage:
    python scripts/derive-claims-annotate.py <ASN>
    python scripts/derive-claims-annotate.py 36
"""

from lib.claim_derivation.annotate import main

if __name__ == "__main__":
    main()
