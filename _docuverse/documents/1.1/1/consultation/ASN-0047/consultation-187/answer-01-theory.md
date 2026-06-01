## Question 1 [theory]

> Is the reverse index meant to record genuinely *past* containment — a fact that was once true and may since have ceased — or merely that a content-document association was registered at some point, present included?

## Short answer

Neither framing is quite right. Nelson's reverse index (`FINDDOCSCONTAINING`) is meant to record **genuine, present-tense containment** — but because Xanadu storage is append-only and versions are permanent, a containment relation that was ever true never simply "ceases." It persists as a fact about the *version* in which it held. So the index is not a mere registration log divorced from truth, nor a record of bygone facts no longer true; it tracks actual structural inclusion in a docuverse where the past is preserved as addressable present.

## The operation is phrased in the present

The two specifications of the operation both use present-tense "containing":

> "This returns a list of all documents containing any portion of the material included by <vspec set>." (4/70)

> "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." (4/63)

This is not a "was-associated" or "was-registered" predicate. Containment is computed structurally: a document contains content X if its V→I mapping references X's Istream address. It's a live property of arrangement, not an entry in an audit trail.

## Why "past vs. present" partly collapses

The reason the question is subtle is Nelson's non-destruction model. Deleting transcluded content from your *current* version does not erase the containment fact — it only changes the current arrangement:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

Because every prior version is itself a permanent, addressable entity, a version that ever contained X *still contains* X. So "D once contained X" is never a fact that has fully "ceased to be true" — it remains true of the version that established it. The containment relation is rooted in shared I-addresses, which are permanent:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

This is why a single link or inclusion reaches across versions:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." (2/26)

## So which interpretation is correct?

- It is **not** "genuinely past containment, a fact that has ceased" — Nelson's architecture has no mechanism by which a containment fact ceases to be true; the deleted bytes "remain included in other versions" and Istream is never destroyed.
- It is **not** merely "an association registered at some point" in the weak, possibly-untrue-now sense — the index reflects *actual* structural inclusion (shared I-addresses), not a historical annotation that may no longer correspond to reality.

The accurate reading is a third option: containment is a **present-tense structural fact, evaluated per version, over a version-space that is itself permanent**. "Ever contained" implies "still contains, in some version," because nothing is thrown away. The index therefore behaves like an append-only accumulation in *effect* (associations never vanish from the docuverse), but it does so honestly — every association it reports is genuinely true of some addressable version.

## One genuine gap

Nelson does not explicitly state whether `FINDDOCSCONTAINING X` returns a document whose *current* version has deleted X (i.e., whether the result is keyed to the current arrangement or to version-space as a whole). The present-tense wording ("containing") suggests current arrangement, while "may remain included in other versions" (4/11) implies the prior versions still surface. The two are reconciled only if the operation searches version-space, where the deleting version simply no longer matches but earlier versions still do.

NEED_RAW: 4/63, 4/70 (pages 225, 237) — to confirm whether Nelson disambiguates current-version vs. all-version scope for `FINDDOCSCONTAINING`, which is the one point the curated text leaves underdetermined.
