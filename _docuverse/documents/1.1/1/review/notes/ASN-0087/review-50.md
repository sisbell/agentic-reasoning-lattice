# Review of ASN-0087

The mathematics here is sound — I checked the worked example's prefix computations, the `ℓ ∉ ran(Σ_mid.M(d))` derivation, the wp case split, and the invariant tables against the foundations, and found no correctness gap. The findings are about accreted meta-prose, which this note's anti-bloat classifier directs me to surface.

## REVISE

### Issue 1: Defensive rationale wrapped around the StandardAuthoring definition
**ASN-0087, Inputs (Standard authoring)**: "The restriction to substrate-emittable addresses is essential, not a convenience: `coverage(e)` is a union of half-open T1-intervals... each infinite by T0(a)/T0(b)... whereas the stores are finite (C-fin, L-fin). An unrestricted `coverage(e) ⊆ dom(Σ.C) ∪ dom(Σ.L)` (infinite ⊆ finite) would hold for *no* endset containing a span, making the predicate vacuous."
**Problem**: This is rationale explaining *why* the definition intersects with `F`, not what the definition says. It is exactly the "prose around a definition explains why it is needed rather than what it says" pattern. The reader must skip this essay to reach the actual predicate `StandardAuthoring(e, Σ) ≡ coverage(e) ∩ F ⊆ dom(Σ.C) ∪ dom(Σ.L)`.
**Required**: State the predicate and the one-line reason (`coverage` is infinite, stores are finite, so intersect with the emittable set `F`). Drop the multi-clause vacuity argument.

### Issue 2: The `ℓ ∈ F` + freshness ⟹ `ℓ ∉ coverage(eᵢ)` derivation is written three times
**ASN-0087, Inputs / wp "Reduction under standard authoring" / Side Effects**: The same argument — "since `ℓ ∈ F` (LP-Sub) and `ℓ ∉ dom(Σ.C) ∪ dom(Σ.L)`, `ℓ ∈ coverage(eᵢ)` would force `ℓ ∈ coverage(eᵢ) ∩ F ⊆ dom(Σ.C) ∪ dom(Σ.L)`, a contradiction" — appears in *Inputs* (closing sentence), in *Weakest Precondition* (Reduction under standard authoring), and again in *Side Effects* (with the backward Store-Monotonicity★ transfer).
**Problem**: Three near-verbatim re-derivations of one fact. "Two paragraphs in the same document say the same thing in different words."
**Required**: Derive it once (Inputs), then cite it at the two downstream sites. The Side Effects instance adds only the backward-transfer step, which is the sole part worth restating there.

### Issue 3: Essay content justifying the reflexive route in the wp analysis
**ASN-0087, Weakest Precondition (Case 2)**: "For a caller to author an endset covering `ℓ`, the address must be known before allocation; it is. Although `ℓ` is not a parameter, it is deterministically derivable from `Σ`... This predictability is what makes the reflexive route authorable."
**Problem**: The operative claim is that `ℓ` is derivable from `Σ` via `A_L(d)`'s emission rule, which establishes the reflexive disjunct is reachable. The surrounding sentences ("must be known before allocation; it is", "This predictability is what makes...") restate that point twice without advancing it.
**Required**: Keep the single sentence stating `ℓ` is state-derivable (hence the reflexive disjunct is non-vacuous); remove the motivational restatements.

## OUT_OF_SCOPE

### Topic 1: Well-formedness of endsets referencing not-yet-allocated addresses
**Why out of scope**: The first Open Question (constraints beyond `e₃ ≠ ∅` for forward-reaching spans) is genuine new territory; L4 (ASN-0043) already permits such spans, and tightening them belongs to a future authoring-discipline ASN, not to this operation's definition.

VERDICT: REVISE
