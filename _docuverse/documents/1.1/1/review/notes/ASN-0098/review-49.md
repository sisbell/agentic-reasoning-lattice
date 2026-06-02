# Review of ASN-0098

## REVISE

### Issue 1: K.σ referenced outside the declared working frame
**ASN-0098, LP8 and LP18**: LP8 — "either K.σ (ASN-0093) or K.δ in the IsDocument case (ASN-0047) — registering a fresh document"; LP18 — "any document-registration operation (K.σ of ASN-0093 or K.δ in the IsDocument case of ASN-0047 — unified by LP8...)".
**Problem**: The ASN fixes its working frame as "the ASN-0047 transition-model frame layered over the ASN-0093 allocation substrate." ASN-0047's atomic vocabulary (per ValidComposite★) is K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ — document creation is K.δ-IsDocument. K.σ is the substrate primitive that K.δ subsumes in this frame; it is not an operation of the frame. The closing claim "LP4–LP10 and LP14 cover every atomic operation kind of the working frame" is already true without K.σ. So the K.σ disjunct covers an operation the frame excludes — either redundant coverage or a frame inconsistency.
**Required**: State the lemmas over the frame's operation (K.δ-IsDocument), and drop the K.σ disjunct — or, if K.σ is genuinely reachable in this layered frame, say so explicitly rather than hedging "either/or."

### Issue 2: "Tightness is state-relative" stated twice, near-verbatim
**ASN-0098, tight definition vs. achievability**: First — "Tightness is a state-relative predicate; in the canonical use case `Σ_e` is the state at which `e` was incorporated into a link, but the predicate is well-defined at any state." Later — "Tightness is a state-relative predicate evaluated at `Σ_e`; what it requires here is that every F-candidate from `A_X(d_0)` lying in `[s, s ⊕ ℓ)` is already in `dom(Σ_e.C) ∪ dom(Σ_e.L)`..."
**Problem**: Two paragraphs assert the same fact in different words. Worse, the second sentence immediately restates its own preceding sentence: "...hence already emitted at `Σ_e` — discharging tightness against this chain at `Σ_e`. Tightness is a state-relative predicate evaluated at `Σ_e`; what it requires here is... discharges exactly that obligation." The reader processes the same discharge claim twice.
**Required**: State the state-relativity of `tight` once (at the definition). In the achievability argument, assert the constraint discharges the tightness obligation in a single sentence and delete the restatement.

### Issue 3: Provenance-indifference claim restates its own opening
**ASN-0098, Discovery Independence of Origin**: Opening — "The discoverability of a link from `d` depends on none of them — only on the I-address content of `d`'s arrangement." Closing — "A link can therefore be discovered from any document whose arrangement currently maps to any I-address... The system commits to indifference of provenance at the point of discovery."
**Problem**: The closing two sentences re-deliver the paragraph's opening claim with added editorial flourish ("The system commits to indifference..."). The load-bearing content — that LP12's RHS references only `coverage` and `ran` — is already made mid-paragraph.
**Required**: Keep the inspection-of-LP12 derivation; drop the closing restatement to a single concluding clause.

### Issue 4: Minor — `F` introduced informally before its formal definition
**ASN-0098, Boundary and Width Behaviour (opening)**: "The set `F` of substrate-emittable addresses is the domain against which the 'boundary insertion does not extend the link' property is formalised — the addresses the substrate could K.α/K.λ-emit..." followed two sentences later by "The set of substrate-emittable addresses is the union of all such chain elements... defined formally as: F = {...}."
**Problem**: "Substrate-emittable addresses" is described twice (motivational gloss, then formal set-builder). The first description's only non-redundant content is the zero-extension exclusion remark.
**Required**: Fold the zero-extension exclusion into the formal definition's surrounding prose and remove the duplicate informal introduction.

## OUT_OF_SCOPE

### Topic 1: Reverse-discovery, V-order reflection, cross-link induced discovery
**Why out of scope**: Correctly deferred to Open Questions. These require new primitives/invariants and belong in future ASNs, not revisions here.

### Topic 2: Link-canonical endsets under content-subspace-emptying contraction
**Why out of scope**: The ASN explicitly notes (final Open Question) that LP12b's disjointness argument inverts for link-resident endsets and defers the matching guarantee. This is new territory, not a defect in the present claims.

The core technical content is sound: LP-Fin's interval count, the LP12a weakest-precondition derivation (with its enabledness conjunct and `R = ∅` collapse to `false`), LP12b's content-canonical discharge, and the LP11 rebinding proof are each carried out case-by-case with boundaries (empty arrangement, empty endset, maximal contraction) addressed. The worked trace exercises both a transclusion branch and a reordering branch with explicit admissibility checks. The findings above are scope/redundancy, not gaps in the proofs.

VERDICT: REVISE
