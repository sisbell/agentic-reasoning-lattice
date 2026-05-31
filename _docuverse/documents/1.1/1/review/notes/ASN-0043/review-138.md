# Review of ASN-0043

I checked the proofs (PrefixSpanCoverage both directions, CPP, FSP/FSE, L1c chains, the six-step worked example arithmetic, L8 discrimination/coverage-equality) and they hold up. The substantive content is sound. Under the `review-mode.anti-bloat` lens, two residual accretions remain.

## REVISE

### Issue 1: L11a closes with an essay sentence that does not advance the claim
**ASN-0043, L11a — LinkUniqueness (final sentence)**: "L11a is the cross-event strengthening of the within-state single-valuedness already given by the partial-function typing `Σ.L : T ⇀ Link`."
**Problem**: L11a's content (distinct allocation events → distinct addresses, via GlobalUniqueness) is fully stated and derived in the preceding two sentences. This trailing sentence compares L11a to an unrelated typing fact rather than establishing anything — it is "essay content in a structural slot," the pattern the anti-bloat classifier targets. A reader following the proof must skip it.
**Required**: Delete the sentence. The GlobalUniqueness instantiation already stands on its own.

### Issue 2: The `.type` accessor guard contemplates a case L3 excludes
**ASN-0043, Convention — StandardTriple (Named accessor)**: "Conditional on `|Σ.L(a)| ≥ 3`, we introduce the abbreviation `Σ.L(a).type ≡ Σ.L(a).e₃` as a synonym for the indexed accessor of slot 3."
**Problem**: L3 guarantees `|Σ.L(a)| ≥ 3` for *every* `a ∈ dom(Σ.L)` in a conforming store, and L3 explicitly places sub-arity links "outside this ASN's conforming link store." So within this ASN's universe the conditional is always satisfied; the guard defensively contemplates the non-conforming sub-arity case the conformance carrier already excludes. This is the "imagines a case the precondition already excludes" pattern.
**Required**: Drop the conditional and define `Σ.L(a).type ≡ Σ.L(a).e₃` directly, noting (if needed) that well-definedness follows from L3. The slot-3 well-definedness is L3's job, not a guard on the abbreviation.

## OUT_OF_SCOPE

None — the ASN keeps to state (`Σ.L`), invariants (L0–L14), and definitions, deferring operations (MAKELINK, resolution, V-space effects) as marked.

VERDICT: REVISE
