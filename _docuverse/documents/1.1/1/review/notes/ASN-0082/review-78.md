# Review of ASN-0082

I worked through the arithmetic of both operations (I3/insertion and the contraction lemmas), the OrdinalExceedsDisplacement / OrdAddHom machinery, and all the worked examples. The mathematical content is sound and the boundary coverage (insert-at-start, insert-past-end, empty document; L=∅, R=∅, full deletion, cross-subspace) is genuinely complete. The TA4/TA2/TA3-strict precondition discharges at depth 1 check out, and the D-SEQ-post cardinality chain (N − c) is correct. My findings are confined to the anti-bloat patterns the review note asks me to surface.

## REVISE

### Issue 1: Accreted meta-prose in the Post-Contraction Shift preamble
**ASN-0082, "Post-Contraction Shift" → Scope / "We work with V-positions…" / Scoping axioms**: 

The scope restriction `S = 1` is stated four times in immediate succession — in the **Scope** note, in the "We work with V-positions…" paragraph, in the **Scoping axioms** (Subspace axiom), and again in the formal-contract **Preconditions**. The "We work with…" paragraph specifically accumulates three non-advancing patterns:

- A notation-convention sentence that also forward-points to the next paragraph: *"Throughout this section we write V_1(d) consistently — the contraction operation is scoped to the text subspace by the scoping axioms below, and any reference to a non-text subspace V_S(d) with S ≠ 1 is explicitly qualified."*
- Why-needed prose for the scoping axiom rather than what it says: *"The restriction to S = 1 is what lets us invoke the foundation's contiguity invariants D-CTG, D-MIN, and D-SEQ, which are stated for V_1(d)."*
- A redundant re-definition of `M(d) : T ⇀ T` (already introduced verbatim in Post-Insertion Shift and cited in the registry).

**Problem**: A reader must skip past a notation announcement, a forward reference to the paragraph directly below it, and a justification of *why* the restriction exists before reaching the axiom statements that actually carry the scope. This is the "new prose around an axiom explains why it is needed rather than what it says" and "forward-defers to a downstream location" pattern compounding at one site.

**Required**: Collapse to the two Scoping axioms (which state `S = 1` and `#p = 2` cleanly) plus the formal-contract preconditions. Delete the notation-convention sentence, the "what lets us invoke" justification, and the duplicate `M(d)` definition. The `(recorded at D-I)` aside in the Scope note plus the full D-I frame can keep a single statement of "content store unchanged."

## OUT_OF_SCOPE

### Topic 1: Depth > 1 generalization of gap-closure and the projection round-trip
**Why out of scope**: The Open Questions already correctly mark the depth-2 restriction (`#p = 2`) and the TA4/S8a collision at intermediate components as future work. The `#p = 2` scoping is a deliberate, internally consistent choice for this ASN, not a defect — generalizing D-SEP/D-DP to deeper ordinals belongs in a follow-on ASN.

META: (not applicable — the ASN defines arrangement-layer operations, invariants, and their preservation abstractly; it has not drifted into implementation mechanics.)

VERDICT: REVISE
