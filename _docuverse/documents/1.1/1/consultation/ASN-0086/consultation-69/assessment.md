# Channel Assignment — ASN-0086 review-69

**Date:** 2026-05-19 15:31

## Issue 1: R0 proof — "IH for L1" wording is loose
Reason: Pure wording cleanup — L1 is a substrate-level invariant at every reachable Σ (ASN-0043), so citing it directly is internally derivable. No design intent or implementation evidence is at stake; the fix audits the proof's own citation phrasing against invariants already imported.

## Issue 2: R7a proof — substrate-conformance discharge is too informal
Reason: Exposition task within the existing invariant catalogs of ASN-0043/0036/0093. The needed enumeration — which Frame conditions, structural properties, and reachability inheritance discharge which invariants per K.σ-step vs. K.λ-step — is mechanical against the cited ASNs and the K-op contracts already present in this note.

## Issue 3: Notation `L_K^Σ` conflates K with its coverage class [K]
Reason: Notation/presentation decision internal to this ASN. The mathematical content (coverage-equivalence membership at slot 3) is already settled by the Definition; the choice between `L_{[K]}^Σ` renaming and a quotient-notation note is editorial.

## Issue 4: R5's generalization paragraph should be a separate corollary
Reason: Structural reorganization of material already proved within R5. The endset-content-uniformity claim is grounded in R0's invariant-by-invariant verification (also in this ASN); extracting it as a named corollary or expanding R5's statement is purely internal restructuring.

## Issue 5: R0a-Cor2 — Route A citation should route through ASN-0093's named lemma
Reason: Citation cleanup against ASN-0093's named abstraction (ChainElementT4Validity), which already packages the T10a.4 + SubAllocatorAxiom.ChainDiscipline correspondence. Internal to the ASN's existing dependency on ASN-0093.
