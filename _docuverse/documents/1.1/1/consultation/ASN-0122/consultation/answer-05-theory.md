## Question 5 [theory]

> When a document is compared with itself, must the result be the trivial whole-extent identity, or must the system also report internal correspondences where the same content appears at multiple places in that one document?

## Short answer

Not the trivial whole‑extent identity alone. When a document is compared with itself, the system **must** report internal correspondences wherever the *same Istream content* recurs at more than one place in the document — but "same content" here means **shared Istream origin** (a transclusion/copy), **not** merely identical-looking text. If the document contains no internal repetition of shared‑I content, then self‑comparison degenerates to the whole‑extent identity. The off‑diagonal pairs appear exactly when, and only when, there is real internal recurrence of the same source bytes.

## Why this follows from the definition of correspondence

Correspondence in Xanadu is not a stored annotation about "what changed." It is a **structural relation defined by shared Istream origin**: two V‑positions correspond if and only if they map to the same I‑address. Critically, that rule names no restriction to *distinct* documents or *distinct* versions — it is a property of the addresses themselves. So two V‑positions in *one* document that happen to point at the same I‑content satisfy the relation just as surely as two positions in different versions do.

The comparison operation is specified to return *all* such pairs, with no diagonal‑only carve‑out:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." `[LM 4/70]`

Give it the same spec‑set twice and it returns the ordered pairs of spans that correspond. That set is the diagonal (every span trivially shares its own I‑address) **plus** every off‑diagonal pair `(s₁, s₂)` where `s₁ ≠ s₂` but both carry the same Istream bytes. To omit the off‑diagonal pairs would be to fail to report spans that genuinely correspond — a violation of the operation's own specification.

This is consistent with the purpose Nelson gives correspondence: intercomparison that shows, "word for word, what parts ... are the same" `[LM 2/20]`. Applied to a single document, the substantive thing self‑comparison reveals is precisely *where the same source material is used in more than one place*.

## The crucial refinement: origin, not appearance

The reason this is *not* a general "find me repeated text" feature is that Xanadu identity is by creation, not by value. The same byte stream that is included from elsewhere keeps its home address:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." `[LM 4/11]`

A `COPY` is exactly such an inclusion — it shares I‑addresses with its source:

> "The material determined by `<spec set>` is copied to the document determined by `<doc id>` at the address determined by `<doc vsa>`." `[LM 4/67]`

So if a document `COPY`s a span into two places (or transcludes the same source span twice), those two V‑positions share one I‑address and therefore **correspond** — self‑comparison must surface that pair. By contrast, two passages that were *independently typed* to the same wording have *different* I‑addresses; they do **not** correspond, and self‑comparison must **not** invent a pair for them. The operation distinguishes "this is the same material, used twice" from "someone wrote the same words" — and reports only the former.

## The degenerate case

A document with no internal shared‑I recurrence — purely native, linear content typed once — has nothing off the diagonal. Self‑comparison then yields only the whole‑extent identity (the document corresponds to itself, span for span). So the answer is conditional in the right way: the result is the identity *plus* the internal correspondences, and the internal set is empty exactly when there is no internal transclusion/copy.

## Honesty flag

Nelson does not, in the curated sources, explicitly walk through the self‑comparison edge case. The conclusion above is a **deduction** from two things he does state explicitly: (1) that `SHOWRELATIONOF2VERSIONS` returns *the* corresponding span pairs `[LM 4/70]`, and (2) that correspondence is grounded in shared Istream origin rather than textual equality `[LM 4/10–4/11, 4/67]`. As the statement of design *intent*, I'm confident in it; if you want to confirm Nelson nowhere adds an explicit edge‑case note about identical or self spec‑sets (or about reporting multiplicities), the page to check is:

NEED_RAW: 4/70 (and surrounding 4/68–4/70, the operation definitions)
