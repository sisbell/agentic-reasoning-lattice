# Review of ASN-0131

I checked the proofs and the worked instance line by line. The technical content is sound: RE-NCD's prefix-relation argument is valid; RE-ADDR's fresh-output reasoning (antichain + unit-depth to-set ⇒ only self-retraction can nullify a fresh emission) holds; the worked instance computes correctly and exercises each distinctive postcondition; RE-UDIST, both RE-UDIST-∩ counterexamples (the injective one is the right way to show injectivity is no rescue), RE-CWP, and RE-RET (including the R-Scope-discharged backward half and the careful bridge from ASN-0086's narrower `→` to ASN-0047's full vocabulary for nullification permanence) are all correct. The stability catalog is complete over the transition vocabulary, the wp analysis is non-trivial, and every cited claim is a foundation claim that exists.

The findings below are prose-redundancy, which is the active anti-bloat concern for this note. No correctness REVISE.

## REVISE

### Issue 1: The "injectivity cannot restore ⊇" conclusion is stated four-to-five times in one paragraph
**ASN-0131, §"Composing regions" (RE-UDIST-∩, reverse-inclusion paragraph)**: the conclusion is first asserted ("*no injectivity-style structural restriction on the arrangement recovers it*"), then demonstrated by the injective counterexample, and then re-summarized repeatedly:
- "the second shows that *removing* it does not restore `⊇`."
- "An arrangement restriction such as injectivity therefore **provably cannot** recover `RE(W₁ ∩ W₂, d, Σ) = RE(W₁, d, Σ) ∩ RE(W₂, d, Σ)`."
- "The obstruction is *injectivity-proof*, not *restriction-proof*."
- "(the injective counterexample violates it under a perfectly injective arrangement)"

**Problem**: After the thesis and the two constructions establish the point, three-plus closing restatements say the same thing in different words. The reader has to wade through repeated summaries of a conclusion already proved. This is exactly the "two paragraphs say the same thing in different words" pattern, compressed into one paragraph.

**Required**: State the conclusion once (the thesis sentence plus the two constructions suffice). Keep the genuinely new content — the *degeneracy* sufficient condition and the "not structural / not checkable without inspecting coverage" characterisation of the exact condition — and drop the redundant re-summaries, including the parenthetical that re-cites the injective counterexample.

### Issue 2: "Anchoring without names" stated twice in near-identical phrasing
**ASN-0131, §intro vs §"The unit of the answer: anchoring without names"**:
- Intro: "We want to be told **that** this content is bound, and **how** it is bound … without being told **which** links bind it."
- Definition section: "it surfaces *that* anchoring is present, and its shape, without ever naming the anchored link."

**Problem**: The two carry the same content in the same "that/how … without which" shape. RE-UNIT, the worked-example bullet, and the closing retraction sentence then make the point a third, fourth, and fifth time. The intro framing and the RE-UNIT claim each earn their place; the definition-section restatement is the redundant one — it precedes the mechanism sentences ("The existential `(∃ a : …)` consumes the link and discards it…") that actually *establish* the property.

**Problem is milder than Issue 1** but is the same compounding pattern: lead with the mechanism, let RE-UNIT carry the claim, and cut the prose restatement of the intro's motivation.

## OUT_OF_SCOPE

None. The note defers link enumeration, counting, pagination, named-link reads, and rendered-into-V-order answers to siblings and to its own Open Questions (1–7), and it cites — rather than rebuilds — ASN-0127's image machinery and existence/discovery taxonomy. Scope is handled correctly.

VERDICT: REVISE
