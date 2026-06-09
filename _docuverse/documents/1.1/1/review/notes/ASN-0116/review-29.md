# Review of ASN-0116

I worked through the composite construction, the precondition discharge at each intermediate state, the I-DOM interval argument, the link-survival and discoverability analyses, the provenance coupling, and the boundary cases. Below is what I verified and why I find no revision required.

## Verification performed

**Composite validity (the load-bearing claim).** INSERT is exhibited as `K.α`(×n) → `K.μ⁻` → `K.μ⁺` → `K.ρ`(×n), with K.μ⁻ correctly dropped in the append/empty cases. I checked that:
- Clause-1 preconditions hold at each *intermediate* state: the n K.α steps each discharge SubsequentEmissionFreshness against the store as it then stands; K.μ⁻'s strict-contraction precondition is met (content subspace `J−1 < N`, including the front-insertion extreme `J=1` with `n'_{s_C}=0`); K.μ⁺'s `a ∈ dom(C)` precondition is met precisely because allocation precedes it; K.ρ's `a ∈ dom(C') ∧ d ∈ E_doc` holds.
- The note correctly treats J0/J1★/J1'★ as *boundary-only* (clause 2), so the intermediate J0/P7a violations after K.α are harmless — this is handled cleanly rather than glossed.

**I-DOM index attribution.** The trickiest derivation. I confirmed the three index intervals `{1..J−1}`, `{J..J+n−1}`, `{J+n..N+n}` are consecutive and pairwise disjoint, and that block positions are genuinely absent from ASN-0082's gapped arrangement: index `≤ N` withheld by I3-V, index `> N` withheld by I3-CS, with the "no block position is a shifted-suffix image" step (`i−n ≤ J−1 < J ⟹ u < p`) checked and sound.

**Multi-step lemma discipline.** P4 and P6 correctly invoke L12 + **LP3★** (multi-step coverage invariance) rather than single-step LP3, since `Σ → Σ'` spans n+1 elementary steps. This is exactly the care the standards demand.

**P6 weakest precondition.** The wp resolves to a *containment* `Added ⊆ D(d,Σ)`, not an emptiness — and the note explicitly identifies that the emptiness form is sufficient-but-strictly-stronger, over-rejecting the ghost-plus-live-span pre-state. This is a genuine, non-trivial wp, and the worked "P6 trap" example exercises exactly that pre-state.

**Link survival.** P4's bijection-not-inclusion form is correct: prior witnesses partition into left/suffix/cross-subspace and map bijectively (suffix relabelled by `v↦shift(v,n)`, injective by TS2) onto three disjoint target sets, with the new-block part disjoint from all three — so the count formula and monotone content-growth formula hold.

**Boundary cases.** Front (`J=1`), append (`J=N+1`, K.μ⁻ correctly *inapplicable* and dropped), empty subspace (`m` fixed by ValidFirstInsertionPosition), and `n=1` all check out. The worked example arithmetic (`[d.0.s_C.7/.8]`, reading `a_1,a_2,X,Y,a_3,a_4,a_5`) is correct.

**Content chain.** `inc(·,0) = shift(·,1)` on T4-valid content addresses (TA5-SigValid + TA5(c)) justifies `A_new = {shift(a,k)}` as a contiguous chain run; `shift(a,k) = incᵏ(a,0)`.

**No cross-ASN violations.** All references (0034, 0036, 0043, 0047, 0082, 0093, 0098) are to foundation ASNs whose claim statements are provided. Retired-ASN mentions are confined to Scope/Open-Questions boilerplate.

## Depth requirements
Concrete example (present, exercises P0/P1/P4/P5/P6 against a specific shift), non-trivial wp (P6), and derived consequences (P3 impermanence, P4 monotonicity, P5 isolation as a corollary of the two-layer split) are all satisfied.

## Anti-bloat assessment
I looked specifically for forward-reference accretion, defensive justifications, use-site inventories, and duplicated paragraphs. The note has clearly been tightened: the one near-duplication (P2 re-bundling I-ALLOC's domain-growth + I-IMM under a preserved-invariant name) is structurally motivated — Effect clauses define the operation, the "invariants preserved" section answers the problem's named questions — and is transparently labeled "restated." It does not rise to a defect. The "valid composite" section's explanation of why no single atomic suffices is load-bearing justification for the K.μ⁻/K.μ⁺ decomposition, not meta-prose. Open Questions are correctly scoped to future work (transclusion, concurrency, post-edit fragmentation).

VERDICT: CONVERGED
