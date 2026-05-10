# Regional Review — ASN-0034/TA6 (cycle 3)

*2026-04-23 02:21*

### T4 over-invokes NAT-discrete for non-separator positivity
**Class**: REVISE
**Foundation**: T4 (HierarchicalParsing)
**ASN**: T4 prose: "NAT-zero together with NAT-discrete (at `m = 0`) force every non-zero component to be strictly positive". T4 Depends for NAT-discrete: "at `m = 0`, rules out `0 ≤ tᵢ < 1` under `tᵢ ≠ 0`, so the component `tᵢ` at every non-separator position is strictly positive (`0 < Nᵢ, 0 < Uⱼ, 0 < Dₖ, 0 < Eₗ`)".
**Issue**: The step `tᵢ ≠ 0 ⟹ 0 < tᵢ` for `tᵢ ∈ ℕ` follows from NAT-zero's axiom `(A n ∈ ℕ :: 0 < n ∨ 0 = n)` alone — instantiate at `tᵢ`, exclude the equality branch via `tᵢ ≠ 0`. This is precisely the clean path TA-PosDom's step (iii) now uses after the prior detour was removed. T4 instead routes the same conclusion through NAT-discrete's successor bound plus NAT-zero's `0 ≤ tᵢ` plus trichotomy — a reviser drift pattern already flagged elsewhere in this ASN, now sitting here in T4's dependency rationale. NAT-discrete remains genuinely needed by T4 for the Exhaustion Consequence's iterated `m < zeros(t) ⟹ m+1 ≤ zeros(t)` step, so it is not spurious as a whole; only the first stated role is.
**What needs resolving**: Either drop the non-separator-positivity role from NAT-discrete's rationale (keeping only the Exhaustion role) and rewrite the prose sentence to say "NAT-zero's disjunction instantiated at each non-separator component forces strict positivity", or exhibit a step that genuinely needs NAT-discrete's successor-bound form rather than NAT-zero's disjunction.

### T4 Exhaustion re-derives NAT-zero's exported Consequence
**Class**: OBSERVE
**Foundation**: T4 (HierarchicalParsing), NAT-zero (NatZeroMinimum)
**ASN**: T4 Exhaustion at `m = 0`: "the case `zeros(t) < 0` is excluded by `0 ≤ zeros(t)` via the exactly-one route just described".
**Issue**: NAT-zero already exports `(A n ∈ ℕ :: ¬(n < 0))` as a Consequence. Instantiated at `zeros(t)`, this directly gives `¬(zeros(t) < 0)` without any unfolding of `≤` or trichotomy exactly-one appeal. The Exhaustion proof rederives it through the "uniform mechanism" route because the author chose a stylistically uniform iteration; that choice is already flagged in Previous Findings. Noting here only that the base step of the iteration has a one-line shortcut that makes the uniform-mechanism framing visibly unnecessary.

VERDICT: REVISE
