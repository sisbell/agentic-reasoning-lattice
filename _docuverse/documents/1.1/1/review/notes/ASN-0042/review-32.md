# Review of ASN-0042

## REVISE

### Issue 1: O10's fork postcondition relies on sub-delegate cooperation but doesn't elevate this to a stated limitation

**ASN-0042, O10 trajectory for `zeros(pfx(π)) = 0`**: "Total trajectory: u + 2 baptisms — π performs (u − |S'|) + 2, the immediate sub-delegates {π_k : k ∈ S'} perform |S'|. ... each cooperative baptism is an act π_k is independently O5-authorized to perform, so every transition in the chain Σ →⁺ Σ_{u+2} is valid under the abstract spec's reachability relation."

**Problem**: This is the crucial design point of the ASN and it is buried inside the proof. The existential `(E Σ', a' : Σ →⁺ Σ' ∧ ...)` is satisfied by *any* sequence in the abstract reachability relation, including ones where sub-delegates cooperate. But the prose framing of O10 ("π may create a new address a'") implies π acts alone. For a node-level principal whose sub-delegates have already occupied the immediately-available user-field slots (slots `1..hwm`), π cannot advance the namespace past any slot `k ∈ S'` without π_k's participation — `next(B, pfx(π), 2)` is strictly sequential. The "denial as fork" architecture purports to convert ownership boundaries into creative acts; the ASN should establish whether this conversion is always unilaterally achievable, and if not, what the operational consequences are.

**Required**: Distinguish abstract reachability (existence of *some* transition sequence) from unilateral feasibility (π can fork without others' acts). Either (a) prove a stronger postcondition — a unilateral subtrajectory always exists, e.g., by choosing `u = hwm + 1` and showing this slot can be made not-in-S' under O1a — or (b) explicitly note that the fork is cooperative in the general zeros=0 case, with consequences for "denial as fork" as a usable mechanism.

### Issue 2: Trajectory step count in O10 inconsistent with starting state's `hwm`

**ASN-0042, O10 proof of `zeros(pfx(π)) = 0` case**: "By induction on k, after k such authorized baptisms Σ_0 → ... → Σ_k, B_{Σ_k} ∩ S(pfx(π), 2) = {pfx(π).0.1, ..., pfx(π).0.k}" and "Total trajectory: u + 2 baptisms".

**Problem**: This indexing assumes `B_{Σ_0} ∩ S(pfx(π), 2) = ∅`, i.e., no slot in the child stream is baptized in the starting state. But Σ is a general reachable state with `hwm(Σ.B, pfx(π), 2) = m_0 ≥ 0`. When m_0 > 0, the trajectory baptizes slots `m_0 + 1, ..., u`, requiring `(u − m_0) + 2` baptisms, not `u + 2`. Additionally, the induction "after k baptisms slots 1..k are in B" doesn't account for already-baptized slots — those are in B without being baptized in the trajectory.

**Required**: Reindex the trajectory relative to `hwm(Σ.B, pfx(π), 2)`, or explicitly normalize: write `Σ_0` to mean the state where the trajectory begins (not the bootstrap state), state that `hwm_0 = hwm(Σ_0.B, pfx(π), 2)`, and adjust the step count to `(u − hwm_0) + 2`.

### Issue 3: Sub-lemma FirstDelegatorIsπ has a restrictive hypothesis and unclear role

**ASN-0042, Sub-lemma**: "Let Σ be reachable from Σ₀, π ∈ Π_Σ with S_π(Σ) = ∅..."

**Problem**: The hypothesis `S_π(Σ) = ∅` (no sub-delegates of π exist in Σ) is restrictive. The text justifies it as "the canonical setting in which the first-delegator claim is invoked" — applicable when π was just introduced or has not yet delegated. But AccountLevelPermanence★ (the multi-step corollary) is proved by induction on path length directly, not via the Sub-lemma. The Sub-lemma's contribution to the overall argument is therefore unclear: it neither closes a gap in AccountLevelPermanence★ nor is it cited from any other proof. If it's standalone supporting machinery for Nelson's "forevermore" intuition, this should be explicit; if it's load-bearing for some downstream argument, that argument should cite it.

**Required**: Either (a) cite the Sub-lemma from a derivation that needs its stronger conclusion (chain of *delegations* between fixed-π and the witness, not just chain of *delegators* with extending prefixes), or (b) demote it to a remark with the canonical-setting caveat, since AccountLevelPermanence★ alone suffices for the corollary's intended claims.

### Issue 4: Informal "T4(a)" notation conflates multiple foundation properties

**ASN-0042, multiple sites**: "By T4(a) (positive-component constraint, at most three zeros, no adjacent zeros, no leading or trailing zero)", "By T4(b) and T4(a)...", "T4(a) applied to a...", etc.

**Problem**: The foundation has T4 (HierarchicalParsing), T4a (SyntacticEquivalence), T4b (UniqueParse), T4c (LevelDetermination). The ASN's "T4(b)" maps cleanly to T4b and "T4(c)" to T4c, but "T4(a)" is used to refer to (variously): the positivity of non-separator components (a consequence of T4's separator definition), the non-empty-field property (which is T4a's content), and the zero-count bound (which is T4's own clause). These are distinct properties. Conflating them under one label muddies the citation chain.

**Required**: Cite precise foundation names. The "positive non-separator" property follows from T4's separator definition (a position is a separator iff its value is 0) combined with T4-validity's zero-count bound; "non-empty field segment" is T4a (SyntacticEquivalence)'s reverse direction; "field decomposition" is T4b. Use these directly instead of "T4(a)".

### Issue 5: Worked example presents fork as a single allocation, eliding the multi-step trajectory it claims O10 produces

**ASN-0042, Worked Example "Fork (O10)"**: "`π_A` creates a fork: a new address `a' = [1, 0, 2, 0, 6, 0, 1]` within dom(π_A). We verify O10's conditions..."

**Problem**: The worked example treats the fork as a single atomic act. But the O10 proof shows the fork involves a multi-step trajectory (2 baptisms for the zeros=1 case here: `pfx(π_A).0.m` then `inc(·, 2)` for the element-level). The worked example doesn't trace the baptismal trajectory, doesn't identify `m = hwm(Σ.B, [1, 0, 2], 2) + 1`, doesn't verify the per-step O5 authorization, and uses `[1, 0, 2, 0, 6, 0, 1]` (`m = 6`) without showing how that `m` arises from the prior state's `hwm`. This leaves the most procedurally subtle property (O10) under-verified relative to others.

**Required**: Either trace the explicit trajectory in the example (showing the two baptisms and their per-step authorization), or add a separate worked example that does so. The latter is more useful for verifying both the trajectory analysis and the cooperative-vs-unilateral distinction (Issue 1).

### Issue 6: O15 condition (vi) preservation is asserted but not fully derived

**ASN-0042, O15 / Delegation definition**: "(vi) ¬(E π'' ∈ Π_Σ : pfx(π') ≺ pfx(π''))" combined with the inductive arguments showing delegation preserves O1a, O1b, T4.

**Problem**: The ASN proves delegation preserves O1a (via condition (iv)), O1b (via length contradiction), and T4 (via condition (v)), and derives FiniteRegistry. But the proof never explicitly verifies that delegation preserves *non-nesting* of bootstrap-or-already-delegated principals beyond what condition (vi) directly forbids. Specifically: O14's pairwise non-nesting clause applies to Π₀, but the running invariant "no principal nests within another's domain except by being a sub-delegate" isn't established inductively. The Sub-lemma's correctness depends on this — `pfx(π_d) ≼ pfx(π'')` is derived from condition (ii) at delegation time but propagated through the chain by appeal to the same conditions at subsequent delegations.

**Required**: State and prove an explicit non-nesting invariant: in every reachable state, the principal prefixes are organized such that any two are either non-nesting or stand in an ancestor-descendant delegation relation. Show this follows from (vi) at each transition plus O12/O13. Without it, the relationship between domains across the registry is left implicit.

### Issue 7: `acct(a)` definition introduction is internally inconsistent

**ASN-0042, AccountField definition**: "Define acct(a) for any valid tumbler a: when zeros(a) = 0 (node-level), acct(a) = a; when zeros(a) ≥ 1, acct(a) is the tumbler whose components are N(a) followed by [0] followed by U(a) — using the foundation's field projections defined by T4(b) (UniqueParse), with component-wise access decidable from T3 (CanonicalRepresentation) — having zeros(acct(a)) = 1."

**Problem**: The clause "having zeros(acct(a)) = 1" appears as if it characterizes acct(a) generally, but it's only true for the `zeros(a) ≥ 1` branch — the `zeros(a) = 0` branch has `zeros(acct(a)) = 0`. The formal contract correctly states postcondition (b) as `zeros(acct(a)) ≤ 1`, but the introductory prose suggests equality with 1. This is a minor inconsistency but causes friction when the proof of AccountPrefix dispatches on `zeros(a) = 0` (where `acct(a) = a` has zeros = 0).

**Required**: Reword the introduction to state `zeros(acct(a)) ≤ 1` (matching the formal contract), or move the "zeros(acct(a)) = 1" clause inside the `zeros(a) ≥ 1` branch.

## OUT_OF_SCOPE

### Topic 1: Cross-node identity federation invariants
**Why out of scope**: O9 establishes node-locality structurally. Any federation mechanism would be a separate authentication/identity-binding layer atop O11. Belongs in a future federation ASN, not a revision to ownership.

### Topic 2: Ownership transfer mechanism
**Why out of scope**: The ASN explicitly flags this as an open question and treats O3's refinement regime as the design as specified. The tension with O6 (inalienable provenance) makes transfer a separable design decision requiring its own ASN.

### Topic 3: Revocation of delegation
**Why out of scope**: O8 establishes irrevocability as a design property. Any revocation mechanism would be a separate, distinct delegation model.

VERDICT: REVISE
