# Review of ASN-0071

I checked the PC derivation (componentwise fact + totality + prefix agreement), the PC-RANGE biconditional at position `#u` for both depth regimes, the F-CONTENT set algebra, the F-FIN three-step bound, and the worked scenarios (single-address, multi-address, cross-depth). The mathematics is sound: the depth guard `#v ≥ #u` is correctly load-bearing, the T1/T0/well-ordering arguments are complete, and boundary cases (empty query, `#u > m_C` resolving empty, empty-arrangement source via F-FILT) are handled by precondition or construction. My findings are confined to the accretion this note's `review-mode.anti-bloat` classifier targets.

## REVISE

### Issue 1: PC-RANGE claims-table entry re-derives the lemma instead of citing it
**ASN-0071, Claims Introduced, PC-RANGE row**: "...The depth guard `#v ≥ #u` is load-bearing: positions with `#v < #u` (which arise whenever `#u > m_C`) are excluded from both sides by PC totality, so a vspec anchored deeper than the source arrangement resolves empty"
**Problem**: The body section *Which positions resolve — cross-depth capture in general* already proves exactly this — the depth split, the load-bearing guard, and the `#u > m_C ⟹ ∅` boundary. The table row restates the rationale a second time rather than stating the claim and naming its basis. This is the claims-table verbosity that compounds across cycles.
**Required**: Reduce the row to the set-equality statement plus a basis pointer (PC + T1 at `#u`; PC totality for the depth guard). Move the "load-bearing"/"resolves empty" rationale out of the table — it lives in the body already.

### Issue 2: Nelson LM 4/38 citation deployed twice for the same point
**ASN-0071, intro** ("*A digit of 'one' may be used to designate all of a given version...*") and **Resolution, three-regimes paragraph** ("the coarse-coordinate reach Nelson's address convention names (LM 4/38)")
**Problem**: The same quote anchors the same coarse-coordinate-reach observation in two places; the three-regimes paragraph re-invokes the intro's framing rather than advancing it. The `#u < m_C` regime it names is then a third time demonstrated in the cross-depth worked scenario.
**Required**: Cite LM 4/38 once (the intro foreshadow or the regime consequence, not both). The three-regimes paragraph can state the consequence without re-quoting; the worked scenario is the concrete demonstration and should carry it.

## OUT_OF_SCOPE

### Topic 1: vspec vs ASN-0058 ContentReference relationship
The vspec deliberately relaxes ASN-0058's ContentReference (drops `V_{u₁}(d_s) ≠ ∅` and the `#u = m` anchor-equals-arrangement-depth constraint) to admit cross-depth queries and F-FILT semantics. PC is correctly labeled "the relaxed analogue of C0a." The generalization is justified by the cross-depth requirement — reusing ContentReference would forbid PC-RANGE's whole point. Not a reinvention to flag, but the explicit statement of *which* ContentReference conditions are dropped and why is a clarification that could be sharpened rather than a defect.

### Topic 2: Relationship of current-containment result to provenance `R`
Correctly deferred to Open Questions; belongs in a future ASN connecting `find` to the historical `R` relation.

VERDICT: REVISE
