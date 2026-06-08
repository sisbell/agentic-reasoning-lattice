# Review of ASN-0114

## REVISE

### Issue 1: Worked example misstates coverage as a finite address set

**ASN-0114, A worked instance**: "Hence `coverage(e₁) = {a₃, a₄, a₇, a₈}`." and "F1 demands `coverage(R) = {a₃, a₄, a₇, a₈}`."

**Problem**: `coverage` (ASN-0098) is defined over all of `T` as a union of half-open intervals, not over the emittable set `F`. The span `(a₃, δ(2, #a₃))` denotes `{t ∈ T : a₃ ≤ t < a₅}`, which contains far more than `{a₃, a₄}` — e.g. `[1,0,1,0,5,0,1,3,1] = a₃.1` satisfies `a₃ < a₃.1 < a₅`, so it lies in the coverage. Therefore `coverage(e₁) = [a₃, a₅) ∪ [a₇, a₉)`, not the four-element set written. The text earlier qualifies correctly ("within the emittable addresses, `{a₃, a₄}`", matching LP-Fin Corollary), but then drops the `∩ F` qualifier and asserts a literal set equality over `T` that is false. Since F1, F2, and F3 all bind coverage over `T`, the example as stated contradicts the contract it is meant to verify. (The disconnection witness `q = a₅` and the F2 conclusion survive — only the enumeration is wrong.)

**Required**: Either write `coverage(e₁) ∩ F = {a₃, a₄, a₇, a₈}` (and likewise for `R`), or state coverage in its true interval form `[a₃, a₅) ∪ [a₇, a₉)`, and adjust the F1/F2 checks to use that form.

### Issue 2: F5 applies a single-step invariant to a multi-step sequence without the closure

**ASN-0114, F5 derivation**: "Let `Σ →* Σ'` be any reachable transition sequence ... Link addresses persist and link values are fixed under every transition (L12), so `Σ'.L(a) = Σ.L(a)`."

**Problem**: L12 (ASN-0043) is stated for a *single* transition `Σ → Σ'`. F5 quantifies over the reflexive-transitive closure `Σ →* Σ'` and concludes `a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)` directly, skipping the inductive composition across the sequence. The single→multi step is exactly what foundation lemma LP13 (UnconditionalLinkPersistence, ASN-0098) — "for every reachable state sequence `Σ →* Σ'` and every `a ∈ dom(Σ.L)`: `a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)`" — already discharges, and ASN-0098 introduces a Closure schema (★) precisely because this transition is not free.

**Required**: Cite LP13 (or invoke the closure schema ★) for the multi-step persistence, or state the one-line induction over the sequence explicitly, rather than citing only the single-step L12.

## OUT_OF_SCOPE

### Topic 1: Resolution of the recorded endset against a particular document's arrangement
**Why out of scope**: The ASN itself correctly identifies (section "A boundary we must respect") that projecting the recorded end into a chosen document's live arrangement and filtering absent addresses is a separable concern (the resolution / project family, ASN-0098), not part of reading the recorded end. The Open Questions about shrinkage and per-document resolution are future territory, not defects here.

VERDICT: REVISE
