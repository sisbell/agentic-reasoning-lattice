# Xanadu Engine — Module Decomposition

## Overview
Three kernel modules sit at the bottom: a pure value-level **address & span algebra** (M1), a **transaction/journal/concurrency kernel** (M2) that makes every change atomic-ordered-durable-recoverable, and a **namespace** (M3) that mints, records, and owns addresses. On that kernel ride the system's two great state families as feature modules — the document substrate (immutable content store M4, mutable arrangement+editing M5, read-only queries M6) and the link/relation subsystem (store+types M7, discovery M8) — capped by a programmable coordination layer (M9). The single organizing idea: separate the **permanent immutable record** from the **mutable presentation**, funnel every mutation through one kernel, and keep every derived index as a recomputable hint over an append-only journal.

## Modules

### M1 — Address & Span Algebra
- **Responsibility:** The pure value-level calculus of the address space — tumbler identity/order/containment/classification, position arithmetic, and the interval algebra over spans and span-sets — decidable from values alone, consulting no state and doing no I/O.
- **Sources:** ASN-0034 (tumbler value, intrinsic comparator, field parser/validator, action point & `sig`, ⊕/⊖/`inc`, spans, ordinal shift); ASN-0045 (node/account/document/element classifier, `T4-valid`, level vocabulary); ASN-0053 (span & span-set algebra — classify/merge/split/intersect/difference, canonical normalization, coverage).
- **Depends on:** — (foundation)
- **Key components:** tumbler value & lexicographic order; field parser + T4 admission validator; level classifier (node/account/document/element/invalid); action-point & last-significant-position primitives; ⊕/⊖/`inc`; ordinal-only shift; span & span-set types; coverage; span-set canonical normalization; `origin`/level projectors.
- **Seams:** Hands tumblers, spans, coverage, and the `origin`/level projections upward as the universal key/endpoint/classification types; leans only on ℕ.

### M2 — Transaction, Journal & Concurrency Kernel
- **Responsibility:** Turn every state change into one atomic, totally-ordered, durable, recoverable step (and composites thereof), and present the spec's sequential semantics faithfully to concurrent clients.
- **Sources:** ASN-0047 (seven-primitive atomic-step model, composite executor, commit-marker durability, three-layer permanence discipline); ASN-0134 (Minimal Isolation Contract — single linearization point, per-(home,subspace) serialization, snapshot reads, commit-before-acknowledge); the pervasive journal+replay+snapshot recovery discipline running through the corpus.
- **Depends on:** M1 (the `(home, subspace)` contention unit and step keys are address structure).
- **Key components:** append-only journal of record; single-step linearization / serialization point; composite-transaction boundary; per-home serialization & MVCC snapshot reads; snapshot/checkpoint; replay-driven recovery; commit-before-acknowledge gate.
- **Seams:** Stores register record-types and index-rebuilders and obtain atomic commit + consistent snapshots through it (dependency-inverted); it owns ordering/durability/isolation, never store semantics.

### M3 — Namespace: Allocation, Registry & Ownership
- **Responsibility:** Own the authoritative permanent name/entity space — mint fresh globally-unique addresses under the frontier discipline, record what exists, and resolve who owns what by prefix.
- **Sources:** ASN-0040 (baptismal registry, next-address allocator, atomic baptism, B6 gate, per-namespace frontier); ASN-0093 (allocation substrate, K.σ document/entity registration, sub-allocator chains); ASN-0034 (per-domain allocators, durable monotone frontier); ASN-0042 (principal registry, `owns` predicate, longest-prefix `ω` resolver, delegation gate, fork); ASN-0103 (CREATENEWDOCUMENT).
- **Depends on:** M1, M2.
- **Key components:** per-(home,subspace) frontier allocator (`inc`-modes, gap-free, monotone); baptismal/entity registry (append-only existence set; node/account/document); validity/admission gate; principal registry + `owns` + effective-owner resolver `ω`; delegation gate; fork allocation; genesis/seed init; CREATENEWDOCUMENT.
- **Seams:** Hands fresh, T4-valid, owned addresses plus "is allocated?"/"who owns?" answers to every store and operation; persists registry + frontier via M2; deliberately decoupled from content (ghost elements).

### M4 — Content Store (Istream)
- **Responsibility:** The permanent, append-only, immutable byte store keyed by allocated address — Nelson's permascroll; the never-mutated, never-GC'd half of the two-layer state.
- **Sources:** ASN-0036 (content store C — write-once, origin-identity-not-value, no update/delete, run-decomposition on demand); ASN-0093 (K.α content allocation); consumed by ASN-0115.
- **Depends on:** M1, M2, M3.
- **Key components:** address→value append-only map; membership & value-at lookup; origin-identity discipline (no value-dedup as identity); kind-from-address; the no-mutate/no-delete/no-GC guarantee; replay-recovered index (a hint).
- **Seams:** Receives content addresses from M3, durability from M2; hands immutable value lookups to retrieval (M6) and serves as the referential-integrity target for arrangements (M5); never read for bytes by the link layer.

### M5 — Arrangements & Editing (Vstream)
- **Responsibility:** Own each document's mutable V→I arrangement (the POOM) and the content provenance relation, and provide the editing/versioning operations — the only layer where destructive change lives.
- **Sources:** ASN-0036 (arrangement M, S-invariants); ASN-0058 (POOM mapping block, split/merge/canonicalize, resolve); ASN-0082 (gap open/close displacement); ASN-0084 (cut-point rearrangement primitive); ASN-0116 INSERT; ASN-0117 DELETE; ASN-0118 COPY; ASN-0119 REARRANGE; ASN-0123 CREATENEWVERSION; ASN-0047 (extend/contract/reorder + provenance R).
- **Depends on:** M1, M2, M3, M4.
- **Key components:** per-document arrangement store (POOM, content + link subspaces); split / merge / canonicalize; resolve (V→I); displacement (extend/contract/reorder); INSERT / DELETE / COPY / REARRANGE / VERSION; provenance relation R (append-only, authoritative); subspace confinement & contiguity maintenance.
- **Seams:** Mints content addresses via M3, writes bytes via M4, commits composites via M2; exposes V→I resolution and arrangement-mutation (including a link-seating API for M7); hands R to content query (M6).

### M6 — Content Retrieval & Query
- **Responsibility:** Read-only observers over documents — deliver content, report extents, attribute origin, and answer provenance/version/containment questions; owns no authoritative state.
- **Sources:** ASN-0115 RETRIEVEV; ASN-0112 RETRIEVEDOCVSPAN; ASN-0113 RETRIEVEDOCVSPANSET; ASN-0077 SHOWORIGIN; ASN-0075 SHOWDELETIONS; ASN-0122 COMPARE; ASN-0124 FINDDOCSCONTAINING.
- **Depends on:** M1, M2, M4, M5.
- **Key components:** content delivery (resolve→fetch); document-extent queries (span / span-set); origin projection (SHOWORIGIN); deletion classification (SHOWDELETIONS); version comparison (COMPARE); document-containment oracle (FINDDOCSCONTAINING) + its reverse-index hint over R.
- **Seams:** Resolves through M5's arrangements, fetches bytes from M4, reads R for provenance, projects origin via M1, takes snapshots from M2; writes nothing.

### M7 — Link & Relation Store
- **Responsibility:** Own the authoritative link/typed-relation store — create, read, type, retract, and supersede links and typed relations as immutable, address-identified, append-only objects under the shape/admission discipline.
- **Sources:** ASN-0043 (link store, endsets, type-by-coverage, link value); ASN-0093 (K.λ); ASN-0120 MAKELINK; ASN-0111 READLINK; ASN-0114 FOLLOWLINK; ASN-0086 (Emit/Nullify, active/audit, retraction); ASN-0126 (shape gate); ASN-0128 (type registry, idempotence/dedup, behaviors, shipped types); ASN-0125 (link editing / supersession).
- **Depends on:** M1, M2, M3, M5.
- **Key components:** link store (L) + endset/link value; type-by-coverage matching; MAKELINK / READLINK / FOLLOWLINK; Emit / Nullify + active vs audit slices; nullified/tombstone set; shape gate + type registry (shape/idem/behaviors); de-duplication; supersession claims & determinate-walk.
- **Seams:** Allocates link addresses via M3, resolves V-region endset args & seats home links via M5's arrangement API, commits via M2; hands the canonical store + active/audit slices to discovery (M8) and the typed-relation surface to coordination (M9).

### M8 — Link Query & Discovery
- **Responsibility:** Read-only indexed discovery and resolution over the link store — which links touch a content region, project/follow/count/paginate them — backed by the spanfilade index (a recomputable hint).
- **Sources:** ASN-0098 (project / coverage / discoverability); ASN-0127 (content-region link query); ASN-0121 (findlinks / Observe); ASN-0108 (windowed search); ASN-0132 (count); ASN-0131 (RETRIEVEENDSETS); ASN-0043 (spanfilade).
- **Depends on:** M1, M2, M5, M7.
- **Key components:** spanfilade content-coverage index (per-slot, hint); project / coverage / discoverability; findlinks (four-set match) & Observe; count; windowed enumeration (identity cursor); RETRIEVEENDSETS; the V→I image primitive (via M5).
- **Seams:** Reads the link store + active slice from M7, resolves content regions to I-addresses via M5, rebuilds its index by replay through M2; hands link-discovery answers to readers and to coordination (M9); writes nothing authoritative.

### M9 — Predicate & Coordination Layer
- **Responsibility:** The substrate's closed predicate/query language, its persistence as first-class content, and the reactive rule engine built on it — the programmable, self-monitoring automation layer with a defined quiescence theory.
- **Sources:** ASN-0129 (PL: closed algebra, evaluator, dynamics/stability analyzer); ASN-0130 (predicate definitions as substrate content — registration, references, versioning); ASN-0133 (quiescence: rule registry, fires, scheduler, termination); consumes ASN-0128's behavior atoms.
- **Depends on:** M1, M2, M3, M4, M7, M8.
- **Key components:** PL term representation + type checker + pure evaluator; dynamics/stability classifier; predicate-definition encoding/registration/expansion (defs stored as content); rule registry + trigger evaluation + atomic fires; quiescence detector + fair scheduler.
- **Seams:** Reads structural state via M7's Observe/behaviors and M8's queries, resolves residence via M3, stores predicate-defs as content in M4, leans on M2 for snapshot-consistent multi-read verdicts and atomic fires; hands a programmable coordination surface upward (out of corpus).

## Module DAG
```
M2 → M1
M3 → M1, M2
M4 → M1, M2, M3
M5 → M1, M2, M3, M4
M6 → M1, M2, M4, M5
M7 → M1, M2, M3, M5
M8 → M1, M2, M5, M7
M9 → M1, M2, M3, M4, M7, M8
```
Acyclic — every edge points to a lower-numbered module. The one seam that could have closed a cycle (M5 owns the arrangement; M7's MAKELINK *writes* its link subspace) is broken by direction: M5 exposes a link-seating API and never interprets link semantics, so **M7 → M5** with no return edge.

**Valid topological build order:** M1, M2, M3, M4, M5, M6, M7, M8, M9.

## Open partition questions
- **Content store (M4) vs Arrangements (M5).** Split here on change-profile (immutable Istream vs mutable Vstream — the system's architectural spine). But M4 is thin in *mechanism*; the two are "the strand model" of one note (ASN-0036) and could merge into a single "Document Substrate." I kept them apart to make the Istream/Vstream split module-visible.
- **Ownership (ASN-0042) inside M3 vs its own Authority module.** Folded in because principals are a labeling of the registry and delegation *is* a baptism — but authority is *policy* over allocation's *mechanism* (Lampson's separation), and a session/access layer is its natural consumer. The longest-prefix `ω` resolver + delegation + fork could stand alone.
- **M7/M8 link boundary — where the typed-relation behavior queries live.** Type registry, shapes, dedup, and behavior *declarations* are in M7; indexed *query execution* (findlinks/count/window) is in M8. But `Observe` (M7-declared) and `findlinks` (M8) overlap heavily, and determinate-walk/reverse-lookup/age could sit on either side. This is the softest seam in the design; the whole link subsystem could also collapse to one module.
- **M9 as one module vs two.** PL + predicate-defs-as-content (the language and its persistence) is arguably a separate responsibility from the reactive rule engine (ASN-0133) written *in* PL. Bundled as "the programmable layer"; splittable into PL-evaluator and rule-engine.
- **Provenance R: distributed vs its own module.** R's authoritative state is in M5 (written by edits); its query family (SHOWDELETIONS, FINDDOCSCONTAINING) is in M6; SHOWORIGIN is pure M1 projection. A dedicated "Provenance & Attribution" module (R + those queries) is defensible, since R is non-recomputable authoritative history and shares the spanfilade *shape* with M8's link index.
- **Transaction kernel (M2): module vs cross-cutting discipline.** Treated as a buildable WAL/MVCC/recovery engine that stores plug into. One could instead make only the MIC *contract* shared and let each store own its own journal/recovery — at the cost of duplicating the recovery story the whole corpus leans on.
