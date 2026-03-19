## Question 7 [nelson]

> When one document includes content that originated in another document, what relationship must the system maintain between those two documents?

## The Inclusion Relationship: What the System Must Maintain

When document A includes content originating in document B, Xanadu must maintain **six structural relationships** between them. These are not optional features — they are consequences of the architecture itself.

---

### 1. Origin Traceability (Structural, Not Metadata)

The included bytes retain their permanent I-space addresses, which encode their home document. The system fetches included content from its origin:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The I-address itself — `Node.0.User.0.Document.0.Element` — structurally encodes which document created those bytes. This cannot be stripped or severed:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

---

### 2. Ownership Preservation

The original owner retains ownership of the included content. Inclusion does not transfer ownership:

> "Document A can include Document B, even though Document B is owned by someone else." [LM 2/35]

> "Each compound document is like the other documents: it has an owner and receives royalties." [LM 2/33]

The compound document has its own owner who controls the arrangement. But the included bytes belong to whoever created them. Two ownership claims coexist without conflict — one over the arrangement (V-space), one over the content (I-space).

---

### 3. Non-Destruction of the Original

Inclusion must never alter, damage, or consume the source document:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

> "The integrity of each document is maintained by keeping the two aspects separate: derivative documents are permanently defined (and stored) in terms of the originals and the changes." [LM 2/37]

The original remains exactly as its author wrote it. Readers of the compound document can always say "Show me what this originally was."

---

### 4. Navigability Between Documents

Users must be able to traverse from included content back to its source, and from the source forward to everything that includes it:

> "Only when you step through the window — turning one glass page and going on in the next — do you reach the original that you wanted. But stepping through the window means you are now in another work." [LM 2/34]

This works in both directions:

> "As already stated, it is possible for the reader to ask to see the materials which are windowed to by a given document. However, it must also be possible for the reader to ask to see whatever documents window to the current document. Both are available at any time." [LM 2/37]

The FEBE operation `FINDDOCSCONTAINING` supports the reverse direction: "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

---

### 5. Automatic Royalty Flow

When included content is delivered to a reader, the original owner receives payment automatically:

> "In our planned service, there is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned, as part of the proportional use of byte delivery." [LM 2/43]

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

The system knows which bytes belong to whom (via I-addresses), so the royalty split is mechanical — no negotiation, no tracking, no invoicing.

---

### 6. Liveness (for Location-Fixed Windows)

The system supports two inclusion modes, and the relationship differs:

> "A quotation — an inclusion window — may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." [LM 2/37]

For location-fixed inclusions, the system must maintain a **live connection** — changes to the source propagate to the including document:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document." [LM 2/36]

---

### Why This Is Architectural, Not Policy

These six relationships are consequences of the I-space/V-space separation, not features bolted on top. When document A includes content from document B:

- A's V-space maps positions to I-addresses that live under B's ownership
- The COPY operation creates this mapping without duplicating bytes
- Fetching A's content requires resolving those I-addresses back to B's storage
- The I-address encodes B's identity structurally

The alternative — copying bytes and severing the connection — is precisely what Nelson designed the system to prevent:

> "Remember the analogy between text and water. Water flows freely, ice does not. The free-flowing, live documents on the network are subject to constant new use and linkage, and those new links continually become interactively available. Any detached copy someone keeps is frozen and dead, lacking access to the new linkage." [LM 2/48]
