# Concept → FEBE Operation Map

Maps concept files from `resources/xanadu-concepts/` to FEBE operations.

---

## Concepts Overview

| Concept File | Core Idea |
|--------------|-----------|
| [i-space-v-space](../resources/xanadu-concepts/i-space-v-space.md) | Two address spaces: permanent content vs. mutable arrangement |
| [tumblers](../resources/xanadu-concepts/tumblers.md) | Universal addressing that never invalidates |
| [spans](../resources/xanadu-concepts/spans.md) | Contiguous regions in address space |
| [documents](../resources/xanadu-concepts/documents.md) | Owned evolving units |
| [versions](../resources/xanadu-concepts/versions.md) | Arrangements of content through time |
| [transclusion](../resources/xanadu-concepts/transclusion.md) | Inclusion by reference, not copy |
| [links](../resources/xanadu-concepts/links.md) | Three-endset connections between spans |
| [endsets](../resources/xanadu-concepts/endsets.md) | What links connect to (arbitrary span sets) |
| [correspondence](../resources/xanadu-concepts/correspondence.md) | Matching parts across versions |

---

## FEBE Operations → Concepts

### Content Operations

#### INSERT (opcode 0)
*Insert text at position in document*

| Concept | Relevance |
|---------|-----------|
| **i-space-v-space** | INSERT adds to Istream (permanent) and updates Vstream (arrangement) |
| **tumblers** | New content gets fresh tumbler addresses; existing addresses unchanged |
| **spans** | Insertion point specified as address; content becomes a span |
| **documents** | Only owner can INSERT; document evolves |
| **versions** | INSERT changes current version only |

**Key insight from concepts:**
> "Addresses are absolute and immutable" (i-space-v-space)
> "New items may be continually inserted in tumbler-space while the other addresses remain valid" (tumblers)

---

#### DELETEVSPAN (opcode 12)
*Remove span from document*

| Concept | Relevance |
|---------|-----------|
| **i-space-v-space** | DELETE only affects Vstream; Istream content survives |
| **versions** | Deleted content still exists in old versions |
| **spans** | Deletion target is a span |
| **links** | Links to deleted content still point to Istream addresses |

**Key insight from concepts:**
> "Content you 'delete' still exists in Istream, recoverable from old version" (i-space-v-space)
> "Every version you ever created still exists" (versions)

---

#### COPY (opcode 2)
*Transclude content to position*

| Concept | Relevance |
|---------|-----------|
| **transclusion** | COPY IS transclusion - reference not copy |
| **i-space-v-space** | Creates new Vstream mapping to existing Istream content |
| **spans** | Source specified as span-set |
| **correspondence** | Transcluded content corresponds to original |

**Key insight from concepts:**
> "You see the original content (not a copy)" (transclusion)
> "The connection to the source is always visible and traceable" (transclusion)
> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native" (i-space-v-space)

---

#### REARRANGE (opcode 3)
*Transpose two regions of text*

| Concept | Relevance |
|---------|-----------|
| **i-space-v-space** | Pure Vstream operation; Istream unchanged |
| **spans** | Regions specified by cut addresses |
| **documents** | Document evolves through rearrangement |

**Key insight from concepts:**
> "Your document's arrangement (V-stream) can evolve" (i-space-v-space)

---

#### APPEND (opcode 19)
*Append text to document end*

| Concept | Relevance |
|---------|-----------|
| **i-space-v-space** | Adds to Istream at new addresses |
| **tumblers** | New addresses allocated |
| **documents** | Simple document evolution |

---

### Link Operations

#### MAKELINK (opcode 4)
*Create a link between spans*

| Concept | Relevance |
|---------|-----------|
| **links** | Core link creation |
| **endsets** | Link has three endsets: from, to, type |
| **spans** | Each endset is a span-set |
| **documents** | Link lives in specified home document; owner controls it |
| **tumblers** | Link gets its own tumbler address |

**Key insight from concepts:**
> "A Xanadu link is a connective unit... owned by a user" (links)
> "A link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." (endsets)
> "Link types may be ghost elements" (endsets)

---

#### FINDLINKSFROMTOTHREE (opcode 7)
*Find links matching criteria*

| Concept | Relevance |
|---------|-----------|
| **links** | Link search by satisfaction of endsets |
| **endsets** | Search constrains from-set, to-set, type |
| **spans** | Search criteria are span-sets |

**Key insight from concepts:**
> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request" (links)
> "The quantity of links not satisfying a request does not in principle impede search on others" (links)

---

#### FINDNUMOFLINKSFROMTOTHREE (opcode 6)
*Count matching links*

Same concepts as FINDLINKSFROMTOTHREE.

---

#### FINDNEXTNLINKSFROMTOTHREE (opcode 8)
*Paginated link retrieval*

Same concepts as FINDLINKSFROMTOTHREE plus pagination.

---

#### RETRIEVEENDSETS (opcode 26)
*Get link end-sets from spec-set*

| Concept | Relevance |
|---------|-----------|
| **endsets** | Returns the from-set and to-set |
| **spans** | Results are span-sets |

---

### Version Operations

#### CREATENEWDOCUMENT (opcode 11)
*Create empty document*

| Concept | Relevance |
|---------|-----------|
| **documents** | Establishes owner, creates document identity |
| **tumblers** | Document gets permanent tumbler address |

**Key insight from concepts:**
> "Every document has an owner... Only the owner has a right to withdraw a document or change it" (documents)

---

#### CREATENEWVERSION (opcode 13)
*Create version copy of document*

| Concept | Relevance |
|---------|-----------|
| **versions** | Core version creation |
| **i-space-v-space** | New Vstream arrangement, same Istream content |
| **transclusion** | Version effectively transcludes all content from source |
| **correspondence** | New version corresponds to source |
| **tumblers** | New version ID indicates ancestry |

**Key insight from concepts:**
> "A version is not a copy of a document—it is a particular arrangement of content at a particular moment in time" (versions)
> "There is no 'basic' version... any more than one arrangement of the same materials is a priori better than other arrangements" (versions)

---

#### SHOWRELATIONOF2VERSIONS (opcode 10)
*Compare two versions, show correspondence*

| Concept | Relevance |
|---------|-----------|
| **correspondence** | Core operation for finding what matches |
| **versions** | Compares two version arrangements |
| **spans** | Returns corresponding span pairs |
| **i-space-v-space** | Correspondence comes from shared Istream origin |

**Key insight from concepts:**
> "A facility that holds multiple versions is not terribly useful unless it can help you intercompare them in detail" (correspondence)
> "Links may be refractively followed from a point or span in one version to corresponding places in any other version" (correspondence)

---

### Retrieval Operations

#### RETRIEVEV (opcode 5)
*Retrieve content by spec-set*

| Concept | Relevance |
|---------|-----------|
| **spans** | Request is a spec-set (spans) |
| **i-space-v-space** | Retrieves from V-stream (the document's arrangement) |

---

#### RETRIEVEDOCVSPAN (opcode 14)
*Get document's V-stream extent*

| Concept | Relevance |
|---------|-----------|
| **spans** | Returns the bounding span |
| **i-space-v-space** | Describes V-stream boundaries |

---

#### RETRIEVEDOCVSPANSET (opcode 1)
*Get document's V-stream span-set*

Same as RETRIEVEDOCVSPAN but returns span-set for text and links separately.

---

#### FINDDOCSCONTAINING (opcode 22)
*Find documents containing specified content*

| Concept | Relevance |
|---------|-----------|
| **transclusion** | Multiple docs can contain same content via transclusion |
| **i-space-v-space** | Search by Istream content, find all Vstream appearances |
| **correspondence** | Shared origin enables reverse lookup |

**Key insight from concepts:**
> "The connection to the source is always visible and traceable" (transclusion)

---

## Concepts → Operations (Reverse Index)

### i-space-v-space
The foundational concept. Affects nearly every operation.
- **INSERT, APPEND** - Add to Istream, update Vstream
- **DELETE** - Vstream only; Istream unchanged
- **COPY** - New Vstream mapping to existing Istream
- **REARRANGE** - Pure Vstream
- **CREATENEWVERSION** - New Vstream, same Istream
- **FINDDOCSCONTAINING** - Search Istream, find Vstream appearances

### tumblers
Addressing underlies everything.
- **INSERT, APPEND** - New addresses allocated
- **CREATENEWDOCUMENT** - Document address assigned
- **MAKELINK** - Link gets address
- All retrieval operations use tumbler addresses

### spans
The currency of FEBE requests and responses.
- Every operation uses spans for specifying content regions
- **FINDLINKSFROMTOTHREE** - Search criteria are span-sets
- **SHOWRELATIONOF2VERSIONS** - Returns corresponding spans

### documents
Ownership and identity.
- **CREATENEWDOCUMENT** - Creates owned document
- **INSERT, DELETE, REARRANGE, APPEND** - Require ownership
- **MAKELINK** - Link home determines ownership

### versions
Time dimension.
- **CREATENEWVERSION** - Creates version
- **SHOWRELATIONOF2VERSIONS** - Compares versions
- All content ops implicitly affect "current version"

### transclusion
Reference not copy.
- **COPY** - The transclusion operation
- **CREATENEWVERSION** - Effectively transcludes all content
- **FINDDOCSCONTAINING** - Finds all transclusions

### links
Connections.
- **MAKELINK** - Creates link
- **FINDLINKSFROMTOTHREE** - Searches links
- **FINDNUMOFLINKSFROMTOTHREE** - Counts links
- **FINDNEXTNLINKSFROMTOTHREE** - Paginates links
- **RETRIEVEENDSETS** - Gets link endsets

### endsets
Link structure.
- **MAKELINK** - Specifies three endsets
- **FINDLINKSFROMTOTHREE** - Searches by endsets
- **RETRIEVEENDSETS** - Returns endsets

### correspondence
Matching across versions.
- **SHOWRELATIONOF2VERSIONS** - Core correspondence operation
- **CREATENEWVERSION** - Establishes correspondence
- **FINDDOCSCONTAINING** - Uses shared origin

---

## Example: INSERT Trace

When INSERT executes, these concept guarantees apply:

1. **i-space-v-space**: New content stored in Istream; Vstream arrangement updated
2. **tumblers**: Fresh addresses allocated; no existing addresses change
3. **spans**: Inserted content becomes addressable as a span
4. **documents**: Must be owner; document history grows
5. **versions**: Current version changes; old versions unaffected
6. **links**: Any links to surrounding content still valid (point to Istream)

---

## Open Questions

1. **How do links "survive editing"?** If Vstream addresses shift after INSERT, how do link endpoints stay valid? Do links point to Istream or Vstream?

2. **What exactly is in a vspec vs a span?** The FEBE protocol uses both - what's the difference semantically?

3. **How does correspondence get established?** Is it automatic (shared Istream origin) or explicit (counterpart links)?

4. **What happens to links when content is deleted?** The concepts say links survive "if anything is left at each end" - what defines "left"?
