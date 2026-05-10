# Regional Review — ASN-0034/T4c (cycle 8)

*2026-04-22 05:54*

### T4b case-splits on `zeros(t) ∈ {0, 1, 2, 3}` without deriving exhaustion or citing it from T4c
**Foundation**: exhaustion `zeros(t) ∈ {0, 1, 2, 3}` is established in T4c's Exhaustion paragraph via iterated NAT-order trichotomy, NAT-discrete, and NAT-addcompat's strict successor inequality. T4b's Depends lists T0, NAT-zero, NAT-discrete, NAT-order, NAT-closure, NAT-sub, NAT-card, T4, and T4a — but not T4c and not NAT-addcompat.
**ASN**: T4b main text: "Let the zero positions in increasing order be `s₁ < s₂ < ... < s_k` (...), `k = zeros(t) ∈ {0, 1, 2, 3}`." T4b Definition: "Let `s₁ < s₂ < ... < s_k` enumerate the zero positions, with `k = zeros(t) ∈ {0, 1, 2, 3}`. The values are fixed by case on `k`: for `k = 0`, ...; for `k = 1`, ...; for `k = 2`, ...; for `k = 3`, ...". T4b Postconditions' presence pattern: "`zeros(t) = 0` → only `N` defined; `zeros(t) = 1` → `N, U` defined; `zeros(t) = 2` → `N, U, D` defined; `zeros(t) = 3` → all four defined."
**Issue**: T4b's case analysis and its presence pattern are exhaustive on `k ∈ {0, 1, 2, 3}` — the well-definedness conclusion depends on those four cases covering all T4-valid inputs. But T4-validity supplies only `zeros(t) ≤ 3`; collapsing this to `zeros(t) ∈ {0, 1, 2, 3}` is precisely the exhaustion that T4c derives, using (among other things) NAT-addcompat's strict successor inequality. T4b neither cites T4c (which is downstream) nor lists NAT-addcompat, and does not redo the exhaustion argument in-line. The four-case split and the presence pattern therefore rest on a step no dependency or proof in T4b underwrites.
**What needs resolving**: Either cite T4c for exhaustion (restructuring the DAG if needed), duplicate the exhaustion argument locally in T4b (adding NAT-addcompat to Depends), or recast T4b's case analysis to avoid pre-committing to `{0, 1, 2, 3}` (e.g., parameterised on any `k ∈ ℕ` with `0 ≤ k ≤ 3`, with the four-case presentation marked as instantiated rather than exhaustive).

### ℕ⁺ is defined twice — once in T4, once in T4b
**Foundation**: structural — a term should have one definitional site in the ASN, with later uses citing that site
**ASN**: T4 main text: "NAT-zero together with NAT-discrete (at `m = 0`) force every non-zero component to be strictly positive; **write `ℕ⁺ = {n ∈ ℕ : 0 < n}` for the strictly positive naturals.**" T4b main text: "**Writing `ℕ⁺ = {n ∈ ℕ : 0 < n}`**, each projection's image lies in the subset of `T` whose every component is in `ℕ⁺`".
**Issue**: `ℕ⁺` is introduced with the same defining equation in two different claims, both using the hedge "write/Writing … for". A reader encountering the T4b definition must decide whether it is a re-definition (in which case T4's earlier introduction is redundant) or a reminder (in which case the "Writing" framing overstates its role). Other notations introduced in T4 (e.g., `zeros(t)`) are not re-introduced in downstream claims; `ℕ⁺` is the only symbol double-defined.
**What needs resolving**: Pick one definitional site for `ℕ⁺` (most naturally T4, since that is where the strict-positivity argument first lands), and have T4b simply use the symbol without redefining it.

### T4c cites "NAT-zero's `0 ≤ zeros(t)`" but NAT-zero's axiom body no longer states `≤`
**Foundation**: NAT-zero's stated Axiom is `0 ∈ ℕ` and `(A n ∈ ℕ :: 0 < n ∨ 0 = n)`; its prose explicitly notes that the second clause is "phrased with the primitives `<` and `=` rather than the defined `≤`, so NAT-zero is self-contained and does not presuppose NAT-order."
**ASN**: T4c Exhaustion: "At `m = 0`: the case `zeros(t) < 0` is excluded by **NAT-zero's `0 ≤ zeros(t)`** via the exactly-one route just described". T4c Formal Contract Depends: "**NAT-zero (NatZeroMinimum) — supplies `0 ≤ zeros(t)` for the exhaustion step.**"
**Issue**: NAT-zero's axiom body was rephrased specifically to avoid `≤` (so that NAT-zero is self-contained and does not presuppose NAT-order). But T4c's body and Depends both cite NAT-zero as directly supplying `0 ≤ zeros(t)` — a formulation that now lives only in NAT-order's *definition* of `≤` applied to NAT-zero's disjunction. A precise reader auditing "which axiom in scope yields `0 ≤ zeros(t)`?" finds that no single axiom does; NAT-zero supplies `0 < zeros(t) ∨ 0 = zeros(t)` and NAT-order's definition of `≤` re-expresses that as `0 ≤ zeros(t)`. T4c attributes the combined result to NAT-zero alone.
**What needs resolving**: Either rephrase T4c's cite to "NAT-zero's `0 < zeros(t) ∨ 0 = zeros(t)` (equivalently `0 ≤ zeros(t)` via NAT-order's definition of `≤`)" and update T4c's Depends role for NAT-zero accordingly, or restore `0 ≤ n` to NAT-zero's axiom body (re-introducing the NAT-order presupposition the earlier rephrasing was chosen to avoid).

## Result

Regional review not converged after 8 cycles.

*Elapsed: 10867s*
