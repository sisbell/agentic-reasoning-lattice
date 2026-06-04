# Review of ASN-0091

## REVISE

### Issue 1: RA-adm is a single-state preservation property but is discharged with a reachability-closure theorem
**ASN-0091, "Remaining per-state invariants (from ExtendedReachableStateInvariants)"**: "K.μ~ is a valid composite and ASN-0047's ExtendedReachableStateInvariants establishes that it preserves the full per-state invariant package at its boundary."
**Problem**: RA-adm is defined as a *relative preservation* property — "every per-state foundation invariant satisfied by Σ is satisfied by Σ'." But the foundation theorem cited, ExtendedReachableStateInvariants, is keyed to *reachability*: "Every state reachable from Σ₀ … satisfies the per-state invariants." It gives `reachable(Σ') ⟹ invariants(Σ')`, not `invariants(Σ) ⟹ invariants(Σ')`. The only per-transition theorem ASN-0047 supplies, ExtendedTransitionInvariants, covers P3 alone — not the arrangement-dependent package (S3★, S3★-aux, CL-OWN, CL-UNIQ, S8★) that this layer must discharge. As written, the hardest conjuncts of RA-adm are delegated to a theorem whose hypothesis (reachability of Σ) is never assumed. In the abstract Vstream-only class, Σ is an arbitrary invariant-satisfying state, not necessarily reachable.
**Required**: Either add "Σ reachable from Σ₀" as a standing premise and show the K.μ~ composite extends reachability (so ExtendedReachableStateInvariants then applies to Σ'), or cite/establish a genuine single-step preservation property for the arrangement-dependent invariants. The current one-line delegation does not discharge them under RA-adm's stated hypothesis.

### Issue 2: "State-Component-Only Invariants" conflates per-transition invariants with single-state predicates
**ASN-0091, "State-Component-Only Invariants"**: "This class is precisely the frame-inherited invariants: … S0, S1, S4, S7 … P0, P1, P2, P3 … M1 … L12 … C0 … all hold at Σ' iff they hold at Σ."
**Problem**: Several listed invariants are not single-state predicates but relations on a transition `Σ → Σ'` (S0, S1, P0, P1, P2, P3, M1, C0, L12 are each `(A Σ → Σ' :: …)`). For these the phrase "hold at Σ' iff they hold at Σ" is ill-typed — there is no "holds at Σ'" for a binary transition invariant. The correct discharge is "the REARRANGE transition Σ → Σ' *satisfies* them, because the components they constrain are fixed by RA-frame" (e.g., P0 holds because `Σ'.C = Σ.C` gives both `dom(C) ⊆ dom(C')` and value preservation). The substance is sound, but the framing mixes two categories and applies a single-state iff to transition predicates.
**Required**: Separate the single-state predicates (S4, S7, S7a, S7b, S7d, M0, P6, P7, P8, C1, C1b, …) from the transition invariants (S0, S1, P0–P3, M1, C0, L12, …); discharge the former by frame inheritance ("holds at Σ' because the component is unchanged") and the latter as transition-satisfaction.

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics
**Why out of scope**: CS3 confines cuts to the content subspace; what invariants a link-subspace rearrangement would preserve is new territory, correctly deferred to the Open Questions rather than treated as a gap here.

### Topic 2: Reconstitution of a same-source split span
**Why out of scope**: RE-trans explicitly disclaims whether two fragments jointly reconstitute the original source span ("is not established here"); this is a future-ASN question, not a defect in the present claims.

VERDICT: REVISE
