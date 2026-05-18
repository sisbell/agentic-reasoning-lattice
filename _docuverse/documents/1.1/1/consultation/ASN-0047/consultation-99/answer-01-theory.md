## Question 1 [theory]

> Does Literary Machines describe or sanction versioning from a document address that is structurally valid but has not been allocated as an entity, and if so what use case does it serve?

# Versioning from Unallocated Addresses

Based on the curated sources from Literary Machines, **I do not describe or sanction versioning from a structurally valid but unallocated address**. The CREATENEWVERSION operation as specified requires an existing document as its source.

## What the protocol actually specifies

CREATENEWVERSION operates on an allocated document:

> "This creates a new document with the contents of document <doc id>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

The operation takes `<doc id>` as input — an existing, allocated document — and produces a new id derived from it. There is no variant that operates on a structurally valid address that nothing currently occupies.

## Ghost elements: linking, not versioning

The closest analogous capability I describe is the **ghost element** — but its sanctioned use is linking, not versioning:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

> "However, these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." [LM 4/23]

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." [LM 4/23]

Ghost elements are virtually present *for linking purposes*. I do not extend this to versioning. A link traverses to an address; a version is *derived from* something — and you cannot derive from what does not exist.

## Address structure does not imply derivation

I am explicit that the address relationship between a document and its versions is structural convention, not a derivation claim:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

This cuts against any reading that would let you "version from" an address simply because the address is structurally valid. The address arrangement is bookkeeping; the derivation relationship comes from the actual CREATENEWVERSION operation acting on existing content.

## Allocation requires baptism, not structural validity

New addresses are not auto-existent because they are well-formed; they must be **baptized** by an owner:

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

An unallocated address has not been baptized. To version *from* it presumes content that no one has yet brought into being.

## Verdict

I sanction:
- Linking *to* ghost elements (unallocated addresses with no stored object)
- Creating new versions *from* existing allocated documents
- Forking addresses under owned numbers via baptism

I do not sanction or describe versioning from a structurally valid but unallocated address. The use case is not one I take up in Literary Machines.

NEED_RAW: 4/29, 4/65-4/68 — to confirm CREATENEWVERSION has no documented variant for unallocated source addresses, and to verify the "accidental extension... no specific relationship of derivation" passage is not qualified elsewhere in the protocol section.
