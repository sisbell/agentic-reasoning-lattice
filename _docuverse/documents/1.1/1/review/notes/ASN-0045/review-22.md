# Review of ASN-0045

I read this as a definitional ASN: it coins four one-place level predicates over T4-valid tumblers, plus the Partition invariant and its off-domain complement. I checked every derivation, the boundary split (valid vs. invalid subdomain), the examples, and the dependency citations against the foundations.

## REVISE

No REVISE items. Specifically, I verified:

- **T4-valid coinage is justified, not a reinvention.** The ASN explicitly notes T4 introduces no one-place predicate symbol, then pins `T4-valid(t)` to T4's exact four clauses (`zeros(t) ≤ 3 ∧ no-adjacent-zeros ∧ t₁ ≠ 0 ∧ t_{#t} ≠ 0`). It uses the foundation, naming what the foundation left unnamed.

- **The user→account rename is documented and derived, not silently divergent.** The "Rename equivalence" postcondition derives `Account(t) ⟺ t is a user address per T4c` explicitly, discharging T4c's preconditions (T4 constraints from `T4-valid(t)`, T4b from T3 + those constraints) before chaining the biconditionals. The `U` projection symbol is correctly left unbound.

- **At-least-one is not circular and not hand-waved.** The ASN flags and avoids the circularity of reading `{0,1,2,3}` off T4c's bijection domain, instead enumerating `0 ≤ n ≤ 3 ∧ n ∈ ℕ ⟹ n ∈ {0,1,2,3}` via NAT-order trichotomy at the boundaries, NAT-discrete to void the interior gaps, and NAT-addcompat for numeral consecutiveness. Airtight.

- **At-most-one rests on the right premises.** Disjointness is derived from functionality of `zeros(t)` plus pairwise distinctness of 0,1,2,3 in ℕ — correctly *not* routing through T4c's level-injectivity, since the predicates compare zero-counts directly.

- **Boundary coverage is complete.** Partition covers `T4-valid(t)`; Off-Domain Vacuity covers `¬T4-valid(t)` by conjunction elimination on the shared left conjunct. Together they classify all of T (exactly-one on the valid subdomain, exactly-zero off it). The counter-example `[3,0,0,5]`-style case (zeros = 2 but invalid) is correctly falsified by all four predicates.

- **Concrete examples present and correct.** Both the positive table (one level per row) and the four counter-examples (one per violated T4 clause) check out: `[7]`→Node, `[7,0,3]`→Account, `[7,0,3,0,5]`→Document, `[7,0,3,0,5,0,1]`→Element; `[1,0,1,0,1,0,1,0,1]` has zeros = 4 > 3.

- **No non-foundation cross-references.** Every citation is to ASN-0034 (foundation) — T0, T3, T4/T4a/T4b/T4c, NAT-*. Permitted.

## OUT_OF_SCOPE

None. The ASN stays within its declared scope (predicate definitions and their partition), correctly deferring field-component projection and any operation-level use to downstream work.

VERDICT: CONVERGED
