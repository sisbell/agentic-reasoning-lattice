# Review of ASN-0110

## REVISE

### Issue 1: Result multiplicity — RE-exact contradicts the latitude granted in the RE-anon discussion

**ASN-0110, RE-exact vs. the RE-anon discussion**: RE-exact states `resultᵢ(I, Σ) = Eᵢ(I, Σ)`, where `Eᵢ` is a **set** of endset values, and asserts this leaves "an implementation no latitude in *which* endsets to report." But the discussion under RE-anon says "an implementation of `retrieveendsets` is free to collapse or preserve multiplicities — so multiplicity is not part of the guaranteed semantics."

**Problem**: These conflict. If `resultᵢ` is a set (RE-exact, set equality), duplicates are structurally impossible and there is *no* latitude to "preserve multiplicities." If an implementation may "preserve multiplicities" (return the same endset value once per contributing link), then `resultᵢ` is a multiset/sequence and `resultᵢ = Eᵢ` cannot be read as literal equality. The ASN never fixes whether the returned per-role object is a set, a multiset, or a sequence, so the two claims cannot both stand as written.

**Required**: Fix the return type. State explicitly that the guaranteed object is the *set* `Eᵢ` (so RE-exact is literal and there is no multiplicity latitude), and reword the RE-anon discussion accordingly — or, if a sequence/multiset presentation is intended, restate RE-exact as underlying-set equality and define the multiplicity contract. (Compare F10's explicit "unique strictly T1-increasing presentation" in ASN-0099, which pins the shape unambiguously.)

### Issue 2: The operation is defined over arbitrary `I ⊆ T` but never shown to be realizable/decidable

**ASN-0110, RE-touch / RE-overlap / RE-result**: RE-touch takes the query region as "an I-region `I ⊆ T` — a set of I-addresses," with no constraint on its representation. The only computational characterization offered, RE-overlap, applies *only* "When `I` is itself a span denotation `⟦(q, m)⟧`."

**Problem**: For an arbitrary (possibly infinite, non-span) `I ⊆ T`, the test `coverage(e) ∩ I ≠ ∅` is not reduced to anything decidable — RE-overlap does not apply, and the ASN gives no other handle. The note repeatedly calls this "the operation" and a "pure query," yet never establishes that the search terminates or that the touching test is decidable. The analogous foundation operations do discharge this: ASN-0086's CoverageEqualityDecidable and ASN-0099's F4 remark ("decidable because `F̂` is finite and each per-span membership test is decidable by T2"). This ASN silently omits the parallel argument while inheriting the same `coverage ∩ I` shape.

**Required**: Either constrain the query region's representation (e.g., a finite span-set, as the foundations do) and connect RE-overlap to a termination/decidability statement over the finite store (`L-fin`, finite endsets, per-span overlap decidable by T2), or explicitly carry the decidability lemma. As written, "operation" is not discharged — the general definition has no realizable test.

### Issue 3: Empty query region (`I = ∅`) not addressed on the I-side

**ASN-0110, RE-empty and RE-Vside**: RE-empty discusses an empty *result* for a non-empty region (it requires `I ≠ ∅` for the recovery construction), and RE-Vside notes the V-side `image` can be empty ("finds nothing"). The I-side input `I = ∅` is never stated.

**Problem**: `I = ∅` is a reachable boundary — precisely the I-side image of a fully-deleted V-region (RE-Vside). The semantics handle it trivially (`touches(e, ∅)` is false for all `e`, so the result is `⟨∅, …, ∅⟩` of length `N_max(Σ)`, not the empty tuple), but the ASN never says so, and a reader could plausibly expect an empty tuple. Boundary cases (empty/zero) are mandatory.

**Required**: Add one line fixing the `I = ∅` case on the I-side and confirming the tuple length is still `N_max(Σ)` (consistent with RE-arity), so the V-side "finds nothing" reduction has an explicit I-side referent.

## OUT_OF_SCOPE

### Topic 1: The V-space presentation contract for partially-arranged endsets
The ASN correctly defers (final paragraph and Open Questions) the precise lossy contract for presenting a returned endset back in a querying document's V-coordinates. This is genuinely a separate projection, appropriately left to future work — not an error here.

VERDICT: REVISE
