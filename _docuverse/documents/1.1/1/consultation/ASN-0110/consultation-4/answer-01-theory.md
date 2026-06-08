## Question 1 [theory]

> Was RETRIEVEENDSETS intended to return endsets only for the three standard roles (from, to, type), or for every role of arbitrary-arity (N ≥ 3) links touching the region?

I don't have file-read access in this session, so I'll answer from the curated sources and flag where the original page is needed.

## Short answer

The question's premise — "arbitrary-arity (N ≥ 3) links" — does not match Nelson's design. In *Literary Machines*, a Xanadu link is a **fixed three-endset structure**, not an N-ary relation of variable arity. RETRIEVEENDSETS is therefore defined over the standard endset roles of that three-part link, not over some variable-arity role list, because variable-arity links do not exist as a primitive.

## Why Nelson's links are not arbitrary-arity

The link is consistently described as having exactly three endsets — from, to, and type:

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." (4/44)

> "A link's home (any home) is an element located on one side; and its three endsets map to the other sides." (4/46)

The three roles are from-set, to-set ("2-set"), and type ("three-set" / "3-set"). What looks like "arbitrary arity" in Xanadu is actually achieved by **composition**, not by a single N-ary link:

> "Complex relational structures, such as the faceted link (discussed in Chapter 2), may be constructed with links to links. These use the two-sided link structure much like the CONS cell in LISP, and may be built into arbitrary compound links." (4/51)

So a faceted/compound relation of high arity is built from many three-endset (or two-sided) primitives linked together. There is no single link object carrying N ≥ 4 endsets that RETRIEVEENDSETS would need to enumerate. Where arbitrary structure exists, it lives in a *graph of three-endset links*, and RETRIEVEENDSETS would surface the endsets of each constituent primitive link in the region — not a flattened list of "every role" of one synthetic N-ary link.

Note also that arity can be *lower* than three: one-sided links exist (e.g. the paragraph designator), using only the first endset (4/48). This further confirms the model is "a fixed small set of named roles," not variable arity.

## What RETRIEVEENDSETS itself returns

The verbatim command definition is:

> **RETRIEVEENDSETS**: "This returns a list of all link end-sets that are in <spec set>." (4/70)

This is scoped by region (the spec-set), returning the endsets of links touching that region. It operates on the standard three-endset link structure.

## One unresolved precision point

There is a discrepancy I cannot fully resolve from the curated material. The verbatim quote says "all link end-sets," but the curated operation tables in `endsets` and `links` summarize RETRIEVEENDSETS as returning specifically **the from-set and to-set** (i.e., possibly *excluding* the type/3-set). So the open question is not "three standard roles vs. arbitrary arity" (the answer there is clearly: three standard roles), but rather **whether RETRIEVEENDSETS returns from+to only, or all three including type**. The curated text is internally inconsistent on this narrower point.

NEED_RAW: 4/70 (raw page 237) — to confirm whether RETRIEVEENDSETS returns from-set + to-set only, or all three endsets including the type/three-set, and to verify it has no provision for more than three roles.

## Bottom line

RETRIEVEENDSETS returns endsets for the standard named roles of Nelson's three-endset link, because that is the only link primitive he defines. Arbitrary-arity links are not part of the model; high-arity relationships are represented as compound structures built from three-endset/two-sided links (4/51), and RETRIEVEENDSETS would return the endsets of those constituent links rather than the "N roles" of any single variable-arity link. The only genuinely open detail is whether the returned set includes the type endset or just from/to.
