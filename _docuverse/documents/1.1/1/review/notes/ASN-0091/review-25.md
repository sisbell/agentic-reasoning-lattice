# Review of ASN-0091

## REVISE

### Issue 1: R-SP hypothesis fails in unified state when link subspace is populated
**ASN-0091, "REARRANGE as Vstream-Only Operation"**: "R-SP (RearrangeSufficientPrecondition) discharges RA-adm with respect to the ASN-0036 foundation invariants at the cut-sequence level by deriving that they hold at Σ' under the precondition `R-PRE(K) ∧ ASN-0036-invariants(Σ, d)`."

**Problem**: R-SP's hypothesis `ASN-0036-invariants(Σ, d)` is the conjunction of ASN-0036 invariants at the pre-state, which includes legacy S3 (referential integrity with target `dom(C)`). In the unified state shared with ASN-0047, when the link subspace is populated (as in every worked example with `[2, 1] ↦ a_link`), pre-state legacy S3 *fails* — link-subspace V-positions map to `dom(L)`, not `dom(C)`. The ASN itself acknowledges that S3 "cannot hold at any state populating the link subspace", yet then invokes R-SP for discharging the load-bearing invariants. As a whole-package sufficiency lemma, R-SP cannot be invoked when its hypothesis fails. The worked example admissibility verifications correctly do *not* cite R-SP — they verify each invariant directly. The abstract section's invocation of R-SP is the methodological outlier.

**Required**: Either (a) extract per-invariant discharges from R-SP's proof structure, verifying each load-bearing invariant's discharge depends only on a subset of pre-state invariants that survive in the unified state, or (b) provide a modified sufficiency lemma whose hypothesis uses S3★ in place of legacy S3. The discharges themselves are likely correct (the worked examples verify them directly); only the framing needs repair.

### Issue 2: S8★ content-subspace clause incorrectly cites "R-SP's discharge of ASN-0036's S8"
**ASN-0091, "REARRANGE as Vstream-Only Operation"**: "The content-subspace clause `M'(d)|_{V_{s_C}(d)} : V_{s_C}(d) → dom(Σ'.C)` is a direct application of ASN-0036's S8 to the restricted arrangement: under R-SP's discharge of ASN-0036's S8 at Σ' (which covers the foundation per-document arrangement decomposition)..."

**Problem**: The ASN earlier states "R-SP's S3 and S8 clauses, by contrast, are *not* load-bearing in the unified state" — yet here it invokes R-SP's S8 discharge as a load-bearing premise. R-SP's S8 discharge requires pre-state legacy S3, which fails in the unified state. The actual mechanism (direct application of ASN-0036's S8 to the restricted arrangement, where legacy S3 holds on the restriction because its range lies wholly in `dom(C)`) is sound and is what the worked example uses ("discharging S8★'s content-subspace clause by direct application of ASN-0036's S8"). The "under R-SP's discharge" parenthetical is both wrong and contradicts the surrounding text.

**Required**: Remove the "under R-SP's discharge of ASN-0036's S8 at Σ'" phrase; the direct application of ASN-0036's S8 to the restricted arrangement is the operative argument and should stand alone.

### Issue 3: RE-trans single-step claim's "origin(a)'s arrangement unchanged" fails for a case the ASN admits
**ASN-0091, "Cross-Document Transclusion Preserved"**: "the same relationship holds at Σ', with the same multiplicity, and the home document `origin(a)`'s arrangement is unchanged" — explicitly quantifying with "`d` here can be the rearrangement target or any other registered document, both of which are admitted".

**Problem**: The derivation reads "RE-other applies at `d' = origin(a)` (which satisfies `d' ≠ d` since `origin(a) ≠ d`) — independent of whether d itself is the rearrangement target." But RE-other's actual condition is `d' ≠ rearrangement-target`, not `d' ≠ d` (where d is the *transclusion-target* document). When d ≠ rearrangement-target ∧ origin(a) = rearrangement-target — admitted by the explicit quantifier — `origin(a) ≠ d` holds vacuously (the transclusion target d differs from both), but origin(a) *is* the rearrangement target, so its arrangement IS changed. The "independent of whether d itself is the rearrangement target" claim is wrong; the argument silently requires d = rearrangement-target. The multi-step RE-trans★ correctly identifies this gap with its "(iii) requires no step targets origin(a)" qualification, but the single-step version has no equivalent.

**Required**: Either restrict RE-trans to d = rearrangement-target, or split the claim into (i)+(ii) (transclusion persistence and multiplicity, which hold unconditionally) and (iii) (source arrangement unchanged, conditional on `origin(a) ≠ rearrangement-target`). The table entry needs corresponding qualification.

### Issue 4: RE-proj single-step formula's domain is not the quantifier's range
**ASN-0091, "Projection Transports Along π" and claims table**: "`project(e, d, Σ') = π(project(e, d, Σ))` for every endset `e`".

**Problem**: The formula uses π, which is the bijection on `dom(Σ.M(d_target))` for the rearrangement target d_target. For d ≠ d_target, π is not defined on `dom(Σ.M(d))` — the formula is type-incorrect. (RE-other gives the trivial preservation `project(e, d, Σ') = project(e, d, Σ)` for d ≠ d_target, but this is a different statement.) The multi-step section makes the correct distinction explicit via π̂_i (π_i on targeting steps, id otherwise); the single-step claim does not.

**Required**: Restrict the single-step RE-proj formula to d = d_target, or use a uniform formulation analogous to π̂ in the composition section. The table entry needs corresponding qualification.

### Issue 5: "RE-sub is the one consequence" is internally outdated
**ASN-0091, "Subspace Frame (REARRANGE_K-specific)"**: "RE-sub is the one consequence in this ASN that does not flow from the abstract class alone."

**Problem**: The "In-Subspace Exterior Frame" section a few paragraphs later introduces RE-ext, also explicitly "REARRANGE_K-specific". The "one consequence" framing is false by the ASN's own subsequent admission. This is minor but ought to be aligned during revision of the surrounding sections.

**Required**: Update the framing in the RE-sub introduction to acknowledge RE-ext as a companion REARRANGE_K-specific claim, or restructure so both are introduced under a single heading.

## OUT_OF_SCOPE

### Topic 1: Semantics of rearrangement on the link subspace
**Why out of scope**: The ASN's CS3 fixes the cut subspace at s_C, so REARRANGE_K does not realize the abstract class for the link subspace. Open Question 2 already names this; a separate ASN would establish K.μ~ semantics for link-subspace cuts.

### Topic 2: When a cut splits a transcluded span, are the two pieces "the same transclusion"?
**Why out of scope**: The ASN's RE-trans guarantees the (a, d) pair persists; whether the fragmented V-geometry constitutes "one" or "two" semantic transclusions is a higher-level question. Open Question 1 names this.

### Topic 3: ASN-0058 and ASN-0098 invariants in admissibility check
**Why out of scope**: The worked example admissibility check covers ASN-0036, ASN-0047, ASN-0093 invariants but does not enumerate ASN-0058 (M0–M16) or ASN-0098 (LP1–LP21) invariants. These are theorems derived from the foundation invariants verified, so they should be preserved transitively — but explicit verification belongs in a downstream consolidating ASN, not this one.

VERDICT: REVISE
