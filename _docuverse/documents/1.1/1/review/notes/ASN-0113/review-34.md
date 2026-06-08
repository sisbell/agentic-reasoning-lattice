# Review of ASN-0113

## REVISE

### Issue 1: W5's converse reasons about a configuration D-CTG★ excludes
**ASN-0113, "The extent of a single subspace" (W5)**: "Were `V_S(d)` *not* contiguous — `p, q ∈ V_S(d)` and `r ∈ VSlice(S, m)` with `p < r < q` and `r ∉ V_S(d)` — then for any level-uniform span `σ`..."

**Problem**: The note states elsewhere that "D-CTG★ holds at every reachable state," so `V_S(d)` is *always* contiguous; the non-contiguous case the converse analyzes cannot arise under the operation's carrier. The converse's only consumer is a speculative open question ("should a foundation extension ever relax D-CTG★..."). This is the excluded-case pattern the anti-bloat classifier targets. Compounding this, W5's *forward* direction ("contiguous ⟹ a single exact span exists") is acknowledged to be "immediate from W4" — it restates what W4 already proves. So W5's novel content is exactly the counterfactual half.

**Required**: Either drop W5 and replace it with a one-line note inside W4 identifying D-CTG★ (contiguity) as the load-bearing invariant that makes the single-span encoding exact, or move the full iff and its counterfactual converse into the open-question framing where the relaxed-foundation scenario belongs. Do not carry a standing claim whose substance is a configuration the reachable-state invariants forbid.

## OUT_OF_SCOPE

### Topic 1: Behavior under a relaxed D-CTG★ (fragmented span-set emission)
**Why out of scope**: The first open question — whether the operation must emit a fragmented span-set if D-CTG★ is ever relaxed — is genuine future territory contingent on a foundation change, correctly parked as an open question rather than specified here.

### Topic 2: Cross-vintage report comparison and kind-list evolution
**Why out of scope**: Interpreting an omitted member across documents of differing vintages (open questions 2 and 6) depends on a versioning/subspace-extension regime this ASN does not define; the in-scope same-kind-list comparison (W14) is fully discharged.

The core results are sound. W4's exact-coverage derivation (T5 prefix-confinement, half-open last-component bound) is correct and well-instantiated; the depth-3 worked instance properly exercises T5 where it is non-vacuous. W10/W11 (subspace confinement and disjointness, hence span-set necessity), W9 (TwoKindsOnly via S3★-aux), W19 (cardinality wp), and W20 (faithful count via CL-OWN/CL-UNIQ and S2/S3★) are all correctly derived. Boundary cases — unallocated vs. allocated-empty (W-pre), single-occupied-subspace, degenerate `m_S = 2` — are handled. No cross-ASN references outside the foundation set; no implementation-mechanics drift.

VERDICT: REVISE
