# FEBE (Front-End/Back-End Protocol)

Source: Literary Machines, pages 4/61-4/73 (raw pages 228-240)

## Semantic Intent

### What It Means

FEBE is the interface through which users interact with the Xanadu docuverse. It defines the contract between user-facing applications (front ends) and the storage system (back end). Rather than exposing storage internals, FEBE presents a clean semantic interface: users work with documents, spans, links, and versions - never with memory addresses, file offsets, or internal data structures.

The protocol treats the docuverse as a unified information space. Users can create documents, insert and delete content, make links, copy material between documents, and retrieve both text and links - all through operations that preserve Xanadu's fundamental guarantees.

### User Guarantee

**What users can always do through FEBE:**

- Create new documents and versions
- Insert content at any position
- Delete spans (logically, not destroying content)
- Copy content between documents (preserving source identity)
- Append to documents
- Retrieve any content by address
- Create links connecting any content
- Find all links to/from any content
- Discover what documents contain specific material

**What is hidden from users:**

- How content is physically stored
- Internal representation of addresses
- Caching and performance optimizations
- Network distribution details
- Storage format and compression

### Principle Served

**Separation of concerns.** The front end (user interface) and back end (storage) evolve independently. A new front end can be built without understanding storage internals. Storage can be optimized without breaking user applications.

**Permanence through abstraction.** Because users work with semantic operations (INSERT, COPY, MAKELINK) rather than storage operations, the system can maintain permanent addresses and content even as storage evolves.

**Universal access.** Any conforming front end can access any content in the docuverse. The protocol is the contract that makes the unified docuverse possible.

### How Users Experience It

- Write a document, save it, receive a permanent address
- Edit a document - changes create new versions, old content remains addressable
- Copy a passage from another document - the copy knows its source
- Create a link between two passages - survives editing of either document
- Search for links - find everything connected to your content
- Retrieve by address - always works, addresses never become invalid

### Operations

**Document Operations:**
- CREATENEWDOCUMENT - Create empty document, receive its ID
- CREATENEWVERSION - Fork a document as new version (ancestry preserved)
- INSERT - Add content at a position
- DELETEVSPAN - Remove a span (content preserved in I-space)
- COPY - Duplicate content between documents
- APPEND - Add to end of document
- RETRIEVEV - Get material at specified positions
- REARRANGE - Reorder content regions

**Link Operations:**
- MAKELINK - Create link between content sets
- FINDLINKSFROMTOTHREE - Find links connecting specified content
- FINDNUMOFLINKSFROMTOTHREE - Count such links
- FINDNEXTLINKSFROMTOTHREE - Iterate through link results

**Discovery Operations:**
- RETRIEVEDOCVSPAN - Find document extent
- RETRIEVEDOCVSPANSET - Get span and link counts
- SHOWRELATIONOFVERSIONS - Compare documents
- FINDDOCSCONTAINING - Find all documents containing material

### Nelson's Words

> "In computer parlance, 'protocol' refers to the formal rules for interchange in some sort of communications system. The protocols of Xanadu are called FEBE and BEBE; there are also additional complications of various sorts."
> — page 4/61

> "Now that some of these commands are to be seen by the user: The user's concerns are document content and links, and the complications of the protocol are to be handled invisibly by programs in the user's front-end machine, leaving the user free to think about other things."
> — page 4/61

> "FEBE includes instructions for insertion in a document, deletion from a document, and rearrangements of unlimited size. These are conceptually simple."
> — page 4/61

> "However, the commands for links and connectivity (material shared between documents and versions) are more esoteric, particularly since they have been generalized for the interconnection of broken lists of spans."
> — page 4/61

> "FEBE commands are presently in verbose ASCII. They will be shortened as needed."
> — page 4/61

> "FEBE is the protocol for handing off what the user wants to see, retrieve and follow."
> — page 4/62 (diagram caption)

## Design Philosophy

### Three-Tier Architecture

Nelson describes a "middle end" between front and back:

1. **Front End** - User interface, local to user
2. **Middle End** - Parsing, scanning, search (shared infrastructure)
3. **Back End** - Storage and retrieval

The middle end handles:
- Parsing FEBE commands
- Scanning and search (too expensive for front end alone)
- Back-comparison between versions
- Finding commonalities for compression

### User-Facing Simplicity

> "Many people, particularly those who are accustomed to the assorted 'model' of other file systems, have a hard time getting used to our link model, and insist that scanning should be part of the Xanadu back end."
> — page 4/72

Nelson pushes back: scanning belongs in the middle end, not exposed to users. Users work with high-level operations; the system handles search optimization internally.
