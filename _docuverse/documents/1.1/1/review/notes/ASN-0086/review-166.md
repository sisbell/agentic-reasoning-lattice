# Review of ASN-0086

I checked the core proof chain — R0 (freshness + state-local preservation), L-ContiguousPrefix, R0a (antichain), Cor1 (`#E = 2`), R1–R7a, and both wp cases — against the foundation contracts (ASN-0034/0036/0040/0043/0093). The mathematics is sound: the two-case split in R0a (cross-home zero-counting vs. same-home chain contiguity) is clean, R0's careful `#E ≥ 2` vs. `#E = 2` distinction across the state-local/substrate-conforming boundary is correct, and the wp Case 2 disjunction with its two-failure-mode domain analysis is a genuine weakest precondition, not a sufficient one. The worked sketch's concrete tumblers verify out. I found no correctness errors in the proofs.

The remaining issues are a contract inconsistency and anti-bloat (the `review-mode.anti-bloat` classifier is active).

## REVISE

### Issue 1: Nullify's P1/P2 are presented as preconditions in the Properties table but as non-gating in the body
**ASN-0086, Definition — Nullify and Properties table**: The body states "(P2) `|Σ.L(a)| = 3` ... does not gate emission" and "P1 gates only the postcondition `a ∈ nullified(Σ')`, not emission" — only P0 (`d_retr ∈ dom(Σ.M)`) gates the operation. But the Properties table row reads "Nullify ... for caller-supplied `d_retr ∈ dom(Σ.M)` and `a ∈ A_rel^Σ` with `|Σ.L(a)| = 3`," presenting all three uniformly as input conditions.

**Problem**: The contract is ambiguous about what `Nullify` actually requires of `a`. This is not cosmetic: the wp Case 1 load-bearingness argument *drops P1* ("For P1, choose `a ∉ A_rel^Σ` distinct from the fresh emitter") and analyzes the resulting behavior. That argument is only well-posed if `Nullify` is callable with `a ∉ A_rel^Σ` — i.e., if P1 is not a hard precondition. The Properties table contradicts the premise of the analysis that depends on it.

**Required**: Make the signature consistent. Either state in the table that `Nullify`'s only gating precondition is `d_retr ∈ dom(Σ.M)`, with P1/P2 as a postcondition-establishing / scope condition respectively; or, if `a ∈ A_rel^Σ` is a true precondition, reframe wp Case 1 so it does not "drop" a typed precondition.

### Issue 2: Non-fixpoint semantics of retraction-of-retraction stated twice in the same property
**ASN-0086, R6b body and R6b "Remark (non-fixpoint interpretation)"**: The body's closing sentence — "The membership test consults the audit slice `L_R^Σ`, which retains `b`'s tuple regardless of `b`'s active-subset status" — and the Remark — "nullifying a retractor `b` does not 'undo' `b`'s nullifying effect ... because `nullified` ranges over the audit slice `L_R^Σ`, which retains `b`'s tuple" — assert the identical mechanism in different words.

**Problem**: Two paragraphs in the same property say the same thing. The same point is then demonstrated concretely in Worked Step 3 (legitimate) and touched again in R6c's consequence and Open Question 3. The Remark's mechanism clause is verbatim-equivalent to the body's and advances no new reasoning.

**Required**: Drop the Remark's mechanism restatement; if the "not a fixpoint" naming is worth keeping, fold it into the body's final sentence rather than appending a separate paragraph.

### Issue 3: Worked sketch attributes L2/L11a/L12b discharge to "R0's generic argument," outside R0's scope
**ASN-0086, Worked Sketch Step 1**: "The remaining L-invariants (L2, L3, L4(c), L11a, L12, L12a, L12b, L14, L14a, L-fin) discharge by R0's generic argument applied with the concrete `b₁`."

**Problem**: R0's stated conclusion is "Σ' state-local-conforming," whose `StateLocalInvariants` set (ASN-0043) does not include L2, L11a, or L12b — these are lemma-consequences (L2 from the `home` definition, L11a = GlobalUniqueness instantiated, L12b from L12a+L1a), not step-preserved state-local invariants, and R0's proof body never addresses them. Attributing their discharge to "R0's generic argument" overstates what R0 proves.

**Required**: Either note that L2/L11a/L12b hold automatically as consequences (not via R0's preservation argument), or drop them from the per-step discharge list since they are not invariants the step must maintain.

## OUT_OF_SCOPE

### Topic 1: Atomicity/consistency of Observe against concurrent Emit
The Open Questions already defer the concurrency model (atomicity of Emit vs. Observe, ordering of Observe results) to future work. Correctly excluded — this note specifies the single-authority sequential substrate only.

### Topic 2: Higher-arity typed relations `L_K^{(n)}`
The restriction to standard-triple links is explicit and the generalization is flagged as a future question. Not an error here.

VERDICT: REVISE
