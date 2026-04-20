# Link Type System

Source: Literary Machines, 4/43-4/55, 4/58

## What It Means

A **link type** is the semantic categorization of a link, specified by the **third endset** (the "three-set" or "3-set"). The type endset tells you WHAT KIND of connection exists between the from-set and to-set.

The link type system has three defining characteristics:

1. **Type is an endset like any other** - it points anywhere in the docuverse, is an arbitrary span-set, follows the same conventions as from-set and to-set

2. **Types are matched by ADDRESS, not content** - when searching for links of a type, the system matches the type endset's ADDRESS, not what is stored there

3. **Types are open-ended** - any user may define new types by choosing addresses to represent them; no schema changes, no registry, no committee

## User Guarantee

- **Address matching enables efficient search.** To find "all citation links," you specify the address that represents "citation type." The system finds all links whose 3-set includes that address. It does NOT parse content at that address.

- **Ghost types are valid.** Link types can point to addresses where nothing is stored. The type's meaning exists by convention, not by content.

- **User-definable without system changes.** Define your own types by choosing addresses. Your types work with the same search mechanism as standard types.

- **Hierarchical types possible.** The mechanism supports subtypes and supertypes. Search for upper-links finds all sub-types below.

- **Standard types by convention.** Certain common types will have standardized addresses for interoperability. But the system does not enforce this.

## Principle Served

**Extensibility without authority.** By making types arbitrary addresses rather than a fixed enum, the system allows organic growth of link semantics without central control.

**Symmetry and generalization.** All three endsets follow the same convention. The type endset gets the same power as from/to endpoints - it can be any span-set pointing anywhere.

**Search efficiency.** Address matching (not content inspection) makes type filtering fast. The quantity of non-matching links does not impede search.

## Standard Link Types

While types are open-ended, Nelson proposed standard types for common literary needs:

### Ordinary Text Links (4/53-4/54)

| Type | Purpose |
|------|---------|
| **Connection Link** | General connection between material |
| **Comment Link** | Commentary on a passage |
| **Counterpart Link** | Shows correspondence between equivalent portions |
| **Translusion Link** | Translation relationship |
| **Alternative-Version Link** | Points to alternative version |
| **Quote-Link** | Acknowledges material origin |
| **Certified Link** | Verified by authority |
| **Mail Link** | Material addressed through mail |

### Literary Links (4/54-4/55)

| Type | Purpose |
|------|---------|
| **Citation Link** | Like a footnote reference with bridge to source |
| **Vanilla Jump-Link** | Plain link from place to place |
| **Moral Jump-Links** | Distinguished from vanilla by type |
| **Suggested-Threading Links** | Suggests pathway through material |
| **Expansion Links** | Proposes expansion of text/graphics |

### Document Metadata Links (4/53)

| Type | Purpose |
|------|---------|
| **Heading Link** | Internal heading or subtitle |
| **Paragraph Link** | Points to paragraph for navigation |
| **Footnote Link** | Provides break sequence for author |

### On Standardization (4/52)

> "Standardization of a working set of link types is now a high priority, but has less priority than establishing a robust demonstration rig."

> "A TENTATIVE LISTING OF SOME LINK TYPES. Link types are open-ended, so this is not the original beginning, but a first provisional, to give the flavor of current thinking."

## Nelson's Words

> "Links are meant to be extensible for the arbitrary needs of any user. Thus the set of link types is open-ended, and indeed any user may define his or her link types for a particular purpose. This is done with a mechanism which is powerful and symmetrical." (4/43)

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." (4/44)

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." (4/44-4/45)

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." (4/45)

> "Note that this mechanism can be used for hierarchical link types, subtypes and supertypes. It is searchable for upper- and under-links, and all final data matter below; as well as for many other compound structures." (4/51)
