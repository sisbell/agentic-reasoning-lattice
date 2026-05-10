# Cone Review — ASN-0034/D2 (cycle 7)

*2026-04-18 19:29*

Looking at this ASN as a system, I've read through D0, D1, D2, TumblerSub, ZPD, Divergence, and the foundation definitions, checking for gaps between properties and within proof chains that aren't already captured in Previous Findings.

### TumblerSub precondition-consequence sub-case (ii-a): prose never derives `k > #w` that it silently assumes

**Foundation**: ZPD's Definition names `zpd(a, w)` as the *least* `k` with `âₖ ≠ ŵₖ`. TumblerSub's Depends entry for ZPD explicitly enumerates site (ii-b) as "*minimality-driven identification of `k > #w`* — that the named `k = zpd(a, w)` actually falls at one of these `i > #w` positions, rather than somewhere within the prefix range `1 ≤ i ≤ #w` where the sequences agree, requires ZPD's minimality clause combined with the same prefix agreement".

**ASN**: TumblerSub precondition-consequence, sub-case (ii-a) of Divergence case (ii) for pair `(w, a)`: "We are therefore in sub-case (ii-a): `w` is a proper prefix of `a`, so `#w < #a` and `wᵢ = aᵢ` for all `1 ≤ i ≤ #w`. The padded extension sets `wₖ = 0` for `k > #w`, with `0 ∈ ℕ` supplied by NAT-zero so that the equality is a well-formed ℕ-valued comparison. Since zpd is defined, the longer operand `a` has some nonzero component beyond `#w`; at `k = zpd(a, w)`, `aₖ ≠ 0 = wₖ`."

**Issue**: The prose jumps from "some nonzero component beyond `#w`" (an existential) to "at `k = zpd(a, w)`, `aₖ ≠ 0 = wₖ`" (which presupposes the *named* `k` lies at position `> #w`, since only then is `wₖ = 0` via the prefix zero-padding). The connecting step — that ZPD's minimality forces `k > #w` because the prefix agreement at positions `1 ≤ i ≤ #w` means no disagreement can occur there — is recorded in the Depends but never stated in the proof prose. The Depends and prose are therefore misaligned: a reader working through the proof sees an unexplained leap, while a reader working through Depends sees a minimality step that has no textual home.

**What needs resolving**: Either extend the prose to derive `k > #w` from ZPD's minimality combined with sub-case (ii-a)'s prefix-agreement hypothesis, or adjust the sub-case-(ii-a) narrative so the `k > #w` fact is stated and justified at the point where `wₖ = 0` is invoked.

---

### D2 postcondition `w = b ⊖ a` requires `#(b ⊖ a) = #b`, but D2 never dispatches TumblerSub's length at `(#b, #a)`

**Foundation**: TumblerSub's Postconditions state `#(a ⊖ w) = L` with `L` named by NAT-order's trichotomy on the operand-length pair. D1 explicitly performs this dispatch on `(#b, #a)` under `#a ≤ #b` to conclude `#w = #b`: "The precondition `#a ≤ #b` forecloses sub-case (β): NAT-order's exactly-one clause at the length pair `(#a, #b)` … rules out `#b < #a` … Sub-case (α) and sub-case (γ) both give `L = #b`, so `#w = #b`."

**ASN**: D2 Step 2 (`b ⊖ a` branch) derives `Pos(b ⊖ a)` and `actionPoint(b ⊖ a) = k ≤ #a`, but never establishes `#(b ⊖ a)`. D2's TumblerSub Depends entry enumerates three sites (carrier membership, component formulas, conditional postcondition for action point) and does not mention the length-pair dispatch, unlike D1's parallel Depends which enumerates it explicitly.

**Issue**: D2's conclusion `w = b ⊖ a` requires both sides to have equal length (via T3, inside TA-LC's proof). `#w = #b` is pinned via TumblerAdd's result-length identity (which D2 does record). But `#(b ⊖ a)` is never pinned: TumblerSub's dispatch at `(#b, #a)` under `#a ≤ #b` gives `L = #b`, matching `#w = #b`, so the equation goes through — but this dispatch is never cited in D2's Depends and never argued in the prose. A reviewer verifying that TA-LC's length-matching requirement is met at `y = b ⊖ a` has no Depends-backed route to `#(b ⊖ a) = #b`. The gap is structurally parallel to the length-pair-dispatch enumeration D0 and D1 both include explicitly.

**What needs resolving**: Either add the TumblerSub length-pair dispatch at `(#b, #a)` to D2's Step 2 and extend the TumblerSub Depends entry to enumerate it (matching D1's treatment), or argue explicitly that `#(b ⊖ a) = #b` follows transitively from TA-LC's internal length argument (`#x = #(a ⊕ x) = #(a ⊕ y) = #y`) and make that routing the Depends entry's justification.

## Result

Cone converged after 8 cycles.

*Elapsed: 4716s*
