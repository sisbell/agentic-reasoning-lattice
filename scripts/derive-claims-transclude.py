"""Transclude — section YAMLs to per-claim file pairs.

Usage:
    python scripts/derive-claims-transclude.py <ASN>
    python scripts/derive-claims-transclude.py 36
    python scripts/derive-claims-transclude.py 36 --dry-run
"""

from lib.claim_derivation.transclude import main

if __name__ == "__main__":
    main()
