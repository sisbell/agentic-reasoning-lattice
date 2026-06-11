# Review of ASN-0121

The core of this ASN holds up well under checking: the FL-DEF forcing argument is genuinely tight (the R_min/R_max slack analysis is correct), the `nullified`-monotonicity bridge across the full ASN-0047 vocabulary is properly assembled from F-PRES + R6a, all three FL-WP derivations are biconditionals whose conjuncts I verified are pre-state predicates (including the easy-to-miss ⊆ direction of the nullified equation in case (c), which the ASN correctly notes R6b alone does not supply), and Traces 1–5 and 7 compute correctly — I re-derived the frontier addresses, the prefix-incomparability claims, the `p ⊕ ℓ = [1,0,1,0,2,1,1,1]` example, and the nullified sets, and they all check. The remaining issues are below.

## REVISE

### Issue 1: `findlinks` shadows a foundation symbol with different semantics
**ASN-0121, "The answer is forced" (FL-DEF)**: "`findlinks(q, Σ) = { a ∈ addressable(Σ) : sat(a, q, Σ) }`"
**Problem**: ASN-0127 (foundation) already defines `findlinks(I, Σ) ≡ {a ∈ dom(Σ.L) : matches(a, I, Σ)}` (F-FIND), and the two operations sharing the name disagree on substance, not just signature: (i) 0127's `matches` is slot-agnostic — it existentially quantifies over *all* slots `1 ≤ i ≤ |Σ.L(a)|`, including type and higher slots — while this ASN's `sat` is positional over the first three; (ii) 0127's comprehension ranges over the full `dom(Σ.L)` with no nullification filter, while FL-DEF ranges over `addressable(Σ)`; (iii) consequently the two have *opposite* dynamic behavior — 0127's E-MONO makes its `findlinks` monotone across `→*`, whereas this ASN's shrinks under retraction (FL-WP(c), Trace 4). The collision is live inside this very document: FL-STB routes through 0127's F-CIL, and the FL-STB section discusses `findlinks_V`, whose second phase *is* 0127's `findlinks`. A reader composing the extracted claim sets gets two incompatible theorem families under one symbol. Relatedly, the Claims Introduced table writes "`addressable(Σ) = dom(Σ.L) \ nullified(Σ)` (ASN-0086)" — but ASN-0086 defines `nullified` and the per-type `A_K`, not `addressable`; that symbol is introduced here.
**Required**: Rename this ASN's operation (e.g., a subscripted or FTT-marked name), or keep the name and add an explicit disambiguation note stating the relationship to 0127's F-FIND primitive — positional vs. slot-agnostic matching, addressability-filtered vs. unfiltered, and that neither is a restriction of the other. Fix the table attribution so only `nullified` is credited to ASN-0086.

### Issue 2: Trace 6 does not fix its starting store, and its results are correct only on the base store
**ASN-0121, "A worked instance," Trace 6**: "Augment the store with a second document `d' = [1,0,1,0,2]` … and a further link homed there, `a₅` …"
**Problem**: Trace 4 mutated the running store by adding the retraction link `r₄`, after which `nullified(Σ) = {a₁}`. Trace 6 says "augment the store" without saying which one. On the post-Trace-4 store the trace's computed answers are wrong: `findlinks((H_d, X, Y, ∗), Σ)` would be `∅` (not `{a₁}`, since `a₁` is nullified) and `findlinks((H_node, X, Y, ∗), Σ)` would be `{a₅}` (not `{a₁, a₅}`). The claims hold only on the base three-link store plus `d'`/`a₅`. Trace 7 disambiguates itself explicitly ("Starting again from the base three-link store (Trace 4's `r₄` not present)"), which makes Trace 6's silence read as continuation of the mutated store — the wrong reading.
**Required**: Open Trace 6 with the same reset clause Trace 7 uses (base store, `r₄` absent), so the three computed answer sets are correct as stated.

### Issue 3: FL-JUNK's formal hypothesis mismatches its own gloss and is stronger than the proof uses
**ASN-0121, "Non-impedance: junk links do not obstruct" (FL-JUNK)**: "Let `Σ →* Σ'` be any reachable sequence that retracts nothing and whose added links … all fail the request: `nullified(Σ') = nullified(Σ)` and …"
**Problem**: The gloss "retracts nothing" and the formal conjunct `nullified(Σ') = nullified(Σ)` are not the same condition, and the gap is exactly a regime this ASN itself establishes as live. A sequence that adds only junk links, one of which is *born-nullified* by a pre-existing ghost-covering retraction tuple — the FL-WP(a) hazard, concretely exercised in Trace 7(a) — retracts nothing in any operational sense, yet has `nullified(Σ') = nullified(Σ) ∪ {j} ≠ nullified(Σ)`, so FL-JUNK as stated declines to cover it even though its conclusion still holds (the born-nullified junk link fails `sat` and existing links' membership conjuncts are untouched, `L_R` being unchanged). The proof paragraph in fact uses nullified-equality only on *existing* links ("both membership conjuncts of every existing link are unchanged"), so the stated hypothesis over-demands relative to the proof. Nelson's claim is about arbitrary quantities of junk; the formalization should cover junk additions that happen to be pre-covered ghosts.
**Required**: Weaken the hypothesis to `nullified(Σ') ∩ dom(Σ.L) = nullified(Σ)` (no *existing* link becomes nullified) — the same proof goes through verbatim — or, at minimum, align the prose gloss with the formal conjunct. Update the Claims Introduced row, which repeats the strong form.

## OUT_OF_SCOPE

### Topic 1: Result presentation order
Nelson's text says the operation "returns a list"; the ASN specifies the answer as a set. Enumeration order and delivery in batches are the business of the paginated retrieval operation (FINDNEXTNLINKSFROMTOTHREE), which the Scope section already excludes — the snapshot set is the right abstract content here.
**Why out of scope**: ordering is a presentation contract for a different operation, not a gap in this one.

### Topic 2: Constraining higher endsets (n-set requests)
The ASN correctly has `sat` leave `e₄ … eₙ` unconstrained, matching the FROMTOTHREE name. An operation that *searches on* higher endsets — Nelson's "4-sets, 5-sets … n-sets supported in link storage and search" (4/79) — is a distinct future operation.
**Why out of scope**: this ASN faithfully specifies the three-slot operation; n-slot search is new territory.

VERDICT: REVISE
