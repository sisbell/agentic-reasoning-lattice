---
create_note: 129
title: "Substrate Predicate Composition"
source_doc: "_workspace/asn-new-predicate-composition-draft.md"
depends: [34, 43, 86, 126, 127, 128]
---

# Why I'm importing this doc

ASN-0128 converged at review-36 (two consecutive clean reviews closing a
28-cycle anti-bloat audit), completing the protocols stack's atomic read
surface: per-type default predicates, behavior-unlocked predicates, the
AD/AM denotation discipline, and the three views. This note closes the
chain above it — the algebra (PC0–PC2a) under which those atoms compose
into the substrate's full predicate language, the evaluation guarantees
(purity, termination), the expressive ceiling (PC6, with PC6a turning
ASN-0128's authority-based withholding of `reach` into a theorem), and
the dynamics classification (PD0–PD2) a protocol author needs to choose
trigger and termination predicates soundly.

The strategic intent: PL is the substrate's extension language. A
third party registers types at construction and composes predicates,
composition being the only extension mechanism — which is why the
guarantees quantify over every predicate any builder will ever write,
enabling independently-built protocols and stigmergic systems on top
of the link substrate. It settles ASN-0128's Open Questions 1 (UV: the
uniform default-view rule) and 2 (PC2a: set semantics for counts), and
descends from docs/protocols/substrate/predicate-composition.md in the
established lineage (types.md → ASN-0086), with retired ASN-0095 mined:
every seam 0095 documented is settled here (aggregation → PC2a,
recursion → PC6a, primitive admission → V-PRIM) or explicitly fenced.

Dependency note: ASN-0127 is a boundary-only dependency — the
arrangement-reading query layer (`image`/`findlinks_V`) that PL's
structural-reads-only commitment deliberately excludes; the citation
draws the layer map rather than consuming results.
