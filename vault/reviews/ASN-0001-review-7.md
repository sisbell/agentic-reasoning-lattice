# Review of ASN-0001

## REVISE

### Issue 1: TA4 verification contradicts stated property
**ASN-0001, Verification of TA4**: "Sub-case: some aᵢ ≠ 0 for i < k... This is a only if w has no components beyond k, i.e., #w = k. When #w > k, the subtraction in this sub-case does not recover a exactly"
**Problem**: The stated property claims `(a ⊕ w) ⊖ w = a` whenever `k = #a`. The verification itself demonstrates a counterexample: let `a = [5, 3]`, `w = [0, 7]`, action point `k = 2 = #a`. Then `a ⊕ w = [5, 10]`. Now `[5, 10] ⊖ [0, 7]`: the subtraction finds first divergence at position 1 (`5 ≠ 0`), produces `[5 - 0, 10] = [5, 10] ≠ [5, 3]`. The subtraction never reaches position `k` to undo the addition because the divergence between the result and `w` occurs earlier. The precondition `k = #a` is insufficient — the inverse also requires that the subtraction's divergence point coincides with the addition's action point. This holds when all components of `a` before `k` are zero (the second sub-case), but fails otherwise.
**Required**: Either strengthen TA4's precondition to `k = #a ∧ (A i : 1 ≤ i < k : aᵢ = 0)` (or equivalently, `#w = k = #a = 1` for the single-component case that editing actually uses), or redefine `⊖` so that it takes the action point `k` as an explicit parameter rather than discovering it from the first divergence. The current subtraction-by-divergence algorithm is fundamentally incompatible with the stated inverse property for multi-component operands with nonzero prefixes.

### Issue 2: TA1 inconsistency between body and table
**ASN-0001, Properties Introduced table**: "TA1: Addition preserves the total order: a < b ⟹ a ⊕ w < b ⊕ w for w > 0"
**Problem**: The body defines TA1 with weak order preservation (`≤`): `(A a, b, w : a < b ∧ w > 0 ∧ k ≤ min(#a, #b) : a ⊕ w ≤ b ⊕ w)`. The constructive verification confirms that equality can arise (Case 1: `k < divergence(a, b)` gives `a ⊕ w = b ⊕ w`). The table states the strict form, which is TA1-strict with the additional precondition `k ≥ divergence(a, b)`. This is not a typo — the wrong property is listed under the TA1 label.
**Required**: The table entry for TA1 must state the weak form (`≤`) matching the body, or add the divergence precondition.

### Issue 3: TA3 stated without proof or verification
**ASN-0001, Subtraction for shifting**: "(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w : a ⊖ w < b ⊖ w)"
**Problem**: TA3 claims strict order preservation for subtraction. The constructive verification section ("Verification of TA1 and TA1-strict") verifies the addition properties only. No corresponding verification of TA3 against the constructive definition of `⊖` appears anywhere in the ASN. The subtraction algorithm is structurally different from addition — it zeros positions before the divergence point and copies the tail from the minuend, whereas addition copies the tail from the displacement. The proof obligation for TA3 is not "by similar reasoning" to TA1; the cases differ. In particular: does TA3 hold strictly in all cases, or are there conditions (analogous to TA1's Case 1) where strict degrades to weak?
**Required**: A case-by-case verification of TA3 against the constructive definition of `⊖`, parallel to the TA1/TA1-strict verification. If TA3 holds strictly without additional preconditions (as claimed), demonstrate why the subtraction algorithm's structure prevents the equality-collapse that affects addition.

### Issue 4: Partition Monotonicity proof assumes k = 0 without justification
**ASN-0001, Partition monotonicity proof**: "By T10a, subsequent sibling prefixes are produced by the same allocator using its fixed depth parameter — here k = 0 for sibling allocation"
**Problem**: T10a states that each allocator uses "a single fixed k ≥ 0" for its sibling allocations. The proof asserts `k = 0` as if this were a consequence of T10a, but T10a permits any fixed `k`. The non-nesting claim that follows depends critically on `k = 0`: TA5(c) preserves length only for `k = 0`, so same-length outputs are guaranteed only when `k = 0`. For `k > 0`, TA5(d) gives `#inc(t, k) = #t + k`, so successive siblings have lengths `L, L + k, L + 2k, ...` — all different. Worse, when `k > 0`, each output extends the previous: `inc(t, k)` agrees with `t` on all `#t` positions and appends `k` more (by TA5(b,d)), making `t` a proper prefix of `inc(t, k)`. Successive sibling outputs nest, not merely differ in length. This directly breaks the non-nesting premise required by the Prefix Ordering Extension lemma.
**Required**: Either constrain T10a to require `k = 0` for sibling allocations (reserving `k > 0` exclusively for child-spawning), or restructure the proof to handle arbitrary fixed `k`. The first option is consistent with Gregory's implementation evidence (`rightshift=0` for element allocation) and with the architectural intent (siblings at the same depth).

### Issue 5: Global Uniqueness Case 4 depends on the flawed non-nesting argument
**ASN-0001, Global uniqueness, Case 4**: "However, the two allocators produce outputs of different lengths, and T10a is the property that guarantees this."
**Problem**: Case 4 argues that parent and child allocators produce outputs of different lengths, relying on the claim that "all sibling outputs from a single allocator have the same length." As established in Issue 4, this holds only when the allocator's fixed `k = 0`. The proof also claims `γ₁ + k' + δ > γ₁` with `k' ≥ 1`, asserting that child outputs are strictly longer than parent outputs. But if the parent uses `k > 0`, parent outputs grow in length with each allocation, and some parent output could have the same length as some child output. The length-separation argument collapses.
**Required**: This is downstream of Issue 4. If T10a is constrained to `k = 0` for siblings, then parent sibling outputs have uniform length `γ₁`, child outputs have length `γ₁ + k' ≥ γ₁ + 1` (or `γ₁ + k' + δ` for grandchildren), and the length separation holds. State this dependency explicitly.

### Issue 6: Reverse inverse proof has a gap in the TA3 application
**ASN-0001, Corollary (Reverse inverse)**: "If y ⊕ w > a, then applying ⊖ w to both sides (order-preserving by TA3, both sides ≥ w since y ⊕ w > a ≥ w) gives y > a ⊖ w = y, a contradiction."
**Problem**: TA3 requires `a < b ∧ a ≥ w ∧ b ≥ w` and yields `a ⊖ w < b ⊖ w`. The proof applies TA3 with `a := a` and `b := y ⊕ w`, needing `a < y ⊕ w` and `a ≥ w`. The hypothesis gives `a ≥ w`, but the conclusion `(y ⊕ w) ⊖ w = y` comes from TA4, which — per Issue 1 — requires additional preconditions beyond `k = #a`. The proof inherits TA4's unsound precondition. Additionally, TA3 itself is unverified (Issue 3); the proof chains through two unestablished properties.
**Required**: Once TA4's precondition is corrected and TA3 is verified, revisit this proof with the corrected statements.

## DEFER

### Topic 1: Multi-component displacement inverses
**Why defer**: The ASN identifies that the mutual inverse holds cleanly for single-component displacements at the element level — the case editing operations actually use. The general theory of multi-component displacement inverses (where tail replacement discards structure) is acknowledged as incomplete. This is genuinely new territory: it would require either a different subtraction algorithm (one that takes the action point as a parameter) or a formal characterization of which displacement shapes admit inverses. This belongs in a future ASN on displacement algebra, not as a patch to this one.

### Topic 2: Subtraction results as valid addresses
**Why defer**: Subtraction zeros out components before the divergence point, potentially producing tumblers like `[0, 0, 5]` that satisfy T's membership (finite sequence of non-negative integers) but violate T4's positive-component constraint for I-space addresses. Whether subtraction results must be valid I-space addresses (they need not be — they are V-space positions) and what constraints V-space positions must satisfy is a question about the V-space invariants, which belong in an operations ASN.

### Topic 3: Concrete constraints on T10a's depth parameter
**Why defer**: The ASN's evidence from Gregory shows `rightshift=0` for elements and `rightshift=1` for sub-documents. A complete enumeration of which allocation contexts use which depth parameters — and whether the system permits user-defined allocation depths — is an implementation-mapping question that a future ASN on allocation protocols should address.
