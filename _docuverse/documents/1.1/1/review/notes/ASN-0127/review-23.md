# Review of ASN-0127

The core algebra is sound this round: F-IMG/F-IMG-MONO/F-IMG-CONTR are correct, the F-IMG-SWING reindexing formula checks out, F-UDIST/F-IMONO/F-VDIST are properly derived, F-FULL correctly closes the loop to LP12, F-CIL/F-LAMBDA and the E-lane results are airtight, D-CWP's bridge and biconditional are right (I verified `A = A ∪ B ⟺ B ⊆ A` and the `R = ∅` boundary), and the worked illustration's computations all verify, including the prefix-incomparability discharge for `a_θ`. Four residual items remain — one rigor gap in F-IMG-SWING's witnesses, one precision error in D-CWP's gloss, and two noise items of the kind the anti-bloat classifier targets.

## REVISE

### Issue 1: F-IMG-SWING's realizability witnesses are never discharged as admissible K.μ~ instances
**ASN-0127, F-IMG-SWING**: "the forward image of a fixed sub-region `W` may change membership; and when `Σ.M(d)` is non-injective — content sharing (M13/M14, ASN-0058) — the image may additionally gain or lose members (change cardinality)" — supported by "*Injective witness:* … the transposition reorder `π = (v₁ v₂)` …", the gain witness `π(v₁) = v₁, π(v₂) = v₃, π(v₃) = v₂`, the loss witness, and the four-position witness.
**Problem**: These "may" clauses are realizability claims, so each witness must be a *valid* K.μ~ step. K.μ~ admissibility (ASN-0047) requires (i) post-state shape invariants, (iii) length preservation, (iv) subspace preservation, (v) link-subspace fixity, plus the precondition that `M(d)|_{dom_C}` takes at least two distinct values. None of this is discharged for the four schematic witnesses — they are called "reorders" by fiat, over positions `v₁ … v₄` of unspecified depth and subspace. The Worked illustration discharges admissibility only for its own transposition, and its swings keep the *image* cardinality fixed (the arrangement there is injective), so the gain and loss witnesses — the sole support in the entire note for the image-cardinality-change claim and for the availability taxonomy's "containment motion" branch, which D-NONMONO's reorder clause then consumes — are validated nowhere.
**Required**: One discharge sentence in F-IMG-SWING: pin the witness positions to canonical same-subspace, same-depth forms (e.g., `[1,1] … [1,4]`, available under D-SEQ★), then observe that any permutation of same-depth content-subspace positions satisfies (iii)/(iv) automatically and (v) vacuously, K.μ~-FIX keeps the domain fixed so the shape invariants (i) persist, each witness's value multiset exhibits ≥ 2 distinct values, and each `π` has non-trivial net effect (ii).

### Issue 2: D-CWP states its pre-state-evaluability point twice
**ASN-0127, D-CWP**: statement — "Both `I_R = …` and `Δ = …` are functions of the pre-state `Σ` and the retention set `R` alone — the bridge eliminates every post-state quantity — so the biconditional is a genuine precondition on `(Σ, R)`, evaluable before the step." Derivation tail — "…the discovery analog, on the contraction side, of ASN-0098's LP12a (ContractionDiscoverabilityWP), and like LP12a it is stated purely over the pre-state `Σ` and the retention set `R`."
**Problem**: The closing clause repeats, in different words, the point already made in the statement. This is the same-thing-twice accretion pattern; the tail's only new content is the LP12a analogy.
**Required**: End the derivation at "…LP12a (ContractionDiscoverabilityWP)." and delete "and like LP12a it is stated purely over the pre-state Σ and the retention set R."

### Issue 3: D-CWP's prose gloss and table row understate the region restriction on the retained side
**ASN-0127, D-CWP and Properties table**: "— i.e. iff every link reaching a dropped I-address also reaches a retained one"; table row: "K.μ⁻ stability iff every dropped-region link also reaches a retained I-address".
**Problem**: "A retained I-address" is ambiguous between `I_R = {Σ.M(d_q)(v) : v ∈ W ∩ R}` (correct) and the image of all of `R` (wrong). The loose reading gives wrong stability verdicts: with `v₁, v₂, v₃ ↦ a₁, a₂, a₃`, `W = {v₂, v₃}`, `R = {v₁, v₂}`, a link reaching `a₃` and `a₁` does reach a retained address (`a₁`, via `v₁ ∈ R`) — yet `I_R = {a₂}`, the link is in `findlinks(Δ, Σ)` but not in `findlinks(I_R, Σ)`, and it correctly drops out of `findlinks_disc(W, d_q, Σ')` since `image(W, d_q, Σ') = {a₂}`. The formal biconditional is exact; the two glosses, read standalone (especially the table row), misstate it.
**Required**: In both places: "also reaches an I-address retained *within the queried region* (`I_R`)".

### Issue 4: F-CIL-perlink is bracketed by two statements of the same classification
**ASN-0127, F-CIL-perlink**: intro — "A weaker per-link form is the residual that F-LAMBDA applies at each prior key"; derivation tail — "This is the per-link tail of F-CIL's chain, begun from per-link value equality rather than the global store equality … F-CIL-perlink is therefore not an instance of F-CIL but the residual per-link reasoning that survives the weaker hypothesis."
**Problem**: The sub-lemma's taxonomy (residual, not an instance of F-CIL) is stated before it and again after it — meta-prose about the lemma's relationship to F-CIL rather than its content, said twice. The one substantive clause in the tail (`dom(Σ'.L) = dom(Σ.L) ∪ {ℓ_new} ≠ dom(Σ.L)` makes F-CIL's global hypothesis fail under K.λ) is worth keeping — once.
**Required**: State the K.λ-failure fact in exactly one place (here or at F-LAMBDA's citation of the sub-lemma); delete the provenance/classification framing ("This is the per-link tail…", "…is therefore not an instance of F-CIL but the residual…").

## OUT_OF_SCOPE

### Topic 1: Behavior of the discovery-anchored query across version forking (J4)
**Why out of scope**: A fork is a composite of K.δ + K.μ⁺ + K.ρ, all individually covered here, but the *characterization* — e.g., that the new version's discovery set initially equals the operand's content-slice matches via the order-preserving bijection φ — is new derivational territory, not an omission in this note.

### Topic 2: Effective computation of `matches` and `findlinks`
**Why out of scope**: Deciding `coverage(eᵢ) ∩ I ≠ ∅` from finite span representations (interval/tumbler comparisons rather than set intersection over infinite `T`) is a decision-procedure result for a future ASN; this note correctly confines itself to the set-level algebra.

VERDICT: REVISE
