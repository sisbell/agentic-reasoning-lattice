# Cone Review — ASN-0034/TA-MTO (cycle 1)

*2026-04-25 23:38*

Reading the ASN end-to-end now.

### Transitive dependencies declared in TumblerSub
**Class**: REVISE
**ASN**: TumblerSub's *Depends:* list cites NAT-cancel, NAT-wellorder, and NAT-discrete with justifications such as "Required in scope for the consumed T1 contract: T1's trichotomy discharge (Case (ii, ii), `m + 1 = n + 1 ⟹ m = n`) … rest on this clause" and "Required in scope for the consumed contracts of Divergence, ZPD, and ActionPoint, whose existence clauses … all rest on the least-element principle."
**Issue**: TumblerSub's proof body does not directly invoke any of these three claims — they are needed only by other contracts that TumblerSub already cites. Every other Depends list in this ASN (TumblerAdd, TA-MTO, ActionPoint, Divergence, ZPD, etc.) lists only direct dependencies; transitive needs are absorbed through the dependency chain. The mixed convention is a structural inconsistency, and the bullets read as meta-prose explaining why a dependency is needed downstream rather than what its clause does at a local site (the "new prose around an axiom explains why the axiom is needed rather than what it says" reviser-drift pattern).
**What needs resolving**: Apply one convention uniformly. Either drop the transitive citations from TumblerSub or justify (and apply) the transitive-closure convention across all Depends lists in the ASN.

### "Displacement" in TA-MTO statement is informal
**Class**: OBSERVE
**ASN**: TA-MTO's natural-language statement: "For any displacement w with action point k and any tumblers a, b with #a ≥ k and #b ≥ k …".
**Issue**: "Displacement" is used as if it were a defined predicate, but it is only introduced informally in the prose around TumblerAdd; the formal carrier is TA-Pos's `Pos(w)`. The contract correctly lists `Pos(w)` as a precondition, but the in-text statement omits it, leaving the reader to infer that "displacement" stands for `Pos(w) ∧ w ∈ T`.
**What needs resolving**: (none required — contract is sound; flag only)

### Mixed `<`/`≤` chaining in TumblerAdd strict advancement
**Class**: OBSERVE
**ASN**: TumblerAdd, strict-advancement paragraph: "NAT-addcompat's left order-compatibility gives `aₖ + wₖ ≥ aₖ + 1`, and its strict successor inequality gives `aₖ + 1 > aₖ`. NAT-order composes these into `aₖ + wₖ > aₖ`."
**Issue**: The composition uses `a < b ∧ b ≤ c ⟹ a < c`, which NAT-order does not export as a named clause; it exports `<`-transitivity, `≤`-transitivity (Consequence), and the `≤`-defining disjunction, from which the mixed form is derivable but not immediate. Other sites in the ASN (e.g., T1 transitivity) explicitly walk the disjunction; this site elides it.
**What needs resolving**: (none required — derivation is sound)

VERDICT: REVISE
