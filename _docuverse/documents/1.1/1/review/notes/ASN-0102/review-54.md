# Review of ASN-0102

## REVISE

### Issue 1: The "Amendment to ValidComposite★" paragraph pre-announces X14 and X10(b)/X15

**ASN-0102, "Definition of COPY" (Amendment to `ValidComposite★`)**: "It is *coupling-self-sufficient*: around its own step it records its own provenance ... and discharges, for its own effect, the step-local content of the couplings J0/J1★/J1'★ and the boundary property P4★, needing no support from neighbouring steps. The precondition PC1–PC4 ... is evaluated at COPY's own immediate pre-state ... the self-transclusion guarantee of X10(b)/X15 thus reads the source against COPY's own pre-state."

**Problem**: This paragraph asserts the conclusions that X14 proves in full (J0, J1★, J1'★, P4★ discharge) and that X10(b)/X15 establish (pre-state resolution under self-transclusion). It is pre-announcement meta-prose: the reader meets the same claim twice, once unproved here and once proved downstream. The only content the Amendment must carry is the *registration* fact — that COPY enters `ValidComposite★`'s atomic vocabulary as an elementary kind changing `M` and `R`.
**Required**: Trim to the registration sentence. Let the coupling discharge live solely in X14 and the pre-state pinning solely in X10(b)/X15.

### Issue 2: Document-ordering prose in X8

**ASN-0102, X8**: "Canonicalisation reduces the count in two distinct places ... We treat the within-region merges here and the boundary merges in X12."

**Problem**: This is a navigational note about where material is placed, not a step that advances the fragmentation argument. It is the forward-reference-accretion pattern (prose deferring to a downstream location).
**Required**: Drop the sentence; X8 can state its within-region result and X12 its boundary result without the explicit hand-off.

### Issue 3: PC3 justification drifts into link semantics to pin an in-scope fact

**ASN-0102, PC3**: "the link subspace `s_L` is populated only in creation order by MAKELINK and is not a legal target for COPY (Q1)."

**Problem**: The load-bearing fact PC3 needs is structural: COPY's resolved addresses are content-subspace-resident (`subspace_I(·) = s_C` by C1), so the target subspace is `s_C`. The appeal to *how* `s_L` is populated (MAKELINK, creation order) imports link-operation semantics — out of scope for this ASN — to justify a pin the structural argument already delivers.
**Required**: State PC3 from the resolution fact alone (sources are `s_C`-resident, hence `S = s_C`); drop the MAKELINK/creation-order rationale.

## OUT_OF_SCOPE

### Topic 1: Discoverability of copied content after later displacement (first Open Question)
**Why out of scope**: Link projection/discoverability under subsequent arrangement change is ASN-0098 territory; correctly deferred as an Open Question rather than claimed here.

### Topic 2: Containment obligations when a reference-holding document is itself re-referenced (second Open Question)
**Why out of scope**: Transitive containment/provenance across chained references is a future composite property, not a COPY postcondition.

---

Assessment of rigor: the operative proofs are unusually complete — the wp(COPY, S3★) reduction, the X16 last-component tiling (with disjointness within `s_C` and across the subspace boundary), and the X14 invariant sweep all hold up, and the five worked examples exercise interior, self-transclusion, empty-subspace, append, and coalescing boundaries. The remaining findings are accretion around the `ValidComposite★` amendment, not gaps in the mathematics.

VERDICT: REVISE
