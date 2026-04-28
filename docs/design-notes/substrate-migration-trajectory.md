# Substrate Migration Trajectory

*Design note. How the substrate evolves from filesystem-backed scaffolding to a native link graph. Why specific design decisions anticipate this transition. What changes and what stays the same.*

## The architectural commitment

The substrate is designed to be forward-portable without restructuring. The link graph is the durable artifact. The filesystem backing is scaffolding that satisfies the same properties (SUB1–SUB6) the target implementation will satisfy. When the backing store changes, protocols don't change — they depend on properties, not on implementation.

This is not aspirational. It's a testable claim: every protocol's safety arguments reference SUB properties, not filesystem paths. Every query goes through FindLinks/ActiveLinks, not directory scans. Every link is created through MakeLink, not file writes. The abstraction boundary exists and is maintained.

## What changes

**Document versioning.** Currently documents are mutable — the reviser overwrites a claim's markdown on every `resolution.edit`, and git provides version history. The target implementation versions documents natively at the document layer: each edit creates a new version; previous versions remain addressable. Links point at the document; the version index determines which version a reader sees.

This is the single largest change. The link graph doesn't change; it already handles the immutable-link side correctly. What changes is that documents gain the same durability links have — content at a path is no longer destroyed by editing. The gap between "links are permanent" and "documents are overwritten" closes.

**Query implementation.** FindLinks moves from filtered directory scans to whatever the native query interface provides. The semantics (SUB2, SUB3) are unchanged. Performance characteristics may improve.

**Path-based addressing.** Documents are currently referenced by filesystem paths. The target implementation uses content-addressed or structurally-addressed identifiers. The `from` and `to_set` fields in links transition from paths to native addresses. This is a one-time migration at the cut — every path in every link maps to its native address.

## What stays the same

**The link graph.** Every link filed during the filesystem-backed phase is migratable. Link IDs, type strings, from/to relationships — all transfer. The graph structure is the same graph, with different addresses at the endpoints.

**SUB1–SUB6.** The properties don't change. Permanence, query soundness, count consistency, retraction semantics, shadow interpretation, idempotence — all hold in both implementations. The properties were specified to be implementation-independent for exactly this reason.

**Protocol documents.** No protocol document references the filesystem. They reference the substrate's operations and properties. The convergence predicate, the review/revise cycle, the lattice operations — all specified in terms of links and documents, not in terms of files and directories.

**The type vocabulary.** Every link type — substrate-owned (`retraction`, `label`, `name`, `description`) and protocol-defined (`claim`, `citation`, `comment`, `resolution`, `contract`, `review`, `note`, etc.) — transfers as-is. Type strings are strings; they work in any backing store.

## Why specific design decisions anticipate the transition

**Flat link types.** The substrate uses flat top-level types (`name`, `label`, `description`) rather than a parent-with-subtypes hierarchy (`meta.name`, `meta.label`). The target implementation's link system has no privileged categories — a link is a link, distinguished by its type string. Parent types that group link kinds add a taxonomy the target doesn't have. Flat types match what the target provides.

**Link-to-link references for retraction.** Retraction's `to_set` holds a link ID, not a document path. This requires the substrate to support link-level addressing — every link has an ID and that ID is referenceable by other links. The target implementation provides this natively (every link is an addressable object). The filesystem implementation provides it via generated IDs in the store's index. The design tests the pattern now rather than discovering at migration time that link-to-link references don't work.

**Everything is a document.** Label, name, and description are stored as sibling documents reached by typed links — not as link payloads, not as inline fields, not as filesystem conventions. A name is a document. A label is a document. The indirection costs one extra file per attribute during the filesystem phase. The target implementation stores documents natively; the file-per-attribute overhead disappears. The pattern (typed link → document carrying a value) is what the target provides; testing it now means the migration is a backing-store swap, not a structural redesign.

**Document mutability as temporary.** The substrate spec states that documents are mutable and links are immutable, without treating document mutability as a design goal. It's a limitation of the current implementation. The spec's properties (SUB1–SUB6) apply to links. Documents are out of scope for the substrate's guarantees. When document versioning arrives, the substrate spec doesn't change — it never promised anything about documents.

**Retraction rather than deletion.** The append-only constraint (SUB1) means links cannot be removed. Retraction nullifies without removing. This is the same constraint the target implementation imposes — permanent, append-only link storage where nullification is a structural operation rather than deletion. The retraction mechanism, the shadow semantics, the idempotence property — all designed for an append-only world because the target is append-only.

## The migration path

Migration is a bounded operation, not an ongoing process:

1. **Map paths to native addresses.** Every document path in the lattice maps to a native address in the target. One-time, mechanical.
2. **Rewrite link endpoints.** Every link's `from` and `to_set` values change from paths to native addresses. One-time, mechanical.
3. **Transfer documents.** Every file in the lattice becomes a document in the target, at its native address. One-time.
4. **Verify SUB1–SUB6.** Run the protocol test suite against the target implementation. The same properties must hold.
5. **Cut over.** Protocols use the target implementation. The filesystem-backed store becomes archival.

Steps 1–3 are mechanical. Step 4 is verification. Step 5 is operational. No protocol changes. No document restructuring. No link-graph changes. The graph transfers; the backing store changes.

## What the filesystem phase is testing

The filesystem implementation is not a prototype. It's a production implementation that happens to be backed by files. Its purpose is to test the link-graph patterns under real protocol operation — hundreds of review cycles, lattice operations, retraction, convergence — so that when the backing store changes, the patterns are battle-tested.

Specifically:
- Append-only links work for protocol safety. Tested across hundreds of convergence cycles.
- Retraction works as nullification. Tested in citation pruning during proof evolution.
- Shadow semantics produce unambiguous active sets. Tested by every ActiveLinks query.
- Flat link types compose without parent-type overhead. Tested by the full type vocabulary.
- Document-as-value (label, name, description as sibling docs) works for attribute storage. Testing begins with yaml retirement.

Each pattern, once tested, transfers to the target implementation without redesign. The filesystem phase is the testing phase.

## Known risks

**Path encoding in document content.** Some documents reference other documents by filesystem path in their markdown content (e.g., `[T0](T0.md)` links). These are content-level references, not substrate-level references. The substrate's link graph doesn't use them. But they exist in document text and would need content-level migration (rewriting markdown links to native addresses). This is bounded but tedious.

**Git-dependent version history.** During the filesystem phase, document version history lives in git. The target implementation provides native versioning. Git history before the cut is not automatically transferred to the native version index. Whether pre-cut history matters depends on whether anyone needs to query "what did this claim say before the cut." Probably not — the link graph carries the structural history (which comments were filed, which resolutions were made), and document-level history before the cut is archival.

**Scale assumptions.** The filesystem implementation is tested at ~500 links and ~300 documents. The target implementation may behave differently at larger scales. SUB2 (query soundness) and SUB3 (count consistency) are easier to guarantee with directory scans than with distributed storage. The properties must be verified at target scale.

## Related

- [Substrate Module](../modules/substrate-module.md) — the specification this design note explains the trajectory for.
- [Vision](../vision.md) — the broader architectural trajectory of the system.
- [Architecture](../architecture.md) — the six-level hierarchy and lattice structure.