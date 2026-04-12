"""Validate — check per-property file pairs for completeness and consistency.

Usage:
    python scripts/validate.py <ASN>
    python scripts/validate.py 36
"""

from lib.blueprinting.validate import main

if __name__ == "__main__":
    main()
