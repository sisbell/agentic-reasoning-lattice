# Cone Review — ASN-0034/TA-assoc (cycle 1)

*2026-04-17 22:40*

### TA-assoc Depends omits ActionPoint
**Foundation**: ActionPoint (sister property in this ASN; supplies the action-point function, the zeros-below-action-point fact `wᵢ = 0 for i < actionPoint(w)`, and the minimum-nonzero value `wₖ ≥ 1`)
**ASN**: TA-assoc (AdditionAssociative). Depends lists only "TumblerAdd, TA0, T3, NAT-addassoc."
**Issue**: The proof invokes ActionPoint facts repeatedly without citing them. Examples: "for `i < min(k_b, k_c)`, we have `i < k_b` (so `bᵢ = 0` by definition of action point) and `i < k_c` (so `sᵢ = bᵢ = 0`...)"; Case 1 sub-case "`s_{k_b} = b_{k_b} > 0`, since `k_b` is the action point of `b`"; Case 2 "both summands are positive action-point values"; Case 3 "since `k_c < k_b` gives `b_{k_c} = 0`." The `actionPoint(·)` function symbol and the variables `k_b = actionPoint(b)`, `k_c = actionPoint(c)` referenced in the preconditions and the postcondition `actionPoint(b ⊕ c) = min(k_b, k_c)` also have no licensed source without ActionPoint. This breaks the per-step citation discipline TumblerAdd itself enforces at structurally identical sites.
**What needs resolving**: TA-assoc's Depends must cite ActionPoint with the specific facts it consumes (action-point function definition, zeros-below-k, minimum-nonzero value at k), or the proof must be rewritten to route those facts through a cited source.

### TA-assoc Depends omits TA-Pos
**Foundation**: TA-Pos (PositiveTumbler; defines the predicate `Pos(·)`)
**ASN**: TA-assoc. Preconditions list "`Pos(b)`, `Pos(c)`"; Depends does not cite TA-Pos.
**Issue**: `Pos(·)` is an undefined symbol in TA-assoc without a citation to TA-Pos — the same gap TA0's Depends explicitly guards against ("without this citation `Pos` is an undefined symbol in the preconditions"). The proof's appeal to action-point existence for `b` and `c` also silently relies on `Pos(·)` being the predicate that ActionPoint consumes as input.
**What needs resolving**: Add TA-Pos to TA-assoc's Depends with the role it plays (supplying the predicate used in the preconditions and licensing ActionPoint's action-point existence for `b` and `c`).

### TA-assoc Depends omits NAT-closure
**Foundation**: NAT-closure (NatArithmeticClosureAndIdentity; supplies closure of ℕ under `+` and the additive identity `0 + n = n`)
**ASN**: TA-assoc. Two passages invoke NAT-closure's additive identity: action-point analysis of `s = b ⊕ c` — "If `k_b > k_c`: `s_{k_c} = b_{k_c} + c_{k_c} = 0 + c_{k_c} = c_{k_c} > 0`" — and Case 3 — "`s_{k_c} = b_{k_c} + c_{k_c} = 0 + c_{k_c} = c_{k_c}`". The closure-of-ℕ-under-+ clause is also implicitly consumed wherever the proof forms sums such as `a_k + b_k + c_k` and treats the intermediate result as a ℕ-valued component of a tumbler (required for the tumbler-membership conclusion inherited through T3 at the closing step).
**What needs resolving**: Cite NAT-closure in TA-assoc's Depends at the specific sites where `0 + x = x` is used and where closure of ℕ under `+` licenses ℕ-valued components of intermediate sums.

### TA-assoc Depends omits NAT-order
**Foundation**: NAT-order (NatStrictTotalOrder; supplies trichotomy on ℕ)
**ASN**: TA-assoc. The proof's exhaustive case analysis is "*Case 1: `k_b < k_c`* ... *Case 2: `k_b = k_c = k`* ... *Case 3: `k_b > k_c`*" — a three-way split over the ordering of `k_b` and `k_c` in ℕ.
**Issue**: Exhaustiveness of the three cases over ℕ is NAT-order's trichotomy. Without citing NAT-order, the case analysis appeals to background `<`/`=`/`>` on ℕ — the same appeal to unsourced background arithmetic that NAT-addassoc's rationale warns against and that TumblerAdd's dominance proof carefully avoids by routing each dichotomy through NAT-zero + NAT-order.
**What needs resolving**: Either cite NAT-order in TA-assoc's Depends for the trichotomy that makes Cases 1–3 exhaustive, or rephrase the case split so its exhaustiveness is discharged from an already-cited source.
