# Review of ASN-0045

## REVISE

### Issue 1: Summary status contradicts the per-predicate Depends clauses

**ASN-0045, Summary table**: rows state Node/Document/Element are "derived from T4c" and Partition is partly "T4c supplies level names."

**Problem**: Each predicate's *Depends* clause says the opposite. Node: "T4c justifies the *node* level label only; it does no work in this biconditional and is not a proof dependency." Same for Document and Element. The predicates are *defined* by ASN-0045 as `T4-valid(t) ∧ zeros(t) = k`; their proof content comes from T4 (validity, `zeros ≤ 3`) and T0 (`zeros ∈ ℕ`), not from T4c. Labeling them "derived from T4c" in the Summary asserts a provenance the body explicitly denies. A reader using the Summary as the authoritative dependency record gets the wrong proof graph.

**Required**: Make the Summary status consistent with the Depends clauses — these are *definitions coined by ASN-0045*, with T4c supplying only the level *name*. Reserve "derived from T4c" (if anywhere) for the Account rename equivalence, which is the one place T4c does load-bearing work.

### Issue 2: Account rename equivalence invokes T4c without discharging T4c's preconditions

**ASN-0045, Properties Introduced → Account, Rename equivalence**: "T4c's *Postcondition* (the bijection clause) instantiated at t supplies `zeros(t) = 1 ⟺ t is a user address`."

**Problem**: T4c's preconditions are not just "t satisfies the T4 constraints" — they also include "t satisfies T4b (UniqueParse)." The derivation fixes only `T4-valid(t)` (the four T4 positional conditions) and then invokes T4c's postcondition directly. The step that `T4-valid(t)` actually entails T4c is applicable — i.e., that T4b holds at t (which requires T3 as well as the T4 constraints) — is left implicit. Given that this ASN explicitly guards against circularity elsewhere in *Well-Definedness*, the unstated precondition discharge is out of character and should be closed.

**Required**: Add one line discharging T4c's applicability: `T4-valid(t)` supplies the T4 positional constraints, and T3 (universal) plus those constraints supply T4b (UniqueParse), so T4c's bijection postcondition is licensed at t. Then chain to the rename equivalence as written.

## OUT_OF_SCOPE

None. The ASN stays within field-level predicate definitions and claims nothing in the excluded topic list.

VERDICT: REVISE
