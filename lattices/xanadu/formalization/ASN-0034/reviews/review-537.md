# Regional Review — ASN-0034/ZPD (cycle 1)

*2026-04-24 14:45*

### T0 comprehension axiom unused within the ASN
**Class**: OBSERVE
**Foundation**: T0 (CarrierSetDefinition)
**ASN**: T0's *Axiom* bullet includes the comprehension clause `(A p ∈ ℕ : p ≥ 1 : (A r : {j ∈ ℕ : 1 ≤ j ≤ p} → ℕ :: (E t ∈ T :: #t = p ∧ ...)))` with prose framing it as licensing the "construction of new tumblers from a length and a component map"
**Issue**: No downstream claim in this ASN constructs a tumbler from a length-and-map. T1, T3, Divergence, and ZPD all quantify over pre-existing tumblers or manipulate component maps on an index domain (ZPD's padded projections are indexed maps, not tumblers). The comprehension axiom is presumably export infrastructure for dependents, but within ASN-0034 it carries no load — the consumers cited in T0's own prose do not appear.

### T1 trichotomy Case 3 re-derives a split it already has in hand
**Class**: OBSERVE
**Foundation**: T1 (LexicographicOrder), part (b) Case 3
**ASN**: "Both clauses force `m ≠ n`: (β) gives `m + 1 ≤ n`, hence `m < n` via NAT-addcompat's `m < m + 1`; (γ) gives `n < m` symmetrically. So `a ≠ b` by T3. NAT-order's trichotomy at `(m, n)` resolves `m ≠ n` into `m < n ∨ n < m`. If `m < n`, then `k = m + 1 ≤ n`..."
**Issue**: The proof has just established `m < n` (under β) and `n < m` (under γ) directly, making the invocation of trichotomy on `(m, n)` a reshuffle rather than new information. The subsequent "If `m < n`" / "If `n < m`" branches coincide with β / γ, so the trichotomy step is a cosmetic rebranding of the already-named sub-case.

### Divergence body restates symmetry already implied by the case structure
**Class**: OBSERVE
**Foundation**: Divergence
**ASN**: "The function is symmetric: `divergence(a, b) = divergence(b, a)`. In case (i), the qualifying conjunction is invariant under operand swap ... In case (ii), swapping `(a, b)` exchanges sub-cases (ii-a) and (ii-b); both select one-plus the shorter tumbler's length."
**Issue**: The symmetry argument is correct, but the body's listing of which conjuncts swap trivially (`∧`-commutativity, `≠`-symmetry, `=`-symmetry) is meta-justification more than reasoning; the content is essentially "the definition mentions `a` and `b` symmetrically." A tighter formulation would state the symmetry postcondition and note that the qualifying predicate is manifestly symmetric in `(a, b)`.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 758s*
