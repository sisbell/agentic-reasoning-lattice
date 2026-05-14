# Review of ASN-0045

## REVISE

### Issue 1: At-most-one step cites T4c's disjointness without bridging from label predicates to zeros equalities
**ASN-0045, *Well-Definedness***: "By T4c's Pairwise extensional disjointness, the four cases `zeros(t) = k` for distinct k cannot both hold."
**Problem**: T4c's *Pairwise extensional disjointness* is stated for the four **label predicates** (`t is a node address`, `t is a user address`, `t is a document address`, `t is an element address`), not for `zeros(t) = k` equalities. The ASN treats them as the same fact but never shows the bridge. Inside T4c, label disjointness is itself derived (via *Injectivity*) from the substitutivity-of-`=` fact that distinct values can't both equal `zeros(t)`; lifting back to zeros equalities requires reapplying T4c's biconditionals or going around T4c entirely.
**Required**: Either (a) derive at-most-one directly: zeros is a function (T4 + NAT-card place `zeros(t) ∈ ℕ` single-valued), and T4c's *Injectivity* gives `0, 1, 2, 3` pairwise distinct, so by substitutivity `zeros(t) = i ∧ zeros(t) = j ⟹ i = j` contradicting distinctness — no T4c disjointness needed; or (b) explicitly chain through T4c's biconditionals `(zeros(t) = k ↔ Lₖ(t))` for each k, apply T4c's label disjointness, and transfer back.

### Issue 2: Account rename equivalence asserted without derivation
**ASN-0045, *Properties Introduced*, Account postconditions**: "*Rename equivalence:* `(A t : T : T4-valid(t) :: Account(t) ⟺ t is a user address per T4c)`."
**Problem**: The biconditional is stated as a postcondition but no derivation is shown. The standards require claims labelled as derived to have an explicit derivation.
**Required**: Show the chain: fix T4-valid(t); Account's definition collapses to `zeros(t) = 1` under the T4-valid antecedent; T4c's biconditional `(A t ∈ T : t is T4-valid :: zeros(t) = 1 ↔ t is a user address)` instantiated at t gives `zeros(t) = 1 ⟺ t is a user address`; chain biconditionals.

### Issue 3: Numeral constants 2 and 3 misattributed in Depends
**ASN-0045, *Properties Introduced*, Document and Element**: "*Depends.* T0, T4, T4c, NAT-closure (the constant 2)." / "*Depends.* T0, T4, T4c, NAT-closure (the constant 3)."
**Problem**: NAT-closure axiomatizes only `1 ∈ ℕ` and addition closure. The numerals `2 := 1 + 1` and `3 := 2 + 1` are defined in T4's *Numerals* sub-clause (T4 is already in Depends). The annotation as stated suggests NAT-closure supplies the constants directly, which it does not.
**Required**: Reattribute the constants 2 and 3 to T4's *Numerals* clause; keep NAT-closure cited as the source of `1 ∈ ℕ` and addition closure that grounds those numeral definitions in ℕ.

VERDICT: REVISE
