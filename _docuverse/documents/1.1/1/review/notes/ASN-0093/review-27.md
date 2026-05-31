# Review of ASN-0093

This ASN is mathematically sound — I checked the anchor constructions (`b_C(d) = inc(d,2)`, `b_L(d) = inc(b_C(d),0)`), the B6-validity boundary (zeros=3 at depth 1, the tight `3 ≤ 3` case), the C1c/L1c chain admissibility (TA5a side conditions all discharged by M0's `zeros(d)=2`), the simultaneous-induction non-circularity, and the worked example's nine steps (Step 5 `d ≺ d'` separator divergence at position 6, Step 8 `inc(ℓ,0)` at position 8). All correct. The findings below are bloat patterns the `anti-bloat` classifier asks me to surface at source.

## REVISE

### Issue 1: Use-site inventories duplicating the discharge matrix

**ASN-0093, StoreT4Validity corollary**: "This corollary discharges the T4-validity precondition of T7 ... **in particular, in the L14 discharge (matrix below) and in the FirstEmissionFreshness lemma below against `dom(L)`.**"
**ASN-0093, Properties table, StoreT4Validity row**: "**Used to discharge T7's precondition in the L14 derivation and in the FirstEmissionFreshness lemma against `dom(L)`.**"

**Problem**: Both enumerate downstream consumers of the corollary — the exact "definition's introduction enumerates downstream consumers" pattern. The L14 discharge note and FirstEmissionFreshness already cite StoreT4Validity at their own sites; the consumer list here is redundant and must be re-synced whenever a consumer moves. The same shape recurs in the K.α/K.λ "Derived structural facts" lists, whose parenthetical invariant tags (`— C1`, `— L0`, `— C1b`, `— C2`, `— L14`) restate the per-(invariant, transition) discharge matrix.
**Required**: State the corollary's conclusion once; let consuming sites cite it. Drop the consumer enumeration from the corollary sentence and the table row. In the "Derived structural facts" lists, keep the consequences (`zeros=3`, `E(·)₁=s_C`, …) and drop the invariant tags, since the matrix is authoritative.

### Issue 2: Duplicated non-circularity justification in FirstEmissionFreshness

**ASN-0093, FirstEmissionFreshness, content case against `dom(L)`**: "for the new key `a` we read `E(a)₁ = s_C` from the FirstEmission lemma's structural form ... **rather than from L0, since `a` is not yet committed at the firing event and invoking L0 at `Σ'` would be circular under the simultaneous induction (L0 at `Σ'` itself depends on FirstEmissionFreshness).**"
**ASN-0093, FirstEmissionFreshness, link case against `dom(C)`**: "for the new key `ℓ` we read `E(ℓ)₁ = s_L` from the FirstEmission lemma's structural form ... **rather than from L0, by the same non-circularity reasoning as the content case (`ℓ` is uncommitted at the firing event, so L0 at `Σ'` is unavailable).**"

**Problem**: The non-circularity point is genuine and load-bearing, but it is stated twice — the "two paragraphs say the same thing in different words" pattern. The reader processes the same justification on both passes.
**Required**: State the non-circularity discipline once (e.g., a single sentence at the lemma head: "throughout this proof, new-key subspace identifiers are read from FirstEmission's structural form, not from L0 at `Σ'`, which would be circular"), then let both cases simply cite the structural form.

### Issue 3: Defensive applicability padding on ChainPrefixExtension

**ASN-0093, ChainPrefixExtension, *Quantifier scope***: "S1 ranges over the abstract stream `S(b_·(d), 1)` at every index `n ≥ 1`, independent of which elements are committed to `dom(C)` (resp. `dom(L)`) at `Σ`; in particular the prefix relation holds at a freshly emitted stream element `inc(a_prev, 0)` (resp. `inc(ℓ_prev, 0)`) before it is committed."

**Problem**: This is a defensive justification of why the citation applies, attached to a CITATION whose conclusion (`p ≼ cₙ` for all `n ≥ 1`) already makes the index-range explicit. The "independent of which elements are committed ... before it is committed" framing pre-empts an objection rather than advancing the claim — the kind of meta-prose a precise reader skips past. S1's universal quantifier over `n ≥ 1` says this directly.
**Required**: Delete the sub-note. If the subsequent-emit freshness argument needs the prefix relation at an uncommitted element, cite S1 there inline; the quantifier carries the point without a standalone defense.

## OUT_OF_SCOPE

### Topic 1: Link-withdrawal formulation taxonomy in Open Questions
The first open question enumerates three withdrawal formulations (value transition / arrangement-side retraction / embedded marker) and adjudicates which touches L12. Link withdrawal is explicitly OUT OF SCOPE per the Scope list, so this is correctly deferred — but the three-way taxonomy is more design-essay than open question. Not an error in this ASN; noted only because the elaboration leans toward content the withdrawal ASN should carry. A one-line pointer ("withdrawal must decide whether to weaken L12's value-equality clause") would suffice.

VERDICT: REVISE
