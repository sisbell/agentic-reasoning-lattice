# Review of ASN-0126

## REVISE

### Issue 1: The non-guarantee of unit-depth/R-Scope is stated four times in one passage
**ASN-0126, Single-source**: "Consequently `→_sh` does **not** guarantee unit-depth, and it does **not** guarantee R-Scope's single-tuple-scope result… Both are *additional operational disciplines*, not framework guarantees… `→_sh` itself does not mandate that wrapper — it gates R by Binary alone…"
**Problem**: The same fact — "Binary is weaker than unit-depth, so `→_sh` admits non-unit (contiguous-range) retractions" — is restated four ways in a single paragraph: (1) "does not by itself entail UnitDepthRetractionDiscipline," (2) "does not guarantee unit-depth," (3) "does not guarantee R-Scope's single-tuple-scope," (4) "does not mandate that wrapper… gates R by Binary alone." This is defensive restatement, not accumulating argument.
**Required**: Collapse to one statement: Binary is strictly weaker than unit-depth; `→_sh` gates R by Binary alone, so a non-unit (contiguous-range) retraction is a legal `→_sh`-step, and unit-depth/R-Scope hold only when the app routes through the unit-depth wrapper. Drop the duplicate clauses.

### Issue 2: P6 proof digresses to justify Emit_K over R0 rather than proving the step
**ASN-0126, The shape-gated emit (P6 proof, "Second")**: "This distinction is the crux of the address claim: R0 delivers merely *some* address fresh against `dom(Σ.L)`… of which `a_emit(Σ, d)`… is only the least; likewise ASN-0086's `K.λ` StateTransition deposits at 'a fresh key,' not specifically at `a_emit`. It is the `Emit_K` *operation*… that pins the address P6 names."
**Problem**: This is methodological self-defense against a possible objection ("why not R0?"), not a proof step. The proof needs only: apply `Emit_K` at `π(Σ)`, whose contract pins `a_emit(Σ, d)`. The L-ContiguousPrefix enumeration of "infinitely many on-chain indices" advances nothing toward the claim. This reads as a prior finding's content relocated into the proof body.
**Required**: Delete the digression; retain the one operative sentence ("apply `Emit_K`, whose contract pins the fresh address to `a_emit(Σ, d)`").

### Issue 3: The conditional disciplined-domain wp simplification advances nothing in this framework
**ASN-0126, The shape-gated emit**: "*Disciplined-domain simplification (conditional).*… *If* the substrate is so operated… the wp reduces to… collapsing… to `K registered ∧ Sh-conf(K, F, G) ∧ d ∈ dom(Σ.M)`… This characterizes what `K.λ_sh` checks only on the unit-depth-disciplined sub-domain; at a general `→_sh`-reachable state the full inherited wp… stands."
**Problem**: This sub-derivation conditions on a discipline `→_sh` explicitly does *not* enforce (Issue 1), then concludes that at a general reachable state the unsimplified wp stands — i.e., the simplification is never in force for this framework. It mirrors ASN-0086's wp Case-2 disciplined simplification structurally but feeds no property (P1–P7) and characterizes a sub-domain the framework never guarantees entering. It is mirrored content, not load-bearing.
**Required**: Remove the conditional simplification, or reduce to a single sentence noting that the third inherited conjunct does not vacate under `→_sh` because R is gated by Binary alone — which is the only consequence the rest of the note actually uses.

### Issue 4: "Span-count not residence" stated as a forward-pointer one-liner and again in full
**ASN-0126, Three shapes by G span count**: "The framework constrains the *span count* per shape, never the residence of the addresses those spans cover (Shape-conformance)."
**Problem**: This sentence is a bare restatement of the Shape-conformance section's full treatment ("`Sh-conf` consults nothing about content residence…"), pointing forward to the place that says it properly. The one-liner-plus-forward-pointer adds a hop the reader must resolve without gaining anything.
**Required**: Drop the trailing sentence from Three shapes; the residence point belongs once, in Shape-conformance where it is derived.

## OUT_OF_SCOPE

### Topic 1: idem semantics
**Why out of scope**: The registry carries an `idem` flag and P3 establishes its stability, but no operation in this ASN consults it; semantics are correctly deferred to Open question 1. Registering the field now is acceptable structural setup for the immutable registry — not an error. (P3 itself is a one-line corollary of P2 and reads as such; that is the most it should be.)

VERDICT: REVISE
