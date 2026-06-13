## Question 2 [theory]

> If a single link is reachable through transcluded content shared by many documents, must the count remain one for that link, or does each document through which it can be encountered constitute a separately countable appearance?

# On Counting a Link Reachable Through Shared Transclusion

**The count of the link, *as a link*, remains one.** Reachability through many transcluding documents does not multiply it. But your question conflates three different cardinalities, and the design intent only becomes clear once they are pulled apart. Let me do that.

## 1. A link is a single first-class object with a single identity

A link is not markup embedded in the documents it touches. It is its own thing, sitting at its own address, owned by one user:

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user." (4/41)

> "The link mechanism ties together the whole corpus of materials on the Xanadu system. There is essentially nothing in the Xanadu system except documents and their arbitrary links." (4/41)

Its identity is its **home address**, and that home is singular:

> "A document includes only the links of which it is the home document." (4/31)

> "The links designated by a tumbler address are in their permanent order of arrival." (4/31)

So there is exactly one link object. There is nothing for a second copy of it to *be* — it has one home, one address, one place in the order of arrival.

## 2. Transclusion shares the anchor; it does not duplicate it

The reason you *feel* a tension is that the link seems to be "in" many documents at once. But it is not in any of them — it is *strapped to bytes*, and those bytes have one identity in the Istream:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." (4/42)

When many documents transclude the same content, they do **not** each get their own copy of those bytes. They share the originals by reference:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

The link's endset points at *one* set of Istream addresses. The transcluding documents merely window to those same addresses. One strap, one set of bytes, reachable through many windows. The windows multiply; the strap does not.

## 3. This is exactly the version case, which I settled explicitly

I never wrote a sentence about counting-under-transclusion directly (so treat the *counting corollary* below as my design intent, not a verbatim ruling). But I *did* settle the structurally identical case — a link reaching the same shared content across many **versions** — and the answer there is unambiguous:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." (2/26)

Read that carefully: "a link to one version... **is a link** to all versions." Singular. One link, refracting through every version that shares the content. Transclusion across *different documents* rests on the same foundation as versioning across *the same document* — shared Istream. The conclusion transfers directly: one link, reachable through all documents that share the anchor.

## 4. What the counting operation actually counts

The satisfaction rule for link search is phrased in the singular, and that is deliberate:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

A link either satisfies a request or it does not. If its from-set lands on the shared anchor, it satisfies — **once**. `FINDNUMOFLINKSFROMTOTHREE` returns the number of *distinct link objects* satisfying the constraint; the single link L contributes 1, no matter how many documents window to the anchor. (Even if several spans of L's own from-set fall inside the request, it is still one link satisfying once.) This is also why I insisted:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

Links are discrete, enumerable objects. The count is over objects, not over encounters.

## 5. Where the number N legitimately lives — and it is never "more links"

Your instinct that "many documents" matters is not wrong; you have just attached the multiplicity to the wrong noun. There are two places N appears, and **neither is a link count**:

- **Document reachability.** "Through how many documents can this be encountered?" is a count of *documents*, and it has its own operation:
  > "This returns a list of all documents containing any portion of the material included by `<vspec set>`." (4/70) — "...regardless of where the native copies are located." (4/63)

  `FINDDOCSCONTAINING` on the link's anchor span returns N documents. That N is a property of the *(link-anchor, docuverse)* relationship — a document cardinality, not a link cardinality.

- **Delivery events.** A link rides along with its content on retrieval:
  > "This returns the material (text and links) determined by `<spec set>`." (4/67)

  Retrieve the transcluded region of document D₁ and L is delivered; retrieve it from D₂ and L is delivered again. Across contexts the link is *delivered* many times — and this is the count that matters for the byte-royalty machinery. But a delivery is an *event*, not a link. Counting deliveries no more multiplies the link than playing a record twice multiplies the song.

## Summary — three cardinalities, do not conflate them

| You are counting… | Operation | Result for one shared link |
|---|---|---|
| The link as an object | `FINDNUMOFLINKSFROMTOTHREE` | **1** — one home, one address |
| Documents it is reachable through | `FINDDOCSCONTAINING` (on the anchor) | **N** — a document count, not a link count |
| Times it is transmitted | `RETRIEVEV` deliveries | **≥ 0**, grows per delivery — an event count |

So: **the count remains one for that link.** Each document is *not* a separately countable link — it is a separately countable *window onto the same link*. A link's identity is its home address (4/31), it straps to one set of Istream bytes (4/42), and transclusion shares rather than copies those bytes (4/11). The link is one. What proliferates is the set of documents that can reach it, and the set of occasions on which it is delivered — and I gave you distinct operations to count each, precisely so they would never be mistaken for one another.

---

*Boundary note:* The principles cited above (link identity, strap-to-bytes survivability, Istream sharing under transclusion, the search-satisfaction rule, and the version-refraction ruling at 2/26) are verbatim from *Literary Machines*. The explicit corollary — "therefore the link-count under transclusion-sharing is exactly one" — is my design intent extended to a case I did not address word-for-word in the book. If you want a textual ruling rather than my reasoned extension, the pages to scrutinize are the link-search/counting passages (4/58–4/60) and the endset/anchor structure (4/42–4/47); I have reviewed the curated extracts of both and neither contradicts this, but neither states the transclusion-counting corollary outright.
