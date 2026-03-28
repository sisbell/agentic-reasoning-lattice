### [REVIEW-49] [VERIFIED] T0

### [REVIEW-49] [VERIFIED] T0(a)

### [REVIEW-49] [VERIFIED] T3

### [REVIEW-49] [VERIFIED] T1

### [REVIEW-49] [VERIFIED] TA1

### [REVIEW-49] [VERIFIED] TA1-strict

### [REVIEW-49] [VERIFIED] Divergence

### [REVIEW-49] [VERIFIED] T4

### [REVIEW-49] [VERIFIED] TA6

### [REVIEW-49] [VERIFIED] TA3

### [REVIEW-49] [VERIFIED] TumblerSub

### [REVIEW-49] [VERIFIED] TA2

### [REVIEW-49] [VERIFIED] TA4

### [REVIEW-49] [VERIFIED] TumblerAdd

### [REVIEW-49] [VERIFIED] TA0

### [REVIEW-49] [VERIFIED] D0

### [REVIEW-49] [VERIFIED] D1

### [REVIEW-49] [VERIFIED] TA-LC

### [REVIEW-49] [VERIFIED] D2

### [REVIEW-49] [VERIFIED] TA5

### [REVIEW-49] [VERIFIED] T10

### [REVIEW-49] [VERIFIED] T10a

### [REVIEW-49] [VERIFIED] T2

### [REVIEW-49] [FOUND] T8
RESULT: FOUND

**Problem**: The formal contract's Frame clause mischaracterizes algebraic properties and pure functions as state-transition operations. It states:

> *Frame:* Read-only operations (T1, T2, T4) and pure arithmetic (⊕, ⊖, inc) preserve the allocated set exactly: `allocated(s') = allocated(s)`.

T1 (lexicographic order definition), T2 (intrinsic comparison property), and T4 (hierarchical parsing axiom) are not operations — they are static properties of the tumbler algebra that define no state transitions. Similarly, ⊕, ⊖, and inc are pure functions from tumblers to tumblers; they do not act on system state. None of these items can "preserve" or "fail to preserve" `allocated(s)` because they never produce a state `s'` from a state `s`. The Frame clause is vacuously true but categorically wrong in what it identifies as operations.

Additionally, this Frame claim is not present in the narrative text of T8. The narrative states only "No operation removes an allocated address from the address space" (captured by the Axiom field) and "The set of allocated addresses is monotonically non-decreasing" (captured by the Invariant field). The exact-preservation claim for specific "operations" is an expansion introduced in the formal contract with no narrative basis.

**Required**: Either (a) remove the Frame clause entirely, since T8 is a design axiom about monotonicity and does not need to identify specific operations that preserve exactly — that analysis belongs in the operation ASNs where each operation's effect on `allocated(s)` is individually proved; or (b) rewrite the Frame to correctly characterize what it means: "Pure tumbler algebra (comparison, parsing, arithmetic) does not interact with allocation state; only system operations (INSERT, COPY, DELETE, etc.) produce state transitions, and T8 constrains those transitions." This would be narrative clarification rather than a formal Frame clause, since the items in question are not operations with state transitions.
