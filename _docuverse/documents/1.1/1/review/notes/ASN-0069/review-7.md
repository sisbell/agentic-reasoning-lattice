# Review of ASN-0069

## REVISE

### Issue 1: K.δ's uniform precondition `parent(e) ∈ E` not discharged
**ASN-0069, "The Fork Composite"**: Both K.δ sub-case verifications discuss per-sub-case preconditions (`d_src ∈ E_doc` for sub-case A; `d_prev ∈ E ∧ ¬IsNode(d_prev) ∧ inc(d_prev, 0) ∉ E` for sub-case B) but skip K.δ Case (ii)'s uniformly required clause `parent(e) ∈ E` (ASN-0047 K.δ).
**Problem**: This conjunct is required for any K.δ Case (ii) firing. The ASN's verification chain is incomplete without it. The standards require addressing every precondition conjunct, even when the discharge is one line.
**Required**: Add explicit discharge in both sub-cases: by KDeltaParentK01 (ASN-0047), `parent(d_new) = parent(d_src)` (sub-case A) or `parent(d_prev)` (sub-case B); by P8 (EntityHierarchy, ASN-0047) applied to `d_src ∈ E` (or `d_prev ∈ E` by P1), `parent(d_src) ∈ E` (resp. `parent(d_prev) ∈ E`).

### Issue 2: K.δ's outer preconditions `ValidAddress(e)` and `¬IsElement(e)` not explicitly discharged
**ASN-0069, "The Fork Composite"**: K.δ's outer precondition is `e ∉ E ∧ ValidAddress(e) ∧ ¬IsElement(e)`. The verification addresses `e ∉ E` (freshness) and indirectly addresses `¬IsElement(d_new)` via the zeros-count argument, but never explicitly discharges `ValidAddress(d_new)` (T4-validity).
**Problem**: T4-validity is a precondition of K.δ. Without it, the K.δ firing is not authorized by ASN-0047.
**Required**: Explicitly cite T10a.4 (T4PreservationUnderDiscipline, ASN-0034) applied to A_v(d_src) — established as a T10a-conforming sub-allocator by SubAllocatorAxiom.T10aConformance (ASN-0047) — to conclude every A_v(d_src) output, including d_new, satisfies T4. Similarly, make explicit that `IsDocument(d_new)` (already derived from `zeros(d_new) = 2`) entails `¬IsElement(d_new)`.

### Issue 3: Subsequent-fork freshness argument compresses two independent facts
**ASN-0069, "The Fork Composite"**: Sub-case B's freshness derivation reads "T10a.7 (EnumerationInjectivity, ASN-0034) applied to A_v(d_src)'s sibling-stream enumeration — the next sibling tumbler is distinct from every prior emission — combined with T10a.6, which places the new emission outside every other allocator's domain."
**Problem**: T10a.7 establishes injectivity of the enumeration map: distinct indices yield distinct outputs. But concluding `inc(d_prev, 0) ∉ E` requires three independent facts: (a) T10a.7's within-allocator injectivity; (b) the SequentialTransitionAxiom (ASN-0047) ordering events so the "next" enumeration index has not yet fired — combined with P1 to show prior emissions are in E while the new one is freshly proposed; (c) T10a.6's cross-allocator disjointness. The current text conflates (a) with (b).
**Required**: Separate the three steps: (i) T10a.7 for within-allocator distinctness, (ii) SequentialTransitionAxiom + P1 for "next emission hasn't fired yet," (iii) T10a.6 for cross-allocator non-collision.

### Issue 4: V12(d)'s intersection notation collapses to a trivial set
**ASN-0069, V12(d)**: "(A a ∈ ran(M'(d_new)) ∩ ran(M(d_src)) :: (a, d_src) ∈ R'')"
**Problem**: By V4, `ran(M'(d_new)) ⊆ ran(M(d_src)|_{V_{s_C}(d_src)}) ⊆ ran(M(d_src))`, so the intersection equals `ran(M'(d_new))`. The notation suggests "shared I-addresses" is a non-trivial subset — but it isn't. The timing of `ran(M(d_src))` is also unclear: pre-fork, post-fork (V5 makes them equal), or subsequent-state-relative (which would meaningfully differ but is not stated). A reader cannot tell whether V12(d) is a content-store-level claim or a current-arrangement claim.
**Required**: Either simplify to `(A a ∈ ran(M'(d_new)) :: (a, d_src) ∈ R'')` and supply a one-line derivation (a is content-subspace-referenced in d_src at fork-time by V4; P4★ pre-fork gives `(a, d_src) ∈ R`; P2 carries it forward), or, if a subsequent-state intersection is intended, write `ran(M''(d_new)) ∩ ran(M''(d_src))` explicitly and justify the meaningfulness.

### Issue 5: V8b's "no monotonic-decay" claim requires more grounding
**ASN-0069, V8b**: "a position lost from `Π_g` via one transition may re-enter `Π_h` at a later state via restoration on both sides… K.μ⁺ may re-install a previously-removed v ↦ a binding (admissible whenever a ∈ dom(C), which P0 of ASN-0047 ensures permanently for every a ∈ ran(M'(d_new)))."
**Problem**: K.μ⁻ removes a suffix per its per-subspace-suffix-retention precondition (ASN-0047). K.μ⁺ extends contiguously per D-CTG★/D-MIN★. Re-installing a specific binding `v ↦ a` at a specific V-position requires that V-position to be the next contiguous position under D-SEQ★ at the time of the K.μ⁺. The ASN claims re-installation is "admissible whenever a ∈ dom(C)" — but this overlooks the structural constraints on *which* V-position can be re-added. For example, if K.μ⁻ retains only positions 1..3 in subspace s_C and the operator wants to restore [s_C, ..., 7], the intermediate positions 4, 5, 6 must be filled first; restoration is not a single-step operation for arbitrary positions.
**Required**: Either restrict the claim to V-positions that *can* be restored (next contiguous position from the current retention), or note explicitly that arbitrary positions require multiple intervening K.μ⁺ steps to satisfy D-CTG★.

VERDICT: REVISE
