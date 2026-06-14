# Review of ASN-0131

This is a strong, substantively rigorous note. I checked the load-bearing arguments and they hold:

- The `e₃`/`θ` content-disjointness argument (worked instance) is sound: `θ ≼ c` carries θ's three separator zeros onto `c`, and `zeros(c)=3` forces those to *be* c's separators, fixing `E(c)₁ = E(θ)₁ = s_type ≠ s_C`. The identical argument for the retraction to-set (`ℓ` element-level, `E(ℓ)₁ = s_L`) is likewise correct, and the note correctly restricts it to **unit-depth** spans and refuses to extend it to wide `Θ` spans.
- The worked instance is internally consistent (`a₄ = shift(a₂,2)` is the exclusive upper bound of the width-2 span via TS3/TS5, so `{a₂,a₃} ⊆ coverage(e₁)` but `a₄ ∉`), and it genuinely exercises RE-OVL, RE-CLIP, RE-WHOLE, RE-UNIT.
- RE-CWP's weakest precondition checks out, including the `R = ∅` collapse to `RE = ∅` and the factoring of "no pair dropped" into `coverage(e) ∩ Δ ≠ ∅ ⟹ coverage(e) ∩ I_R ≠ ∅`.
- The RE-RET iff (forward: sole addressable bearer ⟹ drop; backward: other bearer survives via R-Scope + antichain) is correct under its stated hypothesis, and the hypothesis is honestly flagged and routed to OQ6.
- Stability coverage of the ASN-0047 vocabulary is exhaustive (all eight transition kinds + the ASN-0082 shift-based insert/delete are addressed), and the foundation citations are all to foundation ASNs — no cross-ASN violations, no reinvented notation.

The remaining items are prose/structure, not correctness.

## REVISE

### Issue 1: The retraction-type symbol `Θ` is used before it is introduced, and is reintroduced inconsistently as `R`

**ASN-0131, "Stability" — "Under link emission" and "Under retraction"**: The "Under link emission" paragraph writes "a *non-retraction* emission (one not `Θ`-typed, ASN-0086's `K ≁ R`)", but `Θ` is not defined until the *later* "Under retraction" paragraph ("writing `Θ` for ASN-0086's designated retraction type, kept distinct from the retention set `R` of the contraction analysis above").

**Problem**: Three compounding snags in one stretch of prose. (a) `Θ` (capital) is used before its definition. (b) The definition exists precisely to keep ASN-0086's retraction type distinct from the retention set `R` — yet the *same* sentence that uses it cites "ASN-0086's `K ≁ R`," reusing `R` for the retraction type and defeating the disambiguation the note went out of its way to introduce. Within the stability section the reader has just seen `R` = retention set (RE-CWP) and now sees `R` = retraction type. (c) The capital `Θ` is glyph-adjacent to the worked instance's lowercase `θ` (a classifying *type address* — a different object), inviting conflation since both are "types."

**Required**: Introduce `Θ` at its first use (move the "writing `Θ` for ASN-0086's designated retraction type…" clause up to the link-emission paragraph, or define it once before either). Replace "ASN-0086's `K ≁ R`" with the note's own `Θ` (e.g., "non-retraction-typed (`K ≁ Θ` in this note's renaming)") so the `R`/`Θ` convention is honored throughout. Confirm the `θ`/`Θ` distinction is intended and survives the glyph collision.

### Issue 2: The computability paragraph forward-references `addressable(Σ)` and "the answer" before they are defined

**ASN-0131, "When does an endset touch the region?"**: "The touch test is decidable, so the operation is a realisable query and not merely a defined set. The touch test and the addressability filter are decidable over finite sets: … `nullified(Σ)` is a computable set … so membership in `addressable(Σ) = dom(Σ.L) ∖ nullified(Σ)` is settled … Hence the answer is a finite, computable object."

**Problem**: This paragraph sits in the section that *defines* `touch_W`, but it reasons about the **addressability filter**, inline-defines `addressable(Σ) = dom(Σ.L) ∖ nullified(Σ)`, and concludes about "the answer" — all three of which belong to the next section ("The unit of the answer"), where `addressable` and RE-DEF are actually introduced. The reader meets the addressability machinery and a computability conclusion about RE before either the filter or RE itself has been stated. The touch-decidability content is correctly placed; the addressability/whole-answer computability content is premature.

**Required**: Restrict this paragraph to touch-test decidability (its proper slot), and move the addressability-decidability and "finite, computable object" conclusion to after RE-DEF, where `addressable(Σ)` and the answer are in scope.

## OUT_OF_SCOPE

The Open Questions (OQ1 whole-endset vs touching-spans; OQ2 multiplicity; OQ3 rendered/V-position answer; OQ4 intersection-distributivity; OQ5 non-co-resident link store; OQ6 type-slot match against content; OQ7 link-subspace region) are correctly scoped as future territory rather than gaps in this note — in particular OQ4 is genuinely open (the union half is proven as RE-UDIST; intersection fails because the forward image does not distribute over intersection under the non-injective arrangement), and the `W ⊆ s_C` content-subspace restriction is a deliberate scoping consistent with the title, not an evasion. No additions needed.

VERDICT: REVISE
