# Review of ASN-0118

The technical core of this ASN is sound. I checked the composite decomposition (K.μ⁻ retention arithmetic, K.μ⁺ precondition discharge including S8a/S8-depth at both placement and displaced positions, the j = 0 and empty-destination boundaries), the J0/J1★/J1'★ coupling analysis including all three provenance branches, the no-holes tiling derivation (TS1/TS3/TS4 used correctly, including the `[1,10] < [1,10,0]` prefix-boundary subtlety in the relaxation example, which is handled correctly), the CP4 exactness argument under shift-vacating, the `ran(Σ'.M(d))` equality underlying the link-discoverability wp, and the worked example's arithmetic. All check out. The remaining findings are accretion and one rigor nit.

## REVISE

### Issue 1: V-spec definition paragraph has accreted genealogy, defense, example, and implementation evidence into one block
**ASN-0118, "What a spec-set names, and what resolution recovers"**: the single paragraph running from "A *V-spec* is a pair `ρ = (d_s, σ)`..." to "...rather than by offset arithmetic."
**Problem**: Four distinct kinds of content are interleaved in one ~450-word block, and the reader must skip past meta-prose to extract the three admissibility conditions. Specifically: (a) the relaxation is stated twice in adjacent sentences — "a *deliberate relaxation* of its condition (iii)... of which we keep only the bare level-uniformity `#s = #ℓ`, dropping the `= m` conjunct" and then "A V-spec is therefore a *relaxation* of an ASN-0058 ContentReference, not one simpliciter" (the only new content in the second sentence is the containment direction, which deserves one clause, not a restatement); (b) the udanax-green evidence is a three-call-site inventory (`acceptablevsa`, `specset2ispanset`, the resolution path) embedded mid-definition, and the lead sentence "matches the relaxed admissibility at every stage" is immediately undercut by the parenthetical recording a clipping-arithmetic divergence — "matches at every stage" and "one implementation divergence is worth recording" cannot both stand without qualifying which stages are meant; (c) the depth-mismatch micro-example (`s = [1,1,5]`, `ℓ = [0,9,0]`) is correct and valuable but sits inside the definition rather than after it. This paragraph is recognizably the deposit of prior review cycles on the depth-mismatch question.
**Required**: Restructure: state the three admissibility conditions and `act(ρ, Σ)` first, as the definition; one sentence noting the relaxation of ASN-0058's condition (iii) and the containment direction (no restatement); move the worked micro-example to its own paragraph immediately following; compress the udanax-green evidence to its load-bearing content and reconcile "matches at every stage" with the recorded divergence (e.g., "matches the relaxed admissibility; its clipping arithmetic diverges at resolution").

### Issue 2: Repeated forward deferrals to the composite section
**ASN-0118, "Standing precondition (composite boundary)" and "The COPY operation"**: "COPY is itself an ASN-0047 composite (we exhibit its decomposition below)..." and, one section later, "...COPY's decomposition into atomic steps is exhibited in the next section..." — with CP8's introduction adding a third deferral, "(both discharged below)".
**Problem**: Three paragraphs in different sections defer to the same downstream location (the "COPY as a valid composite" section). One deferral orients the reader; the second and third are accretion — each was presumably added to pre-empt a reviewer objection at its own site.
**Required**: Keep a single deferral at the operation definition; let the standing-precondition paragraph state its assumption without advertising where the decomposition lives, and let CP8's clauses stand without the parenthetical (the discharge section is adjacent).

### Issue 3: The link-discoverability wp omits the enabledness conjunct that the foundation's own wp convention includes
**ASN-0118, "Survival of links anchored to the reused content"**: "`wp(COPY, "a discoverable from d") = (E j : coverage(Σ.L(a).eⱼ) ∩ {c₀, …, c_{W−1}} ≠ ∅)`"
**Problem**: ASN-0098's LP12a, the in-house precedent this analysis parallels, writes its wp as `enabled(K.μ⁻[d, R]) ∧ ⟨pullback⟩`. The displayed equation here is the pullback conjunct only. The surrounding prose ("ask what must hold of Σ for `a` to be discoverable from `d` after COPY") implicitly assumes COPY is enabled — `W` and the `cᵢ` are only defined when COPY's preconditions hold — but the equation as written asserts an equality between wp and a predicate that is not even well-formed on pre-states where COPY is not applicable.
**Required**: Either conjoin an explicit `enabled(COPY(Σ, d, p, R))` to the right-hand side, matching LP12a's form, or state once that the wp is computed over the operation's enabled domain (where `W ≥ 1` and the resolved sequence exist).

## OUT_OF_SCOPE

### Topic 1: Relationship between COPY and the fork composite's arrangement-population step
ASN-0047's J4 (ForkComposite) populates a new version's arrangement via an order-preserving bijection from the source's content subspace — structurally a whole-subspace transclusion into an empty destination. Whether fork's step (ii) is a special case of COPY (empty destination, single full-subspace spec) is a unification question for a future ASN.
**Why out of scope**: Version creation is explicitly excluded from this ASN's scope, and the question is about factoring two operations, not an error in either.

### Topic 2: Temporal stability of a stored spec-set
Resolution is indexed to the invocation state Σ; what a spec-set held by a client denotes at a later state (after source edits) is a versioning/correspondence question the ASN's fourth open question already gestures at.
**Why out of scope**: The ASN correctly defines resolution as a pure read of one state; cross-state semantics is new territory.

VERDICT: REVISE
