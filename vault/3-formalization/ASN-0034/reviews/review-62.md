# Cone Review — ASN-0034/D0 (cycle 1)

*2026-04-16 00:59*

I'll read the full ASN content carefully, then check for cross-property consistency.

### actionPoint referenced in preconditions before definition
**Foundation**: TumblerAdd — defines `actionPoint` as `min{i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0}`
**ASN**: TA0 (WellDefinedAddition), formal contract: "Preconditions: a ∈ T, w ∈ T, Pos(w), actionPoint(w) ≤ #a"
**Issue**: TA0's preconditions reference `actionPoint(w)`, but `actionPoint` is defined constructively within TumblerAdd, which appears after TA0 in the document. The operation symbol `⊕` (used in "the result `a ⊕ w`") is likewise defined in TumblerAdd. TA0 cannot be stated — let alone proved — without TumblerAdd's definitions. The same structural problem affects TA2, which references `⊖` before TumblerSub defines it. Unlike the T1→T3 forward reference (which is explicitly flagged and involves an axiom whose content is paraphrased at each use), these forward references introduce a constructive definition and an operation symbol into preconditions and postconditions with no self-contained paraphrase.
**What needs resolving**: Either the defining constructions must precede the well-definedness theorems, or `actionPoint` and the operation symbols `⊕`/`⊖` must be established as standalone definitions before any theorem references them in its contract.

---

### Divergence section misattributes TA0's precondition and references absent properties
**Foundation**: TA0 (WellDefinedAddition), formal contract: "Preconditions: … actionPoint(w) ≤ #a"
**ASN**: Divergence definition, paragraph following the formal contract: "Since TA0 requires k ≤ min(#a, #b), the condition k ≥ divergence(a, b) in TA1-strict below is unsatisfiable for prefix-related operands. This is correct: when a is a proper prefix of b (or vice versa), Case 1 of the verification below shows that addition erases the divergence … TA1-strict makes no claim about prefix-related pairs — TA1 (weak) covers them, guaranteeing non-reversal."
**Issue**: Two problems. (a) TA0 requires `actionPoint(w) ≤ #a`, not `k ≤ min(#a, #b)`. The `min` bound requires combining TA0's precondition with the fact that `k ≤ #w` (the action point is an index within `w`) and the result-length identity `#(a ⊕ w) = #w` (identifying `#b = #w`). The text attributes the combined result to TA0 alone — a formalizer looking at TA0's contract will not find the stated precondition. (b) "TA1-strict below," "TA1 (weak)," and "Case 1 of the verification below" are referenced but do not appear in this ASN. The unsatisfiability argument depends on a property whose statement and scope are unknown.
**What needs resolving**: (a) The derivation must cite the additional premises (`k ≤ #w`, result-length identity) that combine with TA0 to yield the `min` bound, or the sentence must be rewritten to state the correct TA0 precondition. (b) TA1-strict and TA1 (weak) must either appear in this ASN or the Divergence section must not reference them; dangling forward references break the self-contained argument chain.

---

### Systematic absence of Depends declarations in formal contracts
**Foundation**: T1, TA0, and TumblerAdd — these three include Depends lines in their formal contracts
**ASN**: D0 (DisplacementWellDefined), TA2 (WellDefinedSubtraction), TumblerSub, PositiveTumbler, Divergence — all lack Depends despite having proofs that invoke other properties
**Issue**: The formal contracts are inconsistent about dependency tracking. Specific gaps: **D0** invokes TA2, TumblerSub (for the length postcondition `#(b ⊖ a) = max(#a, #b)`), Divergence, ZPD (for the `zpd = divergence` identification), T1 (for `a < b` entailing `b ≥ a`), T3 (for the length-inequality argument), and PositiveTumbler — but declares none. **TA2** appeals entirely to TumblerSub's construction ("By TumblerSub, subtraction zero-pads…") but has no Depends line. **TumblerSub** embeds partial dependency information in an ad hoc parenthetical ("by Divergence case analysis via T1, Divergence, ZPD") within its Preconditions section rather than a dedicated Depends line. **PositiveTumbler**'s postcondition proof invokes T1 cases (i) and (ii) to conclude `z < t`. **Divergence**'s exhaustiveness argument invokes T3 to derive the contradiction `a = b`. Without Depends lines, the dependency DAG cannot be reconstructed from formal contracts alone.
**What needs resolving**: Every formal contract whose proof or well-definedness argument invokes another property must declare it in a Depends line, following the pattern established by T1, TA0, and TumblerAdd. The format should name the dependency and state which postcondition is consumed, as TumblerAdd's contract does.

---

### TA2 drops TumblerSub's length postcondition, creating an invisible bypass
**Foundation**: TA2 (WellDefinedSubtraction), formal contract: "Postconditions: a ⊖ w ∈ T" — membership only, no length
**ASN**: D0 (DisplacementWellDefined), postconditions: "#(b ⊖ a) = max(#a, #b)" and "#a > #b → a ⊕ (b ⊖ a) ≠ b"
**Issue**: TA2 exports only membership (`a ⊖ w ∈ T`). TumblerSub additionally exports `#(a ⊖ w) = max(#a, #w)`. D0 needs the length to derive two of its own postconditions: `#(b ⊖ a) = max(#a, #b)` directly, and the `#a > #b` inequality via the chain `#(a ⊕ w) = #w = max(#a, #b) = #a > #b`, concluding `≠ b` by T3. Since TA2 doesn't forward the length, D0 must silently bypass TA2 and depend on TumblerSub directly — but D0 has no Depends line, so this bypass is invisible. By contrast, TA0 forwards both membership and length from TumblerAdd (`#(a ⊕ w) = #w`), so the analogous problem does not arise for addition. The asymmetry between the two summary theorems' postcondition sets is itself a contract gap: a consumer of subtraction who cites TA2 (the apparent "public interface") cannot derive the length of the result.
**What needs resolving**: Either TA2 must export TumblerSub's length postcondition (matching TA0's treatment of TumblerAdd), or the TA2/TumblerSub split must be reconsidered. Independently, D0 must declare its actual dependency (TumblerSub, not merely TA2) so the postcondition chain is traceable.
