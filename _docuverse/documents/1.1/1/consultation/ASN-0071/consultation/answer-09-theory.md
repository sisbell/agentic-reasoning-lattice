## Question 9 [theory]

> What guarantee governs the result when the specified content spans material drawn from many original sources?

When content spans material drawn from many original sources, several interlocking guarantees govern the result. The architecture is designed so the user experiences unity while the system preserves origin.

## The Coherence-Origin Duality

The fundamental guarantee is that **distribution is invisible to the user, but origin is always recoverable**. The result appears as one coherent stream, yet every byte traces to its home.

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The user sees a continuous result. The system handles fetching invisibly:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

## Per-Byte Attribution

No matter how many sources contribute, attribution operates at byte granularity:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This is structural, not metadata. It cannot be stripped, because every byte carries a permanent Istream address whose Document field IS the proof of origin.

## Instantaneous Assembly (Part-Pounce)

The result materializes on demand from wherever its fragments live:

> "When you 'go to' a certain part of a document, the whole document is not ready to show; yet the system gives you that part instantly, materializing it for you from the many fragments of its actual storage." [LM 2/16]

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." [LM 2/16]

## Proportional Royalty

When a result combines material from multiple owners, payment flows automatically to each in proportion to what they contributed:

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

> "There is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned, as part of the proportional use of byte delivery." [LM 2/43]

This is the deepest commitment: the result is not an aggregation of orphaned text. Each byte remembers who created it and pays them when delivered.

## Live, Not Frozen

Because the result is assembled from references rather than copies, included material remains alive — it is the original, not a duplicate. This is the central virtue of transclusion over copying:

> "The free-flowing, live documents on the network are subject to constant new use and linkage, and those new links continually become interactively available. Any detached copy someone keeps is frozen and dead, lacking access to the new linkage." [LM 2/48]

## Cross-Origin Discovery

The dual operation — finding all documents that contain a given span — is also guaranteed regardless of where native copies sit:

> "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." [LM 4/63]

## Summary

The governing guarantee is that **a multi-source result preserves per-byte origin while presenting seamless unity** — and that origin drives both attribution (who wrote this character?) and economics (who is paid for delivering it?). The user is never required to know where the pieces come from to read them, but can always discover where any piece came from, and the original owner of any piece is always compensated for its transmission.
