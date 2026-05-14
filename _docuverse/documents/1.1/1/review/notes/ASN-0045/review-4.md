# Review of ASN-0045

## REVISE

### Issue 1: `Bool` type referenced as if foundation-defined
**ASN-0045, Hierarchy Level Definitions**: "Each predicate has type `T → Bool` on the tumbler carrier T (T0, ASN-0034)."
**Problem**: T0 defines the carrier `T`, the length operator, and component projection — it does not introduce a `Bool` type. The foundation is unsorted first-order logic over ℕ and T; there is no `Bool` codomain to cite.
**Required**: Drop the `T → Bool` typing, or restate as "each predicate is a one-place proposition on T." If a typed framing is wanted, ground it explicitly rather than attributing it to T0.

### Issue 2: "Decidable" claim has no foundation basis
**ASN-0045, Hierarchy Level Definitions**: "T4-valid(t) is decidable (T4, ASN-0034)"
**Problem**: T4's contract states the validity predicate but does not establish decidability — a computational property not addressed by any ASN-0034 dependency. The argument for totality here is reaching for a property the foundation does not provide.
**Required**: Replace the decidability appeal with what T4 actually delivers: T4-valid is a predicate on T (so `T4-valid(t)` is a well-formed proposition for every t : T) and zeros : T → ℕ is total (T4 + NAT-card). That suffices to show the conjunctions are well-formed without invoking decidability.

### Issue 3: `succ(0)` notation introduces a function the foundation does not define
**ASN-0045, Properties Introduced (Account)**: "NAT-closure (the constant 1 = succ(0))"
**Problem**: NAT-closure posits `1 ∈ ℕ` directly as a primitive — there is no `succ` function in the foundation. The "addition-based successor" in NAT-closure is the term `n + 1`, not `succ(n)`. Equating `1 = succ(0)` reaches outside the foundation's vocabulary.
**Required**: State the dependency as "NAT-closure (`1 ∈ ℕ`)" or "NAT-closure (the constant 1)" — drop the `succ(0)` gloss.

### Issue 4: NAT-card listed as dependency without consumption
**ASN-0045, Properties Introduced (Partition)**: "*Depends.* ..., NAT-card (cases on natural-number equality)."
**Problem**: NAT-card axiomatizes the cardinality operator `|·|` over finite subsets of initial segments of ℕ. It is not consumed by the Partition derivation. The proof in *Well-Definedness* uses T4c's Exhaustion (discrete enumeration) and Pairwise extensional disjointness — no cardinality counting. "Cases on natural-number equality" is generic logic, not what NAT-card supplies.
**Required**: Remove NAT-card from Partition's *Depends*, or replace with the specific axiom actually consumed (none appears needed beyond T4c).

### Issue 5: Counter-example row 4 framing is inconsistent with the table's structure
**ASN-0045, Examples (counter-examples table, row 4)**: "[1, 0, 1, 0, 1, 0, 1, 0, 1] | zeros(t) = 4 > 3 | even if parseable, no k ∈ {0,1,2,3} matches; T4 forbids this"
**Problem**: The hedge "even if parseable" is incoherent — being T4-valid IS what "parseable" means in this framework, and the `zeros(t) ≤ 3` clause is part of T4's validity definition. So this tumbler is unambiguously T4-invalid, and the explanation should mirror the other rows: "T4-valid fails (zeros(t) = 4 > 3 violates T4(i)); each predicate's left conjunct is false." The current framing suggests there is a "parseable but unclassified" case, which there is not.
**Required**: Rewrite the cell parallel to the first three rows — name the violated T4 conjunct directly and conclude all four predicates false via the T4-valid conjunct.

### Issue 6: "equality on ℕ is functional via NAT, ASN-0034" — vague citation, redundant work
**ASN-0045, Well-Definedness, At-most-one**: "(equality on ℕ is functional via NAT, ASN-0034)"
**Problem**: Two problems. First, "via NAT" without naming a specific axiom is vague — NAT-* is twelve distinct axioms, and the functional nature of equality is generic logic, not a specific NAT axiom. Second, the parenthetical is redundant: T4c's Pairwise extensional disjointness directly delivers "no two of the four label predicates hold simultaneously on T4-valid t" — which is precisely the at-most-one conclusion needed. The detour through ℕ-equality functionality adds nothing.
**Required**: Delete the parenthetical. T4c's disjointness postcondition is the complete justification.

### Issue 7: Forward-only postconditions for individual predicates
**ASN-0045, Properties Introduced (Node, Account, Document, Element)**: e.g., `(A t : T : Node(t) ⟹ T4-valid(t) ∧ zeros(t) = 0)`
**Problem**: Each predicate's *Postcondition* states only the forward direction of an `≡` (definitional biconditional). Since `Node(t) ≡ T4-valid(t) ∧ zeros(t) = 0` is the *Definition*, the biconditional is automatic — but stating only one direction as the postcondition is asymmetric and leaves a reader wondering whether the converse is intended. The Account entry breaks symmetry by adding a *Rename equivalence* in iff form, then reverts to one-way for the structural postcondition.
**Required**: Either state the iff explicitly (`Node(t) ⟺ T4-valid(t) ∧ zeros(t) = 0`) or omit the postcondition entirely on the grounds that it is the unfolding of the definition. Pick one form and apply it uniformly across all four predicates.

### Issue 8: Partition postcondition restates the Definition verbatim
**ASN-0045, Properties Introduced (Partition)**: "*Postcondition.* Same as Definition; carried as a corollary of T4c."
**Problem**: A postcondition that literally equals the Definition is not a postcondition — it is the claim itself. If Partition is genuinely a derived statement, the postcondition slot should record a consequence (e.g., for any t : T, at most one of the four predicates holds; for T4-valid t, exactly one holds). If it is truly definitional, then the *Definition* alone suffices and the *Postcondition* slot should record what is *proved* (the Well-Definedness derivation), which is the forward direction of `T4-valid(t) ⟹ exactly-one-of(...)`.
**Required**: Distinguish definition from theorem. The exactly-one-of biconditional on T4-valid t is what's derived; state that as the postcondition with explicit reference to T4c's Exhaustion and Pairwise extensional disjointness as the two ingredients.

## OUT_OF_SCOPE

None — the ASN does not stray into the listed scope exclusions.

VERDICT: REVISE
