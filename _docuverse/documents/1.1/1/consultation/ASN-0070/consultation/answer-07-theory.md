## Question 7 [theory]

> What must the system promise about the stability of a link's resolution — if the same link is resolved against the same document version twice, must the result be identical?

Yes — resolution of the same link against the same document version must produce identical results. This is not an optimization or a convenience; it is a structural guarantee that falls out of three deeper invariants of the system.

## Why the guarantee holds

**1. Istream content is immutable.** A byte at an I-address is that byte forever. The whole point of separating Istream from Vstream is that the content layer is frozen even while arrangements (Vstreams) evolve. As I put it: "Native bytes of a document are those actually stored under its control and found directly in storage under its control" [LM 4/11]. Once stored, they don't shift, mutate, or get rewritten.

**2. Versions are frozen arrangements.** When you specify a version, you specify a particular Vstream mapping over particular Istream content. New edits create new versions; they don't modify old ones. This is the whole point of the "ongoing braid" model — "A document is really an evolving ONGOING BRAID" [LM 2/14], and *each strand* is fixed once laid down. "The user may go back in time to any previous version" [LM 2/15] presupposes those previous versions are stable enough to go back *to*.

**3. Links resolve via permanent addresses.** "A Xanadu link is not between points, but between spans of data" [LM 4/42], where those spans are identified by tumbler addresses that "remain valid" [LM 4/19] forever. Resolving the link means dereferencing those addresses. Same address, same bytes.

## The pounce guarantee makes this explicit

The whole part-pounce model only works if resolution is deterministic:

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." [LM 2/16]

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

That sentence — "a given part of a given version at a given time" — is the contract. The same triple yields the same answer. If it didn't, citation would be impossible, version comparison meaningless, and the whole archival vision incoherent.

## What I am NOT promising

Three things that look like exceptions but are actually consistent with the guarantee:

**Live windows are NOT exceptions.** "A quotation — an inclusion window — may be fixed to another document in two ways: at a certain point in time... Or second, at a relatively fixed location in the document space, in which case updates are seen automatically" [LM 2/37]. The "live" window resolves against *the current version*, and "current" is a moving target. But against any *specific* version, resolution is stable. The non-determinism is in your specification ("latest"), not in the resolution.

**Link search is stable against the docuverse state.** FINDLINKSFROMTOTHREE returns all links matching the predicate *at the time of the query*. New links get created, so two queries hours apart against "the docuverse" may differ. But against a frozen snapshot — same docuverse, same query — the result is identical.

**Refractive following across versions is deterministic per version pair.** "Links may be refractively followed from a point or span in one version to corresponding places in any other version" [LM 2/26]. The correspondence between two fixed versions is computable and fixed.

## What this means for implementers

The system must promise:

| Input | Guarantee |
|-------|-----------|
| Same link + same target version + same docuverse snapshot | **Identical bytes returned** |
| Same link + "latest version" | May vary as new versions are created |
| Same search + same docuverse snapshot | **Identical link set returned** |
| Same search at different times | May vary as new links are made |

The first and third must be bit-identical. No randomization, no ordering jitter, no implementation-defined behavior. If you cannot reproduce a citation, the archive has failed its central purpose.

## Flagging the implicit

NEED_RAW: 4/58-4/60 — The curated material presents resolution determinism as a structural *consequence* of immutability rather than an explicit promise. I do not have a verbatim Nelson quote saying "resolution is deterministic." Pages 4/58-4/60 on link search semantics ("THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS" appears at 4/60) might contain a more direct statement worth verifying against the originals.
