# Review of ASN-0101

I verified the core machinery in depth — the containment-reduction proof, the shift bijection D1, the well-formedness preservation D8 (source-correspondence over S2/S3★/S8★/CL-OWN/CL-UNIQ), the wp derivations D10 (including the inclusion-exclusion cardinality step), and the D11 induction. The mathematics is sound: the region partition `V_S(d) = Λ ⊎ X ⊎ Π`, the order-preserving inverse `σ_d`, the J0/J1★/J1'★ vacuity, and the three worked examples all check out. References are all to foundation ASNs (0034, 0036, 0043, 0047, 0053, 0058, 0082, 0093, 0098), so no cross-ASN violations. The only findings concern accreted implementation-mechanics prose that the note carries the `review-mode.anti-bloat` classifier to catch.

## REVISE

### Issue 1: Decorative implementation-mechanics paragraph in D6's structural slot
**ASN-0101, D6 (Subspace isolation)**: "*Implementation evidence.* Gregory's code delivers both directions of isolation, by two unrelated mechanisms (an exponent-guarded `tumblersub` short-circuit in one direction, positional ordering of text below link addresses in the other). The abstract guarantee is mechanism-agnostic: D6 requires only that the unaffected subspace be preserved, by whatever means."

**Problem**: This labeled paragraph names two C-level mechanisms and then disowns them in its own concluding sentence ("mechanism-agnostic ... by whatever means"). It does not verify a postcondition against the implementation (unlike the worked examples, which do real verification) — it asserts how one implementation happens to work and then declares that irrelevant to D6. A reader following the D6 isolation claim must process and discard implementation detail the ASN itself says carries no abstract weight. This is the accretion the anti-bloat classifier targets.

**Required**: Delete the implementation-evidence paragraph, retaining at most the load-bearing sentence "D6 requires only that the unaffected subspace be preserved" if it adds anything beyond the claim already stated.

### Issue 2: Recurring disowned implementation asides
**ASN-0101, "What shifts"**: "(Gregory realises this through a two-phase knife-and-shift walk over the tree of POOM crums materialising `M(d)`; the tree structure is an implementation choice, not an abstract commitment.)"
**ASN-0101, "The operation"**: "Gregory's `bed.c` likewise realises the deletion as a single run-to-completion procedure."

**Problem**: Same pattern as Issue 1, repeated across sections: each names an implementation realization and immediately frames it as non-binding. The `bed.c` sentence in particular adds nothing to the preceding argument (the K.μ~ admissibility-clause-(v) reasoning already establishes that DEL has no composite substitute); it is redundant corroboration appended after the claim is closed. These asides compound across cycles and should be flagged at source.

**Required**: Remove the disowned implementation asides, or consolidate genuine implementation grounding into the verification done by the worked examples (where it actually discharges a postcondition) rather than scattering disowned mechanism-naming through the structural prose.

## OUT_OF_SCOPE

### Topic 1: The Open Questions (versioning, reconstruction, causal ordering, orphan rediscovery)
**Why out of scope**: These are correctly marked as downstream obligations — reconstruction of prior arrangements, DELETE/INSERT round-trip recovery, orphan enumeration, and cross-document causal ordering all require additional state components (a versioning mechanism, an orphan registry) beyond D0's frame. The note properly states them as open rather than attempting them. No action needed.

VERDICT: REVISE
