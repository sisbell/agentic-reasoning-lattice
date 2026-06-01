# Review of ASN-0086

## REVISE

### Issue 1: R0's manual invariant-preservation discharge duplicates K-Step Conformance Preservation

**ASN-0086, R0 proof ("L-invariant preservation across the K.λ-step")** and **Lemma — K-Step Conformance Preservation**: The lemma states "Every K-op `→`-step (K.σ, K.α, K.λ) is conformance-preserving, by its ASN-0093 contract" — and clause (a) of substrate-conforming is "preserve the full L/S/M/C invariant catalog." Yet R0 then re-derives that same preservation conjunct-by-conjunct across four paragraphs ("The frame-fixed and transition-shape invariants…", "The address-structural L-invariants at `a`…", "The one conjunct that needs a per-address chain argument is L1c…"), and *then* closes with "K-Step Conformance Preservation yields that Σ' is itself substrate-conforming."

**Problem**: The full invariant-preservation obligation is discharged twice. If the lemma's appeal to the ASN-0093 contract genuinely settles clause (a) (it should, since K.λ's invariant preservation is an ASN-0093 result), then R0's multi-paragraph re-derivation is redundant bloat. If it does *not* settle it, then the lemma's blanket "by its ASN-0093 contract" is the hand-wave and R0 is where the real work lives — in which case the lemma should cite R0, not assert independently. As written, the reader must reconcile two discharges of one obligation, and R0 invokes the very lemma whose content it just re-proved.

**Required**: Discharge invariant preservation in exactly one place. Either keep the lemma's citation-based discharge and have R0 cite it for the state-local catalog (retaining only the genuinely R0-specific obligation — L1c's per-address chain construction and the standard-triple L3 shape — which the generic lemma does not specialize), or localize the detailed argument and have the lemma defer to it. The same redundancy appears in R7a's discharge bullets (1)–(2), which re-establish state-independent predicates L0/L1/L1b at `a_k` after already asserting "preserves the full invariant and chain-discipline catalog by its own ASN-0093 contract."

### Issue 2: Nullify's P1 (and PC) are mischaracterized as execution "gates"

**ASN-0086, Definition — Nullify**: "Nullify gates on two conditions — P0: `d_retr ∈ dom(Σ.M)` … and P1: `a ∈ A_rel^Σ` … together with the precondition PC that Σ be substrate-conforming…"

**Problem**: P0, P1, and PC do not behave alike, yet "gates on" lumps them together. The wp Case 1 analysis itself disentangles them: dropping P0 means "Nullify does not execute, no post-state Σ' is produced" (a genuine execution guard, via K.λ's home-precondition), whereas dropping P1 means the op *does* execute (Σ' is produced) and merely fails the single-tuple-scope postcondition. So P1 is not an execution gate at all — it is a precondition for the *scope postcondition*, and PC likewise conditions R-Scope, not execution. Calling all three "gates" would lead an implementer to add a runtime guard rejecting non-live targets, which the formal semantics (the `Emit_R` alias, which emits unconditionally given P0) does not do.

**Required**: Distinguish the execution precondition (P0) from the postcondition-conditioning preconditions (P1, PC). State explicitly that Nullify executes whenever P0 holds, and that P1/PC are what the single-tuple-scope guarantee (R-Scope) is conditioned on — not validation checks that abort the operation.

### Issue 3: Arity-3 restriction stated twice in adjacent sections

**ASN-0086, AdmissibleTypes** ("For the rest of this development we restrict attention to standard-triple links … Higher-arity links … exist in `dom(Σ.L)` but are not members of any `L_K`; they admit an analogous construction with additional slot positions, which we do not pursue here.") and **Definition — TypedRelation** ("Note that `L^Σ` collects only the arity-3 links; higher-arity links in `dom(Σ.L)` are outside its scope, as noted above.").

**Problem**: The same restriction-plus-deferral is asserted in two places, the second explicitly back-pointing ("as noted above") — two paragraphs saying the same thing. This is the duplication pattern the anti-bloat classifier targets.

**Required**: State the arity-3 restriction once (at AdmissibleTypes, where it is introduced) and drop the TypedRelation restatement.

### Issue 4: Essay-content remark in a structural slot

**ASN-0086, Remark — relation to ℘(A) × ℘(A)**: "A generic mathematical typed relation is a subset of `℘(A) × ℘(A)` … Our typed relation is richer … The projection … loses information that the substrate retains (R0, R1)."

**Problem**: This paragraph advances no claim's reasoning; it is motivational framing with forward references (R0, R1) embedded among the definitions. Per the anti-bloat guidance, prose that the precise reader must skip to follow the construction is a finding.

**Required**: Either remove, or compress to a single clause attached to Definition — TupleAddress noting that the address component is what distinguishes this structure from the set-theoretic relation. The forward references to R0/R1 should not appear before those lemmas are stated.

## OUT_OF_SCOPE

### Topic 1: Higher-arity typed relations `L_K^{(n)}`
The note restricts to standard triples and defers `|Σ.L(a)| > 3` to an Open Question. The binary-projection-vs-direct-higher-arity question is genuinely new territory (it requires a slot-indexed relational algebra this note does not develop), not a gap in the present construction.

### Topic 2: Concurrency/atomicity of Observe vs Emit
The Open Questions on Observe ordering and Emit/Observe atomicity concern a consistency model the substrate layer does not yet specify. These belong to a future ASN on the observation interface, not to this one.

VERDICT: REVISE
