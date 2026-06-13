# Review of ASN-0123

This is an unusually careful note. The operation is *derived* from its guarantees (G1–G3) rather than asserted-then-checked; the proofs show their work (VN-B1's four-case K.δ analysis, V9's two-branch severance argument, SA's antichain proof); boundary cases are handled (empty source via `n = 0`, iterated forks via V6, shared content via the image-set `A`, links-only source via the content-subspace restriction); invariant preservation is routed cleanly through V-WF → ExtendedReachableStateInvariants; and the implementation deviations are identified against the abstract requirement rather than excused. I verified the load-bearing proofs (SA, VN-B1, V8 coverer-equality, V9 severance, the J1★/J1'★ discharge, the PS coverage induction) and they hold. I found one issue.

## REVISE

### Issue 1: V1's consequence gloss overstates content-volume independence

**ASN-0123, V1 (ZeroContentFootprint)**: "consequently its entire state delta is independent of content volume: ΔE = {v}; ΔM is one arrangement function whose every image is a pre-existing address; ΔR = A × {v} with |A| ≤ n."

**Problem**: The topic sentence is contradicted by its own elaboration. `M'(v) = M(d_src)|_{V_{s_C}(d_src)}` is a function on `dom(M'(v)) = V_{s_C}(d_src)`, which has `n` entries; and `ΔR = A × {v}` has `|A| ≤ n` pairs. Both scale with the number of content positions in the source — i.e., with content volume. The clause "`ΔR = A × {v} with |A| ≤ n`" *states* this dependence in the same breath as the claim of independence. What is genuinely content-volume-independent is narrower: the count of newly **allocated** content/link addresses (zero, `C' = C ∧ L' = L`) and the new-identity count (one, `ΔE = {v}`).

The implementation-evidence reading — "V→I entries and DOCISPAN entries scale with the source's span count, never its byte volume" — is a *representation-level* property (the block/run decomposition of M11/M12), and it depends on V2's representation invariance to apply. It is not a property of the abstract state delta, where `M'(v)` has one entry per V-position. So the gloss conflates two distinct things: (a) "no content-volume-proportional **allocation** (unlike the naive copy)," which is true and is the operation's real content; and (b) "the entire state delta is independent of content volume," which is false at the abstract level and only becomes "independent of byte volume" at the representation level.

The formal statement `C' = C ∧ L' = L` is correct and is unaffected.

**Required**: Narrow the gloss to what holds — e.g., "the fork allocates zero content/link addresses and exactly one identity, regardless of source size; the arrangement `M'(v)` and the provenance delta `A × {v}` scale with the source's content-position count, and the implementation's *block* representation reduces this storage to span count (never byte volume) by V2's representation invariance." Drop "entire state delta is independent of content volume," or restate it as "no allocated substance, independent of source size."

## OUT_OF_SCOPE

### Topic 1: cross-owner identity allocation mechanics
**Why out of scope**: The cross-owner branch mints `v` in the forker's own document namespace — document creation from scratch (CREATENEWDOCUMENT). V-WF correctly gestures at the mechanism ("account document sub-allocator, k = 2 descent or k = 0 sibling") and imports the three postconditions (`Document(v)`, `v ∉ E`, `pfx(π') ≼ v`), which suffice for V9/V9w. The precondition discharge (parent ∈ E via PS, freshness at the document frontier) is verifiable from what is given; the precise frontier formula belongs to ASN-0103. This is correctly deferred, not a gap.

### Topic 2: concurrent-fork serialization
**Why out of scope**: V5's fork-counting and V0's same-namespace distinctness lean on B-Seq (serialized commits), and the atomicity remark openly notes a genuine interior state. The ASN flags the serialization guarantee for concurrent forks of one source as an explicit Open Question — appropriately, since it is new territory, not an error here.

META: not applicable — the note specifies abstract state (the VERSION composite), an operation, and its invariants V0–V13, with the implementation treated as evidence and its deviations measured against the spec; it has not drifted into implementation mechanics.

VERDICT: REVISE
