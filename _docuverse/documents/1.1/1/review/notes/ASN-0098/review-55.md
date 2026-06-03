# Review of ASN-0098

I checked the projection definition, the immutability lemmas (LP2–LP3★), the frame conditions (LP4–LP8, LP14), the operation-effect lemmas (LP9–LP11), discoverability (LP12, LP12a/b), the substrate machinery (LP-Sub, LP-Fin), tightness (LP19/LP19a), and the worked trace. The core arithmetic is rigorous: the exact-difference formulas in LP9/LP10 are proved both directions, the LP11 biconditional and its reverse inclusion via π⁻¹ are complete, the LP12a wp pullback correctly establishes `project(a,i,d,Σ') = project(a,i,d,Σ) ∩ R` with `R ⊆ dom(Σ.M(d))` argued, and the LP-Fin case split (sub-case A empties, sub-case B contributes exactly `n`) is exhaustive. Boundary cases (empty endset, empty arrangement, `R = ∅`, maximal contraction) are handled. The findings below are notation drift and forward-reference/redundancy accretion consistent with the anti-bloat classifier.

## REVISE

### Issue 1: Invented predicate name for a foundation concept
**ASN-0098, LP8 and Claims-Introduced table**: "K.δ in the IsDocument case (ASN-0047)" / "Document-registration invariance (K.δ-IsDocument of ASN-0047)"
**Problem**: ASN-0047 names the entity predicate `Document(e)` (e.g. `E_doc = {e ∈ E : Document(e)}`, and K.δ's frame clause "`dom(M') = dom(M) ∪ {e}` ... for Document(e)"). "IsDocument" / "K.δ-IsDocument" is a coined synonym for a predicate the foundation already fixes. Per the self-containment standard, an ASN should use the foundation's term rather than reinvent notation.
**Required**: Refer to the `Document(e)` sub-case of K.δ by the foundation's name throughout LP8 and the table.

### Issue 2: Exhaustiveness/use-site inventory paragraph (forward-reference accretion)
**ASN-0098, end of "Operation Effects on Projection"**: "The atomic per-step lemmas LP4–LP10 and LP14 cover every atomic operation kind of the working frame; K.δ's node and account cases have frame `M' = M` and so fall under LP4, while its document case is LP8. ... any multi-step argument is analysed step-by-step, each atomic step governed by one of these lemmas. LP11 is composite-level ..."
**Problem**: This is a coverage inventory — an exhaustiveness claim cataloguing which lemma governs which operation — not a step in any proof. No multi-step projection-displacement lemma actually consumes it (the multi-step results LP2★/LP3★/LP13 are discharged by the closure schema (★), not by this routing table). The frame facts ("`M' = M`") are legitimate, but the "LP4–LP10 and LP14 cover every atomic operation kind ... falls under LP4 ... is LP8" routing is the accretion flagged by the anti-bloat classifier.
**Required**: Either delete the routing inventory, or fold the single load-bearing fact (atomic decomposition via SequentialTransitionAxiom) into wherever a multi-step displacement argument actually needs it.

### Issue 3: Redundant permanence-thesis restatement
**ASN-0098, Immutability section / LP13 / LP17**: the "stored link is permanent; only the projection moves" thesis is asserted at least four times — after LP3 ("the link, the slot, and the I-addresses it reaches are all permanent. What can vary is only which ... are currently arranged"), after Store Monotonicity★ ("These invariants pin down what a link holder owns ... The link is, in this strict sense, a permanent record"), in LP13's closing ("A holder can therefore rely on the stored object permanently"), and after LP18 ("A link can pass through arbitrarily many states of orphanage and resurrection without any modification to its stored data").
**Problem**: Two or more paragraphs saying the same thing in different words. The thesis is already stated once at the head of "The Projection Operation" ("of the two inputs, only the arrangement varies"). The repetitions do not advance reasoning.
**Required**: Keep one statement (LP13's, where it is load-bearing for the discoverability contrast) and remove the duplicative restatements.

### Issue 4: Redundant external citation where an inline derivation is already present
**ASN-0098, LP11**: "The second postcondition `ran(Σ'.M(d)) = ran(Σ.M(d))` is K.μ~-RANGE (range-invariance) of ASN-0047, cited directly."
**Problem**: The proof has already established `Σ'.M(d)(π(v)) = Σ.M(d)(v)` for all `v` with `π` a bijection on the (K.μ~-FIX–fixed) domain. Range-equality is then a one-line consequence (`ran(Σ'.M(d)) = {Σ'.M(d)(π(v)) : v} = {Σ.M(d)(v) : v} = ran(Σ.M(d))`). Reaching for a separately-named foundation postcondition for a fact the local argument already yields is dependency accretion.
**Required**: Derive `ran(Σ'.M(d)) = ran(Σ.M(d))` inline from the bijection equation and drop the external citation.

## OUT_OF_SCOPE

### Topic 1: Reverse discovery, V-order reflection, cross-document operation comparison, link-to-link induced discovery
**Why out of scope**: These are correctly parked in the Open Questions section as future ASNs; the present note deliberately confines itself to forward projection of a fixed endset through a single document's arrangement. No action needed.

### Topic 2: Link-canonical endset contraction (link subspace emptied content retained)
**Why out of scope**: The final Open Question notes the content-canonical disjointness argument (LP12b) does not invert to the link subspace. This is genuinely new territory (LP-Fin Corollary at `X = s_L` does not yield disjointness from the link store), appropriately deferred rather than claimed here.

VERDICT: REVISE
