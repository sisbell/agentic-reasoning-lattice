## Question 3 [theory]

> What relationship must the new version's identity bear to the source's identity, given your stipulation that a version's ancestry be readable from the identity itself?

The relationship is **descent by forking**: the new version's identity must be a *daughter* of the source's identity — a sub-address obtained by subdividing the source's own number, so that the source's tumbler stands as the leading portion (the prefix) of the version's tumbler. That is the whole trick by which ancestry becomes legible: you read the lineage by reading the nested digits from left to right.

When CREATENEWVERSION runs, this is exactly the promise I attach to it:

> "This creates a new document with the contents of document <doc id>. It returns the id of the new document. The new document's id will indicate its ancestry." (4/66)

The id "indicates its ancestry" because it is not a freshly minted, unrelated number — it is baptized *under* the source. The version lives in the Document field as a new subfield:

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." (4/29)

And the act of subdivision is the ordinary forking mechanism, governed by ownership:

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." (4/17)

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." (4/20)

So the formal requirement is: **the source's identity must be a proper prefix of the new version's identity, the version being a digit-extension to the right of the source.** Because every CREATENEWVERSION subdivides the *exact* thing it was made from — whether that thing is an original document or itself a prior version — the chain of nested digits records the full derivation path. Each level of nesting is one generative step. Read the whole address and you have read the genealogy.

Note what is *not* encoded: time.

> "Note that 'time' is not included in the tumbler. Time is kept track of separately." (4/18)

The address gives you the *tree* of descent, not the clock. Which version is newer, and the ordering among siblings, are matters tracked separately; the tumbler tells you only who was forked under whom.

**One honest caution about how much the numbers can be made to mean.** The forking apparatus is a generic allocation device — the same mechanism mints daughter documents and versions alike — and I have been careful to say that, structurally, the subdivision is not self-interpreting:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." (4/29)

Read those two passages together and the precise situation is this: the tumbler structurally guarantees *allocation lineage* — that this number was baptized under that one. The *semantic* claim "this is a version derived from that document" is supplied by the operation that performed the subdivision (CREATENEWVERSION), not by the digits in isolation. My stipulation that "the id will indicate its ancestry" is therefore a convention deliberately laid over the addressing mechanism: I require the operation to subdivide the source, so that the allocation lineage in the address coincides with the line of derivation. The numbers carry the genealogy because the operation is disciplined to make them do so — not because a string of digits, on its own, knows it is a version.

This is consistent with the larger picture I intend, in which the whole docuverse is one nested forking structure:

> "So the docuverse is all really one big forking document." (4/18)

A version is simply one more fork — placed under its parent precisely so that the parent can always be read back out of the child.
