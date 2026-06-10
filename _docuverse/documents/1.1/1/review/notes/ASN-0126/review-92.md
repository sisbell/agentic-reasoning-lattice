# Review of ASN-0126

I checked the substantive content closely — P1–P6, C0, the lemmas (ProjectionBridge, RegisteredAdmissible, B1/B2), the wp Case-2 refinement, the three-move R-Scope re-derivation for the Binary wrapper, and every address in the Worked illustration. The proofs are sound: the gate is well-defined under the partial `Sh-conf`, the projection bridge transfers ASN-0086 results without claiming successors B2 cannot supply, and the born-nullified example checks out numerically (`a_R = …2.3 ∉ coverage(G_rng)`, `a = g = …2.4` at the lower endpoint, C3 false). The single finding is localized prose, consistent with the anti-bloat classifier.

## REVISE

### Issue 1: Forward-reference accretion in "The shape-gated emit"

**ASN-0126, The shape-gated emit** — two of the section's closing sentences point elsewhere instead of advancing the gate's definition:

(a) "The operation set an app invokes refines ASN-0086's {Emit_K, Observe_K, Nullify}... the empty-from Nullify... is superseded by the attributed-Binary wrapper Nullify_Binary — itself an instance of Emit_K... The set an app actually invokes is therefore {Emit_K, Observe_K, Nullify_Binary}."

(b) "K.σ and K.α keep their preconditions and C/M/L effects; like K.λ_sh they additionally frame the registry (Registry permanence)."

**Problem**:
- (a) names `Nullify_Binary` two sections before it is defined (Retraction as an attributed Binary). Its only content — which operations an app invokes — is not understandable until the wrapper exists, so it advances nothing where it sits; it is a use-site inventory parked in the gate section, forcing the reader to carry an undefined term forward.
- (b) previews the frame-condition list that Registry permanence states formally and then uses in P1's proof. "K.σ, K.α frame the registry" thus appears in two places; the gate-section mention is the redundant one.

**Required**: Move (a) to the end of Retraction as an attributed Binary, after `Nullify_Binary` is defined. Delete (b) — Registry permanence carries it where it is used. (The adjacent arity>3 paragraph — "every N > 3 emission has no →_sh image... left to Open Question 6" — is a legitimate deferral to an open question and need not move, though one paragraph for a consequence the arity-3 note never uses is generous.)

## OUT_OF_SCOPE

### Topic 1: Formal operation contract for Nullify_Binary
The note defines `Nullify_Binary` as a bare macro and correctly shows single-tuple-scope is an app obligation: the gate cannot inspect P-tgt, and raw `Emit_R` (Worked illustration, Step 1) lets an app file a range retraction regardless of any wrapper, so the substrate genuinely cannot guarantee it. Whether the *operation* should additionally carry P-tgt as a formal precondition — as ASN-0086's Nullify does, recovering single-tuple-scope as an operation-level guarantee for disciplined callers — is operational-semantics work the note explicitly defers (Open questions intro). Not a defect here.

### Topic 2: Runtime type registration
The registry is immutable by construction (P1), fixing the type vocabulary at `Σ_init`. Whether a substrate may admit types after initialization is left open (OQ4 touches pre-registration). New territory, not an error.

VERDICT: REVISE
