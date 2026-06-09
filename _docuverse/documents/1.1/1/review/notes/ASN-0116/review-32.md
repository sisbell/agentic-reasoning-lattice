# Review of ASN-0116

This is a thorough, largely correct treatment. The two-layer split (content allocation vs. arrangement shift) is cleanly maintained, boundary cases (front-insertion J=1, append J=N+1, empty subspace) are all covered, contiguity is proven by an explicit interval argument rather than hand-waved, the provenance coupling (J0, J1★, J1'★) is discharged with the J1'★ subtlety handled correctly, and the weakest-precondition analysis (P6) is genuinely non-trivial. The issues below are notational/clarity, not correctness.

## REVISE

### Issue 1: Local claim labels P0–P6 collide with cited foundation ASN-0047
**ASN-0116, "Invariants the operation must preserve" and Claims Introduced table**: the ASN defines its own headline claims `P0 (OriginIdentity)`, `P1 (InsertedRun)`, `P2 (ContentAppendOnly)`, `P3 (PositionImpermanence)`, `P6 (DiscoverabilityWP)`, etc.
**Problem**: ASN-0047 — a foundation this ASN cites repeatedly in the same proofs — already uses `P0 (ContentPermanence)`, `P1 (EntityPermanence)`, `P2 (ProvenancePermanence)`, `P3 (ArrangementMutabilityOnly)`, `P6 (ExistentialCoherence)`. The collision is live, not latent: I-PROV cites *"(P2 of ASN-0047, R monotone)"* (provenance permanence) while the P7-preservation argument cites bare *"P2-monotonicity of the store"* (the local content claim). A reader meeting bare `P2` must guess which of two distinct invariants is meant. The same proof neighborhood also cites ASN-0047's `P7`, `P7a`, `P8` bare, so the namespace is genuinely shared.
**Required**: Rename the local INSERT claims to a non-colliding prefix (the ASN already uses `I-*` and `F-*` for its other local clauses — a `P` collision with the cited foundation is avoidable). At minimum, every reference to an ASN-0047 P-invariant must carry the "of ASN-0047" qualifier consistently.

### Issue 2: Claims-Introduced table orders P6 before P5
**ASN-0116, Claims Introduced table**: rows run `… P4 … P6 (DiscoverabilityWP) … P5 (DocumentIsolation) …`.
**Problem**: P5 is defined before P6 in the body (P5 in "Invariants the operation must preserve," P6 in "A weakest precondition"), so the table's reversed order is a small but real navigation snag.
**Required**: Reorder the table to match body sequence, or renumber.

### Issue 3: Depth-`m` rationale duplicated between framing prose and precondition
**ASN-0116, "The problem" framing vs. INSERT precondition**: the framing paragraph ("The depth `m` deserves care: S8-depth fixes a single common depth only when `V_S(d) ≠ ∅` … We carry `m = #p ≥ 2` throughout, equal to the S8-depth of `V_S(d)` whenever that set is non-empty") restates what the precondition then states formally ("`m := #p ≥ 2`, and when `V_S(d) ≠ ∅` this `m` equals the common depth that S8-depth fixes").
**Problem**: Per the anti-bloat checks, two passages carry the same content in different words. The empty-subspace depth-fixing insight (ValidFirstInsertionPosition) is the one non-duplicated nugget; the rest is restated at the precondition.
**Required**: Collapse to one statement — fold the empty-case insight into the precondition and drop the framing restatement (or vice versa).

## OUT_OF_SCOPE

### Topic 1: Insertion at a transclusion-shared position, concurrent insertions, transclusion provenance, post-edit fragmentation
**Why out of scope**: These are correctly posed as Open Questions, not claimed. Transclusion (COPY), concurrency, and fragmentation belong to future operations (ASN-0118 and beyond per the scope notes); the ASN draws no claims about them.

VERDICT: REVISE
