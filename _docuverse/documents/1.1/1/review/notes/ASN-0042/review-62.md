# Review of ASN-0042

## REVISE

### Issue 1: Bootstrap seed wording conflates seeding with allocation

**ASN-0042, Worked Example, State Σ₁**: "Suppose `a₁ = [1, 0, 2, 0, 3, 0, 1]` (a document element under account `[1, 0, 2]`) was allocated by `π_N` before delegation, so `a₁ ∈ Σ₀.B`."

**Problem**: The ASN's technical definition of `allocated_by_Σ(π, a)` is "the baptism procedure, executing on behalf of `π`, produced `a` during the transition yielding `Σ`." Bootstrap seeds enter `Σ_0.B` at genesis — there is no transition yielding `Σ_0`. The bootstrap-seeds table itself correctly distinguishes seed-coverage (`π_N`) from allocation, but this narrative line slips into the wrong category. The same issue recurs implicitly elsewhere when the worked example refers to "pre-delegation allocations."

**Required**: Replace "allocated by π_N before delegation" with "seeded in Σ_0.B under π_N's coverage" (or equivalent). Audit all worked-example prose for the same conflation.

### Issue 2: "Account-level family" misnomer in O7(c) chain construction

**ASN-0042, O7 proof of postcondition (c)**: "We exhibit an account-level family explicitly. The bootstrap principal is `π_0` with `pfx(π_0) = [1]`..."

**Problem**: `pfx(π_0) = [1]` has `zeros = 0`, which by T4c is node-level, not account-level. The proof correctly distinguishes the "boundary step π_0 → π_1" (which opens the user field) from the "inductive extension" for `k ≥ 1` — implicitly conceding that π_0 is structurally distinct from the rest. Calling the whole family "account-level" obscures this distinction and creates a small invariant-violation surface (a reader could miss that condition (iv) `zeros ≤ 1` applies non-vacuously at the boundary step).

**Required**: Rename to "chain of account-level delegates rooted at a node principal" or split presentation into the node→account boundary step (verified explicitly) and the within-account extension (verified inductively).

### Issue 3: O3 worked-example verification omits the delegator witness

**ASN-0042, Worked Example, State Σ₁, "O3 (refinement)"**: "The new principal `π_A ∈ Π_{Σ₁} ∖ Π_{Σ₀}` has `pfx(π_A) ≼ a₁` and `#pfx(π_A) = 3 > 1 = #pfx(π_N)`. ✓"

**Problem**: O3's postcondition is `(E π_d ∈ Π_Σ, π' ∈ Π_{Σ'} ∖ Π_Σ : ... ∧ delegated_Σ(π_d, π'))` — it requires existence of **both** the delegate and the delegator. The verification names only the delegate (`π_A`). Identifying `π_d = π_N` and noting that `delegated_{Σ_0}(π_N, π_A)` was verified above would close the loop. As stands, the worked example partially verifies O3's postcondition.

**Required**: Add explicit identification `π_d = π_N` (already verified) to the O3 line.

### Issue 4: Implicit uniqueness of the most-specific covering principal

**ASN-0042, delegation predicate condition (ii)**: "`(A π'' ∈ Π_Σ : pfx(π'') ≼ pfx(π') ⟹ #pfx(π'') ≤ #pfx(π))`"

**Problem**: Condition (ii) bounds prefix length but does not directly assert that `π` is unique. The proofs of O7(a) (case `pfx(π'') = pfx(π')`) and DelegatorAllocatesPrefix (the `π_a = π_d` step) both rely on the fact that no other `π'' ∈ Π_Σ` achieves `#pfx(π'') = #pfx(π)` with `pfx(π'') ≼ pfx(π')`. This uniqueness follows from O1b (PrefixInjectivity) plus the covering-chain lemma, but the inference is left implicit. A reader checking condition (ii) on its face cannot derive uniqueness without retracing this two-step argument.

**Required**: State as a derived corollary of condition (ii) + O1b + covering-chain lemma: "The most-specific covering principal of any tumbler in `Π_Σ` is unique." Cite at the proof sites that depend on it (O7(a), DelegatorAllocatesPrefix).

### Issue 5: O10's namespace-vs-content gap is acknowledged but not in the postcondition

**ASN-0042, O10 proof closing**: "The fork *as ownership boundary* (the architectural response O10 captures) is the structural act; content placement is the organizational continuation, conducted under the same sovereignty."

**Problem**: O10's narrative motivation is "modification of content," but for a node-level principal (`zeros(pfx(π)) = 0`) the single-baptism witness produces a namespace slot (`zeros(a') = 1`), not a content-bearing address. The prose acknowledges this honestly, but a reader of the formal contract — which says only `a' ∈ dom(π) ∩ Σ'.B ∧ ω_{Σ'}(a') = π` — could mistakenly take the postcondition to discharge the motivating content-modification scenario. Either the postcondition should record the structural-vs-content distinction (e.g., adding `zeros(a') = zeros(pfx(π)) + 1`), or the property's narrative should be reworded so the formal claim matches the motivation.

**Required**: Either strengthen the postcondition to characterize `a'`'s structural level, or restate the narrative as "the fork is the structural ownership response; content placement is an organizational continuation requiring additional baptisms when starting from node level."

## OUT_OF_SCOPE

### Topic 1: Mechanism by which delegation operations are invoked

**Why out of scope**: O7(c) asserts the **right** to delegate; the **act** of delegation (FEBE command, protocol step, authentication of the request) belongs to protocol/operations ASNs, and the Scope section correctly excludes BEBE / authentication mechanisms.

### Topic 2: Ownership transfer

**Why out of scope**: The ASN flags this as an Open Question and notes Nelson's ambivalence between "forevermore" and "bought document rights." Treating transfer as future work is correct — a transfer regime would require machinery (an off-address registry) outside the prefix model.

### Topic 3: Cross-node identity federation

**Why out of scope**: O9 establishes node-locality structurally. Federation would require an exogenous identity-binding mechanism; the *Principal Identity and the Trust Boundary* section correctly puts authentication outside the model.

VERDICT: REVISE
