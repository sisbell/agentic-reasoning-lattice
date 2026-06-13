# Review of ASN-0123

I worked through the operational proofs in detail — VN-B1's case analysis, V-WF's discharge of both ValidComposite★ clauses, the V9 severance theorem, V8's coverer-set argument, V9w's boundary-dependent provenance, and both worked instances (carry-through and cross-owner). The logical content is sound: the case analyses are exhaustive (the K.δ taxonomy in VN-B1 rules out Node/k=2/k=1/k=0 individually; severance closes both branches of the d_src≼pfx(π) split), the boundary cases are handled (empty source n=0, first fork, repeated addresses with |A|<n, cross-owner), the load-bearing precondition P-bdy is identified with a concrete interior-state failure scenario, and the ASN correctly proves a *local* analog VN-B1 rather than citing ASN-0040's B1 (whose transition system does not transfer) or B2 (whose global precondition is unavailable). No cross-ASN reference outside the foundation set; no reinvented notation. I verified the cross-owner worked instance arithmetic (d_src=1.1.0.1.0.1, v=1.1.0.2.0.1 diverging at position 4 → severance; a₁'s subtree ∩ ran(M'(v))={a₁} via SA → project={[1,1],[1,3]}).

I found one defect.

## REVISE

### Issue 1: Garbled sentence in the implementation-evidence section
**ASN-0123, The Implementation Evidence, deviation 1**: "The comment "increased from 11 to support deeper version chains" records that the previous bound bound in practice."
**Problem**: The clause "the previous bound bound in practice" has no predicate — "bound bound" is a doubled/garbled verb. As written the sentence does not parse. (Compare the foundation phrasing in T0(b): "the original bound of 11 was concretely hit in practice.")
**Required**: Fix to a well-formed sentence, e.g. "records that the previous bound was hit in practice." This is the sole remaining issue; the proof content and verdict-bearing arguments are otherwise sound.

## OUT_OF_SCOPE

The topics deferred in the Open Questions (concurrent-fork serialization, recoverability of derivation direction across ownership boundaries, link-subspace carry-through, location-fixed windowing, withdrawal/supersession semantics) are correctly future territory rather than gaps in this ASN — each is a guarantee about a future operation or a concurrency model, not a missing clause of the fork's contract. The scope note's enumerated topics (document creation, version comparison, content/link operations, delivery, replication) are appropriately untouched; the ASN defines no claims for them.

VERDICT: REVISE
