# Review of ASN-0058

I read through the ASN three times, checking every proof step, every boundary case, and every foundation citation. This is a substantial piece of work — the mapping block algebra, the canonical decomposition uniqueness proof, and the content reference resolution machinery are all developed with care.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Operation effects on block decompositions
How INSERT, DELETE, COPY, and REARRANGE interact with the block decomposition — splitting existing blocks, creating new ones, maintaining B1–B3 through transitions. The ASN establishes the static algebra; the dynamics are the natural next layer.
**Why out of scope**: Explicitly excluded; requires its own ASN defining pre/postconditions per operation.

### Topic 2: Enfilade representation of the POOM
The ASN works with abstract block decompositions. The tree-structured enfilade that implements them (composable width properties, bottom crums, spanfilade coalescing) is an implementation concern.
**Why out of scope**: The ASN correctly separates the abstract algebra from its representation; the enfilade is a data structure choice, not a system guarantee.

### Topic 3: Content reference placement
The ASN defines content references and resolution (extracting I-address runs from a source document), but does not define how resolved content is placed into a target document's arrangement. That placement operation would need to establish new blocks in the target's decomposition, allocate V-positions, and maintain all invariants.
**Why out of scope**: Placement is an operation on arrangements, which is explicitly out of scope.

---

**Detailed notes on what I checked:**

**M0–M1 (WidthCoupling, OrderPreservation).** The injectivity argument via T3 at the last component is correct. The strict ordering via T1(i) follows. The v+0=v convention is cleanly stated in M-aux and doesn't conflict with OrdinalShift (which is undefined, not differently defined, at n=0).

**M-aux (Associativity).** TS3 covers c,j ≥ 1; the convention handles the zero cases. All four quadrants (both zero, one zero, neither zero) are accounted for.

**M5 (SplitPartition).** The substitution k = c + j via M-aux correctly shows the union covers [0, n). The disjointness follows from the integer ranges [0, c) and [c, n). Clean.

**M6(d) (Origin traceability).** The claim origin(a+k) = origin(a) is derived correctly: δ(k, #a) has action point #a, TumblerAdd copies all components before #a, and the document prefix N.0.U.0.D occupies positions strictly before #a (since the element field has δ ≥ 1 components by T4, giving α+β+γ+2 < α+β+γ+δ+3 = #a).

**M7 (MergeCondition).** Both necessity arguments are valid. V-adjacency without I-adjacency violates B3 at the boundary position. I-adjacency without V-adjacency leaves a V-gap the merged block would incorrectly claim to cover. The verification via M-aux is correct.

**M12 (CanonicalUniqueness).** This is the hardest proof in the ASN and I checked it in full detail:

- *Maximal run partition:* The left-extension condition (condition 2) correctly avoids TumblerSub by searching for a predecessor v' with v'+1=v. The finiteness of dom(f) guarantees termination.
- *Uniqueness of maximal runs:* If v ∈ R₁ ∩ R₂ with v₁ ≤ v₂, the contiguity argument (V-extents are contiguous ranges at fixed depth via S8-depth and ordinal shift structure) correctly establishes v₂ ∈ V(R₁). The left-extension contradiction at k₂ ≥ 1 is valid. The length equality follows from condition 3 applied symmetrically.
- *(⟹) direction:* Both cases (condition 3 fails, condition 2 fails) correctly derive a mergeable pair contradicting maximally merged. The argument that β' must start exactly at v+n (not before, by B2 disjointness; not after, by S8-depth and contiguity at depth m) is sound.
- *(⟸) direction:* The set of maximal runs cannot have a mergeable pair by condition 3 of the left run.
- The final step — every maximally merged decomposition equals the set of maximal runs, which is uniquely determined by f — is airtight.

**M16 (CrossOriginMergeImpossibility).** The proof that origin(a₁ + n₁) = origin(a₁) is correct by TumblerAdd's component-copying behavior. The contrapositive (different origins → different tumblers → no I-adjacency) is valid.

**C0 (OrdinalDisplacementNecessity).** The proof by contradiction is correct: if the action point k < m, the family w_j = [u₁,...,u_{m-1}, j] for j > u_m gives infinitely many depth-m tumblers in ⟦σ⟧ (each satisfying u < w_j < reach(σ), the latter because u_k < u_k + ℓ_k = reach(σ)_k makes the comparison resolve at component k regardless of j). This contradicts S8-fin.

**C0a (PrefixConfinement).** The contradiction argument is valid: if t disagrees with u at any j₀ < m, then t_{j₀} > u_{j₀} (from u ≤ t) and t_{j₀} > reach(σ)_{j₀} = u_{j₀} (from C0's action point being m), giving t > reach(σ). The depth bound #t ≥ m follows from the prefix case of T1(ii).

**C1a (RestrictionDecomposition).** The verification that f = M(d_s)|⟦σ⟧ satisfies S2, S8-fin, S8-depth is correct. The explicit B3 preservation argument under merge (case split for i < n₁ and n₁ ≤ i < n₁+n₂) is thorough.

**C2 (ResolutionWidthPreservation).** The enumeration of depth-m tumblers in [u, reach(σ)) as exactly {[u₁,...,u_{m-1}, j] : u_m ≤ j < u_m + ℓ_m} follows from C0a (prefix fixed) and S8-depth (only depth-m positions in dom). The cardinality ℓ_m follows. The partition sum via B1+B2+M0 is correct.

**Worked examples.** Both verify correctly against the definitions. The merge check in the main example correctly identifies the I-discontinuity at [1,14]→[1,40]. The content reference example correctly demonstrates restriction, decomposition, and C1/C2 verification.

**Foundation usage.** The ASN uses ASN-0034 (TumblerAdd, T1, T3, TS3, TA0, TA-strict, OrdinalShift, T0(a), S7), ASN-0036 (S2, S3, S5, S7, S8, S8-fin, S8-depth, S8a), and ASN-0053 (S4, S3, S6, T12, ⟦σ⟧) correctly and without reinventing their notation.

VERDICT: CONVERGED
