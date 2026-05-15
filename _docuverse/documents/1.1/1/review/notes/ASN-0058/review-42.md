# Review of ASN-0058

The ASN constructs an algebra of mapping blocks with careful attention to edge cases. The proofs handle the boundary structure rigorously: n = 1 vs n ≥ 2 in M0/M1 distinctness arguments, k = 0 vs k ≥ 1 in OrdinalShiftBase-dependent reasoning, the empty arrangement case in M2, and the proper case split in C0a between #t < m and #t ≥ m. M-int serves as the structural keystone consumed by M2's V-extent translation, M7-cov's non-overlap argument, M12a's run-disjointness proof, and C2's measure-theoretic step.

The split-merge duality (M9, M10), canonical uniqueness via maximal runs (M12, M12a, M12b), and cross-origin merge impossibility (M16, M16a) form a coherent body of results. M16a's proof correctly traces the document-prefix preservation through TumblerAdd's action-point structure (#a ≥ 8 from S7b + S7c + T4a ensures the prefix lies strictly below the action point).

The two worked examples are well-chosen: the first verifies M7's necessary-and-sufficient condition with concrete tumbler arithmetic showing one mergeable and one non-mergeable pair; the second verifies C1, C2 against a content reference and correctly invokes M16's contrapositive to explain why two V-adjacent blocks with different origins cannot merge.

The C1a extension argument (M11/M12 to restrictions) handles the S8-depth substitution uniformly. M-int isn't explicitly named in the substitution discussion, but the "rest of the argument is unchanged" clause covers it correctly, since M-int's only ASN-0036 dependencies are S8a (#v ≥ 2, discharged by common-depth m ≥ 2) and S8-depth (the named substituendum).

Foundation references are consistently to ASN-0034, ASN-0036, and ASN-0053 — all on the verified foundation list. No invented notation reinvents what foundations already provide.

## REVISE

(None)

## OUT_OF_SCOPE

The Open Questions section appropriately defers:
- Classification of I-space discontinuity types at canonical decomposition boundaries
- Lattice structure of equivalent decompositions under refinement
- Relationship between V-extent and block count in canonical decompositions  
- Depth constraints between V-starts and I-starts within blocks
- Source-order preservation in multi-source content reference resolution

These belong in future ASNs treating arrangement transformations, content reference placement semantics, and structural metrics.

VERDICT: CONVERGED
