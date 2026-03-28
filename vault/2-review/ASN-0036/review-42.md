# Proof Verification: S0

RESULT: FOUND

**Problem**: The property section has no `*Formal Contract:*` section. S0 states a universal invariant over all state transitions but the section ends after the weakest-precondition restatement without a formal contract summarizing the invariant.

Additionally, the section's status is ambiguous: it describes what S0 *requires* of operations but never states whether S0 is an **axiom** (imposed by design on the two-stream architecture) or a **derived invariant** (proved by case analysis over all operations). The text "This is the central invariant of the two-stream architecture" and "This constrains every operation" reads as a design constraint, but if so it should be explicitly labeled as an axiom. If it is instead meant to be proved, no proof is present — there is no enumeration of operations and no per-operation argument that each preserves `dom(C)` membership and value equality.

**Required**:

1. Add a formal contract. If S0 is an axiom:
   ```
   *Formal Contract:*
   - *Invariant:* a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a) for every transition Σ → Σ'
   - *Axiom:* imposed as a design constraint on all content-store operations
   ```

2. If S0 is instead a derived property, provide the proof: enumerate every operation that produces a successor state Σ' and show that each either (a) does not modify `C`, or (b) only extends `dom(C)` at fresh addresses with new values, leaving all existing mappings intact. This would require declaring dependencies on the definitions of those operations.
