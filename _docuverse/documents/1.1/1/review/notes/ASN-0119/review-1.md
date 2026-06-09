# Review of ASN-0119

## REVISE

### Issue 1: No concrete worked example
**ASN-0119, throughout**: The note derives P0–P9 entirely in the abstract and never verifies them against a specific scenario.
**Problem**: The review standard requires the key postconditions be checked against at least one concrete case (e.g., a pivot of "ABCDE" with named cuts `c₀,c₁,c₂`, exhibiting the resulting `M'(d)` and confirming P1, P2, P3 numerically; and a four-cut swap confirming the middle's `w_β − w_α` displacement). Without one, the tiling arguments and the middle-displacement sign claim are asserted but never exercised.
**Required**: Add a worked pivot and a worked swap with explicit ordinals, showing the destination intervals tile exactly and that a sample link footprint relocates through `π`.

### Issue 2: Atomicity claims P8a/P8b are asserted, not derived
**ASN-0119, "Atomicity":** "M'(d) under T = M(d) under (T₁ ; T₂)" and "∃ observable Σ_mid with M_mid(d) ≠ M(d) ∧ M_mid(d) ≠ M'(d)."
**Problem**: "Two-move composite" is never defined — what operations compose to the same `π`? P8a is near-tautological (it presupposes the composite "achieves the same net permutation"), and P8b asserts the *existence* of a distinct observable intermediate with no construction. The whole interest of atomicity (Q6, Q19) is the existence of an observable divergent state, and that existence is exactly what is left unproven.
**Required**: Exhibit a concrete decomposition of a specific `π` into two realizable moves and compute its intermediate arrangement, showing it differs from both endpoints; or restate P8b as an open question rather than a claim.

### Issue 3: Scope inconsistency — general subspace S vs. text-only/depth-2 foundations
**ASN-0119, "The two streams" / "Cuts and regions"**: "We confine the operation to a single subspace S … the text subspace s_C is the case of interest," then reasons generically over "subspace S" while grounding cut-naming in "the active text positions are contiguous and densely indexed (D-SEQ)."
**Problem**: D-CTG/D-SEQ/D-MIN hold only for the text subspace `V_1`; the closed-form permutations cited (R-PPERM, R-SPERM) are established only for `S = 1`, depth 2. The note cannot simultaneously claim a general-`S` operation and lean on text-only, depth-2 results. The link subspace does not satisfy the contiguity the cut-naming argument requires.
**Required**: Either fix the scope to text subspace at depth 2 explicitly and drop the general-`S` framing, or supply contiguity/closed-form justification valid for arbitrary `S`.

### Issue 4: Restatement of and label collision with the existing REARRANGE specification
**ASN-0119, "The transposition as a permutation" and Claims table**: introduces `R-EXT`, `R-P1`, `R-P2`, `R-S1/R-S2/R-S3`, and `π` — the exact labels and equations already defined as PivotPostcondition/SwapPostcondition/R-PPERM/R-SPERM in the prior bundle-projection-displacement ASN it then cites for the closed form.
**Problem**: The operation, its frame, and its permutation are reintroduced verbatim rather than imported, and P1 (`M'(d)(π(v)) = M(d)(v)`, `ran` invariance) and P2 (bijectivity) duplicate the already-proved R-RI/R-PIV/R-SWP. Reusing another ASN's labels for the same content breaks self-containment and creates two authorities for one operation.
**Required**: Cite the existing REARRANGE operation (REARRANGE_K, its postconditions, R-PPERM/R-SPERM, R-RI) as the definition, and let this note introduce *only* the genuinely new system guarantees built on top (link survival P6/P7a/P7b, isolation P9, discoverability P5, atomicity). Rename or remove the colliding `R-*` labels.

### Issue 5: S2 (functionality) and S3 (referential integrity) preservation not discharged as named invariants
**ASN-0119, "What is preserved"**: P1 gives `ran(M'(d)) = ran(M(d))`, and the tiling argument gives disjoint destinations.
**Problem**: The note never states, as obligations, that `M'(d)` remains single-valued (S2) and that `ran(M'(d)) ⊆ dom(C)` (S3). Both follow from the tiling/P1, but a rearrangement spec that omits them as explicit preserved invariants leaves the hardest-to-maintain conjuncts implicit.
**Required**: Add explicit S2 and S3 preservation, each one line, citing the disjoint tiling (S2) and P1 with `ran(M(d)) ⊆ dom(C)` (S3).

## OUT_OF_SCOPE

### Topic 1: Transclusion-shared cuts (Open Question 1)
**Why out of scope**: A cut that is interior in a transcluding document is a multi-document coordination question; this note correctly isolates a single document (P9) and defers the shared-boundary semantics.

### Topic 2: Concurrent unserialized rearrangements (Open Question 2)
**Why out of scope**: Commutativity of independent rearrangements is a concurrency-control concern beyond a single-operation spec.

### Topic 3: Recoverability of the prior arrangement / version history (Open Question 4)
**Why out of scope**: REARRANGE records only the new mapping; recovering prior order is version-graph territory (CREATENEWVERSION), not this operation.

VERDICT: REVISE
