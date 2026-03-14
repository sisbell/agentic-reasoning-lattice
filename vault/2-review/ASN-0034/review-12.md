# Review of ASN-0034

## REVISE

### Issue 1: TA5 commentary makes false claim about immediate successor

**ASN-0034, TA5 (Hierarchical increment)**: "When k > 0, inc(t, k) produces the first child at depth k below t, which IS the immediate successor of t when k = 1 and the first intermediate position is 0 (giving t.0.1 — but this is t.0 extended, not t.0 itself)."

**Problem**: This sentence is factually wrong and internally confused. For k = 1: inc(t, 1) produces t.1 (one component appended, value 1, zero intermediate positions). The immediate successor of t in the total order is t.0 (the zero-extension), and t.0 < t.1, so inc(t, 1) is NOT the immediate successor. For k = 2: inc(t, 2) produces t.0.1, and t.0 < t.0.0 < t.0.1, so inc(t, 2) is also not the immediate successor. The sentence also conflates the k = 1 case (no intermediate positions) with the k = 2 case (one intermediate zero), producing the nonsensical phrase "when k = 1 and the first intermediate position is 0." This contradicts the ASN's own correct statement in the "Order structure" section: "Every tumbler has an immediate successor: its zero-extension."

**Required**: Replace with: "For any k > 0, inc(t, k) does NOT produce the immediate successor of t in the total order. For k = 1 the result is t.1; for k = 2 the result is t.0.1. In both cases, t.0 (the true immediate successor) lies strictly between t and the result. The gap between t and inc(t, k) contains t's entire subtree of zero-extensions."

### Issue 2: Global uniqueness proof — Case 4 does not cover parent's child-spawning output vs child's sibling outputs

**ASN-0034, Global uniqueness, Case 4**: "Since k' ≥ 1, the child's outputs are strictly longer than the parent's: γ₁ + k' > γ₁. By T3, a ≠ b."

**Problem**: Case 4's length-separation argument compares the parent's *sibling* outputs (length γ₁) against the child's sibling outputs (length γ₁ + k'). But the parent also produces a *child-spawning* output — the address inc(parent\_sibling, k') that established the child's prefix — which has length γ₁ + k', the *same* length as the child's sibling outputs. The length-separation argument does not apply to this pair. The four cases are supposed to be exhaustive over all pairs of distinct allocation events, and this pair falls in Case 4 (different allocators, nesting prefixes, same zero count) but is not covered by the argument.

The fix is straightforward: the parent's child-spawning output IS the child's base address, and every child sibling output equals inc(base, 0), inc(inc(base, 0), 0), etc. — each strictly greater than the base by TA5(a). So the child-spawning output is distinct from all child sibling outputs. But this one-sentence argument is missing from the proof of the ASN's most important theorem.

**Required**: Add to Case 4: "The parent's child-spawning output that established the child's prefix has the same length as the child's sibling outputs (both γ₁ + k'). However, this output IS the child's base address, and every child sibling output is strictly greater than its base (by TA5(a)), hence distinct."

### Issue 3: Subtraction definition — "When a = w" conflates T3 equality with zero-padded agreement

**ASN-0034, Definition (Tumbler subtraction)**: "When a = w (no divergence exists after padding), the result is the zero tumbler of length max(#a, #w)."

**Problem**: The notation "a = w" is T3 equality (same length and same components). But two tumblers of *different* lengths can agree after zero-padding — e.g., [1, 0] and [1] are distinct under T3 yet identical after padding [1] to [1, 0]. The parenthetical "(no divergence exists after padding)" is the correct condition, but "a = w" before it anchors the reader on T3 equality, which is a different (stricter) condition. An implementer checking `a == w` via T3 equality would skip this clause for [1, 0] ⊖ [1] and fall into the "Otherwise" branch, which expects a divergence point k — but no such k exists after padding. The algorithm is correct; the specification of when the zero-tumbler case applies is imprecise.

**Required**: Replace "When a = w (no divergence exists after padding)" with "When the zero-padded sequences agree at every position (no divergence exists)." This makes the condition unambiguous without relying on the overloaded "a = w" notation.

## OUT_OF_SCOPE

### Topic 1: Span level-matching constraint
The worked example correctly notes that a single-component length [3] applied to an 8-component element address produces a node-level address — semantically wrong. T12 requires only k ≤ #s (algebraic well-formedness), not that the action point match the hierarchical level of the start address. Formalizing the level-matching constraint (the action point of a span length should correspond to the element-field depth of the start address) belongs in a future ASN on span semantics.

**Why out of scope**: T12 defines algebraic well-formedness; semantic span constraints are a separate concern that requires the operation layer.

### Topic 2: Implementation finite-model constraints
The ASN correctly notes that Gregory's 16-digit mantissa violates T0 and asks whether reachable allocation states can be shown to stay within a finite representation. This is an implementation verification question, not an algebraic one.

**Why out of scope**: The abstract algebra is defined over unbounded naturals; bounding the reachable state space is a finite-model theory question for a future ASN.

VERDICT: REVISE
