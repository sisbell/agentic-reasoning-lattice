# Review of ASN-0051

## REVISE

### Issue 1: Structural identity formula incorrect in general

**ASN-0051, Worked Example, "Attribution of the 4 → 2 gap (witness-specific)" paragraph**: "The cross-block sharing's quantitative footprint is the term-cardinality inflation, captured by the structural identity `Σ_{j,k} |term_{j,k}| − |π_text(e, d)| = Σ_{a ∈ π_text(e, d)} (m_a − 1) · s_a`"

**Problem**: The formula is incorrect in general. For each `a ∈ π_text(e, d)`, the I-address appears in exactly `s_a · m_a` decomposition terms (one per (covering span, containing block) pair), each contributing 1 to its term's cardinality. So `Σ_{j,k} |term_{j,k}| = Σ_a s_a · m_a`, and inflation `Σ_{j,k} |term_{j,k}| − |π_text| = Σ_a (s_a · m_a − 1)`. The ASN's formula `Σ_a (m_a − 1) · s_a = Σ_a s_a · m_a − Σ_a s_a` matches the correct formula only when `Σ_a s_a = |π_text|`, i.e., `s_a = 1` for every `a`. Counterexample: 2 spans both covering a single I-address `a` in 1 block (s_a = 2, m_a = 1). Correct inflation: `s_a · m_a − 1 = 1`. ASN formula: `(m_a − 1) · s_a = 0 · 2 = 0`. The ASN explicitly claims the identity is "the structural identity... through which any witness's term-vs-fragment count gap can be read" — overstated.

**Required**: Either restrict the identity's stated scope to "witnesses where each I-address in `π_text(e, d)` is covered by exactly one span", or correct the formula to `Σ_a (s_a · m_a − 1)`.

### Issue 2: Conflation of term-cardinality inflation with term-vs-fragment count gap

**ASN-0051, Worked Example, same paragraph**: "the structural identity above gives the general decomposition through which any witness's term-vs-fragment count gap can be read"

**Problem**: The structural identity computes `Σ_{j,k} |term_{j,k}| − |π_text(e, d)|` — the term-cardinality inflation. This is *not* the term-vs-fragment count gap, which is `(m · p) − (fragment count)`. They coincide in the worked example by coincidence (both equal 2), but diverge in general. Counterexample: m=1 span with coverage `{a}`, p=2 blocks each containing `a` in their I-extents (achievable via non-injective M(d) with a forced inter-block split via M7 I-adjacency failure). Then: `Σ|term| = 2`, `|π_text| = 1`, inflation = 1; but m·p = 2, fragment count = 2 (per the per-block Maximal Endset Fragment definition), gap = 0. Inflation = 1, gap = 0 — different. The gap is governed by mechanisms (a) and (b) of the SV11 biconditional; the inflation is a separate quantity that records non-injective sharing's footprint on `Σ|term|`.

**Required**: Clarify that the identity captures term-cardinality inflation, not term-vs-fragment count gap; or remove the "term-vs-fragment count gap can be read" claim. The two are independent quantities.

### Issue 3: Informal hedge for (m ≥ 4, p = 2) and (m = 2, p ≥ 4) attainment

**ASN-0051, SV11 attainment scope discussion**: "the construction-pattern generalisation to (m ≥ 4, p = 2) by enlarging both blocks to size ≥ 2m − 1 with m single-element spans placed at non-adjacent within-block offsets" and "We do not enumerate explicit p ≥ 4 constructions, but the procedure is mechanical".

**Problem**: The formal "Inductive lift schema for (m ≥ 3, p ≥ 3) attainment" with lifts (α) and (β) starting from explicit base witnesses W(3, 3) and W(4, 3) is rigorous. The (m ≥ 4, p = 2) and (m = 2, p ≥ 4) cases use informal "construction-pattern generalisation" language. The lift (α) is well-defined for any p ≥ 2 and lift (β) is well-defined for any m ≥ 2 — the schema could be extended to cover these cases by iterating from explicit W(2, 2), W(3, 2), and W(2, 3) (all already provided). The hedge is therefore unnecessary.

**Required**: Either extend the formal lift schema to (m ≥ 3, p = 2) and (m = 2, p ≥ 3) explicitly via (α) and (β) starting from the existing explicit base witnesses, or note that the procedure is identical to (α)/(β) and explicitly bound the schema's applicability.

## OUT_OF_SCOPE

The ASN identifies its open questions explicitly. The Scope declaration places link type semantics and inter-server protocol (BEBE) out of scope — appropriate. Broader-level spans (k ≤ p₃) are deferred to ASN-0034's address-hierarchy treatment — appropriate.

VERDICT: REVISE
