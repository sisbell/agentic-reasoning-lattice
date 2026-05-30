# Review of ASN-0042

## REVISE

### Issue 1: O1a's boxed statement omits the reachable-state quantification that O1b carries

**ASN-0042, The Account-Level Boundary**: O1a is stated as
> "`(A π ∈ Π : zeros(pfx(π)) ≤ 1)`"

while the structurally parallel O1b is stated as
> "a derived reachable-state invariant ... `(A Σ reachable, π₁, π₂ ∈ Π_Σ : pfx(π₁) = pfx(π₂) ⟹ π₁ = π₂)`"

**Problem**: O1a and O1b are proved by *the same shared induction over the reachability sequence*, and the surrounding text repeatedly calls O1a "a derived reachable-state invariant." The bound `zeros(pfx(π)) ≤ 1` is only established for principals reachable from `Σ₀` (bootstrap via O14(iii), delegates via condition (iii)); it is not a fact about an unqualified global `Π`. The boxed formula uses bare `Π` with no state subscript and no reachability guard, contradicting both its own proof and O1b's matching form. Every downstream citation ("O1a (AccountOwnershipBoundary), a derived reachable-state invariant") reads it as `(A Σ reachable, π ∈ Π_Σ ...)`.

**Required**: State O1a as `(A Σ reachable from Σ₀, π ∈ Π_Σ : zeros(pfx(π)) ≤ 1)`, matching O1b.

### Issue 2: The shared-induction bookkeeping is described three times

**ASN-0042, O1b parenthetical / paragraph after O1a / opening of Delegation**:
- O1b: "established by the shared induction of *The Account-Level Boundary* and the delegation-step argument of *Delegation*"
- After O1a: "O1a, O1b (PrefixInjectivity), and T4-validity of prefixes are all reachable-state invariants, proved by one induction ... only the delegation step differs per invariant ... *Delegation step:* discharged per invariant — O1a's here, T4's and O1b's in the *Delegation* section"
- Delegation: "O1a, T4-validity, and O1b (PrefixInjectivity) share the single reachable-state-invariance induction whose base case and non-delegation step were given in *The Account-Level Boundary*. It remains to discharge the delegation step for T4 and O1b..."

**Problem**: Three paragraphs in two sections restate the same proof-management fact (one induction, common base + non-delegation step, per-invariant delegation step split across sections) in different words. This is exactly the "multiple paragraphs defer to the same downstream location" / "two paragraphs say the same thing in different words" pattern the anti-bloat mode flags. The reader must reconcile three descriptions of one structure.

**Required**: State the shared-induction structure once (where the base case lives), and at each delegation step write only the one-line discharge for that invariant — no re-announcement of the overall scheme.

### Issue 3: O10(c) prose is defensive justification plus forward-deferral, not derivation

**ASN-0042, O10 (after the statement)**: "Condition (c) is enforced by the construction `a' = pfx(π).0.{hwm_0 + 1}` (verified below), not by an additional axiom ... The clause makes formal the namespace-vs-content distinction: O10 guarantees the next structural tier (user from node, document from account), and no more."

**Problem**: "(verified below)" defers to the construction proof that already discharges `zeros(a') = zeros(pfx(π)) + 1`; "not by an additional axiom" justifies the proof strategy rather than advancing the claim; "The clause makes formal the namespace-vs-content distinction ... and no more" is essay restatement of the postcondition. The only load-bearing content here (the `B5a`/`B5` zero-count computation) is repeated in the construction. A reader following the proof skips past this paragraph.

**Required**: Delete the strategy-justification and the namespace-essay sentence; keep the zero-count derivation in the construction only.

### Issue 4: Repeated full parenthetical re-citation of the covering-chain lemma

**ASN-0042, Ownership Domains / O2 / O3 / OwnershipDomainPermanence / O7 / O10**: the parenthetical "the covering-chain lemma (PrefixesOfCommonAddressAreComparable, *Ownership Domains* section)" is reproduced verbatim at roughly five call sites.

**Problem**: After the lemma is named and proved, the full "(PrefixesOfCommonAddressAreComparable, *Ownership Domains* section)" tag at every reuse is citation accretion — a milder instance of the same noise the classifier targets.

**Required**: Cite the lemma by short name after first use.

## OUT_OF_SCOPE

The ASN already routes ownership transfer, cross-node federation, domain density, and delegation-history recording to its Open Questions; these are correctly deferred and need no coverage here.

VERDICT: REVISE
