## Question 9 [theory]

> Must the boundaries of the deleted span be exactly reflected in how the remaining content is renumbered or re-positioned within the document?

## Answer

Yes — but only in **Vstream** (the document's current arrangement), not in Istream (permanent content identity). The distinction is the whole point.

### Vstream: the gap closes exactly

A document's V-addresses are a dense, contiguous sequence — there are no gaps. When you delete a span, the content following it shifts down by exactly the width of the deleted span, so the boundaries of the deletion are precisely reflected in how the remaining content is re-positioned.

Nelson states this explicitly for the inverse operation, INSERT:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66)

DELETEVSPAN is the symmetric case. Nelson describes it tersely —

> "This removes the given span from the given document." (4/66)

— and the V-stream's density guarantee (addresses are "the byte position in the current ordering of bytes," 4/30) means removal must re-sequence the trailing content downward by exactly the span's length. The deleted span's boundaries determine, exactly, the amount every following byte's V-address decreases.

### Istream: nothing is renumbered or re-positioned

Critically, the content's permanent I-addresses do **not** change. "Deletion" is a Vstream operation; the bytes remain in Istream. Nelson:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

And the deleted bytes themselves persist:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

Because links attach to the bytes (their I-addresses), not to V-positions, this re-positioning does not disturb them:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

### Summary

| Aspect | Re-positioned by the deletion's boundaries? |
|--------|---------------------------------------------|
| Vstream addresses of trailing content | **Yes** — shift down by exactly the span width (gap closes) |
| Istream addresses of remaining content | No — permanent, never renumbered |
| Deleted bytes | No — persist in Istream, recoverable via backtrack |
| Links | No — stay attached to bytes (I-addresses) |

So the deleted span's boundaries must be exactly reflected in the *virtual* renumbering of the document (the trailing content closes the gap precisely), while the underlying content identity and any links are untouched.

---

One caveat on sourcing: Nelson gives a verbatim "shift by exactly the length" statement only for INSERT (4/66); the symmetric exact-gap-closing for DELETE is inferred from the Vstream density property and the terse DELETEVSPAN definition rather than from an explicit symmetric quote. If you want Nelson's exact treatment of DELETE's effect on following V-addresses confirmed at the source: NEED_RAW: 4/66
