## Question 6 [nelson]

> If a document transcludes content from another document and that transcluded region is split by a cut point during rearrangement, does the transclusion relationship survive intact for each resulting piece?

## Yes — the transclusion survives intact for each piece

The answer follows directly from the Istream/Vstream architecture. Let me trace through the mechanics.

### What transclusion actually is

A transclusion is not a pointer or a reference object — it is a **Vstream-to-Istream mapping**. When document B transcludes bytes from document A, B's Vstream contains entries that map to A's Istream addresses. Those bytes are "non-native" to B:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The transclusion relationship IS the I-address identity. There is no separate "transclusion record" that could be broken — the relationship is encoded in the addresses themselves.

### What REARRANGE does

REARRANGE is a **pure Vstream operation**. It transposes regions of the virtual byte stream:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3..." [LM 4/67]

V-addresses shift. I-addresses do not. Nelson is explicit about this separation:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

### The split scenario

Suppose document B transcludes a 100-byte region from document A (I-addresses A.1 through A.100), appearing at V-positions 50–149 in B. A REARRANGE with a cut point at V-position 80 splits this into two Vstream regions:

- **Piece 1**: still maps to I-addresses A.1–A.30
- **Piece 2**: still maps to I-addresses A.31–A.100

Each piece retains its I-address mapping to A's content. The bytes are still "native elsewhere" — still fetched from their home locations in A. The system still knows their origin because:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

FINDDOCSCONTAINING would still return document A for both pieces, because:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

### Why this must be so

The entire architecture is designed to make Vstream operations non-destructive to content identity:

- **Istream is permanent**: content at an I-address never changes
- **Vstream is ephemeral**: V-addresses shift freely during editing
- **Identity is structural**: the I-address encodes the home document in its tumbler fields (Node.0.User.0.Document.0.Element)

DELETE confirms the same principle from the other direction:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

If deletion doesn't sever transclusion for *other* documents, rearrangement certainly doesn't sever it within the *same* document. Both are Vstream operations that leave I-address identity untouched.

### Summary

The transclusion relationship survives because it is not a fragile pointer that a cut can sever — it is the **identity of the bytes themselves**. Each byte's I-address permanently encodes its origin. REARRANGE changes where bytes appear in the Vstream; it cannot change what they are or where they came from. After the split, you have two Vstream regions, each still composed of bytes whose home is the source document, each still fetchable from that source, each still attributable and royalty-generating.
