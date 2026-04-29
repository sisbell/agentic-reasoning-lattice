# Regional Review — ASN-0034/T4a (cycle 1)

*2026-04-24 12:40*

### T4c lacks a Definition slot; biconditionals defining address-label predicates live in Postconditions
**Class**: OBSERVE
**ASN**: T4c (LevelDetermination). The body introduces four predicates: "`t` is a *node address* iff `zeros(t) = 0`, a *user address* iff `zeros(t) = 1`, a *document address* iff `zeros(t) = 2`, and an *element address* iff `zeros(t) = 3`." The Formal Contract has Preconditions, Depends, Postconditions — but no Definition slot. The four biconditionals (the actual *defining* equations of the four label predicates) appear only as a conjunction in the Postconditions slot: `(zeros(t) = 0 ↔ t is a node address) ∧ ...`.
**Issue**: Postconditions report what the claim establishes; Definitions introduce new vocabulary. Since T4c declares itself "a pure definition on whatever T4-valid tumblers exist" and the four labels are used by T4's body prose and referenced in T4b's `dom(E) = {... : zeros(t) = 3}` (element pattern), the defining biconditionals belong in a Definition slot. The Postconditions slot should export what was proved *about* the definition — e.g., exhaustion and pairwise-distinctness of the label predicates — rather than carry the definition itself. Parallels the previous cycle's "field separator" slot-hygiene observation at T4.

### Defensive "path-not-taken" prose in T4b Derivation and T4a Depends
**Class**: OBSERVE
**ASN**: T4b Derivation: "each matches the native form T4a's Reverse direction delivers (no subtractive rewriting is performed; in particular the last-segment inequality is kept in its `+1` form rather than rewritten as `s_k ≤ #t − 1`, which would require NAT-sub's strict-monotonicity Consequence at `p = 1` plus right-telescoping and a split on the `≤`-unfolding)." T4a Depends (NAT-discrete entry): "The Last-segment output is NAT-discrete's native `+1` form ..., avoiding a detour through a subtractive form like `s_k ≤ #t − 1` that would require a further non-strict-monotonicity step not declared by NAT-sub."
**Issue**: Both passages argue in detail about an alternative derivation path (subtractive rewriting) that the authors chose *not* to take, explaining why that path would have cost more. A precise reader reading the claim as it stands does not need to know what the authors decided against. This is defensive meta-prose — essay content in structural slots — and matches the reviser-drift pattern "new prose around an axiom explains … rather than what it says." The prose would be equivalent if both paragraphs ended at "each matches the native form T4a's Reverse direction delivers" / "The Last-segment output is NAT-discrete's native `+1` form," respectively.

### NAT-sub's Consequence slots carry architectural essay about "laundering" and cross-reference NAT-order's structural choices
**Class**: OBSERVE
**ASN**: NAT-sub Consequence for strict monotonicity: "recorded as a Consequence rather than an axiom clause so the derivation is not laundered through a non-minimal clause, the same concern that kept NAT-order's disjointness form `m < n ⟹ m ≠ n` from being separately exported and left it as a derivable contrapositive of the exactly-one-trichotomy Consequence's `¬(m < n ∧ m = n)` conjunct." Strict-positivity Consequence: "recorded as a Consequence rather than an axiom clause because its content is not purely subtractive — lifting `m − n ≠ 0` to `m − n ≥ 1` leans on NAT-discrete's structural commitment to discreteness of ℕ."
**Issue**: Both Consequence entries include prose about *why* the authors chose the Consequence slot over the Axiom slot, including cross-references to the analogous decision at NAT-order. This is design-rationale commentary inside a structural slot that is supposed to state the derived fact and its derivation. A reader consulting the Consequence slot wants the consequence and its derivation path; the slot-choice rationale belongs in commit-message / design-doc territory. Compounds across ASNs when the same pattern is echoed (here at NAT-sub, pointing back at NAT-order).

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 618s*
