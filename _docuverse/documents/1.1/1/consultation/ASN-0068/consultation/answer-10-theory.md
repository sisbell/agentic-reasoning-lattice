## Question 10 [theory]

> Must the shared-content result itself be a permanent, addressable, and linkable entity within the system?

# Yes — but with an important clarification about what "the shared-content result" actually IS

The shared content in Xanadu is not a *separate* entity produced by a transclusion operation. It IS the original content, viewed through a window. Because all content in the docuverse lives in Istream with permanent I-addresses, shared content inherits permanence, addressability, and linkability automatically — there is no special category for "transcluded" or "shared" content.

## The architectural reason

Nelson makes the distinction structural, not operational:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The shared bytes have the same I-address whether viewed in their home document or in a transcluding document. There is no second copy with a second address. The same bytes appearing in document A (transcluded) and document B (native) are *one entity* in Istream.

## All three guarantees follow

**Permanent.** Shared content lives at its home I-address, which never changes. This is the foundation of Istream:

> "Native bytes... all other bytes are obtained by... requests to their home locations." [LM 4/11]

**Addressable.** Every byte has a permanent tumbler address. Transclusion does not create a new address; it references the existing one. This is precisely why you can always ascertain origin:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

**Linkable.** Links attach to spans of bytes via their I-addresses. Anyone can link to shared content because it is just content in the docuverse:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse." [LM 4/43]

"Anywhere in the docuverse" explicitly includes shared/transcluded content.

## Why this matters

If shared content were a *separate* result-entity, several core guarantees would collapse:

1. **Attribution would break.** A separate result-entity could exist without traceable origin. The structural attribution guarantee depends on shared content keeping its original I-address.

2. **Royalty flow would break.** The cash register sits at the home document. Royalty accrues "every time a fragment is summoned" [LM 2/43 quoted in publishing.md] — which only works if the summoned fragment IS the original, not a derived copy.

3. **Version-spanning links would break.** Links "may be refractively followed from a point or span in one version to corresponding places in any other version" [LM 2/26] precisely because correspondence is computed from shared I-addresses.

4. **The "live vs dead" distinction would collapse.** Nelson is explicit: a copy is "frozen and dead, lacking access to the new linkage" [LM 2/48]. Transclusion stays live because it is not a copy — it is reference to the same permanent, addressable, linkable entity.

## The Vstream view IS addressable, but ephemerally

One nuance worth distinguishing: the *arrangement* in document A that includes B's content has Vstream positions in A. Those V-positions are addressable while they exist, but they are ephemeral — editing changes them. The permanent identity belongs to the Istream content being shared, not to the arrangement that includes it.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing." [LM 4/11]

So: **the shared content is permanently addressable and linkable via its home I-address. The Vstream position where it currently appears in a transcluding document is also addressable, but only as long as that arrangement persists.** Links that need to survive editing must attach to the Istream side — which they do automatically, because that is how links work.
