# Channel Assignment — ASN-0086 review-80

**Date:** 2026-05-31 14:11

## Issue 1: Load-bearing citations to foundation claims that do not exist in the cited foundations
Reason: This is a citation-correction issue against sibling spec documents (ASN-0093, ASN-0040), not a question of design intent or implementation behavior. The review already identifies the real constructs (`ChainDiscipline`, `FirstEmission`, `ChainMembershipForOrigin`) and the ASN-0040 `S(p,d)` postcondition the uniform-length/zero-count facts derive from; the fix is to read those foundations and substitute the correct names. Derivable from the ASN's own dependency set.

## Issue 2: Citations to ASN-0034 / ASN-0036 claims that do not exist
Reason: `NAT-zero` and `T10a.8` are pure tumbler arithmetic the note can argue inline from the real NAT axioms (`NAT-discrete`, `NAT-addcompat`); `S7c` is a mislabel; and content-invariance under arrangement modification is already available via the note's own catalogued `S0 (ContentImmutability)` rather than the phantom `S9`. All resolvable by reading ASN-0036/ASN-0034 or supplying the arithmetic inline.

## Issue 3: Foundation claims cited under the wrong label
Reason: Pure label corrections — `T7` is `SubspaceDisjointness` and ASN-0093's store-disjointness claim is `SD`, both of which the note already uses correctly elsewhere. No external channel needed; the correct labels are fixed by the cited foundations and the note's own usage.

## Issue 4: Meta-prose around definitions and forward references (anti-bloat)
Reason: Purely editorial deletions of inclusion justifications, label rationale, downstream-use inventories, and essay content. No design or implementation input required to remove prose the argument does not depend on.

## Issue 5: R0 re-derives a freshness result the foundation already names
Reason: The fix is to cite `SubsequentEmissionFreshness (ASN-0093)` in place of the re-derivation, which the review confirms establishes exactly the three-way split R0 reconstructs. Resolvable by reading the foundation lemma; no design intent or code evidence required.
