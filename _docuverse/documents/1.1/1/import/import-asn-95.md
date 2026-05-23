---
create_note: 95
title: "Predicate Composition"
source_doc: "_workspace/drafts/asn-0095-predicate-composition.md"
depends: [34, 43, 86, 94]
---

# Why I'm importing this doc

ASN-0094 establishes, for each `K ∈ T_cat`, an atomic vocabulary of
predicate templates (Sh5 catalog) with stable signatures (Sh-conf,
Sh0–Sh3). What ASN-0094 does *not* establish is the closure under
which those atomic templates compose into the substrate's full
predicate language — Boolean composition, quantification, value
composition — and the expressive ceiling that closure pins down.

ASN-0095 closes this chain. The substantive claim is PC6
(ExpressiveClosure): the substrate's predicate language is *exactly*
the closure of the atomic vocabulary under PC0–PC2. Composition
extends within a ceiling fixed by the shape catalog; it does not
raise the ceiling. Without ASN-0095 (or an equivalent), the
substrate's predicate language is ad hoc — every consumer defines
its own composition rules, and quality questions about "what can the
substrate ask" have no formal answer.

Importing now because the FanOutPair shape patch for ASN-0094 is in
flight; ASN-0095's first review will see the new catalog row after
ASN-0094's revise cycle settles. Direct deps `[34, 43, 86, 94]` — no
transitivity assumption. ASN-0036 enters only transitively via
ASN-0094's *Content-store finiteness* scaffolding clause and is not
cited directly.

Pre-import state of the draft: Phase 1–4 revisions applied by an
external pass (citation fixes, type-correctness fix in the
Confirmation example using `addr`, Layer Composites Remark on PC2,
parametric universalization in PC1 Cd, view-parametricity Cd
clarifying view-affected vs view-independent primitives). Two new
Open Questions surface residual issues — substrate-primitive
admission in PC2 chains, and Layer Composites discharge mechanism —
which the review cycle can route per the operator's preference.

The first review cycle should also catch the FanOutPair bookkeeping:
ASN-0095 currently enumerates seven canonical shape rows (Classifier
through Provenance) and PC6's ⊇-proof enumerates the matching
template-row coverage; both will need updating to include FanOutPair
once the ASN-0094 patch lands.
