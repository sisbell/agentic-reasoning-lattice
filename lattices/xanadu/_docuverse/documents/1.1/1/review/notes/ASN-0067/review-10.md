# Review of ASN-0067

## REVISE

### Issue 1: Block decomposition scoped to text subspace while insertion position is unrestricted

**ASN-0067, Phase 2 — Mutation**: "Let B be the maximally merged block decomposition of M(d) in state Σ (M11, M12, ASN-0058)."

**Problem**: ASN-0058 defines block decomposition for "the text-subspace arrangement of document d" — B1 carries the guard `v₁ ≥ 1`. The COPY definition, however, places no restriction on the subspace identifier S = v₁. When S = 0 (link subspace), B contains no link-subspace blocks, so B_S = ∅ and B_post = ∅. Existing link-subspace positions are then neither shifted (they are absent from B_post) nor preserved by the non-target frame (which covers `subspace(p) ≠ S`, i.e. only text subspace when S = 0). The result is a definitional gap: M'(d) at existing link-subspace positions is undefined, and placing new content at v could overlap with them, violating S2.

For S ≥ 1 the issue does not arise — B covers all text subspaces, B_S extracts the target, and link-subspace positions are covered by the non-target frame because `0 ≠ S`.

**Required**: Either add `v₁ ≥ 1` (text subspace) to the COPY preconditions, or scope B to the target subspace explicitly: "Let B be the maximally merged block decomposition of `{(v, M(d)(v)) : v ∈ dom(M(d)) ∧ v₁ = S}`." The first fix is simpler and aligns with COPY's role (content placement, not link creation). The second is more general but requires noting that C1a's extension of M11/M12 applies to any subspace restriction.

### Issue 2: S8a preservation proof assumes text subspace

**ASN-0067, C3 — InvariantPreservation, S8a**: "new V-positions in the γⱼ blocks have the form v + offset, where v satisfies S8a ... Since v has all positive components (zeros(v) = 0), the shifted position also has all positive components."

**Problem**: S8a is guarded by `v₁ ≥ 1`. When S = 0, the insertion position v has v₁ = 0, so `zeros(v) ≠ 0` and the claim "v has all positive components" is false. S8a is still preserved — new positions with v₁ = 0 fall outside S8a's guard, and all text-subspace positions (in B_other) are unchanged — but the proof argument is incorrect for this case. The same gap applies to the "Shifted post-block V-positions satisfy S8a by the same component-preservation argument" sentence.

**Required**: If Issue 1 is fixed by restricting S ≥ 1, this issue vanishes (v₁ ≥ 1 guarantees all positive components). If S = 0 is to remain valid, add: "For S ≥ 1: v has all positive components by S8a, and ordinal shift preserves this. For S = 0: new positions have v₁ = 0, falling outside S8a's guard; S8a is preserved because no text-subspace position is added or modified."

## OUT_OF_SCOPE

### Topic 1: Concurrent COPY semantics
**Why out of scope**: The ASN correctly identifies (C13, Observation — Concurrency) that ValidComposite provides sequential correctness only. Serialization guarantees for concurrent COPY operations targeting the same document require a concurrency model not present in the foundation.

### Topic 2: Time-fixed vs location-fixed transclusion
**Why out of scope**: The COPY definition operates on the current arrangement M(d_s) at the time of resolution. Whether the placed content tracks the source's subsequent edits (location-fixed) or is pinned to a snapshot (time-fixed) requires version semantics, which this ASN does not introduce.

VERDICT: REVISE
