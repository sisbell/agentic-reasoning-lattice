# Review of ASN-0126

## REVISE

### Issue 1: Single-source overstates that unit-depth / R-Scope is "preserved by that construction"
**ASN-0126, Single-source (¶3)**: "The unit-depth property is supplied instead by the retraction *operation's construction* … which the framework inherits from ASN-0086 as a layer/operational commitment. R-Scope's single-tuple-scope result `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` … so it is preserved by that construction, not by the registration."
**Problem**: This reads as if unit-depth and R-Scope's single-tuple scope hold in the framework. They do not. `→_sh` gates R by **Binary only**, not unit-depth — and your own Worked illustration (Step 1) emits a *legal* `→_sh` retraction `(a_R, [c₁], G_rng)` with a non-unit range `G_rng` that nullifies three siblings, directly violating `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}`. So R-Scope is *not* preserved at the `→_sh` level; it holds only when the app exclusively routes through the wrapper, which `→_sh` does not mandate. The later "disciplined-domain simplification" paragraph states the correct position ("`→_sh`'s gate enforces only Binary conformance on R, not unit-depth"), contradicting Single-source.
**Required**: Reconcile the two. In Single-source, say plainly that `→_sh` does **not** guarantee unit-depth or R-Scope single-tuple scope; both are additional operational disciplines (an app-side commitment to the unit-depth wrapper), not framework guarantees — exactly as the disciplined-domain paragraph and the Worked illustration establish.

### Issue 2: Duplicate "Multi is permissive" prose
**ASN-0126, Three shapes**: "Multi (`|G|` finite) subsumes both — a Multi registration admits every tuple a Unary or Binary registration would, and more." **ASN-0126, Shape-conformance**: "For Multi the conjunct `|G| < ∞` holds for *every* endset … it is the unrestricted, permissive shape, constraining only F."
**Problem**: Two paragraphs in different sections state the same fact in different words — the flagged "same thing in different words" pattern.
**Required**: State it once (at the conformance definition, where `|G| < ∞`'s vacuity is derived) and drop the duplicate in Three shapes.

### Issue 3: Gate-vs-landing / born-nullified distinction stated three times with forward references
**ASN-0126, The shape-gated emit / P6 / Worked illustration**: the wp section says the gap is "witnessed concretely in the Worked illustration"; P6 closes with "the born-nullified gap"; the Worked illustration re-explains "P4 (the gate's enablement guarantee) is satisfied, while the strictly stronger active-subset wp is violated."
**Problem**: Multiple sections defer to the same downstream location and re-assert the same gate-vs-landing point — the flagged "multiple paragraphs defer to the same downstream location" pattern.
**Required**: Make the wp section the single site that states the gate/landing separation and forward-points once to the witness; remove the restatements in P6 and trim the Worked illustration to the trace itself.

### Issue 4: P4 re-derives the gate and the ASN-0086 contrast already given
**ASN-0126, P4**: "The only store-of-links step is `K.λ_sh`, whose preconditions are (0) arity 3, (i) K registered, and (ii) `Sh-conf(K, F, G)`: a non-triple value fails (0) … This is a definitional refinement of ASN-0086's relation, not a property of the unmodified `→` — which, having only L3 on `K.λ`, admits both unchecked-type and non-conforming tuples."
**Problem**: The full precondition list and the "refinement of ASN-0086's `→`, which admits non-conforming tuples" contrast are already established verbatim in *The shape-gated emit*. The Properties catalog should state the property and cite the derivation, not re-run it.
**Required**: Reduce P4 to the claim plus a pointer to *The shape-gated emit*; drop the re-enumerated preconditions and the repeated ASN-0086 contrast.

### Issue 5: P3 restates P2's argument; idem carries no role in this note
**ASN-0126, P3**: "Corollary of C0 and P1, by the same two-premise argument as P2."
**Problem**: P3's derivation re-states P2's two-premise argument rather than citing it, and `idem` has no operational meaning here — every use is deferred to Open Question 1. Listing idem-stability as a co-equal property when it is P1 applied to one inert registry field is redundant with P2.
**Required**: Collapse P3 into a one-line corollary of P2 ("same argument, applied to the idem field"), or fold idem-stability into P2's statement. Do not re-run the derivation.

## OUT_OF_SCOPE

### Topic 1: Idem-at-emit semantics, behavior catalog, default/composed predicates, standard registrations
**Why out of scope**: Open Questions 1–6 correctly defer all operational semantics. The registry's job in this note is shape gating; what `idem`, behaviors, and pre-registered types *do* is the successor note's territory, not a gap in this one.

### Topic 2: Multi-source (`|F| > 1`) and arity `N > 3` relations
**Why out of scope**: The note deliberately commits to `|F| = 1`, arity 3; richer relations drop to ASN-0086's ungated `→`. Open Question 6 owns the extension path. Not an error here.

META:

VERDICT: REVISE
