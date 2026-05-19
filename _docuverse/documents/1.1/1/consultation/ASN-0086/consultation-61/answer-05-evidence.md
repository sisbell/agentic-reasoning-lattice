## Question 5 [evidence]

> Does ASN-0093 publish K.σ/K.α/K.λ with explicit frame conditions covering document allocation, content emission, and link emission — including SubAllocatorAxiom and its lemmas to make T10a's runtime activation chain explicit?

## KB Synthesis

Not answerable from this KB.

ASN-0093, the K.σ/K.α/K.λ notation, `SubAllocatorAxiom`, and `T10a` do not appear anywhere in findings 0001–0078. The KB covers implementation behavior extracted from the udanax-green source; it does not contain records of any ASN-0093 consultation, its published theorems, or the specific lemma/axiom naming scheme you are referencing.

The KB does contain the underlying behaviors those constructs would likely formalize — address allocation ([SS-ADDRESS-ALLOC], [ST-ADDRESS-ALLOC], [SS-ADDRESS-SPACE]), content I-address monotonicity ([INV-MONOTONIC], [FC-GRANF-ON-DELETE]), and link emission frame conditions ([ST-CREATE-LINK], [FC-CONTENT-SPANF-ISOLATION]) — but I cannot confirm or deny what ASN-0093 published, what frame conditions it specified, or whether `SubAllocatorAxiom` is stated there, because that document is outside this KB's scope.

---

## Code Exploration

**ASN-0093, SubAllocatorAxiom, K.σ, K.α, K.λ, and T10a do not exist anywhere in this repository.**

None of these identifiers appear in `backend/`, `findings/`, `knowledge-base/`, or any other file in the test harness tree.

The closest related material is `findings/0067-frame-axiom-f0-confirmed.md`, which documents **F0** — a frame axiom established empirically from golden tests stating that INSERT/DELETE/COPY operations on one document produce no cross-document side effects, with evidence from `febe/scenarios/`. That finding covers frame conditions for content and structure operations, but it is not a published formal specification and uses none of the Greek-letter schema identifiers the question names.

**To be precise:** there is no axiomatic document in this codebase named ASN-0093, no `SubAllocatorAxiom` lemma, no K.σ/K.α/K.λ kernel schema, and no T10a theorem or "runtime activation chain." These may exist in a separate specification repository not present here. I will not speculate about their content.

If you can point me to where ASN-0093 lives (a file path or sibling repository), I can read it directly and answer against the actual source.
