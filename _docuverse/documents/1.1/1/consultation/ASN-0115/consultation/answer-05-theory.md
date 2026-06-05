## Question 5 [theory]

> If the same underlying content appears in two of the requested spans through transclusion, must the system reveal that the two deliveries are the identical content, or may it return them as if unrelated?

## Short answer

The system cannot return the two deliveries as genuinely unrelated content. Their identity is **structural**, not optional metadata: transcluded content shares the *same Istream address* as its source, and that shared address *is* the content's identity. The relationship is therefore always preserved and always ascertainable — to sever it would be to make a copy, which is exactly what Xanadu's reference-not-copy model forbids.

## Why the identity cannot be hidden at the system level

Content identity in Xanadu is based on creation, not value. Independently-typed identical text gets *different* I-addresses; transcluded content gets the *same* I-address:

> "The virtual byte stream of a document may include bytes from any other document." (4/10)

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

Because both spans resolve to the same native home, the attribution guarantee applies to every byte of both deliveries:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." (2/40)

The word **"at once"** is the operative commitment: the home document of any character is always ascertainable. A system that returned the two spans as if unrelated would be claiming two independent origins for bytes that have one — contradicting this guarantee.

## The relationship is queryable, not merely incidental

Nelson provides an explicit operation to surface exactly this:

> **FINDDOCSCONTAINING** — "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." (4/63)

So the shared-origin relationship between the two spans is not something the system *may* discard — it is something a user can directly ask for and receive. Correspondence in Xanadu "emerges from shared I-addresses" and is structural, "computed from the I-addresses themselves," not from separate tracking that could be omitted.

## The boundary: delivery vs. display

There is a distinction worth flagging:

- **At the storage/protocol level:** The identity is inviolable. Both spans carry their I-addresses; the shared origin is preserved and ascertainable. The system *may not* destroy or falsify this — that would be copying, and "any detached copy someone keeps is frozen and dead" precisely because copying severs the live connection (transclusion).

- **At the front-end/display level:** Whether the two appearances are *visually highlighted as identical* is a presentation choice. Nelson treats highlighting of correspondence as a front-end function ("highlighting the corresponding parts is a vital aspect of intercomparison," 3/13), so a front end is not obligated to draw attention to the coincidence in every view.

But that display latitude does not let the system return the deliveries "as if unrelated" in any binding sense: the underlying identity travels with the content and remains queryable. The front end may choose not to *emphasize* the relationship; it cannot make the bytes genuinely unrelated.

## Bottom line

The system **must preserve and make ascertainable** that the two deliveries are the same content — that is the direct consequence of identity-by-I-address (4/10–4/11), the attribution guarantee (2/40), and FINDDOCSCONTAINING (4/63). It may not represent them as independent content. What it *may* do is leave it to the front end whether to visually surface the coincidence in a given view.

NEED_RAW: 4/63, 4/67, 4/70 — to confirm whether RETRIEVEV's returned material carries I-address provenance inline in a single delivery, versus the relationship being recoverable only via a separate FINDDOCSCONTAINING / SHOWRELATIONOF2VERSIONS call. This distinguishes "revealed in the delivery itself" from "revealed on request," which my answer treats as the meaningful boundary.
