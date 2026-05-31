# Review of ASN-0086

## REVISE

### Issue 1: "Computable from Σ.L alone" asserted without the finiteness argument the note demands elsewhere
**ASN-0086, Definition — ActiveSubset**: "`A_K^Σ` is computable from `Σ.L` alone: `L_K^Σ` is a slice of `Σ.L`, and `nullified(Σ)` is fixed by `L_R^Σ`, itself a slice of `Σ.L`."
**Problem**: `nullified(Σ)` is defined by `a ∈ coverage(G')`, and `coverage(G')` is in general infinite (the note itself stresses, in Observe_K's decidability remark, that a single prefix span covers an entire subtree). "Fixed by `L_R^Σ`" establishes *determination*, not *computability*. The note supplies the finite-intersection / per-address-decidability argument for Observe_K but never for `nullified`, despite the parallel structure. This is exactly the rigor the note holds itself to one section earlier.
**Required**: Either weaken the word "computable" to "determined" here, or supply the argument: `A_rel^Σ` is finite (L-fin), `L_R^Σ` is finite (L-fin), and `a ∈ coverage(G')` is decidable per address by T2 over the finitely many spans of `G'`; hence `nullified(Σ) = {a ∈ A_rel^Σ : …}` is a finite, computable set.

### Issue 2: R0 "Content-uniformity remark" is a use-site/discharge inventory, not argument
**ASN-0086, R0 proof, *Content-uniformity remark***: "every other L-invariant discharges on the emitter address `a` alone (L0/L1/L1a/L1b/L1c on `a`'s tumbler structure, L2 on `home(a)`, L11a on `a`'s freshness, L12/L12a/L12b/L-fin as K.λ frame consequences, L5/L6 as construction-time tuple properties, L8/L13 structurally, L14/L14a by SC-NEQ exclusion of `a`)."
**Problem**: The preceding paragraph already states the K.λ-step "preserves the full L/S/M/C invariant catalog … by its own contract." Re-enumerating which invariant discharges by which route adds no inferential step — it is a downstream-consumer inventory of the kind the anti-bloat classifier names. The genuinely content-dependent obligation (L3) and the fresh-key obligation (L14/L14a via FreshLinkKeyDisjointness) are the only items that warrant naming.
**Required**: Cut the parenthetical inventory; retain only the statement that K.λ's contract discharges the catalog, plus the L3 content-shape obligation and the L14/L14a fresh-key discharge.

### Issue 3: Forward-reference accretion — repeated deferrals to the Worked Sketch and to R6c
**ASN-0086, R5 / R6b / Nullify**: "(The Worked Sketch below, Step 1, instantiates R5 …)"; "Restoration must proceed by fresh emission at a distinct address (Worked Sketch Step 2; R6c formalizes it)."
**Problem**: Multiple lemmas in different sections point forward to the same downstream illustration (Worked Sketch) and to R6c. The Worked Sketch already labels which R-claims it witnesses at each step; the upstream pointers are redundant advertising of a later section and match the flagged pattern "multiple paragraphs … defer to the same downstream location."
**Required**: Remove the forward pointers from R5, R6b, and the Nullify definition; let the Worked Sketch carry the cross-references in one direction only.

### Issue 4: R0a Case 2 carries a second, equivalent proof of the same conclusion
**ASN-0086, R0a proof, Case 2**: "(Equivalent argument via T10a.2: same-home chain elements are siblings … T10a.2 … then forces prefix-incomparability …)"
**Problem**: Case 2's primary argument (ChainMembershipForOrigin + (UL) + T3) already establishes `a ≼ a' ⟹ a = a'`. The parenthetical re-derives the identical conclusion by a second route. This is the "two paragraphs say the same thing in different words" pattern; nothing in the downstream development selects between the two routes.
**Required**: Keep one derivation; delete the parenthetical (or demote it to a one-clause "equivalently, by T10a.2" without re-spelling the argument).

### Issue 5: Notation-rationale and `↝`-rationale prose in structural slots
**ASN-0086, Emit_K Definition / `↝` definition**: "(Equivalently: writing the family as a single operation … The subscripted form is used throughout this note for parallelism with `L_K`, `A_K`, and `Observe_K`.)"; "R7a quantifies over `↝` so its claim is categorical across the class of substrate-conforming layers."
**Problem**: These are justifications of notation and of why a construct exists, not statements of what the construct is or does — meta-prose the classifier flags ("new prose … explains why … rather than what it says"). The `↝` relation is consumed by exactly one lemma (R7a); the parallelism rationale for the subscript adds nothing to Emit_K's meaning.
**Required**: State Emit_K's signature and effect without the parallelism justification; introduce `↝` with its definition only, letting R7a's quantifier speak for itself.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity of Emit vs. Observe, Observe result ordering, retraction cardinality bounds, dynamic type collision
**Why out of scope**: These are already correctly parked in the Open Questions list and concern a consistency model and observation semantics not yet defined — new territory, not defects in the present substrate-level relational layer.

### Topic 2: Tightening L1b (`#E ≥ 2` → `#E = 2`) at the source
**Why out of scope**: R0a-Cor2 establishes `#E = 2` for this note's link addresses; whether the foundation invariant L1b should itself be narrowed is a change to ASN-0043/ASN-0093, not to this ASN.

VERDICT: REVISE
