# Review of ASN-0036

## REVISE

### Issue 1: Broken NAT-* citation chain for "1 < 2" in S8 auxiliary lemma

**ASN-0036, S8 auxiliary lemma, Conclusion (i) (Derivation of the strict inequality)**: "From δⱼ ≥ 2, NAT-order (≤-transitivity) chains 2 ≤ δⱼ; NAT-discrete promotes 1 < 2 (NAT-zero gives 0 < 1, NAT-discrete at (0, 1) gives 0 + 1 ≤ 1 hence 1 ≤ 1; NAT-discrete at (1, 2) then gives 1 + 1 ≤ 2, i.e. 1 < 2..."

**Problem**: NAT-discrete is m < n ⟹ m + 1 ≤ n. Applying at (m=1, n=2) requires `1 < 2` as antecedent — which is the very fact being derived. The chain is circular at the final step. Also, "0 < 1" comes from NAT-closure's *Consequence*, not from NAT-zero (NAT-zero gives a disjunction, not the strict inequality directly).

**Required**: Replace the chain with the direct derivation: 2 := 1 + 1 (T4 numerals); NAT-addcompat's strict successor inequality `n < n + 1` at `n = 1` gives `1 < 1 + 1 = 2`; combined with `2 ≤ δⱼ` and NAT-order's <-transitivity, `1 < δⱼ`. The same fix is needed in S7c Consequence (b) which carries the parallel derivation.

### Issue 2: Unstated NAT addition commutativity in S8 auxiliary lemma

**ASN-0036, S8 auxiliary lemma, Conclusion (i)**: "note that the left-hand side 1 + (#aⱼ − δⱼ) = (#aⱼ − δⱼ) + 1 by NAT addition's commutativity (Consequence of NAT-closure together with NAT-addcompat's symmetric handling of left/right positions, ASN-0034)"

**Problem**: NAT-addcompat in ASN-0034 explicitly states "Both compatibility directions are stated as independent axiom clauses because commutativity has not yet been declared at this stratum, so neither direction is derivable from the other." No commutativity Consequence exists in NAT-closure or NAT-addcompat. The cited Consequence does not exist.

**Required**: Restructure the derivation to avoid commutativity. Use NAT-addcompat's *left* order compatibility at `(m, p, n) = (#aⱼ − δⱼ, 1, δⱼ)` to lift `1 ≤ δⱼ` to `(#aⱼ − δⱼ) + 1 ≤ (#aⱼ − δⱼ) + δⱼ`; NAT-sub's *left-inverse* `δⱼ + (#aⱼ − δⱼ) = #aⱼ` (which is what the proof already invokes) needs to be paired with NAT-sub's *right-inverse* `(#aⱼ − δⱼ) + δⱼ = #aⱼ` (both are listed in NAT-sub) to identify the RHS as `#aⱼ`. Then strict-lift via NAT-cancel.

### Issue 3: Strict-lifting of NAT-addcompat without NAT-cancel citation

**ASN-0036, S8 auxiliary lemma Conclusion (i); D-CTG-depth alternative-construction parenthetical**: Multiple steps lift NAT-addcompat (a weak-order axiom: `p ≤ n ⟹ ...`) to a strict conclusion (e.g., `(#aⱼ − δⱼ) + 1 < #aⱼ` from `1 < δⱼ`; `(v₁)ⱼ₊₁ < (v₁)ⱼ₊₁ + (i + 1)` from `0 < i + 1`).

**Problem**: NAT-addcompat as axiomatized in ASN-0034 produces only weak inequalities. To strengthen to strict from `p < n`, the canonical move is: split `p < n` into `p ≤ n ∧ p ≠ n` (NAT-order), apply NAT-addcompat to get `... ≤ ...`, then use NAT-cancel to rule out equality (since equal sums would force `p = n`). S8's depends list omits NAT-cancel entirely; D-CTG-depth's depends list cites NAT-cancel only for injectivity (not for the strict-lifting role).

**Required**: Add NAT-cancel to S8's depends list with the strict-lifting role spelled out, and add a note in D-CTG-depth's NAT-cancel entry covering both injectivity and the `0 < i + 1` → `(v₁)ⱼ₊₁ + 0 < (v₁)ⱼ₊₁ + (i+1)` strict-lifting step.

### Issue 4: Incorrect length bound gloss in S8 auxiliary lemma

**ASN-0036, S8 auxiliary lemma, T4-validity of shift(aⱼ, k) bridging (ii) to (iii)**: "Positive first component: shift(aⱼ, k)₁ = aⱼ₁ since position 1 is strictly less than #aⱼ (because #aⱼ ≥ 4 — three field-separator zeros plus at least one non-separator component in N(aⱼ), U(aⱼ), D(aⱼ), and E(aⱼ) — and hence #aⱼ ≥ 4 > 1)"

**Problem**: T4's field-segment constraint (and T4a's reformulation) requires *every* present field to be non-empty. With `zeros(aⱼ) = 3` (S7b), all four fields N, U, D, E are present, so the minimum count is 3 separators + 4 × 1 components = 7 components. With S7c's `#E(aⱼ) ≥ 2`, the minimum is 8. The arithmetic "3 + 1 = 4" undercounts non-separator components by treating "at least one in N, U, D, E" as a single non-separator total rather than one per field. The conclusion `#aⱼ > 1` is correct but the bound is unnecessarily loose.

**Required**: Correct the gloss to `#aⱼ ≥ 7` (or `≥ 8` invoking S7c) with the explanation "three field-separator zeros plus at least one non-separator component in *each* of N(aⱼ), U(aⱼ), D(aⱼ), and E(aⱼ)".

### Issue 5: S5 cross-document construction notation inconsistency

**ASN-0036, S5 proof, Cross-document construction**: "Fix a single V-position v = [1, 1] — the depth-2 V-position in subspace 1, shared across all N + 1 documents — and define each arrangement as M_N(dᵢ) = {v ↦ a}. The pairs (dᵢ, v) are pairwise distinct..." — but the *Conclusion* of the same paragraph says "since each of the N + 1 documents contributes exactly one pair (dᵢ, vᵢ)".

**Problem**: The V-position is declared fixed (v = [1, 1] shared across all documents), but the sharing-multiplicity count uses `(dᵢ, vᵢ)` with indexed `vᵢ`, suggesting varying positions. Either notation is workable, but the proof switches between them within one paragraph.

**Required**: Standardize on `(dᵢ, v)` with v fixed; the pairs are distinct because the first coordinates are pairwise distinct.

### Issue 6: Properties Introduced table missing subspace(v) row

**ASN-0036, Properties Introduced table**: The table lists `subspace_I(a)` as an introduced function with its own row, but `subspace(v) = v₁` — defined with its own Formal Contract block in the D-CTG section and used pervasively throughout the ASN (V_1(d) definition, OrdAddHom (b), OrdShiftHom (b), D-MIN, D-SEQ, ValidInsertionPosition, etc.) — has no corresponding row.

**Required**: Add a row for `subspace(v)` parallel to the `subspace_I(a)` row, with the appropriate dependencies (T0, S8a).

### Issue 7: S8 auxiliary lemma applicability under singleton existence proof

**ASN-0036, S8 Postconditions and Auxiliary lemma**: The existence proof exhibits only the singleton decomposition (every nⱼ = 1). The auxiliary lemma is then stated to hold "for any correspondence run (vⱼ, aⱼ, nⱼ) satisfying conjunct (b)" with the k ≥ 1 case load-bearing only for nⱼ ≥ 2 decompositions.

**Problem**: The existence claim establishes only nⱼ = 1 runs in the constructive witness, so the lemma's k ≥ 1 branches are not exercised by what S8 proves to exist. The worked example then claims a non-singleton decomposition `(1.1, ..., 5)` as exhibiting "the *coarser* decomposition that S8's existence claim admits alongside the trivial singleton form" — but S8 does not prove the coarser decomposition exists; it only proves the singleton form exists and notes coarser forms "exist whenever consecutive (vⱼ, aⱼ) pairs admit the index-arithmetic identity." Whether a length-5 run actually satisfies S8's conjunct (b) on the worked example's arrangement is asserted, not derived.

**Required**: Either (a) strengthen S8 to prove that non-singleton runs exist under specified conditions (e.g., when consecutive M(d)(shift(v, k)) = shift(a, k) holds for k > 0), explicitly invoking the auxiliary lemma; or (b) clarify in S8 and in the worked example that the non-singleton decomposition is *admitted* by S8 conjuncts (a) and (b) when it can be verified directly from state, but its *existence as a witness for S8* is not separately proved. The worked example's verification of the length-5 run is the right move — but it should be presented as confirming that the length-5 form is *also* a valid decomposition (not as something S8 produces).

## OUT_OF_SCOPE

(None — the open questions and scope sections adequately defer operations, link-subspace semantics, and version operations.)

VERDICT: REVISE
