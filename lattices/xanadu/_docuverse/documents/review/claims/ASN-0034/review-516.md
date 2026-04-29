# Regional Review — ASN-0034/NAT-addbound (cycle 1)

*2026-04-24 11:14*

### Use-site inventory in NAT-addbound body references external NAT-sub
**Class**: REVISE
**Foundation**: N/A (internal to this ASN)
**ASN**: NAT-addbound, second paragraph: "The two facts are derivable from four NAT foundations and recorded jointly as a named theorem so that NAT-sub's right-telescoping clause `(m + n) − n = m` can discharge the implicit precondition `m + n ≥ n`, and its left-telescoping clause `(n + m) − n = m` can discharge the implicit precondition `n + m ≥ n` (the left-dominance clause instantiated at `(m, n) := (n, m)`) — both required by NAT-sub's own conditional-closure clause to make `(m + n) − n` and `(n + m) − n` denote ℕ-elements — without each downstream consumer re-deriving the lifts."
**Issue**: This paragraph is a defensive use-site inventory explaining why the lemma exists in terms of a downstream consumer (NAT-sub) that is not part of this ASN, not part of its Depends list, and whose clauses are not in scope. It does not advance the argument — neither the statement nor the derivation of the two dominance facts depends on NAT-sub's existence. The "left-dominance clause instantiated at `(m, n) := (n, m)`" aside also silently relies on the symmetry between the two consequences rather than deriving `n + m ≥ n` as an independent instantiation, which a precise reader must reconstruct. The paragraph is exactly the pattern the reviewer guide names: "new prose around an axiom explains why the axiom is needed rather than what it says," combined with a use-site inventory pointing at an ASN not yet introduced.
**What needs resolving**: The ASN must either remove the NAT-sub-targeted justification paragraph entirely (the two dominance facts stand on their own derivations below), or replace it with a single sentence that states what the lemma asserts and defers the motivation to downstream ASNs' own Depends lists. The `n + m ≥ n` claim, if it is load-bearing for the ASN's exports, should be stated as its own *Consequence* with an explicit derivation rather than left as an aside.

VERDICT: REVISE

## Result

Regional review converged after 2 cycles.

*Elapsed: 283s*
