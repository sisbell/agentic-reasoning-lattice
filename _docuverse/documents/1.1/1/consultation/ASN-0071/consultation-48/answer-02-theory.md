## Question 2 [theory]

> Does "retrieve any portion of the material specified ... regardless of where the native copies are located" (LM 4/63) describe the *result* (each returned document may contain only a fragment of the queried material) or the *query reach* (naming a coarse coordinate pulls in its whole subtree)?

## Short answer

The clause **"regardless of where the native copies are located"** describes neither of the two things the question proposes as a binary. It is a third thing: **location transparency of the search** — the operation finds every document that contains the queried material *wherever that material physically lives and wherever it has been transcluded*. The "fragment" property the question files under *result* is real, but it comes from a **different clause** ("any portion"), not from this one. And the "coarse-coordinate-pulls-in-its-subtree" property the question files under *query reach* is a general property of span addressing, not what this clause is about.

Let me separate the operation's two clauses.

## The operation is FINDDOCSCONTAINING

From `prompts/.../operations.md` (verified):

> "This returns a list of all documents containing any portion of the material included by <vspec set>." (4/70)

> "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." (4/63)

These are two independent qualifiers on the returned set.

### Clause 1 — "any portion / any of the material" → result granularity

This is what makes each returned document possibly a fragment-holder: a document qualifies for the result if it contains *any* part of the queried span — it need not contain all of it. That is the "result" reading the question describes ("each returned document may contain only a fragment"). But that reading is carried by *this* clause, not by the native-copies clause.

### Clause 2 — "regardless of where the native copies are located" → location transparency

"Native copies" is a specific Xanadu term. Content has exactly one native (home/Istream) location, and may appear in many documents by **transclusion** without being copied:

> "Native bytes of a document are those actually stored under its control... all other bytes are obtained by front-end or back-end requests to their home locations." (4/11, `i-space-v-space.md`)

So FINDDOCSCONTAINING is the "find all transclusions" operation. The curated FEBE mapping states this directly: it "Finds all documents that transclude specified content" and "Searches Istream origin, returns Vstream locations" (`transclusion.md`, `i-space-v-space.md`).

"Regardless of where the native copies are located" therefore means: the search returns documents that contain the material **whether they own it natively or window to it from elsewhere, and no matter which server holds the native bytes**. It is a statement about the *reach of the search across native storage location / distribution*, i.e. transclusion-following and cross-server transparency — consistent with the BEBE promise that the docuverse is "a single unified space" (`bebe.md`, 4/70).

## Why it is *not* the "coarse-coordinate subtree" reading

The subtree-pull-in property — naming an account or node and getting everything under it — is real, but it is a property of **span/tumbler addressing generally**, governing the *input* `<vspec set>`:

> "A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author... or the entire docuverse." (4/38, `spans.md`)

> "A link to or search of an account or node will find any of the documents under it." (4/23, `ghost-elements.md`)

That subtree behavior is about *what you named on the way in*. The phrase in question is about *where the answers come from on the way out* (native vs. transcluded, local vs. remote). They are orthogonal.

## Bottom line

- "Regardless of where the native copies are located" = **location transparency of the result set** (transclusion-following across the distributed docuverse), not subtree query-reach.
- The "each returned document may contain only a fragment" property is true, but is supplied by the separate clause **"any portion / any of the material."**
- Subtree expansion from a coarse coordinate is a property of the `<vspec set>` *input* under span addressing, governed by the 1-position convention (4/38), not by this clause.

So if forced onto the question's axis, the phrase sits on the **result/search-scope side** — but specifically as *location independence*, which the question's "result" gloss (fragment-holding) does not capture.
