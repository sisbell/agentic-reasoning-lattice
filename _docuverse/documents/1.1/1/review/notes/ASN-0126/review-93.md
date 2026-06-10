# Review of ASN-0126

I checked the proofs line by line — P1, P3, P4, P5, P6, RegisteredAdmissible, ProjectionBridge, the three-move R-Scope re-derivation for the Binary wrapper, the refined wp, and the worked-illustration arithmetic (including the `a_emit` chain `ℓ₁→ℓ₂→a_R→g` and the `δ(3,9)` range). They hold. The note is genuinely rigorous, has concrete examples, a non-trivial wp case (the "born nullified" witness), and derives its consequences. One precision defect remains.

## REVISE

### Issue 1: "Emit_K ... carry over unchanged" contradicts the gating thesis

**ASN-0126, Retraction as an attributed Binary (operation-set paragraph)**: "`Emit_K` and `Observe_K` carry over unchanged; the empty-from `Nullify`, excluded above (The shape-gated emit), is *superseded* by the attributed-Binary wrapper `Nullify_Binary` ..."

**Problem**: The framework's central act, stated in *The shape-gated emit*, is "This framework **refines** the emit step," replacing `K.λ` with the gated `K.λ_sh`. The note itself shows that an `Emit_K` invocation failing the gate has "**no** `→_sh` image" (*The shape-gated emit*, para 3: an `|F|=0` emit fails (ii) for registered K and (i) for unregistered K, "either way ... no `→_sh` image"), and P5's proof realizes every emit by "lifting `Emit_K`'s ungated `K.λ` step ... back to a gated `K.λ_sh` step." So `Emit_K`'s firing condition is strictly tightened — it is *the* gated operation. Describing it as carrying over "unchanged," lumped with the genuinely-unchanged pure-read `Observe_K`, contradicts the note's own thesis and obscures the one thing this note exists to add. A reader reconciling "refines the emit step" with "`Emit_K` ... carry over unchanged" is left with a contradiction.

**Required**: Separate the two. `Observe_K` (a pure read) carries over unchanged; `Emit_K` carries over but is now gated by `K.λ_sh` — its successful invocation requires registration and `Sh-conf`. E.g.: "`Observe_K` carries over unchanged and `Emit_K` carries over now gated by `K.λ_sh`; the empty-from `Nullify` is superseded by `Nullify_Binary` (itself a gated `Emit_R`)."

## OUT_OF_SCOPE

### Topic 1: Operational semantics, runtime registration, and richer arity
**Why out of scope**: I checked whether the note skips genuine gaps versus deferring future territory. The immutable-registry design (no runtime registration), the `N>3` and `|F|>1` extensions (OQ6), and the predicate/behavior/idempotency semantics (OQ1–5) are all correctly fenced off by the Open Questions and the explicit "no runtime registration to add one" constraint. These are new territory for successor notes, not defects here. The note also correctly inherits its foundation invariants (S0–S3, L0–L14) via the projection bridge rather than re-proving them — appropriate, not a gap.

VERDICT: REVISE
