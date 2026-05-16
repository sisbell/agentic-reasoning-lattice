# Review of ASN-0051

## REVISE

### Issue 1: SV2 and SV3 statements cover π but proofs additionally establish locate
**ASN-0051, SV2 and SV3**: The formal statements quantify only over `π_Σ(e, d) ⊆ π_{Σ'}(e, d)` (SV2) and `π_{Σ'}(e, d) ⊆ π_Σ(e, d)` (SV3). The proofs then "additionally" derive locate-set monotonicity. SV5 by contrast carries both π and locate in its formal content (with locate transforming by ψ).
**Problem**: Asymmetry across SV2/SV3 (resolution-as-afterthought) vs SV5 (resolution-explicit). A reader who scans only the formal statements misses that locate is governed.
**Required**: Either expand SV2/SV3's formal statements to include the locate inclusion explicitly, or split each into two named claims (e.g., SV2-π / SV2-locate). Same treatment for SV3.

### Issue 2: SV6 sub-lemma elides a needed agreement step
**ASN-0051, SV6 sub-lemma**: The proof of "t cannot first diverge from s at any position j < k" derives `tⱼ > sⱼ` and `(s ⊕ ℓ)ⱼ = sⱼ`, then concludes "the first divergence of t and s ⊕ ℓ is at position j with tⱼ > sⱼ = (s ⊕ ℓ)ⱼ. By T1(i), t > s ⊕ ℓ".
**Problem**: T1(i) requires `(A i : 1 ≤ i < j : tᵢ = (s ⊕ ℓ)ᵢ)` for j to be a "first divergence" between t and s ⊕ ℓ. The proof relies on transitivity (t agrees with s on 1..j−1, and s ⊕ ℓ agrees with s on 1..k−1, j < k, so t agrees with s ⊕ ℓ on 1..j−1) without stating it.
**Required**: One sentence: "Since t agrees with s on positions 1..j−1 (first divergence at j) and s ⊕ ℓ agrees with s on positions 1..k−1 (TumblerAdd with k as action point), and j−1 < k−1, t agrees with s ⊕ ℓ on positions 1..j−1."

### Issue 3: SV6 precondition is embedded inside a paragraph
**ASN-0051, SV6 Precondition paragraph**: The precondition is stated as prose ("The action point k of ℓ must satisfy: for s with zeros(s) = 3, let p₃ denote the position of the third zero component in s; the precondition is k > p₃").
**Problem**: A multi-sentence narrative isn't a Precondition block. The conditions on s, b, and k are mixed with definitional asides (p₃ notation, equivalence reformulation) in a single paragraph. The reader cannot read off the SV6 precondition without untangling prose.
**Required**: Convert to a bullet/structured form: `s, b ∈ T`; `zeros(s) = 3 ∧ zeros(b) = 3`; `s, b T4-valid`; `origin(b) ≠ origin(s)`; `k > p₃` where `p₃ = ` position of third zero of s. The "equivalently, |{i ≤ k−1 : sᵢ = 0}| = 3" remark belongs in a separate sentence.

### Issue 4: Two-span worked example asserts "this is the maximally merged decomposition" without verifying merge condition fails between β₁ and β₂
**ASN-0051, Two-span non-injective scenario**: The example states β₁ = (v₁, a₁, 5) and β₂ = (v₆, a₂, 2) and asserts "The block boundary at v₅ → v₆ is enforced by a discontinuity in M(d)'s I-address sequence (a₅ → a₂ is not a +1 step), forcing M12's split rule."
**Problem**: For the maximally merged decomposition, one must check M7's merge condition for β₁ and β₂: V-adjacency requires v₆ = v₁ + 5; I-adjacency requires a₂ = a₁ + 5. The prose addresses I-adjacency by noting "a₅ → a₂ is not a +1 step", but the V-adjacency check is implicit (it would need v₆ to be the V-position immediately after v₅).
**Required**: One line verifying both adjacency checks fail (or one fails) so the merge condition cannot succeed. Or cite v₅ → v₆ as V-adjacent (v₆ = shift(v₅, 1)) but I-discontinuity blocks merge.

### Issue 5: SV13 part (e) statement on K.μ~ characterizes locate transformation but doesn't include in part (e)'s K.λ/frame coverage that K.μ⁺_L is a new-link path
**ASN-0051, SV13(e)**: The summary covers extension, contraction, reordering, isolation, then "K.α, K.δ, K.ρ, and K.λ all preserve M in their frame, so locate(e, d) is unchanged for every endset e that existed prior to the transition."
**Problem**: K.μ⁺_L is missing from this list. K.μ⁺_L *does* change M (adds a link-subspace mapping) — so it's not a frame-on-M transition. But the statement enumerates the M-frame cases distinct from the M-modifying cases. The list of M-frame transitions (K.α, K.δ, K.ρ, K.λ) is structurally separate from M-modifying transitions (K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~). SV13(e) handles K.μ⁺ and K.μ⁺_L in one bullet ("Extension of M(d) — whether K.μ⁺ ... or K.μ⁺_L ...") but the rest of the breakdown should be symmetric.
**Required**: Verify the M-frame list is complete. K.λ in particular is M-frame (frame condition `(A d' :: M'(d') = M(d'))`), and the wp analysis treats it correctly. The body claim is sound; only the SV13 summary risks misreading. Either explicitly state "K.μ⁺_L is the link-subspace path of extension" within the extension bullet's caption, or note its placement relative to the M-frame list.

### Issue 6: SV11's "exactly m · p decomposition terms" claim states a count of terms-as-formula-positions, not distinct sets
**ASN-0051, SV11(a)**: "The union is over *exactly* m · p decomposition terms (one per (span, block) pair), some possibly empty."
**Problem**: When two distinct (j₁, k) and (j₂, k) yield the same decomposition term as a set (e.g., two spans whose intersections with the same block coincide), the set-theoretic count of distinct decomposition terms is < m · p, even though the formula has m · p index positions. The text's "exactly m · p" refers to *indexed* terms, not distinct sets. This is the natural reading, but the contrast with SV11(b)'s "at most m · p maximal fragments" invites confusion: both bounds are formally upper bounds on counts but measure different things.
**Required**: One clarifying sentence: "Here 'exactly m · p decomposition terms' counts (span, block)-indexed positions in the Cartesian product, not distinct subsets of π_text(e, d); two terms may coincide as sets."

## OUT_OF_SCOPE

### Topic 1: Higher-arity links (N > 3)
**Why out of scope**: The scoping note explicitly defers arity-N treatment to ASN-0043 / future link-model work. The standard-triple framework is sufficient for SV2–SV13 as stated.

### Topic 2: Same-origin coverage growth formal characterization
**Why out of scope**: The same-origin discussion explicitly defers formal conditions to ASN-0034's allocator-discipline treatment. The descriptive content here motivates SV6's element-level scope without committing to which allocator regimes close which spans.

### Topic 3: Broader-level spans (k ≤ p₃)
**Why out of scope**: The SV6 scope note explicitly defers broader-level spans to ASN-0034's address-hierarchy treatment. udanax-green's restriction to element-level spans is correctly cited as supporting context.

### Topic 4: Link-subspace projection / endsets referencing link addresses (L13 ReflexiveAddressing)
**Why out of scope**: The "Distinct architectural roles" note and SV11's text-subspace scoping defer link-subspace projection to a future "Link Subspace ASN". The reflexive-addressing strictness analysis for SV2 is properly deferred.

### Topic 5: Discovery latency / eventual consistency
**Why out of scope**: Implementation-level concern about when newly created links become discoverable in distributed deployments. Belongs to inter-server protocol territory, not foundational invariants.

### Topic 6: Fork (J4 composite) bilateral vitality conditions
**Why out of scope**: TransclusionCouplingAbsence corollary touches fork; detailed bilateral-vitality preservation analysis across J4 belongs to a fork-semantics ASN.

### Topic 7: Fragment ordering within a partially-surviving endset
**Why out of scope**: The fragments inherit ordinal ordering within blocks from M1 (OrderPreservation, ASN-0058) and block-to-block ordering from V-position ordering. A separate canonical-ordering invariant for clients to rely on is reasonable future-ASN territory.

VERDICT: REVISE
