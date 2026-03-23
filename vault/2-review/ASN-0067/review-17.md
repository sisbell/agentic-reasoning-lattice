# Review of ASN-0067

## REVISE

*No issues identified.*

The proofs are explicit, each invariant conjunct from ExtendedReachableStateInvariants is individually addressed, boundary cases (empty document, insert-at-first, insert-at-last) are covered by the Case 1/Case 2 elementary decomposition split, and the worked example is arithmetically correct.

Specific verifications performed:

- **Elementary decomposition intermediate preconditions.** K.μ⁻ at Σ₀ produces a D-CTG/D-MIN-satisfying intermediate state (the range [v₀, v) or ∅ is contiguous). K.μ⁺ at Σ₁ satisfies strict extension (w ≥ 1 guarantees new V-positions), S8a (ordinal shift preserves positivity and zero-count), the K.μ⁺ amendment (all new V-positions have subspace s_C), and produces a D-CTG/D-MIN-satisfying result. The K.μ⁻ amendment's per-subspace requirement is met because only B_S entries are removed; link-subspace positions are untouched.

- **B' well-formedness.** B2 (disjointness) holds across all four groups: B_pre reaches ≤ v, placed blocks in [v, v+w), shifted B_post starts ≥ v+w, and B_other differs at component 1. Within-group disjointness is inherited (B_pre, B_post from the original decomposition; placed blocks by consecutive non-overlapping construction; shifted blocks by TS2 injectivity). B1 (coverage) and B3 (consistency) verified by tracing through each group.

- **Coupling constraints.** J0 vacuous (dom(C') \ dom(C) = ∅). J1/J1' hold by the explicit provenance extension. J1★/J1'★ coincide with J1/J1' because COPY creates only content-subspace V-positions (P.7), link-subspace V-positions map to dom(L) by S3★, and dom(C) ∩ dom(L) = ∅ by L14.

- **L' = L.** The elementary decomposition uses K.μ⁻, K.μ⁺, K.ρ — none of which have L in their effect. L12 (LinkImmutability) and P3★ confirm L can only grow and only through K.λ.

- **Worked example arithmetic.** Split at c = 2 verified: shift([1,1], 2) = [1,3] = v. Shift by w = 2 verified: [1,3] + 2 = [1,5], [1,4] + 2 = [1,6]. I-adjacency checks for maximally-merged verification: blocks 3 and 4 share origin 1.0.1.0.1 but I-reach 1.0.1.0.1.0.1.4 ≠ I-start 1.0.1.0.1.0.1.7.

- **Self-transclusion (C11).** Resolution in pre-state is a structural consequence of the composite transition definition (Phase 1 reads, Phase 2 writes). After self-transclusion, duplicate I-address occurrences cannot merge by M14 (ASN-0058): the merge condition requires a = a + n, which fails for n ≥ 1 by TA-strict.

## OUT_OF_SCOPE

### Topic 1: Link discoverability after COPY
**Why out of scope**: When content referenced by links is placed in a new document via COPY, the same I-addresses now appear in a new arrangement. How link traversal discovers the new occurrence is a link-semantics question — the ASN correctly confines itself to preserving existing link invariants (L0–L14, CL-OWN) rather than defining discovery behaviour.

### Topic 2: Interaction between COPY and version DAG
**Why out of scope**: The ASN operates on a single version's arrangement. Whether a COPY triggers version creation, and how the version DAG records the relationship between pre-COPY and post-COPY states, is version-creation territory.

VERDICT: CONVERGED
