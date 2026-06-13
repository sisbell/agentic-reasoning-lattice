## Question 4 [theory]

> The content-region foundation distinguishes a link's mere existence from its discoverability through the arrangements a region participates in; which side of that distinction must this operation answer — does surfacing anchoring without naming links report existence, or report discoverability?

## Answer: it reports **existence**, not discoverability.

Surfacing anchoring without naming links answers the existence side of the distinction. It asserts that a content region is bound by linking — that something connects here — while deliberately withholding exactly what discoverability would require. Let me lay out why, because the question is built around a trap worth naming explicitly: *region-side* is not the same as *discoverability-side*.

### The two layers the distinction lives on

In my design, a link does not attach to a position in a document. It attaches to **content** — to spans of bytes in the invariant store:

> "A Xanadu link is not between points, but between spans of data." [LM 4/42]

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

That binding — the strap between the link and its bytes — is the *anchoring*. It is an existence-level fact. It holds regardless of which arrangements the content currently appears in, which is precisely why links survive editing: the anchoring is to the content, not to any one document's ordering of it.

Discoverability is a different layer. A content region participates in many arrangements — every version and every compound document that includes (transcludes) those bytes. The link reaches the reader *through* those arrangements:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

So: anchoring is one binding at the content layer; discoverability is the projection of that binding through the many arrangements the region participates in. The question's own phrasing — "discoverability **through the arrangements a region participates in**" — pins discoverability to the arrangement layer. Anchoring sits beneath it, on the content layer, where existence is decided.

### Why "without naming links" forecloses discoverability

Discovery, in my system, *shows you the connections*. The whole point of the inbound query is delivery:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'— and be shown all these outside connections without appreciable delay." [LM 2/46]

To be *shown* a connection is to have it named and made followable. A link you cannot name is a link you cannot refractively follow through any arrangement — it is not discoverable to you; you have only learned that it is *there*. Withholding the names is therefore the act that keeps the report on the existence side of the line.

My own operations draw the same boundary cleanly:

- **RETRIEVEDOCVSPANSET** — "This returns a span-set indicating both the number of characters of text and the number of links in document" [LM 4/68]. A *count*. Presence without identity. Existence.
- **FINDLINKSFROMTOTHREE** — "This returns a list of all links which are (1) in <home set>, (2) from all or any part of <from set>, and (3) to all or any part of <to set> and <three set>" [LM 4/69]. Named, retrievable, followable. Discoverability.

"Surfacing anchoring without naming links" is of the first kind: it reports the presence of the binding, like a count, not the retrievable list.

### Disarming the trap

One could argue the operation must be discoverability because it is *region-side* and inbound, and inbound discovery is "what connects here." But region-side does not entail discoverability. The inbound view can report either thing:

- *Anchoring present* (unnamed) → the region's bytes are bound by some link → **existence**.
- *Here are the links* (named, followable through this arrangement) → **discoverability**.

That the in-links live elsewhere, not in the region itself, makes this sharper:

> "By contrast, a document's in-links are those stored elsewhere which point to it. These out-links are under control of its owner, whereas its in-links are not." [LM 2/31]

The link's existence is established at its own home, independent of the region. What the region can contribute, when you actually search it, is *discoverability* — and that contribution is only realized when the links are named and made followable (and, in principle, scales: "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]). Stop short of naming, and the region has reported only that the anchoring exists.

### Design intent

So the operation *must* answer existence. It says "this content is anchored" — links are bound here — which is the content-layer, arrangement-independent fact. It must **not** be read as reporting discoverability, because it withholds the very things discoverability is made of: identified links, followable through the arrangements the region participates in. Surfacing anchoring tells you there is something to discover; it is not itself the discovery.

---

*A scoping note on sources:* the vocabulary in the question — "content-region foundation," "the arrangements a region participates in," "surfacing anchoring" — is this project's design language, not phrasing from *Literary Machines*. I have answered by mapping it onto my own constructs: anchoring = the link's strap to its bytes in invariant content space; arrangements = the versions/documents that include (transclude) that content; discovery = the named, refractively-followable "what connects here." All quotations above are verbatim from the verified curated extracts. If you want me to ground any step against the original pages on links and search rather than the curated summaries, the relevant raw range is **NEED_RAW: 4/41–4/60** (link structure, endsets, and the search/satisfaction model).
