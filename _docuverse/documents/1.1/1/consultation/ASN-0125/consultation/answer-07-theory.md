## Question 7 [theory]

> Under repeated edits to the same link, must the chain of supersessions remain fully traversable from any member to both the earliest original and the current successor?

# Supersession chains: what I specified, and what I did not

Short answer: **no — not as an unconditional, automatically-maintained invariant.** And the premise needs untangling first, because in my design "repeated edits to the same link" does not produce a supersession chain at all. Three different things are being fused here; let me separate them.

## 1. Editing a link's targets creates no chain — survivability does the work

A link is a strap between bytes, not between positions. When the content at either end is edited, the link is **not** superseded and no new version of it is minted — it stays attached to whatever bytes remain:

> "A Xanadu link is not between points, but between spans of data... This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." (4/42)

So under repeated edits to a link's surroundings you still have *one* link, unchanged in identity. There is nothing to traverse because there is no chain. Survivability — not supersession — is the operative guarantee here.

## 2. Supersession is specified for documents/versions, and it is forward-oriented

The supersession link is a metalink "expected to apply to whole documents" (4/52). Its canonical purpose is to walk **forward** to the newest state:

> "Document Supersession Link: This link indicates that one document or version supersedes another. It is the canonical way to find out whether you are reading the latest version. A front-end request for supersession links is normally expected before starting to read a new document." (4/52–4/53)

Forward traversal to the current successor is therefore stated design intent — and because the front end is expected to do this *before reading*, it is expected to follow the relation to the **end** of the chain, not merely one hop.

Note also that I never specified an in-place "edit the link" operation that mints link-versions. Links keep permanent creation-order addresses (4/31), and subdividing them by further digits for such purposes I called only "a distinct possibility... discussed" — not a guarantee. A revised link is normally a *new* link at its own address, with any "this replaces that" relation **asserted** by someone.

## 3. The backward direction: the original always exists and edges are discoverable — but the chain is not auto-maintained

Two principles bear on reaching the earliest original. First, permanence — the predecessor is never destroyed:

> "the former version must remain on the network. This is vital because of the links other users may have made to it—which can now reach through from the previous version (to which they were originally attached) into the newer version." (2/43)

> "(The old viewpoint is still present too—you can always say, 'Show me what this originally was.')" (2/45)

Second, links are discoverable from *any* endset, so a supersession edge can be found from either of its ends. Searching by the to-set finds what points **at** a version (its predecessor edge); searching by the from-set finds where it points (its successor edge):

> "FINDLINKSFROMTOTHREE... This returns a list of all links which are (1) in <home set>, (2) from all or any part of <from set>, and (3) to all or any part of <to set> and <three set>." (4/69)

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

So the *mechanism* to walk a chain in both directions exists, and the earliest original is always still there. But this is **conditional**, not invariant, for two reasons I built into the design on purpose:

- **Supersession is a claim that must be created**, not auto-generated on every edit. It is asserted by whoever owns the link's home, and anyone may even assert a competing one — so a chain may have missing edges, and may *fork* rather than form a single line.
- **A supersession link, being a link, can be deleted** by its owner, entering the "not currently addressable" state: *"DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)"* (4/9). An edge can therefore drop out of the *currently* traversable set (recoverable by historical backtrack, but not "current").

## Verdict — and what a formalization should actually encode

"Must the chain remain fully traversable from any member to both the earliest original and the current successor?" is **not** an absolute structural invariant of the link algebra. What I guarantee is narrower and conditional:

1. **The earliest original is never lost** (version permanence) — the far end always *exists*.
2. **Forward resolution to the current successor is the canonical operation** — the front end is expected to follow supersession to the latest version.
3. **Every supersession edge that exists is discoverable from either of its ends** (search by any endset) — so wherever the chain is intact, it is walkable both ways.

Full member-to-both-ends traversability is a *derived* property that holds exactly when the chain has been fully asserted and no edge deleted. Encode (1)–(3); do **not** assert "full bidirectional chain traversability" as an unconditional invariant — that would over-claim, since the system supplies the mechanism and the forward expectation but does not force the chain into existence, forbid forks, or forbid edge deletion.

---

NEED_RAW: 4/52–4/53 (supersession/metalinks — to confirm whether any *multi-hop chain* language exists beyond the single-relation statement) and 2/43 (reach-through across versions). I cannot open page images in this environment, so the multi-hop/bidirectional-chain framing above is my design-intent synthesis from the verified single-relation and search-operation quotes, not a verbatim guarantee in the text.
