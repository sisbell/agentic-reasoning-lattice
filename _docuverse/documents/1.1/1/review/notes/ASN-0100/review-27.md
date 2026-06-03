# Review of ASN-0100

This is an unusually thorough ASN — two worked examples, explicit wp analysis, a careful per-step invariant survey, and a deliberate (correct) disclaiming of ASN-0082's I3-V/I3-CS/I3-CX. Most invariants are discharged with genuine depth. Two completeness gaps remain in the invariant verification.

## REVISE

### Issue 1: S8★ verification establishes existence but not condition (c) (uniqueness)

**ASN-0100, §Per-subspace span decomposition (S8★)**: "The post-state decomposition is finite and well-defined; its existence is also guaranteed independently by M2 applied to the post-state. S8★ is preserved."

**Problem**: S8★ (PerSubspaceSpanDecomposition; ASN-0047) is defined to retain "conditions (a) (lockstep displacement) and (b) (label well-definedness); condition (c) (uniqueness of the maximal-run decomposition) ... only on the content subspace." The §S8★ verification discharges (a) (the run construction), (b) (block well-definedness), and *existence* via M2 (DecompositionExistence; ASN-0058) — but it never discharges condition (c), uniqueness. "Finite and well-defined" is not "unique." The section nonetheless concludes "S8★ is preserved," which overclaims relative to what is shown. This is precisely a skipped conjunct of a required invariant.

**Required**: Discharge condition (c) on the content subspace by citing M12 (CanonicalUniqueness; ASN-0058) — confirming its standing preconditions (the same S8-fin, S2, S3★|_{s_C}, S8a, S8-depth already verified for M2) hold of the post-state, so the maximal-run decomposition of `M'(d)|_{V_{s_C}(d')}` is unique. Existence alone (M2/M11) does not close S8★.

### Issue 2: ActivatedEmission omitted from the per-state invariant survey

**ASN-0100, §Atomicity and Canonical Order**: "ASN-0047's ExtendedReachableStateInvariants enumerates ~28 per-state invariants. Many of these are trivially preserved by frame ... We group these by the state component they range over: *Entity-set invariants* — P8 (EntityHierarchy), NodeLineage (NodeDescentFromBootstrap), M0 (DocumentTumblerWellFormed; ASN-0093)."

**Problem**: ASN-0047's ExtendedReachableStateInvariants explicitly conjoins `... P8 ∧ NodeLineage ∧ ActivatedEmission ∧ L0 ...`. ActivatedEmission is a required per-state invariant but appears in no grouping; the entity-set grouping instead names M0, which is *not* in the enumeration. Since the ASN claims to systematically cover the enumerated invariants, the omission of a named conjunct is a real gap, even though it holds trivially by the `E' = E` frame.

**Required**: Add ActivatedEmission to the entity-set grouping, noting it is preserved by `E' = E` (INS.frame.E) since INSERT fires no K.δ. While there, confirm the composite transition obligation P3 (ExtendedTransitionInvariants; ASN-0047) explicitly — all its conjuncts (P0, L12, `E ⊆ E'`, `R ⊆ R'`, value preservation) are verified piecemeal, but P3 itself is never named as discharged.

## OUT_OF_SCOPE

None. The ASN correctly bounds itself (content-subspace INSERT only) and defers DELETE, COPY, REARRANGE, link-subspace insertion, version derivation, and replication.

VERDICT: REVISE
