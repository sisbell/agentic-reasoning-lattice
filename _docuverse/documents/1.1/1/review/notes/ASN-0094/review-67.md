# Review of ASN-0094

## REVISE

### Issue 1: ASN length impacts reviewability and specification clarity

**ASN-0094, whole document**: The ASN runs to roughly 50,000 words.

**Problem**: A specification should be concise and normative. This ASN is buried under repetitive disclaimers ("recorded as a deliberate commitment"), multiple worked examples per concept (e.g., five worked checks of Sh5(b)'s checklist for the same discipline), consolidated reference tables that restate per-section material, and extensive cross-reference language. The substantive content — Sh-conf axiom, Sh0–Sh4 preservation, EffectiveWpSimplification, LinkAddressNotPrefixOfEmit — could be presented in roughly a third the prose. The current length makes thorough review impractical and obscures the underlying mathematical structure.

**Required**: Aggressive pruning. Many of the "deliberate commitment" framings, "consolidated reference tables", and "named in *Properties Introduced*" cross-references duplicate material already in body. Pick one canonical reference per concept.

### Issue 2: Counterfactual worked example for LinkAddressNotPrefixOfEmit Case II.B

**ASN-0094, "Worked examples — Cases I and II at concrete tumblers"**: The Case II.B worked example exhibits `b = [1, 0, 2, 0, 3, 0, 7, 1]` and `a = [1, 0, 2, 0, 3, 4, 0, 7, 1]` and claims the proof's "trace" can be walked on this configuration despite acknowledging "at position 6, `b_6 = 0 ≠ 4 = a_6`, so Prefix's componentwise-agreement clause already fails".

**Problem**: The example does not actually satisfy the proof's hypothesis `b ≼ a`. The "walk through the trace step-by-step" is a hypothetical-on-a-falsified-hypothesis exercise. The framework justifies this as "the formal proof discharges Steps II.0, II.1, II.2, II.3 unconditionally from the *supposition*, not from the concrete operands". But a worked example whose configuration doesn't satisfy the proof's premise is pedagogically confusing — it doesn't validate the proof on a concrete case; it walks through a contradiction trace where the contradiction surfaces earlier than the formal proof's stated terminus.

**Required**: Either remove the Case II.B "counterfactual" worked example (the formal proof and the Sub-case II.A example suffice) or replace it with a clearer framing — e.g., "the lemma rules out the existence of satisfying configurations; here is what the proof's argument *would* derive if the configuration existed, exhibiting the contradiction concretely". The current "walking the trace step-by-step" wording on a non-satisfying configuration suggests the proof has been validated on the example when it hasn't.

### Issue 3: Sh5(b) status downgraded to "documentation aspiration"

**ASN-0094, "Sh5(b) practical-strength status"**: "Sh5(b) operates as a documentation aspiration, not as a strict META discipline that the framework enforces through a tooled gate."

**Problem**: Sh5(b) is labeled META in the Properties Introduced table and is presented as a falsifiability discipline ("mechanical falsifiability without mechanical derivation"). But the framework admits the *enumeration step* (identifying which symbols appear in a template body) is "a manual reading task by the catalog author", and "a misclassified or omitted symbol at step 1 propagates to step 2 as a wrong (or missing) classification that no framework check catches." Combined with Sh5(a)'s same downgrade ("per-shape uniformity at body-shape level is downgraded to *aspiration*"), Sh5 in its current form is not a discipline the framework enforces — it's a design convention followed by hand-review. The "META falsifiability" claim is significantly weaker than initially advertised.

**Required**: Either commit to a tooled verification recipe (symbol extraction + classification gate), or drop the claim that Sh5(b) is a "discipline" and frame it explicitly as "design convention". The current wording promises more than the framework delivers.

### Issue 4: Audit-slice multiplicity loss as a "deliberate commitment" is a semantic shift from ASN-0086

**ASN-0094, "Audit-slice set-semantics commitment"**: The framework's registration `shape(R) = (*, 1, A, A_rel, ⊤)` with `idem = ⊤` causes duplicate Nullify calls to produce only one tuple in `L_R^Σ`, where ASN-0086 would produce two distinct tuples (by R0's freshness + R1's address injectivity).

**Problem**: This is a substantial change in observable behavior at the audit slice — not just a framing choice. ASN-0086's `Nullify` postcondition is silent about audit multiplicity but R0/R1 jointly admit duplicate calls. The framework's choice to register R with `idem = ⊤` effectively removes that admissibility for the bare-Nullify form. The framework provides a "migration discipline" but the compatibility commitment of `NullifyActiveSubsetCompatibility` is *scope-restricted to active-subset content*. Whether `idem = ⊤` should be the framework's *default* registration for R, or whether layers should be allowed to choose `idem = ⊤` vs `idem = ⊥` for R at registration time, is not given a clear justification.

**Required**: Either justify the `idem = ⊤` default explicitly (what positive property does it secure?) or move the Retraction `idem` flag to a per-layer choice with both readings supported. The current "deliberate commitment" framing assumes the choice is settled without making the design rationale visible.

### Issue 5: Resolution standalone admissibility verification path depends on aspirational discipline

**ASN-0094, "Resolution base templates at a standalone K"**: The framework adds a separate sub-walkthrough verifying that Resolution's base templates can be used standalone (no `_via` consumer). Verification is via worked example plus a "Sh5(b) audit walk".

**Problem**: The Sh5(b) audit walk's force depends on Sh5(b)'s status. With Sh5(b) downgraded to "documentation aspiration" (Issue 3), the audit walk verifies catalog admission by manual hand-curation — not by a framework gate. The framework's claim that the standalone path is "settled and exhibited" rests on author diligence rather than a normative rule.

**Required**: Tighten the relationship between Sh5(b)'s enforcement strength and the catalog claims that depend on it. If Sh5(b) is aspiration, then "settled" overstates the verification path.

### Issue 6: Three framework-local Peano-style axioms expand the commitment surface significantly

**ASN-0094, "Locally derived NAT primitives"**: The framework introduces (Peano-rec), (Peano-zero-least), (Peano-pred) as "framework-local commitments" because they are not derivable from the listed foundation NAT axioms (NAT-closure, NAT-order, NAT-discrete, NAT-addcompat, NAT-wellorder).

**Problem**: The framework's commitment package now requires three additional axioms beyond the foundation. The non-derivability arguments via counterexample carriers (e.g., `ℕ_a := {a} ∪ ℕ`) are sound, but this raises a question: should the foundation's NAT axioms be strengthened directly rather than supplemented per-ASN? The framework rejects this alternative as "out of scope" but doesn't argue why the supplements wouldn't propagate upstream. The result is that downstream consumers of ASN-0094 inherit these axioms as a package.

**Required**: Either (a) push the Peano supplements upstream into ASN-0034's NAT axiom list (where they belong if they're foundational), or (b) restructure the NAT-card and NAT-sub derivations to avoid the supplements (the ASN dismisses this as "mathematically infeasible" without showing the obstruction). The current framework-local supplement route is the least desirable option — it spreads ℕ-arithmetic across multiple ASNs.

### Issue 7: Sh4 Case A enumeration of transitions has unclear load-bearing status

**ASN-0094, Sh4 proof, "Step (Case A: A_K^{Σ'} = A_K^Σ)"**: "Case A's preservation is closed at the case-equation alone, with no further lemma consumed at the closure step." Followed by an enumeration of transitions that produce the case-equation: K.σ, K.α, non-K-coverage-equivalent K.λ, arrangement-modifying. Then: "The earlier draft's disclaimer 'transitions outside the enumeration but still satisfying the case-equation are equally admitted' is retracted: under the present exhaustiveness commitment, there are no `↦`-steps within the framework's scope outside the four enumerated classes, so the disclaimer's residual set is empty and the enumeration is load-bearing rather than expository."

**Problem**: The enumeration's role is ambiguous. The closure step ("Sh4 inherits") is trivial, but the enumeration *is* needed to know which transitions land in Case A's case-equation. The text vacillates between "expository orientation" and "load-bearing rather than expository". A reader trying to verify Case A's coverage needs to know which transitions are exhaustively covered.

**Required**: Pick one: either (a) the enumeration is load-bearing for completeness and each transition class must be verified to produce the case-equation (cite the supporting lemmas at each), or (b) the enumeration is illustrative and the case-equation is taken as the case-defining hypothesis. The current draft mixes the two readings.

## OUT_OF_SCOPE

### Topic 1: Multi-process consistency for the Sh4/FDD/SHCD contracts

**Why out of scope**: The framework explicitly restricts to single-process substrates and acknowledges multi-process atomicity as outside its scope (Open Questions item). A multi-process port would require a distributed coordination protocol at the `~`-equivalence class scope, which the current framework doesn't supply.

### Topic 2: Higher-arity link shapes (`|Σ.L(a)| > 3`)

**Why out of scope**: The framework operates on the standard-triple slice `L^Σ` of arity 3. Extending to higher-arity links would require additional shape components per extra slot and is explicitly flagged in *Scope and Substrate Scaffolding*.

### Topic 3: Composite shapes and shape-aware predicate composition

**Why out of scope**: The framework's atomic templates are derived from shape components; composite predicates that combine multiple K's into a new shape's worth of constraints are flagged as future work (Open Questions item).

### Topic 4: Ghost-targeting slot semantics

**Why out of scope**: The framework restricts slot addresses to already-allocated (`⊆ A^Σ`). Allowing ghost addresses in slot positions would require state-dependent conformance rules that the current framework doesn't support (Open Questions item).

META: The ASN remains within specification territory — it defines typed-relation state, operations, and invariants — but its scope has grown to encompass extensive META commentary (Sh5 catalog construction), worked-example pedagogy, and migration disciplines that probably belong outside the spec.

VERDICT: REVISE
