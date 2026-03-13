# Review of ASN-0034

## REVISE

### Issue 1: TA6 formal statement omits the ordering claim it is cited for

**ASN-0034, TA6**: "Every zero tumbler is less than every positive tumbler under T1."

**Problem**: The TA6 label carries two claims in prose — (1) no zero tumbler is a valid address, and (2) every zero tumbler is less than every positive tumbler. The formal formula captures only claim (1). Yet the TA3 proof (Case 0, sub-case "a = w" and sub-case "a > w without divergence") cites "by TA6" to invoke claim (2). The Properties Introduced table also lists both claims under TA6. A citation to a labeled property should resolve to a formalized statement; here it resolves to the wrong one.

**Required**: Add a second formal line to TA6:

`(A s, t ∈ T : (A i : 1 ≤ i ≤ #s : sᵢ = 0) ∧ (E j : 1 ≤ j ≤ #t : tⱼ > 0) ⟹ s < t)`

The argument already appears in the paragraph preceding TA6; it just needs to be elevated into the formal statement.

### Issue 2: TA3 Case 0 proof — inaccurate justification for tail positions

**ASN-0034, TA3 verification, Case 0 sub-case "a > w with divergence"**: "(b ⊖ w)ᵢ = bᵢ ≥ 0 (from b's actual components, copied in the tail phase since i > d)"

**Problem**: This sentence covers positions `#a < i ≤ max(#a, #w)`. When `#w > #b` (which occurs when `#a < #b < #w`), positions `#b < i ≤ #w` fall within this range. At those positions the minuend `b` is zero-padded, so `(b ⊖ w)ᵢ = 0`, not `bᵢ` — `b` has no actual component at position `i > #b`. The conclusion `(a ⊖ w)ᵢ ≤ (b ⊖ w)ᵢ` still holds (both are zero), so the proof is logically valid, but the stated justification is wrong for that sub-range. A reader following the proof step-by-step encounters a claim that attributes zero-padded values to "b's actual components."

**Required**: Replace the sentence with something like: "At positions `#a < i ≤ max(#a, #w)`: `(a ⊖ w)ᵢ = 0` (from `a`'s zero padding). For `(b ⊖ w)ᵢ`: when `i ≤ #b`, the value is `bᵢ` (copied in the tail phase); when `i > #b`, the value is `0` (from `b`'s zero padding). In either case `(a ⊖ w)ᵢ ≤ (b ⊖ w)ᵢ`."

## OUT_OF_SCOPE

### Topic 1: Span operations beyond well-formedness
The ASN defines span well-formedness (T12) and verifies basic span computation. Intersection, union, splitting, and behaviour when spans cross hierarchical field boundaries are not addressed. These are operations on spans, not properties of the tumbler algebra itself.

**Why out of scope**: Span operations compose the algebra's primitives into higher-level machinery — a future ASN on span arithmetic or content reference.

### Topic 2: Complete allocation protocol
T10a constrains each allocator to `inc(·, 0)` for siblings and `inc(·, k>0)` for child-spawning, but does not specify the full protocol: when child-spawning occurs, whether multiple children can be spawned from the same parent output, or how the initial allocator at each level is bootstrapped. The proofs (partition monotonicity, global uniqueness) work under T10a's constraints without needing the full protocol.

**Why out of scope**: Protocol specification is system design, not algebra. The algebraic properties are sufficient to prove uniqueness and ordering.

VERDICT: REVISE
