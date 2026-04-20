#!/usr/bin/env bash
# Copy expert consultations from one ASN to another.
#
# Usage:
#   ./run/copy-experts.sh 28 29    # copy ASN-0028 experts to ASN-0029
set -euo pipefail

if [ $# -lt 2 ]; then
    echo "Usage: $0 SOURCE_ASN TARGET_ASN" >&2
    exit 1
fi

# Normalize ASN numbers to 4-digit labels
src=$(printf "ASN-%04d" "$1")
tgt=$(printf "ASN-%04d" "$2")

src_dir="lattices/xanadu/discovery/consultations/$src"
tgt_dir="lattices/xanadu/discovery/consultations/$tgt"

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
