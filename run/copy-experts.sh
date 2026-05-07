#!/usr/bin/env bash
# Copy expert consultation files from one ASN's directory to another's.
#
# Filesystem-only operation: copies the consultation directory tree
# from source ASN to target ASN under the substrate's consultation
# document tree. Does NOT emit substrate links — for full substrate-
# aware ASN cloning (note + inquiry + consultations + lineage links),
# use scripts/note-clone.py with a clone spec doc.
#
# Usage:
#   ./run/copy-experts.sh 28 29                  # default lattice (xanadu)
#   LATTICE=materials ./run/copy-experts.sh 28 29
set -euo pipefail

if [ $# -lt 2 ]; then
    echo "Usage: $0 SOURCE_ASN TARGET_ASN" >&2
    exit 1
fi

LATTICE="${LATTICE:-xanadu}"
src=$(printf "ASN-%04d" "$1")
tgt=$(printf "ASN-%04d" "$2")

src_dir="lattices/$LATTICE/_docuverse/documents/consultation/$src"
tgt_dir="lattices/$LATTICE/_docuverse/documents/consultation/$tgt"

if [ ! -d "$src_dir" ]; then
    echo "Error: $src_dir does not exist" >&2
    exit 1
fi

if [ -d "$tgt_dir" ]; then
    echo "Error: $tgt_dir already exists" >&2
    exit 1
fi

cp -r "$src_dir" "$tgt_dir"
git add "$tgt_dir"
git commit -m "experts: copy $src consultations to $tgt for redraft"

echo "Done: $src_dir → $tgt_dir"
