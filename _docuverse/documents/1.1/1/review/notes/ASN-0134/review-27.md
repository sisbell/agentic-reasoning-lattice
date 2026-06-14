# Review of ASN-0134

I read this as a manuscript on a consistency model, and it is an unusually careful one. The conflict core (H0→H2), the literal-vs-operative reading of ASN-0128's I1a in §4 instance (i), the access-count discriminator that separates `age` (single-index) from `stale` (N+1), and the honest two-level "step confluence vs operation non-confluence" framing all hold up under scrutiny. The boundary cases a review of this kind demands — first-emission (`φ=0`), `m=0`/`m=1` degenerate batches, the cross-home/cross-subspace and *nesting*-home pairs in H1 — are each addressed rather than waved past. I found one genuine precision lapse and one cosmetic one.

## REVISE

### Issue 1: §8's trace is misattributed as a converse-failure witness for the first implication
**ASN-0134, §8 (V2)**: "A short witness exhibits that converse-failure as concretely as §8's trace exhibits the *first* implication's: take the *short-circuit* combiner `g(v₁, v₂) = (v₁ ≠ ∅) ∨ (v₂ = ∅)` ..."

**Problem**: The V2 chain is `[all reads at one index] ⟹ [no Q-affecting step] ⟹ [sound]`. The short-circuit combiner correctly witnesses the *second* implication's converse-failure (`sound ⇏ no Q-affecting step`). The sentence asserts, in parallel, that §8's trace witnesses the *first* implication's converse-failure — i.e. `[no Q-affecting step between the reads] ∧ ¬[all reads at one index]`. But §8's trace contains the T₂-nullify, which the trace's own conclusion identifies as "the lone **`Q`-affecting** step." So the full trace does **not** satisfy `[no Q-affecting step]`, the antecedent of the converse. It therefore cannot be a witness for `[no Q-affecting] ∧ ¬[one index]`. The trace as written demonstrates something different (and correct): that a `Q`-affecting step between drifting reads *causes* unsoundness, while a non-`Q`-affecting step is harmless. That is the second implication's necessity plus the *gap* between the two conditions — not the first implication's converse-failure.

**Required**: Either (a) reword so the trace is said to *illustrate the gap* between `[one index]` and `[no Q-affecting]` — its non-`Q`-affecting K₁-emit being the step `[one index]` excludes but `[no Q-affecting]` tolerates — rather than to "exhibit the first implication's converse-failure"; or (b) supply the clean witness: the *same trace with the T₂-nullify removed* (only the K₁-emit falling between the two reads). That trace has `[no Q-affecting step]` holding, reads at two distinct indices, and — by the banking argument — a sound verdict, so it genuinely witnesses `[no Q-affecting] ∧ ¬[one index] ∧ sound`.

### Issue 2: claim labels are non-monotonic in presentation order
**ASN-0134, §8 and §5–§6**: V1 (VerdictRetrospective) is introduced *after* V2 (VerdictReaderSnapshot); W4 (RunContiguityCritical) is introduced in §6, *after* W5/W6 in §5.

**Problem**: Consistently applied (the summary bullets and the Claims table also read "V0, V2, V1"), so it is not an internal inconsistency, but for a note whose claims are referenced by label it makes navigation mildly counterintuitive — a reader scanning for V1 finds it past V2.

**Required**: Either renumber to match presentation order (V1↔V2; W4 ahead of W5), or, if the topical grouping is deliberate (W4 belongs with the run discussion, V1 as a durability coda), add a one-line forward pointer at first mention. Lowest priority; decline if the grouping is intentional.

## OUT_OF_SCOPE

No additional items. The boundaries the note draws are clean and each is named explicitly: document-registration races are scoped out to the assumed document-address-freshness precondition of the excluded entity-allocation layer (§4, M1(c)); the concurrency-control *mechanisms* for clauses 2/7/8, multi-step batch read-atomicity, verdict durability, and cross-server composition are all deferred to the Open Questions rather than half-specified here. The note stays at the contract level (MIC clauses are implementation-independent obligations, not mechanics), so it has not drifted into implementation territory.

VERDICT: REVISE
