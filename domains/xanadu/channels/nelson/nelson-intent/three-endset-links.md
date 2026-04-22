# Three-Endset Link Structure

Source: Literary Machines, 4/42-4/47 (pages 209-214)

## What It Means

A Xanadu link is a **three-way connection** between content in the docuverse. Unlike conventional hyperlinks that connect point A to point B, Xanadu links have three components:

| Endset | Also Called | Purpose |
|--------|-------------|---------|
| **From-set** | first endset | The bytes the link is "from" |
| **To-set** | second endset, 2-set | The bytes the link is "to" |
| **Type** | three-set, 3-set | Categorizes the link |

Each endset is an **arbitrary span-set** - not a single point, but potentially multiple discontiguous regions anywhere in the docuverse.

## User Guarantee

- **Semantic directionality.** Links have a "from" and "to" with user-defined meaning. A citation goes from citing text to source. A comment goes from commentary to subject.

- **Structural bidirectional discovery.** The system indexes links by ALL three endsets. You can find links starting from any direction - what links FROM here, what links TO here, what links OF THIS TYPE.

- **User-definable types without system changes.** The type endset points anywhere. You create new link types by choosing an address to represent them. No schema updates, no registry, no committee.

- **Type by address, not content.** Search matches on the type's ADDRESS, not what is stored there. Types can be "ghost elements" - addresses where nothing is stored.

- **Links survive editing.** Because links attach to bytes (via I-addresses), not positions, they persist through insertions, deletions, and rearrangements. As long as any bytes remain at each end, the link survives.

- **Links are independent objects.** A link exists in its home document, not in the documents it connects. You can comment on someone else's content without modifying it - your link lives at your address.

## Principle Served

**The backlinks problem solved.** Traditional hyperlinks are one-way - you can follow a link, but cannot discover what links TO a page. Xanadu's three-endset structure with bidirectional indexing means EVERY link is discoverable from EITHER end (and from its type).

**Literature as interconnected system.** Nelson views all literature as a web of interconnections - quotations, citations, responses, refutations. The three-endset structure makes these connections explicit, typed, and navigable from any direction.

**Symmetry and generalization.** All three endsets follow the same convention - each is an arbitrary span-set pointing anywhere. One mechanism handles all three, and types get the same power as from/to endpoints.

**Extensibility without authority.** By making types arbitrary addresses rather than a fixed schema, the system allows organic growth of link semantics without central control.

## Why Three and Not Two?

Two endsets (from, to) establish WHAT is connected.

The third endset (type) establishes WHAT KIND of connection it is.

Without the type endset, you would have:
- No way to distinguish citations from comments from refutations
- No way to search for "all citations" vs "all comments"
- A need for system schema changes to add new link meanings
- Links that are structurally identical but semantically different

The type endset gives links their MEANING, and by making it an arbitrary address (not a fixed enum), the system allows infinite extensibility.

## The Tumbler Square

Page 4/47 shows the "Tumbler Square" visualization:

```
                    HOME
                     |
          [tumbler line]
                     |
    FROM -------- LINK -------- TO
                     |
          [tumbler line]
                     |
                   TYPE
```

The link sits at its home position (its own tumbler address). Its three endsets reach out to connect arbitrary spans on the tumbler line. This visualization emphasizes:

- Links are concrete objects with their own addresses
- Links are owned (by whoever owns the home document)
- Links reach ACROSS the docuverse (not confined to one document)
- Links can be found from any of the four "sides" (home, from, to, type)

## Nelson's Words

> "A link is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.' (What 'from' and 'to' mean depend on the specific case.)" (4/42)

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." (4/44)

> "Links are meant to be extensible for the arbitrary needs of any user. Thus the set of link types is open-ended, and indeed any user may define his or her link types for a particular purpose." (4/43)

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." (4/44-4/45)

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." (4/45)

> "ENDSETS MAY POINT TO SPANS ANYWHERE IN THE DOCUVERSE" (4/45)

> "A link's home (any home) is an element located on one side; and its three endsets map to the other sides." (4/46)

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)
