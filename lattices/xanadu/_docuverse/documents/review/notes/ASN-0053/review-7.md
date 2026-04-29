# Review of ASN-0053

## REVISE

### Issue 1: Incorrect parenthetical claim about #a < #b round-trip
**ASN-0053, "The reach function"**: "(The case #a < #b also admits a faithful round-trip — the D1 proof generalizes straightforwardly — but since every span operation below uses level-uniform spans with #start = #reach, the equal-length case is all we need.)"

**Problem**: The claim is false for type (ii) divergence (prefix case). When a is a proper prefix of b — e.g., a = [1, 3], b = [1, 3, 5] — the divergence is k = #a + 1 = 3, exceeding #a = 2. The displacement b ⊖ a = [0, 0, 5] has action point 3 > #a, violating TA0. The addition a ⊕ (b ⊖ a) is undefined. The D1 proof only generalizes when the divergence is type (i), i.e., when the tumblers differ at a shared position rather than one being a prefix of the other.

**Required**: Either qualify the statement — "The case #a < #b with type (i) divergence (k ≤ #a) also admits a faithful round-trip" — or remove the parenthetical entirely, since it is not load-bearing (the ASN correctly restricts all subsequent work to #a = #b).

## OUT_OF_SCOPE

### Topic 1: Existence conditions for level-compatible interior points
S4 is conditional on a level-compatible interior point existing, but such points may not exist — e.g., the span ([1, 5], [0, 1]) has no length-2 tumbler strictly between [1, 5] and [1, 6]. A characterization of when S4 is applicable (the width component at the action point must exceed 1) belongs in a future ASN on span operations or document editing, not here.
**Why out of scope**: S4 is correctly stated as a conditional; the existence question is about the tumbler space's discrete structure, not the span algebra's correctness.

### Topic 2: Normalization for mixed-level span-sets
S8 requires mutual level-compatibility. Span-sets mixing tumblers of different lengths (e.g., a set containing [1, 3] and [1, 3, 0, 5]) have no normalization guarantee. This matters for cross-depth content operations.
**Why out of scope**: The ASN's open questions already identify cross-level interaction as future work. The level-uniform restriction is a deliberate scope boundary.

### Topic 3: Algebraic structure of the span algebra
The ASN proves individual properties (commutativity, associativity of union, uniqueness of normal form) but does not identify the span algebra as an instance of a known algebraic structure (e.g., a Boolean algebra over a distributive lattice of intervals). This would unify the individual results.
**Why out of scope**: Identifying the abstract algebraic structure is a future theoretical contribution, not a gap in the current ASN's correctness.

VERDICT: REVISE
