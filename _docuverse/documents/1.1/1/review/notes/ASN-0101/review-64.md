# Review of ASN-0101

## REVISE

### Issue 1: D10 boundary derivation uses P4★/P7a at Σ without closing the induction over DEL-extended traces
**ASN-0101, D10, *Boundary derivation***: "We use four premises: P4★ at Σ and P7a at Σ (both hold because the composite's initial state Σ is itself a composite boundary)..."

**Problem**: The ASN itself states (one paragraph earlier) that "ASN-0047's ExtendedReachableStateInvariants theorem guarantees these at composite boundaries *only for the pre-DEL vocabulary*." Once DEL is admitted, a boundary state Σ may have been reached via a DEL-containing composite, for which ASN-0047's theorem does not establish P4★/P7a. So the premise "P4★/P7a hold at Σ because Σ is a composite boundary" is licensed only if D10's own conclusion is applied at the *previous* boundary. The derivation proves a valid inductive step but presents it as self-standing — the closure over all DEL-extended traces (base + step) is never stated. As written, the argument that "every composite boundary in a DEL-extended trace satisfies P4★/P7a" is incomplete.

**Required**: Make the induction explicit: base case Σ₀ (satisfies P4★/P7a by initialisation); inductive step over the composite sequence, with non-DEL composites discharged by ASN-0047's ExtendedReachableStateInvariants and DEL-terminated composites by this derivation. Only then is the use of P4★/P7a at Σ licensed for traces that contain DEL.

### Issue 2: D8 restates its Group (ii)/(iii) collective justification twice
**ASN-0101, D8**: the Group (ii)/(iii) paragraph states "A predicate over frame-fixed components... propagates from Σ to Σ' unchanged; no member requires an individualized argument," and the justification's closing sentence repeats "Groups (ii) and (iii) are discharged inline in their descriptions above, each member propagating trivially under D0's pointwise frame."

**Problem**: The same collective discharge is asserted in two places with no added content in the second — a duplicate that the precise reader must recognise as redundant rather than as a distinct step. (`review-mode.anti-bloat`: two passages say the same thing in different words.)

**Required**: Keep the collective justification once (at the group description) and drop the trailing restatement, or have the trailing sentence carry actual content (e.g., the single non-trivial member, if any).

## OUT_OF_SCOPE

### Topic 1: Reconstruction/reversibility of the pre-DELETE arrangement
The Open Questions correctly defer versioning and historical backtrack to downstream ASNs. No error here — flagged only to confirm these are appropriately scoped out.

VERDICT: REVISE
