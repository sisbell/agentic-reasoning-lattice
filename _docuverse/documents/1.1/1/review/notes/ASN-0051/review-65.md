# Review of ASN-0051

## REVISE

### Issue 1: Construction-pattern generalisation lacks rigor for higher (m, p)

**ASN-0051, SV11 "Generalisation to (m ≥ 5, p ≥ 3) and (m ≥ 3, p ≥ 4)"**: "We mark `(m ≥ 5, p ≥ 3)` and `(m ≥ 3, p ≥ 4)` as *witnessed in this ASN via the construction-pattern generalisation* of the (m = 3, p = 3) and (m = 4, p = 3) witnesses above; the procedure is mechanical..."

**Problem**: Attainment at infinitely many (m, p) configurations is asserted from two explicit anchors plus a procedural description. The description tells the reader how to construct witnesses but does not constitute a proof. The pattern, while clear to the careful reader, is exactly the kind of "by similar reasoning" Dijkstra would refuse to accept — the m=3 and m=4 anchors differ in how many nested odd-offset elements appear (5,7,9,11 vs 5,7,9,11,...) and the larger-block offset shifts are not explicitly characterized.

**Required**: Either (a) give explicit constructions for a few more anchor points (e.g., (m=5, p=3), (m=3, p=4)) and an inductive argument lifting from (m, p) to (m+1, p) and (m, p+1), or (b) prove attainment by induction on (m+p), giving the inductive step's witness construction explicitly with the offset shifts spelled out parametrically. The current procedural prose is detailed but informal.

### Issue 2: Pigeonhole sub-case analysis in SV11 disjoint-pair case (b) at m=2

**ASN-0051, SV11 "Pigeonhole on the boundary set {e_i, e_{i+1}}"**: Three separate m=2 sub-cases enumerate every distribution pattern of B_1, B_2 ⊆ {e_i, e_{i+1}}.

**Problem**: The three m=2 sub-cases (both ⊇ {e_i, e_{i+1}}; shared boundary element with at least one proper; disjoint at {e_i} vs {e_{i+1}}) cover the same conclusion (coalescence) by the same mechanism (overlap or adjacency at the boundary set). The case enumeration is correct but redundant; an integrated argument over "any two non-empty subsets of a 2-element set either share an element or are ordinally adjacent singletons" would discharge all three at once.

**Required**: Consolidate the three m=2 sub-cases into a single argument that observes: B_1 and B_2 are non-empty subsets of {e_i, e_{i+1}}; either they share an element (overlap at that element, coalesce) or they are the two singletons {e_i} and {e_{i+1}} (ordinally adjacent at offsets h, h+1 in β_{k₁}, coalesce by mechanism (b)). Then the m≥3 case follows by pigeonhole as already stated.

### Issue 3: SV13(e) K.δ caveat under-covers the new-document case

**ASN-0051, SV13(e)**: "K.α, K.δ, K.ρ, and K.λ all preserve M-values in their frame, so locate(e, d) is unchanged for every endset e and every pre-existing document d ∈ dom(Σ.M) carried over the transition."

**Problem**: The clause correctly handles pre-existing documents but does not state what `locate(e, d_new)` is for a newly-allocated d_new. The K.δ caveat paragraph below notes `locate_{Σ'}(e, d_new) = ∅` trivially, but this consequence belongs in the main clause, not as a remark. A reader who skips the caveat sees only "unchanged for pre-existing d" and may wonder whether the new document's locate is undefined or unspecified.

**Required**: Either fold the empty-locate claim for d_new into the main bullet — "K.δ additionally introduces d_new with `locate(e, d_new) = ∅` for every endset e, by definition of locate on the empty arrangement" — or add a parallel clause covering newly-introduced state slots, similar to how NewLinkEvaluationDefinedness is given its own corollary for K.λ.

### Issue 4: SV6 narrative gloss conflates origin-of-address with origin-of-allocator

**ASN-0051, SV6 "Note on framing"**: The note clarifies that SV6 holds for any T4-valid element-level b with `origin(b) ≠ origin(s)` regardless of allocation status. Good. But the surrounding prose throughout the "Content Allocation and Coverage Stability" section freely uses "different origin" both for (i) tumblers with different origin field decompositions and (ii) addresses produced by different allocators.

**Problem**: The structural origin function `origin(t) = N(t).0.U(t).0.D(t)` projects from a tumbler's components alone; it has nothing to do with which allocator emitted t. T10a.4 ensures conformant allocators produce T4-valid outputs, and S7d ties documents to allocators, but the cross-origin exclusion SV6 is purely structural. The "same-origin coverage growth" subsection then discusses allocator-discipline-dependent growth without flagging the conceptual shift from structural origin to allocator identity.

**Required**: In the "Content Allocation and Coverage Stability" section, distinguish explicitly between "addresses with the same structural origin field" (a T4-projection fact) and "addresses produced by the same allocator" (a T10a-discipline fact). These coincide under S7d but the SV6 proof relies only on the structural reading. Make this explicit so readers don't conclude SV6 depends on T10a's allocator semantics.

### Issue 5: Prose drift in "After reordering" admissibility argument

**ASN-0051, Worked Example "After reordering"**: "The minimal removal set covering ψ's altered V↦I assignments is {v₂, v₃}, which is *not* an upward tail of {v₁, v₂, v₃, v₄}. The composite is realised instead by removing the upward tail {v₂, v₃, v₄} at cut n' = 1..."

**Problem**: The argument states K.μ~ is realised by a *specific* K.μ⁻ + K.μ⁺ decomposition (the one that removes the upward tail covering {v₂, v₃}). But ASN-0047's K.μ~ "distinguished composite" reading is silent on whether any specific decomposition is canonical — only that *some* K.μ⁻ + K.μ⁺ pair must realise the reordering. The ASN should either cite ASN-0047 for the existence interpretation explicitly or note that the choice of decomposition is non-canonical (multiple decompositions yield the same K.μ~ effect).

**Required**: Add a sentence at the first admissibility check (Step 1) clarifying: "ASN-0047 reads K.μ~ as the *existence* of some K.μ⁻ + K.μ⁺ decomposition; we exhibit one such decomposition to discharge enabling, without claiming canonical choice." This clarification need not be repeated at every subsequent admissibility check.

## OUT_OF_SCOPE

None to flag. The ASN explicitly defers several topics that are appropriately out of scope:
- Same-origin coverage growth (formal SV claim deferred to ASN-0034 allocator discipline) — correctly handled as descriptive
- Broader-level spans (k ≤ p₃) survivability — correctly deferred to ASN-0034
- Link-subspace projection contribution (endsets referencing link addresses) — correctly deferred to Link Subspace ASN
- Links with arity > 3 — correctly deferred to ASN-0043
- Link type semantics, replication protocol — explicitly scoped out

The Open Questions section captures additional deferred topics (fragment ordering, latency, vitality-restoration mechanisms, fork interactions) without prematurely fixing answers — appropriate.

VERDICT: REVISE
