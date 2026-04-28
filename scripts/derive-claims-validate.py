"""Validate — check per-claim file pairs for completeness and consistency.

Usage:
    python scripts/derive-claims-validate.py <ASN>
    python scripts/derive-claims-validate.py 36
"""

from lib.claim_derivation.validate import main

if __name__ == "__main__":
    main()
