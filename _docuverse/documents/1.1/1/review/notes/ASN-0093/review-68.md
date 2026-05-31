# Review of ASN-0093

This is a late-stage, mathematically tight note. I traced the core obligations — anchor construction (`d → inc(d,2)=b_C(d) → inc(b_C(d),0)=b_L(d) → inc(·,1)`), the first-emit/subsequent-emit branches, freshness (cross-document via T10, cross-subspace via T7, within-document via ChainEnumerationInjectivity), and the simultaneous-induction matrix — and found the proof content sound, including the prefix-comparable (`d ≺ d'`) cross-document case. The findings below are accretion/duplication, per the anti-bloat classifier.

## REVISE

### Issue 1: Worked-example Steps 6 and 7 re-derive Steps 2 and 3 verbatim
**ASN-0093, Worked example, Steps 6–7 vs Steps 2–3**: Step 2 — "Admissibility: TA5a at `k = 2` requires `zeros(d) ≤ 2`; M0 gives `zeros(d) = 2 ≤ 2`, satisfied — hence `t₁` is T4-valid"; Step 6 — "Admissibility: TA5a at `k = 2` requires `zeros(d') ≤ 2`; M0 gives `zeros(d') = 2 ≤ 2`, satisfied — hence `t₁` is T4-valid."
**Problem**: The per-step TA5a admissibility prose in Steps 6 (content first-emit under `d'`) and 7 (link first-emit under `d'`) is word-for-word the prose of Steps 2 and 3 with `d → d'`. The admissibility *reasoning* (which TA5a case fires, which side condition M0 discharges) is parametric in `d` and identical; only the concrete tumblers differ. This is the "two paragraphs say the same thing in different words" pattern, compounded across the second document. The genuinely new content in Steps 5–9 — multi-component document field `D(d') = [5,3]`, prefix-comparable and prefix-incomparable cross-document disjointness — does not require re-running the anchor-admissibility citations.
**Required**: In Steps 6/7, state the concrete resulting tumblers and the cross-document/cross-subspace freshness (the new material), and cite Steps 2/3 for the identical per-step TA5a admissibility rather than re-deriving it.

### Issue 2: C1b's Source-column parenthetical restates the intro's "what's new" claim
**ASN-0093, Properties Introduced (C1b row)** vs **opening paragraph**: C1b source — "content-side analog of L1b (ASN-0036 carries no content-side `#E(a) ≥ 2`)"; intro — "The substrate adds four content-side invariants that the inherited models do not carry — C1b (content element-field depth) ... — proved within this note."
**Problem**: The intro already enumerates the four added content-side invariants and states they are absent from the inherited models. The C1b Source-column parenthetical repeats that ASN-0036 lacks `#E(a) ≥ 2` — a rationale ("why this invariant is added"), not a provenance, duplicated from the intro. The sibling rows (C1c, C2) correctly give bare provenance ("content-side analog of L1c / L1a") without re-justifying.
**Required**: Drop the parenthetical from C1b's Source cell to match C1c/C2; the intro carries the "not inherited" accounting.

## OUT_OF_SCOPE

### Topic 1: Document-allocation discipline for K.σ
K.σ registers any T4-valid `zeros=2` tumbler with no allocator-conformance precondition relative to existing documents. The substrate's guarantees (cross-document disjointness, SD) hold regardless, so this is not an error here — who may baptize documents (the node/user allocator discipline) is legitimately a higher-layer concern.

VERDICT: REVISE
