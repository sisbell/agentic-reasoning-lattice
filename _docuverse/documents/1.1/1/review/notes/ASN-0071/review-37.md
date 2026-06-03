# Review of ASN-0071

I checked the central derivation (prefix confinement), the resolution/find definitions, the subset and routing arguments, and traced the worked scenario step-by-step. The mathematics is sound: the PC argument (componentwise fact → totality → full agreement) is acyclic and complete; the S3★ ∧ S3★-aux routing correctly forecloses a third subspace; the worked scenario's composite-boundary coupling discharges (J0/J1★/J1'★) are correct; the cross-depth and interior-action-point examples are computed correctly. I found no proof gap.

What remains are anti-bloat findings, which this note's `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: Rationale prose justifying a precondition rather than stating it
**ASN-0071, The query**: "A link-subspace span would name nothing the operation is for, since a link address has a unique home document recoverable directly from its tumbler via `origin` ... we exclude such queries by construction. The companion floor `actionPoint(ℓ) = #u ≥ 2` ... Both preconditions feed the *prefix confinement* argument below"
**Problem**: This paragraph explains *why* the preconditions are needed (link-subspace motivation, "we exclude such queries by construction") and forward-references the PC argument, rather than stating what the preconditions are. The preconditions are already listed completely in the vspec definition one paragraph above. This is the "new prose explains why X is needed rather than what it says" pattern; a reader must skip past it to reach the actual PC derivation.
**Required**: Cut the motivational sentences. Keep only the load-bearing fact that PC actually consumes (`subspace(u) = s_C` and `actionPoint(ℓ) = #u ≥ 2`), and let the PC derivation use it directly.

### Issue 2: Implementation-advice meta-prose in guarantee sections
**ASN-0071, Set semantics**: "Set semantics must be stated explicitly because the natural implementation — iterating over each queried I-address and collecting source documents — produces duplicates by default. The specification requires deduplication; an implementation that returns a multiset of `(d, a)` pairs satisfies neither the type signature nor the intent."
**ASN-0071, Finiteness**: "The operation does not promise a small result, only a finite one. Implementations that must materialize the entire result before returning it should be designed expecting that the result can grow with the docuverse."
**Problem**: Both passages justify the spec to implementers and give implementation guidance rather than advancing the abstract guarantee. The guarantee (`|{x ∈ find(Q)(Σ) : x = d_*}| ≤ 1`; `|find(Q)(Σ)| < ∞`) is fully stated by the formulae and their derivations; the surrounding implementer-facing prose adds nothing to the system-level claim.
**Required**: Delete the implementation-rationale sentences. The set codomain `P(E_doc)` and the finiteness derivation already carry the guarantee.

### Issue 3: Forward-reference deferral of the subset claim's gating precondition
**ASN-0071, Resolution**: "the subset claim `iaddrs(Q)(Σ) ⊆ dom(Σ.C)`, gated on the `wp-defined` precondition of *The operation* below (which ensures every `Σ.M(d_s)` consulted is a defined arrangement)."
**Problem**: The subset claim is proven in *Resolution* but is made conditional on a precondition (`wp-defined`) not introduced until the following section, forcing the reader forward and back to evaluate the claim. The `wp-defined` precondition (`d_s ∈ Σ.E_doc`) is elementary and could be stated where it is first relied upon, removing the deferral.
**Required**: State the `d_s ∈ Σ.E_doc` gating where `iaddrs_one` is defined (it is already needed for `dom(Σ.M(d_s))` to be meaningful), so the subset claim is self-contained at the point of proof rather than deferred.

### Issue 4: Verification bullets restate the already-computed trace
**ASN-0071, A worked scenario, "What this verifies"**: the F-SHARE / F-DIST / F-PART / Resolve-equivalence / F-SOUND / F-FILT / F-CUR bullets.
**Problem**: Each bullet re-narrates a computation performed verbatim a few lines earlier in the same scenario (e.g., F-SHARE restates that `d_A, d_B, d_D ∈ find(Q)`; F-DIST restates the set-membership counts; F-SOUND restates the `d_C` exclusion). This is the "two paragraphs say the same thing in different words" pattern — the trace and the bullet list duplicate each other.
**Required**: Either drop the bullet restatements and let the trace stand, or reduce each bullet to a one-line label binding the named property to the line of the trace that established it, without re-deriving.

## OUT_OF_SCOPE

### Topic 1: Relationship between current-state `find` and the historical containment relation `R`
**Why out of scope**: The ASN correctly distinguishes present-tense `find` from the permanent `R`, and defers the formal guarantee linking them to an open question. This is genuinely new territory (a separate query semantics), not a defect in the present-tense operation specified here.

VERDICT: REVISE
