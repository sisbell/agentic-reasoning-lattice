# Review of ASN-0047

## REVISE

### Issue 1: SC-NEQ mislabeled "axiom, introduced here" — contradicts the ASN's own inherited table and the foundation

**ASN-0047, Notation (V-position projections)**: "In this ASN the two subspaces are `s_C` (content/text) and `s_L` (link), with `s_C ≠ s_L` (SC-NEQ axiom, introduced here)."

**Problem**: SC-NEQ is not introduced here. ASN-0093's `FixedSubspaceIdentifiers` axiom states `s_C = 1 ∧ s_L = 2` and explicitly names `s_C ≠ s_L` (abbreviated SC-NEQ) as an *immediate consequence*. ASN-0047's own *Inherited from foundation* table agrees, listing `SubspaceConventionAxiom ... consequence SC-NEQ` with source `ASN-0093 (FixedSubspaceIdentifiers)`. The Notation paragraph therefore relabels a foundation consequence as a locally introduced axiom, contradicting both the foundation and a later section of this same ASN. This is the foundation-reinvention pattern: the ASN should cite ASN-0093's axiom, not re-baptize its consequence.

**Required**: Change the parenthetical to attribute SC-NEQ as a consequence of ASN-0093's `FixedSubspaceIdentifiers` (matching the inherited table), and drop "introduced here."

### Issue 2: K.μ~ admissibility clause (i) omits S8★, yet the discharge prose claims (i) stipulates it

**ASN-0047, Decomposition of K.μ~ (admissibility) vs. Class (a) discharge**: Admissibility clause (i) reads "the induced post-state M'(d) would satisfy the arrangement-*shape* invariant package on M'(d) — S8a, S8-depth, S8-fin, D-CTG★, D-MIN★, from which the derived D-SEQ★ follows." But the Class (a) discharge prose states "The shape invariants — S8a, S8-depth, **S8★**, D-CTG★, D-MIN★, D-SEQ★ — share one K.μ~ discharge ... each is stipulated on M'(d) by K.μ~ admissibility (i)."

**Problem**: S8★ is in the discharge prose's "shape invariants" list and is asserted to be "stipulated ... by admissibility (i)," but clause (i)'s enumerated package does not contain S8★. Either S8★ is part of clause (i) (then clause (i) must list it) or it is discharged only by the decomposition mechanics (then the prose must not claim it is stipulated by (i)). As written the two passages disagree about whether S8★ is an admissibility precondition.

**Required**: Make the two consistent — either add S8★ to clause (i)'s package, or correct the discharge prose to state that S8★ is established via the K.μ⁻+K.μ⁺ decomposition (ASN-0036's S8 on the rebuilt projection), not stipulated by admissibility (i).

### Issue 3: ValidComposite★ stated three times — skeleton with ordering meta-prose, full statement, and a third restatement

**ASN-0047, "ValidComposite★ (skeleton, stated at first need)", "ValidComposite★ (ValidComposite, amended)", and the following paragraph**: The skeleton opens "Several statements in this section appeal to the validity of a composite transition before its full definition is reached. We fix the skeleton here, once, and refer to it locally thereafter ... full statement in *Scoped coupling constraints* below." Its clauses (1)/(2) are then restated almost verbatim in the full ValidComposite★ definition, after which a further paragraph restates them again: "ValidComposite★ is the sole definition of validity for the extended state: it enumerates the elementary transition set ... and imposes the coupling constraints J0 together with the content-subspace provenance couplings J1★ and J1'★."

**Problem**: This is forward-reference accretion of the kind this note's anti-bloat mode targets — prose that justifies document ordering ("We fix the skeleton here, once," "full statement in ... below," "the full ValidComposite★ paragraph also records ...") plus two-to-three paragraphs that say the same two clauses in different words. The two-clause content (step preconditions at intermediate states; J0/J1★/J1'★ at the boundary) is the load-bearing definition; the ordering apologia and the third "sole definition" restatement do not advance the argument.

**Required**: Keep one statement of ValidComposite★ (the full one). Replace the skeleton with a single forward pointer or move the full definition earlier so the skeleton is unnecessary; delete the "sole definition of validity" restatement, retaining at most a one-line note that K.λ and K.μ⁺_L are included in the transition set.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link/content contraction (DELETEVSPAN compaction)

The ASN's K.μ⁻ contracts only by per-subspace suffix removal, and the final Open Question already records that interior withdrawal with V-position compaction is unmodeled. This is correctly deferred — interior-DELETE renumbering is named-operation territory (DELETEVSPAN) and belongs to a future operations ASN, not a defect in this transition model.

VERDICT: REVISE
