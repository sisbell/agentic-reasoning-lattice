# Shared Vocabulary

Common language for ASN authors. NOT normative — use these terms consistently but derive properties independently.

## Core Types

**Tumbler**: A finite sequence of non-negative integers used as an address. Tumblers are hierarchically structured (node.user.document.version.element) and totally ordered. Every piece of content in the system has exactly one permanent tumbler address.

**Address Space**: The set of all tumblers, with a total ordering. Partitioned into subspaces by the first component of the element field (e.g., `1` for text content, `2` for links within a document).

**Istream (Invariant Stream)**: The permanent, append-only content store. The docuverse order of content pieces — the local order of arrival and storage. Content in the Istream is addressed by I-addresses and is never modified or deleted. The Istream is the ground truth for what content exists.

**Vstream (Variant Stream)**: The mutable arrangement layer. A current permutation of a document's content — another ordering of the same contents. Editing operations (insert, delete, rearrange) modify the Vstream while the Istream remains unchanged. The Vstream-to-Istream mapping is represented by the POOM (Permutation Of Order Matrix).

**Document**: A named, owned, versioned container. A document has an owner, a version history (DAG), and two element subspaces: text content (subspace 1) and links (subspace 2).

**Version**: An immutable snapshot of a document's Vstream arrangement. Versions form a DAG via forking — creating a new version from an existing one. All versions share the same Istream content pool.

**Enfilade**: An abstract tree-structured index over a range of addresses. Satisfies composable width properties (the parent's width is a function of children's widths). Supports efficient range queries. Three types: I-enfilade (content storage), V-enfilade (arrangement via POOMs), link enfilade (bidirectional link indexing).

**Operation**: A transformation of system state (INSERT, DELETE, COPY, MAKELINK, etc.) defined by preconditions, postconditions, and frame conditions. Operations modify the Vstream; the Istream is append-only.

**Link**: A typed, bidirectional association between address ranges. A link has three endsets (from, to, type), each being a set of spans. Links attach to content identity, not position — they survive editing.

**Endset**: A set of spans that a link endpoint connects to. Endsets reference Istream addresses, so they track content identity through editing operations.

**Span**: A contiguous range in address space, specified by a start tumbler and length. The fundamental unit of content reference.

**Transclusion**: Inclusion by reference — sharing content across documents without copying. Transcluded content maintains identity with the original: edits, links, and attributions follow the content, not the location.

## Key Distinctions

- **Istream vs Vstream**: Content exists (Istream) vs content is arranged (Vstream). DELETE removes from the Vstream but content persists in the Istream.
- **Address vs position**: A tumbler address is permanent (content identity in the Istream). A position in a document is mutable (arrangement in the Vstream).
- **Copy vs transclusion**: Copy creates independent content with a new address. Transclusion creates a reference — same content, same address, shared identity.
- **Link to content vs link to position**: Links attach to Istream addresses (content identity), not Vstream positions. When content moves, links follow.
