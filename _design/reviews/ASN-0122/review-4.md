I read the digest against the note, the formal claims, and the verified Green evidence, hunting specifically for misreads of what's "forced," unsound approaches, ungrounded Green claims, missing load-bearing commitments, and altitude slips. The high-risk areas I checked hardest all hold up:

- **The "forced" tags are right.** Address-not-value identity (X1/X2), total frame (X12), locality (X5), binding soundness+completeness (R1/R2), content-subspace losslessness (X9), edit-transport (X6/X7/X-T) — each is correctly classified as forced, and R4/canonical-form is correctly classified as conventional.
- **The R3-vs-R4 distinction is handled precisely** — "deterministic presentation is binding, canonical form is not" is the subtle thing a digest usually botches, and this one gets it exactly.
- **The fan-out diagnosis is well-grounded.** "Resolution enumerates every occurrence faithfully; only the final per-interval-width-budget merge drops repeats" matches Q15/Q16 and Deficiency 1; the equal-window self-comparison test (6 vs 4 elements in the worked example) is the right probe.
- **Two genuinely sharp catches that go beyond the note's prose but are sound:** the address-keyed join is cross-document by nature (a left foot may pair a right foot in another document), and the read must be **one Σ across all named documents**, not a per-document timing — both correct and load-bearing.
- **No fabricated source-level claims:** the digest describes reference *behavior* (Q11–Q19) without naming C functions it can't cite.

I could not find a material misread, an unsound approach, a fabricated claim, an internal contradiction, or a missing load-bearing commitment. The remaining items are tightenings.

---

**Revision list**

1. **[SHARPENING] "Matching" section — "emits one pair per shared address-unit" mischaracterizes the merge's output granularity.** The reference merge emits one pair per co-advancing *run/crum*, not per address-unit (Q13/Q18; in the worked example the reference diagonal is 2 pairs over 4 positions, not 4). The true property — which the digest itself states correctly one sentence later ("per-interval width budget, exhausted after the first occurrence") — is *single-coverage*: the budget gives each shared address one pairing and orphans the repeats. Align the lead-in to the precise version (e.g., "accounts for each shared address once against a per-interval width budget, orphaning every repeated occurrence") so the granularity implication doesn't read as a per-address claim.

2. **[SHARPENING] "What must be built" / resolver — add the note's explicit "whole-document is not a separate notion" guidance.** The digest establishes bounded-window traversal ("never scan a whole document to answer a windowed question") but never states the note's design point that *whole-document comparison is itself just the largest window* — the single span `σ_full = ([s_C,1…1], δ(n,m))`, with the empty document handled as the empty span-set `(d,∅)`. This is real anti-over-building guidance (don't write a separate whole-document code path); it's worth one sentence in the resolver bullet.

3. **[SHARPENING] "How it fits" / decisions — make the arrangement-presence basis an explicit design decision.** The region resolver already commits to "the documents as they stand" (clip to current arrangement), which silently answers one of the note's open questions (whether correspondence extends to content referenced-but-not-arranged). Surface this as a deliberate choice — *arrangement-presence is the basis for "what counts as part of a version"* — with the boundary flagged as open, rather than leaving it implicit in the clip.

VERDICT: CONVERGED
