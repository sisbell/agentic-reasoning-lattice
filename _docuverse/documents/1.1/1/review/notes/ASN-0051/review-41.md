# Review of ASN-0051

## REVISE

### Issue 1: NoStaleResolutionState relies on un-enumerated transition inspection
**ASN-0051, "Schema closure (NoStaleResolutionState)" paragraph (under Endset Projection)**: "direct inspection of each transition's effect (ASN-0047) confirms this; there is consequently no operation that *could* establish a stale V-position field"
**Problem**: The architectural claim is load-bearing for the downstream freshness conclusion ("The resolution is always *fresh* — computed from the current state, with no creation-time arrangement participating"). The proof references inspection of all 8 elementary transitions but does not perform it. The reader must independently verify that none of K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ writes a V-address into Σ.L. Operational closure is the *only* foundation for the schema-precludes-stale-cache argument and warrants explicit per-transition verification.
**Required**: Enumerate the per-transition check, one line each. E.g.: "K.α modifies C only; K.δ modifies E and seeds M(d_new)=∅; K.λ writes Σ.L(a_new) = (F, G, Θ) which by L3 carries spans over T with no V-fields; K.μ⁺/K.μ⁺_L/K.μ⁻/K.μ~ modify M only; K.ρ modifies R only."

### Issue 2: SV6 sub-lemma — implicit T1 index bound at j ≤ #(s⊕ℓ)
**ASN-0051, SV6 sub-lemma proof, "Divergence is upward" paragraph**: "the first divergence of t and s ⊕ ℓ is at position j with tⱼ > sⱼ = (s ⊕ ℓ)ⱼ. By T1(i), t > s ⊕ ℓ"
**Problem**: T1(i) requires both tumblers to have a component at the divergence position j. The proof verifies `#t ≥ j` for t explicitly via prefix exclusion. The symmetric check `j ≤ #(s⊕ℓ) = #ℓ` for s⊕ℓ is not stated. The verification chains from `j < k = actionPoint(ℓ) ≤ #ℓ` (ActionPoint codomain, ASN-0034) and the TumblerAdd result-length identity `#(s⊕ℓ) = #ℓ`, but is left implicit. The same implicit step recurs when t is compared with s in the prefix-exclusion sub-argument.
**Required**: Add one sentence: "Since k = actionPoint(ℓ) ≤ #ℓ (ActionPoint codomain bound) and `#(s⊕ℓ) = #ℓ` (TA0 result-length), j < k gives j < #(s⊕ℓ), so position j is within range for s⊕ℓ as well."

### Issue 3: SV11 worked example exhibits only mechanism (b) of the strictness biconditional
**ASN-0051, "Two-span, non-injective scenario"**: "The fragment count is 2 — strictly less than the non-empty-term count (4) and the m · p upper bound (4) — because adjacency within blocks merges term-level contiguous regions, while non-injective sharing introduces no new fragments..."
**Problem**: The SV11 biconditional explicitly names two mechanisms for strictness of m·p: (a) some decomposition term is empty, and (b) two non-empty terms within a single block are ordinally adjacent or overlap. The two-span example exhibits only mechanism (b) — all four terms are non-empty, and adjacency drives the coalescing. Mechanism (a) — a span whose denotation is disjoint from some block's I-extent, yielding an empty term across that block — is described in prose but not demonstrated concretely. Per the "boundary cases mandatory" standard, both regimes of an explicit two-mechanism strictness claim should be exercised against concrete tumbler values.
**Required**: Add a small scenario exhibiting mechanism (a). E.g., extend the two-span endset to three spans, where the third span's reach lies in an interval disjoint from both block I-extents (perhaps spanning a coverage region between a₅ and some later sibling not present in M(d)). Verify that the third span contributes empty terms `⟦(s₃, ℓ₃)⟧ ∩ I(β_k) = ∅` for both k, dropping the non-empty-term count from m·p = 6 to 4 while leaving the fragment count at the same 2 the example already shows. This isolates mechanism (a) from mechanism (b) operationally.

### Issue 4: SV11 maximal-fragment count proof — the upper bound on fragment-per-term assumed without statement
**ASN-0051, SV11 biconditional proof, "(⇒) Suppose the maximal-fragment count equals m · p"**: "The fragment count is bounded above by the non-empty-term count (each non-empty term lies inside some maximal fragment within its block, so distinct fragments arise from distinct or non-coalescing terms)"
**Problem**: The parenthetical asserts that each non-empty term lies inside a single maximal fragment within its block — equivalently, that a single term cannot span two distinct maximal fragments. This is true because each term is contiguous in the block's ordinal sequence (S0 convexity, established earlier in the same section) and a maximal fragment is itself a maximal contiguous region — so a contiguous set lies in exactly one maximal contiguous region. But the proof does not cite the convexity result it is relying on; the reader must connect the parenthetical back to the S0-contiguity paragraph that immediately follows.
**Required**: Cite the contiguity result at the point of use: "(each non-empty term is contiguous within its block by the S0-convexity argument below, hence lies in exactly one maximal fragment within its block)".

## OUT_OF_SCOPE

### Topic 1: Broader-level span survivability (k ≤ p₃)
**Why out of scope**: The ASN explicitly scope-excludes broader-level spans in the "Note on scope — what k ≤ p₃ permits" passage and the "Scope — broader-level spans are admitted but not formally characterised here" note in the Content Allocation section. SV6 covers element-level spans (k > p₃) only. Treatment of broader-level spans — including the open-by-design coverage-growth structure for cross-document/account/node spans — is deferred to ASN-0034's allocator and address-hierarchy machinery.

### Topic 2: Higher-arity links (|Σ.L(a)| > 3)
**Why out of scope**: The ASN's scoping note explicitly works within the standard-triple framework: "treatment of those additional endset slots is deferred to ASN-0043". The generalization to N > 3 is noted as slot-wise application of the same machinery.

### Topic 3: Link-subspace contribution to projection in SV11
**Why out of scope**: SV11 focuses on the text-subspace projection π_text. The full π(e, d) admits link-subspace contributions when M(d) contains link-subspace V-positions (via K.μ⁺_L), including reflexive addressing through L13. The ASN explicitly defers these to "the Link Subspace ASN".

### Topic 4: Dormant link revival and version-fork bilateral vitality preservation
**Why out of scope**: The ASN's Open Questions section explicitly identifies these as future work: "Must the system provide a mechanism to transition a dormant link (vital in no document) back to vitality...?" and "Under what conditions must bilateral vitality be preserved across a fork..."

### Topic 5: Discovery latency and consistency guarantees
**Why out of scope**: The Open Questions section: "What must the system guarantee about discovery latency — must newly created links be discoverable immediately, or is eventual consistency permitted?" — this is implementation policy, not foundation-level survivability.

VERDICT: REVISE
