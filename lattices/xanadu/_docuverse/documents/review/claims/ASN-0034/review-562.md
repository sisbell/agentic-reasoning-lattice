# Cone Review — ASN-0034/T4b (cycle 1)

*2026-04-25 19:46*

### T4c label biconditionals placed in Postconditions, not a Definition slot
**Class**: REVISE
**Foundation**: n/a (internal)
**ASN**: T4c (LevelDetermination). Formal Contract has only `Preconditions`, `Depends`, `Postconditions` — no `Definition` or `Axiom` bullet. The four label biconditionals `(zeros(t) = 0 ↔ t is a node address) ∧ ... ∧ (zeros(t) = 3 ↔ t is an element address)` appear only inside the Postconditions slot.
**Issue**: The prose explicitly says "T4c defines four hierarchical level labels by zero count" and notes "The four biconditionals are the definition of the labels." A *postcondition* names what a proof has established; these biconditionals are not established by the proof — they are stipulated as the meaning of the label terms (`node address`, `user address`, ...). The Exhaustion + Injectivity proof discharges the *consistency* of these definitions (well-defined assignment), not the biconditionals themselves. Consumers reading the contract will see no introductory site for the label terms — they appear only as RHSs in Postcondition biconditionals.
**What needs resolving**: Move the four label-introducing biconditionals into a `Definition` slot (the natural counterpart to NAT-order's `Definition` slot for `≤`, `≥`, `>`). Use the Postconditions slot only for what the proof actually establishes — well-definedness of the assignment, exhaustion of the T4-valid subdomain, and pairwise distinctness of labels.

### T4 conflates definitional and axiomatic content in the Axiom slot
**Class**: REVISE
**Foundation**: n/a (internal)
**ASN**: T4 (HierarchicalParsing) Axiom slot. Sentence: "T4 stipulates that a position `i` of `t` is a *field separator* iff `tᵢ = 0`."
**Issue**: A stipulation introducing the term *field separator* by a defining biconditional is definitional content, not an axiom. The same Axiom slot also contains the per-`k` schema "for each `k ∈ ℕ` with `0 ≤ k ≤ 3` at which `zeros(t) = k`, the form is —" which restates definitional decomposition rather than asserting a substantive constraint. The genuine axiomatic content (the four constraints `zeros(t) ≤ 3`, no two zeros adjacent, `t₁ ≠ 0`, `t_{#t} ≠ 0`) is mixed with these definitions in one slot. Downstream T4a and T4b cite "T4-validity" as a four-condition predicate — but T4 never names that predicate explicitly, leaving readers to reconstruct its definition.
**What needs resolving**: Either give T4 a `Definition` slot for the term *field separator* and an explicit `Definition` of the *T4-valid* predicate as the conjunction of the four constraints, or rephrase the Axiom slot so it asserts a constraint (e.g., that any tumbler used as an address must satisfy the four conditions) rather than mixing definitional stipulations with the constraints they qualify.

### NAT-sub Consequence prose explains slot choice rather than mathematical content
**Class**: OBSERVE
**Foundation**: n/a (internal)
**ASN**: NAT-sub (NatPartialSubtraction), prose introducing the strict-monotonicity Consequence: "is exported as a *Consequence:* rather than an additional axiom clause, because its content derives from the right-inverse together with NAT-addcompat's right order compatibility and NAT-order's at-least-one trichotomy with irreflexivity. Retaining it as an axiom clause would launder that derivation through a non-minimal clause, the same concern that kept NAT-order's disjointness form `m < n ⟹ m ≠ n` from being separately exported and left it as a derivable contrapositive of the exactly-one-trichotomy Consequence's `¬(m < n ∧ m = n)` conjunct."
**Issue**: This and the parallel passage above the strict-positivity Consequence are meta-commentary on slot-choice methodology, including a comparison to a slot decision in a *different* claim (NAT-order). It explains why something is a Consequence rather than what is being asserted. A precise reader has to skip past the policy discussion to reach the derivation.

### T4b component-access notation `t.X₁` introduced in Postconditions
**Class**: OBSERVE
**Foundation**: n/a (internal)
**ASN**: T4b (UniqueParse). Notation `t.X₁ := (X(t))₁` appears in body prose and is recapitulated only in the Postconditions slot ("The component-access notation `t.X₁ := (X(t))₁` — T0's component projection at index 1 applied to `X(t)`..."), not in the Definition slot, which limits itself to characterising `N, U, D, E`.
**Issue**: `t.X₁` is a defining abbreviation, not a postcondition. Like the T4c biconditionals, it would more naturally sit in a Definition bullet so downstream claims that import `t.N₁`, `t.U₁`, etc. have a single canonical introduction site.

### Verbose Depends inventories with use-site narration
**Class**: OBSERVE
**Foundation**: n/a (internal)
**ASN**: T4a and T4b Depends entries (and to a lesser degree T4 and NAT-sub). Each foundation entry runs to multiple sentences cataloguing where it is cited and which substep consumes it (e.g., T4a's NAT-discrete entry enumerates four distinct invocations across Forward (i), Reverse First/Interior/Last segments, including parenthetical commentary on why a "subtractive form like `s_k ≤ #t − 1`" is *not* used).
**Issue**: Depends ought to declare what is needed; the per-citation site narration duplicates what the prose already shows and introduces the sort of "subtractive form would have required..." counterfactual that the review prompt flags as defensive justification. A precise reader scanning the dependency surface has to wade through use-site inventories that belong (if anywhere) inline at the citation site.

VERDICT: REVISE
