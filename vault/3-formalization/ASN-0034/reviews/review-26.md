# Cone Review — ASN-0034/D1 (cycle 4)

*2026-04-13 21:43*

Looking at this ASN as a system, reading every definition against every use, checking each precondition chain end-to-end.

I note that several previous findings appear to have been addressed in this revision (TumblerSub now has postconditions, T-membership preconditions, the zpd case split, and the Divergence exhaustiveness argument cites T3). I'm looking only for what remains uncaught.

---

### TumblerSub precondition equates T1 ordering with zpd component ordering without establishing the implication
**Foundation**: (internal — foundation ASN)
**ASN**: TumblerSub formal contract: "*Preconditions:* a ∈ T, w ∈ T, a ≥ w (when a ≠ w: if zpd(a, w) is defined (ZPD), aₖ ≥ wₖ at k = zpd(a, w); if zpd(a, w) is undefined, the condition holds vacuously)"; TumblerSub body proof: "rₖ = aₖ − wₖ ∈ ℕ since the precondition `a ≥ w` ensures `aₖ ≥ wₖ`"
**Issue**: The formal contract presents `a ≥ w` (T1 total order) and the parenthetical zpd-based condition as a single precondition — the parenthetical reads as an elaboration of what `a ≥ w` means at the component level. But this elaboration is an implication (`a ≥ w` ⟹ `aₖ ≥ wₖ` at zpd) that is never argued. T1 ordering is determined at the Divergence point (using actual, unpadded components), while TumblerSub's constructive definition acts at the zpd point (using zero-padded components). The document itself distinguishes these concepts. The implication holds — in Divergence case (i) zpd coincides with divergence and T1 directly gives component ordering; in case (ii) the longer operand has a nonzero actual component against a zero pad — but neither case is argued. This gap propagates: the body proof of `a ⊖ w ∈ T` cites "the precondition `a ≥ w` ensures `aₖ ≥ wₖ`" at the step that establishes `rₖ ∈ ℕ`, grounding the T-membership postcondition on the unargued transfer. D1 then cites that postcondition ("its postcondition gives w = b ⊖ a ∈ T") to feed `w` into TumblerAdd. The chain is: D1 establishes `b ≥ a` (T1) → TumblerSub accepts it as precondition → TumblerSub's body proof transfers T1 ordering to component ordering at zpd (unargued) → postcondition `w ∈ T` follows → D1 cites postcondition. The unargued step sits in the middle of a load-bearing chain. A formalizer must either (a) prove the transfer as a lemma relating T1, Divergence, and zpd, or (b) treat the zpd component condition as an independent precondition that callers must discharge separately from T1 ordering — but the contract gives no guidance on which path to take.
**What needs resolving**: Either prove that `a ≥ w` in T1 implies `aₖ ≥ wₖ` at `k = zpd(a, w)` when zpd is defined (a short case argument by Divergence case suffices), making the parenthetical a cited consequence; or decouple the conditions so that callers know they must establish component ordering at zpd independently of T1 ordering. The current presentation — one condition wearing two faces — leaves both TumblerSub's body proof and its callers' precondition checks resting on an unstated lemma.

## Result

Cone converged after 5 cycles.

*Elapsed: 6411s*
