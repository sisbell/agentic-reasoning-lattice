# Review of ASN-0091

## REVISE

### Issue 1: Defensive meta-prose contrasting an unused derivation route
**ASN-0091, Composite-Boundary Properties**: "The earlier route — exhibiting a single trace (trace-to-Σ then the REARRANGE step) and arguing that `Σ'.R = Σ.R` adds no provenance pair — would establish only the existential 'for some trace,' which is strictly weaker than P4a's universal and does not discharge it. The boundary citation discharges the universal directly."

**Problem**: The claim is fully discharged one sentence earlier: under RA-bndy, Σ' is a reachable composite boundary, so ExtendedReachableStateInvariants delivers P4★∧P4a∧P7a (P4a already universally quantified over traces in its ASN-0047 statement). The quoted paragraph describes a *rejected weaker derivation* and argues why it fails — defensive justification that advances no reasoning. This is reviser drift: prose defending the chosen approach against a strawman alternative. The same defensiveness recurs in the worked example ("but these are illustrations of the cited theorem, not an independent re-derivation"), so the point is being guarded twice.
**Required**: Delete the "earlier route" contrast; the ExtendedReachableStateInvariants citation under RA-bndy is the whole argument. Drop the parallel "not an independent re-derivation" guard in the worked example.

### Issue 2: Clause (v) discharge forward-references a frame stated ~10 sections downstream
**ASN-0091, Clause Correspondences table, row (v)**: "discharged by RE-sub (Pointwise-Fixity Frames, below): RE-sub fixes `π(v) = v` on every non-cut-subspace V-position…"

**Problem**: RE-sub and RE-ext are derived *directly* from ASN-0084's R-PPERM/R-SPERM and R-FRAME-P/S(a) — they do not depend on the K.μ~ realisation argument they are used to complete. Yet they are stated in "Pointwise-Fixity Frames (REARRANGE_K-specific)" near the end of the note, forcing clause (v) (in the realisation section) to defer downstream. The ordering manufactures a forward reference for a fact that has no upstream dependency.
**Required**: Relocate RE-sub/RE-ext ahead of the clause-correspondence table (they sit naturally with the per-clause discharges), so clause (v) cites an already-established frame rather than pointing "below."

## OUT_OF_SCOPE

### Topic 1: Split-span transclusion reconstitution
**Why out of scope**: Whether two fragments of a same-source transcluded span jointly reconstitute the original is correctly deferred to Open Questions; it is genuinely new territory, not a defect here.

VERDICT: REVISE
