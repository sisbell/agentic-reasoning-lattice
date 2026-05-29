# Review of ASN-0045

## REVISE

### Issue 1: At-least-one leaps from a bound to a four-element enumeration without discreteness
**ASN-0045, Well-Definedness (At-least-one)**: "Together `0 ≤ zeros(t) ≤ 3` forces `zeros(t) ∈ {0, 1, 2, 3}`. ... Hence at least one of the four equalities zeros(t) = k holds."

**Problem**: The step from `0 ≤ zeros(t) ≤ 3` (with `zeros(t) ∈ ℕ`) to the *disjunction* `zeros(t) = 0 ∨ 1 ∨ 2 ∨ 3` is not licensed by the bound alone. Ruling out a natural number strictly between the enumerated values requires the discreteness of ℕ (NAT-discrete: `m ≤ n < m+1 ⟹ n = m`), applied to enumerate the bounded segment. The ASN cites T4 for the upper bound and T0 for the lower bound with deliberate care, then silently performs the enumeration — exactly the per-step gap its own citation convention forbids. As written, "forces ∈ {0,1,2,3}" treats the four-element set as if interchangeable with the interval `{n ∈ ℕ : 0 ≤ n ≤ 3}` without proving the equality.

**Required**: Cite NAT-discrete (or an explicit finite-induction enumeration) to discharge `0 ≤ n ≤ 3 ∧ n ∈ ℕ ⟹ n ∈ {0,1,2,3}`, and add NAT-discrete (and NAT-closure, which grounds the numerals 1, 2, 3 used in the disjunction) to Partition's Depends list.

### Issue 2: Account's rename-equivalence derivation invokes T4b and T3 but omits them from Depends
**ASN-0045, Properties Introduced (Account, Depends)**: "*Depends.* T0, T4, T4c, NAT-closure (the constant 1)."

**Problem**: The Account postcondition's rename equivalence is explicitly derived using two foundation facts not listed in Depends: "T4c's preconditions are the T4 positional constraints together with T4b (UniqueParse)... T3 (CanonicalRepresentation, universal) together with those same constraints supplies T4b at t." Both T4b and T3 are load-bearing in discharging T4c's applicability at `t`, yet neither appears in the Depends list. For an ASN that otherwise tracks dependencies per-step (e.g., Node disclaiming T4c, numerals grounded in NAT-closure), this omission is a genuine inconsistency.

**Required**: Add T4b and T3 to Account's Depends list, scoped to the rename-equivalence postcondition.

## OUT_OF_SCOPE

None. The ASN stays within field-level predicate classification and does not stray into the listed out-of-scope topics.

VERDICT: REVISE
