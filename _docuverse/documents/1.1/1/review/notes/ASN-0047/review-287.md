# Review of ASN-0047

This is a large, heavily-revised ASN whose core rigor — the per-state/composite-boundary invariant partition, the K.μ~ admissibility decomposition, the worked-example arithmetic — holds up under checking. The findings below are scoped to the `review-mode.anti-bloat` directive: accreted meta-prose and intra-document redundancy, not correctness gaps in the proofs. I did not find a load-bearing proof gap, and I am not raising scope/sprawl (per the declined findings).

## REVISE

### Issue 1: S8★ definition enumerates its downstream consumers
**ASN-0047, S8★ definition (link-subspace route)**: "This weakening is harmless because nothing downstream consumes link-run maximality — the link subspace is read only through CL-OWN, CL-UNIQ, and LRP, all of which depend on the per-position map `M(d)|_{dom_L}`, never on its run structure."
**Problem**: This is exactly the flagged use-site-inventory pattern — a definition justifying its own shape by naming the downstream sites that consume (or don't consume) it. The inventory rots: if a later ASN reads the link subspace through a fourth consumer, this sentence becomes a false claim embedded in a foundation definition. The substantive content is already carried by the preceding sentence ("S8★(s_L) asserts the existence of *a* run-partition... not the canonical maximal-run partition").
**Required**: Delete the "nothing downstream consumes... read only through CL-OWN, CL-UNIQ, and LRP" inventory. The non-canonicity of the link-subspace decomposition is a property of S8★ itself; it does not need to be defended by listing readers.

### Issue 2: "Modeling choice (layer separation)" restates one claim three times
**ASN-0047, D-CTG★/D-MIN★, *Modeling choice (layer separation)***: "D-CTG★/D-MIN★ constrain the *arrangement* layer `M(d)`... never `dom(L)`... The strengthening is admissible because link permanence is discharged independently on `dom(L)` by L12... an I-space fact, not an arrangement-layer obligation to hold a positional gap. D-CTG★/D-MIN★, acting only on `M(d)`, thus do not contradict tombstoning."
**Problem**: The single load-bearing point — "D-CTG★ acts on `M(d)`; link permanence is discharged separately on `dom(L)` by L12, so the strengthening does not contradict tombstoning" — is asserted three times ("constrain M(d)... never dom(L)" / "an I-space fact, not an arrangement-layer obligation" / "acting only on M(d)"). The Nelson LM 4/9 I-space elaboration is defensive padding around a one-sentence consistency note.
**Required**: Reduce to a single sentence stating the layer separation and the L12 discharge. Drop the repeated re-phrasings.

### Issue 3: Cross-document disjointness machinery restated across five sites
**ASN-0047, CrossDocDisjoint lemma; SubAllocatorBundle.Disjointness; S4 verification; *Entity distinctness*; *Link distinctness***: The chain T10a.{2,5} → T10 (non-nesting prefixes ⟹ partition independence) is re-narrated at each site — once as the CrossDocDisjoint lemma proper, then re-invoked in prose at SubAllocatorBundle.Disjointness, the S4 cell, "Entity distinctness," and "Link distinctness."
**Problem**: This is the "two paragraphs say the same thing in different words" pattern. CrossDocDisjoint is stated as a named lemma precisely so it can be cited; the later sites should cite it at the relevant anchor pair rather than re-deriving the T10a→T10 reasoning. The CrossNodeAccountBase sub-argument is genuinely new (node-nesting case) and should stay, but the surrounding restatements of the base lemma are redundant.
**Required**: Have "Entity distinctness," "Link distinctness," and the S4 cell cite CrossDocDisjoint at their anchor pairs in one clause each, deleting the re-narrated T10a.{2,5} → T10 chains. Keep only CrossNodeAccountBase's novel content.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link withdrawal
The ASN's K.μ⁻ contracts the link subspace by suffix removal only; the implementation's interior `DELETEVSPAN` compacts-and-renumbers. The ASN itself flags this as an open question. This is future-ASN territory (a new contraction operation), not a defect in the present suffix-only model.

### Topic 2: Forked-document arrangement/source invariant precision
J4 bounds `ran(M'(d_new)) ⊆ ran(M(d_op)|_{V_{s_C}(d_op)})` (subset, not identity). The precise invariant relating a fork's initial arrangement to its source's *current* arrangement is left open and belongs in a future ASN on version-derivation correspondence.

### Topic 3: Concurrent allocation under a shared home document
Serialization vs. coordination-free distinct-address guarantees for concurrent K.λ/K.α on one document is an open question; concurrency is explicitly out of scope here.

VERDICT: REVISE
