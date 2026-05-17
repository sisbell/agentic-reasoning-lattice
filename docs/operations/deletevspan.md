# DELETEVSPAN

| | LM | Green | This project |
|---|---|---|---|
| **Label** | DELETEVSPAN | DELETEVSPAN | DELETE Operation (note title) |
| **Opcode** | 12 | 12 | — |
| **Source** | LM 4/66 | `requests.h:29`, `fns.c:333`, dispatch at `init.c:53` | ASN-0061 (retired, pending regen) |
| **Status** | Specified | Shipped | Note retired |
| **Deps** | — | — | 34, 36, 43, 47, 53, 58 (substrate-registered `citation.depends`); **missing**: 82 (Strand Projection Displacement — hosts D-SHIFT/D-BJ/D-SEP absorbed from DELETE; see Pending absorptions) |

## What it does

Remove a span of content from a document's arrangement. Per LM 4/66: *"This removes the given span from the given document."*

In a system where the content store is append-only and every allocated I-address is permanent, "deletion" cannot mean destruction. It means removal of the arrangement mapping: V-positions referencing the deleted span are excised from the document's Vstream, and surviving positions close the gap. Nelson: *"the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included"* [LM 4/11].

## Structure (ASN-0061)

The note frames DELETE as a **composite transition** built primarily from one kernel primitive (K.μ⁻ Map-Restrict) plus the arrangement-shift discipline that closes the gap. The properties decompose into four groups:

### Foundation invariants the operation must preserve

- **D-CTG (VContiguity, ASN-0036):** within each subspace, V-positions form a contiguous ordinal range. DELETE assumes and preserves this.
- **D-MIN (VMinimumPosition, ASN-0036):** the minimum V-position in each non-empty subspace is `[S, 1, ..., 1]`. DELETE assumes and preserves this.

### Locally defined primitives

- **ord(v)** = `[v₂, ..., vₘ]` — extract the ordinal component of a V-position (strip the subspace identifier)
- **vpos(S, o)** = `[S, o₁, ..., oₖ]` — reconstruct a V-position from a subspace + ordinal
- **w_ord** = ordinal projection of a V-depth displacement
- Inverses: `ord(vpos(S, o)) = o` and `vpos(subspace(v), ord(v)) = v`

### Arrangement effects (the three-region partition L / X / R)

- **D-PRE (DeletePrecondition):** the span to delete must be a valid sub-range of an existing subspace's contiguous occupancy
- **D-LEFT (LeftInvariance):** positions left of the deleted span are unchanged
- **D-SHIFT (RightShift):** positions right of the deleted span survive with their I-addresses but shift left by `w_ord` via `σ(v) = vpos(S, ord(v) ⊖ w_ord)` (TumblerSub at the ordinal layer)
- **D-DOM (PostStateDomain):** the post-state domain in subspace S is exactly L ∪ σ(R)

### Frame conditions and structural correctness

- **D-CF (ContentFrame):** content store unchanged
- **D-XD (CrossDocumentFrame):** other documents unaffected
- **D-XS (SubspaceConfinement):** other subspaces of `d` unaffected
- **D-IID (DocumentIdentity):** `d` itself persists
- **D-BJ (ShiftBijectivity):** σ is order-preserving bijection R → Q₃
- **D-SEP (GapClosure):** minimum shifted ordinal equals `ord(p)` — no gap, no overlap with L
- **D-DP (ArrangementStructurePreservation):** D-CTG and D-MIN propagate through DELETE
- **D-WR (WidthReduction):** the extent of `M_S(d)` decreases by exactly `w_ord`
- **D-BLK (BlockTransformation):** post-DELETE block decomposition computable from the pre-state decomposition by removing X-region blocks and shifting R-region blocks

## LM vs Green divergence

### Name mismatch (project-side)

The LM and Green names are **DELETEVSPAN**. The project's deprecated note titles itself "DELETE Operation" and uses "DELETE" throughout. Functionally identical, but the canonical wire name is DELETEVSPAN — the note's title elides the "VSPAN" suffix that signals "delete by V-span specification." When the regen happens, worth deciding whether to align the note title with the LM/Green name or keep the shorter "DELETE."

### Opcode and BNF

| | LM | Green |
|---|---|---|
| Opcode | 12 | 12 |
| Name | DELETEVSPAN | DELETEVSPAN |
| Request shape | `<doc id> <span>` | matches LM |

No renumbering. No name change at the wire. No BNF divergence observed.

### Safe-mode behavior

DELETEVSPAN is never safe-mode-disabled — it's a core content operation.

## Current project state

ASN-0061 went through 5 review cycles before reaching CONVERGED, then was deprecated in the 5-operation batch (2026-05-13) pending regen. The retired note is high-quality:

- Three-region partition (L / X / R) gives clean structural decomposition
- Ordinal extraction (`ord(v)`, `vpos(S, o)`) introduced as named primitives here for the first time across operations
- Shift correctness factored into two independent lemmas (D-BJ bijectivity, D-SEP gap closure)
- Block-decomposition transformation explicitly stated (D-BLK)
- Full invariant preservation pass with D-CTG/D-MIN propagation through D-DP

A subsequent extension ASN-0081 (DELETE backward shift extraction) was created during convergence to handle the backward-shift derivation more rigorously. ASN-0081 derives shift-increment commutativity locally — flagged by reviewer during cycle 13 as "used without derivation in D-SHIFT." The local derivation is a symptom of the missing foundation-level lemma; see Pending absorptions.

## Pending absorptions

DELETE is the **origin point for two foundation-level primitives** that several other operations also need. Resolving these absorptions removes redundancy across DELETE, REARRANGE, COPY, and likely future operations.

- **`ord(v)` / `vpos(S, o)` primitives → ASN-0036.** DELETE introduces these as named operations on V-positions (lines 31-45 of the retired note). REARRANGE (ASN-0065) re-introduces them without cross-reference. INSERT uses ordinal arithmetic implicitly via I3's shift. Every operation that touches V-position arithmetic needs these. Belong in ASN-0036 (Strand Model)'s V-position vocabulary alongside `subspace_I`, `V_S(d)`, etc. Memory: `project_asn36_pending_absorptions.md` already tracks this absorption.

- **Shift-increment commutativity → ASN-0034.** D-SHIFT's σ function uses TumblerSub at the ordinal layer; the bijectivity argument (D-BJ) and the verification of D-BLK's σ(v) + j = σ(v + j) identity both depend on the additive compatibility `shift(v+j, n) = shift(v, n) + j` (and its TumblerSub analog). Reviewer flagged this as "used without derivation in D-SHIFT" during cycle 13. ASN-0081 derives it locally; should move down to ASN-0034. Foundation arithmetic.

- **General contiguity preservation lemma → ASN-0036.** D-DP's proof that DELETE preserves D-CTG is one of four independent derivations across operations. The shared statement: an order-preserving bijection on a partitioned contiguous range, with each piece shifted by uniform compatible displacement, preserves contiguity. INSERT, REARRANGE, and COPY all derive it locally. Consolidate to ASN-0036.

### Sequencing

These three absorptions land alongside INSERT's identical set in a single ASN-36 reopen pass, plus the L0a → S7e absorption already pending. Batching is the operator-confirmed strategy (`project_asn36_pending_absorptions.md`).

DELETE is special because **the ord/vpos primitives originate here** — when ASN-36 absorbs them, DELETE's note loses its "Ordinal Extraction" section entirely (it becomes a citation to ASN-36). This is the largest single deletion any of the four operations will see in regen.

### Citation cleanup — extension-then-absorption chain

DELETE's properties were extracted into intermediate "extension" ASNs in 2026-04, several of which have since been absorbed into foundation ASNs. The lattice currently has:

- **D-CTG (VContiguity)** → extracted to ASN-0066 (Streams 0) → absorbed into **ASN-0036**. DELETE's existing citation to 36 reaches it. **No action needed.**
- **ord(v), vpos(S, o), w_ord** → extracted to ASN-0085 (V-Position Ordinal Decomposition) → absorbed into **ASN-0036**. DELETE's existing citation to 36 reaches them. **No action needed.**
- **D-SHIFT (RightShift), D-BJ (ShiftBijectivity), D-SEP (GapClosure)** → extracted to ASN-0081 (Span Algebra 1) → absorbed into **ASN-0082 (Strand Projection Displacement)**, which is still **active**. DELETE does not currently cite ASN-0082. **On regen, register `citation.depends` to ASN-0082.**

ASN-0066, ASN-0081, ASN-0085 are all retired now — they should not be cited directly. Verify the current state with `python3 scripts/diagnostics/note_graph.py 61`.

## Open questions

- **TumblerSub well-definedness at the foundation layer.** D-SHIFT uses TumblerSub (TA2, TA3-strict from ASN-0034). The DELETE note carefully checks the precondition `ord(v) ≥ w_ord` at restricted depth 2 (line 122 of the retired note). Worth verifying that ASN-0034's TumblerSub axioms are stated generally enough to discharge the precondition at arbitrary depth, or whether DELETE's restriction to depth 2 reflects a foundation-level limitation.
- **Multi-subspace span deletion.** D-XS (SubspaceConfinement) says other subspaces are untouched. But the BNF `<span>` is a single tumbler-pair — can a span legally cross subspace boundaries in V-space? The note assumes not (the span is within a single subspace). Verify Green's behavior matches.
- **Orphaning of content.** When DELETE removes V-positions, the I-addresses they referenced may no longer be reachable from any V-position in any document — content becomes "orphaned." The note discusses this as DELETE-specific semantics; not formally captured as a postcondition. Worth deciding whether orphan reachability deserves a property (e.g., D-ORPHAN) or remains commentary.

## Cross-references

- [`catalog.md`](catalog.md) — Full operations inventory; DELETEVSPAN row at opcode 12
- [`insert.md`](insert.md) — Sibling operation; shares the three absorption candidates
- LM source: page 4/66
- Green source: `channels/gregory/resources/udanax-test-harness/backend/{requests.h, fns.c, init.c}`
- Project note: `_docuverse/documents/1.1/1/note/ASN-0061-delete-operation.md` (retired, pending regen)
- Extension: ASN-0081 (DELETE backward shift extraction) — derives shift-increment commutativity locally; absorbed into ASN-0034 batch
- Absorption plan: memory `project_operation_absorption_plan.md`, `project_asn36_pending_absorptions.md`
