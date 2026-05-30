# Review of ASN-0042

This is a heavily-revised note (rev. 41) and the mathematics is, as far as I can verify, sound: O2's four-step uniqueness, O3's equal-length exclusion, O8's longest-match permanence, O10's Form-A/Form-B coverage exhaustion, and the subtle monotonicity of `R_Σ` under condition (iv) in NestingByDelegation all check out, including the worked-example arithmetic. My findings are confined to accreted meta-prose, consistent with this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Defensive forward-reference annotation in OwnershipDomainPermanence
**ASN-0042, Permanence and Refinement (OwnershipDomainPermanence statement)**: "This is the formal consumer of NestingByDelegation: the 'sub-delegate' reading is not informal commentary but the `covers_Σ*` conjunct, discharged in Step 4 below."
**Problem**: This sentence advances no reasoning. It defends an earlier gloss against being read as informal and forward-points to the proof step that discharges it — exactly the "prose justifying that a downstream location does the work" pattern. The `covers_Σ*` conjunct is already in the formula above it.
**Required**: Delete the sentence. The formula plus the one-line gloss ("if any address in `odom(π)` changes owner, the delegator `π_d` satisfies `covers_Σ*(π, π_d)`") suffices.

### Issue 2: "π_d is π or a sub-delegate of π" restated five times
**ASN-0042, OwnershipDomainPermanence (statement gloss, Step 4 head, Step 4 conclusion, Formal Contract postcondition, Invariant)**: the same fact — `covers_Σ*(π, π_d)` reads as "π itself or a sub-delegate of π" — appears in the formula gloss ("In words, `π_d` is `π` itself or a sub-delegate"), the Step-4 heading, the Step-4 closing ("This is the precise formal content of…"), the postcondition, and the invariant.
**Problem**: Two paragraphs (and three contract lines) saying the same thing in different words. The natural-language reading needs stating once.
**Required**: State the "`π` or sub-delegate" reading once (at first use), and let Step 4 and the contract carry the bare `covers_Σ*(π, π_d)` symbol without re-glossing.

### Issue 3: Use-site inventory closing the O10 worked example
**ASN-0042, Worked Example (Fork)**: "With `π_A`'s sibling-advance fork and `π_B`'s field-opening fork both exhibited on concrete addresses, the two `hwm_0` branches of Unilateral O10★ are witnessed; with `π_N`'s node-level fork added, both principal levels … are witnessed as well." This duplicates the earlier *Node-level fork* lead-in ("The two forks above are both account-level … exercising the `hwm_0 > 0` and `hwm_0 = 0` branches…").
**Problem**: An inventory of which cases the example covered — meta-commentary about the demonstration rather than part of it — stated twice, opening and closing. The three concrete forks speak for themselves.
**Required**: Drop the closing inventory paragraph and the redundant clause of the *Node-level fork* lead-in; keep only the single sentence that says the node-level case (`zeros(pfx)=0`) is structurally distinct because Form-A sub-delegates become live.

### Issue 4: O7(c) proof paragraph mixes reasoning with restated commentary
**ASN-0042, O7 postcondition (c) proof**: the single essay-length paragraph establishes the entry-state discharge of conditions (i),(ii),(iv) — genuine reasoning — but then restates the self-perpetuation conclusion ("the right is self-perpetuating, bounded only by condition (iii)'s `zeros(p'') ≤ 1`") which is also asserted in the Formal Contract and again demonstrated in the *Unbounded recursion* worked example.
**Problem**: The same self-perpetuation claim lands three times (proof tail, contract, example). The proof paragraph would read more cleanly split at the entry-state-vs-per-state boundary.
**Required**: End the O7(c) proof at the per-state discharge of condition (v); let the *Unbounded recursion* example carry the "self-perpetuating" demonstration without the proof pre-announcing its own conclusion.

## OUT_OF_SCOPE

None. The ASN correctly relegates ownership transfer, cross-node federation, and accessibility-on-principal-death to Open Questions rather than defining claims for them.

VERDICT: REVISE
