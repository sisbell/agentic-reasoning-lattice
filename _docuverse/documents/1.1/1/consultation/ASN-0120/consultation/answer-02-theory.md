## Question 2 [theory]

> What must the system record about each endset a link ties together, and must those recorded endsets remain immutable for the life of the link?

## What the system records about each endset

A Xanadu link ties together **three** endsets, and the system records each one identically: as an **arbitrary span-set of tumbler addresses** pointing anywhere in the docuverse.

- **From-set** — the bytes the link is "from"
- **To-set** — the bytes the link is "to"
- **Type (three-set)** — what categorizes the link

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." (4/42)

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." (4/43)

The recording is symmetrical across all three, and each maps onto the universal address space:

> "There is a universal address space, the tumbler line... We may visualize a link's endsets as mapping to it." (4/45)

The crucial detail is *what* the spans address: **bytes (Istream content), not positions**. A link is recorded as a strap between bytes, not as a pointer to a character offset:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." (4/42)

## Must the recorded endsets remain immutable?

**Yes — and this immutability is exactly what delivers the survivability guarantee.** Two distinct facts underlie this:

**1. The references point to permanent content.** Endsets address Istream bytes, whose I-addresses never change. Editing a document alters its Vstream arrangement, but the bytes the endset refers to retain their permanent identity. So the recorded references stay attached to the same content even as documents are edited:

> "This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." (4/42)

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." (4/43)

Because content "deletion" is a Vstream-only operation (Istream content persists per `delete-semantics.md` / `link-survivability.md`), the bytes an endset references are never actually destroyed — the recorded endset remains valid for the life of the link.

**2. There is no operation to alter an endset.** The FEBE protocol provides `MAKELINK` to create a link with its three endsets, `RETRIEVEENDSETS` to read them back, and search operations — but **no command to modify an existing link's endsets** (see `operations.md`). A link can be deleted by its owner (`link-deletion.md`), but its endsets are fixed at creation. This parallels how links keep their addresses permanently:

> "The links designated by a tumbler address are in their permanent order of arrival." (4/31)

---

**One caveat on what's explicitly stated vs. inferred:** Nelson explicitly establishes (a) that endsets are recorded as span-sets of byte-addresses and (b) that links survive editing because of this. The claim that endsets are *immutable for the link's life* follows from the survivability mechanism plus the **absence of any endset-modifying operation** in the protocol — Nelson does not use the word "immutable" for endsets directly. If you want to confirm no such modify command exists in the full XU.87.1 command set, the relevant pages are:

NEED_RAW: 4/61-4/70 (full FEBE command listing, to confirm no endset-mutation operation)
