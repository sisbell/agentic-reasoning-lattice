"""Validate — check per-claim file pairs for completeness and consistency.

Usage:
    python scripts/note-decompose-validate.py <ASN>
    python scripts/note-decompose-validate.py 36
"""

from lib.note_decomposition.validate import main

if __name__ == "__main__":
    main()
