## Question 2 [theory]

> Does LM 4/60's robustness principle apply at the span level within a single link's endset — such that adding a non-overlapping span to an already-matching endset must not suppress the existing match — or does it only constrain interactions across distinct links?

# Answer

**No — LM 4/60's principle is explicitly about interactions across distinct links, not within a single link's endset. The intra-endset guarantee comes from a different principle: the existential satisfaction criterion at LM 4/58.**

These are two separate guarantees operating at different scopes:

## LM 4/58 — Within-link satisfaction (existential over spans)

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." [LM 4/58]

This is what the curated sources call **"the AND of the ORs"**: each endset must have *at least one* span matching the corresponding part of the request (existential within an endset), and all three endsets must be satisfied (AND across endsets).

Because satisfaction within an endset is existential, it is **monotonic in spans**: adding a non-overlapping span to an endset that already contains a matching span cannot suppress the existing match. The witness span is still there; the existential is still satisfied. This is a structural property of the satisfaction criterion itself, not a separate robustness axiom.

## LM 4/60 — Across-link robustness (junk-link filtering)

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

The literal subject here is **"links not satisfying a request"** — distinct link objects. The curated sources frame this as "the junk-link problem": filtering out irrelevant links in a universe full of them. The principle says system performance (and result completeness) for matching links is not degraded by the volume of non-matching links.

This is a cross-link guarantee, not an intra-endset one.

## Why they're distinct

The two principles concern different quantifications:

- **4/58**: For a *fixed link*, satisfaction is determined by an existential check over spans within each endset.
- **4/60**: Across the *space of all links*, non-matching ones don't impede discovery of matching ones.

Conflating them would be a category error. The within-endset monotonicity property (your scenario — adding a non-overlapping span preserving an existing match) follows directly from 4/58's existential satisfaction criterion. You don't need 4/60 to derive it, and 4/60 doesn't literally state it.

## Caveat on scope

The curated sources do not contain a passage where Nelson explicitly extends 4/60's wording down to the span level inside a single endset. The closest is the architectural symmetry between endsets (each is an arbitrary span-set) and the search model treating endsets uniformly — but symmetry alone doesn't establish that 4/60 *applies* at the intra-endset level; it just shows the two principles compose coherently.

If you need Nelson to have said this explicitly about intra-endset monotonicity, I don't see it in the curated material — and verifying that he didn't say it elsewhere in the 4/58–4/60 passage would require: **NEED_RAW: 4/58, 4/59, 4/60** (raw pages 225-227) to confirm no additional clarifying language was extracted.
