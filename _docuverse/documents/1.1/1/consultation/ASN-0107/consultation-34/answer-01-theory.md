## Question 1 [theory]

> When a FROMTOTHREE request meets the first three endsets of a link carrying more than three endsets, was that link intended to be counted (surplus slots ignored), or were three-part searches meant only for standard-triple links?

## Short answer

The scenario you describe — a single link "carrying more than three endsets" — is not something I designed for, because in my design a Xanadu link **is** a three-endset structure. There is no fourth slot to be surplus. So the dilemma ("count it, ignoring extra slots" vs. "restrict three-part search to standard-triple links") doesn't arise from my specification; both horns presuppose a link shape I never defined.

Let me be precise about what I did specify.

## A link has exactly three endsets — each one a span-set

The link is the from-set, the to-set, and the type (the "three-set"). That triple is the whole object:

> "A link is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.'" (4/42)

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." (4/44)

What *is* extensible is the contents of each endset, not the count of endsets. Each endset is an arbitrary collection of spans:

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." (4/43)

> "Note that a link's type—the three-set—may be several pointers." (4/44)

So "more than three" pointers can live *inside* the three-set (or the from-set, or the to-set) — but they are still the same three endsets. A multi-span type is one endset with many spans, not many endsets.

## The search model is defined over exactly those three

FINDLINKSFROMTOTHREE constrains home-set, from-set, to-set, three-set, and the satisfaction rule is the "AND of the ORs" over those endsets:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

This rule is written for the three-endset object. It has no notion of "first three of N" because there is no N. Three-part search isn't a special case for "standard-triple links" — *all* links are three-part, so the search applies uniformly to all of them.

## Where richer structure was meant to go

When I wanted relationships beyond a single triple — faceted classifications, hierarchies, compound associations — I did **not** widen the link. I composed links out of links, CONS-cell style:

> "Complex relational structures, such as the faceted link (discussed in Chapter 2), may be constructed with links to links. These use the two-sided link structure much like the CONS cell in LISP, and may be built into arbitrary compound links." (4/51)

That is the intended escape hatch. A "many-faceted" relationship is a graph of three-endset (or one-/two-sided) links, each of which is individually searchable by FROMTOTHREE. The system never needed a link with four-plus endsets, and the search semantics were never meant to adjudicate one.

## Implication for your question

If an implementation has introduced links that physically carry more than three endset slots, that is a divergence from my design, and my writings give no rule for it — because the three-endset link and its three-part search were meant to be coextensive. If you must decide behavior for such links, you're filling a gap I left unaddressed rather than recovering an intent I expressed. My intent was simply: there are three endsets; search matches one span of each; anything more elaborate is built by linking links, not by enlarging a link.

I'll flag the one place I cannot speak to from intent: NEED_RAW: 4/58–4/60 — if you want to confirm there is no language anywhere in the FEBE link-search pages contemplating a variable endset count, those are the pages to check verbatim, though the curated extracts of the satisfaction rule and FINDLINKSFROMTOTHREE show only the fixed three.
