## Question 1 [theory]

> Was RETRIEVEDOCVSPANSET intended to accept any document identity (total), or only an allocated document — and does the design distinguish "allocated but empty" from "no such document"?

## Short answer

Nelson never explicitly specifies the totality or error semantics of `RETRIEVEDOCVSPANSET`. The curated material defines only its *successful* behavior on a valid document, and the underlying addressing model actually pushes against making "allocated but empty" distinguishable from "no such document." So the honest answer is: the design *leans toward* treating document identity as a position in tumbler-space (conceptually total), but the spec does not draw the distinction you're asking about, and the ghost-element model suggests the two cases collapse at the storage level.

## What the spec actually says

The operation is defined purely by its return value:

> "This returns a span-set indicating both the number of characters of text and the number of links in document `<doc id>`." (4/68)

Its sibling is likewise defined only positively:

> "This returns a span determining the origin and extent of the V-stream of document `<doc id>`." (4/68)

Neither definition mentions what happens when `<doc id>` names a document that was never created. There is no specified error return, no "no such document" condition.

## Why the model resists the distinction

The deeper point comes from how documents exist at all. In Xanadu, a document is **not a stored object** — it is a ghost element, a conceptual position on the tumbler line:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links. While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it. What's stored is the contents--bytes and links." (4/23)

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." (4/23)

This matters directly. An *allocated but empty* document has zero bytes and zero links stored. An address where *nothing was ever created* also has zero bytes and zero links stored. At the level of "what is actually in storage," both look identical — a span-set of (0 characters, 0 links). The ghost-element principle is explicit that addressing is purely conceptual and storage is "purely operational," so there is no stored "document object" whose presence or absence would let the operation answer "does this exist?"

The system is even designed to *accept* references to unoccupied positions:

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." (4/23)

That bias toward accepting any address suggests the intended reading of `RETRIEVEDOCVSPANSET` is closer to **total over the address space** than to a guarded partial operation.

## The countervailing fact: baptism is real

Against pure totality, allocation is nonetheless a genuine act. `CREATENEWDOCUMENT` is described as doing something:

> "This creates an empty document. It returns the id of the new document." (4/65)

And tumbler ownership rests on "baptism" — an owner deliberately designating new numbers:

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." (4/17)

So there *is* a conceptual event ("this document now exists, owned by X") even though no content-object is stored for it. Whether the back end records that baptism in a way that `RETRIEVEDOCVSPANSET` could consult — and thereby separate "empty document I created" from "address no one ever baptized" — is exactly the point the published spec does not settle.

## Design intent (as best I can characterize it)

The architecture's instincts are: addresses are permanent and universally referenceable; documents are conceptual positions, not objects; and referencing an unoccupied position is allowed rather than an error. Those instincts favor a *total* `RETRIEVEDOCVSPANSET` returning (0,0) for anything with no content, and they make "allocated but empty" vs. "never allocated" a distinction the storage layer does not naturally express. But that is an inference from the ghost-element and tumbler principles, not a stated guarantee about this operation.

## What's missing

The precise return contract on a bad/unallocated `<doc id>` — and whether baptism is recorded distinctly from content — is not in the curated material.

NEED_RAW: 4/64-4/68 (FEBE command definitions for CREATENEWDOCUMENT and the RETRIEVEDOC* operations, to check for any specified error/empty/not-found behavior), and 4/30-4/31 (document/element address structure, to see whether an empty document has any stored marker distinct from an unoccupied address).
