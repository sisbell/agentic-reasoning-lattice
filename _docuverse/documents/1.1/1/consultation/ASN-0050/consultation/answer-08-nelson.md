## Question 8 [nelson]

> Must a removal operation produce a new version of the document, or can a document's history ever lose record of what it previously contained?

## Answer

**No, a removal operation need not produce a formal new version via CREATENEWVERSION. But a document's history can never lose record of what it previously contained. This is architecturally impossible.**

These are two distinct guarantees that operate at different levels.

---

### DELETE Does Not Require CREATENEWVERSION

In the FEBE protocol, DELETEVSPAN and CREATENEWVERSION are separate operations. DELETEVSPAN modifies the current document's V-stream directly:

> "This removes the given span from the given document." [LM 4/66]

There is no specification that DELETE must first fork a version. It operates on the document in place — but "in place" means something radically different in Xanadu than in conventional systems, because the storage model is append-only.

---

### History Can Never Be Lost

This is guaranteed by three interlocking mechanisms:

**1. I-space permanence.** DELETE only removes content from V-space (the current arrangement). The bytes themselves remain permanently in I-space:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

**2. The DELETED BYTES state.** Nelson's diagram on page 4/9 explicitly shows "DELETED BYTES" as a valid system state with the annotation:

> "(not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The phrase "awaiting historical backtrack functions" is critical — deleted content is not gone, it is *waiting to be asked for*.

**3. Append-only storage.** The entire storage paradigm rejects destructive replacement:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

> "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes; integrating them all by means of an indexing method that allows any previous instant to be reconstructed." [LM 2/15]

Every change — including every deletion — is recorded. Every previous instant is reconstructible.

---

### The Historical Trace Records All Changes

While DELETE does not create a formal version, the historical trace enfilade captures every modification. Nelson describes the document as:

> "an evolving ONGOING BRAID" [LM 2/14]

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted... and think then of successive versions of the document, at successive instants of time, as alive in this space-time vortex." [LM 2/15]

The user can then:

> "go back in time to any previous version. The user must also be able to find his or her notes, look back through time, and study its previous states." [LM 2/15]

This is not optional or best-effort. It is the fundamental storage paradigm:

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." [LM 2/16]

---

### Summary

| Question | Answer |
|----------|--------|
| Must DELETE produce a new version? | No — it is a separate FEBE operation from CREATENEWVERSION |
| Does the historical trace record the deletion? | Yes — append-only storage records every change |
| Can deleted content be recovered? | Yes — bytes remain in I-space, "awaiting historical backtrack" |
| Can a document's history lose record? | **Never** — this is architecturally impossible in append-only storage |

The deepest principle here is Nelson's rejection of "destructive replacement" [LM 2/14]. In conventional systems, deletion destroys. In Xanadu, deletion *rearranges the view*. The content endures. The history endures. Nothing is ever truly lost.
