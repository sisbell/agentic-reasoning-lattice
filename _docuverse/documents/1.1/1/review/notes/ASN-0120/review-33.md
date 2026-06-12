# Review of ASN-0120

This ASN is in strong shape: the V→I conversion thesis is carried through with real derivations, the recovery equation's F-trace (versus store-trace) choice is argued from a concrete failure mode, the wp analysis for ML9 is genuine and biconditional, the contracted-home selector divergence is handled at its boundary, and the worked example exercises creation *and* a subsequent edit against ML1/ML7/ML8/ML9. The three items below are precision defects, not structural ones.

## REVISE

### Issue 1: "names a vacuous interval" contradicts T12
**ASN-0120, resolution section (empty-resolution boundary paragraph)**: "a well-formed spec all of whose positions have since been deleted, or that names a vacuous interval, resolves empty, and the operation is defined on it."
**Problem**: A well-formed spec cannot name a vacuous interval. `wf` makes every `σ_j` T12-well-formed, and T12(b) (via TA-strict) guarantees `u_j ∈ ⟦σ_j⟧` — the interval always contains its start. What the sentence means is an interval *capturing no active position* (e.g., a depth-mismatched or beyond-extent interval whose tumblers are never in `dom(Σ.M(d_j))`). As written, the boundary enumeration asserts a case the foundation excludes — and it sits in exactly the paragraph that settles the empty-resolution boundary, where precision matters most.
**Required**: Reword to "or whose interval contains no active position" (or equivalent); the interval itself is never empty.

### Issue 2: The composite is written with the atomic-transition arrow
**ASN-0120, MLop**: "When enabled, the transition `Σ → Σ'` is the ValidComposite★ of `K.λ` followed by `K.μ⁺_L`, and its net effect is two entries." (Same conflation in the substrate section: "The link-creation transition is the substrate's `K.λ` … followed by … `K.μ⁺_L`.")
**Problem**: The foundations reserve `→` for single atomic transitions (SequentialTransitionAxiom) and write composites `Σ →* Σ'` (ValidCompositeAmended, ASN-0047 — the very definition MLop invokes). Calling the two-step composite "the transition `Σ → Σ'`" invites applying per-step-quantified invariants to a non-atomic object — e.g., NoDeallocation and L12 quantify over single `op ∈ Σ` edges — and is internally inconsistent with the ASN's own ML7, which correctly quantifies over atomic `Σ' → Σ''`. The intermediate state exists and the ASN reasons about it (the `K.μ⁺_L` precondition discharge); the notation should not erase it.
**Required**: Write the MAKELINK effect as a composite `Σ →* Σ'` (two named elementary steps), reserving `→` for the elementary transitions, in MLop, the substrate section, and anywhere "the transition" denotes the whole operation.

### Issue 3: The ρ/resolve agreement is asserted, not derived
**ASN-0120, resolution section**: "On that domain the two agree: ρ's contribution for spec j is exactly the set of I-addresses `resolve(d_j, σ_j)`'s runs name."
**Problem**: This is a derived equality stated in one sentence with no premises named. It is true, but it rests on ASN-0058's decomposition conditions and the argument is not shown: `dom(f)` for `f = M(d_s)|⟦σ⟧` is by definition the same active-filtered set ρ consults; then B1 (every `v ∈ dom(f)` in exactly one block) together with B3 (`M(d)(v_j + k) = a_j + k`, which also forces every block position into `dom(f)`) gives that the run-named addresses are exactly `ran(f)` — both inclusions. "X agrees with Y" without naming B1/B3 is a claim, not a proof (Standard 6).
**Required**: Either supply the two-step derivation (dom-identity by definition of restriction; run-set = `ran(f)` by B1 + B3, both directions) or explicitly mark the sentence as an unproved alignment remark rather than a fact the ASN owns.

## OUT_OF_SCOPE

### Topic 1: Direct I-address endset arguments (ghost, foreign, and link-subspace endsets)
**Why out of scope**: The ASN correctly establishes that V-spec resolution can only produce content-backed endsets (`ρ(R_i, Σ) ⊆ dom(Σ.C)`) and explicitly excludes the direct-I-address argument shape that would exercise L4's and L9's full generality, deferring link-pointing-at-link to its Open Questions. Specifying that argument shape — its well-formedness, its recovery equation analogue, and its interaction with `F`-tracing — is a future ASN, not a defect here.

### Topic 2: Semantics of the empty non-type endset (the one-sided link)
**Why out of scope**: The ASN settles definedness, legality, and discoverability-inertness of the empty slot and defers what the degenerate connection *asserts* to its first Open Question. The meaning question is genuinely new territory; this ASN's contract is complete without it.

VERDICT: REVISE
