# INSERT

| | LM | Green | This project |
|---|---|---|---|
| **Label** | INSERT | INSERT | (no per-opcode note) |
| **Opcode** | 0 | 0 | — |
| **Source** | LM 4/66 | `requests.h:21`, `fns.c:84`, dispatch at `init.c:46` | ASN-0059 (retired, pending regen) |
| **Status** | Specified | Shipped | Note retired |
| **Deps** | — | — | 34, 36, 47, 53, 58 (substrate-registered `citation.depends`); **missing**: 82 (Strand Projection Displacement — hosts I3 absorbed from INSERT; see Pending absorptions) |

## What it does

Insert content at a position in a document's arrangement. Per LM 4/66: *"This inserts `<text set>` in document `<doc id>` at `<doc vsa>`. The v-stream addresses of any following characters in the document are increased by the length of the inserted text."*

The operation allocates new content into the I-stream (permanent storage), then shifts V-positions at or beyond the insertion point forward by the inserted width to make room.

## Structure (ASN-0059)

The note frames INSERT as a **composite transition** built from four kernel primitives from ASN-0047 (Transition Model):

- **K.α (Allocate)** — fresh I-addresses with `origin(aᵢ) = d`
- **K.μ⁺ (Map-Extend)** — add new mappings `M(d)(p+k) = aᵢ` for the inserted positions
- **K.μ~ (Map-Shift)** — shift existing mappings at or beyond `p` forward by `n`
- **K.ρ (Record-Provenance)** — record `(aᵢ, d)` provenance pairs

The properties decompose into three groups:

### Content side — what's allocated

- **I0 (FreshContiguousAllocation):** allocate `n` consecutive I-addresses `a₁, ..., aₙ` with `aᵢ = a₁ + (i−1)` and `origin(aᵢ) = d`. Uses T9 (ForwardAllocation) from ASN-0034.

### Arrangement side — how V-positions shift

- **I1 (PreInsertionStability):** content before `p` is unchanged
- **I2 (ContentPlacement):** new content occupies `n` consecutive V-positions starting at `p`
- **I3 (PostInsertionShift):** content at or beyond `p` shifts forward by `n` via ordinal arithmetic on V-positions
- **I4 (SubspaceStability):** V-positions in other subspaces of `d` are untouched
- **I5 (DocumentIsolation):** no other document's arrangement is affected

### Structural side — contiguity, blocks, preconditions

- **I8 (InsertionPrecondition):** legal `p` is either inside `dom(M(d))` or one past the maximum V-position in `V_S`
- **I9 (ContiguityPreservation):** if `V_S` was contiguous before, it remains contiguous after
- **I10 (BlockDecompositionEffect):** the post-INSERT block decomposition can be computed from the pre-INSERT decomposition by a region-split-then-shift operation

### Invariant preservation

P0-P8 — the operation's effect on each system-wide invariant (content permanence, entity permanence, provenance permanence, referential integrity, etc.) is checked individually with the kernel-frame derivations as evidence.

## LM vs Green divergence

### Opcode and name

| | LM | Green |
|---|---|---|
| Opcode | 0 | 0 |
| Name | INSERT | INSERT |

Identical. INSERT is one of the cleanest LM→Green carries: same opcode, same name, same BNF shape.

### Wire format

The LM BNF and Green's wire reader (in `get1.c` / `get1fe.c`) agree on the request shape: `<doc id> <doc vsa> <text set>`. No divergence observed in the test harness.

### Safe-mode behavior

INSERT is never safe-mode-disabled — it's a core content operation that any session needs.

## Current project state

ASN-0059 went through 8 review cycles before reaching CONVERGED, then was deprecated in the 5-operation batch (2026-05-13) pending regen against current foundations. The retired note is high-quality:

- Properties I0-I10 cleanly composed from K-primitives
- Worked example concrete (insert "AB" at position 3)
- Block-decomposition effect explicitly computed
- Full invariant-preservation pass (P0-P8) with kernel-frame citations

When regen happens, the new note will inherit the same shape but with absorption work folded in (see below).

## Pending absorptions

INSERT's deprecated note locally derives or names several properties that belong in foundation ASNs. These were identified during operation-absorption analysis (memory: `project_operation_absorption_plan.md`) and confirmed by reviewing the note's structure.

- **Shift-increment commutativity → ASN-0034.** The identity `shift(v+j, n) = shift(v, n) + j` is used in I3 (post-insertion shift) and I9 (contiguity preservation). Also called the "additive compatibility identity." Independently re-derived in DELETE, REARRANGE, COPY — the **most-repeated derivation in the operation set**. Foundation arithmetic property. Should be in ASN-0034 (Tumbler Algebra) so all operations cite rather than re-derive.

- **General contiguity preservation lemma → ASN-0036.** I9 derives it for INSERT's specific case (one shift, monotonically forward). The general statement — *an order-preserving bijection on a partitioned contiguous range, with each piece shifted by uniform compatible displacement, preserves contiguity* — is independently derived in I9 (INSERT), D-DP (DELETE), R-DP (REARRANGE), C2 (COPY). Should live in ASN-0036 (Strand Model) alongside the existing contiguity definitions, so operations cite a single lemma instead of four parallel derivations.

- **ord(v) / vpos(S, o) primitives → ASN-0036.** `ord(v)` extracts the ordinal component of a V-position; `vpos(S, o)` reconstructs a V-position from a subspace + ordinal. Inverses on the stream's position space. INSERT uses ordinal arithmetic implicitly via I3's shift; DELETE introduced them as named primitives (ASN-0061); REARRANGE re-introduced without cross-reference (ASN-0065). Should be added to ASN-0036's V-position vocabulary alongside `subspace_I`, `V_S(d)`, etc.

### Sequencing

The three absorptions should land in a single ASN-36 reopen pass alongside the L0a → S7e absorption already pending (memory: `project_asn36_pending_absorptions.md`). Batching avoids re-triggering ASN-36's convergence cycle three separate times. The trigger is the operation regen — when fresh INSERT/DELETE/REARRANGE/COPY drafts cite these properties, the absent foundation property will be flagged by review, signaling that ASN-36 needs to reopen and absorb.

### Citation cleanup — extension-then-absorption chain

INSERT's properties were extracted into intermediate "extension" ASNs in 2026-04, several of which have since been absorbed into foundation ASNs. The lattice currently has:

- **OrdinalDisplacement, OrdinalShift, I6, I7** → extracted to ASN-0060 (Tumbler Algebra 0) → absorbed into **ASN-0034**. INSERT's existing citation to 34 reaches them. **No action needed.**
- **I0-I5, I8, I9** → extracted to ASN-0085 (V-Position Ordinal Decomposition) → absorbed into **ASN-0036**. INSERT's existing citation to 36 reaches them. **No action needed.**
- **I3 (PostInsertionShift)** → extracted to ASN-0080 (Span Algebra 0) → absorbed into **ASN-0082 (Strand Projection Displacement)**, which is still **active**. INSERT does not currently cite ASN-0082. **On regen, register `citation.depends` to ASN-0082.**

ASN-0060, ASN-0080, ASN-0085 are all retired now — they should not be cited directly. Verify the current state with `python3 scripts/diagnostics/note_graph.py 59`.

## Open questions

- **Insertion at exactly `v_max + 1` vs APPEND.** INSERT's I8 permits `p = v_max + 1` (one past the maximum existing V-position), which is operationally equivalent to APPEND. LM defines APPEND as a separate opcode (19) but Green never implemented it. Is the equivalence formally provable from I8 + I0–I3, or does APPEND have additional semantics ASN-0059 doesn't capture? Worth confirming on regen.
- **Multi-subspace insertion semantics.** If `p` is in subspace `s`, I4 says other subspaces are untouched. But the BNF only specifies a single `<doc vsa>` — no subspace selector. The note assumes the subspace is implicit in `p`'s tumbler structure. Verify Green's wire-format actually disambiguates subspace from `p`.

## Cross-references

- [`catalog.md`](catalog.md) — Full operations inventory; INSERT row at LM opcode 0
- LM source: page 4/66
- Green source: `channels/gregory/resources/udanax-test-harness/backend/{requests.h, fns.c, init.c}`
- Project note: `_docuverse/documents/1.1/1/note/ASN-0059-insert-operation.md` (retired, pending regen)
- Absorption plan: memory `project_operation_absorption_plan.md`, `project_asn36_pending_absorptions.md`
