## Question 2 [theory]

> Did the design intend that a document's version-allocation capability exists from the moment the document is created, or that it is brought into being by the first CREATENEWVERSION operation on that document?

# Version-Allocation Capability: Inherent at Creation

The version-allocation capability exists **from the moment the document is created**. CREATENEWVERSION exercises a pre-existing capability rather than bringing one into being.

## The Universal Forking Principle

My design treats forking as a property of ownership itself, not as a special operation that must be initialized:

> "A server node, or station, has ancestors and may have possible descendant nodes. An account, too, and a document, all have possible descendants." [LM 4/19]

The phrase "all have possible descendants" is deliberate. A document, from its inception, *has* possible descendant versions — they exist as potential addresses in tumbler-space awaiting baptism.

The general principle from tumblers:

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

The moment a user owns a document, they control allocation of all sub-numbers beneath it — including version numbers.

## Versions as Subdivision of the Document Field

From the address structure:

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." [LM 4/29]

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

A version is just a sub-address under the document number. Since the document owner controls all sub-addresses from the moment of ownership, the version space is implicitly present from creation.

## Ghost Elements: Addressability Precedes Population

This is reinforced by the ghost elements principle — addresses can exist conceptually without anything being stored at them:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." [LM 4/23]

The conceptual address space under any document — including all its possible future versions — exists from the moment that document exists. CREATENEWVERSION merely populates one of those positions.

## What CREATENEWVERSION Actually Does

Per the FEBE specification:

> **CREATENEWVERSION**: "This creates a new document with the contents of document <doc id>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

Notice the operation creates *a new document* whose id *indicates ancestry*. It's exercising the parent document's pre-existing right to baptize sub-numbers. There is nothing in the operation that initializes or unlocks a "versioning subsystem" — it simply assigns one of the always-available descendant addresses.

## Why This Matters Philosophically

The first-version-creates-the-capability model would require a discontinuity: a document that cannot version, which then transforms into one that can. My design has no such discontinuity. Every owned address — every server, account, document, version — has the same forking capability the moment it comes into being. This uniformity is what makes the docuverse "all really one big forking document" [LM 4/18].

The capability is inherent in ownership. Operations like CREATENEWVERSION exercise it; they do not create it.
