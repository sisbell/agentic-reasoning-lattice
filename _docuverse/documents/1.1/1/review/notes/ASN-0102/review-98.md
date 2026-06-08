# Review of ASN-0102

## REVISE

### Issue 1: Resolution-preamble "two facts" paragraph is a forward-reference inventory

**ASN-0102, "The source designation and its resolution"**: "Resolution supplies two facts from ASN-0058. First, *every resolved address already exists*: by C1 ... Second, *the run count `k` is the total number of runs of the concatenated resolution* — the sum over references `k = (+ i ... )`, where each `k_i` ... counts the blocks of `r_i` that are maximal under M7's joint V- and I-adjacency merge condition *within that reference*."

**Problem**: This paragraph pre-states two ASN-0058 results before either is used, then both are re-stated at their actual use sites. The *first fact* (resolved addresses in `dom(Σ.C)`) is re-cited in PC1, X3, the `wp` computation, and X17/P7 — at least four further invocations of C1. The *second fact* (the run-count `k` decomposition into per-reference `k_i` with the within-reference maximal-merge gloss) is **not used anywhere in the Precondition or Definition sections**; it is fully re-derived, with greater precision and the within/across-reference split it actually needs, in X8. The paragraph therefore advances no reasoning where it sits — it is an inventory of downstream consumers of ASN-0058, matching the "two paragraphs say the same thing" and "enumerates downstream consumers" accretion patterns.

**Required**: Delete the paragraph. Cite the first fact (C1) where PC1 first needs it; let X8 carry the run-count decomposition at its single use site.

### Issue 2: X2's body proves a stronger property than its claim and drifts into K.α mechanics

**ASN-0102, X2 (NoFreshAllocation)**: "COPY consumes no previously-unallocated address. K.α's address selection (ASN-0093) is determined by the per-document content set `D_d = {a' ∈ dom(Σ.C) : origin(a') = d}`; X1 leaves `dom(Σ.C)` unchanged and X6 alters no origin, so `D_d` is identical at `Σ'` and `Σ`, and any subsequent K.α behaves identically — whichever case it selects."

**Problem**: The stated claim ("consumes no previously-unallocated address") is the immediate corollary of X1 and needs nothing further. The second sentence proves a *different and stronger* property — that a *subsequent* K.α's allocation frontier is unchanged — by reasoning about K.α's internal address-selection cases. That is downstream-operation mechanics, and the per-case "behaves identically — whichever case it selects" reasoning is exactly the kind of imagined-case prose the carrier (X1, frame-only) already settles. The label and the body are about two different things.

**Required**: Either restate the claim to be the frontier-preservation property it actually proves, or strip the K.α-selection reasoning and let X2 stand as the one-line corollary of X1.

## OUT_OF_SCOPE

### Topic 1: Discoverability of copied content under later displacement; provenance of reference-of-reference; cross-time view divergence; identity after origin unreachability

**Why out of scope**: These are the four Open Questions the ASN itself defers. They concern subsequent operations and projection/provenance dynamics (ASN-0098 territory) rather than COPY's own state transition, and are correctly left to future ASNs.

META: (not applicable — the ASN specifies state, an operation on it, and its invariants abstractly; it has not drifted into implementation mechanics.)

VERDICT: REVISE
