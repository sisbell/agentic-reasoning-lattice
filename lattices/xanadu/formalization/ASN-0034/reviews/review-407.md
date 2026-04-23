# Regional Review — ASN-0034/TA5 (cycle 1)

*2026-04-23 01:07*

### Equality substitution under `<` — disclaimed but used
**Class**: REVISE
**Foundation**: NAT-order (stated-properties inventory) and NAT-zero (meta-prose).
**ASN**: NAT-zero's body: *"this route avoids substituting equals under `<`, a step not among NAT-order's stated properties."* T1 part (c) Case `k₂ < k₁`, case-(ii) branch: *"the second substitutes `k₁` for `n` in `n < k₂` to yield `k₁ < k₂`."* T1 part (b) Case 3: *"(β) gives `m + 1 ≤ n`, hence `m < n` via NAT-addcompat's `m < m + 1`"* — the equality branch of `m+1 ≤ n ⟺ m+1 < n ∨ m+1 = n` requires substituting `n` for `m+1` in `m < m+1`.
**Issue**: NAT-zero's prose explicitly declares that rewriting `<` under equality is not a stated NAT-order property (and restructures its own derivation to avoid it). T1's trichotomy and transitivity proofs then silently use precisely this step in multiple places. Either the step is admissible — in which case NAT-zero's disclaimer is wrong and the detour there is unmotivated — or it is not admissible, in which case T1's proof has gaps at each occurrence.
**What needs resolving**: Decide whether indiscernibility of equals under `<` is available. If yes, NAT-zero's disclaimer and detour should be removed. If no, NAT-order must export (or depend on a carrier of) the property, and the T1 uses must cite it — or be rerouted as NAT-zero was.

### TA5 Depends miscites NAT-zero as premise for NAT-discrete
**Class**: REVISE
**Foundation**: NAT-discrete axiom — `m < n ⟹ m + 1 ≤ n` (strict antecedent).
**ASN**: TA5 *Depends*: *"NAT-zero (NatZeroMinimum) — `0 ∈ ℕ` for the `k − 1` field separators; `0 ≤ k` as premise for NAT-discrete."* And the proof text: *"NAT-zero (`0 ≤ k`) and NAT-discrete (instantiated at `m = 0`) together sharpen `k > 0` to `k ≥ 1`."*
**Issue**: NAT-discrete's antecedent is strict `m < n`, not `m ≤ n`. The premise being discharged at `m = 0, n = k` is `0 < k`, which is already the case hypothesis `k > 0`. The `0 ≤ k` citation is spurious (and is not even NAT-zero's consequence, which is `¬(n < 0)`). The role NAT-zero actually plays here is supplying `0 ∈ ℕ` so `m := 0` is a legal instantiation — that role is already listed separately.
**What needs resolving**: Remove the `0 ≤ k` premise claim; keep only the `0 ∈ ℕ` role, and let `k > 0` discharge NAT-discrete's strict antecedent directly.

### Meta-prose around axioms explains structure rather than content
**Class**: OBSERVE
**ASN**: NAT-closure's paragraph (*"The axiom slot introduces `+` before constraining it… the same register NAT-order uses to posit `<`… no circularity arises because NAT-zero depends on NAT-order rather than on NAT-closure"*); NAT-addcompat's closing paragraph (*"Both foundations are declared in the Depends slot so that the axiom body can be read without silently importing them"*); NAT-discrete's analogous tail; NAT-zero's justification paragraph for the *Consequence* export.
**Issue**: The reviser-drift pattern flagged in the instructions: prose around an axiom explaining why the axiom is structured this way, why the Depends list is needed, why no circularity arises. A reader working forward from `+ : ℕ × ℕ → ℕ; 1 ∈ ℕ; 0 + n = n` does not need the paragraph defending that shape.

### T1 part (c) Case `k₂ < k₁`: "components below k₁" is loose
**Class**: OBSERVE
**ASN**: T1 transitivity, Case `k₂ < k₁`: *"Since `k₂ < k₁` and `a` has components below `k₁`, `k₂ ≤ m`."*
**Issue**: The conclusion `k₂ ≤ m` is reached differently depending on which T1 clause underwrites `a < b`. In case (i) `k₁ ≤ m` gives `k₂ < k₁ ≤ m` directly. In case (ii) `k₁ = m + 1`, so `k₂ < m + 1`, which requires NAT-discrete contrapositively (as the Depends list actually catalogs). The prose collapses these into one hand-wavy step; the Depends catalog is more precise than the proof itself.

VERDICT: REVISE
