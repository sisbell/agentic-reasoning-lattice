"""Disassemble — section YAMLs to per-claim file pairs.

Usage:
    python scripts/note-decompose-disassemble.py <ASN>
    python scripts/note-decompose-disassemble.py 36
    python scripts/note-decompose-disassemble.py 36 --dry-run
"""

from lib.note_decomposition.disassemble import main

if __name__ == "__main__":
    main()
