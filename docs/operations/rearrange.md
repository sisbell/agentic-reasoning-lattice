# REARRANGE

| | LM | Green | This project |
|---|---|---|---|
| **Label** | REARRANGE | REARRANGE | (no per-opcode note) |
| **Opcode** | 3 | 3 | — |
| **Source** | LM 4/66-4/67 | `requests.h:24`, `fns.c:159`, dispatch at `init.c:48` | ASN-0065 (retired, pending regen) |
| **Status** | Specified | Shipped | Note retired; structure-bearing properties have been absorbed into ASN-0084 |
| **Deps** | — | — | 34, 36, 47, 53, 58 (substrate-registered `citation.depends`; 0084 not yet registered despite hosting R-PIV/R-PPERM/R-SWP/R-SPERM/R-DISP/R-BLK/R-COMM) |

## What it does

Transpose two regions of text within a document. Per LM 4/66-4/67:

> *"Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3, assuming cut 1 < cut 2 < cut 3. With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4."*

REARRANGE is the most conservative editing operation: nothing is added to the content store, nothing removed, nothing duplicated. Only the V→I mapping is permuted, leaving `ran(M(d))` invariant as a multiset. Two variants in the BNF — 3-cut (adjacent regions swap, *pivot*) and 4-cut (disjoint regions swap, *swap*) — share the same mathematical core: a region-uniform bijective rearrangement of `dom(M(d))`.

## Why this doc covers two variants

LM specifies REARRANGE with `<ncuts>` = 3 or 4, dispatching to pivot or swap semantics in one opcode. They are not three operations like the FIND family (different return shapes) but two semantic variants of one operation (different region configurations producing different permutations). The project's note treats them as a single ASN.

## Structure (ASN-0065 + ASN-0084)

The deprecated note (ASN-0065) frames REARRANGE as **K.μ~ (ArrangementReordering)**: a distinguished composite (K.μ⁻ + K.μ⁺) admitting a bijection π : `dom(M(d))` → `dom(M'(d))` such that `M'(d)(π(v)) = M(d)(v)` for all v.

### State-side properties

- **R-PRE (RearrangePrecondition):** cuts are strictly ordered, share subspace, satisfy depth and ordinality constraints; the interval between bounding cuts is fully contained in `V_S(d)`
- **R-CP (ContentPreservation):** `ran(M(d)) = ran(M'(d))` as multisets — the multiset of I-addresses is invariant
- **R-CF (RearrangeFrame):** content store, other documents, other subspaces unchanged
- **R-DP (ContiguityPreservation):** D-CTG and D-MIN propagate through REARRANGE

### Permutation-structure properties (now in ASN-0084)

Already absorbed into ASN-0084 (Cut-Point Rearrangements; previously titled "Bundle Projection Displacement"):

- **R-PIV (PivotWellDefined)** + **R-PPERM (PivotPermutation):** 3-cut pivot — total function on `V_S(d)`, induced bijection has region-uniform displacement structure
- **R-SWP (SwapWellDefined)** + **R-SPERM (SwapPermutation):** 4-cut swap — same, for disjoint regions
- **R-DISP (DisplacementUniformity):** within each region, the displacement is uniform and determined by region widths alone
- **R-BLK (BlockTransformation):** correspondence-run decomposition transforms by splitting at cuts, classifying runs into regions, reassembling with per-region displacement
- **R-COMM:** cut-point permutation commutes with ordinal shift (used in R-BLK's correctness argument)

When ASN-0065 regens, the new note cites ASN-0084 for these instead of deriving locally.

## LM vs Green divergence

### Opcode and BNF

| | LM | Green |
|---|---|---|
| Opcode | 3 | 3 |
| Name | REARRANGE | REARRANGE |
| Request shape | `<doc id> <cut set>` where `<cut set> ::= <ncuts> <doc vsa>*` with `ncuts = 3 or 4` | matches LM |

No renumbering, no name change, no BNF divergence.

### Safe-mode behavior

REARRANGE is never safe-mode-disabled — it's a core content operation.

### Implementation note

`fns.c` shows a commented-out earlier version of `rearrange()` at lines 143-158 and the active version at 159. The deprecated version suggests the implementation went through at least one rewrite. Worth checking whether the semantics changed (cut-set interpretation, ordering assumptions) between versions.

## Current project state

ASN-0065 went through 5 review cycles before reaching CONVERGED, then was deprecated in the 5-operation batch (2026-05-13) pending regen. The retired note's structure-bearing properties (R-PIV, R-PPERM, R-SWP, R-SPERM, R-DISP, R-BLK, R-COMM) **have already been hoisted into ASN-0084**, which now serves as the rearrangement-displacement layer for any operation that uses cut-point semantics.

On regen, ASN-0065's new note will be substantially **shorter** than the retired one — most of its structural content now lives in ASN-0084. The regen note becomes an application of ASN-0084's primitives to LM's specific 3-cut/4-cut request shape, plus the operation-specific properties (R-PRE wire-shape preconditions, R-CP content preservation, R-CF frame, R-DP contiguity).

## Pending absorptions

REARRANGE has two categories of pending work, distinct in their target layer:

### Foundation-level (universal across operations)

These three sit alongside INSERT's, DELETE's, and COPY's identical set:

- **Shift-increment commutativity → ASN-0034.** Used in R-PPERM/R-SPERM displacement analysis. Same lemma derived in I3, D-SHIFT, C2. See [`insert.md`](insert.md) for full discussion.
- **`ord(v)` / `vpos(S, o)` primitives → ASN-0036.** Re-introduced at line 16 of the retired note **without cross-reference** to DELETE's earlier introduction at ASN-0061. This is the textbook example of why the primitives need to live upstream. See [`deletevspan.md`](deletevspan.md) for full discussion.
- **General contiguity preservation lemma → ASN-0036.** R-DP's proof is the fourth of four parallel derivations across operations. Consolidate to ASN-0036.

### Citation cleanup (ASN-0084 already populated)

The permutation-structure properties were absorbed into ASN-0084 during earlier convergence cycles, but **ASN-0065 still derives them locally**. The cleanup is dependent-side:

- R-PIV → cite ASN-0084
- R-PPERM → cite ASN-0084
- R-SWP → cite ASN-0084
- R-SPERM → cite ASN-0084
- R-DISP → cite ASN-0084
- R-BLK → cite ASN-0084
- R-COMM → cite ASN-0084

This is not absorption work that requires reopening a foundation ASN — the target already has the claims. The work is: when REARRANGE regens, the new note replaces locally-derived statements with citations to ASN-0084. The deprecated note's "Displacement Analysis" section becomes a citation block.

### Sequencing

The foundation-level three batch into the ASN-36 reopen alongside INSERT/DELETE/COPY. The citation cleanup happens automatically during REARRANGE's regen — no other ASN needs to reopen.

## Open questions

- **Depth-restriction generalization.** ASN-0065 restricts to depth-2 V-positions (line 18: *"We restrict to depth-2 V-positions throughout this ASN"*). The note claims this is structurally identical to deeper ordinals via D-CTG-depth (ASN-0036). Verify the generalization is actually carried in ASN-0036, or whether REARRANGE's depth-2 restriction reflects a foundation-level limitation.
- **3-cut vs 4-cut canonical form.** A 3-cut pivot is mathematically expressible as a 4-cut swap with adjacent regions (cut₂ = cut₃). Worth deciding whether the protocol intentionally distinguishes them (front-end ergonomics) or whether 3-cut is a degenerate-case shorthand.
- **Wire interpretation of `<ncuts>`.** The BNF says `ncuts = 3 or 4`. What happens on `ncuts = 0, 1, 2, 5+`? Likely a protocol error, but worth checking Green's actual behavior — could be silent acceptance with undefined semantics.

## Cross-references

- [`catalog.md`](catalog.md) — Full operations inventory; REARRANGE row at opcode 3
- [`insert.md`](insert.md), [`deletevspan.md`](deletevspan.md) — Sibling operations; share the foundation-level absorptions
- LM source: pages 4/66-4/67
- Green source: `channels/gregory/resources/udanax-test-harness/backend/{requests.h, fns.c, init.c}`
- Project notes: `_docuverse/documents/1.1/1/note/ASN-0065-rearrange-operation.md` (retired), `_docuverse/documents/1.1/1/note/ASN-0084-bundle-projection-displacement.md` (active; hosts R-PIV/R-PPERM/R-SWP/R-SPERM/R-DISP/R-BLK/R-COMM)
- Absorption plan: memory `project_operation_absorption_plan.md`, `project_asn36_pending_absorptions.md`
