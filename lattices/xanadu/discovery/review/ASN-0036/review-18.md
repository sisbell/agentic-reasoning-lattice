# Integration Review of ASN-0036

## REVISE

(none)

The integrated `ValidInsertionPosition` property is well-constructed:

- **Definition correctness.** The two cases (non-empty and empty subspace) are complete and mutually exclusive. The j=0 case is correctly separated from j≥1 to respect OrdinalShift's n≥1 precondition. The m≥2 lower bound is justified by the shift failure at m=1 (demonstrated via TumblerAdd).
- **Structural verifications.** Distinctness (via T3 on pairwise-distinct last components), depth preservation (via OrdinalShift result-length identity), subspace identity (action point m≥2 ensures component 1 is copied), and S8a consistency (all components strictly positive for S≥1) are each shown correctly with explicit ASN-0034 references.
- **Count.** N+1 valid positions in the non-empty case: N existing positions v₀ through v_{N-1} plus the append position shift(min, N). Verified by the explicit last-component enumeration 1, 2, ..., N+1.
- **Placement.** After D-SEQ (which it depends on) and before S9 (which does not reference it). Dependencies on D-CTG, D-MIN, S8-depth, S8-fin, OrdinalShift, TumblerAdd, T3, and TA5 are all satisfied by prior material.
- **Registry.** Label, statement summary, and status ("introduced") are correct for a DEF-type property.
- **Examples.** The non-empty (N=3, four valid positions) and empty (m=2, position [1,1]) examples are consistent with the definition and correctly instantiated.
- **Notation.** V_S(d), shift(·,·), min(V_S(d)), δ(j,m), and bracket notation all match the surrounding document and ASN-0034 conventions.

VERDICT: CONVERGED
