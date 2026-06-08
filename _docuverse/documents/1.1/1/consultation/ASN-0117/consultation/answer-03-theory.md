## Question 3 [theory]

> Does deleting a span from one document guarantee that every other document sharing that same content through transclusion remains entirely unchanged?

# Yes — that is exactly the guarantee.

Deleting a span from one document does **not** alter any other document that has transcluded that content. This is a direct consequence of the Istream/Vstream separation: DELETE is a Vstream operation, while transclusions are anchored to permanent Istream addresses.

## The direct statement

Nelson states this explicitly:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

And the system architecture treats deleted bytes as a valid persistent state, not destruction:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

## Why this holds

**Deletion only removes the Vstream mapping.** When you "delete" a span, you remove it from the *current arrangement* of your document. The content itself remains in Istream at its permanent address, where it never changes. Other documents that transcluded the content reference those Istream addresses directly — your edit to your own Vstream cannot reach them.

This is precisely the problem transclusion was designed to solve. Because inclusion is by reference, not copy, no document depends on another's *arrangement*:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update--especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document." (2/36)

The non-destruction principle backs this at the publishing level too:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate-- without damaging the originals. This is done by inclusion links." (2/45)

## One distinction worth drawing

The guarantee covers the *content that was transcluded*. Be careful about what "unchanged" means for the two window modes:

- A **time-fixed** window references a specific version/state — it is wholly insulated from your deletion.
- A **location-fixed** ("floating in time") window is designed to *track* the source document's evolving arrangement: "in which case updates are seen automatically" (2/37). Such a window is *intended* to reflect changes in the source.

So the precise statement is: the **bytes themselves persist** and remain available to every transcluding document (4/11). A document that deliberately chose a floating window is electing to see the source's current arrangement — that is the window's purpose, not a violation of the content guarantee. The transcluded *content* is never lost or altered by the source owner's deletion; it remains addressable in Istream forever.
