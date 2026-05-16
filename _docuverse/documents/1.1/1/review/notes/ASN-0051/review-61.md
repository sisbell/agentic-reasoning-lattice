# Review of ASN-0051

## REVISE

### Issue 1: T-interleaving structural argument under-justified

**ASN-0051, SV11 non-attainment proof, disjoint-pair case (b)**: The proof asserts "β_{k₂} is itself an ordinal-sibling sequence with a single I-base prefix, its elements share their common prefix up to the second-to-last component and differ only at the last component; siblings under that common prefix all lie within the T-interval (prefix.0.1.0.last_prev, prefix.0.1.0.last_prev_succ) defined by the parent's siblings, hence between two ordinal-adjacent elements of any ordinal-sibling sequence at strictly shorter tumbler length that brackets them."

**Problem**: The notation "prefix.0.1.0.last_prev" is informal and not parseable. The structural claim that β_{k₂}'s elements are confined to one T-window (e_i, e_{i+1}) of β_{k₁} requires:
- β_{k₁} is strictly shorter than β_{k₂} (otherwise the interleaving case doesn't arise)
- β_{k₂}'s first #β_{k₁} - 1 components match β_{k₁}'s prefix (otherwise T-linear separation holds)

A reader can reconstruct from T1 that disjoint sibling chains can interleave only in this asymmetric configuration, but the proof states it as a fait accompli. The four-case structural lemma (same/different length × matching/non-matching prefix) should be made explicit:
- same length, same prefix → not disjoint (excluded by hypothesis)
- same length, different prefix → T-linearly separated (handled by sub-case (a))
- different lengths, prefix mismatch → T-linearly separated (handled by sub-case (a))
- different lengths, prefix match → interleaving case at hand

**Required**: Replace the "prefix.0.1.0.last_prev" prose with an explicit T1-based argument showing why the interleaving case forces β_{k₂} ⊂ (e_i, e_{i+1}) and identifies the strictly-shorter chain as β_{k₁}.

### Issue 2: Pigeonhole sub-argument in T-interleaving is condensed

**ASN-0051, SV11 non-attainment proof, T-interleaving sub-case**: "by pigeonhole on the boundary set {e_i, e_{i+1}} (size 2): either two spans share an element of {e_i, e_{i+1}} in their β_{k₁}-contributions — pairwise overlap, coalescence — or, in the m = 2 case where the two spans include disjoint boundary elements (one β_{k₁}-contribution including e_i, the other including e_{i+1}), the two β_{k₁}-contributions sit at ordinal-adjacent positions in β_{k₁}'s sequence."

**Problem**: The argument implicitly handles two phenomena (a contribution including only one of {e_i, e_{i+1}} vs. including both) and dispatches m=2 separately from m≥3. The proof omits the case where one or both m=2 contributions include both boundary elements (which gives overlap directly), and doesn't fully justify why "include disjoint boundary elements" entails the contributions occupy offsets only i-1 and i in β_{k₁}'s sequence (they might extend further on either side, but the maximal fragments containing them would still coalesce — this should be argued).

**Required**: Expand the m=2 case analysis to show: if both contributions include both boundary elements (overlap directly), if one includes only e_i and other only e_{i+1} (adjacent at offsets i-1 and i, coalesce regardless of how far they extend leftward/rightward), and the m≥3 pigeonhole case (overlap forced).

### Issue 3: SV6 sub-claim (i) hypothesis well-formedness

**ASN-0051, SV6 proof, sub-claim (i)**: "Suppose the first position where tⱼ ≠ sⱼ is some j with j < k. Then #t ≥ j and tⱼ > sⱼ."

**Problem**: The hypothesis "the first position where tⱼ ≠ sⱼ is some j" presupposes #t ≥ j (so tⱼ is defined). The proof then derives "#t ≥ j" — but if the hypothesis already presupposes this, deriving it is circular; if the hypothesis admits #t < j (with tⱼ undefined), then the "minimum j" with tⱼ ≠ sⱼ is also undefined for indices > #t. The reductio against #t < j is correct in substance but the hypothesis framing needs clarification.

**Required**: Rephrase as "Suppose t ≠ s and the T1(i) decomposition gives a first divergence index j with j < k". Then T1(i) provides j ≤ min(#t, #s), making #t ≥ j and tⱼ > sⱼ both consequences of T1(i)'s witness clause, not separate sub-claims requiring contradiction-with-prefix arguments.

### Issue 4: (m ≥ 3, p ≥ 3) attainment witness gap

**ASN-0051, SV11 Conclusion paragraph**: "For m ≥ 3 the same nesting pattern works with each block's size grown to `min_k n_k ≥ 2m − 1` and m spans whose coverages contribute non-adjacent offsets in every block ... we do not exhibit explicit (m ≥ 3, p ≥ 3) witnesses but the construction generalises straightforwardly from the (m = 2, p = 3) pattern."

**Problem**: The witnessed-attainment scope summary explicitly names (m ≥ 3, p ≥ 3) as "constructible by the same nesting pattern". For a foundational ASN, "constructible straightforwardly" without an explicit construction leaves a gap in the witness library — particularly since the (m = 2, p = 3) pattern was itself explicit and non-trivial (eleven sibling tumblers, three nested blocks, specific span structure). A reader cannot verify the (m ≥ 3, p ≥ 3) generalisation without re-doing the geometric construction independently.

**Required**: Exhibit at least one (m = 3, p = 3) witness with explicit sibling tumblers, arrangement, block decomposition, span coverages, and decomposition terms verified to be pairwise non-adjacent within each block. Either that, or revise the scope summary to mark (m ≥ 3, p ≥ 3) as "structurally admissible but not witnessed in this ASN", explicitly distinguishing it from the four witnessed regions.

### Issue 5: SV11 attainment-or-not at single disjoint pair within p ≥ 3

**ASN-0051, SV11 non-attainment "disjoint-pair case"**: "The argument depends only on the two-block pair (β_{k₁}, β_{k₂}); the presence of additional blocks (p ≥ 3) does not rescue attainment — once one disjoint pair forces coalescence inside β_{k₁}, the m · p fragment count is unreachable regardless of what the remaining p − 2 blocks contribute."

**Problem**: The conclusion is correct but the argument as written considers attainment only via coalescence inside β_{k₁}. The proof should also note: even if non-disjoint pairs among the remaining blocks attain their full m contributions, the deficit inside β_{k₁} (m → m−1 or fewer non-coalesced fragments) cannot be compensated by surplus elsewhere because each block independently contributes at most m fragments. State this explicitly.

**Required**: Add one sentence to the disjoint-pair conclusion: "Per-block fragment counts are independently capped at m by the attainment biconditional, so a within-block deficit in β_{k₁} cannot be offset by other blocks; the total fragment count is therefore strictly less than m · p."

### Issue 6: Worked example two-span variant — fragment-attribution claim

**ASN-0051, Worked Example two-span scenario**: "Non-injective sharing — the appearance of {a₂, a₃} in both β₁ and β₂ — plays no role in the fragment-count gap; its only quantitative footprint is inflating the summed term width to 6 (vs |π_text(e, d)| = 4 distinct I-addresses) as exhibited in the 'Cover, not partition' paragraph above."

**Problem**: The claim "non-injective sharing plays no role in the fragment-count gap" is asserted but not directly justified. The argument that follows shows the gap is "per-block coalescence summing to 4 → 2 across blocks," which is correct, but the reader is left to verify that non-injective sharing doesn't introduce additional coalescence between fragments in *different* blocks. (Fragments in different blocks are counted separately even when their I-address sets overlap — but this is by the maximal-fragment definition's restriction to a single block, which the proof should reference explicitly.)

**Required**: Add a one-sentence citation to the maximal-fragment definition's per-block confinement, explaining why I-address sharing across blocks does not reduce the cross-block fragment count.

## OUT_OF_SCOPE

### Topic 1: Detailed link-subspace coverage analysis
**Why out of scope**: The ASN explicitly defers analysis of endsets whose coverage references link addresses (admitted by L4, L13) to "the Link Subspace ASN". SV11 is correspondingly stated for π_text rather than full π. This is an appropriate scope decision — full link-subspace projection involves reflexive-addressing semantics, link discovery through other links, and potentially cyclic discovery structures that belong in a dedicated treatment.

### Topic 2: Broader-level (k ≤ p₃) span survivability
**Why out of scope**: SV6 explicitly scopes itself to element-level spans (k > p₃). The ASN's "Note on scope" paragraph correctly identifies broader-level spans as admitted by L4 but governed by allocator-discipline machinery from ASN-0034 not yet developed for this regime, and notes that udanax-green does not implement broader-level spans. The deferral is justified.

### Topic 3: Same-origin coverage growth formal characterisation
**Why out of scope**: The "Content Allocation and Coverage Stability" section explicitly states "We make no formal SV claim about same-origin coverage growth in this ASN. The analysis below is descriptive..." This is an appropriate scope decision — the conditions are allocator-discipline dependent and belong with the ASN-0034 work.

### Topic 4: Generalisation to arity N > 3 links
**Why out of scope**: The scoping note explicitly restricts to standard-triple (arity-3) links: "Treatment of those additional endset slots is deferred to ASN-0043." The slot-wise machinery of vitality and discovery generalises to N > 3, but the detailed treatment is appropriately deferred.

### Topic 5: Inter-document propagation policy for discovery
**Why out of scope**: SV14 establishes that document-derived discovery `discover_through_s(d)` shrinks under contraction without explicit signal to consumers tracking the discovery set. The policy question — should the system notify consumers when a link exits discover_through? — is a downstream policy concern, not a survivability invariant.

VERDICT: REVISE
