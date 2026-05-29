# Review of ASN-0045

## REVISE

### Issue 1: Z0 is an unnecessary stipulated premise — T4c already constrains the range

**ASN-0045, Well-Definedness / Z0**: "We therefore record the anchor as an explicit stipulated premise on the counting function rather than derive it... **Z0 (cardinality non-negativity).** ... We stipulate, as the defining property of counting, that every such cardinality lands in ℕ with `0 ≤ zeros(t)`."

**Problem**: The entire *at-least-one* reconstruction — Z0 plus the NAT-discrete interval walk that collapses `{n ∈ ℕ : 0 ≤ n ≤ 3}` to `{0,1,2,3}` — re-derives a fact the foundation already delivers. T4c (ASN-0034) states "the mapping `zeros(t) → hierarchical level` is a bijection on `{0,1,2,3}`." A bijection whose domain is `{0,1,2,3}` *is* the assertion that for every T4-valid `t`, `zeros(t) ∈ {0,1,2,3}`. At-least-one therefore follows in one line from T4c. The author's defense ("the lower bound is not derivable from NAT-order") never considers this route and so introduces a brand-new stipulated axiom (Z0) into the specification to recover something already verified upstream.

A premise "not a theorem of the foundation" is an axiom. Adding an axiom that is not needed is a defect: it enlarges the trusted base of the spec for no gain, and standard 7 forbids reinventing what a foundation provides.

**Required**: Remove Z0. Replace the at-least-one argument with a citation to T4c: for T4-valid `t`, `zeros(t) ∈ {0,1,2,3}` because that is the domain of T4c's bijection. If the author wishes to keep an arithmetic argument for self-containment, it must not be dressed as a new stipulated premise — and it still cannot be, since the lower bound it claims to need is supplied free by T4c.

### Issue 2: at-most-one is also a redundant reconstruction of T4c injectivity

**ASN-0045, Well-Definedness, *At-most-one***: "the at-most-one argument rests on the pairwise distinctness of the constructed numerals (`2 := 1+1`, `3 := 2+1`...). That distinctness comes from NAT-addcompat's strict successor inequality..."

**Problem**: T4c's injectivity ("distinct zero counts imply distinct hierarchical levels") combined with the functionality of `zeros` already yields that at most one of the four predicates holds. The numeral-distinctness derivation is correct but duplicates T4c. It is less egregious than Z0 (it adds no new premise), but it is the same over-derivation pattern — reproving a foundation result rather than citing it.

**Required**: Either cite T4c injectivity for at-most-one, or keep the numeral-distinctness argument only if it is explicitly framed as "expanding T4c," not as independent content.

### Issue 3: citation to a nonexistent "Definition slot" of T4c

**ASN-0045, Account postcondition**: "T4c's *Definition* slot instantiated at t supplies `zeros(t) = 1 ⟺ t is a user address`."

**Problem**: T4c's formal contract has only Preconditions and Postconditions; the zeros↔level correspondence lives in T4c's Postconditions, not in a "Definition" slot. The cited slot does not exist. The rename-equivalence derivation is otherwise sound, but the premise pointer is wrong.

**Required**: Cite T4c's Postcondition (the bijection clause `zeros(t) = 1 ↔ user address`), not a "Definition slot."

## OUT_OF_SCOPE

None. The ASN stays within address classification; it does not stray into the listed excluded topics.

VERDICT: REVISE
