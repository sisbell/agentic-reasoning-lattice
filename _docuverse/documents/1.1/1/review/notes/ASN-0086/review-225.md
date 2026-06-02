# Review of ASN-0086

## REVISE

### Issue 1: wp Case 1 self-emit branch contradicts Worked Sketch Step 4's own framing

**ASN-0086, "Weakest-Precondition Analysis" Case 1**: "This is the same self-emit configuration constructed in Worked Sketch Step 4 (`a₃ = a_emit(Σ_3, d)`)."

**ASN-0086, "Worked Sketch" Step 4**: "(This is *not* a relational-layer `Nullify`: Nullify is P1-confined to a pre-existing target `a ∈ A_rel^Σ`, whereas `a₃ ∉ dom(Σ_3.L)`. The call is admissible to a direct K.λ caller.)"

**Problem**: These two passages assign the same construction to two different operations. The recently-widened wp Case 1 treats the self-emit disjunct `a = a_emit(Σ, d_retr)` (where P1 is false, `a ∉ A_rel^Σ`) as lying *inside the operation Nullify's* weakest precondition, and explicitly cites Step 4 as the concrete instance of that branch. Step 4, however, asserts the construction is **not** a Nullify at all — that "Nullify is P1-confined" — and routes it through a direct K.λ caller precisely because the target is not pre-existing. The wp result `P0 ∧ (P1 ∨ a = a_emit)` is sound only if Nullify executes under P0 alone (P1 not a hard precondition); Step 4's "P1-confined" claim says the opposite. One of the two readings must be wrong: either Nullify is P1-confined (then the self-emit disjunct is outside its domain and the wp collapses to `P0 ∧ P1`), or it is not (then Step 4's parenthetical and the relational-layer "P1 target" gloss are misstated).

**Required**: Reconcile the two passages. If P1 is a layer convention rather than an operation precondition (consistent with "Definition — Nullify": *"P0 governs execution; P1 and PC condition the … postcondition"*), then strike "Nullify is P1-confined" from Step 4 and re-frame Step 4's call as a self-emit instance of Nullify (not a non-Nullify). If P1 is genuinely a hard precondition of Nullify, drop the self-emit disjunct from wp Case 1 and remove the cross-reference to Step 4.

### Issue 2: Revision-history prose in wp Case 1 (anti-bloat)

**ASN-0086, "Weakest-Precondition Analysis" Case 1**: "An earlier sufficient-precondition reading wrote `P0 ∧ P1` and silently excluded this branch; the analysis below shows it is the missing slack that separates the weakest precondition from the merely sufficient one."

**Problem**: This sentence narrates the document's own prior state ("an earlier … reading wrote …") rather than advancing the argument — exactly the reviser-drift / essay-in-a-proof pattern the anti-bloat classifier targets. The mathematical content (that the self-emit disjunct is required for weakestness) is already carried by the derivation and the "load-bearing" bullets below it; the historical framing is noise the precise reader must skip.

**Required**: Delete the "earlier sufficient-precondition reading" clause. State the disjunct's role directly from the derivation, without reference to prior versions.

### Issue 3: Meta-definition of "load-bearing" in wp Case 1 (anti-bloat)

**ASN-0086, "Weakest-Precondition Analysis" Case 1**: "…the disjunct is required for weakestness, not merely admitted: 'load-bearing' here means *each disjunct is reachable and the precondition is the weakest*, not that any single conjunct is independently necessary."

**Problem**: This clause defines the reviewer's/author's own terminology ("load-bearing means…") instead of proving anything about the operation. It is meta-prose explaining word choice, compounded by the fact that the substantive content — each disjunct realizable, precondition weakest — is already shown in the two bullets immediately above.

**Required**: Remove the terminological gloss; the preceding bullets already establish reachability and weakestness.

## OUT_OF_SCOPE

### Topic 1: Substrate-level guarantee for the unit-depth retraction discipline
The note correctly leaves the unit-depth retraction discipline as a layer commitment and flags (Open Questions) whether it should become a substrate guarantee via a dedicated retraction K-operation. The wp Case 2 domain restriction is honest about this gap. Elevating it is new territory (a substrate operation addition), not a defect here.

### Topic 2: Concurrency/atomicity of Emit vs Observe
Listed in Open Questions; genuinely belongs to a future ASN that introduces a concurrency model.

VERDICT: REVISE
