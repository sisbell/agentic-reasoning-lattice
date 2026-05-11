# Review of ASN-0036

## REVISE

### Issue 1: S7a–S7d contracts implicitly assume T4-validity of `a ∈ dom(Σ.C)` but their Depends lists do not make this transparent

**ASN-0036, S7b Formal Contract**: "*Axiom (design requirement):* `(A a ∈ dom(Σ.C) :: zeros(a) = 3)`. *Postconditions:* By T4's field correspondence, all four identifying fields — node, user, document, element — are present and the element field exists. The projections `N(a)`, `U(a)`, `D(a)`, `E(a)` supplied by T4b are all well-defined. *Depends:* T4 (HierarchicalParsing, ASN-0034) — field correspondence; T4b (UniqueParse, ASN-0034) — projection definitions."

**Problem**: S7b's axiom constrains only the zero-count (`zeros(a) = 3`), but the postcondition requires T4-validity to apply — T4b's projections are defined only on T4-valid tumblers (no adjacent zeros, positive endpoint components, in addition to `zeros ≤ 3`). For `a ∈ dom(Σ.C)`, T4-validity is supplied by T10a.4 (T4PreservationUnderDiscipline) combined with S0 (persistence), neither of which appears in S7b's Depends. S7c has the identical omission — it cites S7b, T4b, TA7a but not T10a.4. S7a's contract presupposes `D(a)` and the truncation `N(a).0.U(a).0.D(a)`, both of which require T4-validity, yet S7a lists T10a (which implicitly subsumes T10a.4 only as a numbered postcondition) without citing T10a.4 directly. S7d's axiom names "the result of an allocation event under T10a" — implicit T4-validity via T10a's postconditions — but again lists T10a, not T10a.4, in Depends. S7's overall proof correctly invokes T10a.4 to discharge the T4-validity step, but the individual sub-axiom contracts are not self-supporting; a reader of S7b's contract alone cannot derive the projection-well-definedness postcondition from the stated dependencies.

**Required**: Either (a) add T10a.4 (and S0 where it discharges the persistence step) to the Depends lists of S7a, S7b, S7c, S7d, each with a one-line note on the role T10a.4 plays in delivering T4-validity for elements of `dom(Σ.C)`; or (b) strengthen each axiom to require T4-validity explicitly in addition to the zero-count or depth constraint (e.g., S7b becomes "every `a ∈ dom(Σ.C)` is T4-valid with `zeros(a) = 3`"). Option (a) preserves the layered minimal-axiom presentation; option (b) makes each sub-axiom self-supporting on its own contract.

VERDICT: REVISE
