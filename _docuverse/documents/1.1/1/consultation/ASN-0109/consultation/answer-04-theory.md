## Question 4 [theory]

> What does the reader learn about the direction or roles of the connected endpoints — which side is the source and which is the destination of the relationship?

The reader learns that Xanadu links are **typically directional**, with the two primary endsets designated as a **from-set** and a **to-set** — but Nelson is careful to note that the *meaning* of "from" and "to" is not fixed by the system.

## Directionality is present but semantically open

A link's two main endsets carry the directional roles:

> "A link is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.' (What 'from' and 'to' mean depend on the specific case.)" [LM 4/42]

The key qualification is the parenthetical: **the system does not dictate which side is "source" and which is "destination" in any semantic sense.** The from-set and to-set are structural labels; their interpretation depends entirely on the link's type and the user's intent. A citation link goes from citing text to source; a comment link goes from commentary to its subject. The roles are determined by convention and link type, not by the link mechanism itself.

## The third endset (type) is not directional in the same way

Beyond from and to, the link has a third endset that categorizes rather than directs:

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." [LM 4/44]

So while from/to express direction, the type endset expresses *what kind* of relationship it is — which is what actually gives the directionality its meaning.

## Directionality matters to the user, not to indexing

Importantly, the *discovery* of links is bidirectional even though the link itself has a direction. The system indexes by all endsets, so you can search from either end:

> "Links are intrinsically bidirectional in the system's indexing. Some types are a special case where directionality matters to the user." (from the links curated source, paraphrasing the indexing model)

The directional "from/to" distinction is therefore primarily for the user's semantic understanding — the system can always find a link from any side.

## One-sided links: when there is no "from"

Nelson also describes links with only one endpoint, where the directional framing breaks down entirely:

> "Unfortunate terminological problem: since it has only one side, we use the first endset to designate the matter pointed at. To call this 'from' is inane." [LM 4/48]

This shows Nelson's own discomfort with the "from/to" terminology — for a one-sided link (like a paragraph designator), there is no source-and-destination relationship at all, just a single thing being pointed at.

## Summary

- Links are **typically directional**, with a **from-set** (source side) and **to-set** (destination side). [LM 4/42]
- But **what "from" and "to" mean depends on the specific case** — the system assigns the structural roles, while the link's *type* and the user's intent assign the semantic meaning. [LM 4/42]
- The **type endset** (third set) is symmetrical and non-directional, categorizing the relationship. [LM 4/44]
- Directionality matters **to the user**, but link **discovery is bidirectional** — you can search from either side.
- For **one-sided links**, the source/destination framing doesn't apply at all, and Nelson calls labeling the single side "from" "inane." [LM 4/48]
