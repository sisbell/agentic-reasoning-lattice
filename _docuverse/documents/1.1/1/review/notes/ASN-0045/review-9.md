# Review of ASN-0045

## REVISE

### Issue 1: At-least-one enumeration is asserted, not justified, and omits the axiom it needs
**ASN-0045, Well-Definedness (At-least-one)**: "T4's axiom gives zeros(t) ≤ 3 (T4, ASN-0034), and zeros(t) ∈ ℕ (a cardinality over T0's carrier), so zeros(t) ∈ {0, 1, 2, 3}."
**Problem**: The step `zeros(t) ≤ 3 ∧ zeros(t) ∈ ℕ ⟹ zeros(t) ∈ {0,1,2,3}` is not licensed by order alone. Order plus `≤ 3` does not exclude values lying strictly between the numerals — a merely totally-ordered carrier (order-isomorphic to ℚ≥0) would have infinitely many elements ≤ 3. Ruling out intermediate values is exactly **NAT-discrete** (no natural strictly between `m` and `m+1`), which is neither cited nor invoked. The ASN cites NAT-order (trichotomy) in Partition's *Depends* but never the discreteness fact that the at-least-one direction actually rests on. Given this ASN's own per-step citation convention (mirroring T1/TA5, which discharge every ℕ fact explicitly), the bare "so zeros(t) ∈ {0,1,2,3}" is a hand-wave.
**Required**: Make the enumeration `{n ∈ ℕ : n ≤ 3} = {0,1,2,3}` explicit, citing NAT-discrete (or NAT-wellorder) as the axiom that excludes intermediate values, and add it to the *Depends* of Partition.

### Issue 2: Distinctness of the numerals 0,1,2,3 is mis-attributed to trichotomy
**ASN-0045, Well-Definedness (At-most-one)**: "by NAT-order's trichotomy (ASN-0034), distinct naturals are unequal, so e.g. `zeros(t) = 0` and `zeros(t) = 1` cannot both hold."
**Problem**: Trichotomy presupposes the two values are given; it does not establish that `0 ≠ 1` (or `1≠2`, `2≠3`). If `zeros(t)=0` and `zeros(t)=1` both held, transitivity of equality forces `0 = 1`, so the at-most-one argument depends on the *pairwise distinctness of the constructed numerals*. Those numerals are built via NAT-closure (`2 := 1+1`, `3 := 2+1`); their distinctness comes from the strict successor inequality `n < n+1` (**NAT-addcompat**) composed with NAT-order's irreflexivity, not from trichotomy. NAT-addcompat appears in no *Depends* list, yet it is the axiom that makes the successively-constructed numerals differ.
**Required**: Ground numeral distinctness in NAT-addcompat's `n < n+1` together with NAT-order (irreflexivity/transitivity), and add NAT-addcompat to the *Depends* of Document, Element, and Partition (wherever 2 and 3 and their distinctness are used).

## OUT_OF_SCOPE

None. The ASN stays within field-level naming and partition, and does not stray into the excluded operational topics.

VERDICT: REVISE
