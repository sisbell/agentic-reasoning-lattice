# Review of ASN-0047

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Fork arrangement order preservation
**Why out of scope**: J4 constrains `ran(M'(d_new)) ⊆ ran(M(d_src))` — the set of I-addresses — but does not specify whether the V-position ordering of d_new must match d_src. The open question on fork arrangement invariants correctly identifies this as future work.

### Topic 2: Link-subspace withdrawal mechanism
**Why out of scope**: The ASN correctly identifies that D-CTG + link-subspace fixity under K.μ~ constrains link-subspace contractions to suffix truncations, and that Nelson's design suggests an inactive-status mechanism rather than arrangement removal. The precise withdrawal semantics are a separate concern from the transition taxonomy established here.

### Topic 3: Additional subspace identifiers
**Why out of scope**: S3★-aux establishes that all V-positions have subspace s_C or s_L — exactly two subspaces. If a future ASN introduces additional subspaces (e.g., for metadata), S3★-aux, the K.μ⁺ amendment, and the completeness argument would all require extension. This is new territory.

---

**Analysis notes.** I traced every proof in detail. The key results that required the most careful verification:

- **Link-subspace fixity under K.μ~**: The argument chain — S3★ at the output established independently of fixity (by K.μ⁻ + K.μ⁺ decomposition), then π forced to map dom_L into dom_L (by S3★ + L14 + SC-NEQ), then cardinality contradiction if r ≥ 1 link-subspace positions were removed — is airtight. The logical ordering avoids the apparent circularity: S3★ preservation does not depend on fixity, but fixity depends on S3★.

- **K.μ~ when dom_C(M(d)) = ∅**: The contradiction argument (K.μ⁻ removes r link-subspace positions → K.μ⁺ must add r content-subspace positions → S3★ forces these to map into dom(C) → but K.μ~ definition gives M'(d)(π(v)) = M(d)(v) ∈ dom(L) → L14 contradiction) correctly uses S3★ at the pre-state from the inductive hypothesis.

- **ExtendedReachableStateInvariants two-layer structure**: The partition into elementary invariants (preserved per-step) and composite invariants (P4★, P7a — violated at intermediate states, restored at composite boundaries by J1★ and J0+J1★ respectively) is sound. Every invariant in the conjunction is verified for every transition kind.

- **K.μ~-FIX derivation**: D-SEQ at both input and output, equal cardinality from the bijection, and per-subspace preservation yield V_S(d') = V_S(d) for each subspace S — making π a permutation of a fixed domain.

- **D-CTG at intermediate states of K.μ~ decomposition**: The n' = 0 decomposition (remove all content-subspace positions, re-add at permuted positions) satisfies D-CTG/D-MIN vacuously at the intermediate state. Valid decomposition always exists.

The worked examples are thorough: the fork example exercises J0, J1, J2, J3, J4, P4, P5, P6, P7, P8; the link example verifies S3★, CL-OWN, L14, and demonstrates link-subspace fixity on concrete tumbler values.

VERDICT: CONVERGED
