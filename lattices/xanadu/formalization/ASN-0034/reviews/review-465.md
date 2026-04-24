# Regional Review — ASN-0034/NAT-addbound (cycle 8)

*2026-04-24 01:20*

### Downstream claims cite "NAT-order's disjointness Consequence" as a named Consequence, but NAT-order explicitly says it is not separately exported
**Class**: REVISE
**Foundation**: n/a (foundation ASN; internal inconsistency between NAT-order's own contract and its downstream consumers NAT-sub and NAT-discrete)
**ASN**: NAT-order resolves disjointness by recording it as a *Reading note* inside the exactly-one-trichotomy Consequence bullet: "The disjointness form `(A m, n ∈ ℕ : m < n : m ≠ n)` is the contrapositive of the conjunct `¬(m < n ∧ m = n)` and is therefore a derivable restatement of that conjunct, not a separately exported Consequence; downstream citations of the implicational form name this exactly-one trichotomy bullet."

Two downstream claims in the same ASN contradict this:
- NAT-sub strict-positivity prose: "contradicting NAT-order's **disjointness Consequence** `n < m ⟹ n ≠ m`."
- NAT-sub Depends bullet for NAT-order: "supplies the disjointness Consequence `n < m ⟹ n ≠ m`, against which the strict-positivity derivation contradicts the `m − n = 0` case." (This bullet separately lists "the exactly-one-trichotomy Consequence's `¬(x < y ∧ y < x)` clause" — so it is treating disjointness and exactly-one-trichotomy as two distinct named Consequences.)
- NAT-discrete equivalence note: "contradicting NAT-order's **disjointness clause** `m < n ⟹ m ≠ n`."
- NAT-discrete Depends bullet for NAT-order: "The separate equivalence note additionally cites NAT-order's disjointness clause `m < n ⟹ m ≠ n` to derive the converse direction."

**Issue**: NAT-order has moved disjointness to a Reading note and instructed downstream to name the exactly-one-trichotomy bullet for the implicational form. NAT-sub and NAT-discrete still cite a "disjointness Consequence" (NAT-sub) or "disjointness clause" (NAT-discrete) as if it were a separately exported target. A downstream consumer following NAT-sub's Depends bullet to NAT-order looking for a named "disjointness Consequence" finds none — only a reading note inside another bullet. NAT-sub's own Depends bullet is self-inconsistent: it lists the exactly-one-trichotomy Consequence and a "disjointness Consequence" as two siblings, which is exactly the structural separation NAT-order denies. The partial fix in the previous cycle (demoting disjointness inside NAT-order) was not propagated to NAT-sub or NAT-discrete.
**What needs resolving**: Pick one. If disjointness is not separately exported (NAT-order's current stance), rewrite NAT-sub's strict-positivity derivation and its Depends bullet, and NAT-discrete's equivalence-note text and Depends bullet, to cite "the exactly-one-trichotomy Consequence's `¬(m < n ∧ m = n)` conjunct (used contrapositively)" — the target NAT-order designates. If the citations in NAT-sub / NAT-discrete are correct and disjointness is in fact separately needed by downstream consumers as a named target, reverse NAT-order's demotion and add `(A m, n ∈ ℕ : m < n : m ≠ n)` as its own `*Consequence:*` bullet with its one-line contrapositive derivation. The three claims must realise the same answer to "is there a named disjointness Consequence in NAT-order?".

VERDICT: REVISE
