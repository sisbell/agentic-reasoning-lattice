## Question 5 [theory]

> What guarantee does the design make that the same address, read at two different times, yields content that is bit-for-bit identical?

## The Guarantee: Istream Immutability

The guarantee comes from Xanadu's separation of **two address spaces**, and it belongs specifically to the **Istream (Invariant Space)** — not the Vstream.

### Istream addresses are permanent and immutable

Content lives permanently at an Istream (I-) address, and that address always returns the exact same bytes. This is the core promise:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

The mechanism behind this is **append-only storage**. Nothing is ever overwritten:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." (2/14)

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." (2/14)

Because storage is append-only and addresses are never reused, an I-address read today and read years from now resolves to the identical bytes. "Deleted" content is still present at its I-address (it is merely dropped from the current Vstream arrangement), and links to it still resolve.

### Why this is an *address* guarantee, not just a *storage* guarantee

Tumbler addressing ensures addresses are never invalidated as the docuverse grows:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." (4/19)

So both halves of the guarantee hold: the address stays valid forever, *and* the content at it never changes.

### Critical distinction: this applies to I-addresses, NOT V-addresses

The bit-for-bit guarantee does **not** apply to a document's Vstream position. Vstream addresses change as the document is edited:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

In other words: "position 5 in the current document" may yield different content after editing; but the underlying **I-address** of any given byte always yields that same byte. Links survive editing precisely because they attach to immutable I-addresses, not to shifting V-positions.

### Important caveat: trust-based, not cryptographically verified

Nelson provides **no cryptographic mechanism** (hashing, signing, tamper detection) to *prove* bit-for-bit identity. The guarantee is architectural and contractual — it rests on append-only storage and on trusting the licensed Storage Vendor, not on mathematical verification. As the design note `content-verification.md` documents:

> "User acknowledges that all material on the network is stored by users under similar arrangements to User's own, without verification or assurance of truth, authenticity, accuracy, usefulness or other beneficial character of such materials." (5/17)

So the design *guarantees* immutability as an invariant of the storage model, but does not provide a technical means for a reader to independently confirm that the bytes were not tampered with in transit or at a compromised vendor.

---

**Summary:** The same address yields bit-for-bit identical content because Istream is append-only and Istream addresses are permanent and immutable — content at an I-address never changes, and the address is never reused or invalidated (2/14, 4/11, 4/19). This holds for I-addresses, not editable V-positions. The guarantee is a design/contractual invariant, not a cryptographically verifiable one (5/17).
