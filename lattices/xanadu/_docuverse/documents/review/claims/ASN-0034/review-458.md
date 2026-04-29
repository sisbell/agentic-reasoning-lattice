# Regional Review — ASN-0034/NAT-addbound (cycle 1)

*2026-04-23 23:17*

### Disjointness clause is redundant with irreflexivity
**Class**: REVISE
**Foundation**: n/a (foundation ASN)
**ASN**: NAT-order axiom — "Disjointness of `<` and `=`: for any `m, n ∈ ℕ` with `m < n`, `m ≠ n`"
**Issue**: This clause is derivable from irreflexivity together with the indiscernibility of equality — the very same logical principle the ASN explicitly invokes elsewhere (NAT-zero's consequence proof: "indiscernibility of `=` — a logical property of equality available throughout"). Suppose `m < n ∧ m = n`; substituting via indiscernibility yields `m < m`, contradicting `¬(n < n)` at `n := m`. So `m < n ⟹ m ≠ n` is a consequence, not an independent axiom. The exactly-one trichotomy proof's `¬(m < n ∧ m = n)` and `¬(m = n ∧ n < m)` clauses cite "disjointness at (m, n)" / "(n, m)" — exactly the indirection that hides the irreflexivity-only derivation.
**What needs resolving**: Either move the disjointness statement out of the Axiom slot (e.g., fold its content into the Consequence as part of mutual exclusion derived from irreflexivity + indiscernibility), or justify why it must be primitive. As written, the axiom set is non-minimal and the consequence proof launders an axiom through itself.

### Defensive meta-prose accretes across structural slots
**Class**: REVISE
**Foundation**: n/a
**ASN**: Multiple sites — examples:
- NAT-closure: "Successor closure `n + 1 ∈ ℕ` is not axiomatized separately…"; "The mirrored clause `n + 0 = n` is not axiomatized here; commutativity of `+` is not enumerated…"
- NAT-sub: "Single-valuedness on the domain of definition is carried by the function signature itself, so the uniqueness claimed above…is established by positing `−` as a function rather than by derivation from right-cancellation of `+`, which no NAT foundation declares."
- NAT-sub: "Both inverse forms are stated because citing either one without commutativity of addition would otherwise be tacit."
- NAT-sub conditional closure bullet: "subsumed by the signature's codomain commitment, retained for downstream citation."
- NAT-sub: long paragraph explaining *why* the right-telescoping clause is unconditional and *why* NAT-addbound is therefore declared.
**Issue**: These passages explain *why an axiom is or isn't present*, *why a clause is retained despite redundancy*, *why a dependency is needed* — meta-commentary on the structure rather than statements about what the predicates assert. They sit inside the prose blocks above the Formal Contracts and force the precise reader to skip past justification of the structure to reach the structure itself. Several are also defensive against absent properties (no commutativity, no right cancellation), which catalogues what the foundation does not have rather than what it does.
**What needs resolving**: The prose around each axiom should state what the axiom says and how its symbols ground; structural rationale (why a clause is retained, why a dependency exists, why something isn't axiomatized) belongs either out of the body or compressed to a single inline phrase. The conditional-closure bullet retained "for downstream citation" is the clearest case — either the clause stands on its own or it doesn't; its presence shouldn't need a justification clause.

### Strict positivity is a discreteness commitment in subtraction's clothing
**Class**: REVISE
**Foundation**: n/a
**ASN**: NAT-sub axiom — "Strict positivity: `m > n ⟹ m − n ≥ 1`"
**Issue**: The other NAT-sub clauses constrain `−` via `+` and `≤`. Strict positivity is different in kind: from `m > n` and the right-inverse, one obtains `m − n ≠ 0` (since `0 + n = n ≠ m` would follow if `m − n = 0`), but lifting `≠ 0` to `≥ 1` requires the discreteness fact `(A k ∈ ℕ :: k = 0 ∨ k ≥ 1)` — a property of ℕ that no other axiom in this ASN declares. The clause is therefore not "subtraction structure" alone; it imports a structural commitment about how naturals sit between 0 and 1. The prose presents it alongside the inverse clauses without flagging this asymmetry, and no other axiom independently establishes the underlying discreteness.
**What needs resolving**: Either acknowledge in the axiom prose that strict positivity is the carrier of discreteness in this foundation (and accept that downstream consumers needing `k > 0 ⟹ k ≥ 1` for non-subtraction reasons must route through subtraction), or hoist the discreteness fact to a separate named claim (e.g., on NAT-zero or NAT-order) so that NAT-sub's strict positivity is genuinely a subtraction property derivable from inverse + discreteness.

### Presentation order does not follow dependency order
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: Document order is NAT-zero, NAT-closure, NAT-addcompat, NAT-order, NAT-sub, NAT-addbound; dependency order would put NAT-order first (it depends on nothing), then NAT-zero, NAT-closure, NAT-addcompat, NAT-addbound, NAT-sub.
**Issue**: NAT-zero's prose invokes NAT-order's irreflexivity and transitivity ~150 lines before NAT-order's own statement. NAT-closure cites `0 ∈ ℕ` from NAT-zero (forward-ok) but also invokes NAT-order's signature-positing register before NAT-order is shown. A reader walking the document linearly meets every NAT-order property in citation form before in declaration form. Soundness is unaffected — the Depends slots are explicit — but the ordering is inverted relative to the dependency DAG.

VERDICT: REVISE
