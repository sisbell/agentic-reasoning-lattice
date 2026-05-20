# Review of ASN-0047

## REVISE

### Issue 1: Worked example uses "non-vacuously" parenthetical that obscures the claim
**ASN-0047, Worked example: fork with subsequent insertion**: "V-position `[1,3]` has first component 1 and depth 2, matching `[1,1]` and `[1,2]` (S8-depth, non-vacuously: shared first component)"
**Problem**: The parenthetical "non-vacuously: shared first component" conflates two distinct facts (S8-depth says positions share depth within a subspace; the shared-first-component fact identifies subspace membership via `subspace(v)`). S8-depth's substantive content here is uniform depth = 2 within `s_C`; "non-vacuously" is not a defined term and the reader cannot tell what was being contrasted.
**Required**: Rewrite as "V-position `[1,3]` has subspace `subspace([1,3]) = 1 = s_C` and depth 2, matching `[1,1]` and `[1,2]` — S8-depth holds at the common depth `m_{s_C} = 2`."

### Issue 2: Matrix entry "restriction of decomposition" for S8★ under K.μ⁻ understates the discharge
**ASN-0047, Verification matrix in ExtendedReachableStateInvariants, S8★ row, K.μ⁻ column**: "restriction of decomposition"
**Problem**: A restriction of a pre-state decomposition may break correspondence runs (a length-`n` run with a missing interior element no longer satisfies S8's shift-lockstep condition (b)). The cell is correct only because the trivial length-1 decomposition is always available — the same fall-back the link-subspace cell relies on — but the matrix entry does not say so, making the discharge appear stronger than it is.
**Required**: Replace with "restriction to trivial length-1 decomposition on survivors per subspace" (or expand inline: "restriction; trivial length-1 form survives any contraction").

### Issue 3: K.μ⁻ admissible contraction shape — quantifier ambiguity in cited per-state invariants
**ASN-0047, K.μ⁻ admissible contraction shape, Reverse direction**: "D-CTG★ and D-MIN★ at Σ' are part of the hypothesis being characterized — they are not preserved by arbitrary restriction…but are supplied by the post-state characterization being shown equivalent"
**Problem**: The body of the proof writes "D-SEQ★ applied at the post-state gives V_S(d') = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}" — but the proof aims to *characterize* arbitrary admissible contractions, so the post-state invariants must be hypothesised on the *candidate* `M'(d)`, not on `M'(d)` of the constructive form. The status-clarifying paragraph mentions this only after the derivation step that consumes it.
**Required**: At the start of the reverse direction, state explicitly: "Hypothesise that the candidate post-state `M_cand(d)` (with `dom(M_cand(d)) ⊆ dom(M(d))` and value-preservation on survivors) satisfies D-CTG★ + D-MIN★ + D-SEQ★ + the elementary-preserved invariants. We show `M_cand(d)` equals `M(d) ↾ R` for some per-subspace `R` of the constructive form." Then run the bijection-via-φ_S argument.

### Issue 4: GlobalLineage proof for link addresses introduces unstated TA5(d) length identity at k=1
**ASN-0047, GlobalLineage, link-address case (iii)**: "Step i + 1 (i ≥ 1): split on kᵢ₊₁. If kᵢ₊₁ > 0: TA5(b) preserves positions 1..#tᵢ exactly…and sig(tᵢ₊₁) > #tᵢ ≥ #origin(ℓ) + 2 > #origin(ℓ)."
**Problem**: The chain `sig(tᵢ₊₁) > #tᵢ ≥ #origin(ℓ) + 2` rests on (a) TA5(d)'s length-extension `#tᵢ₊₁ = #tᵢ + kᵢ₊₁` at `kᵢ₊₁ > 0`, plus (b) the placement of `tᵢ₊₁`'s new nonzero component at position `#tᵢ + kᵢ₊₁` (the rightmost position) — both needed to identify `sig(tᵢ₊₁)`. Neither is invoked by name; the prose jumps from "TA5(b) preserves positions 1..#tᵢ" to the `sig` conclusion without citing the new-position-value step.
**Required**: Insert one line: "TA5(d) at kᵢ₊₁ > 0 places the new value 1 at position #tᵢ + kᵢ₊₁, the new rightmost nonzero component, so sig(tᵢ₊₁) = #tᵢ + kᵢ₊₁ > #tᵢ."

### Issue 5: K.μ~ dependency chain — Step (A) names L14 as a premise, but the body argument uses only the disjointness `dom(C) ∩ dom(L) = ∅`
**ASN-0047, Decomposition of K.μ~, Case `s_C → s_L` / Case `s_L → s_C`**: "M'(d)(π(v)) ∈ dom(C) ∩ dom(L) = ∅ by L14 — contradiction"
**Problem**: L14 is named ten times across the dependency chain and case analysis; in each invocation the substantive premise consumed is the set-equality `dom(C) ∩ dom(L) = ∅`, not L14's full content. The body alternates between "L14" and "L14 at both states" without distinguishing the per-state invariant from its evaluation in a contradiction. The reader has to chase the chain in *Link store and extended system state* to confirm L14 is preserved at both `Σ` and `Σ'`.
**Required**: At the head of *Decomposition of K.μ~*, state explicitly: "L14 at both states (`dom(C) ∩ dom(L) = ∅` at Σ and `dom(C') ∩ dom(L') = ∅` at Σ', both Class (a) per-state invariants by ExtendedReachableStateInvariants induction)."

## OUT_OF_SCOPE

### Topic 1: Withdrawal/tombstoning mechanism for interior link removal
The Open Questions section already identifies this: under D-CTG★/D-MIN★, K.μ⁻ admits only suffix truncation on the link subspace, but Nelson's tombstoning intent (LM 4/9) calls for interior-link withdrawal preserving trailing link V-positions. Out of scope by explicit acknowledgement; would require a separate status-flag or retraction-link mechanism in a future ASN.

### Topic 2: External node-allocation registry protocol
NodeUniqueAllocation and NodeRegistryBootstrap are stated as axiomatic external commitments. The registry's issuing protocol, persistence model, and concurrency discipline are deferred to future ASN work, as the Open Questions section notes.

### Topic 3: K.δ k = 1 on accounts (account-level version chains)
The current K.δ k = 1 precondition `t ∈ E_doc` restricts version creation to documents. The Open Questions section already flags whether account-level k = 1 should be admitted; new territory for a future ASN.

VERDICT: REVISE
