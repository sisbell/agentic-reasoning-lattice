## Question 4 [nelson]

> When a user rearranges content within a document, what must remain invariant about the content's permanent identity — its bytes, its origin, its order of arrival?

## What Remains Invariant Under Rearrangement

Rearrangement is a **pure V-space operation**. It changes the document's current arrangement (the virtual byte stream) but leaves three things absolutely untouched:

### 1. The Bytes Themselves (I-Space Content)

Content at an I-space address is immutable. Rearrangement changes *where* bytes appear in the document's virtual stream, not *what* those bytes are or *where they permanently live*.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control." [LM 4/11]

The I-space is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Nothing in I-space is overwritten, moved, or modified by a rearrangement.

### 2. The Origin (Encoded in the I-Address)

Every byte's permanent I-address has the form `Node.0.User.0.Document.0.Element` [LM 4/26]. This encodes *which server*, *which account*, *which document*, and *which element position* the byte was born into. Rearrangement cannot alter this.

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

Attribution is structural — it is the address itself, not metadata attached to the address. No V-space operation can sever it.

### 3. The Order of Arrival in I-Space

Bytes are appended to I-space in the order they were created. Their I-addresses reflect this chronological sequence permanently. V-space rearrangement changes the *presentation order* but never the *creation order*.

Nelson makes this explicit for links, which have an even stricter constraint:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

For bytes, the I-space position is similarly fixed at creation time. The V-space is the only thing that moves:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The "constantly changing" address here is the V-address (position in current arrangement). The I-address — the byte's permanent identity — never changes.

---

## What DOES Change

Only V-space is affected:

- **V-addresses shift.** After rearrangement, the same byte may have a different position in the virtual byte stream.
- **The V→I mapping changes.** The document's arrangement — which I-space bytes appear at which V-space positions — is rewritten.

The REARRANGE operation transposes two regions:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." [LM 4/67]

This is purely a remapping of V-space over the same I-space content.

---

## Why This Matters: Link Survivability

The separation is not academic — it is what makes links survive editing:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

Links point to I-space (bytes), not V-space (positions). Rearrangement moves bytes around in V-space but cannot disturb the I-space addresses that links reference. Therefore rearrangement cannot break any link.

---

## Summary

| Property | Invariant under rearrangement? |
|----------|-------------------------------|
| I-space bytes (content) | **Yes** — immutable, append-only |
| I-space address (identity) | **Yes** — permanent, encodes origin |
| Order of arrival in I-space | **Yes** — chronological, never reordered |
| V-space position | **No** — this is what rearrangement changes |
| V→I mapping | **No** — the document's arrangement is rewritten |
| Links to the content | **Survive** — they point to I-space, not V-space |
