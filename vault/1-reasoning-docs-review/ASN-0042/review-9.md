# Review of ASN-0042

## REVISE

### Issue 1: Principal-introduction closure axiom missing
**ASN-0042, Corollary (Account-level permanence)**: "No principal *external* to dom(π) — neither the delegating parent nor any sibling — can introduce a principal whose prefix extends pfx(π), because condition (ii) requires the delegator to be the most-specific covering principal for the new prefix, and that principal is π itself."

**Problem**: This argument relies on delegation being the *exclusive* mechanism for introducing principals into Π. The model defines the `delegated` relation (with its three conditions) and proves it preserves O1b, but never states that delegation and bootstrap (O14) are the only ways principals enter Π. O12 permits arbitrary growth: `Π_Σ ⊆ Π_{Σ'}` places no constraint on *how* new members arrive. A non-delegation mechanism that introduces a principal with a prefix extending `pfx(π)` would bypass condition (ii)'s authorization constraint, changing ω within `dom(π)` without π's consent — breaking the corollary.

The same gap affects the inductive preservation of O1a: the ASN shows delegation preserves `zeros ≤ 1`, but without closure, some other mechanism could introduce a principal at document level.

**Required**: Add a closure axiom, e.g.: "Principals enter Π exclusively through bootstrap (O14) or delegation (O7). No other state transition introduces new principals." This is the missing fourth state axiom alongside O12, O13, O14. Without it, the permanence corollary is a conjecture, not a theorem.

### Issue 2: O1b preservation proof covers only one case
**ASN-0042, Delegation preserves O1b**: "Suppose for contradiction that pfx(π') = pfx(π''') for some existing π''' ∈ Π_Σ."

**Problem**: The proof shows the new principal's prefix differs from every *pre-existing* principal's prefix (π''' ∈ Π_Σ). But O12 permits Π to grow by more than one element in a single transition — nothing constrains |Π_{Σ'} ∖ Π_Σ| ≤ 1. If two delegation acts in the same transition introduce π' and π₄ with `pfx(π') = pfx(π₄)`, the proof as written does not exclude this. The pairwise-distinctness case among newly introduced principals is missing.

**Required**: Either (a) constrain transitions to introduce at most one principal (simplest — add to the closure axiom from Issue 1), or (b) extend the proof: two new principals delegated the same prefix would require two delegators each satisfying condition (ii) for the same prefix in Π_Σ, but the most-specific covering principal is unique (by the total-order argument in O2), so both delegators would be the same principal π — then show π cannot delegate the same prefix twice (e.g., by condition (iii) requiring the delegate to be distinct from all of Π_Σ, but π' and π₄ could both satisfy this while colliding with each other).

### Issue 3: AccountPrefix lemma quantifier domain
**ASN-0042, Lemma (AccountPrefix)**: "`(A a ∈ T : acct(a) ≼ a)`"

**Problem**: The lemma quantifies over all of T (all tumblers), but `acct(a)` relies on field parsing (FieldParsing from ASN-0034), which assumes T4 validity. For a tumbler like `[0, 0, 1]` — which is in T but violates T4 — the "user field" is not well-defined, so `acct(a)` is not well-defined. The lemma's conclusion is sound for all valid addresses (and the ASN only applies it to allocated addresses, which satisfy T4), but the formal statement over-quantifies.

**Required**: Restrict the domain: `(A a ∈ T : T4(a) ⟹ acct(a) ≼ a)` or equivalently quantify over valid addresses.

### Issue 4: O10(b) is a consequence of O10(a), not an independent condition
**ASN-0042, O10 (DenialAsFork)**: "(b) when zeros(pfx(π)) = 1: pfx(π) ≼ acct(a')"

**Problem**: The O6 proof establishes the biconditional `pfx(π) ≼ a ≡ pfx(π) ≼ acct(a)` for any principal with `zeros(pfx(π)) ≤ 1`. Condition (a) gives `ω(a') = π`, which entails `pfx(π) ≼ a'`. The biconditional then yields `pfx(π) ≼ acct(a')` — condition (b) — without further argument. Presenting (b) as a coordinate condition alongside (a) and (c) suggests it carries independent content. It does not. Moreover, the restriction to `zeros = 1` is unmotivated: the derivation works identically for `zeros = 0` (where the prefix is trivially a prefix of everything in its domain, including the account field).

**Required**: Either derive (b) explicitly as a corollary of (a) via the O6 biconditional, or explain what independent constraint (b) adds beyond what (a) already establishes.

### Issue 5: O6 forward-direction wording overstates
**ASN-0042, O6 proof, forward direction**: "these leading components — being confined to node and user fields by the zero count — are exactly the components captured by acct(a)"

**Problem**: "Exactly" implies equality between `pfx(π)` and `acct(a)`. But the proof establishes `pfx(π) ≼ acct(a)` — a prefix relation, which permits strict containment. The ASN itself demonstrates strict containment in the worked example: `pfx(π_A) = [1, 0, 2]` while `acct(a₄) = [1, 0, 2, 3]`. The proof is correct; the word "exactly" misleads.

**Required**: Replace "are exactly the components captured by" with "fall within the components captured by" or "form a prefix of the components in."

## OUT_OF_SCOPE

### Topic 1: Ownership transfer mechanism
**Why out of scope**: The ASN correctly identifies this as an open question. Transfer would require machinery beyond the address-derived ownership model (a "deed" separate from the "birth certificate"). The ASN's conservative reading — O3 describes the system as specified; transfer is unspecified — is the right call for this ASN.

### Topic 2: Delegation recording and history reconstruction
**Why out of scope**: Whether delegation events must be recorded, or whether the address hierarchy provides sufficient structural evidence, is a system-design question that depends on operational requirements beyond the ownership model itself.

VERDICT: REVISE
