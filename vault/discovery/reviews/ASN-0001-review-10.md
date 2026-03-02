# Review of ASN-0001

## REVISE

### Issue 1: TA7a verification for ⊖ rests on a false claim about the divergence point

**ASN-0001, TA7a verification**: "Since the divergence point k is strictly after the subspace-identifier position (element-local displacements agree with the address at all prior positions), the subspace identifier is zeroed — but this position was E₁ in both operands (they share the same subspace), so it was part of the agreement prefix, not part of the divergence. The subspace identifier is preserved in the result."

**Problem**: The parenthetical "element-local displacements agree with the address at all prior positions" is false for the subtraction algorithm applied to full addresses. An element-local displacement like `[0,0,0,0,0,0,0,2]` has leading zeros at positions 1–7. A full element address like `[1,0,3,0,2,0,1,5]` has nonzero components at positions 1, 3, 5, 7. The subtraction algorithm finds the first divergence between minuend and subtrahend — that divergence is at position 1 (`1 ≠ 0`), not at position 8 in the element field. The subtraction produces `r₁ = 1 - 0 = 1`, then copies the remainder from the minuend, yielding the original address unchanged. This is a no-op, not the intended backward shift.

Contrast with addition: `⊕` uses the *action point* (first nonzero component of the displacement), which is at position 8 regardless of the address's prefix. The `⊕` verification is correct. But `⊖` uses the *first divergence between operands*, which is a structurally different concept. For full addresses with element-local displacements, divergence is at the node field, not the element field.

The verification conflates addition's action point with subtraction's divergence point. These are the same only when the operands agree on all positions before the displacement's action point — which requires the address to have zeros at those positions. For full addresses, this fails at position 1.

**Required**: Resolve the ambiguity about V-space position representation (see Issue 2) and rewrite the TA7a verification for `⊖` accordingly. If V-space positions are element-local (relative), state that explicitly and verify the claim for relative operands. If they are full addresses, either define element-local subtraction as a distinct operation or show that the existing `⊖` produces the correct result via a different argument.

### Issue 2: V-space position representation is ambiguous

**ASN-0001, multiple sections**: The TA7a section says "A V-space position in a document has the form `p.0.E₁.E₂. ... .Eδ` where `p` is the document prefix" — suggesting full tumblers. The T11 section says "V-positions run contiguously from 1 to the document's current length" — suggesting simple counters. The worked example uses single-component tumblers `v₁ = [1]` through `v₅ = [5]` "(single-component tumblers for simplicity)."

**Problem**: The "for simplicity" parenthetical leaves open whether full-address V-positions exist in the general case. This ambiguity is not merely editorial — it determines whether TA7a for `⊖` is verifiable (Issue 1), whether TA4's precondition (all components before `k` are zero) is satisfied for editing shifts, and whether TA1-strict's precondition (`k ≥ divergence(a,b)`) holds for element-level operations.

If V-positions are always element-local (relative to a subspace context), then:
- TA4's precondition is trivially satisfied for single-component positions (`k = 1`, no positions before `k`).
- TA1-strict holds because all positions diverge at component 1 = action point.
- TA7a for `⊖` is trivially true (no subspace identifier in the operand to corrupt).
- But then the TA7a verification's discussion of full addresses is misleading.

If V-positions are full addresses, then:
- TA4's precondition fails for editing shifts (nonzero prefix components before the element field).
- TA7a for `⊖` is incorrect as verified.
- The statement "V-positions run contiguously from 1 to the document's current length" would need reinterpretation.

**Required**: State definitively whether V-space positions are element-local (relative to document and subspace context) or full tumblers. Then verify TA4, TA1-strict, and TA7a against the chosen representation.

### Issue 3: TA7a verification for ⊖ self-contradicts

**ASN-0001, TA7a verification**: "the subspace identifier is zeroed — but this position was E₁ in both operands (they share the same subspace), so it was part of the agreement prefix, not part of the divergence. The subspace identifier is preserved in the result."

**Problem**: The verification says "the subspace identifier is zeroed" and then two clauses later says "the subspace identifier is preserved in the result." Both cannot be true. The subtraction algorithm zeros all positions before the divergence point. If the subspace-identifier position is before the divergence (as the verification claims), it IS zeroed. The text attempts to argue that because both operands agree at that position, zeroing preserves the value — but zeroing sets the position to 0, not to the agreed-upon value. If `E₁ = 1` (text subspace), zeroing produces 0, not 1.

The error arises from confusing "part of the agreement prefix" with "preserved." In the subtraction algorithm, the agreement prefix is precisely what gets zeroed. Components after the divergence are copied from the minuend; components before the divergence are set to zero. Agreement does not imply preservation — it implies destruction.

**Required**: Delete the incorrect argument. Replace with a correct verification that accounts for the actual behavior of `⊖` on the operands (which depends on resolving Issue 2).

## DEFER

### Topic 1: Span splitting algebra for partial-overlap operations
**Why defer**: DELETE spanning multiple spans with partial overlap requires splitting a span at an arbitrary point and adjusting endpoints. The ASN defines spans (T12) and arithmetic (TA0–TA4) but does not formalize the splitting operation or prove that split halves tile correctly. This belongs in an ASN on document editing operations.

### Topic 2: Enfilade width composition property
**Why defer**: TA8 states orthogonality of dimensions in 2D displacement arithmetic, but the composability property referenced in the vocabulary ("the parent's width is a function of children's widths") is not formalized. What algebraic properties must the component-wise `min` and `max` satisfy for the enfilade to correctly propagate range queries? This belongs in an ASN on enfilade structure.

### Topic 3: Empty document and zero-length span boundary cases
**Why defer**: The worked example starts with five characters. The ASN does not address: INSERT into an empty document (what is the starting V-position?), a span of length zero (T12 requires `ℓ > 0`, but does the system need to represent "the position between characters 3 and 4" as a zero-width span?), or DELETE of an entire document's content. These are operation-level boundary cases, not algebra-level gaps.

VERDICT: REVISE
