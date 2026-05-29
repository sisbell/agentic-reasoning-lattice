# Review of ASN-0036

I checked every proof in this ASN against its preconditions, case coverage, and boundary behavior. The mathematical content is unusually careful — the S8 singleton-partition proof handles within-subspace, cross-subspace, and the `m = 2` / `m ≥ 3` depth split explicitly; D-CTG-depth, D-SEQ, and the insertion-position predicates all dispatch their boundary cases (empty arrangement, depth-2 vacuity, single position) rather than waving at them. I found no skipped case or unproved postcondition. The findings below are the anti-bloat patterns the `review-mode.anti-bloat` classifier asks me to surface, plus one precision note.

## REVISE

### Issue 1: S0 frame defends a labeling decision instead of advancing the claim
**ASN-0036, S0 ("Read directionally" paragraph)**: "Nelson emphasises this separation as 'the architectural foundation of everything'; it carries no formal content beyond S0, so we do not give it a separate label."
**Problem**: This is meta-prose about the document's own labeling choices — exactly the "defensive justification / prose justifying naming" pattern. The directional reading ("an arrangement-only transition cannot alter C") is fine; the trailing clause justifying why no separate label is assigned advances nothing and must be skipped to follow the argument.
**Required**: Keep the directional reading sentence; delete the Nelson-quote-plus-non-labeling justification.

### Issue 2: S4 states value-independence three times
**ASN-0036, S4**: body — "The content store C is oblivious to values"; proof — "The independence from content values deserves emphasis... invariant under any assignment of values to addresses"; frame — "The content store C and value domain Val play no role in the proof."
**Problem**: The proof's "deserves emphasis" paragraph and the frame line are the same point ("addresses distinct regardless of values") in different words — the "two paragraphs say the same thing" pattern. The proof already established this at "GlobalUniqueness yields a₁ ≠ a₂ directly"; the emphasis paragraph re-derives it.
**Required**: Drop the "independence from content values deserves emphasis" paragraph (the body's value-sensitivity-of-M point carries the one non-redundant idea); let the frame line stand alone.

### Issue 3: T8-comparison essay sits inside the S1 proof
**ASN-0036, S1 proof**: "S1 is the domain conjunct of S0, and it specialises T8... The two properties have different scopes: T8 covers addresses that have been allocated but may carry no content, while S1 covers addresses at which content has actually been stored. ∎"
**Problem**: The proof is complete at "...by definition of subset inclusion." The T8-scope discussion is commentary placed before `∎`, so a reader tracking the proof must pass through essay to reach the QED. Content-wise it is the "explains why a claim differs from a related one" filler.
**Required**: Move the S1-vs-T8 distinction out of the proof body (a one-line remark after the formal contract, or delete — S1's contract already cites S0, not T8).

### Issue 4: S7b/S7a Depends entries carry rationale rather than citation
**ASN-0036, S7b Depends**: "T10a.4 ... supplies the surrounding T4-validity (no adjacent zeros, positive endpoint components a₁ ≠ 0 ∧ a_{#a} ≠ 0) on which T4b's projections in the postcondition rely, and supplies the bound zeros ≤ 3 that S7b strengthens to the equality zeros(a) = 3."
**Problem**: This is a use-site narrative ("on which … rely," "that S7b strengthens") embedded in a dependency slot — the structural-slot-essay pattern. The citation only needs to name what T10a.4 supplies (T4-validity, `zeros ≤ 3`).
**Required**: Reduce to the cited facts; drop the "on which … rely / S7b strengthens" explanatory clauses.

### Issue 5: S5 "vacuous" reading of transition invariants is asserted, not pinned
**ASN-0036, S5 proof**: "S0 (content immutability) and S1 (store monotonicity) quantify over state transitions Σ → Σ'; we consider Σ_N as a single state with no transition, so both hold vacuously."
**Problem**: S5's postcondition says a *state* "satisfies S0–S3," but S0/S1 are defined only over transitions. The vacuous reading is defensible, but "single state with no transition" is doing load-bearing work without saying what "a state satisfies a transition invariant" means — does it quantify over all transitions *out of* the state, all *into* it, or is the witness simply exhibited with no transition relation at all? As written the reader must supply the convention.
**Required**: One sentence fixing the convention (e.g., "a state Σ satisfies a transition invariant iff every transition incident to Σ does; the witness is exhibited as an isolated state, so the universal is vacuous"), so the consistency claim is unambiguous.

## OUT_OF_SCOPE

### Topic 1: Operation-level preservation of D-CTG / D-MIN and displacement invariants
The ASN defines `ValidInsertionPosition` / `ValidFirstInsertionPosition` as state predicates but defers (correctly, per the Open Questions) whether INSERT/DELETE/COPY/REARRANGE preserve D-CTG, D-MIN, S2, and what the displacement mechanism must guarantee.
**Why out of scope**: Operation frame/postconditions are explicitly excluded; the predicates here are state-level characterizations of well-formed positions, and the operation semantics that consume them belong to the operations-layer ASN.

### Topic 2: Subspace-alignment between `subspace(v)` and the first element-field component of `M(d)(v)`
The ASN names this as an operations-layer preservation obligation rather than a state invariant.
**Why out of scope**: This is a property established by editing operations, not a constraint derivable from the strand-model state alone; deferring it is appropriate, not an omission.

VERDICT: REVISE
