# Review of ASN-0086

## REVISE

### Issue 1: "R0a-Cor1" is a prerequisite of R0a, not a corollary — label and ordering are inverted

**ASN-0086, R0a Case 2 / R0a-Cor1**: R0a Case 2 reads "By R0a-Cor1 (ContiguousPrefix, stated and proved below), the set `{a'' ∈ dom(Σ.L) : origin(a'') = d}` is a contiguous initial segment..." and R0a-Cor1 is presented after R0a as its corollary.

**Problem**: R0a-Cor1's proof is an induction on the conformance-witnessing transition sequence using only the at-most-one-key-per-home discipline, the frontier-landing consequence, and ChainEnumerationInjectivity — it never invokes R0a. R0a's same-home case, conversely, *consumes* R0a-Cor1. So the dependency runs R0a-Cor1 → R0a, yet the naming ("Cor1") and document order ("stated and proved below") both assert the reverse. A reader checking the proof must reconstruct that the "corollary" is actually a lemma the main result rests on, and verify the absence of circularity themselves.

**Required**: Reorder so the contiguous-prefix result precedes R0a, and relabel it as a lemma (e.g., L-ContiguousPrefix) rather than a corollary of R0a. State explicitly that its proof does not depend on R0a, so the no-circularity fact is on the page rather than left to the reader.

### Issue 2: R5.1 citation in Nullify's definition assumes a precondition the composition's stated execution domain drops

**ASN-0086, Definition — Nullify**: The same definition both asserts "Only P0 gates emission: ... the underlying Emit_R executes and produces a Σ' even when `a ∉ A_rel^Σ`" and, in the next paragraph, "By Corollary R5.1, R0 at `d_retr` emits the retraction triple `(∅, {(a, δ(1, #a))}, R)`."

**Problem**: Corollary R5.1's contract is stated "For any `a ∈ A_rel^Σ`." When `a ∉ A_rel^Σ` (which the P0-only-gates paragraph explicitly admits), R5.1 does not apply, so the emission must instead be justified by the directly-stated T12 well-formedness (`#a ≥ 1` by T0, `actionPoint(δ(1,#a)) = #a ≤ #a`). The definition reads as though R5.1 governs the whole composition, creating friction at exactly the case the surrounding prose was constructed to handle.

**Required**: Justify the emission via the general T12 argument (already present) and restrict the R5.1 citation to the `a ∈ A_rel^Σ` (P1) path, or drop the R5.1 citation here since the T12 argument covers both.

### Issue 3: Use-site inventory / protocol rationale in the substrate-conforming-state definition

**ASN-0086, Definition — substrate-conforming state**: "This discipline and its frontier-landing consequence are stated authoritatively here; downstream proofs (R0a-Cor1, R7a) invoke them by name without re-deriving the `J+1` mechanics."

**Problem**: This sentence advances no part of the definition. It enumerates downstream consumers (R0a-Cor1, R7a) and explains the protocol for citing the discipline — exactly the "definition's introduction enumerates downstream consumers" and "protocol rationale" patterns the anti-bloat classifier targets. The discipline and its frontier-landing consequence stand on their own; the citation bookkeeping belongs in the consuming proofs, where they already invoke it.

**Required**: Delete the sentence. Let R0a-Cor1 and R7a cite the discipline by name at their use sites without an advance announcement.

### Issue 4: Forward-reference meta-prose in Remark — NestedLinkWitness

**ASN-0086, Remark — NestedLinkWitness**: "...a separating witness between the two classes, reused below wherever an antichain-violating pre-state is needed."

**Problem**: "reused below wherever ... is needed" is a forward-reference annotation, not content about the witness. The witness construction itself (`a'' = inc(a, 1)`, preserving `zeros = 3` and giving `#E ≥ 2`) is the substance; the where-it's-reused clause is accretion that rots as the consuming sites change. The downstream sites (WP Case 1 load-bearingness, WP Case 2 "discipline alone insufficient") already cite the Remark by name.

**Required**: End the Remark at "a separating witness between the two classes." Drop the "reused below wherever" clause.

### Issue 5: Duplicated scope prose in the Weakest-Precondition Analysis

**ASN-0086, WP Case 2, "Domain restriction" vs. "Scope of the result"**: The "Domain restriction" paragraph asserts the wp holds only over states that are (i) substrate-conforming and (ii) unit-depth-disciplined, with both load-bearing; the closing "Scope of the result" paragraph then states the wp "relies on the unit-depth retraction discipline ... and the Nullify-as-sole-`R`-producer rule," and that "A direct K.λ caller voids both disciplines, so the result does not extend to such callers."

**Problem**: Two paragraphs in the same subsection say the same thing in different words — the result depends on the two disciplines, and direct K.λ callers escape. The Nullify-as-sole-`R`-producer point is *also* already made in the third-conjunct discussion ("The Nullify-as-sole-`R`-producer rule satisfies the first disjunct..."). This is the "two paragraphs say the same thing" pattern compounding with a use-site recap.

**Required**: Fold "Scope of the result" into "Domain restriction" (or delete it), keeping one statement of the domain restriction and the direct-K.λ-caller escape.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity model for Emit vs. Observe and the consistency model for `A_K` transitions
**Why out of scope**: The note's `→` is the sequential atomic transition relation inherited from ASN-0093's SequentialAtomicTransitions axiom; a concurrency/consistency model is genuinely new territory, correctly listed in Open Questions rather than treated here.

### Topic 2: Higher-arity typed relations `L_K^{(n)}` and multi-arity link projections
**Why out of scope**: The note restricts to standard-triple links (`|Σ.L(a)| = 3`) and says so explicitly; the n-ary generalization is a distinct construction, appropriately deferred.

VERDICT: REVISE
