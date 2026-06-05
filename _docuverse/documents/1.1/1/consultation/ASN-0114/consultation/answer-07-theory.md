## Question 7 [theory]

> Must two requests for the same end of the same link, with no intervening change to the link, always return specifications that denote identical content?

# Yes — but the guarantee rests on two distinct properties that compose

The question has two layers: (1) does RETRIEVEENDSETS return the *same specification* given an unchanged link, and (2) does that specification *denote identical content*? Both hold, but for different reasons.

## Layer 1: The specification is stable because the link is unchanged

A link is a stored object with its own address, owned by a user. Its endsets are part of that stored structure:

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user." (4/41)

`RETRIEVEENDSETS` simply returns what is stored:

> "This returns a list of all link end-sets that are in <spec set>." (4/70)

With "no intervening change to the link," the stored from-set/to-set is identical between the two requests. Nelson specifies no nondeterminism in this operation, so the returned span-set is the same.

(Caveat: Nelson does not explicitly guarantee a *canonical* representation — `spans.md` notes a span can be given as "a pair of tumblers" or as "address + difference tumbler." So two requests could in principle return equivalent-but-differently-encoded specs. This does not affect the answer, because the question asks whether the specs *denote identical content*, and both encodings denote the same spans.)

## Layer 2: The spans denote identical content because endsets reference Istream

This is the load-bearing property. Endsets attach to bytes via the invariant address space, not to mutable positions:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing." (4/42)

Those bytes live at permanent, immutable Istream addresses:

> "Content you create gets a permanent Istream address... That address will always return that exact content. Content is immutable - it never changes after creation." (`i-space-v-space.md`)

Because the endset denotes Istream spans, and Istream content "never changes after creation," the content denoted is identical across the two requests — even across an arbitrary time gap, and *even if the content has been "deleted"* from some document's current arrangement:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

Deletion changes Vstream arrangement only; the Istream bytes the endset straps onto persist. This is precisely why the survivability annotation reads:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." (4/43)

## Why the answer would be *no* under the alternative design

If endsets were specified in Vstream (positional) terms, then "no change to the link" would not be sufficient — an intervening edit to the underlying document could shift or reinterpret a V-position, so the same specification could denote *different* content. Nelson rules this out by design: the whole point of strapping links to bytes (Istream) rather than points (Vstream) is to decouple link content from document editing. The content-identity guarantee for an unchanged link is therefore inseparable from the I-space/V-space separation.

## Edge case: the type endset / ghost elements

If "end" is taken to include the type ("three-set"), that endset may point at a ghost element where nothing is stored:

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." (4/45)

This does not break the guarantee: an unchanged endset pointing at an empty address consistently denotes the same (empty) content on both requests — matching is "by address, not content" (`link-type-system.md`).

## Bottom line

**Yes.** Two requests for the same end of the same unchanged link must denote identical content, because (a) the stored endset is deterministic when the link is unchanged, and (b) endsets reference the immutable Istream, whose content "never changes after creation." The guarantee is a composition of *link immutability* and *content-address immutability*; remove either and it fails.

One flag on rigor: Nelson does not state an explicit idempotence axiom for `RETRIEVEENDSETS`, nor a canonical-form guarantee for returned spans. The conclusion above is an inference from the link-survivability (4/42–4/43) and Istream-immutability properties, which together strongly entail it. If you want the operation-level determinism stated in Nelson's own words rather than inferred, NEED_RAW: 4/69–4/70.
