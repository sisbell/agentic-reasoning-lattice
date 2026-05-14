# Review of ASN-0042

## REVISE

### Issue 1: NestingByDelegation's equality-case argument is unclear and risks circularity

**ASN-0042, NestingByDelegation proof, sub-case `pfx(π') = pfx(π_1)`**: "`pfx(π') = pfx(π₁)` would force `π_d = π₁` (impossible, since `pfx(π_d) ≺ pfx(π')` strict) or violate O1b at `Σ_{n+1}`."

**Problem**: The "would force `π_d = π_1`" step is unjustified. From `pfx(π') = pfx(π_1)` and `pfx(π_d) ≠ pfx(π')` (condition (i)), it does not follow that `π_d = π_1` — they could simply be distinct principals with distinct prefixes. The alternative "violate O1b at `Σ_{n+1}`" is the very claim being inductively established, so it would be circular if read locally. The argument only works if it cites the Delegation section's O1b preservation proof (which uses condition (ii) of `delegated_Σ`), but the prose says "combined with O1b at `Σ_n`" rather than condition (ii).

**Required**: Replace the inline argument with the clean version that uses condition (ii) directly: "By condition (ii), `π_d` is the most-specific covering principal of `pfx(π')` in `Π_Σ`. Take `π'' = π_1` in (ii): since `pfx(π_1) ≼ pfx(π')`, we get `#pfx(π_1) ≤ #pfx(π_d)`. But `#pfx(π_1) = #pfx(π') > #pfx(π_d)` by (i). Contradiction." Or explicitly cite the Delegation section's O1b preservation proof rather than relying on the implicit "see below" pointer.

### Issue 2: O2's Step 2 inlines what is already a named lemma

**ASN-0042, O2 proof Step 2 ("Total ordering of covering prefixes")**: The argument duplicates the content of PrefixesOfCommonAddressAreComparable (covering-chain lemma) introduced in *Ownership Domains*.

**Problem**: O2 appears in *The Exclusivity Invariant*, which follows *Ownership Domains*, so the lemma is already in scope. The proof should cite it ("By the covering-chain lemma applied to `pfx(π₁), pfx(π₂)` as two prefixes of `a`, they are `≼`-comparable; with `#p₁ ≤ #p₂` WLOG, `p₁ ≼ p₂`.") rather than re-derive it. The duplication is harmless but obscures the pattern.

**Required**: Cite the named lemma instead of inlining the derivation. Alternatively, hoist the lemma above O2 so it precedes its first user, then have both O2 and the later proofs cite it uniformly.

### Issue 3: O7(c)'s "right is recursive" appeals to O7(a)'s domain-restricted result for an unrestricted-tumbler claim

**ASN-0042, O7 proof of postcondition (c)**: "Condition (ii) is satisfiable at `Σ'` because postcondition (a) establishes `π'` as the most-specific covering principal in `dom(π') ∩ Σ'.B` — and the same prefix-ordering argument carries over from `Π_{Σ'}.B` to any `p'' ∈ T` with `pfx(π') ≺ p''`..."

**Problem**: Postcondition (a) is restricted to allocated addresses (`dom(π') ∩ Σ'.B`). The "carries over" claim to arbitrary `p'' ∈ T` (which need not be in `Σ'.B`) is not derived from (a) — it is its own argument using condition (vi) of the delegation that introduced `π'`. The proof gestures at this ("no principal in `Π_{Σ'}` has a prefix strictly extending `pfx(π')`") but presents it as inheriting from (a). The argument is sound under the gesture but the dependence is misstated.

**Required**: Separate the two arguments. State explicitly: "By condition (vi) of the delegation that introduced `π'`, no `π'' ∈ Π_Σ` has `pfx(π') ≺ pfx(π'')`. The only newcomer in `Π_{Σ'} ∖ Π_Σ` is `π'` itself, whose prefix does not strictly extend itself. Hence no `π'' ∈ Π_{Σ'}` has `pfx(π') ≺ pfx(π'')`, so for any `p'' ∈ T` with `pfx(π') ≺ p''`, `π'` is the most-specific covering principal in `Π_{Σ'}`." Postcondition (a) is not load-bearing here.

### Issue 4: Worked-example bootstrap snapshot includes ad-hoc seed addresses without their joint consistency proven

**ASN-0042, *Worked Example* introduction**: The bootstrap seeds include `[1, 0, 1]`, `[1, 0, 2, 0, 1]`, `[1, 0, 2, 0, 2]`, `[1, 0, 2, 0, 3]`, `a_1`, `a_3`, plus the principal prefixes `[1]` and `[2]`.

**Problem**: The justification verifies B1 within each individual sibling stream but does not verify O14's first clause (coverage) for every seeded address explicitly, nor does it check that the claimed B1 is satisfied across *all* affected streams jointly. For example, baptizing `a_1 = [1, 0, 2, 0, 3, 0, 1]` requires `[1, 0, 2, 0, 3] ∈ Σ_0.B` (parent of its baptizing stream) — verified — but does not verify B1 within `S([1, 0, 2, 0, 3], 2)` for `a_1` as `c_1` (vacuous, but should be stated). The reader has to chase down each obligation. Given that the worked example is the principal verification of multi-property correctness, the snapshot's joint consistency deserves a tabulated check rather than prose interleaving.

**Required**: Add a tabulated consistency check listing each seeded address, its B6 status (which doesn't apply to bootstrap, but T4 validity does), the covering principal under O14, and the relevant B1 stream-membership. Or condense the snapshot to the minimum needed for the trajectory and remove unused seeds.

### Issue 5: Form B sub-delegate analysis in O10 leaves the "longer Form B" case under-justified

**ASN-0042, O10 proof, non-coverage analysis Form B**: "Combined with the prior exclusion of longer Form B sub-delegates by length, no Form B sub-delegate covers `a'`."

**Problem**: The "prior exclusion by length" is correct as far as it goes — a Form B sub-delegate with prefix `pfx(π).0.U^{(i)}_1.…` longer than `#pfx(π) + 2` cannot prefix `a'` (length `#pfx(π) + 2`). But the proof should explicitly note that PrefixBaptismCoupling places the *full* prefix (not the length-(#pfx(π)+2) truncation) in `Σ.B`, so longer Form B sub-delegates do not contribute to `hwm_0` via their truncations. A length-(#pfx(π)+2) initial segment `pfx(π).0.U^{(i)}_1` of a longer sub-delegate's prefix may or may not be in `Σ.B` independently, and `hwm_0` therefore reflects only addresses actually baptized in `S(pfx(π), 2)`. The proof concludes correctly but elides this subtlety, which the careful reader will need to reconstruct.

**Required**: Add one sentence after the length-exclusion: "Note that longer Form B sub-delegate prefixes are placed in `Σ.B` by PrefixBaptismCoupling, but their length-(#pfx(π)+2) truncations are not separately required to be in `Σ.B`; consequently their `U^{(i)}_1` values do not constrain `hwm_0`. This is consistent with the argument because such longer sub-delegates do not cover `a'` by length, regardless of `U^{(i)}_1`."

### Issue 6: Properties-Introduced table conflates "axiom" with "design requirement"

**ASN-0042, Properties Introduced table**: Several entries are listed with status "design requirement" (O1a, O1b, O5, O12, O13, O14, O15, O16). Others are listed as "axiom" (O18, `pfx(π)`, `allocated_by_Σ`). 

**Problem**: The two terms are used interchangeably without distinction. "Design requirement" suggests something the design must satisfy (perhaps a derived obligation); "axiom" suggests something posited without derivation. In this ASN, both are used for the same role — properties stipulated rather than derived. The mixed terminology obscures the load-bearing axiomatic structure. By contrast, derived properties are clearly marked ("from X, Y, Z" or "derived from ASN-0040 B10").

**Required**: Pick one term ("axiom") and use it uniformly for all stipulated properties. The "design requirement" justification can appear in the prose; the table should mark provenance unambiguously.

## OUT_OF_SCOPE

None — the Scope section appropriately delimits the model, and the Open Questions correctly defer transfer mechanics, overlap prevention, federation, and other future-ASN concerns.

VERDICT: REVISE
