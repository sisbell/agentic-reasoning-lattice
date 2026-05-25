## Question 5 [theory]

> What form must the result of comparing two documents take — a list, an overlay, a derived document, or something else?

# Form of Comparison Results

The result is **a list of ordered pairs of corresponding spans** — not a derived document, not an overlay, but structural data the front end can render however it chooses.

## At the Protocol Level

The FEBE operation `SHOWRELATIONOF2VERSIONS` returns exactly this:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." [LM 4/70]

This is the canonical form. Each pair says "this span in document A corresponds to this span in document B." The pairs are ordered, and what corresponds is determined by shared Istream origin (for versions) or by explicit counterpart links (for unrelated documents).

## What the Result Is NOT

**Not a derived document.** Comparison does not create a new document. The two originals remain untouched — consistent with the non-destruction guarantee:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals." [LM 2/45]

**Not a static overlay.** The result is structural data about correspondence, not a baked-in visual diff.

## How It Reaches the User

The front end takes the span-pair list and renders it. Nelson describes two user-facing manifestations:

> "The user may scroll through any two versions to see corresponding parts; and much more." [LM 2/21]

> "Moreover, highlighting the corresponding parts is a vital aspect of intercomparison." [LM 3/13]

So the rendering is typically **synchronized scrolling with highlighting** — but those are presentations of the underlying data, which is the span-pair list.

## Why This Form

The list-of-pairs form serves the deeper goal:

> "[A] facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

Span pairs are the minimal structure that answers "what is the same, what is different" at arbitrary granularity. They let the front end build comparison views, enable refractive link-following across versions, and support navigation from any passage to its counterpart — all from one data form.
