# Review of ASN-0040

## REVISE

### Issue 1: B8's formal contract makes the whole claim conditional, contradicting its own "unconditional" cross-namespace clause
**ASN-0040, B8 (Uniqueness)**: Prose states "Baptismal acts in distinct namespaces produce distinct addresses **unconditionally**"; but the Formal Contract Preconditions read "β₁, β₂ are distinct baptismal acts **under a single baptismal authority** (so B-Seq applies)… in a system conforming to B-Seq, B0★…" with Postcondition merely "a ≠ b."
**Problem**: The formal contract gates the *entire* postcondition on single-authority/B-Seq, so as contracted B8 delivers nothing unconditional — the cross-namespace guarantee the prose advertises is lost. The proof compounds this: the preamble "We take β₁ and β₂ to be commits under a single baptismal authority, so B-Seq applies" is stated *before* the case split, yet Case 2 (different namespaces) uses only B7 and never B-Seq.
**Required**: Split the formal contract to match the prose — an unconditional cross-namespace postcondition (precondition: both (p,d),(p',d') satisfy B6) and a single-authority same-namespace postcondition. Move the single-authority assumption into Case 1 only.

### Issue 2: B8 cites a "no-fork clause" that B-Seq's formal axiom does not contain
**ASN-0040, B8 proof, Case 1**: "By B-Seq's no-fork clause, two distinct commits never read the same state, so s₁ ≠ s₂."
**Problem**: B-Seq's Formal Contract Axiom states *only* the total-order property: "for any two such reachable states s, s', either s →* s' or s' →* s." The "no two commits fork from a shared state" appears solely in the Properties-Introduced table gloss, not in the axiom. Total ordering of realized states does not by itself yield s₁ ≠ s₂. So the load-bearing step s₁ ≠ s₂ rests on an unstated premise.
**Required**: Either add the no-fork clause to B-Seq's formal axiom, or derive s₁ ≠ s₂ from the distinctness of the two acts plus determinism of `baptize(p,d)` (same state + same namespace ⇒ same op ⇒ same result ⇒ not distinct). As written the citation has no formal source.

### Issue 3: B7 re-derives a guarantee the foundation already proves, using a notation that duplicates the foundation allocator stream
**ASN-0040, S(p,d) and B7 (Namespace Disjointness)**: S(p,d) is defined by c₁ = inc(p,d), cₙ₊₁ = inc(cₙ,0) — structurally identical to a foundation allocator's domain (base inc(p,d), then inc(·,0) chain). B7 then proves S(p,d) ∩ S(p',d') = ∅, which is exactly the content of T10a.6 (DomainDisjointness) / GlobalUniqueness (and, for non-nesting prefixes, T10/PartitionIndependence).
**Problem**: The multi-case B7 proof reconstructs disjointness reasoning the foundation has already discharged. The only daylight is that B7 ranges over arbitrary B6-valid p ∈ T rather than allocators in a conforming tree — but the ASN never states this as the reason for re-deriving, leaving a precise reader to wonder why the foundation result is not invoked.
**Required**: Either reduce B7 to T10a.6/GlobalUniqueness (mapping distinct B6-valid (p,d) to distinct allocator domains, with B6(i) ruling out the aliasing collision), or add one line stating the generality over arbitrary p ∈ T that prevents the reduction. Do not re-prove a foundation theorem silently.

### Issue 4: Repeated frame-dispatch boilerplate across three invariant proofs
**ASN-0040, B1, B10, B_fin proofs**: Each inductive step contains the near-verbatim sentence "By the s.B-frame dispatch (§B0a) the frame case carries [X] to s' unchanged; the baptismal case we now treat."
**Problem**: This is the same dispatch argument restated three times. It is correct but is mechanical bookkeeping that a single shared lemma (or one statement in B0a) could discharge once.
**Required**: State the frame-case preservation once (e.g., as a consequence of B0a: any s.B-frame invariant is trivially preserved by frame transitions) and cite it, rather than reproducing the paragraph per proof.

## OUT_OF_SCOPE

### Topic 1: The relationship allocated(s) ⊆ s.B and the allocator/registry correspondence
**Why out of scope**: The ASN explicitly distinguishes s.B from the foundation's allocated(s) and defers the alignment discipline to an Open Question. This is correctly future territory, not a defect here.

### Topic 2: Cross-replica baptism ordering in a shared namespace
**Why out of scope**: B-Seq is deliberately scoped to a single serialized commit path; divergent-replica ordering is listed as an Open Question and belongs to a later note on replication/coordination.

VERDICT: REVISE
