# Review of ASN-0047

## REVISE

### Issue 1: S3 does not necessitate J0 — cross-layer narrative misstates the logical dependency

**ASN-0047, Temporal decomposition**: "S3 (referential integrity, ASN-0036: `ran(M(d)) ⊆ dom(C)`) bridges the presentational and existential layers — every V-position must reference allocated content, making it the load-bearing constraint that necessitates J0's coupling."

**Problem**: S3 constrains the M→C direction (arrangements must reference allocated content). J0 constrains the C→M direction (allocated content must appear in some arrangement). These are independent. A system can satisfy S3 while permitting orphan content — K.α extends dom(C), and if no K.μ⁺ follows, S3 is trivially preserved because no new M entry was added and dom(C) only grew.

The parallel with "P4 necessitates J1" is formally grounded: the wp derivation in the J1 section explicitly shows K.μ⁺ alone cannot maintain P4, forcing J1. No corresponding derivation exists for S3→J0, because S3 is maintained by K.μ⁺'s referential integrity precondition alone — K.α's behavior is irrelevant to S3.

J0's actual necessity comes from P7a (provenance coverage). Without J0, freshly allocated content might never enter any arrangement; J1 would never trigger provenance recording for it; P7a would fail. The causal chain is: P7a needs (for fresh a) some d with (a, d) ∈ R′, which needs J1, which needs a ∈ ran(M′(d)) for some d, which needs J0.

**Required**: Replace the S3→J0 claim with the correct dependency. S3 bridges the layers (arrangements reference content) but does not necessitate J0. J0 is necessitated by P7a through the J0→J1→provenance chain. This also means S3 and P4 are not structurally parallel in how they relate to coupling constraints — P4 directly necessitates J1 (by wp), while S3 has no analogous relationship to J0.

## OUT_OF_SCOPE

### Topic 1: J0 permits placement outside the origin document

J0 requires freshly allocated content to appear in *some* arrangement but does not constrain *which* document. Content allocated under d₁'s prefix (S7a) could be placed only in d₂'s arrangement, satisfying J0 while origin(a) = d₁ ≠ d₂. The expected constraint — fresh content appears in the origin document — is an operation-level property (INSERT always targets the editing document), not a transition-model invariant.

**Why out of scope**: Named operations and their specifications are explicitly excluded.

VERDICT: REVISE
