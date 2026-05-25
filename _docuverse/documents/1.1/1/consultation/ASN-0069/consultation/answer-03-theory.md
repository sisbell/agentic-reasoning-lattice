## Question 3 [theory]

> Must the act of forking be invisible to the source document's owner, or does the design require some form of acknowledgment?

The design requires **neither invisibility nor explicit acknowledgment**. Forking is permissionless by construction, but its results are structurally discoverable.

**For pure tumbler-space forking** (creating sub-addresses), no other owner is involved—you can only fork under addresses you already own:

> "The owner of a given item controls the allocation of the numbers under it." (4/20)

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." (4/17)

**For derivative documents that fork from another's work via transclusion**, the design is similarly permissionless. The publishing contract pre-grants this right:

> "Accessibility and free linking make a two-sided coin... each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract." (copyright)

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals. This is done by inclusion links." (2/45)

**However, the act is not invisible either.** Three structural features ensure the source owner can know:

1. **Bidirectional link discovery**: "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'—and be shown all these outside connections without appreciable delay." (2/46)

2. **Automatic royalty flow**: When the derivative is read, "the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." (2/45)

3. **Address-encoded ancestry**: CREATENEWVERSION returns "the id of the new document. The new document's id will indicate its ancestry." (4/66)

The philosophy: **permissionless creation with structural accountability**. The source owner cannot prevent forking, is not actively notified, but can always discover it and is automatically compensated.
