# Review of ASN-0086

## REVISE

### Issue 1: R5-Cor proof mislabels L14 and cites wrong preservation mechanism
**ASN-0086, R5-Cor proof body, L14/L14a discharge block**: "at pre-existing keys, L14 (no (d, v) ∈ dom(Σ.M) mapping into dom(Σ.L)) and L14a (no transcluded link address) are preserved by K.λ's Frame on Σ.M"
**Problem**: The parenthetical for L14 states L14a's content (NonTranscludability, ASN-0043), not L14's. L14 (DualPrimitive, ASN-0043) is `dom(Σ.L) ∩ dom(Σ.C) = ∅` — address-set disjointness over the s_C-resident slice, not arrangement-mapping. The cited mechanism (K.λ's Frame on Σ.M) is correct for L14a but irrelevant for L14, whose preservation at existing keys uses K.λ's Frame on Σ.C combined with L12 on Σ.L. R0's own L14 verification ("Splitting on the K.λ Frame: (i) `dom(Σ.L) ∩ dom(Σ.C)|_{s_C} = ∅`, which is L14 at Σ ...; (ii) `{a} ∩ dom(Σ.C)|_{s_C} = ∅` ...") shows the correct structure that R5-Cor abstracts from but loses fidelity to.
**Required**: Replace the L14 parenthetical with L14's actual statement and split the mechanism citation — L14 by Σ.C-frame + L12, L14a by Σ.M-frame + SC-NEQ on the new key.

### Issue 2: Worked Sketch Step 3 reverses prefix direction in notation
**ASN-0086, Worked Sketch Step 3, nullified(Σ_3) computation**: "a₂: neither retraction tuple's to-coverage contains a₂ (a₂ ⊀ b₁ via R0a; a₂ ⊀ a₁ via R0a)" and analogously for b₂.
**Problem**: For `a_2 ∈ coverage({(a_1, δ(1, 8))}) = {t : a_1 ≼ t}`, the relevant test is whether `a_1` is a prefix of `a_2`. The proof writes "a₂ ⊀ a₁" — which per ASN-0034's Prefix definition unfolds to `¬(a_2 ≼ a_1)` — but the relevant negation is `¬(a_1 ≼ a_2)`, i.e., `a_1 ⋠ a_2`. R0a's antichain excludes both directions for distinct link addresses, so the substantive conclusion (a_2 ∉ coverage) is correct, but the notation invites confusion about which direction R0a is being applied to.
**Required**: Flip the direction in the parentheticals — "a_1 ⋠ a_2" and "b_1 ⋠ a_2" for a_2's case; "a_1 ⋠ b_2" and "b_1 ⋠ b_2" for b_2's case.

## OUT_OF_SCOPE

### Topic 1: Concrete exercise of crafted-span and self-nullifying retraction regimes
The wp Case 2 analysis discusses regimes (ii) (crafted-span retractions outside the unit-depth discipline) and (iii) (self-nullifying R-typed emission) but neither is exercised concretely. The Worked Sketch instead exercises R6b's retraction-of-retractor — substantively more important for the active/audit distinction. **Why out of scope**: Concrete coverage of regimes (ii)/(iii) belongs in a future ASN exploring the substrate vs. layer-discipline boundary on retraction-tuple shape constraints.

### Topic 2: Multi-arity active subsets
The ASN scopes `L_K^Σ` and `A_K^Σ` to standard-triple links; higher-arity links (|Σ.L(a)| > 3) exist in `dom(Σ.L)` but are outside the typed-relation machinery. **Why out of scope**: Listed in Open Questions as future work on `A_K^{(n),Σ}`.

### Topic 3: Predicate interaction between L_K and Σ.M visibility
What invariants must hold between `L_K` and arrangements `Σ.M` when relational predicates depend on whether endset content is currently visible in some document? **Why out of scope**: Listed in Open Questions; cross-layer coupling between typed relations and arrangements is genuinely new territory.

VERDICT: REVISE
