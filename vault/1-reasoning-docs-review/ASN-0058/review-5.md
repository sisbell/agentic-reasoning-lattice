# Review of ASN-0058

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Lattice structure of equivalent decompositions
**Why out of scope**: The open question asks whether equivalent decompositions form a lattice under refinement with the canonical decomposition as coarsest element. This is new algebraic territory — the ASN has done its job establishing the existence and uniqueness of the canonical decomposition; the lattice question is a natural follow-up but requires its own treatment.

### Topic 2: Depth relationship between V-starts and I-starts
**Why out of scope**: The ASN correctly identifies that M0 may entail constraints on `#v` vs `#a` within a single block. The algebra as stated works regardless of the depth relationship (the integer offset `k` is interpreted independently at each depth), so this is a future refinement, not a gap.

### Topic 3: I-space discontinuity structure at canonical boundaries
**Why out of scope**: Whether non-mergeable V-adjacent boundaries must be forward gaps or can be arbitrary jumps depends on system-level arrangement invariants that constrain which arrangements are valid — territory for an operations or arrangement-invariants ASN.

---

**Detailed notes on the verification:**

The M12 (CanonicalUniqueness) proof is the centerpiece and it is watertight. The strategy — characterizing maximally merged decompositions as exactly the set of maximal runs of `f = M(d)`, then showing maximal runs are uniquely determined by `f` — is clean and complete. The left-extension condition (condition 2) correctly avoids TumblerSub by searching forward (`v' + 1 = v`) rather than backward, with the boundary case `v_m = 1` handled explicitly. The contiguity argument (fixed-depth tumblers between `v₁` and `v₁ + k` must be of the form `v₁ + j`) follows from T1's lexicographic order at uniform depth. Both directions of the biconditional (maximally merged ⟹ maximal runs, maximal runs ⟹ maximally merged) are proved with all cases covered.

M-aux's derivation via TA-assoc is correct: `w_c ⊕ w_j = w_{c+j}` because both displacements share their action point, and the TumblerAdd at the shared action point is ordinary integer addition.

M5's partition proof, M7's merge verification, and M9/M10's duality all follow cleanly from M-aux and the mapping block definition. M16's cross-origin impossibility proof is brief but complete: TA5(c) preserves the document prefix, so `origin(a₁ + n₁) = origin(a₁)`, and the contrapositive gives the result.

The worked example correctly verifies B1–B3, the merge/no-merge conditions, and canonicality.

VERDICT: CONVERGED
