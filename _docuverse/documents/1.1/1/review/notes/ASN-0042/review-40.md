# Review of ASN-0042

## REVISE

### Issue 1: O3's dependency list omits O15 and O14
**ASN-0042, Properties Introduced table**: "O3 | `ω(a)` changes only through delegation introducing a longer matching prefix — monotonic refinement | from T8, O12, O13, O1b"
**Problem**: The proof of O3 explicitly cites O15 ("By O15 (PrincipalClosure), `π' ∈ Π_{Σ'} ∖ Π_Σ` arrived through bootstrap or through delegation") and implicitly relies on O14 (the reachability + iterated-O12 argument that gives `Π₀ ⊆ Π_Σ` only works because O14 establishes the non-empty bootstrap). Without these, the bootstrap case cannot be ruled out and the conclusion `π'` arrived by delegation is unjustified.
**Required**: Append O14 and O15 to O3's dependency list (the same dependencies AccountLevelPermanence already lists).

### Issue 2: O8's dependency list omits O15
**ASN-0042, Properties Introduced table**: "O8 | ... | from Delegation, O2, O12, O13, T8"
**Problem**: The proof of O8 invokes O15 directly: "combined with O15 (PrincipalClosure) — `π'` can enter `Π` only via the delegation transition that witnesses `delegated_{Σ_d}(π, π')`". O15 is load-bearing here.
**Required**: Add O15 to O8's dependency list.

### Issue 3: PrefixBaptismCoupling's dependency list omits O13
**ASN-0042, Properties Introduced table**: "PrefixBaptismCoupling | ... | from O14(vii), O15, O18, T8"
**Problem**: The proof's Case 1 (carry-forward) explicitly uses O13: "By O13 (PrefixImmutability), `pfx_{Σ_{n+1}}(π) = pfx_{Σ_n}(π)`". Without O13 the inductive step cannot identify the surviving principal's prefix at the successor state with its prefix at the prior state.
**Required**: Add O13 to PrefixBaptismCoupling's dependency list.

### Issue 4: O8's "trajectory passes through Σ_d^{post}" argument is implicit
**ASN-0042, O8 proof**: "The hypothesis `π' ∈ Π_{Σ'}` is given directly, and combined with O15 (PrincipalClosure) — `π'` can enter `Π` only via the delegation transition that witnesses `delegated_{Σ_d}(π, π')` — it forces the trajectory `Σ_d →⁺ Σ'` to pass through `Σ_d^{post}`."
**Problem**: O15 alone does not say a specific principal can enter Π only once. The actual chain of reasoning required is: (a) `delegated_{Σ_d}(π, π')` plus condition (iii) gives `π' ∉ Π_{Σ_d}` and `π' ∈ Π_{Σ_d^{post}}`; (b) any later transition introducing `π'` would need `π' ∉ Π_{Σ_k}`, but O12 has propagated `π' ∈ Π` to every successor state; (c) hence no later introduction event for `π'` exists, so the unique introduction must be `Σ_d → Σ_d^{post}`. The proof should walk this chain rather than gesturing at O15.
**Required**: Replace the one-line invocation with the explicit chain: condition (iii) + O12 forbid re-introduction; therefore the introduction event on any path bringing `π'` into `Π_{Σ'}` is `Σ_d → Σ_d^{post}`.

### Issue 5: Worked example's hwm = 5 is inconsistent with the explicit baptisms
**ASN-0042, Worked Example, Fork (O10)**: "Assume the pre-fork state `Σ_pre` is reached after earlier baptisms `a₁ = [1, 0, 2, 0, 3, 0, 1]` ... and `a₂ = [1, 0, 2, 0, 5, 0, 1]` ... have established `hwm(Σ_pre.B, [1, 0, 2], 2) = 5`"
**Problem**: `hwm(Σ_pre.B, [1, 0, 2], 2) = #children(Σ_pre.B, [1, 0, 2], 2)` counts elements of `S([1,0,2], 2)` — that is, document-level addresses `[1,0,2,0,1]` through `[1,0,2,0,5]` — that lie in `Σ_pre.B`. Baptizing element-level `a₁` via `Bop([1,0,2,0,3], 2)` does not place the document-level parent `[1,0,2,0,3]` into B (B6 requires only `p ∈ T` with T4, not `p ∈ B`). The example as stated yields hwm = 0, not hwm = 5. Either additional document-level baptisms must be exhibited or the parenthetical "(the largest document-field index used so far under `[1, 0, 2]`)" should be replaced by an explicit construction of `Σ_pre.B`.
**Required**: Either narrate the document-level baptisms at slots 1–5 explicitly (B1 forces all of them once slot 5 is reached), or rebuild the scenario starting from a smaller hwm so the explicit baptisms suffice.

### Issue 6: Properties Introduced entry for `acct(a)` misdescribes the construction
**ASN-0042, Properties Introduced table**: "`acct(a)` | When `zeros(a) = 0`: `acct(a) = a`; when `zeros(a) ≥ 1`: truncation through user field | from T4b, T3"
**Problem**: The body of the ASN defines `acct(a) = N(a) ++ [0] ++ U(a)` for `zeros(a) ≥ 1` — a concatenation built from the field projections, not a truncation of `a`. The two coincide as values when `zeros(a) = 1`, but for `zeros(a) ∈ {2, 3}` the construction is a re-assembly from `N(a)` and `U(a)`, not a positional truncation. The phrase mismatch invites a reader to interpret `acct(a)` as `a[1..k]` for some k, which is correct for valid tumblers but obscures the dependence on T4b's field decomposition.
**Required**: Replace "truncation through user field" with "`N(a) ++ [0] ++ U(a)`" (or "concatenation of node field, separator, user field").

### Issue 7: `dom(π)` notation collides with `dom(A)` from T10a
**ASN-0042, Ownership Domains and throughout**: "For principal `π ∈ Π`, define `dom(π) = {a ∈ T : pfx(π) ≼ a}`."
**Problem**: The foundation defines `dom(A) = {tₙ : n ≥ 0}` for an allocator `A` (T10a AllocatorDiscipline) — a per-allocator enumeration distinct from the prefix-defined ownership set introduced here. The two concepts are mathematically distinct (one ranges over T, the other over a specific increment chain) and load-bearing in different ways (T9, T10a's domain-disjointness chain depend on the allocator reading; O4, O7, O8, O10 depend on the ownership reading). Reusing the symbol risks readers who carry the foundation interpretation forward conflating the two domains in proofs that bridge the two layers (e.g., the AllocatedSet/Bridge1 area).
**Required**: Either rename to `Dom(π)` / `domₒ(π)` / `domain(π)`, or add a one-line disambiguation note at the Definition (OwnershipDomain) site distinguishing it from T10a's `dom`.

## OUT_OF_SCOPE

None beyond what the ASN already lists in its Scope section and Open Questions. Topics genuinely out of scope (transfer mechanism, cross-node federation, authentication binding, content accessibility post-principal-removal) are correctly recorded as open questions or scope notes.

VERDICT: REVISE
