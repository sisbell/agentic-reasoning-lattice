# Review of ASN-0034

## REVISE

### Issue 1: D0 — spurious dependency on D1, missing TumblerSub
**Dependency graph, D0**: `follows_from: [D1, T3, TA0, TumblerAdd]`
**Problem**: D0 is a well-definedness precondition *for* D1; the derivation direction is D0 → D1, not D1 → D0. The paragraph's mention of D1 ("Round-trip faithfulness additionally requires #a ≤ #b … this establishes a ⊕ w = b (D1 below)") is a forward reference, not a premise. Additionally, D0's analysis explicitly constructs w = b ⊖ a using TumblerSub's definition, which is not listed. The ASN's own property table confirms the correct set: "from T3, TA0, TumblerAdd" — no D1.
**Required**: Remove D1 from D0's follows_from. Add TumblerSub.

### Issue 2: TA4 — undeclared dependency on TumblerSub
**Dependency graph, TA4**: `follows_from: [TumblerAdd]`
**Problem**: The verification of TA4 explicitly applies TumblerSub's constructive definition: "Now subtract w from r. The subtraction scans for the first divergence between r and w. For i < k: rᵢ = 0 = wᵢ …" The derivation constructs the subtraction result component by component using TumblerSub's formula, then verifies it equals a.
**Required**: Add TumblerSub to TA4's follows_from.

### Issue 3: ReverseInverse — undeclared dependencies on TumblerAdd and TumblerSub
**Dependency graph, ReverseInverse**: `follows_from: [TA3-strict, TA4]`
**Problem**: Two direct dependencies are missing. First, the proof invokes TumblerAdd's result-length identity: "#(y ⊕ w) = #w = k = #a (the first step by the result-length identity)." Second, it constructs y = a ⊖ w and analyzes its components via TumblerSub's definition: "the divergence falls at position k. The result y has: positions i < k zero, position k equal to aₖ − wₖ." Both are used directly in the derivation, not transitively through TA4.
**Required**: Add TumblerAdd and TumblerSub to ReverseInverse's follows_from.

### Issue 4: TA1-strict — undeclared dependency on TumblerAdd
**Dependency graph, TA1-strict**: `follows_from: [Divergence]`
**Problem**: The proof in "Verification of TA1 and TA1-strict" directly invokes TumblerAdd's constructive definition at every step: "the constructive definition gives (a ⊕ w)ᵢ = aᵢ and (b ⊕ w)ᵢ = bᵢ" (Case 3), "(a ⊕ w)ₖ = aₖ + wₖ < bₖ + wₖ = (b ⊕ w)ₖ" (Case 2), "both results copy from w, giving identical tails" (Case 1). All three cases operate on TumblerAdd's component-level structure.
**Required**: Add TumblerAdd to TA1-strict's follows_from.

### Issue 5: TA-MTO — spurious dependency on TumblerSub
**Dependency graph, TA-MTO**: `follows_from: [T3, TumblerAdd, TumblerSub]`
**Problem**: Neither the forward proof ("From TumblerAdd's definition: for i < k, (a ⊕ w)ᵢ = aᵢ …") nor the converse ("position i falls in the 'copy from start' region of TumblerAdd, so (a ⊕ w)ᵢ = aᵢ …") invokes TumblerSub in any step. The property characterizes equivalence classes of addition, not subtraction. Likely a false positive from textual proximity to TumblerSub's definition.
**Required**: Remove TumblerSub from TA-MTO's follows_from.

### Issue 6: D1 — undeclared dependency on Divergence
**Dependency graph, D1**: `follows_from: [T3, TA0, TumblerAdd, TumblerSub]`
**Problem**: The proof opens: "Let k = divergence(a, b). By hypothesis k ≤ #a ≤ #b, so this is type (i) divergence with aₖ < bₖ." The classification into type (i) — and the consequent conclusion aₖ < bₖ — comes from the Divergence definition, which distinguishes component divergence from prefix divergence.
**Required**: Add Divergence to D1's follows_from.

### Issue 7: PositiveTumbler — spurious dependencies
**Dependency graph, PositiveTumbler**: `follows_from: [T1, TA0, TA4]`
**Problem**: PositiveTumbler is a definition: "A tumbler t ∈ T is *positive*, written t > 0, iff at least one of its components is nonzero." The surrounding text mentions T1 (an ordering observation about positive vs. zero tumblers), TA0 and TA4 (as consumers of the w > 0 condition), but the definition itself is a predicate on components — it does not derive from any of these. A definition is not a derivation.
**Required**: Remove all entries from PositiveTumbler's follows_from (it has no derivation dependencies).

## OUT_OF_SCOPE

### Left cancellation for the order
**Why out of scope**: The ASN's open question — does a ⊕ x ≤ a ⊕ y imply x ≤ y? — is a natural extension of TA-LC and TA1-strict. The answer is non-trivial because the action points of x and y may differ, and the tail-replacement semantics complicate the comparison. This belongs in a follow-up analysis of the order-algebraic structure of ⊕, not in a revision of the current ASN.

VERDICT: REVISE
