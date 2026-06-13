## Question 3 [theory]

> Is RETRIEVEENDSETS intended to query a content (text-subspace) passage specifically, or any region of V-positions, including positions in the link subspace?

**Short answer:** RETRIEVEENDSETS is *not* a text-passage query. Its `<spec set>` argument designates **links** — positions in the link subspace (the `…0.2.N` addresses) — and it returns those links' from-sets and to-sets. So it's your second option: it operates over V-positions in the link subspace, not over a content/text passage. (A pure text passage would yield nothing, since text positions have no endsets.)

## What Nelson specifies

The only verified statement is terse (4/70):

> "This returns a list of all link end-sets that are in <spec set>."

Both the FEBE and endsets concept files gloss this as: *"Returns the from-set and to-set of specified links."*

The decisive point is the **return type**: an *endset* is a property of a link. A text byte has no from-set or to-set. So whatever region `<spec set>` delimits, the only things that contribute output are links — and links live in the link subspace. From the link-address structure:

- `N.0.U.0.D.V.0.2.1` — first link of the document (link subspace `0.2.N`)
- bytes are addressed as `version.position` (the `1.x` text subspace)

You hand RETRIEVEENDSETS the link addresses you want dereferenced; it returns where each one points.

## It uses a general spec-set, not a text-only argument

RETRIEVEENDSETS takes the same `<spec set>` type as RETRIEVEV, and Nelson tells us what a spec-set generically covers (4/67):

> "This returns the material (text and links) determined by <spec set>."

So the argument is a general docuverse-region designator that can span both subspaces — it is in no way restricted to a text passage. What restricts the *output* is simply that only the links falling within that region have endsets to return.

## Why it targets links and not text (division of labor)

Reading RETRIEVEENDSETS as a link-dereference operation keeps the FEBE command set non-redundant:

- **FINDLINKSFROMTOTHREE** — give it *content* regions (from-set/to-set/three-set) plus a home-set, and it returns link IDs: "all links which are (1) in <home set>, (2) from all or any part of <from set>, and (3) to all or any part of <to set> and <three set>." (4/69)
- **RETRIEVEENDSETS** — give it those *link* addresses, and it returns the endsets (where the links actually reach).

That is the standard two-step: FINDLINKS answers "which links touch this text?"; RETRIEVEENDSETS answers "where do these links point?" If RETRIEVEENDSETS instead took a text passage and returned the endsets of links touching it, it would largely duplicate FINDLINKS. The "in `<spec set>`" wording — links/endsets *located in* the region, i.e. at their home link addresses — also points to link-subspace positions rather than to text being pointed *at*.

Note the asymmetry worth keeping straight: the **input** you query is link-subspace positions, but the **endsets returned** are themselves arbitrary span-sets that can point anywhere in the docuverse (including text), per the endset model (4/42–4/45).

## Caveat / where the curated text runs out

The curated sources establish the return semantics ("from-set and to-set of specified links") and that spec-sets generically cover text+links, which together support the answer above. What they do **not** state explicitly is a constraint on the argument — i.e., whether `<spec set>` is *required* to be link addresses, or is simply a general region from which links are filtered (and how "in" is meant when a mixed text+link region is passed). My reading (general region; only contained links produce output) is an inference from the return type and the operation set's division of labor.

NEED_RAW: 4/70 (to confirm Nelson's exact surrounding wording on the RETRIEVEENDSETS argument; 4/63 and 4/67–4/69 give the adjacent RETRIEVEV / FINDLINKS context that frames it).
