# Lattice-Genesis Maturation Stigmergic Protocol

How a new lattice comes into being and reaches a state where its first note can enter the [Note-to-Claim Maturation Stigmergic Protocol](./note-to-claim.md).

This document specifies the **Lattice-Genesis Maturation Stigmergic Protocol** — the protocol that *precedes* Note-to-Claim in the maturation family. Where Note-to-Claim drives content from inquiry to ASN-quiescence, Lattice-Genesis drives content from "scout signal" to "first note ready to enter Note-to-Claim." It composes the same substrate primitives (R0–R7, Sh0–Sh5, PC0–PC6, AG0–AG7, Run0–Run5) and is governed by the same Stigmergic Protocol primitives (Correction, Marker, Self-Review, Cycle).

The pipeline:

> *scout discovers signal* → lattice doc created → canonical agent corpus provisioned → first note drafted → **hand-off to Note-to-Claim Maturation**

Lattice-Genesis is shorter than Note-to-Claim and lives "below" it on the maturation timeline: when L3 fires, the new note enters Note-to-Claim's Stage 1 (Inquiry → Confirmed Note). The two protocols compose, sharing substrate state.


## The arc at a glance

```
Scout signal (bridge probe, operator scout)
   │ create-lattice agent-tool                   (operator/scout-invoked CLI)
   ▼
Lattice doc exists in substrate
   │ LatticeBootstrapAgent                       (stigmergic, per-canonical-spec)
   │ — fires until canonical corpus provisioned
   ▼
Lattice bootstrapped (canonical corpus present)
   │ NoteSpawnAgent                              (TBD — drafts first note from scout's seed)
   ▼
First note exists in lattice
   │ — hand-off to Note-to-Claim Maturation Stage 1
   ▼
... Note-to-Claim continues to ASN-level lattice quiescence (per Q10's CanonicalScopeTiers) ...
```


## L-tier ladder

The protocol's progress is recognized by the substrate at four tiers below Note-to-Claim's Stage 1:

| Tier | State | Recognized by |
|------|-------|---------------|
| **L0** | Scout signal exists | Substrate state TBD — could be a `bridge.candidate` doc, an operator's intent flag, or implicit (scout decides in-prompt without substrate signal). |
| **L1** | Lattice doc exists | A doc at `_docuverse/documents/<node>/<user>/lattice/<name>.md` is registered in `paths.json`. |
| **L2** | Lattice bootstrapped | Every canonical agent spec in `lattice-bootstrap/agents/` has a corresponding doc registered for this `(node, user)` subtree, each carrying `agent` + `agent.caste.<v>` + `agent.scope.<v>` classifiers. |
| **L3** | First note drafted | At least one doc with the `note` Classifier exists in this lattice (linked to the lattice doc via the `lattice` membership type). |

L3 is the hand-off point. Once a note exists in the new lattice, the existing Note-to-Claim Maturation Stigmergic Protocol takes over — `note_review`, `note_consult`, `note_revise`, `note_statements`, `claim_decompose`, ... all the way to ASN-level lattice quiescence (per Q10's CanonicalScopeTiers).


## Stage 1 — L0 → L1: scout creates lattice doc

The L0→L1 transition is **operator/scout-invoked**, not predicate-fired. A scout (or an operator acting as scout) decides a new lattice should exist and invokes:

```
python scripts/agent_tools/create-lattice.py --name <new-name>
```

The tool inherits its `(node, user)` from the calling agent's authorial space (read from `XANADU_AGENT_DOC` env var, with `LATTICE` env var as fallback). Cross-`(node, user)` lattice spawning is intentionally not supported by this tool — the new lattice must live in the same authorial space as the scout that spawns it, at least initially.

What the tool does in one invocation:

1. Resolve calling scout's `(node, user)` from `XANADU_AGENT_DOC`.
2. Validate the new lattice name (single path segment, no clash with existing lattice docs in the same `(node, user)` subtree).
3. Write `_docuverse/documents/<node>/<user>/lattice/<name>.md` with frontmatter:

   ```yaml
   ---
   label_prefix: ASN
   default_campaign: <optional>
   ---
   ```

4. `register_path(rel)` — the account-aware allocator gives a tumbler in the calling scout's user-space (e.g., xanadu's scout creates a sibling lattice under `1.1/1/`).
5. (By default) invoke `LatticeBootstrapAgent` to drive Stage 2 to quiescence in the same process.
6. Print the new lattice doc's tumbler address on stdout for the calling prompt to capture.

**Why operator/scout-invoked rather than predicate-fired:** L0 is the most subtle tier — the substrate signal that "a new lattice should exist" is design-dependent. Today the decision lives in the scout's prompt logic; the substrate sees only the eventual `create-lattice` write. A predicate-fired version would require defining what L0 looks like in substrate (e.g., a `bridge.candidate` doc emitted by a runner-walked bridge probe). That is deferred until the scout-side signal protocol is settled.


## Stage 2 — L1 → L2: bootstrap canonical corpus

Once a lattice doc exists, `LatticeBootstrapAgent` (Family D producer, lattice-scoped) provisions the canonical agent corpus into the new lattice's authorial subtree. Per-fire scope: one canonical spec.

### Predicate

`is_lattice_bootstrapped(session, specs, node, user)` — True iff every canonical spec name from `lattice-bootstrap/agents/` resolves to a registered path under `_docuverse/documents/<node>/<user>/agent/`.

When the predicate is False, the runner (or the CLI in walk-mode) re-fires the agent. When True, the agent skips and the protocol advances to L3.

### Per-fire identity grant

For the first canonical spec whose target path is unregistered, the agent:

1. Writes the spec body to `_docuverse/documents/<node>/<user>/agent/<role>.md`.
2. `register_path(rel)` — allocator gives a doc tumbler in `<node>.<user>.0.X` (the active account's space).
3. Emits `agent` Classifier on the agent doc (F=∅, G=[doc]).
4. Emits `agent.caste.<value>` Classifier from the spec's frontmatter.
5. Emits `agent.scope.<value>` Classifier from the spec's frontmatter (skipped if no scope declared).

### Stigmergic hand-off

The fire flips `is_lattice_bootstrapped`'s answer for the just-provisioned spec. The next runner pass picks up the next missing spec, until the predicate stays True across a pass and the protocol advances.

### Sibling-lattice sharing (current behavior)

When sibling lattices co-reside in one `(node, user)` subtree (e.g., a new lattice spawned by a xanadu scout shares xanadu's space), the canonical agent corpus is **shared by path**. The predicate sees all canonical agents already provisioned (because xanadu provisioned them first) and fires zero times for the new sibling. This is intentional today — sibling lattices share the agent-doc layer. If isolation is desired later, the partition would need to extend below `(node, user)` (e.g., `documents/<node>/<user>/<lattice>/...`).


## Stage 3 — L2 → L3: spawn first note (TBD)

Once the lattice is bootstrapped, the protocol calls for a `NoteSpawnAgent` (TBD) that drafts the first note in the new lattice. This stage is not yet built.

### What's needed

- **Substrate signal for "lattice has no notes yet."** A predicate that reads paths.json for note-classified docs in the lattice's `(node, user)` subtree.
- **A scout-supplied seed.** The scout's intent at L0 (what the new lattice is *for*) has to persist into substrate so a NoteSpawnAgent can read it. Candidate shape: an optional `seed:` frontmatter field on the lattice doc, or a `bridge.candidate` doc that the create-lattice tool can carry forward.
- **NoteSpawnAgent.** Family D one-shot identity grant that fires when the lattice has no notes and a seed exists. Drafts the first note by invoking the equivalent of `note_draft`'s LLM machinery, scoped to the seed.
- **Hand-off into Note-to-Claim Stage 1.** The new note carries the `note` Classifier; `note_review` (the first stigmergic agent of Stage 1 in Note-to-Claim) fires on the next runner pass. The protocol-boundary is just substrate state — no special hand-off mechanism needed.


## Hand-off to Note-to-Claim Maturation

L3 is the entry point to Note-to-Claim's Stage 1 (Inquiry → Confirmed Note). Once at least one `note`-classified doc exists in the new lattice, Note-to-Claim's Stage 1 begins driving it toward `is_doc_quiescent ∧ is_claim_confirmed`. From that point onward, the lattice's content matures through Note-to-Claim until ASN-level lattice quiescence (per Q10's CanonicalScopeTiers).

There is no special protocol-glue. The two protocols compose through shared substrate state.


## Termination

Lattice-Genesis terminates at L3 (first note drafted). The lattice is then "alive" — Note-to-Claim takes over.

The full multi-protocol composition's termination is at ASN-level lattice quiescence (per Q10's CanonicalScopeTiers) of Note-to-Claim, run per-note that the lattice eventually accumulates.


## What's currently built

| Tier | Built? | Implementation |
|------|--------|----------------|
| L0 → L1 | ✓ | `scripts/agent_tools/create-lattice.py` |
| L1 → L2 | ✓ | `LatticeBootstrapAgent` (lib/agents/producers/lattice_bootstrap.py); `scripts/lattice-bootstrap.py` walks fires-until-quiescence; create-lattice optionally invokes the agent |
| L2 → L3 | ✗ | NoteSpawnAgent not yet built |

Plus supporting infrastructure landed in the unified-docuverse arc:

- `agent.scope.lattice` substrate type (lib/backend/types.py)
- Account-aware allocator (lib/backend/store.py): per-author tumbler subspaces
- `(node, user)` filesystem partition under `_docuverse/documents/`
- Lattice config in lattice-doc frontmatter (lib/lattice/config.py)
- `--lattice <name>` CLI argument resolved centrally in lib/shared/paths.py


## Open design questions

1. **Substrate signal for L0.** Today L0 is opaque to substrate — only the eventual `create-lattice` write is visible. To make L0 substrate-driven (predicate-fired bridge probe → lattice creation), we need a `bridge.candidate` shape (or similar) and a runner-walked agent that fires `create-lattice` from substrate state. Deferred until the scout-side signal design is settled.

2. **Seed persistence for L2 → L3.** The scout's intent at L0 needs to reach NoteSpawnAgent at L2. Candidates: lattice-doc frontmatter `seed:` field, a separate `bridge.candidate` doc that survives across stages, or scout-provided argument to `create-lattice` that lands in the lattice doc.

3. **Single protocol vs. composing protocols.** Lattice-Genesis and Note-to-Claim share substrate state but are documented separately. Whether they should be unified into one document with extended tier (L0…Q10) or stay as two composing protocols is a documentation choice — runtime behavior is the same either way.

4. **Sibling-lattice agent-doc sharing.** Current behavior: lattices in the same `(node, user)` share the canonical agent corpus by path. Intentional today, but may need a deeper partition (`documents/<node>/<user>/<lattice>/...`) if lattices need isolated agent docs.

5. **`lattice` Classifier on lattice docs.** Today `lattice` is a membership link type (member → lattice doc). There's no separate "this doc IS a lattice" classifier. Substrate-level "find all lattice docs" queries would need this; deferred until the use case arises.