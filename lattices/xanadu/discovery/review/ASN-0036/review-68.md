I'll read the ASN to conduct the integration review.

# Integration Review of ASN-0036

## REVISE

### Issue 1: Registry status for OrdAddHom, OrdAddS8a, OrdShiftHom lists "introduced" instead of dependencies
**ASN-0036, Properties Introduced table**: OrdAddHom, OrdAddS8a, and OrdShiftHom all have status `introduced`

**Problem**: The section headers correctly label these as LEMMA, LEMMA, and COROLLARY respectively — each with a complete proof deriving from prior definitions and ASN-0034 foundations. But the registry marks all three as "introduced," which is the convention used for definitions (Σ.C, ord(v), vpos(S,o), w\_ord). The rest of the table consistently lists derivation sources for proved results: S1 says "from S0", S4 says "from GlobalUniqueness, T3 (ASN-0034)", S8 says "theorem from S8-fin, S2, S8a, S8-depth, T1, T3, T5, T10, TA5 (ASN-0034)". The three new proved results break this convention.

**Required**: Update registry statuses to list dependencies:
- OrdAddHom: `lemma from ord, w_ord, TumblerAdd, TA0 (ASN-0034)`
- OrdAddS8a: `lemma from OrdAddHom, S8a, TumblerAdd (ASN-0034)`
- OrdShiftHom: `corollary from OrdAddHom, OrdAddS8a, OrdinalShift, OrdinalDisplacement (ASN-0034)`

---

The proofs themselves are clean. Specifically verified:

- **ord, vpos, w\_ord**: Definitions are well-formed, inverse properties are pure sequence identities, S-membership and S8a claims are correctly conditioned.
- **OrdAddHom**: Component-by-component trace checks out at all three regions (prefix copy, action-point advance, tail copy). The index shift `actionPoint(w_ord) = k - 1` is correctly derived. Well-definedness of `ord(v) ⊕ w_ord` is explicitly verified (`k - 1 ≤ m - 1`). Both instances confirm boundary behavior — instance (b) correctly demonstrates S-membership failure with zero tail.
- **OrdAddS8a**: The iff characterization is tight — components before and at the action point are unconditionally positive (S8a on v, positivity of action-point component), leaving only tail components as the deciding factor. The equivalence with `ord(v ⊕ w) ∈ S` follows correctly from OrdAddHom.
- **OrdShiftHom**: The vacuous satisfaction argument is correct — `δ(n,m)` has action point m, so there are no tail components to check.
- **Placement**: After S8/S8-depth (which define V-positions) and before arrangement contiguity. Dependencies flow correctly.
- **Notation**: Consistent with existing conventions. `subspace(v) = v₁` matches S8a usage.

VERDICT: REVISE
