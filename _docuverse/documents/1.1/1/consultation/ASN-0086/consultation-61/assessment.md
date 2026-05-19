# Channel Assignment — ASN-0086 review-61

**Date:** 2026-05-19 10:20

## Issue 1: ASN-0093 foundation not consulted; emission primitives reinvented
Reason: Need Gregory to confirm what ASN-0093 actually defines (K.σ/K.α/K.λ and their preconditions, especially whether K.λ embeds the sibling-frontier discipline). Need Nelson to confirm whether ASN-0086 was intended to layer over ASN-0093 or operate at the more abstract ASN-0043 level.
Nelson question: Was ASN-0086 intended to layer directly over ASN-0093's K-operations, or to operate at the strictly more abstract ASN-0043 substrate with its own emission primitives?
Gregory question: Does ASN-0093 define K.σ/K.α/K.λ as the primitive operations corresponding to ASN-0086's classes (i)/(ii)/(iii), and do K.λ's preconditions impose the sibling-frontier discipline (first emission at d.0.s_L.1, subsequent at inc(ℓ_prev, 0))?

## Issue 2: Setup hypothesis duplicates ASN-0093 L0
Reason: Need Gregory to confirm that ASN-0093's L0 already states `(A a ∈ dom(C) :: E(a)₁ = s_C)`, making the Setup hypothesis a citation rather than an assumption.
Gregory question: Does ASN-0093's L0 (SubspacePartition) state `(A a ∈ dom(C) :: E(a)₁ = s_C)`, equivalent to ASN-0086's Setup hypothesis under `subspace_I(a) = E(a)₁`?

## Issue 3: Subspace-distinctness hypothesis duplicates SubspaceConventionAxiom
Reason: Need Gregory to confirm that ASN-0093's SubspaceConventionAxiom posits `s_C = 1 ∧ s_L = 2` and that `s_C ≠ s_L` is named as a consequence (SC-NEQ).
Gregory question: Does ASN-0093's SubspaceConventionAxiom posit `s_C = 1 ∧ s_L = 2`, and is `s_C ≠ s_L` explicitly named as the SC-NEQ consequence in ASN-0093?

## Issue 4: L1cWitnessOnly axiom is restated content
Reason: Need Gregory to confirm whether ASN-0043's L1c statement already commits to a witness-only reading or leaves room for an operational re-execution reading that the new axiom would rule out.
Gregory question: Does ASN-0043's L1c, as stated, already commit to a witness-only reading of its existential, or does its phrasing leave room for an operational re-execution requirement that L1cWitnessOnly would rule out?

## Issue 5: Definition of `→` reinvents foundation operations
Reason: Need Gregory to confirm that ASN-0093 publishes K.σ/K.α/K.λ with frame conditions covering the three primitive classes, including T10a's runtime activation chain (via SubAllocatorAxiom and its lemmas).
Gregory question: Does ASN-0093 publish K.σ/K.α/K.λ with explicit frame conditions covering document allocation, content emission, and link emission — including SubAllocatorAxiom and its lemmas to make T10a's runtime activation chain explicit?

## Issue 6: R0a/R0a-Cor1 inductive argument's discipline-propagation step lacks explicit Σ_D closure proof
Reason: Pure proof-restructuring within ASN-0086 — either unpack the closure argument using R0a at Σ plus T10a sibling lemmas, or recast Σ_D via an externally-stated atomic discipline predicate. Both options use machinery already in the ASN.

## Issue 7: Stage 1 of R0a's cross-home argument relies on symmetry sketch
Reason: Pure expositional issue — either restate the swapped derivation or identify the symmetry as a one-line variable-substitution. Derivable from the ASN's own argument.

## Issue 8: Worked sketch does not exercise R0 Case A's first-emission construction
Reason: Pure exposition — add a Case A walkthrough using R0 Step 2's already-detailed three-stage chain construction. No external consultation needed.

## Issue 9: R7a's conformance scope hidden in proof's opening, not in the claim
Reason: Pure exposition — lift the conformance assumption from the proof body into R7a's precondition statement. Internal restructuring only.

## Issue 10: Definition of `Σ.L`-affecting effect lacks a concrete witness for the non-trivial branch
Reason: Pure exposition — add an m=4 worked decomposition (two fresh documents, each with an initial link) using R7a's existing iteration construction.

## Issue 11: WP Case 1 conjunct SFD(Σ) load-bearing but not formally specified
Reason: Formalizing SFD as a checkable predicate is internal to ASN-0086's existing machinery — the Implementation Notes describe the discipline informally, and the formal specification can be expressed as a trajectory-level predicate over class-(iii) steps without external input.
