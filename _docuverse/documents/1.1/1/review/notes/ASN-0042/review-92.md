# Review of ASN-0042

This ASN is mathematically polished — the longest-match construction, the reachable-state inductions for O1a/T4/O1b, the O10 fork non-coverage analysis, and the worked example all hold up under scrutiny. The cross-references are confined to the two foundation ASNs (0034, 0040), which is permitted. My findings are concentrated in accreted meta-prose, consistent with the `review-mode.anti-bloat` classifier this note carries.

## REVISE

### Issue 1: O15 retains redundant conditions plus a paragraph explaining the redundancy
**ASN-0042, State Axioms (O15)**: "Conditions (v) and (vii) are not independent admission conditions: condition (viii) entails both... We retain (v) and (vii) in the list for readability, but they are consequences of (viii) via B6 sufficiency and B1/B2."
**Problem**: The recent revision history collapsed conditions into (viii), yet (v) and (vii) survive in the eight-condition gate alongside a justifying paragraph for keeping derivable clauses. This is reviser drift: rather than removing the redundancy, prose was added to explain it. The gate is the load-bearing object; padding it with provably-redundant conjuncts and a defense of their retention forces the reader to track which conditions are primitive. The same redundancy then propagates — DelegatorAllocatesPrefix, NamespacePrincipalExclusivity, and O7(c) all re-cite "(vii), itself a consequence of next-reachability (viii) via B1/B2."
**Required**: Drop (v) and (vii) from the delegation predicate; state once, at the definition of `delegated`, that (viii) discharges T4-validity (via B6 sufficiency) and freshness (via B1/B2). Remove the retention paragraph and the parenthetical re-derivations at each downstream cite.

### Issue 2: Multiple sections defer to the same downstream induction
**ASN-0042, O6 proof**: "By O1a (AccountOwnershipBoundary), which holds because `Σ` is reachable (a reachable-state invariant; the consolidated induction is in the Delegation section)" — and **O9 proof**: "...(a reachable-state invariant; see the consolidated induction in the Delegation section)".
**Problem**: Two proofs pause mid-argument to point forward to the Delegation section's induction. This is the "multiple paragraphs defer to the same downstream location" pattern. The pointer adds no reasoning; O1a is simply a reachable-state invariant the proof may cite.
**Required**: Cite O1a directly as a derived invariant (its status is already recorded in the Properties table). Drop the cross-section deferral in both O6 and O9.

### Issue 3: "Remark (next-reachability discipline)" re-derives (viii) via forward references
**ASN-0042, after O15**: "*Remark (next-reachability discipline).* Condition (viii) restricts delegation to the single address an ASN-0040 baptism would issue: O18's material baptism adds exactly `next(Σ.B, p, d)` (O17b), so the admissible delegate prefix is the `(hwm(Σ.B, p, d) + 1)`-th stream element `c_{hwm+1}`, whose predecessors... are already in `Σ.B`."
**Problem**: This remark re-explains what (viii) already states, leaning on O18 and O17b that appear later in the document. It advances no claim — it is essay content restating the condition's effect. Coming immediately after the redundancy paragraph (Issue 1), it compounds the meta-prose around O15.
**Required**: Remove the remark, or fold its single operative fact (delegate prefix = `c_{hwm+1}`) into the (viii) clause itself without the forward-referenced re-derivation.

### Issue 4: O17b is labeled an axiom but carries an inline derivation and consumer inventory
**ASN-0042, O17b**: "Consequently every registry reachable under `→` is reachable under ASN-0040's baptismal transition relation, so ASN-0040's registry results — B0 (Irrevocability), B1 (ContiguousPrefix), B10 (T4Validity, = O17), and B_fin (RegistryFiniteness) — transfer to every ownership-reachable `Σ`."
**Problem**: The Properties table marks O17b "axiom (coupling)," but its body appends a "Consequently...transfer" derivation enumerating which downstream results it feeds. An axiom should state what it asserts; the list of transferred results is a downstream-consumer inventory, not part of the axiom's content.
**Required**: State O17b as the coupling axiom only (the `Σ'.B = Σ.B ∨ Σ'.B = Σ.B ∪ {next(...)}` disjunction). If the transfer of B0/B1/B10/B_fin needs naming, do it once at the point of use, not as a clause of the axiom.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer invariants
The Open Questions raise transfer (LM 2/29 "bought the document rights"). O3/O8 correctly scope the system to refinement-only; transfer is genuinely new territory for a future ASN, not a gap here.

### Topic 2: Cross-node identity federation
O9 establishes node-locality; federation consistency with O9 is flagged as an open question and belongs in a future ASN.

META: not applicable — the ASN defines ownership state (Π, pfx), operations (delegation, fork), and invariants (exclusivity, coverage, irrevocability) at an implementation-independent level; the implementation citations are corroboration, not specification of mechanics.

VERDICT: REVISE
