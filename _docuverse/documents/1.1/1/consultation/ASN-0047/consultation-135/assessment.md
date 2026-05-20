# Channel Assignment — ASN-0047 review-135

**Date:** 2026-05-19 22:17

## Issue 1: FrontierEquivalence lemma proof is informal
Reason: The fix is restructuring an existing proof into explicit forward (⟹) and reverse (⟸) direction proofs using machinery already in the ASN (T10a chain-advancement uniqueness, P1, T10a.6). All inputs are derivable from foundation results and existing ASN content; no design intent or implementation evidence is needed.

## Issue 2: K.μ~ admissible π existence is asserted but not constructed
Reason: The construction (e.g., transposition swapping two distinct content-subspace V-positions while fixing others) is a standard mathematical move that uses only the precondition |dom_C(M(d))| ≥ 2 and the per-state invariants already established in the ASN. Admissibility verification consumes only S8a/S8-depth/S8-fin/D-CTG★/D-MIN★/S3★ transfer via K.μ~-FIX. No external channels needed.

## Issue 3: K.δ case (ii) k=2 sub-case A2 induction is implicit
Reason: Making the induction principle explicit (chain position in A_account(parent(t))'s emission sequence, well-founded by finite transition history) is a proof-structure restatement using machinery already present. The well-foundedness ground (finite transition history) is a property of SequentialTransitionAxiom and reachable-state framing, both already in the ASN. Internal.

## Issue 4: D-SEQ★ derivation — depth-sharing inference step is asserted without proof
Reason: The fix is making explicit the bijection k ↦ [S, 1, ..., 1, k] between {1, ..., n_S} and V_S(d), under which set inclusion V_S(d') ⊆ V_S(d) reduces to {1, ..., n'_S} ⊆ {1, ..., n_S} and forces n'_S ≤ n_S. This is elementary set theory on canonical forms already defined in the ASN.

## Issue 5: K.μ~ dependency chain Steps (A)-(E) lack explicit proofs
Reason: The substantive content of each step exists in the ASN — Step (A) in the verification matrix and S3★ analysis, Step (B) in the case-split on s_C → s_L and s_L → s_C, Steps (C)-(D) in the link-subspace fixity proof. The fix is separation and explicit per-step presentation, using only existing machinery (S3★ at both endpoints, L14, bijection equation, CL-UNIQ at Σ). Internal.

## Issue 6: L14 derivation chain inconsistency across the ASN
Reason: The decision — whether T7 is actually load-bearing in the contradiction (s_C = s_L vs SC-NEQ) or whether single-valuedness of subspace_I + SC-NEQ suffices — is a proof-analysis question about the existing derivation. T7's definition and L0's two clauses are already in the ASN; the fix is restructuring the chain heading to match what the derivation actually consumes. Internal.

## Issue 7: Verification matrix — some cells require non-trivial expansion
Reason: The fix is presentation — either expanding the matrix cells inline or adding cross-reference conventions like "[§K.μ~-Step3]" pointing to existing body paragraphs. All substantive content already exists in the ASN body; no new derivation, design intent, or implementation evidence is required.

## Issue 8: ASN size and scope coherence
Reason: This is an organizational decision about whether to split content into separate ASNs. The decision belongs to the author's judgment about presentation scope and series organization, informed by how related foundation ASNs (ASN-0036, ASN-0043, ASN-0093) were partitioned. No external channels needed — content is unchanged by splitting.
