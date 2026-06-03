# Review of ASN-0069

## REVISE

### Issue 1: V9a asserts non-reconstructability of the acquisition path without proof
**ASN-0069, §"Provenance Recording", V9b/V9a**: "the acquisition path, the chain of custody by which a document obtained a given I-address (e.g. 'A transcluded to B, B forked to C'), is neither stored in R nor reconstructable. The indistinguishability ranges over the fork and transclusion paths..."

**Problem**: This is a substantive *negative* claim promoted to a "Property Introduced" but stated as fact with no derivation. "Not stored in R" is immediate from `R ⊆ T × E_doc` (no inter-document edges), but "not reconstructable" is the load-bearing half and is never established. Non-reconstructability requires a witness: two distinct acquisition histories (e.g. "fork from B that transcluded `a`" vs "direct transclusion of `a`") that yield an identical post-state — at minimum identical `R`. The ASN exhibits neither construction. Per the standard "claims without proofs are REVISE," the strong claim is unsupported.

**Required**: Either (a) supply an explicit two-history construction producing the same provenance record `(a, d_new)` and otherwise indistinguishable state, discharging the indistinguishability; or (b) weaken the claim to the provable form — "R alone records only containment `(a, d)` pairs, not inter-document derivation edges" — and drop the stronger "not reconstructable."

### Issue 2: V6a builds a self-contained link-query apparatus heavier than the fork guarantee requires
**ASN-0069, §"Subspace Selectivity", V6a and the three local definitions (`coverage`, `project`, `discoverable_from`)**: a 3-part lemma with full ⊆/⊇ derivations formalizing link discoverability across the fork.

**Problem**: The actual fork guarantee about links is small and follows directly: `L' = L` (the composite frames the link store at every step) together with V4 (inherited V-positions carry the *same* I-addresses) immediately gives "any link referencing inherited content still references it." V6a instead introduces three new operators not present in any foundation and proves a three-clause projection theorem. The apparatus is self-contained — `coverage`/`project`/`discoverable_from` are consumed only by V6a itself and its worked-example paragraph; no other claim (V8, V11, V12) depends on them. On a subsequent fork the apparatus also strains: clause (ii) preserves `d_src`'s projection while the content source is actually `d_op = d_prev ≠ d_src`, so (ii) and (iii) are about different documents. Under the anti-bloat classifier, machinery that serves only itself and does not feed the rest of the derivation is exactly the accretion to flag.

**Required**: Reduce V6a to the minimal in-scope statement: `L' = L` (from the constituent frame conditions, as already shown in V6a(i)) plus the shared-I-address consequence of V4. Move the formal `project`/`coverage`/`discoverable_from` theory to a future link-operations ASN (see OUT_OF_SCOPE).

## OUT_OF_SCOPE

### Topic 1: Formal link-discoverability / projection theory
**Why out of scope**: `coverage(e)`, `project(a, i, d, Σ)`, and `discoverable_from(a, d, Σ)` define link-query semantics — how an endset's spans project onto a document's V-positions and when a link is "findable from" a document. This is link-semantics territory (explicitly out of scope for this ASN) and not defined by any foundation. The fork's obligation is only to preserve `L` and the I-address identity of inherited content; the discoverability calculus built on top belongs in the ASN that defines link operations and queries.

### Topic 2: Snapshot vs. living fork; concurrent-modification guarantees
**Why out of scope**: These are correctly listed under Open Questions and not claimed here; flagging only to confirm the ASN's restraint is appropriate — they are new territory, not gaps in this ASN.

VERDICT: REVISE
