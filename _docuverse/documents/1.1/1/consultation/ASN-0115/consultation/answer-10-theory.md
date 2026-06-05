## Question 10 [theory]

> What must the design promise about repeatability: if the same spec-set is asked for again against unchanged arrangements, must the delivered material be identical every time?

## Repeatability: the design must promise determinism

**Short answer: Yes.** The same spec-set, resolved against an unchanged arrangement, must deliver byte-identical material every time. Nelson never states this as a named "repeatability guarantee," but it is *entailed* by three guarantees he does state explicitly. Determinism is not an extra promise bolted on — it falls out of the content/arrangement separation.

### Why it follows necessarily

A retrieval is `RETRIEVEV`, which returns "the material (text and links) determined by `<spec set>`" (operations, 4/67). A spec-set is a set of V-addresses; resolving it means mapping each V-address through the document's arrangement to an I-address, then fetching the bytes stored there. Two things are fixed:

1. **Istream content is immutable.** Content at an I-address never changes; "deleted" bytes still sit at their I-address. So the *bytes* a given I-address yields are constant.

2. **The arrangement (Vstream) is the V→I mapping.** As the v-space curated source puts it, "the document IS the mapping from V-addresses to I-addresses." If the arrangement is unchanged, the mapping is unchanged.

Constant mapping + constant bytes = identical delivered material. Repeatability is the conjunction of permanence and the immutability of Istream, viewed from the retrieval side.

### The guarantees this rests on (verified Nelson quotes)

On immutable home content:
> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

On the arrangement being a separable, addressable layer:
> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." (4/11)

On part-pounce — retrieval reconstructs the same part on demand from fragments:
> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." (2/16)

> "When you 'go to' a certain part of a document, the whole document is not ready to show; yet the system gives you that part instantly, materializing it for you from the many fragments of its actual storage." (2/16)

Part-pounce only makes sense if reassembly is deterministic: pouncing on "a given part of a given version at a given time" (2/15) must yield the same result whenever the version and time are held fixed.

### The crucial qualifier: "unchanged arrangements"

The promise is conditional on the arrangement being unchanged — and Nelson's model makes that condition precise. Editing does **not** mutate an arrangement in place; it produces a *new version* with its own V-stream (versions; CREATENEWVERSION). So "the same spec-set against the same version" is always well-defined and always reproducible, because the old version's V→I mapping is never overwritten:

> "There is thus no 'basic' version of a document set apart from other versions... any arrangement of the same materials is a priori better than other arrangements." (2/19)

This is also what makes permanent citation work: a reference resolves to the same material indefinitely. As the permanence guarantee states, "any address of any document in an ever-growing network may be specified by a permanent tumbler address" (4/19). A citation that re-resolved to different bytes would void that guarantee.

### What is *not* promised

- **Identity across versions.** If the arrangement changes (an edit creates a new version), the same V-addresses may map to different I-addresses. Repeatability holds *per version*, not across edits — by design.
- **Identical link search results over time.** `FINDLINKSFROMTOTHREE` searches the whole evolving docuverse; new links from other owners can appear. Repeatability of *content retrieval* (RETRIEVEV against a fixed version) is the determinate case. Link-discovery results are determinate only against a fixed docuverse state, which the live network does not hold still.
- **Byte-for-byte transport integrity.** Nelson explicitly disclaims technical verification: delivery is "at User's risk" and the system gives "no guarantee as to the correctness or authenticity" (content-verification, 5/17–5/18). So the *logical* promise is determinism of what the spec-set denotes; it is not a cryptographic guarantee that the wire delivered it intact.

NEED_RAW: 4/67, 4/61 — Nelson does not state a named repeatability/idempotence property for RETRIEVEV in the curated sources; the determinism claim above is an architectural entailment of permanence + Istream immutability + version-based editing, not a verbatim Nelson guarantee. If you want a direct textual anchor for "same request → same bytes," the RETRIEVEV definition page (4/67) and the FEBE command overview (4/61) are where it would appear if stated.
