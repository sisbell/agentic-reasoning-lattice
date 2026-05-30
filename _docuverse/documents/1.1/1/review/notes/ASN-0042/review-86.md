# Review of ASN-0042

## REVISE

### Issue 1: O7(c) claims condition (vii) is "trivially satisfied at Σ'" but never derives it
**ASN-0042, Delegation / O7 Formal Contract**: "(c) the delegation relation is satisfiable with `π'` as delegator for any sub-prefix `p''`... at every state at which O15 conditions (ii), (vi), and (vii) hold for `p''`. All three trivially satisfied at `Σ'`."
**Problem**: The proof body verifies conditions (i), (ii), and (vi) at `Σ'`, then says only that "(ii) and (vii) require re-checking" at later states — it never establishes (vii) (freshness, `p'' ∉ Σ'.B`) at `Σ'` itself. For an arbitrary `p''` with `pfx(π') ≺ p''`, freshness at `Σ'` is not obvious: the delegation transition baptizes `pfx(π')` (O18), but the absence of *descendants* of `pfx(π')` from `Σ'.B` is not shown. The Formal Contract asserts triviality for a condition the proof leaves undischarged.
**Required**: Either derive `(vii)` at `Σ'` for arbitrary `p''` (e.g., from B1/contiguity reasoning that no child stream under the just-baptized `pfx(π')` can pre-exist), or drop (vii) from the "trivially satisfied at Σ'" claim and state that the right to delegate `p''` is conditional on freshness at the prospective delegation state in all cases.

### Issue 2: The "descent is the principal's organizational choice, not a requirement of O10" claim appears three times
**ASN-0042, O10 postcondition (c) prose / "Forking at greater depth" / Worked Example**: "Content-bearing depth... is not guaranteed by O10 itself; it requires further organizational baptisms..."; "the descent is `π`'s organizational choice, not a requirement of O10"; "Any further descent to place content inside `a'` is `π`'s organizational choice, not a requirement of O10."
**Problem**: The same fact is stated three times in three sections. Under the anti-bloat classifier this is duplicate prose the reader must skip past.
**Required**: State the namespace-vs-content-depth caveat once (in O10's contract) and delete the restatements.

### Issue 3: O8 duplicates the "owner may be π' or a sub-delegate, but never returns to π" remark
**ASN-0042, O8 formulation discussion and O8 proof closing note**: formulation: "permitting the delegate `π'` to sub-delegate... the address leaves `π'`'s effective ownership but does not return to `π`." Proof: "The effective owner may be `π'` itself, or it may be a sub-delegate `π''`... the address leaves `π'`'s effective ownership but does not return to `π`."
**Problem**: Two near-identical paragraphs in the same property say the same thing in different words.
**Required**: Keep the in-proof note (which carries the `#pfx(π'') > #pfx(π') > #pfx(π)` argument) and remove the redundant lead-in remark.

### Issue 4: AccountField's Formal Contract repeats the prose well-formedness derivation
**ASN-0042, AccountField (The Account-Level Boundary)**: the prose paragraph "Well-formedness of `acct(a)` follows from FieldStructure. When `zeros(a) = 0`... When `zeros(a) = 1`... When `zeros(a) ≥ 2`..." is then re-derived in the Formal Contract postconditions (c) and (d) with parenthetical "(Justification: ...)" clauses covering the identical cases.
**Problem**: The case analysis (`zeros = 0`, `= 1`, `≥ 2`) is given twice — once as prose proof, once as parenthetical justification in the contract. Structural slots should not re-run the proof.
**Required**: Keep the derivation in one place; reduce the postcondition entries to bare claims referencing the single derivation.

### Issue 5: O10 Non-coverage analysis excludes a case the standing prefix invariant already forbids
**ASN-0042, O10 Non-coverage analysis, Form B**: "Length `#pfx(π_i) = #pfx(π) + 1` (so `pfx(π_i) = pfx(π).0`, a trailing zero with empty user field) is excluded by T4 validity (condition (v))."
**Problem**: Every principal prefix is T4-valid as a standing invariant (O1a/T4 maintained in every reachable state). `pfx(π_i) = pfx(π).0` is a trailing-zero tumbler that can never be a principal prefix in the first place. The paragraph imagines and rebuts a configuration the carrier (`π_i ∈ Π_Σ`) already excludes — reviser drift.
**Required**: Drop the explicit `pfx(π).0` exclusion; cite the standing T4 invariant on principal prefixes once and proceed to `#pfx(π_i) ≥ #pfx(π) + 2`.

### Issue 6: Defensive terminology/disambiguation meta-prose in two structural slots
**ASN-0042, State Axioms Notation and Worked Example seed/allocate paragraph**: the Notation block distinguishes `Σ.B` monotonicity "distinct from T8's allocator-domain monotonicity"; the Worked Example contains a full paragraph adjudicating the verbs "seed" vs "allocate" ("Bootstrap seeding is a property of `Σ_0` itself... we therefore reserve the verb 'allocate' for transition-induced entries...").
**Problem**: Both are defensive disambiguation that does not advance the argument — terminology bookkeeping a precise reader works around.
**Required**: Compress the T8 distinction to a parenthetical (if kept at all) and reduce the seed/allocate paragraph to the one operative fact: `a₁ ∈ Σ₀.B` under `π_N`'s coverage at genesis.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer, cross-node federation, domain density
**Why out of scope**: These are genuine future-ASN questions (effect of `ω` diverging from inalienable provenance after transfer; federation invariants consistent with O9; whether domains must be gap-free). The ASN already records them under Open Questions rather than half-specifying them, which is the correct treatment.

VERDICT: REVISE
