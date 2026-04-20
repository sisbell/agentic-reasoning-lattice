# Review of ASN-0027

## REVISE

### Issue 1: Invariant preservation unverified for A3, A4, A5

**ASN-0027, DELETE section**: "P0 is preserved (I-space unchanged), P1 is preserved (dom(Σ.I) unchanged), P2 is preserved on the surviving V-space"

**Problem**: The ASN checks P0, P1, P2, P7 for DELETE (A2) but performs no corresponding verification for REARRANGE (A3), COPY (A4), or CREATENEWVERSION (A5). P2 (referential completeness) is non-trivial for COPY — the target's new positions must map to I-addresses in `dom(Σ'.I)`, which requires chaining P2 on the source through the I-space frame. For REARRANGE, the argument passes through range preservation. For CREATENEWVERSION, it passes through the identity mapping. Each is a short derivation but none appears.

**Required**: For each of A3, A4, A5, state and derive P2 preservation. Two to three sentences each. For A4: "The identity clause maps new positions to `Σ.V(d_s)(p_s + j) ∈ dom(Σ.I)` by P2 on `d_s` in the pre-state. The I-space frame gives `dom(Σ'.I) = dom(Σ.I)`. Shifted positions retain their original I-addresses, also in `dom(Σ.I)`. P2 holds." Similar for A3 (range preservation implies surviving I-addresses unchanged) and A5 (new document maps to I-addresses from source, valid by P2 on source).

### Issue 2: Cross-document frame missing from A4 and A5

**ASN-0027, A4**: "Frame (source): `Σ'.V(d_s) = Σ.V(d_s)` (when `d_s ≠ d_t`)"

**Problem**: A4 states the source frame but not the general cross-document frame. Documents `d' ≠ d_t` other than `d_s` are not covered. A2 states the full frame explicitly; A3 references P7; A4 and A5 do neither. A5 states only "Frame (original): `Σ'.V(d) = Σ.V(d)`" — one document, not all of `Σ.D`. The omission matters because the Permanence Summary appeals to cross-document frames for all operations, and A7's proof chains through the cross-document frame of COPY.

**Required**: Add the general cross-document frame. For A4: `(A d' : d' ∈ Σ.D ∧ d' ≠ d_t : Σ'.V(d') = Σ.V(d'))`. The source frame follows as a special case. For A5: `(A d' : d' ∈ Σ.D : Σ'.V(d') = Σ.V(d'))` — CREATENEWVERSION has no write target among existing documents, so all of `Σ.D` is unchanged.

### Issue 3: A3 swap bijection asserted without verification

**ASN-0027, A3**: "for swap, the three moving segments' images are three disjoint intervals covering `[c_1, c_4)`"

**Problem**: The pivot bijection is straightforward (two complementary intervals), but the swap case involves three segments with different-sized shifts. The formulas are stated, but the claim that images are disjoint and covering requires computing the image ranges. This takes 3–4 lines and is not shown.

**Required**: Compute image ranges from the formulas. B maps `[c_3, c_4)` to `[c_1, c_1 + L_B)`; M maps `[c_2, c_3)` to `[c_1 + L_B, c_1 + L_B + L_M)`; A maps `[c_1, c_2)` to `[c_1 + L_B + L_M, c_4)`. Each starts where the previous ends; together they cover `[c_1, c_4)` with `L_B + L_M + L_A = c_4 - c_1`.

### Issue 4: A8(iii) redundant with (i) and (ii)

**ASN-0027, A8**: "(iii) Any reference expressed as I-address `a` resolves to content by evaluating `Σ_n.I(a)`"

**Problem**: Property (iii) follows trivially from (i): if `a ∈ dom(Σ_n.I)`, then `Σ_n.I(a)` is defined. The word "resolves" suggests system-level retrieval, but the proof establishes only that the mathematical function is defined — it says nothing about how a user reaches this content through the RETRIEVE interface (which requires V-space reachability). As stated, (iii) is either redundant (function evaluation) or misleading (implies accessibility that A9 then shows is not guaranteed).

**Required**: Either drop (iii) or replace it with a precise statement distinguishing I-space resolution (always possible, by (i) + (ii)) from V-space retrieval (requires `reachable(a)`). The distinction is exactly the three-layer separation the ASN opened with.

## OUT_OF_SCOPE

### Topic 1: MAKELINK classification in A1

A1 classifies "each primitive operation" but lists five, omitting MAKELINK. If MAKELINK creates I-space entries (link data) or modifies V-space, it should appear in the I-space frame classification.

**Why out of scope**: MAKELINK is not yet specified in the foundations. A1's scope is the operations defined by ASN-0001 and ASN-0026.

### Topic 2: Document lifecycle under total deletion

A2 permits `k = n_d`, yielding `|Σ'.V(d)| = 0`. Whether `d` remains in `Σ'.D` (empty but extant) or is removed is unspecified. This affects the quantifier domain in A9's proof (iteration over `D_a`) and the reachability analysis.

**Why out of scope**: Document set membership rules are not yet addressed in the foundations.

VERDICT: REVISE
