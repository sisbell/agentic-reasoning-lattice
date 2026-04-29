# Review of ASN-0082

## REVISE

### Issue 1: I3-S(a) derivation has two unjustified steps
**ASN-0082, Span Width Preservation, Derivation of (a)**: "Applying TA-assoc in reverse: s ⊕ (ℓ ⊕ δₙ) = (s ⊕ ℓ) ⊕ δₙ = reach(σ) ⊕ δₙ = shift(reach(σ), n)."
**Problem**: Two gaps in the chain.

First, the reverse TA-assoc application (a=s, b=ℓ, c=δₙ) is a different operand assignment from the forward application (a=s, b=δₙ, c=ℓ). The forward preconditions are verified — "m ≤ #s = m, m ≤ #δₙ = m" — but the reverse application's preconditions (actionPoint(ℓ) ≤ #s and actionPoint(δₙ) ≤ #ℓ) are not verified. They are trivially m ≤ m in both cases, but each TA-assoc application has distinct operand roles and should have its preconditions stated.

Second, the final step "reach(σ) ⊕ δₙ = shift(reach(σ), n)" requires δₙ = δ(n, #reach(σ)), which holds only when #reach(σ) = m. This follows from TumblerAdd's result-length identity: #reach(σ) = #(s ⊕ ℓ) = #ℓ = m — or equivalently from S6 (LevelConstraint, ASN-0053). Neither is cited.

**Required**: (a) State the reverse TA-assoc preconditions explicitly. (b) Justify #reach(σ) = m at the final step, citing TumblerAdd's result-length identity or S6.

### Issue 2: S6 (LevelConstraint) missing from statement registry
**ASN-0082, Statement Registry**
**Problem**: The derivation of I3-S(a) depends on #reach(σ) = #s for level-uniform spans — exactly S6 (LevelConstraint, ASN-0053). S6 is neither cited in the derivation text nor listed in the registry. All other ASN-0053 properties used (SpanReach, D2) are registered.
**Required**: Add S6 to the registry as a cited lemma from ASN-0053.

### Issue 3: Well-formedness of σ' as a span not verified
**ASN-0082, Span Width Preservation**: "Define the shifted span σ' = (shift(s, n), ℓ)."
**Problem**: σ' is used as a span — reach(σ') is computed, D2 is applied to it — but T12 (SpanWellDefinedness) is never verified for σ'. T12 requires ℓ > 0 (inherited from σ) and actionPoint(ℓ) ≤ #shift(s, n). The latter is m ≤ m by the result-length identity of TumblerAdd and the precondition actionPoint(ℓ) = m, but this should be stated before treating σ' as a span.
**Required**: Verify T12 for σ' before computing its properties.

### Issue 4: "Ordinal-level" span definition not registered
**ASN-0082, Span Width Preservation**: "We call a span *ordinal-level* when its width acts purely at the deepest component: actionPoint(ℓ) = m."
**Problem**: This is a new definition that gates the precondition of I3-S, but it does not appear in the statement registry. Every other local definition (M(d), subspace(v)) is registered.
**Required**: Add "ordinal-level span" to the registry as a local definition.

## OUT_OF_SCOPE

### Topic 1: Spans straddling the insertion point
I3-S covers spans entirely within the shifted region (s ≥ p). A span starting before p and reaching past p is split by the insertion: its left portion is unchanged (I3-L) and its right portion shifts (I3). The point-level guarantees handle this, but a span-level property expressing how a straddling span decomposes into a preserved left span and a shifted right span — and that their union covers the original content — is a natural extension.
**Why out of scope**: I3-S explicitly restricts to s ≥ p. The straddling case is new territory requiring S4 (SplitPartition) composed with I3-S.

### Topic 2: Span classification preservation under shift
If two spans α, β in the shifted region have a certain SC relationship (separated, adjacent, overlapping), does shifting both by δₙ preserve that relationship? This follows from I3-S(a) and TS1 but is not derived.
**Why out of scope**: This is a consequence of I3-S, not an error in it. Belongs in a future ASN about span-set operations under insertion.

VERDICT: REVISE
