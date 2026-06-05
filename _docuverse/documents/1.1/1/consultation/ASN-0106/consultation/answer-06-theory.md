## Question 6 [theory]

> Must the identity of each returned fragment remain traceable to its exact place in the document, so the reader knows where within the whole each piece belongs?

Yes — this is a core design guarantee, and it operates on two distinct axes: *where the fragment lives* (its permanent identity/origin) and *where it belongs in the document you're reading* (its position in the current arrangement). Both must remain traceable for every returned fragment.

## Where each piece belongs within the whole

The system reconstructs a document on demand from scattered fragments — Nelson's "part-pounce" — yet the reader always perceives a coherent ordered whole. The key is that each fragment occupies a definite ordinal position in the document's virtual byte stream (Vstream):

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

So even fragments fetched from other documents have a fixed place in the sequence the reader sees. The V-address *is* "where this byte appears in the document right now" (see `i-space-v-space`). When you pounce on a part, "it seems to be there, having been constructed while you wait" (2/16) — assembled from fragments but presented in correct order.

## Why the fragment's exact place is always knowable

Nelson makes this an explicit, user-facing guarantee — you never lose track of where you are or what you are looking at, no matter how deeply fragments are assembled from elsewhere:

> "This world nevertheless remains simple in design. The virtuality is simple in structure and repeats in layers. You always know where you are, and can at once ascertain the home document of any specific word or character." (2/40)

This couples the two axes: *where you are* (position within the whole) and *the home document of any specific word or character* (origin identity). Both are traceable for every fragment.

## Identity is structural, not metadata

The fragment's origin cannot be severed because retrieval itself depends on it. Each byte carries a permanent Istream address whose Document field encodes its home:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

To deliver a non-native fragment, the system *must* request it from its home — so the connection to origin is intrinsic to the act of assembly, not an attachable label (see `origin-traceability`, `transclusion`).

## Position is stable even as the document changes

A fragment's place is well-defined at any moment, and links to it survive rearrangement because they bind to the bytes themselves, not to positions:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

## Summary

The answer is **yes, necessarily**. Every returned fragment is traceable along both axes:

- **Place within the whole** — its V-address gives its ordinal position in the document's current arrangement, so "you always know where you are" (2/40), even though the whole was pounced together from scattered pieces (2/16).
- **Identity/origin** — its I-address structurally encodes the home document, so you "can at once ascertain the home document of any specific word or character" (2/40), because non-native bytes are fetched "to their home locations" (4/11).

This dual traceability is not an optional feature but a foundation of Nelson's "virtuality": the reader experiences one coherent document while the system preserves, for every piece, both where it belongs and where it came from.
