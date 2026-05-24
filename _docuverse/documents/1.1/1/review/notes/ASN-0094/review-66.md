# Review of ASN-0094

## REVISE

### Issue 1: Cross-ASN reference to non-foundation ASN-0093
**ASN-0094, LinkAddressNotPrefixOfEmit Case I**: "By ChainMembershipForOrigin (ASN-0093), both `a` and `a'` are chain elements of `A_L(d)`."
**Problem**: ASN-0093 is not in the foundation list (ASN-0034, ASN-0043, ASN-0086). Direct citation violates the per-ASN self-containment rule.
**Required**: Route this and similar references through ASN-0086's SubstrateConformingLayer Definition, or through the local *Per-document link sub-allocator chains* scaffolding clause.

### Issue 2: Cross-ASN references to ASN-0036 in SubstrateConformingLayer definition
**ASN-0094, *Substrate-conforming-layer scaffolding* section**: "The full L/S/M/C invariant list of ASN-0036, ASN-0043, and ASN-0093."
**Problem**: ASN-0036 and ASN-0093 are not in the foundation list. While the SubstrateConformingLayer Definition is in ASN-0086 (foundation), ASN-0094 reproduces the catalog enumeration here, creating direct dependencies on non-foundation ASNs.
**Required**: Reference the SubstrateConformingLayer Definition by name only ("per ASN-0086's SubstrateConformingLayer Definition"), without enumerating the ASN-0036/ASN-0093 catalog items locally.

### Issue 3: New axioms in Appendix not in foundation
**ASN-0094, Appendix**: "(Peano-rec)", "(Peano-zero-least)", "(Peano-pred)" introduced as supplements with proofs of non-derivability from foundation NAT axioms.
**Problem**: The Appendix introduces three new axioms not present in the listed foundation NAT axioms (NAT-closure, NAT-order, NAT-discrete, NAT-addcompat, NAT-wellorder). The non-derivability arguments justify their addition, but they constitute a foundation extension introduced locally within ASN-0094.
**Required**: Either lift these to the foundation explicitly (extending ASN-0034 or whichever foundation ASN owns NAT axioms), or restructure NAT-card and NAT-sub derivations to avoid them. Note the disclaimer "a future draft may extend the foundation to enumerate (Peano-rec) explicitly" acknowledges the irregularity but does not resolve it.

### Issue 4: Sh5 per-shape uniformity downgraded mid-document
**ASN-0094, *Status of per-shape uniformity (downgraded to aspiration in this draft)***: "The earlier draft phrased per-shape uniformity at the body-shape level... The present draft explicitly downgrades this from a commitment to an aspiration."
**Problem**: Downstream catalog claims that "Resolution inherits DirectedPair's templates," "the two `(0, 1)` rows share `is_K`," and similar body-shape convergences become *aspirations* rather than theorems. A future catalog extension could register divergent template bodies at an existing shape without any mechanical gate rejecting it. The Sh5(b) discipline catches only citation-side violations (data symbols outside (i)–(iv)), not body-shape divergence.
**Required**: Either re-elevate per-shape uniformity to a committed property (supplying the procedural recipe the framework now declines to provide), or explicitly mark each cross-row body-shape claim as catalog-specific rather than framework-derived. Currently the Resolution row reads "*mechanically derived from the same templates as DirectedPair*" — but the *Status* paragraph contradicts this.

### Issue 5: Sh5(b) discipline is only procedurally falsifiable
**ASN-0094, *Catalog extension is a manual review process***: "The discipline above is enforced by hand-review against each proposed catalog addition, not by a mechanical derivation procedure."
**Problem**: The audit table records the author's classification decisions but provides no second-pass verification beyond the audit cell itself. A misclassified or omitted symbol at step 1 (enumeration) produces a downstream classification error that no mechanical check catches. The framework calls this "post-hoc record-keeping" rather than verification — which means the catalog's well-formedness depends on author diligence at every row, not on framework gates.
**Required**: Either commit to a tooled verification recipe (e.g., a symbol-extraction tool against a registered six-category table) or explicitly downgrade Sh5(b) from "META discipline" to "documentation aspiration" so downstream consumers understand the gate's strength.

### Issue 6: Hand-wave at K.λ frame-condition routing
**ASN-0094, *Routing of K-op frame-condition facts***: "The K-op frame-condition properties used here... are sourced through ASN-0086's `SubstrateConformingLayer` Definition... rather than via any ASN outside this review's foundation."
**Problem**: The ASN claims K.σ/K.α/K.λ frame conditions (which store each op touches and preserves) are "sourced through" ASN-0086's SubstrateConformingLayer, but ASN-0086's `→ — DomExtendingTransition` Definition specifies the frame conditions directly. The "routing through SubstrateConformingLayer" framing obscures the cleaner direct citation.
**Required**: Cite ASN-0086's `→` Definition directly for K-op frame conditions; reserve the SubstrateConformingLayer routing for chain-discipline and invariant-catalog facts not directly in `→`'s signature.

### Issue 7: Sh0/Sh1 Case A's exhaustiveness not fully explicit
**ASN-0094, Sh0 proof, Case A**: "This case covers all K.σ-steps and K.α-steps... all K.λ-steps emitting a tuple of type `K'` not coverage-equivalent to K... and all arrangement-modifying steps."
**Problem**: The proof asserts that K.λ-steps at K' ≁ K leave `L_K` unchanged, but does not explicitly cite the `~`-class indexing of `L_K^Σ` (`L_K^Σ = L_{K'}^Σ` iff `K ~ K'`, from ASN-0086) as the reason. A reader reconstructing the argument has to infer this from the `L_K^Σ` definition; without the explicit citation, the case-equation `L_K^{Σ'} = L_K^Σ` is asserted rather than derived.
**Required**: Add explicit citation to ASN-0086's `L_K^Σ` Definition (specifically its `~`-class indexing clause) at Case A's K.λ-at-non-K-type sub-case.

### Issue 8: Worked example for Sub-case II.B contradicts its own framing
**ASN-0094, LinkAddressNotPrefixOfEmit, Case II.B worked example**: "Step II.2: b's three zero positions n_1 = 2, n_2 = 4, n_3 = 6 lift to a's zero positions exactly (verifiable: a_2 = 0, a_4 = 0, a_6 = 4 ≠ 0..."
**Problem**: The worked example states `a_6 = 4`, contradicting Step II.2's claim that `a`'s zeros coincide with `b`'s at positions 2, 4, 6. The ASN handles this by noting "the contradiction surfaces at Step II.2 here rather than at Step II.3," but this means Step II.1's "lift to a's zero positions exactly" *fails* in the concrete example, which contradicts the formal claim that Step II.1 establishes the lift unconditionally.
**Required**: Either pick a worked example where Step II.1's claimed lift actually holds (requiring `a` to have zeros at all of b's zero positions), or rephrase the example to acknowledge that the concrete instance reveals the contradiction at an earlier step than the general proof structure.

### Issue 9: NullifyActiveSubsetCompatibility's "single-tuple scope" reading at suppressed call
**ASN-0094, NullifyActiveSubsetCompatibility Case B**: "(i) single-tuple scope. By R0a applied at Σ, `dom(Σ.L)` is a tumbler-prefix antichain, so `{t : a ≼ t} ∩ A_rel^Σ ⊆ {a}`."
**Problem**: At the suppressed branch, `Σ_target := Σ` and `A_rel^{Σ_target} = A_rel^Σ`. The single-tuple-scope conclusion `{t : a ≼ t} ∩ A_rel^Σ = {a}` is established from R0a, but this is the *pre-call* state's antichain property — it would hold at any reachable Σ regardless of whether `Nullify` succeeds or fails. The corollary claims to *preserve* the postcondition, but at the suppressed branch the postcondition holds *independently* of whether the call fired. This isn't preservation; it's vacuous satisfaction.
**Required**: Either reframe the corollary as "the active-subset content is satisfied at Σ_target whether the call succeeds or fails" (a weaker claim than preservation), or strengthen the corollary to identify when the post-call state's content meaningfully differs from a vacuous read of pre-call state.

## OUT_OF_SCOPE

### Topic 1: Multi-process substrate concurrency
**Why out of scope**: The framework explicitly commits to single-process substrates via the Sh4 contract's *Scope: single-process substrate* clause and the Open Questions section. Multi-process atomicity protocols would extend the framework's scope rather than fix the current draft.

### Topic 2: Layer composite `K_is_fresh` and `mtime` accessor
**Why out of scope**: The composite is documented as illustrative of how `K_target_of` combines with layer-supplied data; `mtime` falls outside Sh5(b)'s six categories by design. The framework's audit table correctly rejects it. Promoting layer-supplied accessors to first-class catalog citizens is future work.

### Topic 3: Ghost-targeting slot semantics
**Why out of scope**: Open Question item explicitly flags ghost-targeting in slot positions as a future shape-family design question. L9 (ASN-0043) admits ghost spans generally; the framework's restriction to allocated addresses in slot positions is a deliberate scope commitment.

META: The ASN's specification core (shapes, Sh-conf, Sh0–Sh4, per-K disciplines) is appropriate abstract specification material; the heavy META commentary (catalog construction methodology, gate ordering rationale, migration disciplines) is acknowledged as META and does not constitute drift into implementation mechanics.

VERDICT: REVISE
