# Foundations — Verified Building Blocks

A foundation ASN is one whose definitions are needed by every (or nearly every) downstream ASN. Without shared foundations, each ASN reinvents the same concepts in incompatible notation — ASN-0002 and ASN-0025 both specified address permanence but defined different state models (`ispace` vs `iota`, `Addr` vs `IAddr`, `vspace` vs `v`). Properties from one could not be referenced by the other.

Foundations solve this by establishing verified, shared definitions. Their formal statements are injected into every review, revise, and discovery prompt so that downstream ASNs build on them rather than reinventing them.

## The Three Layers

The universal foundations form a dependency stack: types → state → invariants.

| Layer | ASN | Provides | Depends on |
|-------|-----|----------|------------|
| **Types** | ASN-0001 | Tumbler algebra, ordering, arithmetic, subspaces, spans | — |
| **State** | ASN-0026 | Σ.I, Σ.V(d), Σ.D, refs(a), +_ext, operations classification | ASN-0001 |
| **Invariants** | ASN-0027 | I-Space Frame, operation specs (DELETE/REARRANGE/COPY/VERSION), reference permanence, reachability | ASN-0001, ASN-0026 |

Each layer depends only on the layers above it. Every downstream ASN needs all three:

- Any ASN that mentions addresses needs ASN-0001's type system.
- Any ASN that mentions system state needs ASN-0026's model.
- Any ASN that specifies an operation must verify it against ASN-0027's I-Space Frame and permanence invariants.

## Why These Three Layers

The layers are not arbitrary groupings — each resolves a specific design tension that every downstream ASN inherits.

### Types (ASN-0001): What addresses are

Tumblers give addresses structure — ordering, arithmetic, prefix relationships, subspace membership. Without a shared type system, each ASN invents its own position algebra. ASN-0002 used `Addr` with a `text_subspace()` function; ASN-0025 used `IAddr` with tagged ordinals. Both were deprecated — the incompatible notation was the direct cause. ASN-0027 (Address Permanence) replaced them both, building on the shared foundations instead of reinventing them. The type system is the syntax of the specification — the alphabet from which all other statements are composed.

### State (ASN-0026): The dual-space architecture

The I-space/V-space separation is the generative architectural decision. Nelson identified a fundamental tension: **permanent citation** (an address given today resolves to the same content forever) and **free editing** (users insert, delete, and rearrange without constraint) are mutually exclusive under a single address space. If addresses are positions, INSERT at position `p` invalidates every citation to `p+1` and beyond.

The resolution: separate identity from arrangement. Content has a permanent I-address (what it IS) and a mutable V-position (where it APPEARS). No operation changes I-addresses. Editing only changes V-positions.

This is foundational because every downstream property presupposes it:

| Property | Depends on I/V separation because |
|----------|----------------------------------|
| Transclusion | COPY works because multiple V-positions can point to the same I-address. Without separation, copying means duplicating — no shared identity. |
| Versioning | CREATENEWVERSION creates a new V-space over the same I-addresses. Without separation, a version is a full copy with no structural connection to the original. |
| Correspondence | "Same content in two documents" means same I-address. Without separation, you need byte comparison — identical content created independently is indistinguishable from transcluded content. |
| Link permanence | Links attach to I-addresses. V-space editing cannot break them. Without separation, every edit risks breaking every link. |
| Non-invertibility | DELETE+INSERT ≠ identity because INSERT allocates fresh I-addresses. This distinguishes "same content" from "identical-looking content." |
| Provenance | Content origin IS its I-address. Without separation, provenance requires a separate tracking system. |

Nelson's phrase captures it: "content identity is based on creation, not value." Two independently typed identical paragraphs have different I-addresses. Transcluded content shares the same I-address. Only the dual-space architecture makes this distinction expressible.

ASN-0026 sits at the State layer not because it defines a convenient data model, but because it defines the semantic structure that every other property presupposes — the way a type system defines not "how we store values" but "what values mean."

### Invariants (ASN-0027): What no operation may do

The I-Space Frame and permanence invariants constrain all operations jointly. Without them, each operation ASN must independently re-derive what operations can and cannot do to I-space — and risk inconsistency. ASN-0027 establishes the master constraint once: I-space is append-only, only INSERT extends it, and every reference to an I-address resolves to unchanged content in all future states.

## Domain Foundations

Not every foundation is universal. Some are needed by a subset of downstream ASNs.

| ASN | Provides | Needed by |
|-----|----------|-----------|
| ASN-0011 | Accounts, owner(d), document creation | ASN-0007 (links need owner), operation ASNs |
| ASN-0007 | Link datatype, endsets, spanindex, discovery | Operation ASNs (link frame conditions) |

ASN-0011 depends on Tier 1 only. ASN-0007 depends on Tier 1 and ASN-0011.

These can be added to the foundation list when they converge. The flat injection mechanism works for up to 5 ASNs within the token budget. Beyond that, selective injection (per-ASN dependency mapping) becomes worth considering.

## Dependency Graph

```
ASN-0001  Tumbler Algebra           ← types
    |
ASN-0026  I-Space and V-Space      ← state
    |
ASN-0027  Address Permanence        ← invariants
    |
    ├── ASN-0011  Document Lifecycle    ← domain
    |       |
    └── ASN-0007  Links and Endsets     ← domain
            |
        Operations  (ASN-0004/5/6/17)
```

## What Makes an ASN a Foundation

The test: if you removed it from the foundation list, would the next ASN you draft define its own version of the same concepts?

- Remove ASN-0001 → every ASN reinvents tumbler ordering. Foundation.
- Remove ASN-0026 → every ASN reinvents the state model. Foundation.
- Remove ASN-0027 → every operation ASN re-specifies permanence and the I-Space Frame. Foundation.
- Remove ASN-0011 → only ASNs about documents or ownership are affected. Domain foundation.
- Remove ASN-0007 → only ASNs about link behavior are affected. Domain foundation.

This connects to [Methodology](methodology.md) principle 3 (vocabulary as abstraction enforcement): foundations enforce shared vocabulary at the prompt level, preventing notation drift the same way type systems prevent type drift.

Qualification criteria:

1. Converged through the review cycle (VERDICT: CONVERGED)
2. Dafny proofs verified and promoted to `vault/proofs/`
3. Formal statements extracted to `vault/3-modeling/formal-statements/`
4. Defines types, state, or invariants that multiple downstream ASNs reference

## How Foundations Are Injected

Foundation ASNs are identified by their project model definition: any ASN with a `covers` field in `vault/project-model/ASN-NNNN.yaml` is a foundation.

1. `scripts/lib/foundation.py` scans `vault/project-model/` for YAML files with a `covers` field
2. For each foundation ASN, it loads formal statements from `vault/3-modeling/formal-statements/`
3. The formatted statements are injected into three prompt entry points:
   - **Review** (`review_check.py`) — via `{{foundation_statements}}` template variable
   - **Revise** (`review_revise.py`) — appended as a foundation section
   - **Discovery** (`draft_discover.py`) — appended as a foundation section
4. The review prompt allows foundation ASN references and flags reinvention of foundation-defined notation as a REVISE item

Additionally, the `covers` text is used by the question filter to prevent downstream ASNs from re-asking what foundations already establish. Each downstream ASN's `depends` and `excludes` fields control which ASNs' coverage is filtered.

## Adding a Foundation

1. Converge the ASN through review/revise
2. Run the modeling pipeline (proof index → statements → Dafny)
3. Promote proofs to `vault/proofs/`
4. Verify formal statements exist: `vault/3-modeling/formal-statements/ASN-NNNN-statements.md`
5. Add a `covers` field to `vault/project-model/ASN-NNNN.yaml`
6. Update `vault/1-promote/asn-status.md` to reflect foundation status

## Token Budget

| Foundation | Statement size |
|------------|---------------|
| ASN-0034 | ~3.8k tokens |

The flat injection mechanism holds comfortably for 3-5 foundation ASNs (~15k tokens total). Beyond that, selective injection via per-ASN `depends` fields becomes worth considering.

## Design Decisions

**Why flat injection, not per-ASN dependencies?** Simplicity. The token cost of injecting all foundations is small relative to the prompt budget. Per-ASN dependency mapping adds complexity for minimal savings. The `depends` field in project-model already tracks which ASNs need which foundations — selective injection can be added when the foundation set grows.

**Why formal statements, not full ASN text?** Statements are compact — 1-4k tokens each. Full ASNs are 15-90k. The statements contain the formal definitions and properties; the prose reasoning is not needed by downstream ASNs.

**Why project-model, not a central list?** Each ASN's foundation status lives with its definition. No shared mutable file — important when multiple worktrees run concurrent ASNs. The `covers` field doubles as the question filter's exclusion source.

## Related Documents

- [Pipeline Overview](pipeline-overview.md) — where foundations fit in the overall pipeline
- [Modeling](modeling.md) — proof imports, statement extraction, Dafny generation
- [Methodology](methodology.md) — design principles, especially vocabulary enforcement
- [Review](review.md) — how reviews check consistency with foundations
