# Review of ASN-0082

## REVISE

### Issue 1: D-BJ enumerates downstream consumers of its own conclusion
**ASN-0082, D-BJ (ShiftBijectivity)**: "Since Q₃ is *defined* as the image {σ(v) : v ∈ R}, σ is surjective onto Q₃ by construction, so σ : R → Q₃ is a bijection — we record this once here to license the 'bijection' phrasing used downstream (D-DP, S2-post, D-SEQ-post)."
**Problem**: The clause "we record this once here to license the 'bijection' phrasing used downstream (D-DP, S2-post, D-SEQ-post)" is a use-site inventory — it enumerates which later lemmas consume the bijection rather than advancing D-BJ's argument. This is exactly the forward-reference accretion the anti-bloat pass targets: a lemma narrating its own bookkeeping role across the document.
**Required**: State the surjectivity-by-construction fact plainly ("σ is surjective onto Q₃ by definition; the proof obligations are order-preservation and injectivity") and delete the downstream-consumer list. Downstream lemmas can cite D-BJ without D-BJ pre-announcing them.

### Issue 2: D-CS rationale lists the invariant proofs that "require" it
**ASN-0082, D-CS (CrossSubspaceFrame)**: "The first conjunct establishes domain equality per non-S subspace (no positions added or removed); the second establishes mapping equality (no values changed). Together they give the biconditional that the invariant proofs (D-CTG-post, D-MIN-post, S8-depth-post, S8a-post) require when citing D-CS for 'unchanged' non-S subspaces."
**Problem**: The trailing sentence is a downstream-consumer enumeration ("the invariant proofs (D-CTG-post, D-MIN-post, S8-depth-post, S8a-post) require"). The two conjuncts are already self-explanatory from the formal statement; the inventory of which post-lemmas lean on D-CS adds no content to D-CS and duplicates the dispatch already centralized in the "Off-subspace and off-document dispatch" convention paragraph.
**Required**: Keep the two-conjunct gloss (domain equality + mapping equality); delete the "the invariant proofs (…) require" clause. The dispatch convention paragraph already states that non-S subspaces are discharged uniformly via D-CS.

### Issue 3: Editorial framing of the tombstone-slot example
**ASN-0082, "Cross-subspace insertion into the link subspace"**: "The text-subspace examples above never exercise the surprising consequence of I3 for S ≥ 1: when the link subspace is itself the active (shifted-into) region, a shifted image may land in a slot that was a tombstone (an absent V-position) in the pre-state. We confirm this raises no S2/S3 conflict."
**Problem**: The lead-in editorializes ("the surprising consequence," "the text-subspace examples above never exercise") rather than stating what the example shows. The example itself (a shifted image filling a former tombstone, with the S2/S3 checks) is legitimate and valuable; the framing prose is the meta-layer to trim.
**Required**: Open directly with the setup — e.g., "When S = 2 is the shifted-into region, a shifted image may land in a former tombstone slot; we verify S2 and S3 still hold." Drop "surprising consequence" and the comparison to the prior examples.

## OUT_OF_SCOPE

### Topic 1: Depth > 1 generalization of gap-closure and the TA4 zero-prefix collision
**Why out of scope**: The Open Questions correctly flag that D-SEP/D-DP and the OrdinalExceedsDisplacement round-trip are proved only at #p = 2 (depth-1 ordinals), and that TA4's zero-prefix precondition collides with S8a positivity at intermediate components for deeper ordinals. Resolving this requires a weaker inverse law and belongs in a successor ASN, not a revision here — the #p = 2 restriction is a declared precondition, not a gap in the stated contract.

The technical core is sound: I3/I3-V well-definedness (injectivity via TS2, strict advance via TS4), the three-region contraction partition, D-CTG-post/D-MIN-post/D-SEQ-post closed forms (V_1(d') = {[1,k] : 1 ≤ k ≤ N − c}), and the span-width lemmas I3-S and D-S all check against their worked examples, including the L = ∅, R = ∅, and full-deletion boundaries. The findings above are accreted forward-reference/use-site prose, not proof errors.

VERDICT: REVISE
