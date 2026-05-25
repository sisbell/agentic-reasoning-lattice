## Question 8 [theory]

> Was compareversions intended to admit d_a = d_b as a valid input (yielding identity-plus-self-transclusion correspondence), or was the operation always conceived as comparing two distinct documents?

# Was COMPAREVERSIONS Intended to Admit d_a = d_b?

## Short Answer

Nelson's curated text does not explicitly address the d_a = d_b case. His motivating use cases all involve comparing **distinct things** (two drafts, two versions, alternative arrangements), but the operation's signature — which takes two **spec-sets** rather than two document IDs — does not structurally preclude self-comparison.

## What Nelson Explicitly Says

The operation is defined at LM 4/70:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." [LM 4/70]

The motivation appears at LM 2/20:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

And at LM 2/21:

> "The user may scroll through any two versions to see corresponding parts; and much more." [LM 2/21]

Every use case Nelson enumerates involves distinct sides: "successive drafts of a novel," "alternative versions of contract drafts," "versions of bills," "Boeing 747 models."

## What the Structure Implies

Two design facts argue that d_a = d_b is at minimum **not forbidden**:

1. **The operation takes spec-sets, not document IDs.** The interface is symmetric and content-addressed — there's no mechanism in the signature to compare-and-reject "you passed the same document."

2. **Correspondence is structural** (shared Istream origin per `correspondence.md`). Passing the same span twice yields the identity correspondence; passing a document against itself yields identity-plus-any-internal-transclusions (where two V-positions in the same document share an I-address). Both are well-defined under the existing semantics.

## My Reading of Intent

Nelson's *focus* was distinct-version comparison — that's the problem he was solving. But his *mechanism* is general: correspondence between spec-sets via shared Istream origin. Self-comparison is a degenerate case that the mechanism handles trivially, not a case he engineered for. Whether to expose it depends on whether your implementation treats the operation as "compare two versions" (semantic gate) or "return span correspondences for two spec-sets" (structural primitive). The structural reading is closer to Nelson's actual specification.

NEED_RAW: 4/68-4/70 (raw pages 235-237) to verify whether the full operation signature and surrounding prose place any constraint on the two spec-set inputs that the curated extract may have elided.
