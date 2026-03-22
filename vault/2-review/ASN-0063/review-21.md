# Review of ASN-0063

## REVISE

### Issue 1: CL0 — Element-level tightness proof incomplete for I-addresses
**ASN-0063, CL0 proof (after CL1)**: "Between consecutive ordinal increments a_β + k and a_β + (k + 1), the only tumbler of depth #a_β in the half-open interval is a_β + k itself — the integer constraint at the last component forces t_{#a_β} = (a_β)_{#a_β} + k."
**Problem**: CL0's formal statement claims element-level tightness: "whose element-level members are exactly the image." The proof of this claim for I-addresses gives only the last-component constraint. The prefix-matching step — that any depth-#a_β tumbler t in [a_β + k, a_β + (k+1)) must agree with a_β + k on components 1 through #a_β − 1 — is needed but unstated. The identical argument IS shown in full for V-positions earlier in CL0 (if t differs at position j < #v_β, then t falls outside the interval by T1(i)). The I-address case requires the same two-step argument: first establish the prefix matches, then invoke the integer gap at the last component.
**Required**: State the prefix-matching step for I-addresses. A brief note acknowledging the symmetric structure suffices — the cases are structurally identical — but the current text gives only half the argument for the I-address case.

### Issue 2: Cross-origin span disjointness — "T10 gives disjointness directly" oversimplifies
**ASN-0063, resolve definition**: "For incomparable origins (where neither document prefix is a prefix of the other), T10 (PartitionIndependence, ASN-0034) gives disjointness directly."
**Problem**: T10 establishes that individual tumblers under incomparable prefixes are distinct (a ≠ b). CL0 I-span disjointness requires the stronger claim that the *span denotations* — sets of all tumblers in half-open intervals — are disjoint. This requires an ordering argument: if origins diverge at position k with p₁_k < p₂_k, then every tumbler in [a₁, reach₁) has value p₁_k at position k (since start and reach agree at k, any tumbler in between must also agree by T1), and every tumbler in [a₂, reach₂) has value p₂_k at position k, so the intervals are separated. This is a short argument but it is not "directly" from T10 — T10 gives point disjointness, not interval disjointness.
**Required**: Add 2–3 sentences making the ordering argument explicit for incomparable origins, paralleling the comparable-origins argument that follows it.

### Issue 3: K.μ~ fixity proof — intermediate-state notation
**ASN-0063, S3★ analysis, Link-subspace fixity**: "K.μ⁺ (amended) neither adds nor modifies link-subspace positions — its frame preserves pre-existing mappings `(A v : v ∈ dom(M(d)) : M'(d)(v) = M(d)(v))`"
**Problem**: In the K.μ~ decomposition (K.μ⁻ + K.μ⁺), K.μ⁺ operates on the intermediate state M_int(d), not the original state M(d). Its frame preserves mappings relative to M_int(d): `(A v : v ∈ dom(M_int(d)) : M'(d)(v) = M_int(d)(v))`. The chain to the original state requires an intermediate step: M_int(d)(v) = M(d)(v) for link-subspace v (from K.μ⁻ preserving values and r = 0). The conclusion M'(d)(v) = M(d)(v) is correct, but the cited frame condition conflates the original and intermediate states.
**Required**: Write the frame relative to M_int, then chain: since r = 0 and K.μ⁻ preserves values, M_int(d)|_{dom_L} = M(d)|_{dom_L}, giving M'(d)|_{dom_L} = M(d)|_{dom_L}.

### Issue 4: K.μ⁺_L — misleading parenthetical
**ASN-0063, K.μ⁺_L precondition**: "ℓ ∈ dom(L)  (the target link must already exist — K.λ must precede this step)"
**Problem**: The formal precondition `ℓ ∈ dom(L)` is correct. The parenthetical "K.λ must precede this step" is accurate in that K.λ is the only transition that adds to dom(L), but a reader will naturally interpret it as "K.λ must immediately precede this step in the same composite." K.μ⁺_L is an elementary transition usable in any composite where ℓ ∈ dom(L) — it can reference a link created in a prior composite, not just one created by K.λ in the current composite. This matters for the link inheritance discussion and for standalone K.μ⁺_L usage.
**Required**: Rephrase: "the target link must already exist in dom(L) — placed there by some prior K.λ."

### Issue 5: VSpanImage definition — "gaps" conflicts with D-CTG
**ASN-0063, VSpanImage definition**: "V-positions outside dom(M(d)) — gaps from prior content removal — contribute nothing to the image."
**Problem**: D-CTG (VContiguity, ASN-0036) ensures that within each subspace, V-positions form a contiguous ordinal range with no gaps. The phrase "gaps from prior content removal" suggests interior holes in the V-position range, which D-CTG prevents. V-positions outside dom(M(d)) in the span's range are those *beyond* the current contiguous range, not gaps within it.
**Required**: Replace "gaps from prior content removal" with "positions beyond the current arrangement range."

## OUT_OF_SCOPE

### Topic 1: Efficient discovery evaluation
**Why out of scope**: The ASN correctly defines disc as a derived function on system state and defers data-structure concerns to implementation. Sub-linear evaluation is an engineering requirement, not an abstract specification property.

### Topic 2: Concurrent CREATELINK
**Why out of scope**: The ASN correctly lists this in open questions. The transition framework is sequential; concurrent link allocation semantics require a separate concurrency model.

### Topic 3: Link inheritance under forking
**Why out of scope**: Explicitly deferred. The ASN establishes that J4 (fork) does not copy link-subspace mappings and notes that a link inheritance mechanism would require K.μ⁺_L steps in the fork composite.

### Topic 4: Link withdrawal invariants
**Why out of scope**: Explicitly deferred. The ASN identifies the constraint landscape (D-CTG restricts contraction to suffix truncation, K.μ~ cannot reorder link-subspace positions) but defers the precise withdrawal mechanism to future work.

VERDICT: REVISE
