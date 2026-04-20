# Architecture

Reference for the system's structural architecture. The [glossary](glossary.md) has terse definitions; this document has the full picture — the six-level hierarchy, how the lattice matures, and how notes interact at different stages.

---

## The six-level hierarchy

Six structural levels, each naming a different kind of thing:

![Six-level hierarchy](./diagrams/six-level-hierarchy.svg)

| Level | What it is | Relationship |
|---|---|---|
| **Domain** | Configuration bundle: verifier binding, channel sources, vocabulary firewall | Hosts lattices |
| **Lattice** | Accumulated dependency graph; one per coverage target | Groups campaigns |
| **Campaign** | Bounded research effort; scope-bounded, not time-bounded | Spawns inquiries (1:many) |
| **Inquiry** | One question producing one note | Produces one note (1:1) |
| **Note** | Reasoning document grouping ~20–40 claims on one topic | Contains claims |
| **Claim** | Atomic unit of formal reasoning and verification | Terminal lattice node |

A domain hosts lattices. Campaigns build a lattice by spawning inquiries. Each inquiry produces one note. Notes contain claims. Claims are the atomic lattice nodes.

**Concrete example.** The Xanadu work today is in the software domain. It has one lattice (Xanadu), built by many campaigns. Each campaign registered one or more inquiries. Each inquiry produced one note (an `ASN-NNNN` directory containing ~20–40 claims).

---

## Key terms

**Domain.** Defined extensionally: two bundles that differ in any binding — verifier, channels, vocabulary firewall — are two domains. The domain is what you swap to move the engine from one subject area to another.

**Lattice.** The coverage target that groups campaigns. A domain can host multiple lattices (Xanadu is one; "battery electrolytes" would be another in a science domain). Also the artifact — the accumulated dependency graph whose maturation is described below.

**Campaign.** Ends when its question is answered (verified attachment) or abandoned (negative result). Scope-bounded, not time-bounded. The scope-promotion pattern (out-of-scope findings becoming new inquiries) operates within a campaign. Genuinely new questions spawn new campaigns.

**Inquiry.** The 1:1 relationship with the note is definitional. Inquiry is the unit of work; note is the artifact it produces.

**Note.** A numbered, bounded, self-contained reasoning document in the Dijkstra EWD tradition. The `ASN-NNNN` identifier prefix is a legacy label retained for stable addressing; prose uses "note."

**Claim.** An assertion that can be verified, contested, or refuted. Domain-neutral across software, materials science, mathematics, and engineering. YAML type values (axiom, theorem, lemma, corollary) classify claims by logical role and are already domain-neutral.

---

## The lattice lifecycle

The lattice is one structure that matures from coarse-grained to fine-grained as its notes progress through the pipeline. Three explicit operations gate that maturation.

![Lattice lifecycle transitions](./diagrams/lattice-lifecycle-transitions.svg)

### The three transitions

**Blueprint.** Decomposes the note's claims into individual per-claim files. The claims already exist in the note's prose; blueprinting gives each one its own file. They are not yet referenceable by other notes. The note's internal structure is taking shape; its external surface hasn't changed.

**Promote.** Makes the note's claim set available to formalization-stage consumers. From this point, any note in formalization can reference individual claims in this note via `follows_from`. This is the gate that enables downstream formalization.

**Assemble.** Packages the formalized claims back into the note form. From this point, discovery-stage consumers see the updated note. This is the gate that refreshes the note-level surface.

### The visibility rule

Which granularity a consuming note sees depends on the consumer's stage:

**Consumer in discovery** (e.g., ASN-0040 depends on ASN-0034): sees ASN-0034 as an assembled note. Claim-level changes inside ASN-0034 are invisible until assemble is called. The note boundary is an opaque interface.

**Consumer in formalization** (e.g., ASN-0036 depends on ASN-0034): sees ASN-0034's promoted claim set directly. Claims in ASN-0036 reference specific claims in ASN-0034 by label. The note boundary is transparent.

### Ripple behavior

Changes to a dependency's claims ripple differently depending on the consumer's stage:

**Formalization-stage consumers** see changes after the dependency's blueprint is promoted. Ripple at claim granularity, gated by promote.

**Discovery-stage consumers** see changes after the dependency is reassembled into note form. Ripple at note granularity, gated by assemble.

Nothing ripples automatically. Both transitions are explicit operations.

### Formalization order

A note's dependencies must be promoted before the note itself can formalize against them — you cannot write `follows_from` edges into claims that don't exist yet. The lattice matures bottom-up through the dependency graph: foundations promote first, then the notes that depend on them formalize.

### Two levels of dependency

Both are real and operational, serving different stages:

**Note-level** (`depends: [ASN-NNNN]` in YAML): declared during discovery. Coarse-grained. Tells the system which notes relate to which and determines what gets loaded as foundation context.

**Claim-level** (`follows_from: [<claim-ref>]` per claim): declared during formalization. Fine-grained. These are the edges that get formally verified and constitute the authoritative dependency structure.

### The terminal state

When every note has been formalized, every dependency is claim-to-claim. Note groupings persist as provenance metadata ("these 34 claims originated in ASN-0034") but carry no dependency weight. The terminal lattice is a pure claim graph.

Notes do not retire at a single moment. They retire gradually as their discovery-stage consumers formalize. The last note boundary dissolves when the last consumer formalizes.

---

## Pipeline stages

Discovery → Blueprinting → Formalization → Verification.

The [Review V-Cycle](design-notes/review-v-cycle.md) — local-review, regional-review, full-review — runs inside formalization. "Verification" refers exclusively to the external-verifier stage (Dafny/Alloy in software; experimental replication in science).

## Scale labels

Local / Regional / Full — aligned one-to-one with operator names (`local-review`, `regional-review`, `full-review`).

---
