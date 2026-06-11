# Review of ASN-0120

## REVISE

### Issue 1: Fact (a) of ML9 asserts a false inclusion at the boundary case `d' = d`
**ASN-0120, "The invariants MAKELINK preserves," ML9, Fact (a)**: "By generalized referential integrity (S3★, ASN-0047) an arrangement's images lie in the store: `ran(Σ'.M(d')) ⊆ dom(Σ.C) ∪ dom(Σ.L)`"

**Problem**: The left side is the *post-state* range; the right side is the *pre-state* store. For `d' = d` the inclusion is false: `K.μ⁺_L` puts `a ∈ ran(Σ'.M(d))`, and `a ∉ dom(Σ.C) ∪ dom(Σ.L)` by ML0's freshness. S3★ at `Σ'` licenses only `ran(Σ'.M(d')) ⊆ dom(Σ'.C) ∪ dom(Σ'.L) = dom(Σ.C) ∪ dom(Σ.L) ∪ {a}`. Fact (a)'s concluding equation `coverage(eᵢ) ∩ ran(Σ'.M(d')) = ρ(R_i, Σ) ∩ ran(Σ'.M(d'))` is in fact true at `d' = d`, but only because `a ∉ coverage(eᵢ)` — a fact established later, inside Fact (b). As ordered, Fact (a)'s derivation has a hole exactly at the boundary case the ASN itself singles out as "the case ML4 highlights."

**Required**: State Fact (a) over the post-state store and dispose of the `{a}` delta there (the subspace argument already in Fact (b) does it: every store address in `coverage(eᵢ)` carries `subspace_I = s_C`, `a` carries `s_L`), or establish `a ∉ coverage(eᵢ)` before Fact (a) is applied at `d' = d`. The composition order must not consume a fact before it is proven.

### Issue 2: Coverage equality of merged vs. unit decompositions is miscited to LP-Fin Corollary
**ASN-0120, "What the endset arguments name…"**: "a decomposition that merges a run of chain-adjacent resolved addresses into one wider canonical span `(aₖ, δ(n, #aₖ))` has the same coverage (ASN-0098, LP-Fin Corollary)" — repeated in the worked example: "the single wider canonical span `(a₁, δ(2, #a₁))` has the same coverage as the two unit spans (LP-Fin Corollary)."

**Problem**: LP-Fin Corollary characterizes only `F ∩ [s, s ⊕ ℓ)` — the trace on substrate-emittable addresses. "Same coverage" is full tumbler-set equality, and the full strength is load-bearing: type matching (L8) compares whole coverage sets, so two records agreeing only on their F-trace but differing elsewhere in coverage would be type-distinguishable, contradicting ML2. The full equality does hold — for a T4-valid chain address, `inc(·, 0) = shift(·, 1)` (TA5-SigValid), so consecutive unit spans are *adjacent* (`reach` of one equals `start` of the next) and the half-open intervals concatenate exactly: `⋃ₖ [aₖ, shift(aₖ,1)) = [a₁, shift(a₁, n))`, which is ASN-0053's S3/S5 merge applied along the run. But that argument appears nowhere; the cited lemma does not establish the claim.

**Required**: Replace the LP-Fin Corollary citation with the actual derivation (chain-sibling adjacency via TA5-SigValid, then ASN-0053 S3 merge / induction over the run), in both places. LP-Fin Corollary remains the right citation for the *store-trace* facts only.

### Issue 3: The first-link V-position depth is undetermined and misattributed
**ASN-0120, "Residence, and its independence…"**: "Finally, the bound V-position `v_a` is the one `K.μ⁺_L` itself selects — `ValidFirstLinkPosition(d, v_a, m)` when `V_{s_L}(d) = ∅`, else `v_a = shift(max(V_{s_L}(d)), 1)`."

**Problem**: `K.μ⁺_L` does not select `m`. ASN-0047's `ValidFirstLinkPosition(d, v, m)` is parameterized by a caller-chosen `m ≥ 2` ("for any chosen `m ≥ 2` it fixes the unique well-formed first link V-position"). When the home document has no links yet, *someone* must choose the depth, and `makelink(d, R₁, R₂, R₃)` carries no such parameter. The non-empty case is fully determined; the empty case is not, and the prose papers over the freedom by attributing the choice to the substrate transition.

**Required**: State how `m` is fixed in the first-link case — a fixed convention (e.g., `m = 2`), an operation argument, or explicit implementation nondeterminism — and correct the misattribution.

### Issue 4: Meta-prose accretion (anti-bloat)
**ASN-0120, multiple locations**:

- **Duplicate disclaimer**: "We argue over store membership, not over projections at arbitrary covered tumblers (where T4b's `E` need not be defined…)" (ML1 surplus argument) and "We establish this over store membership, not over the value of `subspace_I` at arbitrary covered tumblers (where it need not be defined…)" (ML9, Fact (a)) are the same defensive remark in two wordings. The underlying point is a real proof-obligation discharge; state it once, reference it the second time.
- **Correction residue**: "…this holds because both `K.λ` and `K.μ⁺_L` carry `E' = E ∧ R' = R` in their ASN-0047 frames (ML10), not because no range-new address exists." The trailing contrast clause explains why a prior (wrong) justification doesn't apply rather than what is true. The fact is `R' = R`; say that and stop.
- **Forward assurance**: "The confinement and containment arguments below use only `m = #u_j ≥ 2` and prefix sharing, so they are insensitive to the mismatch" — vouches for proofs that appear three sentences later. Let the proofs carry it.
- **Essay in a structural slot**: the ML1 claims-table row embeds proof steps and defensive parentheticals ("depth-match to the arrangement's common depth *not* required," "covering, not exact — ASN-0053 S7"). The table should state the claim; the body already carries the argument.

**Required**: Prune the duplicates and corrective asides; reduce the ML1 (and similarly ML8/ML9) table rows to claim statements.

## OUT_OF_SCOPE

### Topic 1: Forward stability of the recovery equation
The creating-state equation `coverage(e_j) ∩ dom(Σ.C) = ρ(R_j, Σ)` is in fact stable under all future transitions — descendants of resolved addresses never become content (the surplus argument), and merged intervals contain only already-allocated chain addresses by ChainMembershipForOrigin's contiguous prefix — so the recorded reference never silently *gains* content.
**Why out of scope**: this is a property consumed when endsets are *read* over time, the territory of FOLLOWLINK (ASN-0114) and RETRIEVEENDSETS (ASN-0110), both excluded from this ASN's scope.

### Topic 2: Representation independence versus structure-reading operations
ML2's "no operation of the model distinguishes coverage-equal records" is correctly scoped here, but a future READLINK (ASN-0111) that exposes a link's stored span-set would observe the decomposition.
**Why out of scope**: reconciling ML2 with structure-reading belongs to the READLINK ASN, not to MAKELINK.

VERDICT: REVISE
