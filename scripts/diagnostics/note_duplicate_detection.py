#!/usr/bin/env python3
"""Embedding-based duplicate-property detection across discovery notes.

Reads a set of discovery-stage notes, chunks each by property marker,
embeds chunks via nomic-embed-text-v1.5, and outputs a ranked report
of cross-note candidate-duplicate pairs.

Property markers recognised:
  **<ID> — <Name>.**     (em-dash form, used for new properties)
  **<ID> - <Name>.**     (hyphen form)
  **<ID> (<Name>).**     (parenthetical form, used for upstream invariants)

A chunk = marker line + following lines until the next marker or `^##` heading.

Usage:
    python scripts/diagnostics/note_duplicate_detection.py 59 61 65 67

Output:
    Markdown report at lattices/<lattice>/_workspace/duplicate-detection/<asn-list>.md
"""

import argparse
import re
import sys
from itertools import combinations
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.shared.paths import LATTICE, WORKSPACE_DIR


PROPERTY_MARKER_RE = re.compile(
    r"^\*\*([A-Z][\w'-]*)\s*"
    r"(?:[—\-]\s+|\(\s*)"
    r"([A-Z][A-Za-z]+)",
)
SECTION_RE = re.compile(r"^##\s")


def find_note_path(asn_num):
    """Find the discovery note file for an ASN number."""
    note_dir = LATTICE / "_docuverse" / "documents" / "note"
    pattern = f"ASN-{asn_num:04d}-*.md"
    matches = list(note_dir.glob(pattern))
    if not matches:
        return None
    return matches[0]


def parse_chunks(note_path):
    """Parse a note file into property chunks.

    Returns list of dicts: {id, name, text, line_no}.
    """
    text = note_path.read_text()
    lines = text.splitlines()
    chunks = []
    current = None

    for i, line in enumerate(lines):
        match = PROPERTY_MARKER_RE.match(line)
        if match:
            if current is not None:
                chunks.append(current)
            prop_id, prop_name = match.group(1), match.group(2)
            current = {
                "id": prop_id,
                "name": prop_name,
                "line_no": i + 1,
                "lines": [line],
            }
        elif current is not None:
            if SECTION_RE.match(line):
                chunks.append(current)
                current = None
            else:
                current["lines"].append(line)

    if current is not None:
        chunks.append(current)

    for c in chunks:
        c["text"] = "\n".join(c["lines"]).strip()
        del c["lines"]
    return chunks


def embed_chunks(model_pack, chunks):
    """Embed chunk texts; return numpy array of normalized vectors."""
    import torch
    tokenizer, model = model_pack
    texts = [c["text"] for c in chunks]
    inputs = tokenizer(texts, padding=True, truncation=True,
                       return_tensors="pt", max_length=8192)
    with torch.no_grad():
        outputs = model(**inputs)
    last_hidden = outputs.last_hidden_state
    mask = inputs["attention_mask"].unsqueeze(-1).bool()
    last_hidden = last_hidden.masked_fill(~mask, 0.0)
    summed = last_hidden.sum(dim=1)
    counts = inputs["attention_mask"].sum(dim=1, keepdim=True).clamp(min=1)
    pooled = summed / counts
    pooled = pooled / pooled.norm(dim=1, keepdim=True).clamp(min=1e-9)
    return pooled.numpy()


def cosine_similarity(a, b):
    return float(np.dot(a, b))


def render_report(asn_specs, chunks_by_note, similarities):
    """Build the markdown report."""
    lines = []
    lines.append("# Duplicate-property candidates across discovery notes")
    lines.append("")
    lines.append(f"**Notes scanned:** {', '.join(asn_specs)}")
    chunk_counts = {n: len(chunks_by_note[n]) for n in asn_specs}
    lines.append(f"**Chunks per note:** "
                 f"{', '.join(f'{n}={chunk_counts[n]}' for n in asn_specs)}")
    lines.append(f"**Total cross-note pair comparisons:** {len(similarities)}")
    lines.append("")
    lines.append(
        "Each pair shows two chunks (one per note) ranked by cosine similarity "
        "of their embeddings. Embedding model: nomic-embed-text-v1.5."
    )
    lines.append("")

    tiers = [
        ("Near-identical (≥ 0.95)", 0.95, 1.01),
        ("High similarity (0.90 – 0.95)", 0.90, 0.95),
        ("Moderate similarity (0.85 – 0.90)", 0.85, 0.90),
        ("Low-moderate (0.80 – 0.85)", 0.80, 0.85),
    ]

    for tier_name, lo, hi in tiers:
        tier_pairs = [s for s in similarities if lo <= s["score"] < hi]
        lines.append(f"## {tier_name} — {len(tier_pairs)} pairs")
        lines.append("")
        if not tier_pairs:
            lines.append("_(none)_")
            lines.append("")
            continue
        for pair in tier_pairs:
            a, b = pair["a"], pair["b"]
            lines.append(
                f"### {pair['score']:.3f} — "
                f"{a['note']} `{a['id']} {a['name']}` ↔ "
                f"{b['note']} `{b['id']} {b['name']}`"
            )
            lines.append("")
            lines.append(f"**{a['note']} — {a['id']} ({a['name']}):**")
            lines.append("")
            lines.append("> " + a["text"].replace("\n", "\n> "))
            lines.append("")
            lines.append(f"**{b['note']} — {b['id']} ({b['name']}):**")
            lines.append("")
            lines.append("> " + b["text"].replace("\n", "\n> "))
            lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("asns", nargs="+", help="ASN numbers (e.g., 59 61 65 67)")
    parser.add_argument("--threshold", type=float, default=0.80,
                        help="Surface pairs with similarity ≥ this (default: 0.80)")
    args = parser.parse_args()

    asn_nums = [int(re.sub(r"[^0-9]", "", a)) for a in args.asns]
    note_paths = []
    for n in asn_nums:
        path = find_note_path(n)
        if path is None:
            print(f"  Note for ASN-{n:04d} not found", file=sys.stderr)
            sys.exit(1)
        note_paths.append((n, path))
    asn_specs = [f"ASN-{n:04d}" for n, _ in note_paths]

    print("Loading embedding model (nomic-embed-text-v1.5)...", file=sys.stderr)
    from transformers import AutoTokenizer, AutoModel
    tokenizer = AutoTokenizer.from_pretrained(
        "nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True,
    )
    model = AutoModel.from_pretrained(
        "nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True,
    )
    model.eval()
    model_pack = (tokenizer, model)

    chunks_by_note = {}
    embeddings_by_note = {}
    for asn_label, (n, path) in zip(asn_specs, note_paths):
        chunks = parse_chunks(path)
        for c in chunks:
            c["note"] = asn_label
        chunks_by_note[asn_label] = chunks
        if not chunks:
            embeddings_by_note[asn_label] = np.zeros((0, 768))
        else:
            embeddings_by_note[asn_label] = embed_chunks(model_pack, chunks)
        print(f"  {asn_label}: {len(chunks)} chunks", file=sys.stderr)

    similarities = []
    for note_a, note_b in combinations(asn_specs, 2):
        chunks_a = chunks_by_note[note_a]
        chunks_b = chunks_by_note[note_b]
        emb_a = embeddings_by_note[note_a]
        emb_b = embeddings_by_note[note_b]
        for i, ca in enumerate(chunks_a):
            for j, cb in enumerate(chunks_b):
                score = cosine_similarity(emb_a[i], emb_b[j])
                if score >= args.threshold:
                    similarities.append({
                        "score": score,
                        "a": ca,
                        "b": cb,
                    })

    similarities.sort(key=lambda s: -s["score"])
    print(f"\n{len(similarities)} pairs at similarity ≥ {args.threshold}",
          file=sys.stderr)

    report = render_report(asn_specs, chunks_by_note, similarities)
    out_dir = WORKSPACE_DIR / "duplicate-detection"
    out_dir.mkdir(parents=True, exist_ok=True)
    asn_tag = "+".join(s.replace("ASN-", "") for s in asn_specs)
    out_path = out_dir / f"operations-{asn_tag}.md"
    out_path.write_text(report)
    print(f"Report: {out_path.relative_to(LATTICE.parent.parent)}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
