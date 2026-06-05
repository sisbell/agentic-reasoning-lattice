## Question 1 [theory]

> Is creating a document intended to be a baptismal act that necessarily registers the new address in the ownership registry (establishing the creating account as owner at the instant of creation), such that entity allocation and registry extension are coextensive?

## Short answer

Yes — in my conceptual model, creating a document *is* a baptismal act, and baptism establishes ownership at the instant of allocation. But you should be careful with the phrase "ownership registry," because I never posited a registry as a structure *separate from* the address space itself. Ownership is **structural** — encoded in the tumbler — not recorded in a side table. So allocation and ownership-establishment are coextensive *by construction*; whether allocation and "registry extension" are coextensive depends entirely on whether your implementation reifies a registry distinct from the tumbler tree, which I did not specify.

## What baptism is

Baptism is the act by which the owner of a parent number forks a new sub-number. Ownership of the new address is not conferred by a registry lookup — it is *inherited from position in the tree*:

> "The basic principle is that of owned numbers... Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." (4/17)

> "The owner of a given item controls the allocation of the numbers under it." (4/20)

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." (4/29)

So when an account creates a document, the account forks a new Document field under its own (owned) User field. The creating account is owner *because of where the address sits*, established the moment the number is baptized. `CREATENEWDOCUMENT` "creates an empty document. It returns the id of the new document" (4/65) — and that id's position in the tree already names its owner. There is no second step in which ownership is "looked up" or "assigned."

In that precise sense, **entity allocation and ownership-establishment are the same act.** This matches my framing of tumbler addressing as "the spontaneous creation of places to put things, and remembrance of where they are" (4/16) — creation and remembrance are one mechanism.

## Where the "registry" framing diverges from my intent

Two cautions:

**1. Ownership is not a registry; it is the address.** I did not design a separate ownership-registry data structure that gets "extended" on creation. The User field of the tumbler *is* the owner. If your implementation maintains an explicit registry, it is a materialization of information that is already structurally present in the address — useful, perhaps, but not something I require, and not the locus of ownership truth.

**2. Allocation is not storage.** This is the crucial nuance. A baptized document address may be a **ghost element** — addressed and owned, yet with nothing stored:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links. While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it." (4/23)

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." (4/23)

So if "registry extension" means "an entity object is now stored/persisted," then no — allocation and that kind of registration are *not* coextensive in my model. A document can be owned and addressable while remaining a ghost. What is coextensive with allocation is *ownership*, which is conceptual and structural, not *materialization*, which is optional.

## How to read your question

- "Necessarily a baptismal act" — **Yes.** Document creation is baptism; there is no non-baptismal path to a new document address.
- "Necessarily registers... establishing the creating account as owner at the instant of creation" — **Yes, in substance**, but the "registration" is the forking of the number itself; ownership is intrinsic to the resulting address, established at that instant.
- "Entity allocation and registry extension are coextensive" — **True if** by "registry" you mean the owned-number tree (the tumbler line *is* the record). **Not necessarily true if** by "registry" you mean a distinct stored-entity table, because of ghost elements: allocation/ownership can exist with no stored object.

## Caveat on precision

I never formalized "the instant of creation" or a transactional notion of "registry extension" — those are implementation contracts. My specification gives you the *principle* (owned numbers, baptism, structural ownership) and the *latitude* (ghost elements) but not an atomicity guarantee binding allocation to a registry write.

NEED_RAW: 4/16–4/23, 4/29 — to confirm there is no passage describing a registry distinct from the tumbler tree, and to check the exact wording around what `CREATENEWDOCUMENT`/baptism commits at creation time, since the precise coextensiveness claim turns on language the curated summaries may not capture verbatim.
