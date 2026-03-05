# Shared Vocabulary

Common language for ASN authors. NOT normative — use these terms consistently but derive properties independently.

## Core Types

**Tumbler**: A finite sequence of non-negative integers used as an address. Tumblers are hierarchically structured (node.user.document.version.element) and totally ordered. Every piece of content in the system has exactly one permanent tumbler address.

**Address Space**: The set of all tumblers, with a total ordering. Partitioned into subspaces by prefix (e.g., `1.x` for text content, `0.x` for links within a document).

**I-Space (Identity Space)**: The permanent, append-only content store. Content in I-space is addressed by I-stream tumblers and is never modified or deleted. I-space is the ground truth for what content exists.

**V-Space (Virtual Space)**: The mutable arrangement layer. A document's V-space maps virtual positions to I-space content. Editing operations (insert, delete, rearrange) modify V-space while I-space remains unchanged.

**Document**: A named, owned, versioned container. A document has an owner, a version history (DAG), and two subspaces: text content (1.x) and links (0.x).

**Version**: An immutable snapshot of a document's V-space arrangement. Versions form a DAG via forking — creating a new version from an existing one. All versions share the same I-space content pool.

**Enfilade**: An abstract tree-structured index over a range of addresses. Satisfies composable width properties (the parent's width is a function of children's widths). Supports efficient range queries. Three types: I-enfilade (content storage), V-enfilade (arrangement via POOMs), link enfilade (bidirectional link indexing).

**Operation**: A transformation of system state (INSERT, DELETE, COPY, MAKELINK, etc.) defined by preconditions, postconditions, and frame conditions. Operations modify V-space; I-space is append-only.

**Link**: A typed, bidirectional association between address ranges. A link has three endsets (from, to, type), each being a set of spans. Links attach to content identity, not position — they survive editing.

**Endset**: A set of spans that a link endpoint connects to. Endsets reference I-space addresses, so they track content identity through editing operations.

**Span**: A contiguous range in address space, specified by a start tumbler and length. The fundamental unit of content reference.

**Transclusion**: Inclusion by reference — sharing content across documents without copying. Transcluded content maintains identity with the original: edits, links, and attributions follow the content, not the location.

## Key Distinctions

- **I-space vs V-space**: Content exists (I-space) vs content is arranged (V-space). DELETE removes from V-space but content persists in I-space.
- **Address vs position**: A tumbler address is permanent (content identity). A position in a document is mutable (arrangement).
- **Copy vs transclusion**: Copy creates independent content with a new address. Transclusion creates a reference — same content, same address, shared identity.
- **Link to content vs link to position**: Links attach to I-space addresses (content identity), not V-space positions. When content moves, links follow.
