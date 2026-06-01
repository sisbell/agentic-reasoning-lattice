# Review of ASN-0086

I checked the proofs (R0/R0a/R1–R7a, the wp analysis, and the worked sketch arithmetic) against the foundations. Correctness is sound: the chain arithmetic in the worked example is right (a₁=1.0.1.0.1.0.2.1 through a₃=...2.5), R0a's two-case antichain argument holds, the wp Case 2 derivation is valid in both directions, and all cross-ASN references target the listed foundations (no Standard-7 violation). The findings below are anti-bloat / load-bearingness, consistent with the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: R7a's payload is not exercised by its sole consumer
**ASN-0086, Definition — relational layer (Corollary proof)**: "So every Σ.L-affecting step the layer takes simply is an Emit_K call — there is nothing to decompose. By R7a, the layer admits no other composite route to Σ.L, so {Emit_K, Observe_K, Nullify} is exhaustive of its link-store effects."

**Problem**: R7a (NoExtraClassAffectsL) is a heavyweight lemma — a multi-step replay construction discharging four K.λ preconditions plus K.σ interleaving. Its only citation in the note is this Corollary, which then states "there is nothing to decompose." The relational layer by its own Definition has no operations other than Emit_K/Nullify (each already a single K.λ →-step), so "no other composite route" is true by definition, not by R7a. The decomposition machinery is never actually exercised. R7a's genuine payload — that *any* substrate-conforming layer's L-mutations reduce to K-steps, which backs the headline "three operations suffice to span all visible substrate change" — is the claim about *arbitrary* `↝`-steps, not the relational layer's own (trivially-decomposing) ones. As written, the long proof serves a decorative citation.

**Required**: Either (a) state R7a's actual load-bearing thesis directly — exhaustiveness of K-steps against arbitrary substrate-conforming layers — as a first-class result the note relies on, so the proof's weight is justified; or (b) move R7a to the future multi-operation layer that would consume it, since the relational-layer Corollary's conclusion follows from the layer's Definition without it.

### Issue 2: P0/P1/P2 role-assignment stated three times
**ASN-0086, Definition — Nullify** (opening): "Nullify has three conditions, with distinct roles: (P0) ... gates emission ... (P1) ... establishes the nullification postcondition ... (P2) ... is a scope label"; in-body: "Thus P1 gates only the postcondition a ∈ nullified(Σ'), not emission"; **Properties table, Nullify row**: "the only gating precondition is P0 ... while P1 ... establishes the postcondition ... and P2 ... is a scope label".

**Problem**: The same gating/postcondition/scope role-assignment is announced in the Definition's opening paragraph, re-derived in the Definition's body, and restated verbatim in the table. The opening announce-then-derive is redundant with the body's derivation, and the table reproduces the full role text rather than summarizing.

**Required**: Let the Definition body *derive* the roles (P1 from the `nullified` discharge, P2 from the `A_K` scope) without the pre-announcing opening sentence, and reduce the table row to the operation signature plus a pointer.

## OUT_OF_SCOPE

### Topic 1: Higher-arity typed relations
**Why out of scope**: The note explicitly restricts to standard-triple links (`|Σ.L(a)| = 3`); `L_K^{(n)} ⊆ A_rel × ℘(A)^n` and binary projections of multi-arity links are new territory (Open Question 2), not an error here.

### Topic 2: Dynamic type-address collision across layers
**Why out of scope**: Whether two layers independently choosing colliding `T_admissible` type addresses need coordination (Open Question 9) is a future concurrency/coordination concern, not a gap in this note's single-layer development.

VERDICT: REVISE
