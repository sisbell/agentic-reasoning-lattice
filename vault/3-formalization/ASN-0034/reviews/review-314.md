# Cone Review — ASN-0034/D2 (cycle 1)

*2026-04-18 18:22*

### D2 Step 2 uses `min(#a, #b)`, breaking the no-primitive-minimum convention observed everywhere else
**Foundation**: Divergence definition and its Depends entry explicitly state the shared-position bound as the conjunction `k ≤ #a ∧ k ≤ #b` "in place of any primitive binary-minimum on ℕ", and case (ii)'s values are enumerated as sub-cases (ii-a) `#a + 1` and (ii-b) `#b + 1` via NAT-order's trichotomy at `(#a, #b)`. D0 and D1 both rule out case (ii) by explicitly handling sub-cases (ii-a) and (ii-b).
**ASN**: D2 Step 2 — "The hypothesis k ≤ #a combined with #a ≤ #b yields k ≤ min(#a, #b), which rules out Divergence case (ii) — which would require k = min(#a, #b) + 1 > #a — and places us in case (i)".
**Issue**: `min(#a, #b)` is the exact operator the ASN elsewhere forbids. Divergence case (ii) never produces `min(#a, #b) + 1`; it produces `#a + 1` under (ii-a) or `#b + 1` under (ii-b). The appeal here also skips the NAT-order trichotomy at `(#a, #b)` and the NAT-addcompat strict successor step that D0/D1 invoke to refute each sub-case.
**What needs resolving**: Rewrite Step 2's Divergence-case-(ii) elimination to address sub-cases (ii-a) and (ii-b) explicitly (as D0 and D1 do), and update Depends to cite NAT-order (trichotomy at `(#a, #b)`) and NAT-addcompat (strict successor) for that elimination.

---

### D2 Depends conflates Divergence (definition) with D0 (DisplacementWellDefined)
**Foundation**: Divergence and D0 are two distinct properties with distinct formal contracts. Other Depends entries in this ASN (D0, D1) cite them as separate items.
**ASN**: D2 Depends — "D0 (Divergence/DisplacementWellDefined) — referenced in the closing remarks ('D0 ensures the displacement is well-defined') and implicit in the Step 2 reasoning that `b ⊖ a` is well-formed under `divergence(a, b) ≤ #a`."
**Issue**: The single entry names two properties under one label and asserts D0 is "implicit" where the actual load-bearing work in Step 2 is done by direct citations to Divergence, T1, ZPD, TumblerSub, and NAT-sub. If D0 is genuinely invoked, it should be named as a separate entry (not parenthesised alongside Divergence); if it is only referenced in closing remarks, it should not appear in Depends at all.
**What needs resolving**: Decide whether D0 is a Depends or only a thematic reference, and list Divergence and D0 as separate entries if both are consumed.

---

### D2 Preconditions under-constrain `w` vis-à-vis the `a ⊕ w = b` hypothesis
**Foundation**: TA-LC preconditions require `Pos(x), Pos(y), actionPoint(x) ≤ #a, actionPoint(y) ≤ #a, a ⊕ x = a ⊕ y`. D1 supplies these for the `b ⊖ a` branch. For the `w` branch, D2 relies on the caller-supplied hypotheses.
**ASN**: D2 Preconditions list `w ∈ T, Pos(w), actionPoint(w) ≤ #a, a ⊕ w = b`. The proof's Step 2 asserts "The addition a ⊕ w is therefore well-defined and equals b by assumption."
**Issue**: The length of `w` is not pinned by the preconditions, but Step 3's cancellation yields `w = b ⊖ a` whose length is `L` from TumblerSub's dispatch (here `#b` since `#a ≤ #b`). The postcondition `w = b ⊖ a` therefore implicitly forces `#w = #b`, but nothing in D2's preconditions ensures this — it is a consequence of `a ⊕ w = b` via TumblerAdd's result-length identity (`#w = #(a ⊕ w) = #b`). This derivation is not made explicit, and TumblerAdd's result-length identity is not cited in Depends.
**What needs resolving**: Either add the derivation `#w = #b` (citing TumblerAdd's result-length identity in Depends) as part of Step 2, or note that `#w` is pinned transitively through TA-LC's length argument — whichever path, make the length-routing explicit so a reviewer can verify the `w = b ⊖ a` conclusion does not rest on an unstated length premise.
