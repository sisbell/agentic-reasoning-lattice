# Review of ASN-0047

## REVISE

### Issue 1: S3★ is classified inconsistently between the necessity and sufficiency halves of the K.μ~ precondition proof

**ASN-0047, *Decomposition of K.μ~* (admissibility definition + sufficiency construction)**:

The admissibility clauses are defined as: "π is admissible iff (i) the induced post-state M'(d) would satisfy the arrangement-*shape* invariant package on M'(d) — S8a, S8-depth, S8-fin, D-CTG★, D-MIN★, from which the derived D-SEQ★ follows".

Clause (i) is therefore explicitly the **shape package only** — S3★ is *not* an admissibility clause. The necessity proof confirms this reading: "π satisfies admissibility (i) ... and admissibility (ii) ...; S3★(Σ') holds as a derived consequence (Step (B))" — i.e. S3★ is treated as *derived*, not as part of (i).

But the sufficiency construction verifies S3★ *under the "Clause (i)" heading*:

> "*Clause (i) (post-state invariants on M'(d)).* ... S8a, S8-depth, S8-fin, D-CTG★, D-MIN★, D-SEQ★ at the post-state inherit unchanged ... **S3★ at the post-state**: at every v ∈ dom(M(d)), M'(d)(π_swap(v)) = M(d)(v) ... so S3★ carries forward."

**Problem**: S3★ is simultaneously (a) excluded from clause (i) by the definition, (b) called "a derived consequence (Step (B))" in the necessity proof, and (c) verified as part of "Clause (i)" in the sufficiency proof. A reader checking the admissibility obligation against clause (i)'s definition finds S3★ both inside and outside the admissibility predicate. The sufficiency proof also re-derives S3★ inline for π_swap, duplicating the general derivation that Step (B) already supplies for every realisable π.

**Required**: Pick one classification. Either (a) state plainly that the sufficiency block verifies S3★ as the *separately-derived* post-state obligation (not as clause (i)), and cite Step (B) rather than re-deriving it inline; or (b) if S3★ is genuinely intended to be an admissibility clause, add it to the clause (i) enumeration and reconcile the necessity proof's "derived consequence" language. As written, the three treatments contradict one another.

### Issue 2: Forward-reference accretion in the J0 axiom paragraph

**ASN-0047, *Coupling and isolation* (J0)**: "The provenance couplings that pair K.μ⁺ with K.ρ — J1★ and its converse J1'★ — are stated and derived in *Scoped coupling constraints* below; here J0 is the only coupling constraining content allocation K.α."

**Problem**: This sentence neither advances J0's content nor states what J0 does — it inventories which other couplings exist, where they are defined, and which transition each constrains. That is pure downstream-deferral plus use-site inventory (the accretion pattern flagged for this note). J1★/J1'★ are already mentioned-before-definition in P4★'s definition box and in the K.μ⁺/J4 discharge prose; this sentence adds a third deferral to the same downstream section.

**Required**: Delete the sentence. J0's scope (it constrains K.α) is already clear from its statement, and J1★/J1'★ are reached when the reader gets to *Scoped coupling constraints*.

## OUT_OF_SCOPE

### Topic 1: Reordering within the link subspace
K.μ~ is content-only (link-subspace fixity forces π(v) = v on dom_L). A future ASN may define a link-reordering primitive, but its absence here is not a defect — it is already named in the open questions.

VERDICT: REVISE
