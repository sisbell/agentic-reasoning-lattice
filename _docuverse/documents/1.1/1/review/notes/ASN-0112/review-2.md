# Review of ASN-0112

## REVISE

### Issue 1: V5 exact-cover is unproven for a link-only document
**ASN-0112, "Exact cover within a subspace" / V5**: "when all occupied positions share one subspace, `⟦σ_d⟧` contains no occupied-depth position outside `O(d)` — the span is a faithful trace, 'dense and contiguous'."

**Problem**: The substrate section cites D-CTG / D-MIN / D-SEQ only as the *content-subspace* shape. The V5 proof leans entirely on D-SEQ's dense run `{[s_C,1,…,1,k]}`. But "all occupied positions share one subspace" also covers a document whose *only* occupied subspace is the link subspace (content empty, one or more links — reachable: `CREATENEWDOCUMENT` then `K.λ` + `K.μ⁺_L`, with endsets referencing content elsewhere per L4/L9). For that case no density fact is cited, so if link positions had gaps the span would enclose unoccupied positions and V5 would fail. The note's own V5/V6 partition claims to be exhaustive over non-empty documents, but link-only falls in the first bucket without support. V8 already conditions origin-permanence on "content subspace non-empty," showing awareness that content may be absent, yet the span-exactness rigor never handles the residual link-only case.

**Required**: Either cite the per-subspace foundation shape facts (ASN-0047 D-CTG★ / D-MIN★ / D-SEQ★ are foundation) to ground link-subspace density, or restrict V5 explicitly to "content subspace occupied alone" and discharge the link-only case separately (or argue it unreachable).

### Issue 2: V2 single-subspace divergence reasoning is stated only for content
**ASN-0112, "The bounding span and its two endpoints" (V2 well-formedness)**: "in the single-subspace case the two tumblers share the canonical prefix `[s_C,1,…,1]` and differ only at the last component, so `k = #origin_d`."

**Problem**: This justification is content-specific. For a link-only single-subspace document the shared prefix is `[s_L,…]`, not `[s_C,1,…,1]`, and "differ only at the last component" again presumes the content-subspace dense-run shape. The *conclusion* `k ≤ #origin_d` survives (single-subspace ⇒ `#origin_d = #reach_d` by S8-depth ⇒ `divergence ≤ #origin_d` automatically), but the stated reason does not apply, so the proof as written does not cover the case it claims to.

**Required**: Replace the content-specific prefix argument with the level-uniformity argument (`#origin_d = #reach_d` within one subspace by S8-depth forces `divergence ≤ #origin_d`), so the single-subspace branch is correct for either subspace.

## OUT_OF_SCOPE

### Topic 1: Recovering exact per-subspace extents for a multi-subspace document
**Why out of scope**: This is the span-*set* operation (RETRIEVEDOCVSPANSET / ASN-0113), explicitly excluded. V7 correctly records that one span can only enclose disjoint subspaces; the recovery question is left as an open question, which is appropriate.

VERDICT: REVISE
