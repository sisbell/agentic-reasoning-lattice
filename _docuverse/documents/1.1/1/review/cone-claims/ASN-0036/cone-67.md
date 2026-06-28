**Dependency structure audit.** AX-1 → base case of S3. AX-2 → new/redirected case of S3. S0 → S1 → inherited case of S3. These are the four load-bearing lines; I trace each in turn.

**S0 → S1.** The proof is one step: take a ∈ dom(Σ.C), apply S0 to read off a ∈ dom(Σ'.C) as the first conjunct, done. Correct.

**AX-1 base case.** dom(Σ₀.M(d)) = ∅ makes the range of S3's quantifier empty. Vacuous satisfaction. Correct.

**AX-2 well-formedness.** The domain guard `v ∈ dom(Σ.M(d))` in the second disjunct is redundant in classical logic — `¬A ∨ (A ∧ B) = ¬A ∨ B` — but required under strict partial-function evaluation to prevent `Σ.M(d)(v)` from being reached outside its domain. The explanation is accurate.

**S3 inductive step.** For v ∈ dom(Σ'.M(d)) the proof splits on whether the mapping is inherited unchanged. The two cases are mutually exclusive and exhaustive by excluded middle. Inherited case: IH gives a ∈ dom(Σ.C), S1 lifts to dom(Σ'.C). New-or-redirected case: the condition exactly matches AX-2's range, which yields a ∈ dom(Σ'.C) directly. Both cases close. Correct.

**AX-2 formal contract.** The summary phrase "targets an address *already* in the post-state content store" could be read as requiring the address to be in the pre-state, but the body prose ("before, or within the same transition as") and the axiom statement (`Σ'.M(d)(v) ∈ dom(Σ'.C)`) are unambiguous. No gap.

**Frame coverage.** S3 ranges over dom(M(d)), never over dom(C), so orphaned content places no obligation on S3. S1 is unconditioned on whether an address is referenced, so unreferenced content is never reclaimed. Frame condition is correctly stated in the Formal Contract.

---

### Reviser drift marker in S3 post-proof paragraph
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: S3 (ReferentialIntegrity), post-proof paragraph — "The earlier reading, that S1 alone forces `a ∈ dom(Σ'.C)` for any mapping established by a transition, conflated these: it assumed precisely the new-reference half that AX-2, not S1, supplies."
**Issue**: "The earlier reading" refers to nothing in this document. No prior section of S3 takes that reading; the phrase is a marker of a past review cycle, not a proof step or a frame remark. This is reviser-drift pattern 2 (a paragraph looks like a prior finding's content relocated rather than removed) combined with pattern 3 (prose around an axiom explains why the axiom is needed rather than what it says). The substantive content — that S1 is silent on newly established references, and that AX-2 fills the gap — is already fully stated in the Formal Contract's Depends section for S1 and AX-2. The body paragraph repeats it with a drift marker attached.
**What needs resolving**: Remove the sentence containing "The earlier reading." The preceding sentences ("S1 preserves references that are already valid; it is silent on whether a transition may install a fresh mapping Σ'.M(d)(v) = a with a ∉ dom(Σ'.C). Nothing in the content-store invariants forbids an arrangement from naming an as-yet-unstored address; that prohibition lives on the write side of the protocol and is recorded as AX-2. S3 is thus the join of two independent facts…") are statements of what S1 does and does not do and may be retained or moved to a remark slot. The drift marker is only the final sentence.

---

The proof of S3 is sound and the axioms are correctly stated.

VERDICT: OBSERVE