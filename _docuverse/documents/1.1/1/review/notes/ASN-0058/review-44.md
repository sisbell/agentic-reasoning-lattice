# Review of ASN-0058

The ASN develops the mapping block algebra with appropriate rigor. Block decomposition (B1–B3, M2), canonical decomposition (M11, M12 via M12a/M12b), and content reference resolution (C0–C2) are well-proved with no proof-by-similarly or proof-by-checkmark shortcuts.

M-int (TumblerIntervalCharacterization) and M16a (OriginInvarianceUnderShift) function as load-bearing intermediate lemmas, each proved in full detail through explicit T1 case analysis and TumblerAdd prefix-copy reasoning. The M12 uniqueness proof carefully decomposes into M12a (run disjointness, with explicit handling of v_1 = v_2 and v_1 < v_2 cases via M-int) and M12b (no extension in maximally merged, with both right-extension and left-extension contrapositives proved).

Edge cases are handled appropriately: empty arrangement (∅ as unique decomposition), singleton blocks (M4 disallows splits but merges remain available), the depth-1 boundary (M-sub clause (a) sharpness note), k = 0 base case (OrdinalShiftBase convention threaded through M-aux). M7-cov rules out V-overlap via M-int rather than asserting it; M14's extension to general I-extent sharing is proved explicitly using TS5 monotonicity.

The cross-origin merge impossibility (M16) is correctly derived from M16a via the document-prefix preservation argument, with the structural decomposition #a ≥ 8 derived from S7b + S7c + T10a.4. The worked examples verify both the canonical decomposition mechanism (M11/M12) and the resolution machinery (C0–C2) against concrete configurations, including the cross-origin obstruction in the second example.

C1a's extension of M11/M12 to restricted partial functions is principled — it identifies the three load-bearing conditions (functionality, finite domain, common depth m ≥ 2) and shows each is supplied by S2, S8-fin, and (C0a + S8-depth + S8a) for f = M(d_s)|⟦σ⟧.

## REVISE

(no items)

VERDICT: CONVERGED
