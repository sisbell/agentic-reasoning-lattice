# COPY

| | LM | Green | This project |
|---|---|---|---|
| **Label** | COPY | COPY | (no per-opcode note) |
| **Opcode** | 2 | 2 | — |
| **Source** | LM 4/67 | `requests.h:23`, `fns.c:35`, dispatch at `init.c:45` | ASN-0067 (retired, pending regen) |
| **Status** | Specified | Shipped | Note retired |
| **Deps** | — | — | 34, 36, 43, 47, 53, 58 (substrate-registered `citation.depends`) — all required extension absorptions are already reached via foundation citations |

## What it does

Place existing Istream content at a position in a document's Vstream — Nelson's *transclusion*. Per LM 4/67: *"The material determined by `<spec set>` is copied to the document determined by `<doc id>` at the address determined by `<doc vsa>`."*

The name "copy" misleads: nothing is duplicated. The same I-addresses are referenced from a new V-position. From LM 2/36:

> *"No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents."*

This is the operation that gives Xanadu its defining property — content shared across documents through reference, not duplication.

## Structure (ASN-0067)

COPY is the only operation whose K-primitive composition **excludes** K.α (content allocation). It is a pure-arrangement transition composed of K.μ⁻ (arrangement contraction at the target if needed), K.μ⁺ (arrangement extension), and K.ρ (provenance recording).

### The fundamental constraint

- **C0 (ArrangementOnly):** `C' = C` — the content store is entirely in the frame. COPY allocates nothing.
- **C0a (AllocationInvariance):** for any document d', the set of I-addresses allocated under d' is unchanged. A subsequent INSERT receives addresses contiguous with whatever was last allocated, as if the COPY never occurred.

### Source resolution + placement

COPY resolves a content reference (per ASN-0058's resolution machinery — the same mechanism used by FINDLINKS) into I-address runs, then places those runs at the target V-position:

- **C4 (Displacement):** after COPY at position v with total width w, V-positions at or beyond v shift forward by w
- **C5 (NoOverwrite):** every I-address in the pre-state arrangement is preserved in the post-state — no content is lost, only relocated
- **C2 (ContiguityPreservation):** D-CTG propagates through COPY
- **C2a (MinimumPreservation):** D-MIN propagates through COPY

### The transclusion property

This is what makes COPY distinct from INSERT:

- **C6 (IdentityPreservation):** for each placed block γⱼ = (v + offsetⱼ, aⱼ, nⱼ), the I-addresses `aⱼ + k` are the **same I-addresses** as the source's. Transclusion-by-reference, not by value.
- **C7 (OriginInvariance):** every I-address placed by COPY retains its original `origin` — transcluded content does not become "native" to the target document
- **C7a (NativeStability):** pre-existing V-positions in the target document don't change their native/included classification

### Invariant preservation

- **C3 (InvariantPreservation):** the COPY composite preserves every foundational invariant (state invariants S0-S9, provenance P0-P8, link-store invariants L0-L14)

## LM vs Green divergence

### Opcode and BNF

| | LM | Green |
|---|---|---|
| Opcode | 2 | 2 |
| Name | COPY | COPY |
| Request shape | `<doc id> <doc vsa> <spec set>` | matches LM |

No renumbering, no name change, no BNF divergence.

### Implementation note

`fns.c:35` shows the canonical implementation; lines 50-67 contain a commented-out "kluged unix version for speed" with different ordering — the response is sent (`putcopy`) before the work is done (`docopy`). Lint comments suggest known issues at that path. The kluged version was not active in distribution. Worth a finding doc on optimization-vs-correctness tradeoffs.

### Safe-mode behavior

COPY is never safe-mode-disabled — it's a core content operation.

## Current project state

ASN-0067 went through 5 review cycles before reaching CONVERGED, then was deprecated in the 5-operation batch (2026-05-13) pending regen. The retired note is high-quality:

- C0/C0a establish the operation's defining "no allocation" property and its consequence for the allocator
- Source resolution explicitly reuses ASN-0058's content-reference resolution (the same `resolve(R)` machinery FINDLINKS uses)
- Identity and origin invariance (C6, C7, C7a) capture the transclusion semantics formally
- Invariant preservation (C3) is a full pass over S0-S9, P0-P8, L0-L14 with kernel-frame derivations

The note's C7 (OriginInvariance) is essentially the COPY-specific application of ASN-0058's M16a (OriginInvarianceUnderShift, *"ordinal increment never crosses the document prefix"*). This is a citation-cleanup candidate — see Pending absorptions.

## Pending absorptions

COPY has the same foundation-level batch as INSERT/DELETE/REARRANGE, plus a COPY-specific citation cleanup to ASN-0058.

### Foundation-level (universal across operations)

- **Shift-increment commutativity → ASN-0034.** Used in C4 (Displacement) and C5 (NoOverwrite). Same lemma as INSERT/DELETE/REARRANGE. See [`insert.md`](insert.md) for full discussion.
- **`ord(v)` / `vpos(S, o)` primitives → ASN-0036.** COPY uses ordinal arithmetic implicitly via C4's shift mechanism. The primitives originate in DELETE's ASN-0061. See [`deletevspan.md`](deletevspan.md) for full discussion.
- **General contiguity preservation lemma → ASN-0036.** C2 (ContiguityPreservation) is one of four parallel derivations across operations. Consolidate to ASN-0036.

### Citation cleanup — ASN-0058 already has M16a

- **C7 (OriginInvariance) → cite ASN-0058 M16a.** ASN-0058 (now titled "Mapping Block Algebra") already hosts M16a (*"for `a ∈ dom(C)` and `k ≥ 0` with `a + k ∈ dom(C)`, `origin(a + k) = origin(a)`"*) with full proof. COPY's C7 is the application of this lemma to placed-block I-addresses. The regen note can cite ASN-0058 directly instead of deriving the origin-stability claim locally.

This is dependent-side cleanup; ASN-0058 needs no reopen.

### Citation cleanup — extension-then-absorption chain (none needed)

COPY's content-reference and resolution machinery (ContentReference, ContentReferenceSequence, resolve(d_s, σ), C1 ResolutionIntegrity, C1a RestrictionDecomposition) was extracted into ASN-0074 (Permutation Model 0) in 2026-03 (`c2742dd0`) → then absorbed into **ASN-0058 (Mapping Block Algebra)**. ASN-0074 is retired; its contents are in ASN-0058's "Content References" + "Resolution" sections.

COPY's existing foundation citation to ASN-0058 reaches the absorbed content. **No missing extension citations.** Verify with `python3 scripts/diagnostics/note_graph.py 67`.

### Sequencing

The foundation-level three batch into the ASN-36 reopen alongside INSERT/DELETE/REARRANGE. The C7 → ASN-0058 M16a citation cleanup happens automatically during COPY's regen; no other dependent-side cleanups are needed.

## Open questions

- **Self-transclusion semantics.** COPY can place a document's own content at a new position within itself (self-transclusion). The retired note discusses this as "the same content appearing at multiple positions" (cf. ASN-0058's S5 UnrestrictedSharing). Worth verifying that C0a's allocation invariance and C7's origin invariance behave correctly when source and target documents coincide.
- **Spec-set resolution under concurrent edits.** The source content-reference is resolved at the moment of COPY. If the source document is concurrently being edited (INSERT/DELETE/REARRANGE), what consistency guarantee does the resolved I-address run carry? ASN-0067 specifies the operation against a fixed pre-state; concurrent semantics are unspecified.
- **Empty-spec COPY.** What if `<spec set>` resolves to zero I-addresses (e.g., the source document is empty, or the span is degenerate)? Likely no-op, but worth confirming Green's behavior.
- **Optimization path correctness.** The commented-out "kluged unix version for speed" at `fns.c:50-67` sends the response before doing the work. Lint comments suggest known issues. If this path ever ships, callers can't rely on response-arrival meaning operation-completion.

## Cross-references

- [`catalog.md`](catalog.md) — Full operations inventory; COPY row at opcode 2
- [`insert.md`](insert.md), [`deletevspan.md`](deletevspan.md), [`rearrange.md`](rearrange.md) — Sibling operations; share the foundation-level absorptions
- [`findlinksfromtothree.md`](findlinksfromtothree.md) — Shares source-resolution machinery (content references resolve through the same ASN-0058 path)
- LM source: page 4/67
- Green source: `channels/gregory/resources/udanax-test-harness/backend/{requests.h, fns.c, init.c}`
- Project note: `_docuverse/documents/1.1/1/note/ASN-0067-copy-operation.md` (retired, pending regen)
- Foundation: ASN-0058 (Mapping Block Algebra) hosts M16a, the upstream of C7
- Absorption plan: memory `project_operation_absorption_plan.md`, `project_asn36_pending_absorptions.md`
