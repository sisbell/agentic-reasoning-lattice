# Review of ASN-0073

## REVISE

### Issue 1: Bare "+" on tumblers reinvents foundation notation
**ASN-0073, ValidInsertionPosition definition**: "v = min(V_S(d)) + j for some j with 0 ≤ j ≤ N"
**Problem**: The "+" operator on tumblers is not defined in the foundation. ASN-0034 defines `⊕` (TumblerAdd) and `shift(v, n)` (OrdinalShift). The preamble paragraph correctly uses `shift(v_j, 1)`, but the definition itself switches to bare `+`. Additionally, `shift` requires `n ≥ 1` (OrdinalShift definition), so the `j = 0` case — where `v = min(V_S(d))` — is not expressible as `shift(min, 0)`.
**Required**: Use `shift(min(V_S(d)), j)` for `j ≥ 1` and handle `j = 0` as the explicit case `v = min(V_S(d))`. Or define the shorthand `+` in terms of `shift`/`⊕` before using it. The statement registry entry must match.

### Issue 2: Characterization claimed but not established
**ASN-0073, preamble**: "the characterization of V-positions at which content may be placed in a document's arrangement while preserving D-CTG and D-MIN"
**Problem**: "Characterization" means necessary and sufficient. The ASN provides a definition — a set of positions — but proves neither direction:
- **Soundness**: inserting at a ValidInsertionPosition preserves D-CTG and D-MIN. Not argued.
- **Completeness**: inserting at any other position violates D-CTG or D-MIN. Not argued.

These are the central claims and they are entirely absent. The definition alone is just a predicate; calling it a "characterization" is a claim that requires proof.
**Required**: Either (a) remove the characterization claim — call this a definition, state that correctness will be verified when operations are defined, and drop the language about "preserving D-CTG and D-MIN" from the preamble; or (b) formalize the insertion model (at minimum: inserting at v shifts all positions ≥ v by one ordinal) and prove both directions.

### Issue 3: Insertion model is implicit but load-bearing
**ASN-0073, ValidInsertionPosition**: "N positions targeting existing content (which will be displaced)"
**Problem**: The parenthetical "(which will be displaced)" assumes a shift model — inserting at position v moves all existing positions ≥ v forward by one. But this model is never defined. The predicate's correctness depends on it: under pure addition (no displacement), only the append position `j = N` is valid; inserting at `j < N` would collide with an existing position, violating S2 (arrangement functionality). Under a shift model, all N+1 positions work. The predicate can't be validated without specifying which model is assumed.
**Required**: If the ASN is just a definition (per Issue 2 option (a)), remove the displacement claim. If it's a characterization (option (b)), define the displacement operation.

### Issue 4: N+1 count is wrong for the empty subspace
**ASN-0073, after definition**: "There are N + 1 valid insertion positions"
**Problem**: `N` is defined only in the non-empty case (`|V_S(d)| = N`). In the empty case, `N` is undefined. The remark reads as a universal claim, but in the empty case the valid position is `[S, 1, ..., 1]` for any depth `m ≥ 2` — infinitely many distinct tumblers (one per choice of `m`), since tumblers of different lengths are distinct by T3. The count "N+1 = 0+1 = 1" does not hold.
**Required**: Either restrict the N+1 claim to non-empty subspaces, or address the empty case separately. The empty case should note that depth `m` is a one-time choice (establishing S8-depth for the subspace), after which the position is unique — but this still isn't "1 position" in the tumbler-equality sense.

### Issue 5: No concrete example
**ASN-0073**: The entire ASN contains no worked example.
**Problem**: The review standards require verification against at least one specific scenario. For a predicate this simple, a concrete example would also expose whether the notation works as intended.
**Required**: At minimum, one example for each case. E.g., non-empty: a document with V_S(d) = {[1,1], [1,2], [1,3]} (N=3), enumerate the 4 valid insertion positions and show D-CTG is preserved after inserting at one. Empty: show [1,1] of depth 2 satisfies D-MIN.

## OUT_OF_SCOPE

### Topic 1: Interaction with specific operations (INSERT, COPY, DELETE)
**Why out of scope**: The ASN defines the predicate; individual operations will reference it and must prove they only insert at valid positions. That proof obligation belongs in the operation ASNs.

### Topic 2: Non-text-subspace constraints analogous to S8a
**Why out of scope**: S8a constrains text-subspace V-positions. Whether link-subspace positions need analogous well-formedness rules is a question for the link subspace ASN.

VERDICT: REVISE
