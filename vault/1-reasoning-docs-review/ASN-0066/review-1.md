# Review of ASN-0066

## REVISE

### Issue 1: Cross-references to non-foundation ASN-0047
**ASN-0066, Arrangement Contiguity paragraph**: "not a reachable-state invariant in the ASN-0047 sense", "beyond ASN-0047's validity predicate", "M₀(d) = ∅ by InitialState, ASN-0047", "a valid elementary transition under ASN-0047"
**Problem**: ASN-0047 is not a foundation ASN. The classification of D-CTG (design constraint vs. reachable-state invariant), the base case verification, and the justification for why D-CTG is not universally preserved all depend on ASN-0047 machinery. Standard 7 requires self-containment except for foundation references.
**Required**: Restate the needed concepts self-containedly. The base case can be derived from ASN-0036 alone (if no operations have occurred, dom(M(d)) = ∅ for all d). The design-constraint distinction can be made by observing that removing a single interior V-position breaks contiguity, so not all arrangement modifications preserve D-CTG — only well-formed editing operations that restore contiguity after structural changes.

### Issue 2: Undefined notation K.μ⁻
**ASN-0066, Arrangement Contiguity paragraph**: "bare K.μ⁻ — a valid elementary transition under ASN-0047"
**Problem**: K.μ⁻ is not defined in this ASN or any foundation. The reader cannot evaluate the claim that this transition violates D-CTG without importing ASN-0047 wholesale.
**Required**: Either define the concept inline (a single-position removal from the arrangement) or restate the argument without the notation: "Removing a single interior V-position from dom(M(d)) violates D-CTG, since the positions on either side of the removed position are no longer contiguous."

### Issue 3: DELETE preservation claimed without proof
**ASN-0066, Arrangement Contiguity paragraph**: "We treat D-CTG as a precondition that DELETE both assumes and preserves."
**Problem**: This reads as a claim that DELETE preserves D-CTG, but no proof is given. The immediately following sentence defers INSERT, COPY, and REARRANGE as "separate verification obligation" — yet DELETE is singled out as already resolved. If DELETE preservation is proved elsewhere, the ASN should say so and cite the foundation. If it is not yet proved, the phrasing should be parallel with the other operations: a verification obligation, not a settled fact.
**Required**: Either prove DELETE preservation here (showing that removing a contiguous range and shifting subsequent positions down produces a contiguous result), or uniformly defer all operations: "Whether DELETE, INSERT, COPY, and REARRANGE preserve D-CTG is a verification obligation for each operation's ASN."

### Issue 4: Depth > 2 consequences not derived
**ASN-0066, Arrangement Contiguity paragraph**: "For the standard text subspace at depth m = 2, this is a finite condition"
**Problem**: D-CTG is stated for arbitrary depth, but only depth 2 is analyzed. At depth m ≥ 3, D-CTG combined with S8-fin and S8a collapses to a much stronger restriction: all positions in V_S(d) must share components 2 through m−1 and differ only in the last component. To see why: if V_S(d) contained [S, 1, 5] and [S, 2, 1], the intermediates would include [S, 1, 6], [S, 1, 7], ... — infinitely many, violating S8-fin. Even if finiteness weren't the issue, the intermediate [S, 2, 0] has a zero component, violating S8a. So at depth ≥ 3, D-CTG effectively forces a single-ordinal-sequence structure, identical in character to depth 2. This is a non-trivial derived consequence that the ASN should state.
**Required**: Add a derived observation: at depth m ≥ 3, D-CTG combined with S8-fin and S8a forces all positions in a non-empty V_S(d) to share components 2 through m−1, so contiguity reduces to contiguity of the last component alone. Alternatively, restrict D-CTG to depth 2 explicitly if that is the intended scope.

### Issue 5: No concrete verification example
**ASN-0066**: The ASN gives an informal illustration ("If positions [1, 3] and [1, 7] are occupied…") but does not verify D-CTG against a specific document state.
**Problem**: Standard 6 requires a concrete example verifying the key property against a specific scenario.
**Required**: Provide at least one non-trivial state. For example: "Document d with M(d) = {[1,1] ↦ a₁, [1,2] ↦ a₂, [1,3] ↦ a₃}. Then V₁(d) = {[1,1], [1,2], [1,3]}. Check D-CTG: the only pair requiring intermediate verification is ([1,1], [1,3]), and the sole intermediate [1,2] is in V₁(d). ✓" Then show a violation: "If we removed [1,2] to get V₁(d) = {[1,1], [1,3]}, then [1,2] is an intermediate between [1,1] and [1,3] that is absent — D-CTG is violated." Trivial, but it exercises the formal statement.

### Issue 6: Starting-position constraint absent
**ASN-0066, opening paragraph**: Nelson: "if you have 100 bytes, you have addresses 1 through 100"
**Problem**: Nelson's statement specifies both contiguity AND starting position (addresses start at 1). D-CTG formalizes contiguity but not the starting point — a contiguous block starting at [S, 42] satisfies D-CTG. If the design intent is "positions are 1 through n," the formalization is incomplete. If the starting position is intentionally left unspecified (determined by the allocation mechanism), the ASN should say so explicitly to avoid the impression that D-CTG fully captures Nelson's statement.
**Required**: Either add a companion constraint fixing the minimum V-position (e.g., "the minimum element of a non-empty V_S(d) is [S, 1]"), or state explicitly that starting position is outside D-CTG's scope and will be addressed by operation-level specifications.

## OUT_OF_SCOPE

### Topic 1: Link-subspace contiguity
D-CTG applies to all subspaces including S = 0 (link subspace), but the ASN only discusses text-subspace implications. Whether link-subspace V-positions have the same contiguity requirements is a separate design question.
**Why out of scope**: The link subspace has different structural properties (S8a explicitly excludes it), so its contiguity analysis belongs in a link-subspace ASN.

### Topic 2: INSERT / COPY / REARRANGE preservation of D-CTG
The ASN explicitly defers these as "separate verification obligation for each operation's ASN."
**Why out of scope**: Correctly scoped — each operation ASN should prove its own preservation.

VERDICT: REVISE
