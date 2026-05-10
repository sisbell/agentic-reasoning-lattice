# Review of ASN-0030

## REVISE

### Issue 1: INSERT and PUBLISH missing from operations analysis
**ASN-0030, "Operations and the Two Properties"**: "We now examine each operation through the lens of identity and reachability."
**Problem**: The section covers DELETE, COPY, REARRANGE, and CREATENEWVERSION but omits INSERT and PUBLISH. INSERT is the only operation that extends dom(Σ.I) — it is the operation most central to address permanence. Its reachability effect (fresh content enters state (i) immediately) is the primary witness for transition (iii)→(i). PUBLISH (D10a, ASN-0029) trivially preserves both identity and reachability (its frame condition leaves Σ.I and Σ.V unchanged), but "each operation" means each operation.
**Required**: Add an INSERT subsection establishing: (a) A0 applies to all previously allocated addresses, (b) +_ext extends dom(Σ.I) with fresh addresses, (c) fresh content is immediately reachable through the target document. One sentence for PUBLISH suffices.

### Issue 2: A5 not labeled as specification requirement
**ASN-0030, "COPY"**: "COPY(d_s, p_s, k, d_t, p_t) — copy k positions from d_s into d_t — satisfies: ... (a) (A j : 0 ≤ j < k : Σ'.V(d_t)(p_t + j) = Σ.V(d_s)(p_s + j))"
**Problem**: ASN-0026 asserts only that COPY has `fresh = ∅` (+_ext) and writes to the target document (P7). The V-space postcondition A5(a) — that target positions map to the same I-addresses as source positions — is not derivable from any foundation. This puts A5 in the same position as A4a, which the ASN correctly labels "specification requirement — not a derived property." A5 is presented as an established fact ("satisfies") without the same caveat.
**Required**: Label A5 as a specification requirement, matching A4a's treatment. Update the properties table accordingly.

### Issue 3: A4a uses set equality instead of permutation
**ASN-0030, "REARRANGE"**: "(c) {Σ'.V(d)(p) : 1 ≤ p ≤ n_d} = {Σ.V(d)(p) : 1 ≤ p ≤ n_d}"
**Problem**: Set equality is strictly weaker than permutation. Consider V-space `[a, a, b]` → `[a, b, b]`: same set `{a, b}`, same length 3, but the multiplicity of `a` decreased and `b` increased. This satisfies (b)+(c) but is not a permutation — it has silently duplicated one I-address reference and dropped another. For this ASN's reachability analysis, set equality suffices (reachable iff in the set). But A4a is labeled "specification requirement" for a future REARRANGE ASN, and a non-permutation REARRANGE would be a bug. The requirement should be tight enough to prevent it.
**Required**: Strengthen (c) to assert the V-space is a permutation of its pre-state: `(E π : π is a bijection [1..n_d] → [1..n_d] : (A p : Σ'.V(d)(p) = Σ.V(d)(π(p))))`. Alternatively, use multiset equality.

### Issue 4: A7 wp derivation contradicts A8
**ASN-0030, "Link Integrity"**: "This precondition holds permanently. At link creation, endset I-addresses were obtained from some document's V-space (the link's source content must exist to be linked). By P2 (ReferentiallyComplete, ASN-0026), those I-addresses are in dom(Σ.I)."
**Problem**: Two paragraphs later, A8 states: "A link may reference an address `a` where `a ∉ dom(Σ.I)`." The wp derivation claims the precondition `(A a ∈ endset(L) : a ∈ dom(Σ.I))` "holds permanently" by arguing all endset addresses originate from V-space. A8 explicitly permits endset addresses that are ghost (not in dom(Σ.I)). The formal statement of A7 is correctly scoped — it conditions on "whose endset addresses are in dom(Σ.I)" — but the prose derivation asserts universal permanence of the precondition, which is false for ghost links.
**Required**: Revise the wp derivation to acknowledge the two cases: (1) for links whose endsets were drawn from V-space, the precondition holds permanently (as argued); (2) for ghost links (A8), the precondition does not hold until the ghost addresses are allocated, at which point A7 applies from that state onward. The formal statement A7 is fine; the prose must match it.

### Issue 5: `endset(L)` used without definition
**ASN-0030, "Link Integrity"**: "A link L connects endsets — each endset is a set of I-address spans."
**Problem**: Properties A7, A7a, A7b, and A8 all quantify over `a ∈ endset(L)`, where `a` is an individual I-address. But `endset(L)` is described as "a set of I-address spans" — i.e., a set of (start, length) pairs. The ASN never defines how to go from spans to the set of individual addresses. The intended meaning is presumably `endset(L) = ∪{[s, s⊕l) : (s,l) ∈ from(L) ∪ to(L) ∪ type(L)}`, using T12 (SpanWellDefined) to unfold each span into an address set. Without this definition, the formal properties are ambiguous — does `a ∈ endset(L)` range over addresses in any of the three endsets, or over addresses in one specific endset?
**Required**: Define `endset(L)` explicitly as the set of I-addresses covered by all spans across all three endsets (or define per-endset projections if the distinction matters). The definition should reference T12 for span-to-address-set conversion.

### Issue 6: Transition (f) is composite, not single-step
**ASN-0030, "The Accessibility Partition"**: "(f) (iii) → (ii): permitted — allocation without V-space insertion"
**Problem**: No single operation achieves (iii)→(ii). INSERT allocates fresh I-addresses and places them in V-space simultaneously (P9-new and the V-space postconditions are a single atomic operation). The ASN's explanation confirms this is two steps: "INSERT creates fresh I-addresses... but then immediately deleted from V-space." That is (iii)→(i)→(ii), not (iii)→(ii). The transition table presents six transitions as if they are of the same kind, but (f) requires two operations while (a)-(e) are single-operation transitions. This conflation is misleading.
**Required**: Either (a) clarify that A3 classifies reachable state-pairs, not single-step transitions, and note that (f) requires a two-operation sequence; or (b) remove (f) from the transition table and note it as a consequence of (a) followed by (b).

### Issue 7: Ghost permanence claim lacks justification
**ASN-0030, "The Ghost Domain"**: "Ghost addresses at intermediate positions — between existing allocations — remain ghosts permanently. T9 (ForwardAllocation, ASN-0001) guarantees that new allocations occur only at the frontier."
**Problem**: T9 says allocations within a single allocator's stream are strictly monotonically increasing. This prevents a *specific* allocator from backtracking. But T10a (AllocatorDiscipline) allows an allocator to spawn child allocators via `inc(·, k')` with `k' > 0`, which creates a new tumbler extending the parent's prefix. The argument needs to show that no child or sibling allocator can produce an address that lands on a ghost position between existing allocations. The one-line appeal to T9 is insufficient — the interaction between sibling streams and child spawning must be addressed.
**Required**: Provide a multi-step argument: (1) sibling allocations via `inc(·, 0)` increment the last significant position, so they cannot produce an address between two already-allocated siblings; (2) child allocations via `inc(·, k')` produce strictly longer tumblers, which by T1 (LexicographicOrder) and the prefix ordering extension fall within the parent's subtree, not at intermediate sibling positions. Together these establish that ghost addresses between allocations are permanent.

## OUT_OF_SCOPE

### Topic 1: Formal specification of DELETE, COPY, REARRANGE, PUBLISH
**Why out of scope**: ASN-0026 defines INSERT fully (P9) but gives only classification-level properties for the other operations (+_ext, P7). Full pre/post/frame specifications for DELETE, COPY, REARRANGE, and PUBLISH are needed but belong in dedicated ASNs. This ASN correctly works with what the foundations provide and labels gaps as specification requirements (A4a, and A5 once corrected).

### Topic 2: Historical backtrack for recovering truly unreferenced content
**Why out of scope**: The ASN correctly identifies that transition (ii)→(i) is not achievable for truly unreferenced content by any currently defined operation, and explicitly defers the historical trace mechanism to future work. The invariants are stated in a way that is compatible with a future recovery operation (no A0 violation needed).

### Topic 3: Per-endset resolvability
**Why out of scope**: A7b defines resolvability as "at least one endpoint I-address is reachable in d." Whether a link requires both its from-endset and to-endset to be reachable for useful operation is a link semantics question, not an address permanence question. A future links ASN should define granular resolvability predicates.

VERDICT: REVISE
