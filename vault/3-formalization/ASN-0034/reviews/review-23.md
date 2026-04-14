# Cone Review — ASN-0034/D1 (cycle 1)

*2026-04-13 20:33*

### TumblerSub missing T-membership postcondition breaks precondition chain to D1
**Foundation**: (internal — foundation ASN)
**ASN**: TumblerSub formal contract vs. D1 proof
**Issue**: TumblerAdd's formal contract requires `w ∈ T` as a precondition. D1 sets `w = b ⊖ a` and feeds it to TumblerAdd. The D1 proof verifies `w > 0` and `actionPoint(w) ≤ #a` but never establishes `w ∈ T` — because TumblerSub's formal contract has no postconditions section at all. Compare TumblerAdd, which explicitly guarantees `a ⊕ w ∈ T` and `#(a ⊕ w) = #w` as postconditions. TumblerSub states `#(a ⊖ w) = max(#a, #w)` inside its definition clause and never states `a ⊖ w ∈ T` anywhere. The argument is straightforward (all result components are in ℕ, length ≥ 1), but it is neither made nor contracted, leaving an unlinked step in the D1 precondition chain.
**What needs resolving**: TumblerSub needs an explicit postconditions clause guaranteeing at minimum `a ⊖ w ∈ T` and `#(a ⊖ w) = max(#a, #w)`, parallel to TumblerAdd's postconditions. D1's proof should then cite the postcondition when it feeds `w = b ⊖ a` to TumblerAdd.

---

### D1 proof equates zpd with Divergence without bridging argument
**Foundation**: (internal — foundation ASN)
**ASN**: D1 proof, paragraph beginning "Define w = b ⊖ a. By TumblerSub, the divergence between b and a (minuend and subtrahend) occurs at position k"
**Issue**: The variable `k` is defined as `divergence(a, b)` — the formal Divergence. The proof then says TumblerSub's action occurs "at position k" as though this is obvious. But TumblerSub's own text warns: "This concept [zpd] is distinct from the formal Divergence: when one operand is a proper prefix of the other, divergence reports min(#a, #w) + 1 at the prefix boundary (case (ii)), whereas zpd scans past it." The proof needs to argue that under D1's preconditions (divergence case (i), with `k ≤ #a ≤ #b`), both notions coincide: positions `i < k` are within both operands' actual lengths so no zero-padding occurs, and at position `k` both operands have actual (non-padded) values that disagree, making `zpd(b, a) = k = divergence(a, b)`. This argument is short but it is absent — the proof simply asserts identity between two concepts the document itself distinguishes.
**What needs resolving**: The D1 proof must explicitly establish `zpd(b, a) = divergence(a, b)` under D1's preconditions, rather than conflating the terms. Even a one-sentence argument suffices, but the step must be present.

---

### TumblerSub precondition elaboration ill-formed when zpd does not exist
**Foundation**: (internal — foundation ASN)
**ASN**: TumblerSub formal contract: "*Preconditions:* a ≥ w (when a ≠ w, at the zero-padded divergence k = zpd(a, w), aₖ ≥ wₖ)"
**Issue**: The parenthetical claims to restate `a ≥ w` in terms of zpd, but it fails for tumblers that are T3-distinct yet zero-pad-equivalent. Example: `a = [1, 2, 0]`, `w = [1, 2]`. By T3 these are distinct (`a ≠ w`). By T1, `a > w` (proper prefix), so `a ≥ w` holds and the operation is defined (producing `[0, 0, 0]`). But zero-padding `w` to `[1, 2, 0]` makes the padded sequences identical — zpd does not exist, so `k = zpd(a, w)` is undefined. The elaboration references a value that has no referent, making the condition neither true nor false but ill-formed. The constructive definition handles this case correctly (the "no divergence" branch), but the formal contract's precondition cannot express it.
**What needs resolving**: The precondition elaboration must account for the case where `a ≠ w` but `zpd(a, w)` does not exist. Either restructure as a case split (zpd exists: `aₖ ≥ wₖ`; zpd does not exist: condition holds vacuously) or redefine the precondition without routing through zpd.
