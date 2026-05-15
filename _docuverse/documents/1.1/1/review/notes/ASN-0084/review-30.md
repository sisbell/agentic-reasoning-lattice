# Review of ASN-0084

## REVISE

### Issue 1: R-WP invariant list incomplete
**ASN-0084, R-WP section**: Q lists "S0, S1, S2, S3, S7a, S7b, S7c, D-CTG, D-MIN, S8a, S8b, S8-fin, S8-depth"

**Problem**: Missing S4 (OriginBasedIdentity), S5 (UnrestrictedSharing), S7d (DocumentAllocationDiscipline), S9 (TwoStreamSeparation), and D-SEQ (SequentialPositions) from ASN-0036. The earlier "Invariant preservation" paragraph claims "Every ASN-0036 invariant is therefore maintained" but the R-WP enumeration is incomplete, and the prose discharge ("C' = C... carries over S0, S1, S7a, S7b, S7c") explicitly lists only five invariants for the content-store branch — missing S4, S5, S7d, S9 from that route as well.

**Required**: Either enumerate all relevant invariants and verify each, or explicitly explain which are auto-preserved and how — e.g., S4 by C' = C and address-structure invariance, S5 as existence-of-witness-state (preserved trivially), S7d as a discipline on the allocation history (independent of M), S9 by C' = C (dual of S0), D-SEQ as derived from D-CTG + D-MIN + S8-fin + S8-depth.

### Issue 2: Naming clash for "S8a"
**ASN-0084, Invariant preservation paragraph and R-WP section**: "S8a" is used in two distinct senses.

**Problem**: ASN-0036's S8a is the VPositionWellFormedness *predicate*. The Invariant preservation paragraph uses S8a in this sense: "D-CTG, D-MIN, S8-fin, S8a, S8-depth." But R-WP then writes "S8a, S8b via B' = R-BLK(B)... we verify both S8 clauses on the construction" — using S8a/S8b to refer to clauses (a) and (b) of S8 (SpanDecomposition). The same label means two different things within the same ASN.

**Required**: Disambiguate. Use "S8(a), S8(b)" for the SpanDecomposition clauses and reserve "S8a" exclusively for VPositionWellFormedness, matching ASN-0036's nomenclature.

### Issue 3: Non-S subspace handling implicit throughout R-BLK, R-WP, R-DISP
**ASN-0084, R-BLK Phase 1–3, R-DISP, R-WP S8 verification**: All three lemmas focus exclusively on V_S(d) but quantify (explicitly or implicitly) over dom(M(d)).

**Problem**: The partition B from S8 (ASN-0036) covers dom(M(d)) including non-S subspace positions (e.g., V_2(d) for links). The R-BLK Phase 1–3 description never states that non-S runs in B pass through to B' unchanged — a reader must infer this from R-FRAME-P/S. R-DISP's "for all v₁, v₂ in the same region" quantifies over {exterior, α, μ, β} ⊆ V_S(d), saying nothing about non-S positions where π is also the identity (Δ = 0). R-WP's S8 verification reads: "π is a bijection on V_S(d)... so the V-extents of B' are pairwise disjoint and cover V_S(d). Hence for each v ∈ V_S(d), exactly one run in B' contains v." But S8(a) quantifies over dom(M(d)) — the verification covers only V_S(d).

**Required**: Add an explicit clause at each site. In R-BLK: "Non-S subspace runs from B are unchanged in B' by R-FRAME-P/S(a)." In R-DISP: extend the region partition to include "non-S" as a fifth region with Δ = 0, or restrict the quantification to V_S(d). In R-WP S8 verification: "For v ∈ dom(M(d)) with subspace(v) ≠ S, the containing run in B is unchanged in B' (frame), so S8(a)/(b) for v carries over from the pre-state."

### Issue 4: Signed-magnitude lifted ordering unused
**ASN-0084, PermutationDisplacement definition**: "we lift the natural ordering on ℕ to the signed-magnitude carrier as `−m < 0 < +n`"

**Problem**: The lifted ordering is defined but never invoked by any subsequent lemma or proof. R-DISP, R-PPERM, R-SPERM, R-BLK all compare Δ-values only by equality (as the next sentence in the ASN itself acknowledges: "we lift... `−m < 0 < +n`... The lemmas that consume Δ... compare Δ-values only by equality, never by summation."). The lifted ordering is dead weight in the definition.

**Required**: Either consume the ordering somewhere (e.g., to characterize the structural symmetry of forward/backward displacements informally referenced) or remove the lift for parsimony.

### Issue 5: R-COMM precondition citation could be explicit per case
**ASN-0084, R-COMM proof**: Each case (3-cut α, 3-cut β, 4-cut α, 4-cut μ, 4-cut β) computes v + k = c_i + (j' + k) and applies R-PPERM/R-SPERM at the new offset.

**Problem**: R-PPERM/R-SPERM's formulas apply only when the offset lies in the correct range (0 ≤ j' + k < region width). The R-COMM precondition "v and v + k lie in the same region" supplies this bound, but the proof never cites the precondition per case to justify why j' + k stays within the region. A reader has to infer that the precondition implies the offset bound for the R-PPERM/R-SPERM formula to apply legally.

**Required**: Add one sentence at the start of each case: "By the R-COMM precondition, v + k lies in α [resp. β, μ], so j' + k < w_α [resp. w_β, w_μ], and R-PPERM's [R-SPERM's] formula applies at offset j' + k."

## OUT_OF_SCOPE

### Topic 1: Documents with text-subspace depth m_1 > 2
The ASN restricts to documents where the text subspace has been initialized at the minimum permitted depth m_1 = 2. ASN-0036's ValidFirstInsertionPosition only requires m_s ≥ 2, so documents with m_1 ∈ {3, 4, ...} are admissible by the strand model but explicitly excluded from this ASN's scope. This is disclosed in the State and Vocabulary section. Generalizing the cut-point framework to higher depths (where ordinals become multi-dimensional under D-SEQ) is a natural follow-on but not part of this ASN. The Open Questions section currently does not mention this restriction.

### Topic 2: Cross-subspace and cross-document REARRANGE
The ASN confines REARRANGE to a single document's text subspace. Cross-subspace transposition (e.g., between text and link subspaces) and cross-document REARRANGE are excluded by frame conditions R-FRAME-P/S(b) and the subspace confinement consequence of R-PRE. These would be distinct primitives requiring separate analysis.

### Topic 3: Composition of REARRANGE operations
Already flagged in the Open Questions section. Whether the composition of two REARRANGEs is always expressible as a single REARRANGE, and the algebraic structure of the resulting permutation class, are not addressed here.

### Topic 4: Effect of REARRANGE on link endsets
ASN-0036 introduces link content in subspace 2. REARRANGE preserves the link subspace pointwise (frame condition). Links reference I-addresses, so links remain valid across REARRANGE by S0 (content immutability). The interaction between REARRANGE and link discoverability/integrity is not analyzed here but follows from the frame condition combined with link endset semantics in future ASNs.

### Topic 5: k-cut generalizations for k > 4
Already flagged in the Open Questions section. The class of permutations expressible by cut-point rearrangements with more than four cuts, and whether the displacement-uniformity property continues to hold, are deferred.

VERDICT: REVISE
