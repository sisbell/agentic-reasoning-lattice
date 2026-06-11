# Review of ASN-0112

I verified the central constructions by hand: the T12 legality argument (D0 via the two-case divergence bound), both covering cases of V2 (D1 round-trip closure for `#origin_d ≤ #reach_d`; the TumblerSub/TumblerAdd computation showing `reach_d ≺ r⋆` for `#origin_d > #reach_d`), the V5 prefix-pinning and boundary-discreteness steps, the V6 witness `w⋆ = [s_C,1,…,1,n_C+1]`, the V3 tightness via `sig(w) = #w` from S8a + TA5-SIG, the V18 case exhaustiveness over `{K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~}`, and all three worked-example computations (`[2,2] ⊖ [1,1] = [1,2]`, `[1,4] ⊖ [1,1] = [0,3]`, and the depth-divergent `r⋆ = [2,2,0]` overshoot). All check out, including the subtle points: the V6 dichotomy correctly refuses to rest on bare `⊊` (the `origin_d.0` zero-extension makes the inclusion strict even in the exact-cover case), and the V5 proof correctly observes that D-CTG★ cannot close the half-open boundary cell. The wp analyses are non-trivial and both directions are discharged. What remains are three smaller defects.

## REVISE

### Issue 1: Quotation attributed to Nelson without citation, in non-verbatim form
**ASN-0112, "The origin is permanent; the extent tracks quantity, not order" (V9)**: "Nelson distinguishes *arrangement* (order) from *composition* (quantity): 'changing how content is arranged → extent unchanged; changing how much content there is → extent changes.'"
**Problem**: Every other Nelson attribution in this ASN carries a pin-cite (4/68, 4/24, 4/25, 4/11, 4/19, 4/9, 4/65). This one has none, and the arrow notation inside the quotation marks is plainly not verbatim source text — it reads as the authors' own gloss dressed as a quote. The same paragraph's closing attribution, "Nelson's classification of rearrangement as a 'Pure Vstream operation,'" is likewise uncited. In a specification whose claims are systematically grounded in cited evidence, an unverifiable quotation is a defect: the reader cannot tell whether V9's arrangement/composition distinction is Nelson's commitment or the ASN's interpolation.
**Required**: Either supply the pin-cites for both quoted fragments, or drop the quotation marks and state the distinction as the ASN's own reading (the V9 proof itself — span depends on `O(d)` alone, never on the values `M(d)(v)` — stands without Nelson's authority, so the paraphrase form costs nothing).

### Issue 2: V12 attributes the emptiness decision to `σ_d`, which does not exist in the empty case
**ASN-0112, "What the caller learns beyond the name" and Claims table V12**: "`σ_d` decides emptiness (`RETRIEVEDOCVSPAN(d) = ⟨⟩ ⟺ O(d) = ∅`, V11)"
**Problem**: By V0/V11, when `O(d) = ∅` the result is `⟨⟩` and there is no `σ_d` — `origin_d` is explicitly undefined. The value that discriminates emptiness is the returned *span-set* (presence vs. absence of a component span), not the span `σ_d`. As written, the claim's subject is a value that fails to exist in exactly the case the claim is about.
**Required**: Restate V12 (prose and table) with the span-set result as the subject: "the result of `RETRIEVEDOCVSPAN(d)` determines…", reserving `σ_d` for the non-empty facts (the occupied-count recovery in the single-subspace regime).

### Issue 3: Redundant recap of D-CTG★'s scope inside the V5 proof paragraph
**ASN-0112, "Single subspace: exact cover"**: "The restriction needs two steps, because D-CTG★ constrains only slice tuples lying between two members of `V_S(d)` — it is silent both on the half-open boundary cell … and on depth-`m_s` tumblers that are not slice tuples…" followed, after steps (i)–(ii), by "D-CTG★ legitimately certifies only the sub-range `origin_d ≤ t ≤ max O(d)`; the cell beyond `max O(d)` is closed by (ii), not by contiguity."
**Problem**: These two sentences state the same scoping fact — contiguity does not reach the boundary cell — once before the proof and once after it, in different words. The second sentence adds nothing step (ii) did not just demonstrate; it is a defensive recap of the proof's own structure, the accretion pattern this note is flagged for.
**Required**: Keep one statement of D-CTG★'s scope (the opening one, which motivates the two-step structure) and delete the closing recap sentence.

## OUT_OF_SCOPE

### Topic 1: Exact (non-bounding-box) reporting of multi-subspace documents
**Why out of scope**: V6 proves a single span cannot trace a separated series; the exact per-subspace report is RETRIEVEDOCVSPANSET territory (ASN-0113), explicitly excluded by the scope list. The ASN correctly stops at the bounding-box characterization and parks the extent-vs-count question in Open Questions.

### Topic 2: Reports against designated historical versions
**Why out of scope**: The ASN queries the present arrangement only; faithfulness obligations for version-indexed reports (Open Question 3) require the version-comparison machinery excluded from this ASN's scope.

VERDICT: REVISE
