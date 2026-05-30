# Review of ASN-0042

## REVISE

### Issue 1: O7(c) postcondition overstates the recursion as identical constraints
**ASN-0042, Delegation (O7), postcondition (c)**: "The right is recursive: these are exactly the constraints that bound `π` when `π` delegated to `π'`"
**Problem**: The proof body directly contradicts "exactly." It shows that at the entry state `Σ'` conditions (ii) and (iv) *auto-discharge* (because `Π_{Σ'} ∖ Π_Σ = {π'}`), while at a later prospective state they "revert to genuine per-state obligations," and condition (v) (`next`-reachability) is evaluated against the *then-current* registry — a strictly different obligation than the one that bound `π`. So the constraints binding `π'` are not "exactly" those that bound `π`; they depend on the state and on prior sub-delegations. The summary sentence misstates the very distinction the proof labors to establish.
**Required**: Replace "these are exactly the constraints" with the accurate claim — the same *five-condition gate* applies, but conditions (ii), (iv), and (v) are re-evaluated against the delegation state, so the admissible `p''` is state-dependent (as the proof and the formal-contract clause already say).

### Issue 2: O7(c) proof carries multi-paragraph meta-prose classifying when conditions bind
**ASN-0042, O7 proof, postcondition (c)**: "This auto-discharge of (ii) and (iv) is specific to the entry state… revert to genuine per-state obligations… So conditions (iii) and (v) bind at every prospective state, while (i), (ii), and (iv) are fixed or auto-discharged at the entry state; (ii) and (iv) re-enter as binding constraints…"
**Problem**: The same fact — which conditions auto-discharge at `Σ'` versus rebind later — is stated three times in successive sentences (per-condition walkthrough, then "auto-discharge is specific to the entry state," then the "binds at every prospective state / fixed at entry / re-enter" recap). This is precisely the reviser-drift pattern the `anti-bloat` classifier flags: a precise reader must skip the restatements to find the single load-bearing claim.
**Required**: Collapse to one statement: at `Σ'`, (ii) and (iv) hold vacuously since `π'` is the only newcomer; at any later prospective state they and (v) are genuine per-state obligations. Delete the two restatements.

### Issue 3: O17b definition slot enumerates downstream consumers
**ASN-0042, Properties Introduced table, O17b row**: "principal-introducing transitions take the baptism branch with `next(Σ.B, p, d) = pfx(π')` (the primitive from which O18 and Freshness-(v)'s freshness derive)"
**Problem**: The parenthetical names which downstream results consume O17b rather than advancing what O17b states — the definition-introduction-enumerates-consumers pattern. The dependency direction is already recorded in the O18 and Freshness-(v) entries ("derived from O17b…"); restating it here is redundant inventory.
**Required**: Drop the parenthetical; the consumer links live in O18/Freshness-(v)'s own derivation citations.

### Issue 4: "Unilateral O10★" restates the existing postcondition
**ASN-0042, O10 Formal Contract**: the *Postconditions* clause asserts `(E Σ', a' : Σ → Σ' ∧ a' ∈ odom(π) ∩ Σ'.B ∧ ω_{Σ'}(a') = π …)`, then the *Unilateral postcondition (Unilateral O10★)* asserts the same existence "witnessed by a single baptism `Σ → Σ'` performed by `π` alone, producing `a' = pfx(π).0.{hwm_0 + 1}` ∈ `odom(π) ∩ Σ'.B` with `ω_{Σ'}(a') = π`."
**Problem**: Two contract clauses state the same existence claim with the same witness `a'`. The only delta is "performed by `π` alone," which the proof's *Per-baptism authorization* paragraph already establishes via `allocated_by_{Σ'}(π, a')`. Maintaining both as separate postconditions duplicates the claim.
**Required**: Fold the "performed by `π` alone" / `allocated_by` fact into the single Postconditions clause and remove the duplicate ★ line, or demote ★ to a one-line note on the authorization conjunct.

### Issue 5: NamespacePrincipalExclusivity adds no claim beyond O18 + Freshness-(v) + B0
**ASN-0042, State Axioms, NamespacePrincipalExclusivity (derived)**: "once `p ∈ Σ.B` … no later transition can adopt `p` as a new principal's prefix. Proof: by Freshness-(v), admitting `p` as a delegate prefix requires `p ∉ Σ.B`, and by O18 such an adoption materially baptizes `p`. Since `Σ.B` only grows (B0…)…"
**Problem**: The corollary's content is exactly the contrapositive of Freshness-(v)'s freshness conjunct under B0 monotonicity, with no independent reasoning step. It is used only once (worked example), and that use could cite Freshness-(v) + B0 directly. As a standalone named derived result it adds a restatement layer without advancing the argument.
**Required**: Either remove it and cite Freshness-(v)+B0 at the one use site, or, if kept for the worked example's convenience, shorten to a single sentence without re-deriving (the derivation is already implied by its two inputs).

## OUT_OF_SCOPE

### Topic 1: Ownership transfer invariants
The Open Questions raise transfer (divergence of provenance O6 from effective owner O2). Correctly deferred — the system as specified has no transfer mechanism, so this belongs in a future ASN, not this one.

### Topic 2: Cross-node identity federation
O9 establishes node-locality; what a federation must satisfy to remain consistent with O9 is new territory, properly listed as an Open Question rather than an omission here.

VERDICT: REVISE
