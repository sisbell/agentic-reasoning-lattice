# Review of ASN-0069

## REVISE

### Issue 1: V8b's K.μ⁺_L argument cites V4b for a fact V4b does not supply

**ASN-0069, V8b (Non-monotonicity paragraph)**: "K.μ⁺_L extends only V_{s_L} of its target document; since F ⊆ V_{s_C}(d_src) (V4b) and the content and link subspaces are partitioned by subspace(v) (with s_C ≠ s_L by SubspaceConventionAxiom, ASN-0047), F ∩ V_{s_L} = ∅..."

**Problem**: F is defined as V_{s_C}(d_src)|_{Σ'} — the restriction of V_{s_C}(d_src) to state Σ'. The relation F ⊆ V_{s_C}(d_src) is trivially true by F's definition as a restriction (and time-indexing collapses by V5's source isolation, M'(d_src) = M(d_src)). V4b establishes V_{s_C}(d_new) = V_{s_C}(d_src) — a fact about d_new's domain at the post-fork state, not about F. The citation is misdirected; V4b adds nothing to the subset relation being claimed.

**Required**: Drop the V4b citation. If a citation is wanted, cite F's definition directly, or cite V5 (which ensures V_{s_C}(d_src) is the same at Σ and Σ').

### Issue 2: V12(d) contains meta-commentary about an earlier draft

**ASN-0069, V12(d)**: "(The notation ran(M'(d_new)) ∩ ran(M(d_src)) was used in an earlier draft to suggest 'shared I-addresses'; by V4 the intersection equals ran(M'(d_new)) itself, so the intersection adds no content and is dropped.)"

**Problem**: A specification should not contain commentary about its own draft history. Comments about superseded notations belong in commit messages or change logs, not in the formal text. The parenthetical also asserts a positive fact (V4 ⇒ ran(M'(d_new)) ⊆ ran(M(d_src))) while framing it as a deletion rationale — readers must reconstruct the positive claim from the negation.

**Required**: Remove the parenthetical. If the simplification merits a positive statement, write it as one (e.g., "By V4, ran(M'(d_new)) ⊆ ran(M(d_src)) — the shared I-address set is exactly ran(M'(d_new))").

### Issue 3: V11's premise is ambiguous about which state determines the restriction set V_{s_C}(d^{i-1}_new)

**ASN-0069, V11**: "no transition between consecutive fork composites modifies any chain source's content-subspace arrangement — that is, the pre-state of each step i agrees with the post-state of step i − 1 on M(d^{i-1}_new)|_{V_{s_C}(d^{i-1}_new)} for every 1 ≤ i ≤ k"

**Problem**: V_{s_C}(d^{i-1}_new) is state-dependent. The premise does not state whether the restriction set is taken from the pre-state of step i, the post-state of step i − 1, or whether both must yield the same set. A K.μ⁺ that adds new content-subspace V-positions to d^{i-1}_new across the gap would change V_{s_C}(d^{i-1}_new); whether this violates the premise depends on the unstated convention. The Remark clarifies the operational scope (admitting link-subspace modifications, forbidding content-subspace modifications), but the formal premise itself leaves the restriction set ambiguous, and the proof's appeal to "the IH-supplied values are exactly the values V4 reads" depends on the set being unchanged across the gap.

**Required**: Make the premise explicit. For example: "V_{s_C}(d^{i-1}_new) is the same set in the post-state of step i − 1 and the pre-state of step i, and for every v in this set, M(d^{i-1}_new)(v) is the same value in both states." This forces the premise to forbid both domain changes and value changes on the content-subspace, matching the Remark's scope.

## OUT_OF_SCOPE

None. The ASN's open questions appropriately defer future concerns (concurrency, snapshot vs. living fork semantics, transcluded sources, fork enumeration, version DAG structure, deletion interactions). The current ASN restricts itself cleanly to the fork transition mechanics.

VERDICT: REVISE
