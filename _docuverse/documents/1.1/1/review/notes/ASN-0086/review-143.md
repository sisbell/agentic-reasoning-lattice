# Review of ASN-0086

I checked the substantive proofs first — R0 (both emission branches), R0a (both home cases), R0a-Cor1's zero-position tracking, R3, R6a–R6c, R7a's Δ-replay, and the wp analysis. The mathematics holds: the cross-home antichain argument in R0a Case 1 is sound (zeros add along the prefix, forcing the third separator to a shared position and hence equal homes), the same-home case correctly reduces to T3 via (UL), and the wp Case 2 derivation legitimately shows both domain restrictions are load-bearing with distinct witnesses. The worked sketch's nullification arithmetic checks out at every step.

The findings below are the ones the `review-mode.anti-bloat` classifier asks for: prose that does not advance the argument and forces the reader to skip past it.

## REVISE

### Issue 1: Duplicated framing sentence across two adjacent opening paragraphs
**ASN-0086, opening paragraphs (3rd and 4th)**: Paragraph 3 ends "...but predicates compose more cleanly over relations than over endsets, and several substrate-level guarantees become easier to state in this form." Paragraph 4 then states "The answer is that predicates compose more cleanly over typed relations than over endsets, and several substrate-level guarantees — most centrally the active/audit distinction... — become easier to state and prove in this form."
**Problem**: These are near-verbatim restatements of the same claim — the anti-bloat pattern "two paragraphs in the same document say the same thing in different words." The reader processes the affordance claim twice before any reasoning begins.
**Required**: Cut the tail of paragraph 3 (or merge), keeping the single statement in paragraph 4 that adds the active/audit hook.

### Issue 2: Defensive justification and vague inventory in the Foundation paragraph
**ASN-0086, "Foundation"**: "...together with the sub-allocator chain lemmas (ChainDiscipline, FirstEmission, ChainMembershipForOrigin, and supporting chain-structure lemmas)... We consume these directly rather than reinventing them."
**Problem**: "rather than reinventing them" is a defensive justification that advances no reasoning, and "and supporting chain-structure lemmas" is filler that names nothing checkable. Citation of the specific lemmas at their actual use sites is where the orientation belongs.
**Required**: Drop "rather than reinventing them" and the vague trailing clause; cite each lemma where it is first invoked.

### Issue 3: Meta-commentary describing the document's own behavior
**ASN-0086, Weakest-Precondition Analysis preamble**: "Case 1 deliberately stops short of the weakest precondition and says so explicitly."
**Problem**: This is essay-about-the-text (commentary on how the section behaves), not argument. It is also redundant with the in-Case-1 statement "It is **not** the weakest precondition (see *Non-weakestness* below)," which carries the same content at the point where it is load-bearing.
**Required**: Delete the preamble sentence; the Case 1 body already establishes the sufficient-not-weakest distinction.

### Issue 4: Overlapping arity-3 / P2 scope discussion in two locations
**ASN-0086, Definition — Nullify** ("The arity-3 restriction matches this note's scope. ... no `A_K^{Σ'}` would feel the effect under the present definitions.") and **wp Case 1** ("Single-tuple scope is therefore *arity-independent*: nullifying an arity-4 address would establish... The scope condition P2 ... is consequently absent from the wp.").
**Problem**: Both passages make the same point — P2 is a scope label, not an executable gate, and the single-tuple result does not depend on arity. The second restatement does not refine the first; it repeats it in different words.
**Required**: State the arity-3 scope rationale once (in the Nullify definition, where P2 is introduced) and have wp Case 1 reference it rather than re-deriving it.

## OUT_OF_SCOPE

### Topic 1: Concurrency, atomicity, and observation consistency
**Why out of scope**: The Open Questions raise Emit/Observe atomicity, the consistency model for observing `A_K` transitions, and ordering guarantees on Observe results. These are genuine future-ASN territory — this note correctly fixes the sequential, atomic transition model (SequentialTransitionAxiom inherited from ASN-0093) and proves the relational properties within it. A concurrency model is a new layer, not a defect here.

### Topic 2: Multi-arity typed relations `L_K^{(n)}`
**Why out of scope**: The note explicitly restricts to standard-triple links and flags higher-arity relations as an open question. Extending the typed-relation construction to `n`-ary slots is new content, not a gap in the present claims.

VERDICT: REVISE
