## Question 5 [theory]

> In the design, does a version address [N,0,U,0,D,k] require the base document [N,0,U,0,D] (or prior versions) to exist, or can versions be allocated independently of the base's existence?

# Version Address Independence

The design has a nuanced answer that depends on whether you mean *conceptual addressability*, *stored content*, or *operational allocation*.

## Conceptually: No "base" is privileged

There is no architectural distinction between a "base document" and its versions. All versions are peer arrangements:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

And on the addressing itself:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

The address `[N,0,U,0,D,k]` does not encode that `[N,0,U,0,D]` is its "parent" in any stored-object sense — it just sits one level deeper in tumbler-space.

## Storage: Ghost elements make the base optional

Documents can exist as positions in tumbler-space without anything stored at them:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links. While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it." [LM 4/23]

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." [LM 4/23]

So `[N,0,U,0,D]` can be a ghost element while `[N,0,U,0,D,k]` carries actual content — both are addressable positions; only one is "occupied."

## Ownership/allocation: Baptism flows down the tree

Allocation still proceeds through the forking/ownership chain:

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

So conceptual ownership of the `D` position is what authorizes baptism of `D.k`. But ownership of a position is not the same as having content stored there.

## Operationally: CREATENEWVERSION takes an existing doc_id

The FEBE protocol does require a source document at version-creation time:

> "CREATENEWVERSION ... This creates a new document with the contents of document <doc id>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

So *via this command*, a version is forked from an existing addressable document. But Nelson does not say the source must itself have stored bytes — only that it must be a designated doc_id whose ancestry the new version inherits.

## Summary

| Layer | Does `[N,0,U,0,D]` need to "exist"? |
|---|---|
| Address space | No — `D` is a position; `D.k` extends it whether or not `D` has content [LM 4/23] |
| Storage | No — `D` may be a ghost element [LM 4/23] |
| Semantics | No — there is no privileged "base" version [LM 2/19, 4/29] |
| Ownership chain | The `D` position must be **owned** for baptism of `D.k` to be authorized [LM 4/17, 4/20] |
| FEBE operations | CREATENEWVERSION requires a doc_id argument [LM 4/66] |

The design intent is that versions are independently addressable — `D` is not a "parent object" that must materialize before `D.k` can be allocated. What is required is the ownership chain that authorizes baptism, not stored content at the intervening positions.

NEED_RAW: none — the curated sources cover this directly. If implementation-level constraints in XU.87.1 (e.g., whether the back-end refuses CREATENEWVERSION against a ghost doc_id) are needed, that would require pages 4/65-4/70 in the raw.
