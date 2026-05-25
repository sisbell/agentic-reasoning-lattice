## Question 10 [theory]

> What must the system guarantee about resolving origin when a span has passed through several intermediate documents before reaching its current location?

# Origin Resolution Through Intermediate Documents

The guarantee is structural, not procedural: **the home document of any content is directly knowable from its I-address, regardless of how many intermediate transclusions sit between you and that content.**

## The Core Guarantee

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This is unqualified. It holds for ANY byte, regardless of provenance depth. The mechanism is the I-address itself: the Document field of the tumbler encodes origin permanently. Resolution is O(1) — direct lookup — not O(n) chain-walking.

## Why Chain-Walking Is Unnecessary

Transclusion is reference, not copy. When document D includes content originally from A (perhaps after passing through B and C):

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

D's reference points **directly to A's I-address** — not to "the version that was in C, which got it from B." The intermediate documents created their own inclusion relationships with A independently. They are not on the resolution path; they are parallel witnesses to the same origin.

## What This Rules Out

1. **No provenance chain corruption** — An intermediate document cannot rewrite or claim origin of content it included. The I-address is immutable.
2. **No origin drift through hops** — Multi-level transclusion never shifts the home document.
3. **No attribution severance** — The connection to true origin cannot be broken by intermediate handling.

## Indefinite Layering Is Explicit

Nelson addresses arbitrary depth directly:

> "A document may have a window to another document, and that one to yet another, indefinitely. Thus A contains part of B, and so on. One document can be built upon another, and yet another document can be built upon that one, indefinitely: each having links to what was already in place." [LM 2/34]

The glass-pane metaphor makes this concrete: each pane is transparent to its sources. Looking at any character through any number of layered panes, you can ask "where is this REALLY from?" and get back the true home — not the previous pane.

## Navigation Through Intermediates (Optional)

Users may also choose to step through the chain pane-by-pane rather than jumping to origin:

> "Only when you step through the window--turning one glass page and going on in the next--do you reach the original that you wanted. But stepping through the window means you are now in another work." [LM 2/34]

Both views are supported — direct origin (always guaranteed via I-address) and hop-by-hop navigation (available by traversing inclusion links). The **guaranteed** resolution is the direct one. Walking the chain is a navigation choice for users who want to see the intermediate contexts, not a requirement for finding the origin.

## Summary

| Resolution path | Status |
|-----------------|--------|
| Direct to home document via I-address | **Guaranteed**, O(1), regardless of depth |
| Through chain of intermediates | Available as navigation, not required for origin lookup |

The fundamental invariant: **identity is in the address, not in the path that brought the content to its current viewing context.** This is what makes attribution survive through any depth of compound documents.
