# Review of ASN-0051

## REVISE

### Issue 1: K.μ~ composite admissibility not addressed in "After reordering" subsection

**ASN-0051, Worked Example, "After reordering"**: "From the post-removal state, a K.μ~ step swaps v₂ and v₃: M''(d)(v₂) = a₄, M''(d)(v₃) = a₂..."

**Problem**: The K.μ~ swap of v₂ and v₃ requires the K.μ⁻ stage to remove an upward tail containing both — minimally {v₂, v₃, v₄} (the upward tail at cut v₁), since {v₂, v₃} alone is not D-SEQ-admissible. The subsequent subsection "Reordering that changes locate" explicitly addresses this with "The composite is realised instead by the full V_{s_C}(d)-removal...", but this earlier swap doesn't carry the same admissibility note. Readers may wonder whether the swap is admissible at all.

**Required**: Add a brief admissibility note for the v₂↔v₃ swap, paralleling the treatment in the later subsection, or cross-reference forward.

### Issue 2: Construction-pattern generalisations lack at least one explicit higher-(m, p) witness

**ASN-0051, SV11 attainment witnesses**: "We mark `(m ≥ 4, p ≥ 3)` and `(m ≥ 3, p ≥ 4)` as *witnessed in this ASN via the construction-pattern generalisation* of the (m = 3, p = 3) witness above; the procedure is mechanical and yields a concrete (B, e) for every such (m, p) under the block-size threshold `min_k n_k ≥ 2m − 1`."

**Problem**: The procedural recipe is sound, but no explicit instance is constructed beyond (m=3, p=3). Standard 6 requires concrete examples for key claims. The witness sequence reaches the boundary cases (m=2, p=2), (m=3, p=2), (m=2, p=3), (m=3, p=3), but a single explicit instance at (m=4, p=3) or (m=3, p=4) would anchor the generalisation and make the procedure's correctness verifiable rather than only describable.

**Required**: Construct one explicit higher-(m, p) witness — e.g., (m=4, p=3) — showing the I-extents, V-positions, decomposition terms, and within-block non-adjacency checks, paralleling the (m=3, p=3) presentation.

### Issue 3: Consumer note conflicts with SV13(h)'s use of BilateralVitality

**ASN-0051, Endset Projection section, "Consumer note"**: "Consumer note — bilateral vitality has no internal use in this ASN. The SV claims below state per-side vitality conditions directly..."

**Problem**: SV13(h) uses the BilateralVitality predicate by name: "(the bilateral-vitality predicate read at Σ, per the Endset Projection section's definition)". The Consumer note's claim of "no internal use" is therefore inaccurate — (h) is internal to this ASN and does invoke the predicate symbolically.

**Required**: Either reword the Consumer note to "bilateral vitality is exposed for downstream consumers; SV13(h) is the only internal site that names it explicitly" or drop the claim of no internal use.

### Issue 4: Architectural remark's per-transition check doesn't explicitly cover K.μ~ as composite

**ASN-0051, NoStaleResolutionState, point (iii)**: "K.μ⁺, K.μ⁺_L, K.μ⁻, and K.μ~ modify M only..."

**Problem**: K.μ~ is a distinguished composite, not an elementary transition. The per-transition check should clarify whether the property is verified directly on K.μ~ or inherited from its K.μ⁻ + K.μ⁺ expansion. The inheritance is sound (both stages modify M only, so the composite does), but stating it explicitly avoids the reader having to reconstruct the argument.

**Required**: Add a parenthetical note that K.μ~ inherits M-only modification from its elementary stages, mirroring the elementary/composite distinction noted elsewhere in the ASN.

## OUT_OF_SCOPE

### Topic 1: Per-arena resolution of identical V-coordinate tuples across documents

**Why out of scope**: The CrossDocumentDecoupling witness notes V-positions live in disjoint per-document arenas (the `v₁ = [s_C, 1]` used for d₂ in Step 3 is distinct from d₁'s `v₁`). A more comprehensive treatment of V-position identity across documents (whether tuples are shared or per-document) belongs in the Arrangement Operations ASN, not here.

### Topic 2: Cryptographic content integrity at endset addresses

**Why out of scope**: ContentFidelity is established as an architectural guarantee from S0. Cryptographic verification (hashes, signatures) is explicitly noted as out of scope ("Nelson explicitly acknowledges this is contractual trust, not mathematical proof of non-tampering [LM 5/17–18]"). Belongs in a security/integrity ASN if pursued.

### Topic 3: Broader-level span survivability (k ≤ p₃)

**Why out of scope**: The ASN explicitly defers this to ASN-0034's address-hierarchy treatment, noting that broader-level spans are admitted by L4 but their cross-prefix coverage behaviour is governed by allocator-discipline conditions outside this ASN's scope.

VERDICT: REVISE
