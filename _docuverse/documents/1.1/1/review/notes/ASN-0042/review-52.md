# Review of ASN-0042

## REVISE

### Issue 1: Worked example creates two inconsistent trajectories for Σ_0
**ASN-0042, Worked Example**: "Suppose a₁ = [1, 0, 2, 0, 3, 0, 1] (a document element under account [1, 0, 2]) was allocated by π_N before delegation, so a₁ ∈ Σ_0.B."

Later in the Fork section: "Pre-delegation (by π_N as most-specific covering principal of [1, 0, 2] in Σ_0): successive Bop([1, 0, 2], 2) calls baptize [1, 0, 2, 0, 1], then [1, 0, 2, 0, 2], then [1, 0, 2, 0, 3]... then Bop([1, 0, 2, 0, 3], 2) baptizes element a₁."

**Problem**: The first framing treats Σ_0 as the bootstrap state with a₁ already seeded; the second treats Σ_0 as having undergone pre-delegation Bop sequences to produce a₁. Under the first framing, the pre-delegation Bop trajectory cannot occur "at Σ_0" because Σ_0 is the source state. Under the second framing, the original claim "a₁ ∈ Σ_0.B" requires Σ_0 to be reached *after* some baptism transitions, contradicting Σ_0's bootstrap status.

**Required**: Either (a) explicitly designate Σ_0 as a seeded state containing a₁ plus all required B1-prerequisite ancestors {[1, 0, 1], [1, 0, 2, 0, 1], [1, 0, 2, 0, 2], [1, 0, 2, 0, 3]} as seeds, and remove the "Bop calls baptize..." framing from the Fork section; or (b) introduce intermediate states Σ_{-3}, Σ_{-2}, Σ_{-1}, Σ_0 with explicit transitions, with seeds limited to {[1], [2]}. The current dual framing creates confusion when verifying B₀ conf., B1, and O14 simultaneously.

### Issue 2: "delegated_Σ*" is defined informally
**ASN-0042, NestingByDelegation**: "where delegated_Σ*(π, π') denotes the reflexive-transitive closure of 'there exists a state Σ_k on the transition path Σ₀ → ... → Σ such that delegated_{Σ_k}(π, π') held at that step.'"

**Problem**: The base relation that gets transitive-closed is conflated with the closure. The phrase "reflexive-transitive closure of 'there exists a state...'" suggests closing over states, but the closure is over principal pairs. The witness-preservation arguments in NestingByDelegation's proof depend on this being precisely formalized.

**Required**: Define explicitly: let R_Σ ⊆ Π × Π be the relation R_Σ(π, π') iff there exists Σ_k on the witnessing path Σ₀ → ... → Σ with delegated_{Σ_k}(π, π'). Then delegated_Σ* is the reflexive-transitive closure of R_Σ in the standard sense (∪_{n≥0} R_Σ^n with identity at n=0).

### Issue 3: "AccountLevelPermanence" name overpromises
**ASN-0042, Permanence and Refinement section**: "AccountLevelPermanence (Account-level permanence). No principal external to dom(π) can alter effective ownership within dom(π)."

**Problem**: The formal property quantifies over arbitrary π ∈ Π_Σ — it applies at every principal level (node, account, sub-account chains), not specifically at the account level. Nelson's "forevermore" language motivated the name, but the formal statement is more general than the name suggests.

**Required**: Either rename to reflect the generality (e.g., "DomainSovereignty" or "OwnershipDomainPermanence") and note in prose that the account-level case is the historically motivating instance, or restrict the formal statement to account-level principals (clearly weaker). The current asymmetry between informal name and formal scope invites misreading.

### Issue 4: O10 worked example's Σ_pre construction omits required B1 verification
**ASN-0042, Worked Example, Fork (O10)**: "B1 applied intra-stream to S([1, 0, 2], 2) is then consistent with the trajectory: children(Σ_pre.B, [1, 0, 2], 2) = {[1, 0, 2, 0, k] : 1 ≤ k ≤ 5}. Hence hwm(Σ_pre.B, [1, 0, 2], 2) = 5."

**Problem**: The trajectory passes through 5 successive Bop([1, 0, 2], 2) calls plus 2 Bop calls into element streams plus the delegation transition. Each transition's B6 obligation (T4(p), zeros(p)+(d-1)≤3) needs verification, and each B1 obligation requires the cumulative children set to be a contiguous prefix. The example asserts the final invariants hold but doesn't trace per-transition obligations. For Bop([1, 0, 2, 0, 3], 2): zeros([1, 0, 2, 0, 3]) = 2, so 2 + 1 = 3 ≤ 3 — at the bound. This is a non-trivial check.

**Required**: Either explicitly verify B6 and B1 at each step of the trajectory, or state upfront that intermediate verifications are omitted and only the cumulative state is checked. The current presentation reads as if the trajectory is being verified step-by-step but actually skips intermediate obligations.

### Issue 5: O3's corollary on monotonic refinement is stated for "all transitions" without restricting to address-preserving ones
**ASN-0042, O3 Corollary**: "#pfx(ω_{Σ'}(a)) ≥ #pfx(ω_Σ(a)) in all transitions."

**Problem**: For ω_Σ(a) to be defined, a ∈ Σ.B. For ω_{Σ'}(a) to be defined, a ∈ Σ'.B. If a is newly allocated in the transition (a ∈ Σ'.B ∖ Σ.B), then ω_Σ(a) is undefined and the inequality is ill-formed. The corollary's prose handles "ω_{Σ'}(a) = ω_Σ(a)" and "ω_{Σ'}(a) ≠ ω_Σ(a)" but assumes both are defined.

**Required**: Add a precondition a ∈ Σ.B (so ω_Σ(a) is defined; ω_{Σ'}(a) is then defined via B0). Currently the corollary's domain of applicability is implicit and could mislead readers into applying it to newly-baptized addresses.

### Issue 6: Property table for O2 omits load-bearing dependencies
**ASN-0042, Properties Introduced table**: "O2 | Every allocated address has exactly one effective owner ω(a)... | from O4, O1b"

**Problem**: The proof of O2's existence-and-uniqueness uses four explicit steps citing the Prefix (PrefixRelation) definition of ASN-0034 (Step 2 chain ordering), T3 (CanonicalRepresentation) for step 3's "each covering prefix is uniquely determined by its length," and the covering-chain lemma. The table omits Prefix and T3.

**Required**: Update the table entry to "from O4, O1b, Prefix, T3" — these are necessary for the existence-of-unique-maximum argument. Similar audits warranted for other entries (e.g., O10's citation list omits O1b, which is used to exclude pfx(π'') = pfx(π) in the non-coverage closure).

VERDICT: REVISE
