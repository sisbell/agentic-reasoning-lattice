# Review of ASN-0076

The mathematics here is sound and the proofs are, with one class of exception, complete: K.λ preconditions are discharged step-by-step at both intermediate states, boundary cases (empty successor endsets, first-vs-subsequent emission, single-document reuse of `d_new`) are handled, and the worked example checks E0–E10 against concrete tumblers as the standards require. References are confined to foundation ASNs (0034/0036/0043/0047/0098); no cross-ASN violation. The remaining issues are prose accretion around the link-projection reconciliation, consistent with this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Defensive reconciliation prose in E7
**ASN-0076, E7 (Lineage Witness), "Reconciliation with ASN-0098's discoverability"**: "The `covers` predicate above must not be confused with ASN-0098's `discoverable_from`... The two run in opposite directions and rest on different state components... The distinction is load-bearing because EDITLINK never arranges its outputs: E10 establishes that the composite performs no K.μ⁺_L step."
**Problem**: This is defensive meta-prose justifying a non-conflict rather than advancing E7's claim. It explains why a newly-introduced predicate does not collide with a foundation predicate, and defers downstream to E10 and to LP17/LP18 to do so. The claim E7 actually proves — that the spans `(ℓ_old, …)` and `(ℓ_new, …)` lie in `ℓ_sup`'s endsets and their coverage contains those addresses — is fully discharged in the proof above this passage.
**Required**: Cut the reconciliation paragraph to at most one sentence stating that `covers` is an inverse link-store lookup independent of arrangement (so the orphan/resurrection behavior of LP17/LP18 applies), without the "must not be confused" / "load-bearing" framing.

### Issue 2: Motivational essay closing E7
**ASN-0076, E7**: "This property is what makes the supersession link operative as a record of editing. It is not enough to *create* the supersession link; the structural relationship must be present in the link store so that any conforming discovery operation can recover the lineage. Without this structural witness, an 'edit' would be a write-only act with no path to recover the lineage."
**Problem**: Pure motivation in a structural slot — restates the value of E7 without adding a reasoning step. The preceding proof already establishes the structural witness.
**Required**: Delete.

### Issue 3: `covers` predicate introduced for a single use
**ASN-0076, E7**: defines `covers(Σ, a) ≡ {ℓ ∈ dom(Σ.L) : (E i, (s, w) … : a ∈ coverage({(s, w)}))}`.
**Problem**: The predicate is used nowhere outside E7 and its introduction is what forces the Issue-1 reconciliation paragraph (the new name superficially resembles the foundation's `discoverable_from`). E7's content is directly expressible as `ℓ_old ∈ coverage(Σ'.L(ℓ_sup).e₁) ∧ ℓ_new ∈ coverage(Σ'.L(ℓ_sup).e₂)` — which the proof already derives via E4 + PrefixSpanCoverage.
**Required**: State E7 directly in `coverage` terms (a foundation definition) and drop the `covers` wrapper, which removes the need for Issue 1's reconciliation entirely.

### Issue 4: "The implication is…" restatement paragraphs
**ASN-0076, E2 and E10**: e.g. E2 — "The implication is that no operation, applied to no input, can produce two links with the same I-address. A 'fresh edit' of `ℓ_old` is necessarily a *new entity*… indistinguishable in kind from any other newly-allocated link…"
**Problem**: These trailing paragraphs re-express the just-proved claim in prose without deriving a new consequence. E2's distinctness and E10's frame are each fully established in their proofs; the restatements are the kind of interpretive padding the anti-bloat pass targets.
**Required**: Either delete, or replace with a genuine derived consequence not already stated in the claim (E10's "pull model" remark is the one fragment worth keeping; fold it into one sentence).

## OUT_OF_SCOPE

### Topic 1: Supersession-chain invariants, cycle handling, and "current successor" computation
**Why out of scope**: These are correctly deferred to the Open Questions list and depend on a link-search/authorization specification not yet written. EDITLINK only needs to establish that the structural witness exists, which it does.

### Topic 2: Recognition convention for the supersession type (`τ_sup`)
**Why out of scope**: E4 properly hedges that semantic identification of `ℓ_sup` as a supersession requires an external `τ_sup` convention; the note does not — and should not — fix that convention here.

VERDICT: REVISE
