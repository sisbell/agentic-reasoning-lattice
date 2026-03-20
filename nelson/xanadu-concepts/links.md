# Links

Source: Literary Machines 2/43 (page 123), 4/41-4/60 (pages 208-227)

## Semantic Intent

### What It Means

A **link** is a meta-virtual structure connecting parts of documents. Unlike conventional hyperlinks that connect point A to point B, Xanadu links are *connective units* in the docuverse that relate regions of content through three-way associations.

Links are first-class citizens in the docuverse: they have their own addresses, can be owned (and thus controlled) by their creators, exist independently of the documents they connect, and can themselves be the targets of other links.

The link mechanism provides a universal system of retrieval that is unlike any other in the world. Through links, users can build webs of connection, comment, annotation, and relationship across the entire literature.

### User Guarantee

- **Links connect spans, not positions.** A link attaches to bytes, not to character positions. If content moves or surrounding content is edited, the link remains attached.
- **Links survive editing.** As long as *any* of the bytes at each end remain, the link survives. Only complete deletion of all connected content at one end destroys the link.
- **Links traverse versions.** When a document is superseded, links made to the old version "reach through" into the newer version. A reader following an old link can be directed to the same passage in the current version, if it still exists.
- **Links create permanence obligations.** Once others have linked to your published document, you cannot withdraw it - their links depend on its accessibility. This is why published documents stay published.
- **Links are bidirectional in discovery.** The system indexes links by all their endsets. You can search from any direction - find what points to this content, or find where this content points.
- **Links are owned by their creators.** The link's home address determines ownership. Users control their own links even though those links point into others' documents.
- **Link types are user-definable.** The type mechanism is open-ended. Users create their own link types for any purpose without system changes.
- **Links can point to links.** Because links have addresses, they can be targets of other links - enabling commentary on links, meta-links, and complex associative structures.

### Principle Served

**Literature is interconnected.** Nelson views all literature as a system of interconnected writings - quotations, citations, influences, responses, refutations. Links make these connections explicit and navigable rather than implicit and lost.

**The problem of marginalia solved.** Traditional marginalia face the "distribution problem" - your notes in your copy don't reach others. Xanadu links solve this because:
- Your links are yours (at your address, under your control)
- But they're visible to anyone reading the linked material
- The link doesn't modify the target document - it exists independently

**Non-destructive connection.** Links don't alter the documents they connect. They are a separate layer of association that coexists with the base content.

**Links justify permanence.** The reason documents cannot be withdrawn once published is precisely because other users will have linked to them. Their links - which they own, at their addresses - depend on the continued existence of the target. Withdrawing a document would break others' property.

### How Users Experience It

- Select a passage and create a link to another passage - the link exists independently
- Read a document and see all links pointing into it (the "backlinks" problem solved)
- Follow a link to see what it points to, then follow it backward to see what else points there
- Create your own link types (citation, annotation, dispute, explanation) and search by type
- Edit documents freely knowing your connections won't break unless you delete the linked content itself
- Comment on someone else's document without modifying it - your link lives at your address
- Create a link that points to another link (meta-commentary)
- Find all links of a certain type (all citations, all refutations) across the docuverse

### Nelson's Words

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user. It is put in by a user (or a front end), and thereafter maintained by the back end through the back end's inter-indexing mechanisms." (4/41)

> "The Xanadu link is a meta-virtual structure connecting parts of documents (which are themselves virtual structures). The link is used for information that connects, marks, represents alternative structure and points of view, and much more." (4/41)

> "Xanadu links, and the methods by which we search through them, are a system of retrieval quite unlike any other in the world." (4/41)

> "The link mechanism ties together the whole corpus of materials on the Xanadu system. There is essentially nothing in the Xanadu system except documents and their arbitrary links." (4/41)

> "A Xanadu link is not between points, but between spans of data." (4/42)

> "This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, the link remains on them. This also works for alternative versions in which part of each end has survived." (4/42)

> "A link is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.' (What 'from' and 'to' mean depend on the specific case.)" (4/42)

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endsets: a link may be to or from an arbitrary set of bytes. There may be anywhere in the docuverse." (4/42)

> "Links are meant to be extensible for the arbitrary needs of any user. Thus the set of link types is open-ended, and indeed any user may define his or her link types for a particular purpose." (4/43)

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

On links and document permanence:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." (2/43)

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it—which can now reach through from the previous version (to which they were originally attached) into the newer version." (2/43)

> "When a document is updated, a reader will ordinarily want to see the new version—but the reader may be following a link made to an older version. However, the user's front-end machine may easily be set up to follow the link to the same passage in the most recent version—if it's still there." (2/43)

## Link Types

Links are classified by their **type endset** (the "3-set"), which points anywhere in the docuverse. This makes link types completely extensible - any user can define new types without system modification.

### Ordinary Text Links

Standard literary links using established conventions:

| Type | Meaning |
|------|---------|
| **Connection Link** | General connection between material |
| **Comment Link** | Commentary on a passage |
| **Counterpart Link** | Shows correspondence between equivalent portions |
| **Translusion Link** | Translation relationship |
| **Alternative-Version Link** | Points to alternative version of same content |
| **Contents-Document Link** | Points to table of contents |
| **Certified Link** | Verified by authority, may be applied to versions |
| **Mail Link** | Material addressed through mail system |

### Quote-Link

A **quote-link** indicates the author's acknowledgment of material origin. Since a quote-link shows authorship, it differs from an "inclusion" which may not be ordinarily indicated to the user.

> "Note that a quote-link is not the same as an inclusion, which is not ordinarily indicated—whenever there were editorial changes at the beginning of the paragraph. Pointing at the whole paragraph makes more sense." (4/53)

### Literary Links

Extended types for complex document relationships:

| Type | Purpose |
|------|---------|
| **Citation Link** | Like a footnote reference with bridge to source |
| **Expansion Links** | Proposes expansion of text or graphics |
| **Vanilla Jump-Link** | Plain link from place to place |
| **Suggested-Threading Links** | Suggests pathway through material |
| **Moral Jump-Links** | Distinguished from vanilla by type |

### Hypertext Links

> "By 'hypertext links' we mean links to make any possible arrangements for explorable materials." (4/54)

### Document Metadata Links

Links that indicate document properties rather than content connections:

| Type | Purpose |
|------|---------|
| **Heading Link** | Internal heading or subtitle within document |
| **Paragraph Link** | Points front end to a paragraph for navigation |
| **Footnote Link** | Provides a break sequence for an author |

### One-Sided Links

An important variation where a link has only one side - something pointing to material, but not from other material. The paragraph designator is an example. This avoids terminological confusion by using only the from-set to designate the matter pointed at.

> "Unfortunate terminological problem: since it has only one side, we use the first endset to designate the matter pointed at. To call this 'from' is inane." (4/48)

## Link Address Structure

Links within a document occupy the **2.x subspace** and are addressed sequentially by creation order:

```
N.0.U.0.D.V.0.2.1    → first link in document
N.0.U.0.D.V.0.2.2    → second link in document
N.0.U.0.D.V.0.2.755  → 755th link in document
```

Breaking down the address:
- `N.0.U.0.D` = node, account, document
- `V` = version
- `0.2` = delimiter + link subspace (vs `0.1` for bytes)
- `N` = link instance number (sequential)

### Permanent Order of Arrival

Unlike bytes (which can be rearranged in Vstream), **links keep their creation-order addresses permanently**:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

This means:
- Link `2.1` is always the first link created in that document
- Link `2.755` is always the 755th link created
- Deleting link `2.5` doesn't renumber `2.6` through `2.N`

### Subspace Distinction

The document-local address space uses numeric prefixes:

| Subspace | Address Pattern | Contents |
|----------|-----------------|----------|
| Bytes | `version.position` (1.x) | Text content |
| Links | `version.0.2.N` | Links stored in this document |

**Important:** Don't confuse link *instance* addresses (`2.1`, `2.2`) with link *type* addresses (`1.0.2.2` for jump, `1.0.2.3` for quote). The type registry lives in the bootstrap document (doc 1) and uses a similar-looking but semantically different address scheme.

### Nelson's Words

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" (4/31)

> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" (4/31)

> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." (4/31)

---

## Key Properties

### The Strap Between Bytes

Links connect bytes, not positions. The diagram shows a link as a "strap" binding bytes together - if the document is edited and bytes move, the strap stays attached to those same bytes.

### Survivability

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." (4/43)

Links are intrinsically bidirectional in the system's indexing. Some types are a special case where directionality matters to the user.

### Arbitrariness of Type

The "type" designation is completely arbitrary. The search mechanism does not look at what is stored at the type address - it merely matches the address itself. Link types may be "ghost elements" with nothing actually stored at that address.

### Links to Links

Because links have tumbler addresses, a link can point to another link. The to-set simply points to the link's address on the tumbler line with a span of 1 to designate that unit only.

### Compound Links

Complex relational structures, such as the faceted link (two-sided link structure like CONS cell in LISP), may be constructed with links to links. These can be built into arbitrary compound structures mapped to tumbler-space.

## Searching Links

### The AND of the ORs

Link search uses a satisfaction model:

```
A link satisfies a search request if
one span of each endset satisfies a
corresponding part of the request.
```

For each endset (from-set, to-set, type), at least one span must fall within the corresponding part of the request. A request specifies:
- **home-set**: where desired links are to be found
- **from-set**: those spans of the docuverse wanted at the first side of the link
- **to-set**: those spans of the docuverse wanted at the second side of the link
- **three-set**: spans covering the types of link wanted in the request

### The Junk-Link Problem

Filtering out junk links (links in a universe full of them) is important for system performance. The quantity of links not satisfying a request does not in principle impede search on others - you can still do link-search and subdivide with constraints that only deal with parts of the system.

### Link Filters

Filtering links is a key aspect of front-end design. The system supports separating relevant from irrelevant links, giving users control over what connections they see.

### The Resource Unit

Clever users can ask for the moon and stars simultaneously. While early versions will handle simple queries, more sophisticated service will evolve. When the system can't fully satisfy a request, a Resource Unit (RU) becomes the user's friend - the back-end's sophisticated allocation system working on your behalf.

## Contrast with Web Hyperlinks

| Xanadu Links | Web Hyperlinks |
|--------------|----------------|
| Connect spans to spans | Connect pages to pages |
| Survive editing | Break when targets move |
| Bidirectional discovery | One-way only |
| Owned by creator | Part of source document |
| Typed by user | Untyped (or HTML class) |
| Three endsets | Two endpoints |
| First-class objects | Embedded in markup |
| Can point to links | Cannot (easily) |

---

## Related Concepts

| Concept | Relationship |
|---------|--------------|
| [endsets](endsets.md) | Links have three endsets: from, to, type |
| [spans](spans.md) | Each endset is a span-set (can be discontiguous) |
| [documents](documents.md) | Link home document determines ownership |
| [tumblers](tumblers.md) | Links have their own tumbler addresses |
| [i-space-v-space](i-space-v-space.md) | Links point to Istream content (survive Vstream editing) |
| [ghost-elements](ghost-elements.md) | Link types can point to addresses with no content |

### Link Type Concepts

| Concept | Description |
|---------|-------------|
| [counterpart-link](counterpart-link.md) | Shows correspondence between equivalent portions |
| [mail-link](mail-link.md) | Material addressed through mail system |
| [supersession-link](supersession-link.md) | Points to newer version |
| [link-to-link](link-to-link.md) | Links can point to other links |
| [metalinks](metalinks.md) | Links about links |
| [suggested-threading-links](suggested-threading-links.md) | Suggests pathway through material |

## FEBE Operations

| Operation | How links apply |
|-----------|----------------|
| **MAKELINK** | Creates a link with three endsets in home document |
| **FINDLINKSFROMTOTHREE** | Searches links by endset constraints |
| **FINDNUMOFLINKSFROMTOTHREE** | Counts matching links |
| **FINDNEXTNLINKSFROMTOTHREE** | Paginated link search |
| **RETRIEVEENDSETS** | Gets the from-set and to-set of links |

See [Concept-Operation Map](../concept-operation-map.md) for full mapping.