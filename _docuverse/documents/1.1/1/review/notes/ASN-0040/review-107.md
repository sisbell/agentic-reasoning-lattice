# Review of ASN-0040

## REVISE

### Issue 1: Sequential-commitment rationale stated three times across the document
**ASN-0040, "State space and transitions" / "B-Seq" Justification / "B8" proof**:
- "State space and transitions": *"We must not silently assume otherwise: a uniqueness argument that quietly presumes a single execution path would not hold across divergent branches... We therefore make the execution discipline an explicit axiom rather than an implicit reading of the model."*
- B8 proof: *"We invoke B-Seq explicitly because the foundation's Σ framework leaves →\* branching in general — without sequential commitment, β₁ and β₂ could proceed from a shared state onto divergent branches and Case 1 below would not go through..."*

**Problem**: The same argument — "Σ is branching, so uniqueness needs an explicit serialization axiom" — is made in the section preamble, restated in B-Seq's Justification, and restated a third time inside the B8 proof. This is reviser drift: the per-proof sentence in B8 duplicates the motivation already carried by the axiom's own section. The carrier reader must skip the same rationale three times. (Note carries `review-mode.anti-bloat`.)

**Required**: State the branching motivation once, at B-Seq. In B8, cite B-Seq as a dependency and use it; delete the "We invoke B-Seq explicitly because..." sentence. Remove the motivational sentences from the "State space and transitions" preamble.

### Issue 2: B-Seq prose explains why the axiom is needed rather than what it says
**ASN-0040, B-Seq Justification**: *"We must reconcile this with Nelson's design intent, which deliberately contemplates concurrent, branching allocation from genesis... The reconciliation is that concurrency across independent owners is concurrency over disjoint namespaces, where B7 (Namespace Disjointness) already guarantees... so it never threatens uniqueness within an owned subtree."*

**Problem**: This paragraph, plus the formal-contract *Scope:* field, is essay content arguing for the axiom's scope and reconciling it with design intent — not content advancing what the axiom asserts. It also defers forward to "(Open Questions)". This is exactly the "new prose around an axiom explains why the axiom is needed" pattern.

**Required**: Reduce to the axiom statement and a one-line implementation grounding. Move the disjoint-namespace reconciliation, if kept at all, to the Open Questions entry on cross-replica baptism where the deferral already lives.

### Issue 3: B8 Case 1 — the step from comparability to `s₁' →* s₂` is asserted, not derived
**ASN-0040, B8, Case 1**: *"without loss of generality β₁ precedes β₂... Since β₁ precedes β₂, s₂ is reachable from s₁' through a (possibly empty) sequence of transitions — that is, s₁' →* s₂."*

**Problem**: B-Seq orders *states*, not *acts*; "β₁ precedes β₂" is never defined against `→*`. The proof needs `s₁' →* s₂` (so that `a ∈ s₂.B`), but B-Seq only yields that `s₁'` and `s₂` are comparable. The case `s₂ →* s₁` (where `a ∉ s₂.B`) must be excluded by the WLOG, and that exclusion is what the WLOG should make explicit — it is currently glossed.

**Required**: Define "precedes" via `→*` on the states the acts operate on, and state the WLOG as: by B-Seq `s₁'` and `s₂` are comparable, and relabel so `s₁' →* s₂`; the relabeled argument is symmetric.

## OUT_OF_SCOPE

### Topic 1: B3's content-storage constraint
**ASN-0040, B3**: *"Content presupposes baptism: any content-storage layer built atop this model may store content at an address only after that address is baptized."* The negative property "a baptized position may hold nothing" (ghost element) is properly baptism-level, but the constraint on a *content-storage layer* is a guarantee about content storage and retrieval, listed as out of scope.
**Why out of scope**: The ordering constraint between baptism and content writes belongs to a content-storage ASN; this ASN should assert only that baptism is membership in s.B, independent of any content.

VERDICT: REVISE
