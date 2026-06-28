## Audit Narrative

**S0, AX-1, AX-2, S1, S2**: All axioms or immediate structural consequences. S1's one-step proof from S0 is clean; S2 follows directly from the partial-function typing. No issues.

**S3**: Induction on transition sequences is correct. The base case is vacuous by AX-1. The inductive step's two-case split covers its stated domain: the inherited case discharges via J0 + S1, the new/redirected case via AX-2. The domain guard on `Σ.M(d)(v)` in AX-2's antecedent is written correctly. Formal contracts and Depends list are complete.

**S8a, S8-fin, S8-depth**: All three are design posits, explicitly labeled as such. Each justifies its finiteness/well-formedness expression. S8-fin's bijection formulation correctly avoids the out-of-scope `|·|` operator. No soundness issues.

**OrdShiftHom part (a)**: The copy-region argument is tight. Since `m ≥ 2`, position 1 lies strictly below the action point, so `r₁ = v₁`, and the `subspace` projection chain closes immediately. ✓

**OrdShiftHom part (b)**: The component bounds are correctly assembled — copy-region components from the S8a precondition, action-point component from OrdinalShift's exported postcondition `shift(v,n)_{#v} = v_{#v} + n ≥ 1`. The proof then explicitly unfolds T4's zeros definition and invokes NAT-card's `|∅| = 0` to close `zeros(r) = 0`. The expressive path is correct, but the Depends list has a gap (see finding below).

**S8 (CorrespondenceRunPartition)**: The lockstep-successor construction is sound. `succ` is a well-defined partial function: the domain check precedes the application, and both `shift(v,1)` and `shift(M(d)(v),1)` are well-typed before the lockstep-image condition is evaluated. Injectivity of `succ` routes through shift's frame (`#shift(t,1) = #t`, unconditionally from TA0) and then TS2 — the formal contract correctly distinguishes this from S8-depth's domain-restricted quantifier. Acyclicity follows from TS4 + T1 irreflexivity; the chain decomposition terminates by S8-fin. The induction for the displacement identity handles `i = 0` via the convention and `i ≥ 1` via TS3 (both shift amounts ≥ 1). Maximality and uniqueness follow from the forced forward/backward walks. The partition proof's coverage, disjointness, and finiteness are all established. The `shift(t,0) := t` convention is declared as a local axiom and used only at `k = 0`, consistent with OrdinalShift's `n ≥ 1` domain.

---

### OrdShiftHom Depends missing NAT-zero/NAT-order/NAT-closure for the zeros closure in part (b)
**Class**: REVISE
**Foundation**: OrdinalDisplacement (OrdinalDisplacement) — cites both NAT-order and NAT-closure explicitly for the identical inference "n ≥ 1 ⟹ n ≠ 0"
**ASN**: OrdShiftHom (OrdinalShiftPreservation), Depends list; part (b) proof: "since every rᵢ ≥ 1, no index meets the filter rᵢ = 0, so the counted index set is empty"
**Issue**: The proof explicitly unfolds T4's zeros count `zeros(r) = |{i : 1 ≤ i ≤ #r ∧ rᵢ = 0}|` and then concludes the indexed set is empty because every `rᵢ ≥ 1`. That step requires the inference `rᵢ ≥ 1 → rᵢ ≠ 0`. The chain is: `1 ≤ rᵢ` (definition of `≥`, NAT-order) + `0 < 1` (NAT-closure consequence) → transitivity gives `0 < rᵢ` (NAT-order) → `rᵢ ≠ 0` (irreflexivity, NAT-order). Equivalently, NAT-zero's `(A n ∈ ℕ :: 0 < n ∨ 0 = n)` at `n := rᵢ` combined with `rᵢ ≠ 0` gives `rᵢ > 0` directly. Neither NAT-zero nor NAT-order nor NAT-closure appears in OrdShiftHom's Depends list. The foundation claim OrdinalDisplacement (ASN-0034) cites both NAT-order and NAT-closure explicitly for the structurally identical step `n ≥ 1 ⟹ n ≠ 0`. OrdShiftHom performs the same arithmetic silently.
**What needs resolving**: Add NAT-zero (for the disjunction `0 < rᵢ ∨ 0 = rᵢ`, ruling out `rᵢ = 0` once `rᵢ ≥ 1`) or NAT-order + NAT-closure (for the equivalent transitivity chain `0 < 1 ≤ rᵢ → 0 < rᵢ`) to OrdShiftHom's Depends. Update the description for the added entry to identify the inference step it grounds.

---

### S8-depth prose "no claim in this ASN consumes that non-text scope" contradicts S8's formal-contract Depends
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: S8-depth (FixedDepthVPositions), body text: "No claim in this ASN consumes that non-text scope — … S8's chain decomposition draws its per-position depth from `shift`'s frame rather than from this quantifier"
**Issue**: S8's formal-contract Depends entry for S8-depth reads: "supplies the subspace-wide common depth `m`: for `v ∈ dom(M(d))`, `m = #v` is the depth shared by every active position in v's subspace." S8's proof body cites S8-depth explicitly for that characterization — "write `m = #v`, which by S8-depth is the common depth shared by every active position in v's subspace" — and `dom(M(d))` is not restricted to text positions. The prose note's claim that "no claim in this ASN consumes that non-text scope" is directly contradicted by S8's citation of S8-depth for the subspace-wide common depth across all subspaces. The qualifying clause ("S8's chain decomposition draws its per-position depth from `shift`'s frame") is correct for the per-position equality `#shift(v,1) = #v` (an unconditional TA0 property), but S8 additionally uses S8-depth for the subspace-wide framing, which does consume the non-text scope. Formal contracts are accurate; the imprecision is in the prose note.
**What needs resolving**: Narrow the prose to what is accurate: that no proof step in S8 depends on the *evidentiary grounding* of S8-depth for non-text subspaces (as opposed to its posited truth), and that S8 does use S8-depth's quantifier for the subspace-wide common-depth framing across all subspaces. The current wording risks misleading a future author who reads it as license to use S8-depth for non-text positions without acknowledging the grounding gap.

VERDICT: REVISE