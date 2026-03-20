# Endsets

Source: Literary Machines 4/42-4/47 (pages 209-214)

## Semantic Intent

### What It Means

An **endset** is what a link connects to - an arbitrary collection of bytes (spans) that can be anywhere in the docuverse. Links have three endsets: the from-set, the to-set, and the type (called the "three-set"). Each endset can contain multiple spans pointing to different locations.

The key insight is that endsets are not single points or single documents - they are *sets* of arbitrary spans. One end of a link can touch bytes scattered across multiple documents. This generalization from "point-to-point" to "set-to-set" is fundamental to how Xanadu links survive editing and express complex relationships.

### User Guarantee

- **Endsets are arbitrary collections.** A from-set or to-set is not limited to a single span - it can be a discontiguous set of bytes anywhere in the docuverse.
- **Endsets map to the universal address space.** Every endset maps to positions on the tumbler line, making all connections traceable and searchable.
- **The type is also an endset.** Link types follow the same convention as from-set and to-set - the "three-set" is an arbitrary endset pointing anywhere, even to addresses where nothing is stored ("ghost elements").
- **Endsets enable survivability.** Because links attach to spans of bytes rather than positions, links survive as long as any bytes remain at each end.

### Principle Served

**Symmetry and generalization.** Nelson generalizes the link structure by treating all three parts (from, to, type) identically - each is an arbitrary endset. This symmetrical design means the system needs only one mechanism for all three.

**Flexibility over rigidity.** By allowing endsets to be arbitrary collections rather than single pointers, links can express relationships that would be impossible with simple point-to-point connections - a critique that touches three separate passages, or a type defined by multiple spans.

**Address-based search.** The type endset particularly benefits from this design. Searches match on the *address* of the type, not its contents. This means link types can point to "ghost elements" - addresses where nothing is stored - and still work perfectly for categorization.

### How Users Experience It

- Create a link whose from-set touches multiple non-adjacent passages (because the connected idea spans several spots)
- Define your own link types by pointing to any address - even one you've never written to
- Find all links of a type by searching for that type's address, regardless of what's stored there
- Have links survive editing because they attach to bytes, not positions - as long as some bytes remain, the connection persists
- Search for links by constraining any combination of the three endsets

### Nelson's Words

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." (4/42)

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." (4/43)

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." (4/44)

> "Note that a link's type--the three-set--may be several pointers." (4/44)

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." (4/44-4/45)

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." (4/45)

> "There is a universal address space, the tumbler line... We may visualize a link's endsets as mapping to it." (4/45)

> "ENDSETS MAY POINT TO SPANS ANYWHERE IN THE DOCUVERSE" (4/45, diagram caption)

> "A link's home (any home) is an element located on one side; and its three endsets map to the other sides." (4/46)

## The Three Endsets

| Endset | Also Called | Purpose |
|--------|-------------|---------|
| **From-set** | first endset | The bytes the link is "from" |
| **To-set** | second endset, 2-set | The bytes the link is "to" |
| **Type** | three-set, 3-set | Categorizes the link (points anywhere, even to ghost addresses) |

## Endsets and Survivability

Links survive because they connect to spans, not positions. The diagram on 4/43 shows:

```
SURVIVABILITY:
Links between bytes can survive
deletions, insertions and rearrangements,
if anything is left at each end.
```

This is why Nelson emphasizes that links are "straps between bytes" - the strap stays attached to whatever bytes remain after editing.

## The Tumbler Square Visualization

Pages 4/46-4/47 introduce the "Tumbler Square" - a way to visualize how a link's endsets map to the universal address space:

- The link's **home** sits on one side of the square
- The **from-set**, **to-set**, and **type** map to the other three sides
- Each endset traces lines to its target positions on the tumbler line

This visualization emphasizes that links are concrete objects with their own addresses, whose three endsets reach out to connect arbitrary spans across the docuverse.

---

## Related Concepts

| Concept | Relationship |
|---------|--------------|
| [links](links.md) | Endsets are the three parts of a link (from, to, type) |
| [spans](spans.md) | Each endset is an arbitrary span-set |
| [tumblers](tumblers.md) | Endsets map to positions on the tumbler line |
| [ghost-elements](ghost-elements.md) | Type endsets can point to addresses with no content |
| [i-space-v-space](i-space-v-space.md) | Endsets point to Istream (enables survivability) |

## FEBE Operations

| Operation | How endsets apply |
|-----------|------------------|
| **MAKELINK** | Specifies three endsets: from-set, to-set, type |
| **FINDLINKSFROMTOTHREE** | Searches by constraining any combination of endsets |
| **FINDNUMOFLINKSFROMTOTHREE** | Counts links matching endset criteria |
| **FINDNEXTNLINKSFROMTOTHREE** | Paginates through matching links |
| **RETRIEVEENDSETS** | Returns the from-set and to-set of specified links |

See [Concept-Operation Map](../concept-operation-map.md) for full mapping.
