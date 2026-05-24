## Question 5 [theory]

> Is `citation.depends` intended to be coverage-equivalent to the retraction type R (i.e., does it carry retraction semantics under the relational vocabulary), or is it a distinct relation whose coverage class is disjoint from `[R]`?

# On `citation.depends` vs Retraction Type R

I need to flag upfront: the terms `citation.depends`, retraction type `R`, and coverage class `[R]` are **modeling-layer vocabulary**, not terminology I established in *Literary Machines*. I specified link **types** as user-extensible categories, not a formal relational algebra with coverage classes. Let me speak to the underlying design intent.

## What I actually specified

In LM 4/53-4/54, I listed citation and retraction-class links as **distinct types** in the standard set:

> "Citation Link: Like a footnote reference with bridge to source" [LM 4/54]

> "Document Supersession Link: This link indicates that one document or version supersedes another. It is the canonical way to find out whether you are reading the latest version." [LM 4/52-4/53]

These serve fundamentally different semantic purposes:

- **Citation** establishes a *referential dependency* — "I am drawing on this source." It is forward-looking acknowledgment of intellectual lineage.
- **Supersession/retraction** declares *obsolescence* — "this replaces that." It is backward-looking invalidation.

## The design intent: disjoint, not equivalent

These should be **distinct relations with disjoint coverage**, not coverage-equivalent. My architecture treats all link types as discriminated by the third endset's address:

> "Links are meant to be extensible for the arbitrary needs of any user. Thus the set of link types is open-ended... What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." [LM 4/43, 4/44-4/45]

If citation and retraction collapsed to the same coverage class, you could not answer the question I designed supersession links specifically to answer:

> "A front-end request for supersession links is normally expected before starting to read a new document." [LM 4/52-4/53]

A reader checking "am I reading the latest?" needs retraction links to be distinguishable from citation links. If `citation.depends ≡ [R]` under coverage, that distinguishability is lost.

## Where the asymmetry matters

Citation creates a **dependency without invalidation**: cited work remains valid; the citing work acknowledges it. Retraction creates **invalidation**: the retracted work is declared no longer current. The cited document is *strengthened* by being cited; the retracted document is *deprecated* by being superseded.

## Conclusion on design intent

`citation.depends` should be a **distinct relation whose coverage class is disjoint from `[R]`**. Making them coverage-equivalent would conflate "I draw on this" with "this replaces that" — destroying the semantic distinction my standard type set was meant to preserve.

NEED_RAW: 4/53-4/54 — if the formal model needs to verify whether I listed any link type that *bridges* citation and retraction semantics (e.g., a "certified link" or "alternative-version link" that might sit between them), the full enumeration on these pages should be consulted directly.
