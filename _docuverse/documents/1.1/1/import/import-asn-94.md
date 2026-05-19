---
create_note: 94
title: "Typed Relation Shapes"
source_doc: "_workspace/drafts/asn-0094-typed-relation-shapes.md"
depends: [34, 43, 86]
---

# Why I'm importing this doc

ASN-0086 is converging on the typed-relations algebra (L_K with Emit/Observe/Nullify operations and R0–R7 properties). The relational structure as defined is too permissive to support a typed predicate vocabulary — F and G can be any finite endsets whose coverage lies anywhere in `A`, so a predicate over `L_K` has no fixed signature.

The shapes document (sourced from `docs/protocols/substrate/shapes.md`) is the next layer above ASN-0086: a *single structural decision per type* — a shape tuple of cardinality bounds, target-domain restrictions, and idempotency flag — enforced at Emit time, from which predicate template families are mechanically derivable. The pipeline is R0–R7 → shape restrictions → predicate templates → composed predicates.

Importing now because ASN-0086 has stabilized post-rebase onto ASN-0093 (its foundation is now properly substrate-aware), so the shapes layer can take ASN-0086 as a stable consumer surface. Direct deps `[34, 43, 86]` — no transitivity assumption.

Pre-import edits already applied to the drafted source: all 9 `typed-relations.md` references rewritten to `ASN-0086`; H1 retitled to match the ASN-NNNN naming convention.
