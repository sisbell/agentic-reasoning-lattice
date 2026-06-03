# Review of ASN-0071

## REVISE

### Issue 1: Forward-reference use-site pointer in *Resolution*
**ASN-0071, Resolution**: "The cross-depth query `(d_E, σ_E)` below exercises precisely this second axis with zero missing positions."
**Problem**: This sentence does no work for the resolve-equivalence claim it sits inside. Its sole function is to tell the reader where the second relaxation axis is later demonstrated — a downstream use-site pointer of exactly the kind the anti-bloat classifier flags. The reasoning around it (the resolve = iaddrs_one equality and the two-axis bound) stands without it.
**Required**: Delete the forward pointer. The worked scenario already exercises the axis; the Resolution section need not announce that it will.

### Issue 2: Abstract "shallow anchor" pre-explanation duplicates the worked example
**ASN-0071, Resolution**: "*Second*, the vspec preconditions impose no constraint `#u = m_C` … a *shallow anchor* with `#u < m_C`, every named position present, is still not a well-formed ContentReference, so `resolve(d_s, σ)` is undefined and no equivalence is asserted."
**Problem**: This abstractly narrates a case that the cross-depth worked query `(d_E, σ_E)` then demonstrates concretely (`#u = 2 < m_C = 3`, zero missing positions). Stating the bound on the equivalence is legitimate, but pairing it with the standalone "shallow anchor" exposition *and* a forward pointer to the demonstration is the use-site-inventory pattern — two presentations of one fact, one of which defers to the other.
**Required**: Keep the one-clause statement that the equivalence requires `#u = m_C` (it bounds the claim); drop the expanded "shallow anchor" narration and let the worked example carry the concrete case.

## OUT_OF_SCOPE

### Topic 1: Relationship between current-state `find` and historical relation `R`
**Why out of scope**: The ASN correctly defers this to an open question; `find` is specified against current containment only, and the `R`-coincidence condition is future territory, not an error here.

### Topic 2: Replica-divergent completeness and visibility filtering
**Why out of scope**: Distributed views and access-control filtering are explicitly excluded under *What we do not specify*; they belong in later ASNs.

The core mathematics is sound: the PC proof (prefix-copy + T1 trichotomy + well-ordering), the `iaddrs ⊆ dom(C)` subspace-confinement argument, F-CONTENT's use of S3★-aux and L14, the reachability of the worked state, and the M16-based multi-block decomposition all check out. The remaining findings are accreted meta-prose, not correctness gaps.

VERDICT: REVISE
