## Question 4 [theory]

> Was Nullify intended to be a substrate-absolute operation (single-tuple scope unconditional) or a layer-conditional operation whose guarantees rest on caller discipline?

"Nullify" does not appear in the curated sources from Literary Machines. The 17 FEBE commands Nelson specified in XU.87.1 are INSERT, DELETEVSPAN, COPY, REARRANGE, APPEND, MAKELINK, FINDLINKSFROMTOTHREE, FINDNEXTNLINKSFROMTOTHREE, RETRIEVEENDSETS, CREATENEWDOCUMENT, CREATENEWVERSION, SHOWRELATIONOF2VERSIONS, RETRIEVEV, RETRIEVEDOCVSPAN, RETRIEVEDOCVSPANSET, and FINDDOCSCONTAINING (see operations.md). No "Nullify" command is listed.

The terminology "substrate-absolute" / "layer-conditional" is also project-specific formalization language, not Nelson's vocabulary.

That said, I can speak to what design intent **would** constrain a Nullify-like operation, based on Literary Machines:

**1. Istream is sacrosanct.** Nothing Nelson specified ever removes content from Istream. DELETE is explicitly a Vstream operation:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" — 4/9

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." — 4/11

**2. Non-destruction is the conservation law.** From 2/45:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate--without damaging the originals."

**3. Safety is built into storage, not enforced by callers.** From 2/13-2/14:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version."

The implication: I designed against the model where correctness depends on callers being disciplined. The substrate itself preserves history.

**Inference about Nullify:** If Nullify is meant to remove or invalidate a tuple at the substrate level *unconditionally*, that violates the append-only Istream principle. If it is meant to be a Vstream/view-level operation whose semantics depend on layer context (which tuples are addressable in which version), that is consistent with how DELETE works. My design intent points strongly toward the **layer-conditional** interpretation — but with the caveat that "caller discipline" isn't quite right either. The substrate should make destructive interpretations *impossible*, not merely *contractually forbidden*.

NEED_RAW: 4/61-4/79 (full FEBE/BEBE protocol section) to confirm no Nullify-like primitive exists beyond what's in operations.md, and to check whether any operation has the substrate-absolute character implied by the question.
