## Question 2 [theory]

> What identity must a forked version carry that distinguishes it from its source while preserving its lineage?

A forked version carries a **new tumbler address that extends the parent's address by adding digits to the right** — making it distinct while structurally preserving lineage as a prefix.

From `CREATENEWVERSION`:
> "This creates a new document with the contents of document <doc id>. It returns the id of the new document. **The new document's id will indicate its ancestry**." [LM 4/66]

The mechanism is forking by baptism:
> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." [LM 4/29]

**Important caveat** — Nelson is explicit that the lineage encoded in the address is *structural convention*, not a strict semantic claim about content derivation:
> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

So the identity is: **a unique tumbler address whose parent's address is a prefix**. Distinctness comes from the new digits to the right; lineage is visible in what remains to the left. The address shows ancestry, but the actual *correspondence* between content of source and fork is established separately through shared Istream addresses — that is what makes version comparison meaningful, not the address structure alone.
