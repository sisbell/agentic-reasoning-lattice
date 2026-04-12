"""Enrich property YAMLs — add type, dependencies, vocabulary.

Usage:
    python scripts/enrich.py <ASN>
    python scripts/enrich.py 36
"""

from lib.blueprinting.enrich import main

if __name__ == "__main__":
    main()
