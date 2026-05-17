# Review of ASN-0047

## REVISE

### Issue 1: V-ordering not formally defined
**ASN-0047, "Amendments to existing transitions" (D-CTG★ statement)**: "V_S(d) is contiguous under the V-ordering on subspace S"
**ASN-0047, D-SEQ★ derivation Step 1**: "Under the lex order on terminal-varying tuples..."
**ASN-0047, K.μ⁻ case analysis (b)**: "`[S, 1, ..., 1, k₀]` then lies strictly between `[S, 1, ..., 1, k_min]` and `[S, 1, ..., 1, k']`"
**Problem**: The ASN uses "V-ordering" (or "the V-ordering on subspace S") throughout D-CTG★, the K.μ⁻ admissibility case analysis, the D-SEQ★ derivation, and K.μ~-FIX, but never explicitly defines it. The reader must infer from context that this is the lex order on tumblers (T1 of ASN-0034) restricted to depth-m_S positive tuples with first component S. The closed-interval-membership unpacking of D-CTG★ — and consequently the infinite-cardinality contradiction at Step 1 of the D-SEQ★ derivation — depends on this definition being precise.
**Required**: State the V-ordering definition explicitly at first use, anchoring it to T1: e.g., "the V-ordering on subspace S is T1 of ASN-0034 restricted to depth-m_S positive tuples with first component S." Without this, the precise content of "v_lo ≤ z ≤ v_hi under the V-ordering" is left to inference.

### Issue 2: Reachable-state invariants theorem mixes per-state and per-transition properties
**ASN-0047, "Coupling and isolation" section**: "**Theorem (Reachable-state invariants).** Every state reachable from Σ₀ by a finite sequence of valid composite transitions satisfies P0, P1, P2, P4 (Contains(Σ) ⊆ R), P6, P7, P7a, P8, S2, S3, S8a, S8-depth, S8-fin, D-CTG, and D-MIN."
**Problem**: P0, P1, P2 are per-transition predicates quantified over `Σ → Σ'` (`dom(C) ⊆ dom(C')`, `E ⊆ E'`, `R ⊆ R'`), not properties of a single state Σ. The inductive step says "Σ' satisfies P0," which is type-incorrect — P0 is a property of the step Σ → Σ', not the endpoint. The extended-state version handles this correctly by splitting into `ExtendedReachableStateInvariants` (per-state) and `ExtendedTransitionInvariants` (per-transition), with the explicit framing that "saying 'every reachable state satisfies P3★' would be type-incorrect — P3★ quantifies over `Σ → Σ'`." The four-component body theorem should adopt the same discipline rather than relying on the loose framing.
**Required**: Reframe the four-component theorem to separate per-state and per-transition conjuncts, analogously to the extended-state split. Move P0/P1/P2 to a companion per-transition theorem ("every valid composite transition between reachable states satisfies P0/P1/P2"), and let the per-state theorem carry only P4/P6/P7/P7a/P8/S2/S3/S8a/S8-depth/S8-fin/D-CTG/D-MIN.

### Issue 3: Missing concrete worked example for interior content replacement
**ASN-0047, "Elementary transitions" section (structural sufficiency discussion)**: "When the replaced V-position is `[S, 1, ..., 1, k₀]` with `k₀ < n_S` (some positions above it remain)... K.μ⁻ removes the suffix `{[S, 1, ..., 1, k] : k₀ ≤ k ≤ n_S}` (every position from k₀ to the maximum), and K.μ⁺ then re-adds the entire suffix `{[S, 1, ..., 1, k] : k₀ ≤ k ≤ n_S}` with the replaced position k₀ now carrying the new value and all other positions k ∈ {k₀+1, ..., n_S} carrying their previously mapped values."
**Problem**: Interior content replacement is described theoretically as a multi-position K.μ⁻ + K.μ⁺ pair where one new value induces n_S − k₀ + 1 positions removed and re-added. This is the most subtle composite operation in the ASN — the cardinality of the decomposition depends on the replacement position relative to the subspace maximum, and the D-CTG★/D-MIN★ admissibility at the intermediate state is non-obvious. The four worked examples (fork with insertion, ghost-base versioning, node baptism, link allocation/arrangement) exercise all seven elementary transitions, but none traces an interior replacement through its multi-position decomposition.
**Required**: Add a worked example exhibiting interior content replacement on a concrete arrangement (e.g., V_{s_C}(d) initially {[1,1] ↦ a, [1,2] ↦ b, [1,3] ↦ c, [1,4] ↦ d}; replace [1,2] with new value b'; trace through K.μ⁻ removing the suffix {[1,2], [1,3], [1,4]} and K.μ⁺ rebuilding {[1,2] ↦ b', [1,3] ↦ c, [1,4] ↦ d}). Verify D-CTG★/D-MIN★ at the intermediate state (where V_{s_C}(d) = {[1,1]}), the K.μ⁺ subspace amendment at each rebuilt position, J1★ on the new I-address b', and J1'★ vacuity on the unchanged re-added addresses.

## OUT_OF_SCOPE

(none — the ASN stays within its declared scope; deferred topics like withdrawal mechanism, version-management semantics, and non-T10a allocator admissibility are appropriately flagged in Open Questions and "Structural sufficiency and known gaps")

VERDICT: REVISE
