# Review of ASN-0107

## REVISE

### Issue 1: A1's justification asserts a false dependency for the existence count

**ASN-0107, "How the Count Changes: Content Added", A1 (FreshContentNeutrality)**: "K.α adds no element to `dom(Σ.L)` and leaves every `coverage` and the fixed `Q` unchanged (E3), so `match(Q, Σ)` is untouched; the new content address is irrelevant to the count unless it lies in Q, which a request denoting unchanged content excludes."

**Problem**: The clause "irrelevant to the count *unless it lies in Q*" is wrong for the existence count, and it undercuts the very argument it accompanies. For a fixed permanent request, `match(Q, Σ) = {a ∈ dom(Σ.L) : (A i :: coverage(Σ.L(a).eᵢ) ∩ Qᵢ ≠ ∅)}` is a function of the (permanent) coverages and the (fixed) address set `Q` only — both of which are independent of whether content is *stored* at any address. Concretely, if `a_new ∈ Q` and some orphan link `ℓ` already has `a_new ∈ coverage(Σ.L(ℓ).eᵢ)` (a ghost reference, LP17), then `coverage(Σ.L(ℓ).eᵢ) ∩ Qᵢ ∋ a_new ≠ ∅` *already holds at every state*, before and after the K.α step that materialises content at `a_new`. So `ℓ` matched before allocation and matches after; the count does not move. The existence count is unaffected by K.α **whether or not `a_new ∈ Q`** — the qualifier "unless it lies in Q" implies a dependency that does not exist and weakens A1 rather than supporting it.

**Required**: Drop or restate the qualifier. The correct justification is unconditional: for the existence count, K.α changes neither `dom(Σ.L)` nor any coverage nor the fixed `Q`, so `match(Q, ·)` is invariant regardless of where (or whether) the new address sits in `Q`. The membership of `a_new` in `Q` is relevant only to the *discovery* anchoring (where `Q(Σ)` tracks the arrangement), which the following sentences already handle via the no-incoming-links premise.

### Issue 2: R1's statement is a single ~12-line sentence with nested conditions

**ASN-0107, "How the Count Changes: Links Retracted", R1 (MinimalDecrementNoStoreRetraction)**: "In the minimal case — contracting away a single consulted entry that is the *last* consulted V-position mapping to its resolved I-address `a` (so `a` leaves `Qᵢ(Σ')`), where `a` is reached, in the relevant slot, by exactly one matching link `ℓ`, *and that link's slot-`i` coverage meets `Qᵢ(Σ)` only at `a`* — formally `coverage(Σ.L(ℓ).eᵢ) ∩ Qᵢ(Σ) = {a}` … the discovery count drops by exactly one …"

**Problem**: The claim is correct on analysis, but it is delivered as one sentence stacking four interacting conditions (last-position, sole-matching-link, sole-reach, and the `Δ ∈ {−1,0}` split) with em-dash nesting that obscures which conditions are necessary for `−1` versus `0`. A reader cannot extract the precondition set without reconstructing it. This is the kind of load-bearing operational claim where the conditions must be enumerated, not run together.

**Required**: Break R1 into an explicit precondition list and a two-line case split (`coverage(ℓ.eᵢ) ∩ Qᵢ(Σ) = {a}` ⟹ `Δ = −1`; otherwise alternate reach survives ⟹ `Δ = 0`), so the `k = 1` specialisation of R2 reads as a clean derivation rather than a parenthetical aside.

## OUT_OF_SCOPE

### Topic 1: Independently-anchored multi-document requests
The first open question (three parts anchored to different evolving arrangements) is correctly deferred; the invariants there require a multi-arrangement model this ASN does not build.

### Topic 2: Coincidence of discovery and existence counts
The second open question (when every resident matching link is currently discoverable) is genuinely new territory bridging `Σ.L` and `Σ.M` reachability, appropriately left open.

VERDICT: REVISE
