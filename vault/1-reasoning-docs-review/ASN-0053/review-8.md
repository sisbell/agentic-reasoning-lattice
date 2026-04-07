# Review of ASN-0053

## REVISE

### Issue 1: LeftCancellation proof omits the length-equality step required by T3

**ASN-0053, LeftCancellation**: "Every component agrees, so x = y."

**Problem**: T3 defines tumbler equality as same length AND same components. The proof establishes k₁ = k₂ = k and then shows x_i = y_i for all relevant positions, but never establishes #x = #y. The length equality is needed before component-wise comparison even makes sense (the range of "for i > k" depends on #x and #y agreeing). The step is: a ⊕ x = a ⊕ y implies #(a ⊕ x) = #(a ⊕ y) by T3, and since #(a ⊕ w) = #w for any w with action point ≥ 1 (from TumblerAdd's result-length formula), #x = #y follows.

**Required**: Insert the length-equality derivation before the component comparison. Conclude via T3 citing both conditions (same length, same components).

### Issue 2: S5 associativity well-definedness is asserted, not verified

**ASN-0053, S5**: "By the Associativity lemma from ASN-0034 (both compositions are well-defined since all tumblers have length #s)"

**Problem**: The parenthetical claims well-definedness from a length condition alone, but well-definedness of tumbler addition requires two things: the operand is positive (w > 0) and the action point falls within the base tumbler's length (TA0). The length condition handles the action-point bound but not positivity. Specifically, the right-side composition s ⊕ (d ⊕ d') requires d ⊕ d' to be positive. This holds — at position min(k_d, k_{d'}), the sum has a positive component — but the argument has three sub-cases (k_d < k_{d'}, k_d = k_{d'}, k_d > k_{d'}) and none are shown.

**Required**: Verify explicitly that (a) d ⊕ d' is positive (the component at min(k_d, k_{d'}) is > 0 in all cases), (b) the action point of d ⊕ d' is ≤ #s, and (c) the action point of d' is ≤ #d. Three lines, not a parenthetical.

## OUT_OF_SCOPE

### Topic 1: LeftCancellation belongs in the tumbler algebra foundation

**Why out of scope**: The ASN acknowledges this ("properly a tumbler arithmetic fact, belonging with ASN-0034"). It is a general property of tumbler addition, not specific to span algebra. Once corrected per Issue 1, it should be promoted to ASN-0034 so future ASNs can cite it from the foundation rather than re-deriving it.

### Topic 2: General span-set difference (without containment)

**Why out of scope**: S11 addresses only the containment case (⟦β⟧ ⊆ ⟦α⟧), giving a tight bound of 2 spans. The general difference of two overlapping span-sets — where neither contains the other, or where Σ₂ has multiple components — would yield a different bound and requires its own treatment. This is new territory for a future ASN, not an error in S11.

### Topic 3: Span denotation across hierarchical depths

**Why out of scope**: The denotation ⟦σ⟧ = {t ∈ T : s ≤ t < s ⊕ ℓ} includes tumblers at all depths between start and reach (e.g., [1, 3, 0, 5] is in ⟦([1, 3], [0, 4])⟧). The algebra correctly handles this — S4's partition is exact over all depths because T1 is a total order — but the distinction between "positions at the span's native depth" and "all positions in the denotation" is never formalized. Whether this distinction matters is a content-layer question that belongs in a future ASN on arrangement or content semantics.

VERDICT: REVISE
