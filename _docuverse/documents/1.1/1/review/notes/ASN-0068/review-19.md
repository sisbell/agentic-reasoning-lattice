# Review of ASN-0068

## REVISE

### Issue 1: Triplicated "m_a = m_b not required" with self-referential back-pointer
**ASN-0068, Example 4**: "CV-IN admits this input even though `m_a ≠ m_b` ... the constraint `m_a = m_b` is *not* required (the introductory text in this ASN flags this as a design commitment)."
**Problem**: The same design commitment is asserted three times — in the CV-IN region ("We do *not* require `m_a = m_b`"), in the *Self-comparison is admissible* note, and again in Example 4, the last of which adds a self-referential pointer back to "the introductory text in this ASN." This is forward/back-reference accretion: the example should *exercise* the admissibility, not re-justify it by pointing at the prose that already stated it.
**Required**: State the commitment once at CV-IN. Example 4 should simply demonstrate the depth-mismatch walk; drop the "(the introductory text in this ASN flags this as a design commitment)" clause.

### Issue 2: CV-PRED scope paragraph imagines an excluded case to justify itself
**ASN-0068, CV-PRED**: "The scope `v ∈ V_S(d)` is essential — the candidate-form computation `[S, 1, ..., 1, v_m − j]` ... depends on `v`'s D-SEQ★ structure, and a general depth-`m` positive-component tumbler in subspace `S` (with components freely chosen, e.g., `[S, 3, 7, 2, ...]`) would have a different predecessor expression."
**Problem**: The scope `v ∈ V_S(d)` is already declared in the definition's opening line. The added clause defends the scope by constructing a tumbler (`[S, 3, 7, 2, ...]`) that the scope already excludes — the "imagines a case the precondition already excludes" drift pattern. It explains *why the scope is needed* rather than advancing the predecessor definition.
**Required**: Delete the defensive sub-clause. The D-SEQ★ form is used in the Existence clause below where it does object-level work; the scope needs no separate apologia.

### Issue 3: Closure Properties section restates CV-RO and CV-DETERM
**ASN-0068, Closure Properties**: "Because it is read-only (CV-RO), it satisfies the frame conditions of every transition kind trivially — it modifies nothing. ... These two properties together ... make `compareversions` a *pure observation* of state."
**Problem**: This section derives nothing beyond CV-RO and CV-DETERM, which already carry their own derivations. "Satisfies the frame conditions trivially — it modifies nothing" is CV-RO restated; the "pure observation" paragraph is essay framing. Two paragraphs saying what two prior claims already established.
**Required**: Fold any genuinely new consequence (e.g., a named composability guarantee) into CV-RO/CV-DETERM, or cut the section. Do not restate established claims under a new heading.

### Issue 4: Redundant restatement of CV-IN empty-subspace handling in CV-EMPTY
**ASN-0068, CV-EMPTY justification**: "when the subspace is empty in `d_a` — a fresh fork ... so `V_S(d_a) = ∅` ... CV-IN forces `R_a = ⟨⟩` (since no `σ` could satisfy `start(σ) ∈ V_S(d_a) = ∅`) ..."
**Problem**: This re-derives, in full, the empty-subspace → `R_a = ⟨⟩` mechanics already spelled out twice in CV-IN (once per side). CV-EMPTY's actual content is "empty intersection ⟹ empty result," which the first paragraph establishes; the second paragraph is a use-case narrative duplicating CV-IN.
**Required**: Reduce the second paragraph to a one-line pointer: the empty input arises either by explicit `R_a = ⟨⟩` or by CV-IN's empty-subspace clause; in both cases the first paragraph applies. Do not re-derive the CV-IN admissibility logic here.

## OUT_OF_SCOPE

### Topic 1: Concurrent-modification invariants, replication agreement, version-history composition
**Why out of scope**: These are correctly parked in Open Questions and the Scope exclusions (BEBE/replication). The note does not assert claims about them, so no revision is owed.

Note on correctness: I checked the CV-MAX existence and uniqueness proofs (left/right walk termination, the `δ = 0` and `δ > 0` cases, the M-aux offset reductions), the action-point capture argument, and Examples 1–4 against the definitions; the mathematics is sound and the edge cases (empty restriction, self-comparison, differing depths, link subspace, width-1 atoms) are covered. The findings above are accretion, not logic errors.

VERDICT: REVISE
