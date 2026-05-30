# Review of ASN-0042

## REVISE

### Issue 1: O7(c) — internal inconsistency between the claim, the proof, and the Formal Contract on *when* conditions (ii)/(iv) are discharged

**ASN-0042, Delegation / O7, postcondition (c)**: the body proves "the delegation relation's conditions are satisfiable with `π'` as delegator for a sub-prefix `p''` ... *immediately upon entry — that is, at `Σ'`*," then discharges (i), (ii), (iv) using "`Π_{Σ'} ∖ Π_Σ = {π'}`." The Formal Contract then generalizes: "Conditions (i), (ii), and (iv) are discharged at `Σ'` independent of `p''`; condition (v) remains the per-state obligation on `p''`." But the O7 *statement* itself says the opposite: "(ii), (iv), and (v) of O15 re-checked there [at the prospective delegation state]."

**Problem**: The discharge of (ii) relies on `Π_{Σ'} ∖ Π_Σ = {π'}` — true only at `Σ'`. At any later state `Σ''` where `π'` has itself sub-delegated some `p''' ≺ p''`, that sub-delegate is the most-specific cover of `p''`, so `π'` no longer satisfies condition (ii) for `p''`. The Formal Contract's "(ii) and (iv) discharged at `Σ'` ... at every state at which O15 condition (v) holds" therefore overclaims: it asserts (ii)/(iv) are settled once-and-for-all when in fact they are genuinely per-state beyond `Σ'`. This directly contradicts the O7 statement's own "re-checked there."

**Required**: Reconcile the three. Either (a) restrict postcondition (c) to delegation *at `Σ'`* (the only state the proof covers), or (b) keep the "re-checked at the prospective state" reading and delete the "(ii) and (iv) discharged at `Σ'` independent of `p''`" claim, re-deriving (ii)/(iv) as per-state obligations alongside (v).

### Issue 2: O1a preamble — forward-reference, non-circularity defense, and downstream use-site inventory in a structural slot

**ASN-0042, The Account-Level Boundary**: "O1a is a reachable-state invariant; its inductive proof is given in the *Delegation* section (base case O14's third clause, preserved by delegation condition (iii)). The uses of O1a in O6, O9, and O10 below are therefore not circular — they invoke an invariant established by that induction."

**Problem**: Three of the flagged accretion patterns in one paragraph: (i) it defers the proof to a downstream location, (ii) it enumerates downstream consumers ("uses of O1a in O6, O9, and O10"), and (iii) it argues document ordering / non-circularity rather than advancing the claim. The reader must hold this scaffolding to follow nothing — the invariant statement and its proof location stand on their own.

**Required**: Reduce to a bare pointer ("Proved as a reachable-state invariant in *Delegation*"). Drop the consumer list and the circularity defense.

### Issue 3: O3 — proof narration and a duplicated corollary/invariant

**ASN-0042, Permanence and Refinement / O3 proof**: "The reachability hypothesis enters at the one point where the proof excludes the bootstrap origin of `π'` (via BootstrapContainment)."

**Problem**: This sentence narrates where a hypothesis is used rather than performing reasoning — meta-prose. Separately, the "Corollary (monotonic refinement)" proves `#pfx(ω_{Σ'}(a)) ≥ #pfx(ω_Σ(a))`, and the Formal Contract "Invariant:" line restates the identical inequality with the same qualifier ("for all transitions `Σ → Σ'` between reachable states"). Two statements of the same fact.

**Required**: Delete the narration sentence. Keep the inequality in one place (corollary or contract), not both.

### Issue 4: O7(c) witness — same non-termination point stated twice

**ASN-0042, O7 proof of (c)**: "The recursion may continue indefinitely along any chain whose successive delegates remain consistent with this condition." and, in the same paragraph, "We do not claim termination; the construction extends as far as the chosen sequence of delegates permits."

**Problem**: Two sentences in the same construction assert the identical point (the chain is unbounded / non-terminating). One is noise.

**Required**: Keep one.

### Issue 5: DelegatorAllocatesPrefix — Invariant restates the postcondition

**ASN-0042, Delegation / DelegatorAllocatesPrefix**: Postcondition: "`allocated_by_{Σ'}(π_d, pfx(π'))` — the delegator is the allocator of the delegate's prefix." Invariant: "The same `π_d` whose authority condition (ii) admits `π'` into `Π` is the allocator whose O5 authority enters `pfx(π')` into `B`."

**Problem**: The Invariant line is the postcondition rephrased — same fact, different words.

**Required**: Drop the Invariant line or replace it with content the postcondition does not already carry.

### Issue 6: Multiple sections defer to "the Delegation section" for the same proofs

**ASN-0042**: O1a preamble ("its inductive proof is given in the *Delegation* section"); NestingByDelegation ("excluded by O1b (preserved across transitions; see the Delegation section)"); and the Delegation section's own invariant intro all point at the same downstream induction.

**Problem**: The "defer to the same downstream location" accretion pattern. Each forward pointer is a place the reader must jump from.

**Required**: State O1a/O1b/T4 as reachable-state invariants once, with the induction in a single place, and let later claims cite the lemma name without re-justifying its location or non-circularity.

## OUT_OF_SCOPE

### Topic 1: Per-state re-derivation of recursive-delegation authority along a chain
**Why out of scope**: A full account of how delegation authority evolves as a principal accumulates sub-delegates (the dynamics behind Issue 1) is a delegation-lifecycle question. Issue 1 only asks that this ASN not *overclaim* it; the positive treatment belongs to a future ASN.

### Topic 2: Ownership transfer invariants (already in Open Questions)
**Why out of scope**: The divergence between recorded provenance (O6) and effective owner (O2) under transfer is genuinely new territory; the ASN correctly defers it.

VERDICT: REVISE
