# Review of ASN-0036

## REVISE

### Issue 1: Undefined `fields(a)` notation

**ASN-0036, S7 and S7c**: "`origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`" and "`#fields(a).element ≥ 2`"

**Problem**: The notation `fields(a).node`, `fields(a).user`, `fields(a).document`, `fields(a).element` is used but never defined in the ASN. T4b (UniqueParse) in the foundation already provides partial projections `N(t), U(t), D(t), E(t)` for exactly these fields. The ASN reinvents notation for something the foundation supplies.

**Required**: Replace `fields(a).node` with `N(a)`, `fields(a).user` with `U(a)`, `fields(a).document` with `D(a)`, `fields(a).element` with `E(a)`. Per standard 7 (foundation notation usage), the ASN should not invent parallel notation.

### Issue 2: Ambiguous `v > 0` notation

**ASN-0036, S8a postcondition**: "`(A v ∈ dom(Σ.M(d)) :: zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0)`"

**Problem**: The notation `v > 0` is presented as shorthand for "every component of `v` is strictly positive" (per the proof body). But T1 (LexicographicOrder, foundation) defines `>` on tumblers as the lexicographic strict order, and `0` is not a member of `T` (T0 requires `#t ≥ 1`). So `v > 0` is ill-typed under the foundation's interpretation. The intended meaning — all-components-positive — is precisely TA7a's set `S = {o ∈ T : (A i : 1 ≤ i ≤ #o : oᵢ > 0)}`.

Additionally, the conjunct `v > 0` is redundant: `zeros(v) = 0` combined with T0's ℕ-valued components and NAT-zero's `0 < n ∨ 0 = n` already implies every component is `≥ 1`.

**Required**: Either replace `v > 0` with `v ∈ S` (citing TA7a's foundation definition) and remove redundancy, or explicitly write `(A i : 1 ≤ i ≤ #v : vᵢ > 0)`. Do not overload T1's strict order.

### Issue 3: `ord(v)` precondition mismatch with V-position guarantees

**ASN-0036, ord(v) definition (V-position ordinal decomposition)**: "`Preconditions: v ∈ T, #v ≥ 2`"

**Problem**: The function `ord(v)` requires `#v ≥ 2`. But S8a guarantees only `zeros(v) = 0 ∧ v₁ ≥ 1` for V-positions in `dom(M(d))`; with `#v ≥ 1` from T0, a V-position `v = [S]` of depth 1 is consistent with S8a. For such `v`, `ord(v)` is undefined. The decomposition machinery (OrdAddHom, OrdAddS8a, OrdShiftHom) and S8-depth's "subspace" partition are silently assumed to apply to all V-positions, but the precondition is not part of the invariant.

**Required**: Either strengthen S8a to include `#v ≥ 2`, or extend `ord(v)` to handle `#v = 1` (e.g., `ord([S]) = ε` and explicit handling at downstream lemmas), or state explicitly that depth-1 V-positions are excluded by a separate invariant.

### Issue 4: D-SEQ depth precondition not enforced by S8-depth

**ASN-0036, D-SEQ**: "if V_S(d) is non-empty and the common V-position depth m ≥ 2 (S8-depth), then..."

**Problem**: D-SEQ requires `m ≥ 2` as a precondition. The rationale given is that ValidInsertionPosition's empty-subspace case requires `m ≥ 2`. But S8-depth itself only says all V-positions in a subspace share *a* depth — it places no lower bound on that depth. So a system could have `V_S(d) = {[S]}` with `m = 1`, satisfying S8-depth but falling outside D-SEQ's domain. The bootstrap argument ("operations must use ValidInsertionPosition, which requires m ≥ 2") relies on operation behavior, which is OUT_OF_SCOPE here.

**Required**: Either strengthen S8-depth to `(A v ∈ dom(M(d)) :: #v ≥ 2)`, or make the depth-2 lower bound an explicit invariant of the strand model rather than a consequence of operations that are not yet specified.

### Issue 5: D-CTG applicability to link subspace not addressed

**ASN-0036, D-CTG and remark on subspaces**: "Link-subspace arrangement semantics are deferred to a future ASN."

**Problem**: D-CTG, D-MIN, and D-SEQ are stated as universal quantifications over `S` (subspace). Their proofs treat subspace 1 (text) and subspace 2 (links) symmetrically. But the ASN defers link-subspace semantics to a future ASN. It is unclear whether D-CTG/D-MIN/D-SEQ are required to hold for the link subspace, or whether the universal quantification is implicitly restricted.

**Required**: State explicitly whether D-CTG, D-MIN, D-SEQ are required to hold uniformly across all subspaces, or whether they apply only to the text subspace pending link-subspace specification. If uniform, justify; if restricted, scope the quantification.

### Issue 6: `m = 1` case glossed in S8 within-subspace uniqueness

**ASN-0036, S8 proof, "Uniqueness within a subspace"**: "For the case of interest `t = w`, shared subspace `w₁ = v₁ = S` gives `t₁ = v₁`, forcing `j ≥ 2`; at `m = 2` this further forces `j = m = 2`..."

**Problem**: The proof explicitly addresses `m ≥ 2` (forcing `j ≥ 2` via shared subspace), but never explicitly disposes of `m = 1`. At `m = 1`, every V-position in subspace `S` has the form `[S]` — there is only one such tumbler, so V_S(d) is trivially a singleton and uniqueness holds vacuously. This argument is correct but not stated. The reader is left to verify the edge case.

**Required**: Add an explicit "Case m = 1" paragraph noting that V_S(d) contains at most one element (namely `[S]`), so within-subspace uniqueness is vacuous.

### Issue 7: `+ k` notation overloaded with NAT addition

**ASN-0036, throughout (S8-depth and subsequent)**: "We write `v + k` for ordinal displacement applied to V-positions, and `a + k` for the same applied to the element ordinal of I-addresses."

**Problem**: The symbol `+` is used both for NAT addition (on ℕ-valued components and indices) and for tumbler ordinal displacement (`v + k = shift(v, k)`). The ASN does define the tumbler usage, but the same line uses `vₖ + wₖ` (NAT addition) elsewhere. A reader encountering `v + 1` must determine from context whether this is a tumbler operation or a component-level operation.

**Required**: Use `shift(v, k)` or `v ⊕ δ(k, m)` for the tumbler operation, reserving `+` for NAT addition; or introduce a distinct symbol (e.g., `v ⊞ k`) for ordinal displacement.

### Issue 8: T5 cited under non-canonical name

**ASN-0036, S8 proof**: "T5 (PrefixContiguity, ASN-0034) gives: for any `t` with `v ≤ t ≤ v + 1`, `[S₁] ≼ t`."

**Problem**: T5's canonical name in the foundation is `ContiguousSubtrees`. `PrefixContiguity` appears only as a forward-reference label in T12's contract. Using a forward-reference name as the primary citation is confusing.

**Required**: Cite T5 by its canonical foundation name `ContiguousSubtrees` (or just `T5`).

## OUT_OF_SCOPE

No additional out-of-scope items beyond those already enumerated in the ASN's Scope section.

VERDICT: REVISE
