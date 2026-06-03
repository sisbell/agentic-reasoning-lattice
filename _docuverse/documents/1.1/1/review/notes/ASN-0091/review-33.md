# Review of ASN-0091

## REVISE

### Issue 1: K.μ~ admissibility clause (ii) is misstated, leaving the REARRANGE_K → K.μ~ realization incomplete

**ASN-0091, "K.μ~ Admissibility Clauses" / identity-case discussion in "REARRANGE as Vstream-Only Operation"**: "ASN-0047's K.μ~ admissibility clause (ii) (π ≠ id) is the formal vehicle confirming this property; it does not perform additional exclusion beyond what the cut-sequence structure already guarantees."

**Problem**: ASN-0047's K.μ~ admissibility clause (ii) is *not* `π ≠ id`. The foundation states it as **`M'(d) ≠ M(d)`** (non-trivial *net effect* on the arrangement function), and ASN-0047's K.μ~ precondition is "`M(d)|_{dom_C}` takes at least two distinct values" (a constraint on the *range*). The ASN's argument only establishes that the cut-sequence makes π a non-identity *permutation* (`π(c₀) = c₀ + w_β > c₀`). It does **not** establish `M'(d) ≠ M(d)`. These come apart whenever the affected content range is value-uniform — admitted by foundation S5 (UnrestrictedSharing). Concretely: content arrangement `{[1,1] ↦ a, [1,2] ↦ a}`, pivot cut `([1,1],[1,2],[1,3])`, gives R-P1 `M'([1,1]) = M([1,2]) = a` and R-P2 `M'([1,2]) = M([1,1]) = a`, so `M'(d) = M(d)` while π swaps the two positions (π ≠ id). Clause (ii) fails and the K.μ~ precondition fails, yet R-PRE is fully satisfied, so REARRANGE_K is invokable on an input its claimed realizer (K.μ~) rejects. The same collapse arises even with ≥2 distinct values overall (e.g. `{[1,1]↦a, [1,2]↦a, [1,3]↦b}` with the affected range confined to the value-uniform prefix), so K.μ~'s precondition being met does not rescue the *specific* cut-driven π.

A related conflation appears in the same passage: "The existence precondition `|dom_C(M(d))| ≥ 2` ... is forced by R-PRE(iv) ∧ CS2." `|dom_C(M(d))| ≥ 2` is a *domain*-cardinality bound (≥ 2 positions); K.μ~'s precondition is a *distinct-value* bound (≥ 2 I-addresses in the range). R-PRE(iv) ∧ CS2 forces the former but not the latter.

**Required**: Either (a) give REARRANGE_K an explicit non-triviality precondition (the cut rearrangement must change `M(d)`, i.e. `M(d)` restricted to the affected range is not value-uniform), and show this discharges clause (ii); or (b) handle the collapse case (π ≠ id, `M'(d) = M(d)`) as a degenerate no-op explicitly — noting it yields `Σ' = Σ` and so satisfies every RE-* claim trivially, and that K.μ~ is therefore not the realizer in that case. Correct the parenthetical "(π ≠ id)" to the actual clause-(ii) statement `M'(d) ≠ M(d)`, and separate domain-cardinality from distinct-value cardinality.

### Issue 2: RA-π signature is stated two inconsistent ways

**ASN-0091, definition vs. Claims-Introduced table**: The body fixes the signature as `π : dom(Σ.M(d)) → dom(Σ'.M(d))` and argues at length that this "is type-correct without presupposing any equality of these two domains." The Claims Introduced table writes RA-π as "`π : dom(M(d)) → dom(M(d))` ... for every v ∈ dom(M(d))."

**Problem**: The table collapses the pre- and post-state domains into one (`dom(M(d)) → dom(M(d))`), presupposing exactly the equality the body deliberately decouples from RA-π (deferring it to RA-dom). A reader taking the table as the canonical statement of RA-π loses the decoupling the body relies on in RE-ran/RE-μ/RE-proj/RE-subpres/RE-sub type-correctness.

**Required**: Make the table's RA-π signature match the body: `π : dom(Σ.M(d)) → dom(Σ'.M(d))`.

## OUT_OF_SCOPE

### Topic 1: Intermediate-state semantics of the K.μ⁻ + K.μ⁺ decomposition

K.μ~ is a named composite passing through an intermediate contracted state where dom(M(d)) shrinks; links projecting onto dropped positions transiently lose discoverability before re-extension. This ASN's claims are stated between endpoints Σ and Σ', which is correct for its purpose; intermediate-state observability belongs to a separate treatment.

### Topic 2: Link-subspace rearrangement and depth m ≥ 3

CS3 fixes the cut subspace to content (S = s_C) and ASN-0084 scopes REARRANGE_K to depth-2 V-positions. Rearrangement semantics on the link subspace and at m ≥ 3 are correctly deferred (the ASN already records the link-subspace case as an Open Question).

VERDICT: REVISE
