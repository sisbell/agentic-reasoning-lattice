# Lattice

## Pattern

Agents produce reasoning about a domain. Each unit of reasoning — whether a note or a claim — declares what it depends on and builds on verified foundations below it. Over time, shared concepts emerge: the same definition in two places, the same claim assumed by three different proofs. These shared concepts are extracted into new foundation layers. The units that contained them absorb the shared version and depend on it.

The result is a lattice — not metaphorically, but in the mathematical sense. The structure has two operations that give it algebraic structure:

- **Meet** — when two units share a concept, extract/absorb finds the common ground and makes it explicit as a foundation layer below both. The extracted foundation is the meet: the greatest common element.
- **Join** — when an investigation builds on multiple foundations, it creates a new node above them. Scope promotion creates joins: new units that combine multiple lines of reasoning.

The lattice is not designed — it emerges from the interaction of discovery, refinement, and extraction. Meet and join are not imposed — they are discovered through the patterns operating on the structure.

## Two granularities

The lattice operates at two granularities simultaneously:

**Note-level** — nodes are notes. Edges are note-level dependencies declared in each note's YAML (`depends:`). Discovery operates at this granularity: two data authorities produce notes, scope promotion adds new notes at the edges, extract/absorb restructures notes into layers.

**Claim-level** — nodes are individual claims (theorems, definitions, axioms). Edges are claim-level dependencies declared per-claim (`follows_from:`). Formalization operates at this granularity: review/revise iteration refines each claim, regional review handles tightly coupled clusters, verify the whole checks coherence.

The two are not separate structures. Note-level is a coarser view of the same lattice. Each note contains many claims. Each note-level dependency decomposes into claim-level dependencies once both endpoints are formalized. See [Architecture](../architecture.md) for the full lifecycle and the visibility rule that governs which granularity a given consumer sees.

**Blueprinting bridges the two.** It is [scope narrowing](scope-narrowing.md) + [representation change](representation-change.md) applied together: a note at the note-level becomes many per-claim file pairs at the claim-level. This is how reasoning moves from discovery's note granularity to formalization's claim granularity. The content is the same — the lattice gains resolution.

With [Xanadu protocols](../vision.md), the two granularities collapse into one linked structure. Transclusion lets you view at either scope. A note is a collection of claim links. A claim is a node with links to its dependencies.

## Forces

- **Reasoning accumulates.** Agents discover new topics, produce new reasoning. Without structure, the collection becomes flat and redundant.
- **Shared concepts appear independently.** Two notes define the same foundational operation in slightly different ways. Three proofs assume the same foundational constraint without a shared reference. Duplication breeds inconsistency.
- **Foundations must be stable.** Higher-level reasoning depends on lower-level definitions. If foundations change without propagation, the lattice becomes inconsistent.
- **Structure is discovered, not imposed.** You don't know the layers in advance. The lattice reveals its own structure as reasoning accumulates and shared concepts emerge.

## Composition

The lattice is produced by three patterns operating together:

**[Two data authorities](two-data-authorities.md)** — independent channels produce raw findings about the domain. Theory and evidence reason separately, synthesis integrates. The output is a note with claims mapped to their sources. (Note-level.)

**[Review/revise iteration](review-revise-iteration.md)** — refines each unit to internal coherence. Find issues, fix them, re-check. The unit converges to a state where its claims are consistent and its dependencies are explicit. (Both granularities — notes during discovery, claims during formalization.)

**[Extract/absorb](extract-absorb.md)** — finds shared concepts, factors them into new foundation layers. Units that contained the shared concept absorb the extracted version and declare a dependency on it. Duplication is eliminated; the lattice gains a new layer. (Both granularities.)

## Structure

Demonstration (Xanadu formalization):
```
Note-level:
  foundation layer    [tumbler algebra]    [sequence arithmetic]
                           ↑                      ↑
  structure layer     [strand model]        [bundle algebra]
                           ↑                      ↑
  dynamics layer      [strand displacement] [link projection]

Claim-level (within strand model):
  foundation     [Σ.C]  [Σ.M(d)]  [S8a]  [S8-fin]  [S8-depth]
                    ↑       ↑        ↑       ↑          ↑
  derived        [S3]    [S7]     [D-CTG]  [D-MIN]
                    ↑       ↑        ↑        ↑
  complex        [S5]    [S8]     [D-SEQ]  [ValidInsertionPosition]
```

Each layer depends on the ones below it. Each layer was discovered — not planned. The foundation layer emerged when multiple structure-layer notes independently defined the same arithmetic. The extraction created the layer; the lattice grew downward.

## Growth

The lattice grows through its two operations:

- **Meet (inward)** — extract/absorb discovers shared concepts and creates foundation layers. Two units that independently defined the same thing now depend on a shared definition below them. The lattice deepens.
- **Join (outward)** — scope promotion creates new investigations that build on multiple foundations. An out-of-scope finding becomes a new node connecting to existing nodes. The lattice widens.

Every growth event is one of these two operations. Discovery connects outward (creating joins). Extraction pushes inward (discovering meets). Formalization verifies both — checking that new joins cohere with their foundations and that new meets preserve the reasoning above them.

## Rebase

When a foundation is updated, dependents re-run review/revise to verify they still hold against the new version. This is a **rebase** — not a separate process, but [review/revise iteration](review-revise-iteration.md) + [verify the whole](verify-the-whole.md) triggered by dependency change rather than by internal findings. The lattice structure propagates the trigger: updated foundation → dependents re-verify. This is a self-healing property — damage at any layer (a gap found, an axiom tightened, a definition extracted) propagates upward through dependencies, and each layer re-verifies and adapts through the same rhythm that built it.

Rebase operates at both granularities. At the note level: an updated foundation note triggers re-verification of dependent notes. At the claim level: an updated foundation claim triggers re-verification of dependent claims within the same note (through the cone mechanism) or across notes (through the rebase).

## Leads to

[Review/revise iteration](review-revise-iteration.md) — formalization applies review/revise to the lattice's claims, verifying and tightening what discovery produced.

[Dependency cone](dependency-cone.md) — when claim-level review/revise stalls on tightly coupled clusters within the lattice.

## Applications

### Xanadu lattice

The lattice at the note level currently contains notes organized into layers:

- **Foundation**: ASN-0034 (tumbler algebra) — sequence arithmetic, interval algebra
- **Structure**: ASN-0036 (strand model), ASN-0040 (tumbler baptism) — state model, addressing
- **Dynamics**: operation notes (INSERT, DELETE, REARRANGE, COPY) — state transitions

At the claim level within ASN-0034 there are 62 claims. Within ASN-0036, 32 claims. Each was discovered through blueprinting (representation change from note to claim granularity) and refined through formalization.

Foundation was extracted when ASN-0036 and others independently defined tumbler operations. ASN-0045 was eliminated when its claims were found to be corollaries of ASN-0034. ASN-0047 was restructured into pure transition algebra after extraction pushed bridge definitions down. Each extraction was discovered, not planned.

## Origin

The note-level view emerged during discovery on the Xanadu formalization — notes accumulated, dependencies formed, shared concepts were extracted. The claim-level view emerged during formalization — blueprinting decomposed notes into claims, and formalization revealed the fine-grained dependency structure within each note. The two granularities were recognized when the same patterns (meet, join, rebase) appeared at both scales.
