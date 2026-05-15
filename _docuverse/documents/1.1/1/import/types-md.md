---
create_note: 86
title: "Typed Relations on Address Sets"
source_doc: "docs/protocols/substrate/types.md"
depends: [34, 36, 43]
---

# Why I'm importing this doc

`docs/protocols/substrate/types.md` was drafted in formal-note style — R0-R6 properties with proofs, definitions, a Properties Introduced table, an Open Questions section — but it lives outside the lattice in the protocol docs. Bringing it into the lattice so:

1. The review/revise cycle can refine it as a derived note (currently it's a one-shot prose drop that hasn't been through cycle review)
2. Downstream notes can cite it via standard `citation.depends` rather than informally referencing a docs/ path
3. Substrate alignment can be tracked formally — the doc's "Three Operations" (Emit / Retract / Activate) need to track the actual implementation in `scripts/lib/backend/emit.py`, and review findings on drift become first-class

This formalizes the substrate's relation algebra over the link store (R0-R6) and the three primitive operations (Emit / Observe / Nullify) used throughout substrate work. The doc's deps follow from grep — three explicit ASN references in the prose:

- **ASN-0034 (Tumbler Algebra)** — T0, T7, T10a, T12 cited
- **ASN-0036 (Strand Model)** — S0-S6 cited (content store `Σ.C`)
- **ASN-0043 (Link Model)** — L0, L1b, L1c, L3, L4, L8, L9, L11b, L12, L12a, L13, L14 cited (the substrate of the relation algebra)

It sits at the foundation tier alongside its three deps. Note: the doc introduces its own substrate-operation vocabulary (Emit / Observe / Nullify), distinct from ASN-0047's K-primitives (K.α / K.λ / K.μ / K.ρ) — so the Transition Model is not a dependency despite shared general Σ→Σ' notation.

Source doc stays in place per the note-import policy. The lattice copy becomes the canonical derived note as the cycle refines it; `docs/protocols/substrate/types.md` continues to serve as cross-cutting reference documentation.

The expected first round of review findings will likely concern:
- Whether the doc's R0-R6 numbering aligns with the existing label conventions across substrate-touching ASNs
- Whether "Emit / Retract / Activate" map cleanly to the implementation's `emit()` / `emit_retraction()` / `active_links()` surface
- Citation tightening on the L-series references from ASN-0043
