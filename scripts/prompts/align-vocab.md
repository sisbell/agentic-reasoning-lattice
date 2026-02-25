# Align ASN Notation to Canonical Vocabulary

You are aligning the notation in an ASN to match the project's canonical vocabulary. This is a MECHANICAL rewrite — you are changing notation, not content.

## Canonical Vocabulary

{{vocabulary}}

## Assignment

Align **{{asn_label}}** at `{{asn_path}}` to match the canonical vocabulary above.

Read the ASN, then rewrite it in place with aligned notation.

## What to Change

- **State component names** — use canonical names from the vocabulary (e.g., if vocabulary says `Σ.I` but ASN says `ispace`, change to `Σ.I`)
- **Property label prefixes** — use canonical naming conventions (e.g., if vocabulary says `S0-S5` for state invariants but ASN uses `INV-1`, change to `S0-S5` pattern)
- **Section headings** — use canonical organizational pattern from vocabulary
- **Type signatures** — use canonical type names

## What to Preserve

- All mathematical content, proofs, and derivations
- All prose and explanatory text (adjust notation references within prose)
- All open questions and discussion
- The semantic meaning of every property and invariant

## Mapping Rules

- Map labels by MEANING, not by number. If vocabulary defines `S0: content permanence` and the ASN has `IV0: content permanence`, then `IV0` becomes `S0` — even though 0 maps to 0 here, the mapping is by meaning, not by index.
- When the ASN introduces concepts not in the vocabulary, keep the ASN's notation for those — only change notation that HAS a canonical equivalent.
- This rewrite must be IDEMPOTENT: running it on an already-aligned ASN produces no changes.

## Process

1. Read the ASN file
2. Identify every notation that differs from canonical vocabulary
3. Build a mapping table (ASN notation → canonical notation)
4. Rewrite the ASN with all mappings applied
5. Write the updated ASN back to the same path

Do not create new files. Do not modify discovery.md or any other file. Only modify the ASN at the path above.
