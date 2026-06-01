# Review of ASN-0047

This is a carefully constructed transition model and the core arguments (the K.δ case split, the K.μ~ link-subspace fixity proof, the D-SEQ★ derivation, GlobalLineage, the per-state vs composite-boundary partition) are internally consistent and discharge their obligations. My findings concern meta-prose accretion around forward references and a few restatements that the precise reader must skip past, plus one placement issue. No correctness defects found.

## REVISE

### Issue 1: Admissibility-filter prose explains the clause's epistemic status rather than advancing it, and is restated three times
**ASN-0047, *Decomposition of K.μ~***: "**The admissibility filter (clause (i)) is a hypothesis on the candidate π, not a consequence of the preconditions: every π the operation admits yields a post-state satisfying the full per-state invariant package — S3★, S3★-aux, S8a, S8-depth, S8-fin, D-CTG★, D-MIN★ (and hence the derived D-SEQ★) — on `M'(d)`.**"

**Problem**: This sentence (and the following "The filter is non-vacuous, witnessed by the transposition `π_swap`...") explains what *kind* of statement clause (i) is — a hypothesis, not a consequence — rather than doing argumentative work. The same content is then restated in the matrix S3★/K.μ~ cell ("admissibility filter stipulates S3★(Σ'); π_swap witnesses non-vacuity") and again in the Class (a) S3★ prose. This is exactly the "defensive justification" pattern: the reader must read three near-identical framings before reaching Step (A), which is the paragraph that actually derives subspace preservation.

**Required**: State clause (i) once in the definition (the filter is a hypothesis on π; π_swap witnesses non-vacuity) and let Steps (A)/(B) carry the reasoning. Remove the bolded epistemic-status restatement and the duplicate framings in the matrix cell / Class (a) prose; a bare pointer to the definition suffices.

### Issue 2: S8★ "strictly weaker than S8" stated twice within its own definition
**ASN-0047, *Amendments to existing transitions* (S8★)**: First: "S8★ carries only ASN-0036's S8 conditions (a) ... and (b) ... It intentionally does *not* carry ASN-0036's S8 condition (c) — uniqueness ... S8★ asserts only the *existence* of a per-subspace run decomposition, not its maximality or uniqueness." Then later in the same definition: "S8★ takes the place of ASN-0036's S8 ... but it is strictly *weaker* than S8: it carries conditions (a) and (b) ... and drops condition (c) (uniqueness of the maximal-run decomposition), **as detailed above**."

**Problem**: The second passage restates the first in different words and signposts itself ("as detailed above"), confirming the duplication. Two paragraphs in the same definition say the same thing.

**Required**: Keep the first statement (carries (a)/(b), drops (c), existence-only) and delete the second; if a closing reminder is needed before the matrix, compress to one clause.

### Issue 3: Implementation-rationale parentheticals in abstract slots
**ASN-0047, *V-position depth (operational)***: After fully stating the live-depth re-pinning rule, the text adds "(This matches the implementation: after a subspace is fully cleared, the next insertion re-derives its V-position from the current arrangement, floored at that subspace's minimum, with no stored prior depth to reuse.)"

**Problem**: The rule is already fully specified in the preceding sentences; the parenthetical justifies the abstract rule by appeal to implementation mechanics rather than advancing the specification. This is the "explains why ... rather than what it says" pattern. (Compare the boilerplate "(with zero intermediate 1s at m = 2)" repeated across every worked example — each is a local re-derivation of the same D-SEQ★ degeneracy that the D-SEQ★ definition already establishes once.)

**Required**: Drop the implementation parenthetical (the abstract rule stands on its own), and replace the repeated "(with zero intermediate 1s at m = 2)" asides with a single forward note at the D-SEQ★ definition that the canonical form degenerates at m = 2.

## OUT_OF_SCOPE

### Topic 1: Link-inheritance and tombstoning mechanisms under forking/withdrawal
The fork composite deliberately starts d_new's link subspace empty, and the D-CTG★/D-MIN★ strengthening forbids interior link withdrawal. Both are correctly deferred to a future operations ASN (and listed in Open Questions). Not an error here.

### Topic 2: Concurrency and address-space exhaustion for link allocation
The Open Questions raise serialization and freshness-under-exhaustion. These are genuinely new territory (this ASN assumes SequentialTransitionAxiom and unbounded T0), not gaps in the present model.

VERDICT: REVISE
