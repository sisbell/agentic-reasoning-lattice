# Review of ASN-0042

## REVISE

### Issue 1: Missing state axiom — T4 validity of allocated addresses
**ASN-0042, Structural Provenance (O6)**: "All allocated addresses satisfy T4, so the restriction does not limit application."
**Problem**: This is asserted as fact but never stated as an axiom or derived from the stated properties. The `acct` function and `nodeField` function both depend on FieldParsing (ASN-0034), which requires T4 validity for well-defined field boundaries. O6's proof uses AccountPrefix, which requires `T4(a)`. O9's proof uses `nodeField(a)`, which requires `T4(a)`. O10's existence proof constructs addresses and implicitly relies on their T4 validity. The allocation mechanism is declared out of scope, so the T4 guarantee cannot be derived from O5, O16, or any other stated property — it must be axiomatized.
**Required**: Add an explicit state axiom alongside O12–O16:

`(A Σ, a : a ∈ Σ.alloc ⟹ T4(a))`

with the base case that initial addresses in `Σ₀.alloc` satisfy T4 and the inductive step that allocation preserves T4 (which the allocation mechanism, out of scope, must guarantee). Without this, O6 and O9 have a gap in their proof chains.

### Issue 2: O7(a) postcondition is tautological and state-ambiguous
**ASN-0042, Delegation**: "(a) `ω(a) = π'` for all `a ∈ dom(π') ∩ Σ.alloc` where `π'` has the longest matching prefix (O2 applies)"
**Problem**: Two issues. First, the qualifier "where `π'` has the longest matching prefix" makes the statement vacuous — it reduces to "ω(a) = π' for those a where ω(a) = π'," which is the definition of ω. The intended claim is that π' IS the longest match for all addresses in `dom(π')` at the moment of delegation, which follows from condition (vi) (no existing principal extends `pfx(π')`) but is not stated as a consequence. Second, the state reference is ambiguous: `Σ.alloc` presumably means the pre-delegation state, but `ω` should be subscripted as `ω_{Σ'}` (post-delegation) since the claim is about the consequence of delegation. The omitted subscript obscures which state the effective owner is computed in.
**Required**: State O7(a) as a categorical postcondition:

"(a) `ω_{Σ'}(a) = π'` for all `a ∈ dom(π') ∩ Σ'.alloc`"

with justification: by condition (vi), no principal in `Π_Σ` has a prefix strictly extending `pfx(π')`; by condition (i), `#pfx(π') > #pfx(π)` where `π` is the most-specific principal in `Π_Σ` covering `pfx(π')`; hence `π'` has the strictly longest matching prefix in `Π_{Σ'}` for every address in `dom(π')`.

### Issue 3: Domain nesting characterization excludes same-level nesting
**ASN-0042, Ownership Domains**: "`zeros(pfx(π₁)) < zeros(pfx(π₂)) ∧ pfx(π₁) ≼ pfx(π₂)  ⟹  dom(π₂) ⊆ dom(π₁)`"
**Problem**: This condition requires different zero counts (different hierarchical levels), excluding account-level nesting where both principals have `zeros = 1`. The ASN discusses this case extensively — `pfx(π₁) = [1, 0, 2]` and `pfx(π₂) = [1, 0, 2, 3]` both satisfy O1a with `zeros = 1`, and `dom(π₂) ⊂ dom(π₁)`. But the formal statement in the Ownership Domains section doesn't capture it. A reader encountering this statement before the account-nesting discussion could conclude that nesting requires different hierarchical levels. The general property `pfx(π₁) ≼ pfx(π₂) ⟹ dom(π₂) ⊆ dom(π₁)` is simpler, covers all cases, and is one line to prove (transitivity of `≼`).
**Required**: Replace the restrictive condition with the general statement. The zeros ordering can be noted as a corollary that characterizes the cross-level case, not as the defining condition.

## OUT_OF_SCOPE

### Topic 1: Allocation mechanism's obligation to preserve T4
**Why out of scope**: The ASN correctly declares the baptism mechanism out of scope. Once REVISE issue 1 is addressed (adding the T4 axiom on allocated addresses), the obligation transfers to the baptism specification: any conforming allocation mechanism must produce T4-valid addresses. This is a constraint on a future ASN, not an error in this one.

VERDICT: REVISE
