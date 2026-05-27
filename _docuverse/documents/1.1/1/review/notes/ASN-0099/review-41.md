# Review of ASN-0099

## REVISE

### Issue 1: Strengthening 1's witness is structurally incomplete
**ASN-0099, F4 (MatchFormulaDesignJustification)**: "Strengthening 1 — Containment from coverage to query (`coverage ⊆ I`). Witness: slot `i` with one canonical span `(α, δ(1, #α))`, so `coverage = {t : α ≼ t}` ... but `coverage ⊄ I` since `α.0 ∈ coverage` ... Strengthening excludes `a`."

**Problem**: The strengthening predicate read as a link-level slot-existential is `(E i : 1 ≤ i ≤ |L(a)| : coverage(eᵢ) ⊆ I)`. L3 (ASN-0043) permits empty non-type slots (only slot 3 is mandatory non-empty), and `∅ ⊆ I` holds vacuously. The witness specifies only "slot i" without constraining other slots. If slot 1 or 2 is empty (a configuration K.λ admits since L3 only requires slot 3 non-empty), the existential is satisfied at the empty slot regardless of I, so the strengthening admits the link — directly contradicting "Strengthening excludes a". The per-slot argument given (that slot i's coverage is not contained in I) does not discharge the link-level conclusion. Strengthenings 2 (`I ⊆ coverage`) and 3 (`|coverage ∩ I| ≥ k > 1`) are unaffected because empty coverage fails their tests when `I ≠ ∅` and `k > 1` respectively.

**Required**: Either (a) construct the witness link with all slots populated by non-empty canonical spans whose coverages are not subsets of `I` — e.g., slot 1 = `(β, δ(1, #β))` with `β ⋠ α`, slot 2 = `(γ, δ(1, #γ))` with `γ ⋠ α`, slot 3 = `(α, δ(1, #α))` — so every slot's coverage strictly exceeds `{α}` and the existential rejects; or (b) restate the strengthening predicate to exclude vacuous satisfaction, e.g., `(E i : coverage(eᵢ) ⊆ I ∧ coverage(eᵢ) ≠ ∅)`.

### Issue 2: F4 misframes F1's relationship to AND-of-ORs
**ASN-0099, F4**: "the AND-of-ORs existential structure: ∃ per endset (one span witnesses), ∧ across endsets (every endset participates). F1's slot-existential form lives inside this family."

**Problem**: F1 = `(E i : coverage(eᵢ) ∩ I ≠ ∅)` is OR-across-slots, not AND-across-slots. LM 4/58's "one span of each endset" prescribes AND-across-endsets, which structurally matches `findlinks_filtered` (AND across constraints), not F1. The ASN itself later confirms `findlinks(I, Σ) = ⋃_i findlinks_filtered({(i, I)}, Σ)` — F1 is a derived OR-relaxation of `findlinks_filtered`, not a member of the AND-of-ORs link-level family. F4's "lives inside" phrasing elides this relaxation and conflates two distinct design decisions.

**Required**: Distinguish (a) the per-span overlap test `coverage ∩ I ≠ ∅`, which is the LM 4/58-anchored choice for the per-endset existential (spans-monotonicity), from (b) the across-slots quantifier (OR in F1 vs AND in `findlinks_filtered`), which is a separate reader-facing surface choice. Clarify that `findlinks_filtered` is the direct AND-of-ORs realization and F1 is its OR-across-slots relaxation, justified by the unfiltered query "is any slot a witness?".

VERDICT: REVISE
