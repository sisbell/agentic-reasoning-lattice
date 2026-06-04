# Review of ASN-0076

## REVISE

### Issue 1: E2 distinctness involving ℓ_old does not establish that ℓ_old's allocation event is itself conforming
**ASN-0076, E2 (proof)**: "By SubAllocatorBundle (ASN-0047), each K.λ step emits via a T10a-conforming sub-allocator. By L11a (LinkUniqueness, ASN-0043), distinct T10a-conforming allocation events produce distinct link addresses, so the three outputs are pairwise distinct."

**Problem**: L11a's hypothesis is that *both* members of each pair arise from T10a-conforming allocation events. The proof discharges conformance for `ℓ_new` and `ℓ_sup` ("each K.λ step emits via a T10a-conforming sub-allocator"), but `ℓ_old`'s production is *not* a step of EDITLINK — it occurred in some prior state. The sentence "the three K.λ events producing ℓ_old, ℓ_new, and ℓ_sup" silently assumes ℓ_old came from a conforming K.λ event without deriving it. The conclusions `ℓ_new ≠ ℓ_old` and `ℓ_sup ≠ ℓ_old` therefore rest on an undischarged premise.

**Required**: Add the missing step — `ℓ_old ∈ dom(Σ.L)` implies it was produced by a prior K.λ event (the only transition adding to `dom(L)` in ASN-0047's vocabulary), and L1c (LinkAllocatorConformance, ASN-0047) certifies that event is T10a-conforming. Then L11a applies to the pairs `(ℓ_old, ℓ_new)` and `(ℓ_old, ℓ_sup)`.

### Issue 2: Redundant restatement that EDITLINK is "not a primitive"
**ASN-0076, "The Composite" (closing paragraph)**: "The composite is *not* a primitive of the transition vocabulary Σ introduced in ASN-0047. It does not extend that vocabulary. It is a named pattern of two existing primitive applications, no different in kind from any other sequence of transitions a user might issue."

**Problem**: Three sentences assert one fact. "It does not extend that vocabulary" is the contrapositive restatement of "not a primitive of the transition vocabulary," and the introduction already commits this ("No new primitive is required"). This is the same statement in different words across sections — the anti-bloat pattern.

**Required**: Collapse to a single sentence; the intro already carries the commitment.

### Issue 3: E7 reconciliation restates foundation definitions that should be cited, not reproduced
**ASN-0076, E7 (Reconciliation with ASN-0098's discoverability)**: "ASN-0098 fixes `project(e, d, Σ) = {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage(e)}` and `discoverable_from(a, d, Σ) ≡ (E i : project(a, i, d, Σ) ≠ ∅)`, equivalently (LP12) `coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅`."

**Problem**: The load-bearing content of this passage is the *directional* distinction — `covers` is an inverse lookup over `Σ.L` consulting no arrangement, whereas `discoverable_from` is arrangement-conditional — together with the LP17/LP18 orphaning consequence. Re-printing the foundation formulas verbatim (project, discoverable_from, the LP12 equivalence) is restated foundation prose the reader can reach by citation. It pads the one distinction that matters.

**Required**: Replace the verbatim definitions with citations (ASN-0098 project/discoverable_from/LP12), retaining the directional contrast and the orphan/resurrection link.

## OUT_OF_SCOPE

### Topic 1: Weakest-precondition for ℓ_sup discoverability after EDITLINK
**Why out of scope**: A formal `wp(EDITLINK, discoverable_from(ℓ_sup, d, ·))` would sharpen E7/E10, but since EDITLINK performs no arrangement step (E10) the discoverability question is already governed by ASN-0098's LP12a/LP17/LP18 over a subsequent K.μ step. The mechanics of arranging an edited link's referents belong to that downstream territory, not to this composite.

VERDICT: REVISE
