## Question 4 [evidence]

> Which of the seventeen FEBE commands does udanax-green implement, and what is each command's decomposition into POOM mutations (or other arrangement-touching operations) in the C source?

## KB Synthesis

## The Seventeen FEBE Commands — POOM Decomposition

The KB does not list all seventeen opcodes consecutively, but it names every handler and gives enough source references to identify each command and classify its arrangement-touching behaviour. I group them by what they touch.

---

### Commands That Write the Document POOM

**INSERT** (`doinsert`, called via `fns.c`)

Two-enfilade write. [ST-INSERT, SS-TWO-BLADE-KNIFE, SS-DOCISPAN]

1. `inserttextingranf()` — allocates fresh, monotonically-higher I-addresses in the permascroll.
2. `docopy()` → `insertpm()` → `insertnd()` → `makegappm()` — constructs a two-blade knife with `blade[0] = insert_position` and `blade[1] = next_subspace_boundary` (computed by `findaddressofsecondcutforinsert`). Crums in `[blade[0], blade[1])` are shifted by insert width (Case 1); crums outside are untouched (Case 0/2). If the new content is contiguous with an existing same-homedoc crum at its right border, `isanextensionnd()` widens that crum in place instead of creating one (+0 crums). Interior insert where no coalesce applies: +2 crums (split + new).
3. `insertspanf(..., DOCISPAN)` — one spanf write per contiguous I-span.

**APPEND** (`doappend`)

Granf + POOM write; no spanf write. [EC-APPEND-NO-DOCISPAN]

Follows the same `appendpm()` path as INSERT but the `insertspanf(DOCISPAN)` call is commented out, so content placed via APPEND is invisible to `FINDDOCSCONTAINING`.

**VCOPY/COPY** (`docopy`)

POOM write + DOCISPAN write; no granf content allocation. [ST-VCOPY, ST-COPY, FC-CONTENT-SPANF-ISOLATION]

1. `specset2ispanset()` — converts source V-spans to I-spans (POOM read on source).
2. `insertpm()` — same crum-extension-or-split logic as INSERT, but I-addresses are shared existing values, not freshly allocated. Multiple COPYs of the same I-addresses to different V-positions all succeed; POOM is a multimap [SS-POOM-MULTIMAP].
3. `insertspanf(..., DOCISPAN)` — DOCISPAN entries proportional to I-span count, not byte count [SS-DOCISPAN Finding 0047].

**REARRANGE** (`dorearrange`, FEBE command 3)

POOM-only write; granf and spanf are frame conditions. [ST-REARRANGE, FC-GRANF-ON-DELETE, INV-REARRANGE-IDENTITY]

1. `sortknives()` — normalises cut order (misordered cuts silently accepted).
2. `makeoffsetsfor3or4cuts()` — computes tumbler displacement `diff[i]` for each region from cut geometry alone; for pivot: `diff[1] = cut2−cut1`, `diff[2] = −(cut1−cut0)`.
3. `rearrangend()` — iterates POOM crums; `rearrangecutsectionnd()` classifies each crum into a region; `tumbleradd(&ptr->cdsp.dsas[V], &diff[i], ...)` — only the V-dimension displacement is touched, I-addresses are never modified. No crums are created or freed.

**DELETEVSPAN** (`dodeletevspan`, FEBE command 12)

POOM-only write; spanf is an explicit frame condition. [ST-DELETE, INV-SPANF-WRITE-ONLY, FC-GRANF-ON-DELETE]

Three-phase `deletend()`:
1. **Phase 1 — cut** (`makecutsbackuptohere` → `slicecbcpm`): only called when `whereoncrum() == THRUME` (strict interior). Boundary-aligned deletions skip the cut entirely [PRE-DELETE Finding 0075]. Produces two crums of strictly positive width [INV-NO-ZERO-WIDTH-CRUM].
2. **Phase 2 — classify**: Case 1 crums (fully inside deletion range) are `disown`ed and `subtreefree`d. Case 2 crums (after deletion end) have V-displacement reduced via `tumblersub` — cross-subspace crums are protected by `strongsub`'s exponent guard, not by an explicit knife [INT-DELETE-SUBSPACE-ASYMMETRY, FC-SUBSPACE Finding 0055].
3. **Phase 3 — rebalance**: `setwispupwards` + `recombinend` (2D diagonal rebalance). `levelpull` is called but is a no-op, so tree height never decreases [SS-ENFILADE-TREE Finding 0058].

No spanf deletion exists anywhere in the codebase; POOM and spanf diverge permanently after DELETE [INT-DELETE-SPANF-DIVERGENCE, INV-SPANF-WRITE-ONLY].

**CREATENEWVERSION** (`docreatenewversion`, FEBE command/opcode 13)

Granf document allocation + POOM write + DOCISPAN write; no new content I-addresses. [ST-VERSION-CREATE, ST-VERSION, FC-GRANF-ON-VERSION]

1. `createorglingranf()` with `DOCUMENT` hint — allocates new document address as child of source doc (owned) or under creating user's account (unowned) via `findisatoinsertnonmolecule` [SS-VERSION-ADDRESS Finding 0068].
2. `doretrievedocvspanfoo()` → `retrievedocumentpartofvspanpm()` — reads only the text subspace (V-dimension displacement starting at `1`); link subspace at `2.x` is excluded [ST-VERSION-CREATE Finding 0043].
3. `docopyinternal()` → `insertpm()` — copies text V→I mappings into new POOM; shares existing I-addresses, allocates none. VERSION does not break I-address contiguity for subsequent text INSERTs (contrast with CREATELINK) [INV-MONOTONIC Finding 0077].
4. `insertspanf()` — DOCISPAN entries for the copied spans.

**CREATELINK / MAKELINK** (`docreatelink` → `domakelink`)

Three-enfilade write: granf + document POOM + spanf. [ST-CREATE-LINK, SS-THREE-LAYER-MODEL]

1. `createorglingranf()` with `LINKATOM` hint — allocates link orgl I-address in the document's link subspace (`doc.2.x`), advancing the global I-address counter and breaking text I-address contiguity for subsequent INSERTs [SS-ADDRESS-SPACE Finding 0065, INT-LINK-INSERT Finding 0063].
2. `vspanset2sporglset()` — converts endpoint V-spans to sporgls (I-address + width + provenance); a single V-span mapping to non-contiguous I-addresses (due to transclusion) produces multiple sporgls [ST-LINK-CREATE Finding 0037].
3. `findnextlinkvsa()` — computes next `2.x` position; always appends at document end, so in practice no existing crums are shifted by the subsequent `insertpm`.
4. `docopy()` → `insertpm()` — places link orgl ISA at V-position `2.x` in the document POOM. Same crum logic as INSERT; link entries use `2.x` positions, text entries use `1.x` [SS-LINK-SUBSPACE, INV-SUBSPACE-CONVENTION].
5. `insertendsetsinspanf()` — indexes all three endsets (LINKFROMSPAN, LINKTOSPAN, LINKTHREESPAN) in the spanf by I-address [SS-SPANF-OPERATIONS].

---

### Commands That Read the POOM Without Writing It

**retrieve\_contents** (opcode 5, `doretrievev`)

`specset2ispanset()` → `findorgl()` (requires document open, WRITEBERT or READBERT) → `ispanset2vstuffset()` against the granf permascroll. The POOM is consulted for V→I conversion; no mutation. [PRE-RETRIEVE-CONTENTS, SS-DOCUMENT-LIFECYCLE]

**RETRIEVEDOCVSPAN** (opcode 14)

`retrievevspanpm()` reads the root node's raw V-displacement and width. Returns a potentially misleading bounding box for documents containing links [EC-VSPAN-MISLEADING-SIZE, SS-VSPAN-VS-VSPANSET Finding 0035].

**RETRIEVEDOCVSPANSET** (opcode 1)

`retrievevspansetpm()` uses `is1story()` to detect mixed content; emits separate normalised spans for the link subspace (`0.x` in output, `2.x` internally) and text subspace (`1.x`). POOM read only. [SS-DUAL-ENFILADE Finding 0038, SS-VSPAN-VS-VSPANSET]

**SHOWRELATIONOF2VERSIONS** (opcode 10, `correspond.c`)

POOM read on both documents: converts V-spans to sporglsets, intersects by I-address (permascroll only — passing link subspace spans causes a crash, Bug 0009). No mutation. [SS-COMPARE-VERSIONS, PRE-COMPARE-VERSIONS]

**FOLLOWLINK** (`dofollowlink`)

Two-phase read: `link2sporglset()` reads link orgl from granf at the requested endset offset; `linksporglset2specset()` → `span2spanset()` → `retrieverestricted()` against the queried document's POOM for I→V conversion. I-addresses with no current V-position are silently dropped (ghost-link behaviour) [SS-FOLLOWLINK, INV-ITOV-FILTERING, EC-GHOST-LINK]. No mutation.

**RETRIEVEENDSETS** (opcode 28, `retrieveendsetsfromspanf`)

Spanf search restricted by ORGLRANGE subspace (LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3), then `linksporglset2specset()` resolves I→V against the querying document's POOM. Read-only. [SS-RETRIEVE-ENDSETS]

---

### Commands That Touch Only the Spanf (No POOM Access)

**FINDLINKSFROMTOTHREE** (`dofindlinksfromtothreesp`, `do1.c:386–391`)

Pure spanf query: V-spans → I-spans → `findlinksfromtothreesp()` → `sporglset2linkset()`. The orgl-range parameter is silently overridden to width-100-from-zero by a `TRUE||` guard, making every call a global search [EC-FIND-LINKS-GLOBAL, PRE-FIND-LINKS Finding 0069]. Disabled in safe mode (`init.c:75`).

**FINDNUMOFLINKSFROMTOTHREE** (opcode 29)

Executes the full `findlinksfromtothreesp()` search, then linearly counts the result list. No count-only shortcut. [SS-FIND-LINKS Finding 0035]

**FINDNEXTNLINKSFROMTOTHREE** (opcode 31)

Re-executes the full search on each call (stateless), then linearly scans for the cursor ISA and destructively truncates the list at N items. Missing cursor returns empty, not an error [SS-PAGINATE-LINKS, EC-CURSOR-INVALIDATION]. Disabled in safe mode (`init.c:76`).

**FINDDOCSCONTAINING** (`finddocscontainingsp`)

Reads the DOCISPAN sub-index of the spanf. Returns a superset of current document associations because DELETE never removes spanf entries [EC-STALE-SPANF-REFERENCE, INV-SPANF-WRITE-ONLY]. Callers must post-filter via I→V conversion.

---

### Summary Table

| Command | Granf | POOM | Spanf |
|---|---|---|---|
| INSERT | content alloc | insert+shift | DOCISPAN write |
| APPEND | content alloc | insert | — |
| VCOPY/COPY | — | insert+shift | DOCISPAN write |
| REARRANGE | — | displacement only | — |
| DELETEVSPAN | — | disown+shift | — |
| CREATENEWVERSION | doc addr alloc | insert (text only) | DOCISPAN write |
| CREATELINK | link orgl alloc | insert in 2.x | endset write |
| retrieve\_contents | read | read (V→I) | — |
| RETRIEVEDOCVSPAN | — | read (root) | — |
| RETRIEVEDOCVSPANSET | — | read (both subspaces) | — |
| SHOWRELATIONOF2VERSIONS | — | read × 2 | — |
| FOLLOWLINK | read (link orgl) | read (I→V) | — |
| RETRIEVEENDSETS | — | read (I→V) | read |
| FINDLINKSFROMTOTHREE | — | — | read |
| FINDNUMOFLINKSFROMTOTHREE | — | — | read |
| FINDNEXTNLINKSFROMTOTHREE | — | — | read |
| FINDDOCSCONTAINING | — | — | read (DOCISPAN) |

The KB does not provide a single source location giving all seventeen opcodes consecutively. Opcodes explicitly cited are 1, 3, 5, 10, 12, 13, 14, 28, 29, 31; the remainder are identified by handler name from `do1.c`/`do2.c`/`fns.c` references scattered across the findings.

---

## Code Exploration

I now have all the source evidence needed. Let me compile the full answer.

---

## FEBE Commands in udanax-green: Implementation and POOM Decomposition

### Counting the Commands

The question names "seventeen FEBE commands." The source shows more than that. In `requests.h`, 25 command codes are defined. In `init.c:45–69`, 24 non-debug commands are registered in the `requestfns[]` dispatch table. In daemon mode (`bed.c:66`: `backenddaemon = 1`), `init()` is called with `safe=1`, which immediately nulls four of those (`init.c:72–76`):

```c
requestfns[SOURCEUNIXCOMMAND] = nullfun;   /* init.c:72 */
requestfns[NAVIGATEONHT]       = nullfun;   /* init.c:73 */
requestfns[FINDNUMOFLINKSFROMTOTHREE]      = nullfun;   /* init.c:74 */
requestfns[FINDNEXTNLINKSFROMTOTHREE]      = nullfun;   /* init.c:75 */
```

That leaves **20 active non-debug protocol commands** in normal operation. The "seventeen" likely excludes three session-management commands added later (`OPEN`/`CLOSE`/`CREATENODE_OR_ACCOUNT`) that are not part of the original content-manipulation protocol, or excludes `QUIT`, `DUMPSTATE`, and one variant. Rather than arbitrate the count, below I document all 20 fully active commands and their decompositions — the four safe-mode-disabled stubs are noted at the end.

---

### Fundamental POOM Mutations (Building Blocks)

Every mutating command assembles from these primitives:

| Primitive | File | What it does |
|-----------|------|--------------|
| `insertnd(poom, origin, width, infoptr, dimension)` | `insertnd.c:15` | Inserts a new 2-D crum into any enfilade (POOM or spanfilade), via `makegappm` (POOM only), `doinsertnd`, `insertcbcnd`/`firstinsertionnd`, `recombine` |
| `deletend(poom, origin, width, V)` | `edit.c:31` | Cuts a V-range: `makecutsnd` + walk children + `deletecutsectionnd` + `disown/subtreefree` + `setwispupwards/recombine` |
| `rearrangend(poom, cutseq, V)` | `edit.c:78` | Shifts crum DSPs: `makecutsnd` + `makeoffsetsfor3or4cuts` + walk children + `tumbleradd` on DSPs + `setwispupwards/recombine/splitcrumupwards` |
| `insertpm(orglisa, orgl, vsa, sporglset)` | `orglinks.c:75` | Packages I-span as 2-D crum and calls `insertnd(..., V)` on the document's POOM; also calls `logbertmodified` |
| `insertspanf(spanf, docisa, sporglset, spantype)` | `spanf1.c:15` | Packages I-span as 2-D crum and calls `insertnd(..., SPANRANGE)` on the global spanfilade |
| `createorglingranf(granf, hint, isa)` | `granf1.c:50` → `createorglgr()` | Allocates a new ORGL node in the granfilade (new document, link, or node) |
| `inserttextingranf(granf, hint, textset, &ispanset)` | `granf1.c:43` → `inserttextgr()` | Allocates fresh I-addresses for new text in the granfilade |

---

### The 20 Active Commands

---

#### 1. **INSERT** — code 0

Handler: `fns.c:84 insert()` → `do1.c:87 doinsert()`

```
doinsert
  ├── inserttextingranf(granf, hint, textset, &ispanset)    [granf2.c: allocate I-addresses]
  └── docopy(docisa, vsaptr, ispanset)
        ├── specset2ispanset()                              [V→I: no-op here, ispanset already I]
        ├── findorgl(granf, docisa, WRITEBERT)              [load doc's POOM]
        ├── acceptablevsa()                                 [do2.c:110: always TRUE]
        ├── insertpm(docisa, docorgl, vsaptr, ispanset)     [POOM insertnd at V-addr]
        └── insertspanf(spanf, docisa, ispanset, DOCISPAN)  [spanfilade insertnd]
```

**POOM mutations:** `makehint(DOCUMENT,ATOM,TEXTATOM)` → `inserttextgr` (creates content in granfilade) → `insertnd` on the document POOM (shifts existing content after `vsaptr`) → `insertnd` on the spanfilade (records I→doc mapping).

The preparatory step `makegappm` (`insertnd.c:124`) is called by `insertnd` for POOM enfilades: it makes two cuts around the insertion V-address and shifts all crums with DSP > insertion point rightward by the insertion width.

---

#### 2. **RETRIEVEDOCVSPANSET** — code 1

Handler: `fns.c:129 retrievedocvspanset()` → `do1.c:322 doretrievedocvspanset()`

```
doretrievedocvspanset
  ├── findorgl(granf, docisa, READBERT)     [load doc POOM, read-only]
  ├── isemptyorgl()                         [early exit if POOM is empty]
  └── retrievevspansetpm(orgl, &vspanset)   [orglinks.c:173: read POOM root wid]
```

**POOM mutations: none.** Pure read. `retrievevspansetpm` inspects the root crum's `cdsp` and `cwid` fields (`orglinks.c:181`). If the document has both text and links it calls `maxtextwid` to walk leaf crums for the text span; the link span is extracted directly from the top-level wid.

---

#### 3. **COPY (vcopy)** — code 2

Handler: `fns.c:35 copy()` → `do1.c:45 docopy()`

```
docopy
  ├── specset2ispanset(specset, &ispanset, NOBERTREQUIRED)
  │     └── vspanset2ispanset(docorgl, vspanset, ...)    [V→I: traverses source POOM]
  ├── findorgl(granf, docisa, WRITEBERT)   [load target doc POOM]
  ├── acceptablevsa()                       [do2.c:110: always TRUE]
  ├── insertpm(docisa, docorgl, vsaptr, ispanset)   [POOM insertnd on target]
  └── insertspanf(spanf, docisa, ispanset, DOCISPAN) [spanfilade insertnd]
```

**POOM mutations:** same shape as INSERT's second half (no new I-addresses are created — the source I-addresses travel into the target POOM). `specset2ispanset` reads the *source* document's POOM to resolve V→I; then `insertpm` writes into the *target* document's POOM.

---

#### 4. **REARRANGE (pivot / swap)** — code 3

Handler: `fns.c:159 rearrange()` → `do1.c:34 dorearrange()`

```
dorearrange
  ├── findorgl(granf, docisa, WRITEBERT)
  └── rearrangepm(docisa, docorgl, cutseqptr)
        └── rearrangend(poom, cutseqptr, V)   [edit.c:78]
              ├── makecutsnd(poom, knives)         [insert cut-points in enfilade]
              ├── newfindintersectionnd(...)         [find containing node]
              ├── makeoffsetsfor3or4cuts(knives, diff[])
              │     [3 cuts → pivot; 4 cuts → swap]
              └── for each child crum:
                    rearrangecutsectionnd() → tumbleradd(ptr->cdsp.dsas[V], diff[i])
                    ivemodified(ptr)
              └── setwispupwards / recombine / splitcrumupwards
```

**POOM mutations:** no crums are created or destroyed — only DSP values (V-offsets) are shifted. For a pivot at (A, pivot, B): `diff[1] = pivot−A`, `diff[2] = −(pivot−A)`, sections swap their offsets. For a swap of (A..B) with (C..D): four cuts, four offset computations. The actual content I-addresses stay in place; only the V→I mapping shifts.

---

#### 5. **RETRIEVEV (retrieve_contents)** — code 5

Handler: `fns.c:175 retrievev()` → `do1.c:338 doretrievev()`

```
doretrievev
  ├── specset2ispanset(specset, &ispanset, READBERT)
  │     └── vspanset2ispanset(docorgl, vspanset, ...)   [V→I via POOM]
  └── ispanset2vstuffset(granf, ispanset, &vstuffset)   [granf1.c:57]
        └── ispan2vstuffset(granf, ispan, ...)           [granf2.c: fetch text/link data]
```

**POOM mutations: none.** Two traversals: first the document POOM for V→I, then the granfilade for I→content.

---

#### 6. **SHOWRELATIONOF2VERSIONS (compare_versions)** — code 10

Handler: `fns.c:250 showrelationof2versions()` → `do1.c:428 doshowrelationof2versions()`

```
doshowrelationof2versions
  ├── filter_specset_to_text_subspace() × 2   [do1.c:386: strip link subspace V < 1.0]
  ├── specset2ispanset(version1, &ispans1, READBERT)
  ├── specset2ispanset(version2, &ispans2, READBERT)
  ├── intersectspansets(ispans1, ispans2, &common)  [find shared I-addresses]
  └── ispansetandspecsets2spanpairset(common, v1, v2, &relation)
        ├── restrictspecsetsaccordingtoispans(...)
        └── makespanpairset(...)
```

**POOM mutations: none.** Pure I-span set intersection across two documents' V→I lookups.

---

#### 7. **CREATENEWDOCUMENT** — code 11

Handler: `fns.c:276 createnewdocument()` → `do1.c:234 docreatenewdocument()`

```
docreatenewdocument
  ├── makehint(ACCOUNT, DOCUMENT, 0, account, &hint)
  └── createorglingranf(granf, &hint, &newdocisa)
        └── createorglgr(granf, &hint, &newdocisa)   [granf2.c: allocate new ORGL]
```

**POOM mutations:** one call to `createorglgr` — allocates a new empty ORGL node under the account in the granfilade. The new document has an empty POOM (no crums). No `insertnd` calls.

---

#### 8. **DELETEVSPAN (delete / remove)** — code 12

Handler: `fns.c:333 deletevspan()` → `do1.c:158 dodeletevspan()`

```
dodeletevspan
  ├── findorgl(granf, docisa, WRITEBERT)
  └── deletevspanpm(docisa, docorgl, vspanptr)    [orglinks.c:145]
        └── deletend(poom, stream, width, V)       [edit.c:31]
              ├── makecutsnd(poom, knives)              [2 cuts: origin, origin+width]
              ├── newfindintersectionnd(...)
              └── for each child crum:
                    deletecutsectionnd() →
                      case 1: disown(ptr) + subtreefree(ptr)   [crum is in range: delete]
                      case 2: tumblersub(ptr->cdsp.dsas[V], width)  [crum is after: shift]
              └── setwispupwards / recombine
```

**POOM mutations:** crums in the V-range are `disown`ed (detached from the enfilade tree) and freed; crums after the range have their V-DSP decremented by `width`. The spanfilade is NOT updated — this is a known semantic gap (the spanfilade is write-only; `find_documents` may return stale results after deletion).

---

#### 9. **CREATENEWVERSION** — code 13

Handler: `fns.c:289 createnewversion()` → `do1.c:260 docreatenewversion()`

```
docreatenewversion
  ├── makehint(DOCUMENT, DOCUMENT, 0, original, &hint)   [or ACCOUNT,DOCUMENT for others]
  ├── createorglingranf(granf, &hint, &newdocisa)  [new ORGL under original]
  ├── doretrievedocvspanfoo(original, &vspan)       [read original's POOM root wid]
  ├── addtoopen(newdocisa, user, created=TRUE, WRITEBERT)  [bert table, no POOM]
  ├── docopyinternal(newdocisa, &vspan.stream, &vspec)
  │     ├── specset2ispanset(...)   [V→I from original POOM]
  │     ├── findorgl(granf, newdocisa, NOBERTREQUIRED)
  │     ├── insertpm(newdocisa, newdocorgl, &vspan.stream, ispanset)
  │     └── insertspanf(spanf, newdocisa, ispanset, DOCISPAN)
  ├── logbertmodified(newdocisa, user)
  └── doclose(taskptr, newdocisa, user)
```

**POOM mutations:** creates a new ORGL, then shallow-copies the original's I-spans into the new document's POOM via `insertpm` + `insertspanf`. The original's content (granfilade atoms) is shared — only V→I mapping crums are duplicated. The I-addresses are identical across both versions, which is how `compare_versions` later finds shared content.

---

#### 10. **RETRIEVEDOCVSPAN** — code 14

Handler: `fns.c:303 retrievedocvspan()` → `do1.c:312 doretrievedocvspan()`

```
doretrievedocvspan
  ├── findorgl(granf, docisa, READBERT)
  └── retrievevspanpm(orgl, &vspan)   [orglinks.c:165: copy root cdsp/cwid → vspan]
```

**POOM mutations: none.** Returns the single bounding vspan (full extent of V-space) from the POOM root's `cdsp.dsas[V]` and `cwid.dsas[V]` (`orglinks.c:167–171`).

---

#### 11. **QUIT** — code 16

Handler: `fns.c:419 quitxanadu()`

```
quitxanadu
  ├── putquitxanadu(taskptr)           [send response to frontend]
  ├── (if not backenddaemon) diskexit()  [flush enfilades to disk]
  └── (if backenddaemon) dobertexit(user)  [bert.c:339: close all user's opens]
```

**POOM mutations: none.** `diskexit()` writes dirty enfilade pages to disk; `dobertexit` calls `exitbert()` which may call `deleteversion()` for uncommitted created-but-not-modified documents, but `deleteversion()` is a stub (`bert.c:348–353`).

---

#### 12. **FOLLOWLINK** — code 18

Handler: `fns.c:113 followlink()` → `do1.c:223 dofollowlink()`

```
dofollowlink
  ├── link2sporglset(linkisa, &sporglset, whichend, NOBERTREQUIRED)
  │     └── [reads link's own ORGL POOM to find endset sporgl at whichend V-addr]
  └── linksporglset2specset(&sporgladdress, sporglset, &specset, NOBERTREQUIRED)
        └── [converts sporgl I-spans to VSpecs by looking up through referent doc POOMs]
```

**POOM mutations: none.** Reads the link atom's POOM (which contains three endsets at fixed V-positions `0.1.1`, `0.2.1`, `0.3.1` — set by `setlinkvsas` at `do2.c:169`). Then resolves each I-span back to V-addresses.

---

#### 13. **FINDDOCSCONTAINING (find_documents)** — code 22

Handler: `fns.c:20 finddocscontaining()` → `do1.c:15 dofinddocscontaining()`

```
dofinddocscontaining
  ├── specset2ispanset(specset, &ispanset, NOBERTREQUIRED)   [V→I]
  └── finddocscontainingsp(ispanset, &addressset)
        └── [spanf1.c / retrie.c: searches spanfilade for DOCISPAN entries matching I-spans]
```

**POOM mutations: none.** Spanfilade read-only search. Returns all documents that once had `insertspanf(..., DOCISPAN)` called for those I-addresses. Note: returns stale results after deletion (Finding 0057: spanfilade is write-only).

---

#### 14. **CREATELINK** — code 27

Handler: `fns.c:100 createlink()` → `do1.c:195 docreatelink()`

```
docreatelink
  ├── createorglingranf(granf, LINKATOM hint, &linkisa)
  │     └── createorglgr(...)   [new ORGL with LINKATOM type]
  ├── tumbler2spanset(linkisa, &ispanset)   [do2.c:48: single-unit I-span for link atom]
  ├── findnextlinkvsa(docisa, &linkvsa)     [do2.c:151: next V-addr in 0.x subspace]
  ├── docopy(docisa, &linkvsa, ispanset)
  │     ├── insertpm(docisa, docorgl, &linkvsa, ispanset)   [POOM insertnd: place link in doc]
  │     └── insertspanf(spanf, docisa, ispanset, DOCISPAN)  [spanfilade insertnd]
  ├── findorgl(granf, linkisa, link, NOBERTREQUIRED)   [load link's own POOM]
  ├── specset2sporglset(fromspecset, &fromsporglset, ...)   [V→sporgl for each endset]
  ├── specset2sporglset(tospecset,   &tosporglset, ...)
  ├── specset2sporglset(threespecset,&threesporglset, ...)
  ├── setlinkvsas(&fromvsa, &tovsa, &threevsa)   [do2.c:169: V-addrs 0.1.1, 0.2.1, 0.3.1]
  ├── insertendsetsinorgl(linkisa, link, fromvsa, fromsporglset, tovsa, tosporglset, ...)
  │     └── insertpm(linkisa, link, fromvsa, fromsporglset)   [POOM insertnd × 3]
  │     └── insertpm(linkisa, link, tovsa,   tosporglset)
  │     └── insertpm(linkisa, link, threevsa, threesporglset)
  └── insertendsetsinspanf(spanf, linkisa, fromsporglset, tosporglset, threesporglset)
        ├── insertspanf(spanf, linkisa, fromsporglset, LINKFROMSPAN)   [spanfilade insertnd]
        ├── insertspanf(spanf, linkisa, tosporglset,   LINKTOSPAN)
        └── insertspanf(spanf, linkisa, threesporglset,LINKTHREESPAN)
```

**POOM mutations (7 total):**
1. `createorglgr` — new link ORGL in granfilade
2. `insertpm` → `insertnd` — place link atom in document's POOM at V-addr in 0.x subspace
3. `insertspanf` → `insertnd` — DOCISPAN entry in global spanfilade
4–6. Three `insertpm` → `insertnd` calls — insert from/to/type endsets into the link's own POOM
7–9. Three `insertspanf` → `insertnd` calls — LINKFROMSPAN, LINKTOSPAN, LINKTHREESPAN entries in global spanfilade

Total: 1 ORGL creation + 4 POOM `insertnd` calls + 4 spanfilade `insertnd` calls.

---

#### 15. **RETRIEVEENDSETS** — code 28

Handler: `fns.c:350 retrieveendsets()` → `do1.c:369 doretrieveendsets()`

```
doretrieveendsets
  └── retrieveendsetsfromspanf(specset, &fromset, &toset, &threeset)
        └── [searches spanfilade for LINKFROMSPAN/LINKTOSPAN/LINKTHREESPAN entries]
```

**POOM mutations: none.** Direct spanfilade search for the three endset types. Separate from `followlink` in that it takes a link's *V-address* range (not the link's ISA) and returns raw SpecSets.

---

#### 16. **FINDLINKSFROMTOTHREE (find_links)** — code 30

Handler: `fns.c:189 findlinksfromtothree()` → `do1.c:348 dofindlinksfromtothree()`

```
dofindlinksfromtothree
  └── findlinksfromtothreesp(spanf, fromvspecset, tovspecset, threevspecset, NULL, &linkset)
        ├── specset2sporglset(from/to/three, &sporglsets, NOBERTREQUIRED)  [V→I per endset]
        ├── sporglset2linkset(spanf, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN)
        ├── sporglset2linkset(spanf, tosporglset,   &tolinkset,   ..., LINKTOSPAN)
        ├── sporglset2linkset(spanf, threesporglset,&threelinkset,..., LINKTHREESPAN)
        └── [intersect fromlinkset ∩ tolinkset ∩ threelinkset → &linkset]
```

**POOM mutations: none.** Three spanfilade searches, one per endset type, intersected. The `homeset` (home-document filter) parameter is passed as NULL in `fns.c:198` — matching the Bug 0015 finding that `find_links(homedocids=...)` has no effect.

---

#### 17. **XACCOUNT (account)** — code 34

Handler: `fns.c:364 xaccount()`

```
xaccount
  ├── getxaccount(taskptr, &player[user].account)   [read tumbler from protocol stream]
  └── putxaccount(taskptr)                           [send acknowledgement]
```

**POOM mutations: none.** Sets `player[user].account` (an in-memory field in `players.h`). No granfilade or enfilade interaction.

---

#### 18. **OPEN (open_document)** — code 35

Handler: `fns.c:388 myopen()` → `bert.c:264 doopen()`

```
doopen(tp, &newtp, type, mode, connection)
  mode BERTMODECOPY:
    └── docreatenewversion(...)   [full version copy; see command 13 decomposition]
    └── addtoopen(newtp, connection, created=TRUE, type)
  mode BERTMODECOPYIF (CONFLICT_COPY):
    ├── if openState == -1: docreatenewversion + addtoopen
    ├── if openState == READBERT and type==READ: incrementopen
    └── else: docreatenewversion + addtoopen
  mode BERTMODEONLY (CONFLICT_FAIL):
    ├── if openState in {-1, WRITEBERT}: return FALSE
    ├── if openState == 0: addtoopen (new entry)
    └── else: incrementopen
```

**POOM mutations:** conditional. `CONFLICT_FAIL` with no conflict: only a `berttable` hash-table entry (`addtoopen`, `bert.c:128`) — no POOM. `CONFLICT_COPY` / `ALWAYS_COPY` when a conflict exists: full `docreatenewversion` (see command 13).

---

#### 19. **CLOSE (close_document)** — code 36

Handler: `fns.c:404 myclose()` → `bert.c:325 doclose()`

```
doclose(tp, connection)
  └── removefromopen(tp, connection)   [bert.c:154]
        └── if bert->created && !bert->modified: deleteversion(tp)   [bert.c:349: stub]
```

**POOM mutations: none.** `deleteversion` (`bert.c:348`) is currently a stub — it prints a debug message but does nothing. In production, it would garbage-collect unmodified copy-on-open documents.

---

#### 20. **CREATENODE_OR_ACCOUNT (create_node)** — code 38

Handler: `fns.c:375 createnode_or_account()` → `do1.c:243 docreatenode_or_account()`

```
docreatenode_or_account
  ├── makehint(NODE, NODE, 0, &isa, &hint)
  └── createorglingranf(granf, &hint, &isa)
        └── createorglgr(...)   [new NODE-type ORGL in granfilade]
```

**POOM mutations:** one `createorglgr` — allocates a new ORGL at NODE level under the given account tumbler. Structurally identical to `docreatenewdocument` but with `NODE/NODE` hint instead of `ACCOUNT/DOCUMENT`.

---

### Safe-Mode-Disabled Commands (code registered, then nulled to `nullfun`)

| Code | Name | Status |
|------|------|--------|
| 9 | `NAVIGATEONHT` | Dead — `fns.c:238`: `error(taskptr, "GACK ! (historical trace)")`. HT (hypertext tree) support was removed. |
| 21 | `SOURCEUNIXCOMMAND` | Stub — `bed.c:230`: `return 0`. Shells out to Unix commands; disabled for security. |
| 29 | `FINDNUMOFLINKSFROMTOTHREE` | Implemented (`do1.c:355`) but disabled in safe mode. `dofindnumoflinksfromtothree` → `findnumoflinksfromtothreesp` — same spanfilade search as FINDLINKSFROMTOTHREE but returns count only. |
| 31 | `FINDNEXTNLINKSFROMTOTHREE` | Implemented (`do1.c:362`) but disabled in safe mode. Paginated variant: takes `lastlink` and `n`, returns next N matching links. |

---

### Summary Table

| Code | Command | Mutates POOM? | Core primitives |
|------|---------|:-------------:|-----------------|
| 0 | INSERT | **yes** | `inserttextgr` + `insertpm`→`insertnd` + `insertspanf`→`insertnd` |
| 1 | RETRIEVEDOCVSPANSET | no | `retrievevspansetpm` (read root wid) |
| 2 | COPY (vcopy) | **yes** | `specset2ispanset` + `insertpm`→`insertnd` + `insertspanf`→`insertnd` |
| 3 | REARRANGE (pivot/swap) | **yes** | `rearrangend` → shift DSPs via `tumbleradd` |
| 5 | RETRIEVEV (retrieve_contents) | no | `specset2ispanset` + `ispanset2vstuffset` |
| 10 | SHOWRELATIONOF2VERSIONS | no | `specset2ispanset` × 2 + `intersectspansets` |
| 11 | CREATENEWDOCUMENT | **yes** | `createorglingranf` |
| 12 | DELETEVSPAN (delete) | **yes** | `deletend` → `disown/subtreefree` + shift DSPs |
| 13 | CREATENEWVERSION | **yes** | `createorglingranf` + `insertpm`→`insertnd` + `insertspanf`→`insertnd` |
| 14 | RETRIEVEDOCVSPAN | no | `retrievevspanpm` (read root wid) |
| 16 | QUIT | no | `diskexit` (flush only) |
| 18 | FOLLOWLINK | no | `link2sporglset` + `linksporglset2specset` |
| 22 | FINDDOCSCONTAINING | no | `finddocscontainingsp` (spanfilade read) |
| 27 | CREATELINK | **yes** | `createorglingranf` + 4× `insertpm`→`insertnd` + 4× `insertspanf`→`insertnd` |
| 28 | RETRIEVEENDSETS | no | `retrieveendsetsfromspanf` (spanfilade read) |
| 30 | FINDLINKSFROMTOTHREE | no | `sporglset2linkset` × 3 + intersect |
| 34 | XACCOUNT | no | in-memory `player[user].account` only |
| 35 | OPEN | conditional | `addtoopen` (bert table); or full `docreatenewversion` if copy needed |
| 36 | CLOSE | no | `removefromopen` (bert table); `deleteversion` is stub |
| 38 | CREATENODE_OR_ACCOUNT | **yes** | `createorglingranf` (NODE-type ORGL) |

**Eight commands** (0, 2, 3, 11, 12, 13, 27, 38) unconditionally mutate the POOM. Command 35 (OPEN) conditionally mutates when it creates a copy. All twelve remaining commands are pure reads or session-table operations.
