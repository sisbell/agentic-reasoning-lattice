"""Enrich claim YAMLs — add type, dependencies, vocabulary.

Usage:
    python scripts/note-decompose-enrich.py <ASN>
    python scripts/note-decompose-enrich.py 36
"""

from lib.note_decomposition.enrich import main

if __name__ == "__main__":
    main()
