## Question 1 [theory]

> When a user "edits" a link, what must the system guarantee about the original link's continued existence and addressability?

# What Must Be Guaranteed When "Editing" a Link

## A preliminary observation

Nelson's FEBE protocol does NOT include an "edit link" operation. The 17 commands of XU.87.1 include `MAKELINK`, but no `EDITLINK` or `MODIFYLINK`. Link operations are:

- `MAKELINK` — create
- `FINDLINKSFROMTOTHREE` — search
- `FINDNUMOFLINKSFROMTOTHREE` — count
- `FINDNEXTNLINKSFROMTOTHREE` — paginate
- `RETRIEVEENDSETS` — retrieve

So "editing a link" is not a primitive in Nelson's specification. Whatever a front-end calls "editing a link" must be implemented in terms of these primitives — which means creating a new link, and possibly deleting (logically) the old one.

NEED_RAW: 4/61-4/70 (FEBE command list, verification that no EDITLINK exists)

## What the non-destruction principles require

Whatever "edit" means at the user level, the system must guarantee:

### 1. The original link's tumbler address remains valid forever

Links have permanent addresses based on creation order. Address `N.0.U.0.D.V.0.2.755` always refers to "the 755th link to which the document is home" [LM 4/31]. This is non-negotiable:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

Deleting link 2.5 does not renumber 2.6 through 2.N. Editing must not do so either.

### 2. The original link remains historically retrievable

If "editing" logically supersedes a link, the prior state enters the same regime as deleted links:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The original endsets must be reconstructible via historical backtrack — they are not destroyed, only made "not currently addressable" in the current view.

### 3. The original link persists in other versions

Nelson explicitly addresses this for byte deletion, and the same logic applies to links:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

If any other version of the document still references the original link as it was, that link's original state must remain intact in those versions.

### 4. Modifications must not damage originals

This is Nelson's most general non-destruction guarantee:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate-- without damaging the originals." [LM 2/45]

A link is an owned object with its own tumbler address. The same guarantee that protects documents protects links.

## How "editing" must be implemented

Given the FEBE primitives, "editing a link" must operationally mean:

1. Create a new link with the desired endsets (`MAKELINK`)
2. Optionally mark the old link as superseded or delete it (logically — preserving history)

The user-facing experience may LOOK like mutation, but the underlying reality is **append-only**:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes flow into the storage system, filed, as it were, chronologically." [LM 2/14]

## The core guarantee

The original link, at its original tumbler address, with its original three endsets (from-set, to-set, type), must remain reconstructible from the system's storage forever. Its current addressability in the live view may change; its identity and historical accessibility may not.

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." [LM 2/16]

This applies to past states of links as much as to past states of any other content.
