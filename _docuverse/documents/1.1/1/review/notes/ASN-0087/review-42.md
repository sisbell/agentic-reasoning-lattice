# Review of ASN-0087

This note carries `review-mode.anti-bloat`. The technical content is sound — the wp analysis, the worked example, and the three-class invariant sweep are genuinely thorough and correctly cite foundations (all cross-references are to foundation ASNs 0034/0036/0043/0047/0093/0098, no violations). My findings are about accreted meta-prose and forward-reference patterns, which is what this mode asks me to surface.

## REVISE

### Issue 1: Reflexive-route derivation deferred from three separate sites
**ASN-0087, *What Is Indexed?* / M-Reflexive / M-DiscSymmetry**: "(we derive it once, in *Weakest Precondition for Discoverability*, Case 2.)" — and M-Reflexive's table entry: "(derivation in *Weakest Precondition for Discoverability*, Case 2)" — and M-DiscSymmetry's table entry pointing at the same place.
**Problem**: Three locations defer the reflexive-route derivation to WP Case 2. This is the multi-paragraph-deferral-to-one-downstream-location pattern; the reader is bounced forward from three places to a single proof.
**Required**: State the reflexive route once at its derivation site and let the claims reference it without the repeated "(we derive it once, in X)" / "(derivation in X)" scaffolding. The forward pointers compound across the prose, the M-Reflexive table row, and the M-DiscSymmetry table row.

### Issue 2: Foundation lemma's internal proof re-narrated after the result is already obtained
**ASN-0087, *Freshness of the Allocation***: "SubsequentEmissionFreshness (ASN-0093) gives `ℓ ∉ dom(Σ.C) ∪ dom(Σ.L)`. That lemma's own three-way split discharges within-document freshness (via ChainEnumerationInjectivity), cross-subspace freshness (via DisjointSubAllocatorChains and SC-NEQ), and cross-document freshness (via Cross-doc disjointness composed with T10...)."
**Problem**: The first sentence cites the foundation lemma and obtains the freshness result. The second sentence re-narrates that lemma's *internal* three-way proof split, which adds nothing to ASN-0087's argument — the conclusion is already in hand. This is a use-site recap of a verified foundation result.
**Required**: Drop the second sentence. Cite SubsequentEmissionFreshness for the result; the foundation owns its own proof structure.

### Issue 3: Defensive "stated once" / "derive it once" non-duplication signposting
**ASN-0087, *What Is Indexed?***: "We state the resulting symmetry property once here (M-DiscSymmetry)." and "(we derive it once, in *Weakest Precondition for Discoverability*, Case 2.)"
**Problem**: "We state ... once here" and "we derive it once" are defensive meta-prose whose only function is to assure the reader the content is not duplicated elsewhere. This kind of self-justifying signposting is a tell of accreted anti-duplication patches; it does not advance the claim.
**Required**: Remove the "once here"/"once" hedging. A claim stated in one place needs no announcement that it is stated in one place.

### Issue 4: Effect frame restated as prose in *What Does Not Change*
**ASN-0087, *What Does Not Change***: "By the same reasoning, no prior link in `dom(L)` is modified (L12), no other document's arrangement is modified (frame on `M`), no entity is allocated, no provenance pair is recorded."
**Problem**: This enumerates exactly the frame already given as equations in *Effect* (`Σ'.C = Σ.C`, `Σ'.E = Σ.E`, `Σ'.R = Σ.R`, L12, frame on `M(d')`). The section's value is the *derivation* (that the frame follows from the composite's structure — K.λ touches only `L`, K.μ⁺_L only `M(d)`); the re-enumeration of the frame contents is redundant with *Effect*.
**Required**: Keep the structural derivation; drop the clause-by-clause restatement of the frame already given in *Effect*.

### Issue 5: Rhetorical restatement in *Permanence of the Recording*
**ASN-0087, *Permanence of the Recording***: "The link forever names the same set of I-addresses — even as those I-addresses' V-arrangements change, even if all V-arrangements lose them entirely, even if new documents transclude content sharing those I-addresses (in which case LP18 makes the link rediscoverable from those new documents)."
**Problem**: The three guarantees (L12, LP13, LP3★) already establish coverage permanence precisely. The "even as ... even if ... even if ..." cascade is an evocative re-statement of the same consequence, with the parenthetical smuggling in an LP18 scenario that belongs to *Side Effects* / *Permanence*, not here.
**Required**: State the consequence (coverage is fixed across all reachable states) once from the three lemmas; cut the rhetorical cascade.

## OUT_OF_SCOPE

### Topic 1: Mandatory well-formedness for forward-reaching endsets
The first Open Question (constraints on endsets referencing not-yet-allocated addresses) is genuine future territory. The ASN correctly defines `StandardAuthoring` as a *discipline* without mandating it; whether to require it is a downstream decision, not a gap in this ASN.

VERDICT: REVISE
