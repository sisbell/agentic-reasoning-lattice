# Xanadu Operations Catalog

Side-by-side inventory of operations across four sources:

1. **LM** — Nelson, *Literary Machines*, pages 4/61-4/70 (the FEBE protocol spec section). Page 4/61 states explicitly: **"of the 17 current commands in XU.87.1, only one command (RETRIEVEV) is concerned with delivery of the actual content fragments."** Full enumeration from LM 4/65-4/70 confirms 17.
2. **FEBE doc** — `channels/nelson/resources/febe-protocol.md`, our extracted protocol reference. **Faithful to LM** — all 17 ops and all opcode numbers match.
3. **requests.h** — `channels/gregory/resources/udanax-test-harness/backend/requests.h`, the authoritative opcode definitions in udanax-green's C source. **Renumbers several LM opcodes** (see Discrepancies below).
4. **fns.c** — `channels/gregory/resources/udanax-test-harness/backend/fns.c`, the top-level operation entry points implemented in udanax-green.

## Status legend

- **all** — appears in LM, FEBE doc, requests.h, AND fns.c
- **udanax** — in requests.h + fns.c (the udanax-green operational core)
- **doc-only** — in FEBE doc but no opcode/impl found in Green
- **impl-only** — in requests.h or fns.c but not in the FEBE doc extract
- **debug** — debug/admin opcodes (not user-facing operations)
- **stub** — function exists but body is gutted; returns error or no-op

## Core operations

Sorted by LM opcode (Nelson's canonical numbering). LM column lists Nelson's label and source page; FEBE-doc opcodes match LM exactly. requests.h opcodes diverge for link-related operations (see Discrepancies §1).

| LM opcode | LM label | LM page | FEBE doc | requests.h opcode | requests.h label | fns.c | Status |
|----------:|----------|---------|----------|------------------:|------------------|-------|--------|
| 0  | INSERT | 4/66 | INSERT (0) | 0 | INSERT | `insert` (l. 84) | all |
| 1  | RETRIEVEDOCVSPANSET | 4/68 | RETRIEVEDOCVSPANSET (1) | 1 | RETRIEVEDOCVSPANSET | `retrievedocvspanset` (l. 129) | all |
| 2  | COPY | 4/67 | COPY (2) | 2 | COPY | `copy` (l. 35) | all |
| 3  | REARRANGE | 4/66 | REARRANGE (3) | 3 | REARRANGE | `rearrange` (l. 159) | all |
| 4  | MAKELINK | 4/68 | MAKELINK (4) | **27** | **CREATELINK** | `createlink` (l. 100) | all, opcode+name mismatch |
| 5  | RETRIEVEV | 4/67 | RETRIEVEV (5) | 5 | RETRIEVEV | `retrievev` (l. 175) | all |
| 6  | FINDNUMOFLINKSFROMTOTHREE | 4/69 | FINDNUMOFLINKSFROMTOTHREE (6) | **29** | FINDNUMOFLINKSFROMTOTHREE | `findnumoflinksfromtothree` (l. 204) | all, opcode mismatch |
| 7  | FINDLINKSFROMTOTHREE | 4/68-69 | FINDLINKSFROMTOTHREE (7) | **30** | FINDLINKSFROMTOTHREE | `findlinksfromtothree` (l. 189) | all, opcode mismatch |
| 8  | FINDNEXTNLINKSFROMTOTHREE | 4/69 | FINDNEXTNLINKSFROMTOTHREE (8) | **31** | FINDNEXTNLINKSFROMTOTHREE | `findnextnlinksfromtothree` (l. 219) | all, opcode mismatch |
| 10 | SHOWRELATIONOF2VERSIONS | 4/70 | SHOWRELATIONOF2VERSIONS (10) | 10 | SHOWRELATIONOF2VERSIONS | `showrelationof2versions` (l. 250) | all |
| 11 | CREATENEWDOCUMENT | 4/65 | CREATENEWDOCUMENT (11) | 11 | CREATENEWDOCUMENT | `createnewdocument` (l. 276) | all |
| 12 | DELETEVSPAN | 4/66 | DELETEVSPAN (12) | 12 | DELETEVSPAN | `deletevspan` (l. 333) | all |
| 13 | CREATENEWVERSION | 4/65-66 | CREATENEWVERSION (13) | 13 | CREATENEWVERSION | `createnewversion` (l. 289) | all |
| 14 | RETRIEVEDOCVSPAN | 4/68 | RETRIEVEDOCVSPAN (14) | 14 | RETRIEVEDOCVSPAN | `retrievedocvspan` (l. 303) | all |
| 19 | APPEND | 4/67 | APPEND (19) | — | — | — | **LM+doc only — never implemented in Green** |
| 22 | FINDDOCSCONTAINING | 4/70 | FINDDOCSCONTAINING (22) | 22 | FINDDOCSCONTAINING | `finddocscontaining` (l. 20) | all |
| 26 | RETRIEVEENDSETS | 4/69 | RETRIEVEENDSETS (26) | **28** | RETRIEVEENDSETS | `retrieveendsets` (l. 350) | all, opcode mismatch |

**LM total: 17. Confirmed against Nelson's explicit count at page 4/61.**

## Operations added in udanax-green (not in LM 87.1)

These are in requests.h and implemented in the backend, but Nelson didn't include them in the FEBE spec. They are additions made during Green implementation for session/account management, navigation, operator control, and shell access.

| Opcode | requests.h | fns.c | Purpose | Notes |
|-------:|------------|-------|---------|-------|
| 9  | NAVIGATEONHT | `navigateonht` (l. 236) | Navigate on hypertext | **Stub** — body is gutted, returns `"GACK ! (historical trace)"` error. Disabled in safe mode. |
| 16 | QUIT | `quitxanadu` (l. 419) | Quit session | |
| 18 | FOLLOWLINK | `followlink` (l. 114) | Follow a link | |
| 21 | SOURCEUNIXCOMMAND | impl in `xumain.c:91`, `bed.c:230`; no-op stub in `be.c:162` | Execute shell command | Disabled in safe mode |
| 34 | XACCOUNT | `xaccount` (l. 364) | Account operations | |
| 35 | OPEN | `myopen` (l. 388) | Session open | requests.h `OPEN` → fns.c `myopen` (name mismatch) |
| 36 | CLOSE | `myclose` (l. 404) | Session close | requests.h `CLOSE` → fns.c `myclose` (name mismatch) |
| 38 | CREATENODE_OR_ACCOUNT | `createnode_or_account` (l. 375) | Node or account creation | |

## Debug / admin opcodes

These are not user-facing operations but are part of the request dispatch table. (SOURCEUNIXCOMMAND was moved to the Green-additions table above — it's a wired request handler, not just a debug knob.)

| Opcode | requests.h | Notes |
|-------:|------------|-------|
| 15 | SETDEBUG | Toggle debug output |
| 17 | SHOWENFILADES | Display enfilade state |
| 20 | EXAMINE | Inspect internal state |
| 23 | DUMPGRANFWIDS | Granfwid dump |
| 24 | JUSTEXIT | Immediate exit |
| 25 | IOINFO | I/O statistics |
| 32 | SETMAXIMUMSETUPSIZE | Tuning parameter |
| 33 | PLAYWITHALLOC | Allocator test |
| 39 | DUMPSTATE | Internal enfilade state dump |

## Headline counts

- **LM 87.1 spec (Nelson)**: **17 operations** (confirmed; LM 4/61 states the count, LM 4/65-4/70 enumerates them)
- **FEBE doc extract**: **17 operations** (faithful to LM in labels + opcodes, NOT in wire numbering — see Discrepancies §1)
- **udanax-green operational opcodes** (requests.h, excluding pure debug/admin): **25** (17 LM-derived + 8 Green additions, minus APPEND which was dropped)
- **fns.c top-level implementations**: **23**

**Overlap matrix:**
- **16 of 17 LM operations fully implemented in Green** — entry point in fns.c + wired in init.c
- **1 LM operation never implemented**: APPEND (dropped by design — replaceable by INSERT at end-of-doc)
- **8 additional operations in Green** beyond LM: session (OPEN, CLOSE, QUIT), account (XACCOUNT, CREATENODE_OR_ACCOUNT), link traversal (FOLLOWLINK), navigation (NAVIGATEONHT — gutted), shell (SOURCEUNIXCOMMAND)

**Note on the "~27" you may have remembered:** that count is close to udanax-green's operational total (25 ops) but it's NOT Nelson's count. Nelson's spec is 17. The Green implementation grew the surface by ~50% with session/account/shell ops Nelson didn't specify.

## Discrepancies surfaced

### 1. Opcode renumbering between LM and requests.h — wire uses Green's
Five link-related operations were renumbered in udanax-green:
- MAKELINK: LM **4**, requests.h **27** (also renamed to CREATELINK)
- FINDNUMOFLINKSFROMTOTHREE: LM **6**, requests.h **29**
- FINDLINKSFROMTOTHREE: LM **7**, requests.h **30**
- FINDNEXTNLINKSFROMTOTHREE: LM **8**, requests.h **31**
- RETRIEVEENDSETS: LM **26**, requests.h **28**

LM opcodes 4, 6, 7, 8, and 26 were vacated; new opcodes 27-31 were assigned to the link operations. The vacated opcodes were either left empty or reassigned to debug/admin (15, 17, 20, 23, 25 are debug).

**Resolution: the wire protocol uses Green's numbering, not LM's.** `init.c:45-69` registers handlers using `requests.h` constants directly (e.g., `requestfns[CREATELINK] = createlink;` where `CREATELINK = 27`). A client wanting to talk to a real Green backend must use Green's opcodes (27-31 for the link family). The FEBE doc extract is faithful to the LM spec but does not match the wire.

### 2. Name mismatches
- LM/FEBE `MAKELINK` ↔ requests.h `CREATELINK` ↔ fns.c `createlink`
- requests.h `QUIT` ↔ fns.c `quitxanadu`
- requests.h `OPEN` / `CLOSE` ↔ fns.c `myopen` / `myclose`

### 3. APPEND — defined in LM, never implemented in Green
LM 4/67 defines APPEND at opcode 19 with full BNF. Not in requests.h, not in fns.c. Possibilities:
- (a) Removed between LM spec and Green implementation (most likely — APPEND is implementable as `INSERT` at end-of-doc, may have been deemed redundant)
- (b) Front-end synthesizes APPEND via INSERT
- (c) Implemented elsewhere in the backend not via fns.c

### 4. SHOWRELATIONOF2VERSIONS — fully implemented (closed)
Earlier draft of this catalog claimed no fns.c entry. That was a false negative from a regex bug (`[a-z]+` doesn't match the digit `2` in `showrelationof2versions`). The function is at `fns.c:250`, wired at `init.c:51`, parsed by `get1.c:148`, executed by `do1.c:428`, serialized by `putfe.c:299`. Complete chain. Green ships this op as spec'd.

### 5. Safe mode disables four operations
`init.c:71-76` nullfun's these four when the backend is started in safe mode:
- `SOURCEUNIXCOMMAND` (shell-out — obvious safety concern)
- `NAVIGATEONHT` (gutted stub — disabled even though it only returns an error string)
- `FINDNUMOFLINKSFROMTOTHREE`
- `FINDNEXTNLINKSFROMTOTHREE`

Note `FINDLINKSFROMTOTHREE` (the basic find op) stays live; only the count and paginated-find variants are gated. May reflect DoS concerns over heavy-weight queries, or known bugs in those variants.

## Evolution observations

The LM-to-Green delta reads as a small case study in how a 1987 spec survived contact with implementation reality. Four patterns:

### 1. What survived intact (16 of 17)

The conceptual primitives — INSERT, DELETE, COPY, REARRANGE, the link CRUD/query set, version creation, content retrieval, span queries, document discovery. These are the irreducible information operations — what Xanadu *is* in Nelson's framing. They survived because they describe relationships in the data model, not workflow. **Information-model operations transferred wholesale.**

### 2. What got dropped (APPEND, 1 of 17)

The only LM op Green didn't ship. APPEND is `INSERT` at end-of-doc — Nelson included it as ergonomic shorthand. Green's authors decided ergonomics belong in the front-end (synthesize APPEND from INSERT), not the protocol. **The protocol surface shrank in favor of compositional primitives.**

### 3. What Nelson missed (8 Green additions)

Sorted by what they reveal:

- **Session boundaries** (OPEN, CLOSE, QUIT): the spec is stateless; the implementation needs sessions. Nelson treated the back-end as a stateless function from request to response. Green discovered real servers need session lifecycle, especially for transactional consistency and resource cleanup.
- **User identity** (XACCOUNT): the spec is single-user; multi-user reality demands account ops. Nelson's docuverse was a unified space but didn't model how to negotiate user identity at request time.
- **Interactive navigation** (NAVIGATEONHT, FOLLOWLINK): the spec lets you *find* links; the implementation needs to *traverse* them at interactive speed. FINDLINKSFROMTOTHREE is the query API; FOLLOWLINK is the click. Different needs, different ops.
- **Hidden creation paths** (CREATENODE_OR_ACCOUNT): network nodes and account provisioning — implementation infrastructure entirely below the LM spec's level.
- **Shell access** (SOURCEUNIXCOMMAND): the spec is platform-agnostic; the implementation has a Unix host with a shell. Green added an op to run shell commands directly from the protocol — a development/operator convenience that's safe-mode-disabled in production. The fact that this was reachable from the wire at all is striking: Nelson's protocol-level abstraction collapsed against the practical need for ad-hoc operator access.

**The pattern: Nelson specified the information model; implementation discovered the operational model.** Both are real, both are necessary, but only the first was in 1987. The shell-access addition further suggests there's a fourth implicit layer below "operational" — operator/development tooling — that gets quietly added to any real system whose authors also have to maintain it.

### 4. What got renumbered (5 of 17)

The link operations moved from LM's opcodes 4, 6, 7, 8, 26 (interleaved with content ops) to Green's contiguous block 27-31. **Opcode space repurposed as a categorical signal** — link ops live together so they read as a family. LM's numbering was history-of-addition; Green's is taxonomic.

### 5. The one Green addition that didn't make it (NAVIGATEONHT)

Of the eight operations Green added beyond LM, seven shipped working code. **NAVIGATEONHT did not.** Its body is commented out, replaced by `error(taskptr, "GACK ! (historical trace)\n")`. The function exists, the opcode is wired, but invoking it just returns an error.

This is the only true unfinished operation in the whole inventory — and notably, it's a Green addition, not a LM survival. Someone reserved opcode 9 for hypertext-navigation logic, sketched the entry point, and then never landed the implementation. The "(historical trace)" comment is unusual — suggests the original logic existed at some point and was deliberately removed for the distribution. The motivation for keeping the dead opcode (rather than removing it from the dispatch table) is unclear.

Every LM operation either shipped (16) or was deliberately dropped (APPEND, replaceable by INSERT). The only true gap is one Green added to itself and couldn't finish.

### Three-layer split

Re-reading the operations as "what protocols actually need to be," there's a clean three-layer structure that Nelson's 1987 spec didn't make explicit:

- **Information layer** (16 ops): the LM core, unchanged
- **Operational layer** (7 ops): session, identity, navigation, lifecycle — implementation reality (OPEN, CLOSE, QUIT, XACCOUNT, FOLLOWLINK, NAVIGATEONHT, CREATENODE_OR_ACCOUNT)
- **Administrative layer** (~10 ops): debug, dump, examine — operator tooling, plus SOURCEUNIXCOMMAND straddling this and the operational layer

LM 87.1 specified only layer 1. A modern Xanadu spec would have to acknowledge all three. The fact that Green's authors had to invent layers 2 and 3 on their own — and that they invented similar shapes to what every networked system has converged on — is itself evidence that those layers are not optional.

## Open work

1. **Confirm APPEND's fate.** Greps for `append`, `appendrequest`, and `APPEND` in `backend/*.c` and `backend/*.h` returned zero matches — Green truly never implemented it. Worth checking whether any historical commit or comment explains the decision, or whether the front-end synthesizes APPEND from INSERT at end-of-doc.
2. **Investigate NAVIGATEONHT's history.** The "(historical trace)" comment in the gutted stub suggests there was once working code. Check VCS history or other branches for the original logic — recovering it might reveal what Green was trying to express about hypertext navigation that didn't survive to distribution.
3. **Document operation semantics divergence.** Beyond names and opcodes, do any of the 16 shared operations have semantic differences between LM and Green (REARRANGE's 3-cut vs 4-cut form, COPY's transclusion behavior, version-comparison output shape)? This requires reading both sources side-by-side per operation.
4. **Add BEBE operations** (back-end/back-end protocol, LM 4/70-4/79) as a sibling section. BEBE was undefined in LM 87.1 ("undergoing definition and will not be made public anytime soon"); the catalog there will start sparse.
5. **Document why FIND variants are safe-mode gated but FINDLINKS isn't.** May reflect DoS concerns over heavy-weight counts and pagination, or known bugs. Worth a finding doc if the test harness has data.
