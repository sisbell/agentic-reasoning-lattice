# Regional Review — ASN-0034/T4c (cycle 3)

*2026-04-23 01:02*

### NAT-card uniqueness: axiomatic assertion accompanied by proof sketch
**Class**: OBSERVE
**Foundation**: NAT-card (NatFiniteSetCardinality) — Axiom (enumeration characterisation)
**ASN**: NAT-card prose: *"The length `k` is uniquely determined by `S` because two strictly increasing enumerations of the same set must agree element-by-element under NAT-order's trichotomy; hence `|·|` is a well-defined total function…"*
**Issue**: The Axiom already asserts uniqueness (`|S|` *is the unique* `k`). The trailing proof sketch then explains *why* uniqueness holds — a reviser-drift pattern (new prose around an axiom explaining why it holds rather than what it says). The sketch is also materially under-powered: element-by-element agreement of two strictly increasing enumerations of a finite set needs induction / well-ordering, which NAT-card does not invoke and whose declared dependencies do not supply. Either drop the sketch (uniqueness is axiomatic) or promote it to a Consequence with honest machinery. Not a soundness issue because the Axiom carries the weight.

### NAT-card's Axiom quantifiers leave `S` free
**Class**: OBSERVE
**Foundation**: NAT-card (NatFiniteSetCardinality) — Axiom's conditional codomain and upper bound clauses
**ASN**: `(A n ∈ ℕ : S ⊆ {1, 2, …, n} :: |S| ∈ ℕ)` and `(A n ∈ ℕ : S ⊆ {1, 2, …, n} :: |S| ≤ n)`.
**Issue**: In EWD-style quantifier notation `(Q vars : range : body)`, the variables bound should be declared in the `vars` slot. Both clauses declare only `n`; `S` is used in the range and body but never bound, so the universal claim over subsets is only implicit. Intent is unambiguous but the notation is loose compared to the care taken elsewhere in the ASN (e.g. NAT-order's `(A m, n ∈ ℕ : m < n : m ≠ n)`).

### Asymmetry between "stated NAT-order properties" and tacit logical properties of `=`
**Class**: OBSERVE
**Foundation**: NAT-zero (NatZeroMinimum) Consequence derivation; T4c Exhaustion note
**ASN**: T4c Exhaustion flags *"substitution of equals under `<` is not among NAT-order's stated properties."* NAT-zero's revised second case invokes *"symmetry of `=`"* without declaration: *"disjointness … yields `n ≠ 0`, which by symmetry of `=` contradicts `0 = n`."*
**Issue**: The ASN is scrupulous about which NAT-order properties are "stated" vs. derivable, but silently admits the logical properties of `=` (symmetry here; reflexivity elsewhere when reading `m = n` as an equivalence used to rewrite membership). That asymmetry — relational properties must be axiomatized, equality properties are tacit — is never declared. A one-line note ("logical equality is reflexive, symmetric, transitive; these are available throughout and are not counted among NAT-order's properties") would reconcile the posture and remove the ambiguity about what a derivation is allowed to appeal to.

VERDICT: OBSERVE

## Result

Regional review converged after 3 cycles.

*Elapsed: 734s*
