# Review of ASN-0101

## REVISE

### Issue 1: D8 treats composite-boundary properties as per-state invariants with an unlicensed pre-state assumption

**ASN-0101, D8, Group (iii)**: "P4★ by the chain `Contains_C(Σ') ⊆ Contains_C(Σ) ⊆ R = R'`, composed of three independent steps: ... the middle inclusion `Contains_C(Σ) ⊆ R` is pre-state P4★ (assumed at `Σ`)."

**Problem**: In ASN-0047, P4★, P4a, and P7a are *composite-boundary properties*, not per-state invariants — the ExtendedReachableStateInvariants theorem lists them separately ("Every state at a composite boundary additionally satisfies the composite-boundary properties: P4★ ∧ P4a ∧ P7a"). DEL is an elementary transition that, by D10, may appear *inside* a composite at a non-boundary state. At such an intermediate pre-state `Σ`, P4★ is not guaranteed to hold (e.g., a preceding K.μ⁺ may have placed content whose provenance a later K.ρ has not yet recorded). The step "pre-state P4★ (assumed at `Σ`)" is therefore unlicensed for general DEL pre-states. D8's Group (iii) header ("Transition and per-state invariants") and its inclusion of P4★/P4a/P7a in the preserved list assert more than the conditional frame argument delivers: the conditional "if `Σ` has P4★ then `Σ'` does" yields nothing at the DEL-terminated boundary where P4★ must actually be established.

**Required**: Either drop P4★/P4a/P7a from D8's per-state preservation list (handling them as composite-boundary obligations) or recast the claim as what is actually true: DEL is content-subspace-monotone-shrinking (`Contains_C(Σ') ⊆ Contains_C(Σ)`) and R-preserving, so it cannot *break* P4★ regardless of whether the pre-state satisfies it — and the boundary obligation itself is discharged at the composite level, not by an unjustified per-step assumption.

### Issue 2: D10 extends ValidComposite★ without discharging the composite-boundary properties for DEL-containing composites

**ASN-0101, D10**: conditions (1) transition preconditions and (2) coupling constraints "J0, J1★, and J1'★ (ASN-0047) hold between `Σ` and `Σ'`."

**Problem**: D10 claims to extend ASN-0047's ValidComposite★ to admit DEL, and carefully treats J0/J1★/J1'★. But ASN-0047's composite-boundary obligations are P4★ ∧ P4a ∧ P7a *in addition to* the coupling constraints. For a valid composite that ends in a DEL step, `Σ'` is a composite boundary and must satisfy these three. D10 is silent on them. The boundary discharge for DEL-terminated composites is thus left undischarged here, and (per Issue 1) is not supplied by D8 either — D8 only gives conditional per-step preservation. The gap is small in substance (DEL shrinks `Contains_C` and fixes `R`, so it is neutral-to-helpful for all three) but it is exactly the kind of "by similar reasoning" omission the standard forbids: the composite-validity machinery is what D10 is extending, so the reader expects the boundary properties addressed.

**Required**: State and discharge the composite-boundary obligations (P4★, P4a, P7a) for DEL-containing composites within D10, paralleling the J0/J1★/J1'★ treatment.

## OUT_OF_SCOPE

### Topic 1: Full historical reconstruction of arbitrary prior arrangement states
**Why out of scope**: The recoverability discussion correctly defers full versioning/reconstruction to a multi-step composite mechanism (J4 ForkComposite plus retained versions); DEL supplies only the non-destruction substrate. This is future-ASN territory, not an error here, and the Open Questions frame it as such.

VERDICT: REVISE
