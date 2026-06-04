# Review of ASN-0076

I read the note as a composite-operation specification: EDITLINK is two `K.λ` steps, and the E0–E10 claims establish original-preservation, distinctness, divergence, and the supersession witness. The proofs are largely sound and the worked example correctly exercises the claims. My findings are anti-bloat (this note carries `review-mode.anti-bloat`), not correctness.

## REVISE

### Issue 1: Use-site invariant inventory in E0

**ASN-0076, E0 "Invariant inheritance"**: "every per-state invariant of the extended reachable state continues to hold at the post-state — in particular L0, L1, L1a, L1b, L1c, L3, L14, L-fin, C-fin, CL-OWN, CL-UNIQ, and the per-state S-invariants S2, S3★, S3★-aux, S4, S7a–d, S8a, S8-fin, S8-depth, S8★, D-CTG★, D-MIN★, D-SEQ★, P6, P7, P8, NodeLineage."

**Problem**: This is a use-site inventory. The substantive content is exactly "EDITLINK is a ValidComposite★, so by ExtendedReachableStateInvariants (ASN-0047) every per-state invariant holds, and by ExtendedTransitionInvariants the transition invariants hold." The reproduced enumeration advances no reasoning — ExtendedReachableStateInvariants *is* the canonical list — and it is a drift hazard: if ASN-0047's invariant suite changes, this copy goes silently stale.

**Required**: Replace the enumeration with the two citations (ExtendedReachableStateInvariants for per-state, ExtendedTransitionInvariants for transition, P0 subsuming S0/S1). Drop the verbatim invariant list.

### Issue 2: Rhetorical essay content in consequence slots

**ASN-0076, E7 interpretation**: "exactly the failure mode Nelson decries when he writes that history must be navigable." **ASN-0076, E10 interpretation**: "Nelson endorses this posture explicitly when he describes the docuverse as 'what connects here from other documents' being a question the reader (or owner) asks, not a fact pushed at them."

**Problem**: These rhetorical appeals sit in the consequence discussion after the formal claims and add no formal content — they are essay flourishes the precise reader works around. (The neighboring "the implication is…" sentences that derive actual consequences are fine and should stay.)

**Required**: Delete the two Nelson-appeal sentences; retain the consequence statements that do formal work.

## OUT_OF_SCOPE

### Topic 1: Supersession-chain invariants, cycle-freedom, traversal termination, and "current successor" computation
**Why out of scope**: These (raised in Open Questions) concern a future link-search/lineage-resolution ASN, not the EDITLINK composite itself. EDITLINK correctly establishes only the structural witness (E7) and defers reader-side policy.

### Topic 2: Authorization of `d_new` (who may publish a supersession against another's link)
**Why out of scope**: E6's application-layer note correctly defers executor/capability semantics to a future authorization ASN; the link model has no executor field.

VERDICT: REVISE
