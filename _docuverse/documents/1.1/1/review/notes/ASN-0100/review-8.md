# Review of ASN-0100

## REVISE

### Issue 1: K.μ⁻ omission case (ii) rationale doesn't cover V_{s_L}(d) = ∅ sub-sub-case

**ASN-0100, Substrate Decomposition (step 2)**: "(ii) when `p_m = N + 1` (append case — Left = entire pre-state `V_{s_C}(d)`), `n'_{s_C} = N = n_{s_C}` likewise forecloses strict shrinkage in s_C, so the strict-shrinkage clause would require `n'_{s_L} < n_{s_L}` and violate INS.frame.subspace."

**Problem**: The rationale "would require `n'_{s_L} < n_{s_L}` and violate INS.frame.subspace" implicitly assumes `V_{s_L}(d) ≠ ∅`. When `V_{s_L}(d) = ∅` (so `n_{s_L} = 0`), the condition `n'_{s_L} < n_{s_L} = 0` has no solution in ℕ — strict shrinkage isn't achievable at all, so K.μ⁻'s precondition fails. The omission outcome is the same, but the failure mode differs (precondition failure vs. frame violation), and the case (ii) rationale as written doesn't cover the V_{s_L}(d) = ∅ sub-sub-case.

**Required**: Split the case (ii) rationale into the two sub-sub-cases, or unify with wording like: "If `V_{s_L}(d) ≠ ∅`, strict shrinkage via s_L would violate INS.frame.subspace; if `V_{s_L}(d) = ∅`, strict shrinkage via s_L is impossible (no `n'_{s_L} < 0` in ℕ). Either way, K.μ⁻ cannot fire consistent with the canonical retention parameters and INSERT's frame."

### Issue 2: K.μ⁻ omission framed as forced when it is a canonical choice in case (ii)

**ASN-0100, Substrate Decomposition (step 2)**: "Omitted in three cases..."

**Problem**: For case (ii) (append), an alternative decomposition exists: K.μ⁻ with `n'_{s_C} < N` strictly shrinks s_C (satisfying the precondition without touching s_L), and a subsequent K.μ⁺ re-adds the discarded positions before adding Insertion. This reaches the same Σ' via a non-canonical path. The ASN's "omitted" language reads as forced-by-precondition, but the omission in case (ii) (V_{s_L} non-empty) is actually a canonical-decomposition choice — alternative decompositions could fire K.μ⁻. The ASN later acknowledges decomposition non-uniqueness ("the substrate decomposition that realises it is not [unique]"), but the case-omission rationale conflates "K.μ⁻ cannot fire" with "K.μ⁻ is not fired in the canonical decomposition."

**Required**: Distinguish the three omission rationales: case (i.a) is forced (precondition `dom(M(d)) ≠ ∅` fails); case (i.b) is forced under INS.frame.subspace (every admissible firing violates the frame); case (ii) is a canonical-decomposition choice when V_{s_L}(d) ≠ ∅ (alternative decompositions admissible) and forced when V_{s_L}(d) = ∅ (no admissible firing).

### Issue 3: Empty-case worked example is brief and lacks composite-boundary discharge trace

**ASN-0100, A Worked Example**: "Empty-document first insertion. Let `d` have `V_{s_C}(d) = ∅`. Invoke `INSERT(d, [1,1], ⟨v₀, v₁, v₂⟩)` with `m = 2`... Post-state `V_{s_C}(d') = {[1,1], [1,2], [1,3]}` with `m_C = 2` fixed by S8-depth..."

**Problem**: The worked example provides a thorough projection-shift trace and J0/J1★/J1'★ discharge for the interior case, but the empty case only states the composite and post-state. The empty case is the boundary where (a) `ValidFirstInsertionPosition` (ternary) replaces `ValidInsertionPosition` (binary), (b) `m_C` is established for the first time, (c) the empty-arrangement / fresh-allocator-state distinction matters operationally, and (d) K.μ⁻ omission has a different rationale. A boundary case with this much novel structure should not rely solely on the interior worked example for verification.

**Required**: Extend the empty-case description to include either (a) an explicit projection-shift trace verifying the cross-subspace and cross-document frames, or (b) explicit J0/J1★/J1'★ discharge through the n K.α + K.μ⁺ + n K.ρ sequence; preferably also a sub-case where `V_{s_C}(d) = ∅` but `dom(C)` contains prior emissions of `A_C(d)` (the empty-arrangement-but-non-empty-allocator-state case the ASN mentions in passing).

### Issue 4: "V_{s_C}(d') = exact union of three regions" is in narrative, not a labeled postcondition

**ASN-0100, Effect — Arrangement of d, text subspace**: "The post-state's text-subspace domain is exactly the union: `V_{s_C}(d') =` Left positions ∪ Insertion positions ∪ Shifted-right positions."

**Problem**: The three regions are stated via universal-quantifier clauses ("Left positions are preserved," "Insertion positions get the new addresses," "Shifted-right positions are shifted"). These establish that each region is *contained in* `V_{s_C}(d')`, but the *exhaustiveness* — that no other s_C positions enter the post-state — is stated only in a narrative sentence, not as a labeled postcondition. The S2 functionality argument relies on pairwise disjointness of exactly these three regions; if the post-state contained additional s_C positions, the argument would be incomplete.

**Required**: Either add an explicit exhaustiveness postcondition (e.g., `INS.M-exhaustive`: `(A v : v ∈ dom(M'(d)) ∧ subspace(v) = s_C ⟹ v ∈ Left ∪ Insertion ∪ Shifted-right)`), or explicitly note that exhaustiveness follows from the substrate decomposition's step-3 K.μ⁺ adding precisely those positions and no others.

### Issue 5: Insertion-region S8a argument elides the k = 0 case

**ASN-0100, Post-state V-position well-formedness**: "For each Insertion position `shift(p, k)`, TumblerAdd's piecewise rule (ASN-0034) at action point `m_C` copies the leading `m_C − 1` components from `p`, which are all `1`... the final component is `p_m + k ≥ p_m ≥ 1`."

**Problem**: The argument invokes TumblerAdd, but TumblerAdd applies via `shift(p, k) = p ⊕ δ(k, m_C)`, which is defined only for `k ≥ 1` (OrdinalDisplacement's precondition is `n ≥ 1`). For `k = 0`, the ASN's earlier convention gives `shift(p, 0) = p` by OrdinalShiftBase (ASN-0058), without going through TumblerAdd. The S8a verification reads as if a single uniform TumblerAdd argument covers all `k ∈ {0, ..., n−1}`, but the `k = 0` case must be handled by direct appeal to p's own S8a (inherited from the valid-position predicate). Similar elision occurs in the S8-depth verification ("By TumblerAdd's result-length identity, `#shift(p, k) = m_C`").

**Required**: Split the per-position S8a/S8-depth verification: at `k = 0`, `shift(p, 0) = p` satisfies S8a/S8-depth because `p` does (ValidInsertionPosition postcondition (d) or ValidFirstInsertionPosition postcondition (d)); at `k ≥ 1`, the TumblerAdd argument applies.

### Issue 6: Worked-example projection trace assumes tight endset without explicit precondition

**ASN-0100, A Worked Example (Projection-shift correspondence)**: "Among Insertion: `a_{new0}, a_{new1} ∉ coverage(e_1)` (assuming `e_1` is tight at its incorporation — by LP19a, the fresh `a_{new0}, a_{new1}` cannot lie in a tight coverage)..."

**Problem**: The worked example's projection arithmetic gives `N_{ℓ,1} = N_I = ∅`, but this conclusion holds *only if* `e_1` is tight at its incorporation state. For a non-tight `e_1`, the worked example's "post-state `project(ℓ, 1, d, Σ') = {[1,2], [1,5], [1,6]}`" would be incomplete (fresh addresses could land in coverage). The example uses "assuming" parenthetically rather than stating tightness as a precondition of the example. A reader following the trace expects an unconditional concrete result.

**Required**: State the tightness assumption explicitly at the start of the projection trace as a precondition of the worked example, or show two traces: one with tight e_1 (N_I = ∅) and one with non-tight e_1 (where INSERT's allocation may produce new projection entries).

## OUT_OF_SCOPE

None — the Open Questions and the explicit scope-bounding section ("Bounding the Scope") appropriately mark out-of-scope topics (link-subspace insertion, COPY, DELETE, REARRANGE, version creation, inter-server replication, concurrent INSERT semantics, composite atomicity machinery). No misplaced topics surfaced.

VERDICT: REVISE
