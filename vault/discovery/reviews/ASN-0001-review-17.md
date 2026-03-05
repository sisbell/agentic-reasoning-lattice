# Review of ASN-0001

Based on Alloy run-2

## OUT_OF_SCOPE

### Topic 1: T0 UnboundedComponents — bounded scope cannot express unboundedness

The `check UnboundedComponents` returns SAT (counterexample found). T0 asserts that every component position is unbounded — for any value M, a tumbler exists with a component exceeding M. Alloy with `5 Int` (range -16 to 15) hits the integer ceiling: when a component is already at the maximum representable value, no atom in the finite scope can exceed it. The model's own comment acknowledges this expectation. The `run NonVacuity` returns SAT, confirming the model is not vacuous.

No spec issue. T0 is inherently unbounded and cannot be verified by bounded model checking.

### Topic 2: T5 ContiguousSubtrees — lexLTE does not implement T1's prefix convention

The `check ContiguousSubtrees` returns SAT (counterexample found). This is a modeling artifact caused by the `lexLTE` predicate, which uses zero-padded 4-component comparison rather than T1's lexicographic order with the prefix-less-than rule.

Under T1, a proper prefix is strictly less than any extension: `[1] < [1, 0]`. In the Alloy model, both tumblers zero-pad to `(1, 0, 0, 0)` and are treated as equal by `lexLTE`. This creates spurious counterexamples: a tumbler `b` shorter than prefix `p` can appear "between" two extensions of `p` under `lexLTE` (because `lexLTE` equates `b` with a genuine extension of `p`) while failing the `isPrefix` length check (`p.len <= b.len`). Concretely, with `p = [1, 0]`, `a = [1, 0, 0, 0]`, `b = [1]`, `c = [1, 0, 2, 0]`: `lexLTE[a, b]` holds (identical padded values), `lexLTE[b, c]` holds, `isPrefix[p, a]` and `isPrefix[p, c]` hold, but `isPrefix[p, b]` fails because `p.len = 2 > b.len = 1`. Under the real T1, `b = [1] < a = [1, 0, 0, 0]` strictly (prefix rule), so `a ≤ b` is false and the counterexample premise doesn't hold.

No spec issue. The Alloy model's order predicate doesn't faithfully encode T1. The `run NonVacuity` returns SAT, confirming non-vacuity.

### Topic 3: TA5 IncPreservesT4 — missing T4-validity premise on input

The `check IncPreservesT4` returns SAT (counterexample found). The assertion checks that when `zeros(t) + k - 1 ≤ 3`, the result satisfies `zeroCount(tPrime) ≤ 3`. For `k = 0`, the formula reduces to `zeros(t) ≤ 4`, which admits inputs that already violate T4 (e.g., a tumbler `[0, 0, 0, 0, 1]` with `zeros = 4`). Sibling increment preserves the zero count, so the output also has 4 zeros and fails `≤ 3`.

The ASN's prose is unambiguous: the verification section begins "We verify that TA5 preserves T4" and explicitly argues from T4-valid inputs. For `k = 0`, the text says "`zeros(t') = zeros(t) ≤ 3`" — the `≤ 3` bound comes from the premise that the input satisfies T4. The Alloy model's assertion omits this premise, encoding only the compact formula `zeros(t) + k - 1 ≤ 3` without the additional constraint `zeroCount[t] <= 3` in the antecedent.

No spec issue. The compact precondition formula is a necessary condition for the k > 0 case; the k = 0 case relies on T4-validity of the input, which the ASN's prose assumes. The Alloy assertion should include `zeroCount[t] <= 3` as an additional antecedent.

### Topic 4: TA5 IncStrictlyGreater and IncAgreesPrefix — passed

Both assertions return UNSAT (no counterexample within scope). TA5(a) and TA5(b) hold in the bounded model. Both non-vacuity runs (FindSibling, FindChild) return SAT.

### Topic 5: 27 properties passed bounded check

T1, T2, T3, T4, T6, T7, T8, T9, Prefix ordering extension, Partition monotonicity, T10, T10a, Global uniqueness, TA0, TA1, TA1-strict, TA-strict, TA2, TA3, TA4, Reverse inverse, TA6, TA7a, TA7b, T11, T12, TA8 — all returned UNSAT on checks (assertions hold within scope) with SAT on non-vacuity runs where applicable.

VERDICT: CONVERGED
