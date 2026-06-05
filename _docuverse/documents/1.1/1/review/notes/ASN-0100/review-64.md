# Review of ASN-0100

## REVISE

### Issue 1: Post-K.μ⁺ intermediate state mislabeled as Σ'

**ASN-0100, §Atomicity and Canonical Order**: "*After step 3's K.μ⁺ — this intermediate is `Σ'`.*" — followed two bullets later by "*After each of the `n` K.ρ firings of step 4.* ... The final K.ρ intermediate *is* the composite boundary `Σ'`."

**Problem**: Both statements cannot hold. The decomposition is `n` K.α + (optional K.μ⁻) + K.μ⁺ + `n` K.ρ. After step 3's K.μ⁺ the provenance component `R` has not yet been extended by the step-4 K.ρ firings, so the post-K.μ⁺ state differs from Σ' in its `R` component. What is true is the weaker claim the bullet actually needs: the *arrangement* at the post-K.μ⁺ intermediate equals the final `M'(d)` (since K.ρ frames M), so the arrangement-invariant checks of §Verifying the Invariants transfer. Labeling the state itself "Σ'" is wrong and is directly contradicted by the later "final K.ρ intermediate *is* Σ'."

**Required**: Replace "this intermediate is `Σ'`" with a precise statement — e.g., "the arrangement at this intermediate equals the final `M'(d)` because K.ρ frames M" — and keep the single correct identification of Σ' with the final K.ρ intermediate.

### Issue 2: §Formal Contract tail duplicates the atomicity/uniqueness content of §Atomicity

**ASN-0100, §The Operation: Formal Contract**: "**Composite atomicity.** The post-state Σ' is uniquely determined by this contract, though the substrate decomposition that realises it is not." — together with the preceding sentence assigning the Class (a) per-state / Class (b) boundary split.

**Problem**: §Atomicity restates both in different words — "The post-state Σ' is *uniquely determined* by the operation contract; the substrate decomposition that realises it is not" and "per-state invariants (Class (a) ...) hold at *every* state ...; composite-boundary properties (Class (b) ...) ... hold at the boundary." The §Formal Contract versions are bare assertions; the actual derivation (component-by-component uniqueness, per-intermediate verification) lives only in §Atomicity. This is the "two paragraphs say the same thing in different words" accretion pattern: the reader meets the claim asserted, then meets it again proven, with the first copy carrying no reasoning the second lacks.

**Required**: Drop the bold "Composite atomicity" assertion and the Class (a)/(b) sentence from §Formal Contract (or reduce to a one-line pointer to §Atomicity); state and prove once, in §Atomicity.

### Issue 3: INS.frame.dom is a redundant claim of INS.frame.E

**ASN-0100, Claims Introduced table**: "INS.frame.E | E' = E ... specialises to dom(M') = dom(M) for documents" and separately "INS.frame.dom | dom(M') = dom(M): no new documents registered".

**Problem**: INS.frame.E already states the specialization to `dom(M') = dom(M)`, and the Frame Conditions prose says so explicitly ("As a specialisation of `E' = E` for the document subset"). A separate INS.frame.dom claim adds no content — it is the same proposition under a second label, which the index then carries as if it were an independent guarantee.

**Required**: Remove INS.frame.dom, or fold it into INS.frame.E as the noted specialization rather than a distinct claim.

## OUT_OF_SCOPE

None. The note correctly bounds itself to content-subspace INSERT and defers DELETE, COPY, REARRANGE, link semantics, versions, and replication to other notes.

VERDICT: REVISE
