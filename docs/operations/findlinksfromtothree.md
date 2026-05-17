# FINDLINKSFROMTOTHREE — and the FIND family

| | LM | Green | This project |
|---|---|---|---|
| **Label** | FINDLINKSFROMTOTHREE | FINDLINKSFROMTOTHREE | (no per-opcode note) |
| **Opcode** | 7 | 30 (renumbered) | — |
| **Source** | LM 4/68-4/69 | `requests.h:39`, `fns.c:189`, dispatch at `init.c:63` | ASN-0079 (retired, pending regen) |
| **Status** | Specified | Shipped | Aggregate ASN covers it + its two siblings |
| **Deps** | — | — | 34, 36, 43, 47, 53, 58 (substrate-registered `citation.depends`) |

## What the operation does

Given a query specifying constraints on link endsets (from-set, to-set, type-set) and a scope (home-set), return all links in the docuverse satisfying the constraints. Per LM 4/68: *"the most powerful command... If the home-set is the whole docuverse, all links between these two elements are returned."*

## Why this document covers three operations

LM defines three opcodes in the FIND family:

- **FINDLINKSFROMTOTHREE** (LM 7 / Green 30) — returns the list of matching links
- **FINDNUMOFLINKSFROMTOTHREE** (LM 6 / Green 29) — returns the count of matching links
- **FINDNEXTNLINKSFROMTOTHREE** (LM 8 / Green 31) — returns a paginated slice of matching links, advanced by cursor

The project's formalization in **ASN-0079 ("FINDLINKS Operation")** treats all three as one operation with three return-shape projections, not three independent operations. This document records the structural reason and points at the specific note machinery.

## The unified mathematical structure (ASN-0079)

ASN-0079 builds the operation as a single function and three derivations:

### Step 1 — the underlying set

```
FindLinks(Q) = {a ∈ dom(Σ.L) : satisfies(a, Q)}
```

where `Q = (H, S₁, S₂, S₃)` is a query specification (home constraint + three endset constraints) and `satisfies` is the satisfaction predicate **F1**.

The set is proven exactly-correct by:
- **F3 — Completeness:** every link satisfying Q is in `FindLinks(Q)`
- **F4 — Soundness:** every link in `FindLinks(Q)` satisfies Q

`FindLinks(Q)` is a deterministic function of state Σ and query Q. This is the **information layer** answer — *what should be discoverable*.

### Step 2 — the three return shapes

Each LM opcode is a different projection of `FindLinks(Q)`:

| Opcode | What it returns | ASN-0079 derivation |
|---|---|---|
| FINDLINKSFROMTOTHREE | `FindLinks(Q)` as an ordered list | **F5** (ResultOrdering) gives the set a permanent total order via T1 lexicographic order on tumbler addresses (GlobalUniqueness from ASN-0043). The list is the ordering of `FindLinks(Q)`. |
| FINDNUMOFLINKSFROMTOTHREE | `\|FindLinks(Q)\|` (cardinality) | **FindLinksCount definition** (line 120 of the retired note): *"The existence of a dedicated count operation presupposes that this cardinality is computable. One cannot count what one has not determined."* Count is a projection of the same set. |
| FINDNEXTNLINKSFROMTOTHREE | `page(Q, c, N)` (windowed slice) | **F6** (PaginationDeterminism): for cursor `c` and bound `N`, returns `⟨aᵢ, ..., aⱼ⟩` where `i = min{k : aₖ > c}` and `j = min(i + N − 1, n)`. The cursor identifies a position in the fixed F5 ordering; advancing does not re-evaluate the query. |

### Step 3 — shared structural properties

All three variants inherit the same downstream guarantees (every one of these applies regardless of return shape):

- **F7** ScopeUniversality — `H = ⊤` searches the entire link store
- **F8** TransclusionTransparency — transcluded content's I-addresses are searchable across documents
- **F9** SymmetricSearchability — the three endset slots (from / to / type) are interchangeable in the predicate
- **F10** ArrangementIndependence — results don't depend on which document arrangement the query was issued from
- **F15-F16** AccessFilter / AccessMonotonicity — visibility filtering for authenticated users is conjunctive with the query
- **F17** StateInvariance — discovery does not modify state
- **F18** MonotonicDiscoverability — once a link satisfies Q, it satisfies Q in every reachable future state
- **F19** ScaleIndependence — implementation constraint that overhead from non-matching links is sublinear in their count

**Splitting the three opcodes into three separate ASNs would force redundant restatement of F1–F19 in each.** Treating them as projections of one operation keeps the formalization clean.

## The structural insight

The three opcodes aren't really three operations — they're a **single computation with three output adaptations**: existence/membership (the set), aggregate measure (cardinality), and bounded delivery (pagination over the ordered set). The same pattern recurs in modern query APIs (GraphQL `nodes`/`count`/`pageInfo` on a connection; SQL `SELECT`/`COUNT(*)`/`LIMIT-OFFSET`). LM's three opcodes are an early version of that pattern, with each projection given its own protocol entry point.

The math in ASN-0079 unifies them; the protocol surface keeps them distinct because front-ends need to negotiate which projection they want over the wire.

## LM vs Green divergence

### Opcode renumbering

| Opcode | LM | Green |
|---|---|---|
| FINDLINKSFROMTOTHREE | 7 | **30** |
| FINDNUMOFLINKSFROMTOTHREE | 6 | **29** |
| FINDNEXTNLINKSFROMTOTHREE | 8 | **31** |

Green moved the entire FIND family into a contiguous block at opcodes 29-31 (alongside the other link operations CREATELINK=27, RETRIEVEENDSETS=28). LM's interleaved numbering became Green's taxonomic grouping. **The wire protocol uses Green's numbering** (see `init.c`).

### Safe-mode gating

`init.c:74-75` disables two of the three in safe mode:

```c
requestfns[FINDNUMOFLINKSFROMTOTHREE] = nullfun;
requestfns[FINDNEXTNLINKSFROMTOTHREE] = nullfun;
```

FINDLINKSFROMTOTHREE remains live. Reading: the basic list-return is considered safe, but the count and paginated variants get gated. Likely reflects DoS concerns (counting and pagination can be exploited as side-channels or DoS amplifiers on large link stores) or known bugs in those code paths. Worth a finding doc if the test harness has data.

### Name and shape consistency

All three names match between LM and `requests.h`. No renaming, only renumbering. The wire formats (request shape, response shape) also match the LM BNF — the protocol semantics carried over intact.

## Current project state

ASN-0079 was drafted, reviewed, revised through 8+ consultation rounds, and then retired as part of the 5-operation deprecation batch (2026-05-13) pending regen against updated foundations. The retired note still describes the FIND family well — F1-F19 cover the structural properties — but it predates several foundation-level changes (the ord/vpos absorptions, the 0058 block-algebra renaming, the 0043 L0a addition). When regen happens, the new note inherits this aggregate framing.

## Pending absorptions

None identified during ASN-0079's review-revise cycle. The note uses general primitives (T1 ordering, GlobalUniqueness from ASN-0043, L12 LinkImmutability from ASN-0043, S0-S3 from ASN-0036) without re-deriving them. F0 (ResolutionIdentityInvariance) — *identical content produces identical I-addresses regardless of which arrangement it is viewed through* — is borderline: it's about how arrangements and content interact and may belong upstream in ASN-0036 rather than as a FINDLINKS premise, but the cycle didn't flag it. Reassess on regen against current foundations.

## Open questions

- Pagination behavior under concurrent link creation: if the link store grows between successive page requests against the same cursor, does the cursor still produce a consistent paginated walk, or does it drift? ASN-0079's F6 says "for fixed Σ, Q" — the per-state pagination is deterministic, but cross-state pagination is unspecified. The retired note flagged this as an open question (line 357).
- Whether FINDLINKSFROMTOTHREE's safe-mode-live status is correct, given that the count and pagination variants are gated. If FINDLINKSFROMTOTHREE returns a 100-million-link result, it's at least as risky as the count.

## Cross-references

- [`catalog.md`](catalog.md) — Full operations inventory with the FIND family in context
- LM source: pages 4/68 (FINDLINKSFROMTOTHREE definition), 4/69 (FINDNUMOFLINKSFROMTOTHREE, FINDNEXTNLINKSFROMTOTHREE definitions)
- Green source: `channels/gregory/resources/udanax-test-harness/backend/{requests.h, fns.c, init.c}`
- Project note: `_docuverse/documents/1.1/1/note/ASN-0079-findlinks-operation.md` (retired)
