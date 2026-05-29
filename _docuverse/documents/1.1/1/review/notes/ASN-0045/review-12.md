# Review of ASN-0045

## REVISE

### Issue 1: Partition's Depends omits NAT-closure, which its proof uses directly

**ASN-0045, Properties Introduced — Partition, Depends**: lists "Node, Account, Document, Element, Z0, T4, T4c, NAT-discrete, NAT-addcompat, NAT-order" — NAT-closure is absent.

**Problem**: The Partition derivation uses NAT-closure directly, not merely through the predicate definitions:
- At-least-one: the branch "`zeros(t) < 1`, then `0 ≤ zeros(t) < 0 + 1`" rewrites `1` as `0 + 1`, which is NAT-closure's additive identity (`0 + n = n`); the derived form `m < n ⟹ m + 1 ≤ n` constructs the successor `m + 1` via NAT-closure's successor closure.
- At-most-one: the prose explicitly says the numerals are "`2 := 1 + 1`, `3 := 2 + 1`, via NAT-closure (ASN-0034)."

So the Well-Definedness prose cites NAT-closure while the formal Depends slot drops it — an internal inconsistency in a project that enforces per-step citation. By the same convention that drives T0/T1/TA5 direct citation, NAT-closure is a direct premise of Partition.

**Required**: Add NAT-closure to Partition's Depends with the role annotation (additive identity `0 + 1 = 1` and successor construction of the numerals 2, 3 and the `m + 1` term in the derived discreteness form).

### Issue 2: Document and Element over-attribute NAT-addcompat to the predicate

**ASN-0045, Properties Introduced — Document/Element, Depends**: "NAT-addcompat (strict successor inequality `n < n + 1`, distinguishing the numeral 2 from 0, 1, 3 — *used in Partition's at-most-one direction*)."

**Problem**: The annotation itself concedes the dependency belongs to Partition, not to the Document/Element predicate. Each predicate's only postcondition is the biconditional `Document(t) ⟺ T4-valid(t) ∧ zeros(t) = 2`. Establishing that biconditional requires the numeral `2` to denote a specific natural (NAT-closure), but it does **not** require `2` to be distinct from `0, 1, 3` — numeral distinctness is consumed only by Partition's mutual-exclusion argument. Listing NAT-addcompat under the predicate's own Depends conflates the predicate's dependencies with Partition's proof dependencies. (Contrast Node, whose Depends correctly omits all NAT-* beyond the constant 0.)

**Required**: Remove NAT-addcompat from the Document and Element predicate Depends (it is already correctly carried by Partition's Depends). Keep NAT-closure there, since the numeral's existence is genuinely needed to state the predicate.

## OUT_OF_SCOPE

None. The ASN stays within its mandate: naming the four T4c levels as carrier-wide predicates and deriving their partition.

VERDICT: REVISE
