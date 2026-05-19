# Channel Assignment — ASN-0047 review-110

**Date:** 2026-05-19 08:51

## Issue 1: K.α reinvents ASN-0093's allocation primitive
Reason: Pure structural reorganization — reference ASN-0093 instead of restating. Derivable from comparing ASN-0093 and ASN-0047 directly; no design-intent or implementation evidence required.

## Issue 2: K.λ reinvents ASN-0093's allocation primitive
Reason: Same as Issue 1 — reference ASN-0093's K.λ. Verifiable by reading the foundation; no external channel needed.

## Issue 3: SubAllocatorAxiom reinvents ASN-0093's axiom verbatim
Reason: Adopt ASN-0093's axiom directly. The duplication is checkable from the foundation text; no design or implementation question.

## Issue 4: Anchor and sub-allocator notation reinvents ASN-0093
Reason: Reference ASN-0093's symbol definitions. Notation-ownership decision derivable from the foundation; no external channel.

## Issue 5: L0's C-clause is not new in current foundation
Reason: Factual question about ASN-0093's current statement of L0. Resolvable by reading ASN-0093; no design-intent or implementation channel needed.

## Issue 6: K.α and K.ρ frames in extended state omit explicit `L' = L`
Reason: Pure consistency fix — K.α and K.ρ provably do not touch L (their definitions establish this). Add frame paragraphs to match the K.μ⁺/K.μ⁻ treatment already in the ASN.

## Issue 7: J0 quantifies over E'_doc with no explicit guarantee that K.α's content-subspace amendment forces s_C placement
Reason: The S3★ + L14 chain that forces content-subspace placement is already present in the ASN; the fix is to state it explicitly in the P7a discharge. Internal.

## Issue 8: The Cross-document disjointness lemma's Case A length verification has an unverified depth assumption
Reason: One-line derivation using Prefix (ASN-0034) and T3 (ASN-0034). Foundation rules suffice; no external channel needed.

## Issue 9: K.μ~ admissibility clause (iii) creates a derivation-vs-precondition ambiguity for the empty/singleton case
Reason: The dependency chain (S3★(Σ') → subspace preservation → fixity Steps 1–3 → existence condition) is already implicit in the ASN. Fix is to state the chain upfront; internal.
