## Question 5 [gregory]

> When you look across all eight FEBE state-modifying commands, how many distinct kinds of state modification do they actually perform — not how many commands exist, but how many underlying state changes?

## KB Synthesis

Looking across the eight commands (INSERT, DELETEVSPAN, REARRANGE, VCOPY, CREATELINK, CREATENEWVERSION, APPENDTEXT, OPEN/CLOSE), the underlying state modifications reduce to **seven distinct kinds** — eight if you count access control.

The three storage layers [SS-THREE-LAYER-MODEL] each accept distinct write operations:

---

**Granfilade (append-only) — 2 kinds:**

1. **Text content allocation** — fresh I-addresses written to the permascroll. INSERT and APPEND do this via `inserttextingranf`. [SS-ADDRESS-ALLOC, ST-INSERT]

2. **Orgl/address allocation** — a new document or link orgl entry placed in the address tree. CREATELINK (link orgl) and CREATENEWVERSION (document address) use the same `findisatoinsertnonmolecule` path but serve different purposes. [ST-CREATE-LINK, ST-VERSION, FC-GRANF-ON-VERSION]

---

**Spanfilade (write-only) — 2 kinds:**

3. **DOCISPAN indexing** — records which documents contain which I-address ranges. INSERT, VCOPY, and CREATENEWVERSION all call `insertspanf(..., DOCISPAN)`. Notably, APPEND skips this entirely. [SS-DOCISPAN, EC-APPEND-NO-DOCISPAN]

4. **Link endpoint indexing** — records link endpoint I-addresses via `insertendsetsinspanf`. Only CREATELINK does this. [SS-SPANF-OPERATIONS, ST-CREATE-LINK]

---

**POOM (mutable) — 3 kinds:**

5. **Entry insertion** — adds V→I mapping entries and shifts subsequent entries rightward. INSERT, VCOPY, CREATELINK, CREATENEWVERSION, and APPEND all go through `insertpm` → `insertnd` → `makegappm`. [ST-INSERT, ST-VCOPY, ST-CREATE-LINK]

6. **Entry deletion** — removes V→I mapping entries and shifts survivors leftward (or leaves them negative via the `strongsub` exponent path). Only DELETEVSPAN does this via `deletend`. [ST-DELETE, INV-POOM-BIJECTIVITY]

7. **Entry displacement** — shifts V-positions of existing entries without adding or removing any. REARRANGE is the only command that performs this operation alone via `tumbleradd` over cut sections. [ST-REARRANGE, INV-REARRANGE-IDENTITY]

---

**Access control — 1 kind:**

8. **BERT state modification** — opens or closes a document handle (READ or WRITE). [SS-BERT, PRE-OPEN-DOC]

---

The telling asymmetries: APPEND performs kinds 1 + 5 but skips kind 3, making content invisible to `find_documents`. REARRANGE performs only kind 7 — the only command that leaves all three enfilades unchanged [FC-GRANF-ON-DELETE, INV-REARRANGE-IDENTITY]. DELETEVSPAN performs only kind 6 — which is why the spanfilade diverges from the POOM after deletion, making stale DOCISPAN references permanent [INT-DELETE-SPANF-DIVERGENCE, INV-SPANF-WRITE-ONLY].

---

## Code Exploration

Now I have enough to give a complete answer. Let me compile the full analysis.

---

## How Many Distinct Kinds of State Modification? **Six.**

The eight FEBE state-modifying commands are (from `docs/client-api.md` protocol table and `fns.c`):

| Cmd | FEBE Method | `fns.c` handler | `do1.c` worker |
|-----|-------------|-----------------|----------------|
| 0 | `insert` | `insert()` [fns.c:84] | `doinsert()` [do1.c:87] |
| 2 | `vcopy` | `copy()` [fns.c:35] | `docopy()` [do1.c:45] |
| 3 | `pivot`/`swap` | `rearrange()` [fns.c:159] | `dorearrange()` [do1.c:34] |
| 11 | `create_document` | `createnewdocument()` [fns.c:276] | `docreatenewdocument()` [do1.c:234] |
| 12 | `delete` | `deletevspan()` [fns.c:333] | `dodeletevspan()` [do1.c:158] |
| 13 | `create_version` | `createnewversion()` [fns.c:289] | `docreatenewversion()` [do1.c:260] |
| 27 | `create_link` | `createlink()` [fns.c:100] | `docreatelink()` [do1.c:195] |
| 38 | `create_node` | `createnode_or_account()` [fns.c:375] | `docreatenode_or_account()` [do1.c:243] |

---

### The System's Persistent State

Three independent data structures hold all persistent state:

1. **The Granfilade** (`granf`) — A global sequential enfilade indexed by I-address. Contains two kinds of leaf: `GRANTEXT` atoms (raw content bytes) and `GRANORGL` nodes (named POOM containers for documents/links/nodes). Written via `insertseq` in `granf2.c`.

2. **The POOM** (`orgl`) — A per-document (or per-link) 2D enfilade mapping V-addresses ↔ I-addresses. Each document has its own POOM, stored inside its `GRANORGL` entry. Three distinct operations mutate it.

3. **The Spanfilade** (`spanf`) — A global 2D reverse index mapping I-spans → the documents or link-endsets that reference them. Written via `insertnd` on a `SPAN` enfilade; **never pruned**. This is why `find_documents` returns stale results (Finding 0057 in `docs/client-api.md`).

---

### The Six Primitive State Modifications

Tracing every call chain to its leaf writes:

---

**Kind 1 — Allocate I-space content**
Allocates new I-addresses in the granfilade, writes actual text bytes there.

```
doinsert [do1.c:87]
  → inserttextingranf [granf1.c:44]
    → inserttextgr [granf2.c:83]
      → insertseq(GRANTEXT)  ← leaf write
```

`inserttextgr` [granf2.c:83-109] calls `findisatoinsertgr` to compute a fresh I-address, then loops over the text set calling `insertseq` for each piece, storing a `locinfo.infotype = GRANTEXT` crum. **Only `insert` (cmd 0) does this.** Content thus allocated is permanent; there is no I-space deallocation operation.

---

**Kind 2 — Allocate O-space POOM container**
Inserts a new `GRANORGL` node into the granfilade at a freshly-allocated ISA, with an empty POOM attached.

```
docreatenewdocument / docreatenewversion / docreatelink / docreatenode_or_account
  → createorglingranf [granf1.c:50]
    → createorglgr [granf2.c:111]
      → createenf(POOM)          ← creates empty POOM
      → insertseq(GRANORGL)      ← leaf write
```

`createorglgr` [granf2.c:111-128]:
```c
locinfo.infotype = GRANORGL;
locinfo.granstuff.orglstuff.orglptr = createenf (POOM);   // empty POOM
...
insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);        // add to granfilade
```

`create_document` [do1.c:234] uses hint `(ACCOUNT, DOCUMENT, 0)`.
`create_version` [do1.c:260] uses hint `(DOCUMENT, DOCUMENT, 0)` or `(ACCOUNT, DOCUMENT, 0)`.
`create_link` [do1.c:207] uses hint `(DOCUMENT, ATOM, LINKATOM)`.
`create_node` [do1.c:251] uses hint `(NODE, NODE, 0)`.
All four paths land in the same `createorglgr`.

---

**Kind 3 — Insert V→I crums into a POOM**
Adds new crum nodes to a document's (or link's) POOM recording a mapping from a V-address range to an I-span.

```
docopy [do1.c:45]  ← called by insert, vcopy, create_version, create_link
  → insertpm [orglinks.c:75]
    → insertnd(POOM) [insertnd.c:15]
      → makegappm(...)           ← shifts downstream crums to open a gap
      → doinsertnd(...)          ← leaf write: places new 2D crum
```

`insertpm` [orglinks.c:99-134] iterates the ispanset, for each span calling `insertnd` with `cenftype = POOM`. For POOM, `insertnd` [insertnd.c:51-61] first calls `makegappm` [insertnd.c:124] to shift existing crums' V-displacements, then calls `doinsertnd` to write the new crum. The `logbertmodified` call [orglinks.c:99] is session-scoped, not a persistent mutation.

`create_link` [do1.c:195-221] triggers this twice: once for the document POOM (placing the link-ISA reference at a link-subspace V-address via `docopy`) and once for the link's own POOM (writing the from/to/type endsets via `insertendsetsinorgl` [do2.c:130]).

---

**Kind 4 — Rearrange V-displacements within a POOM**
Adjusts the `cdsp.dsas[V]` displacement fields of existing POOM crums. No crums are created or destroyed; only their V-offsets change.

```
dorearrange [do1.c:34]
  → rearrangepm [orglinks.c:137]
    → rearrangend(POOM) [edit.c:78]   ← leaf write
```

`rearrangend` [edit.c:78-160] calls `makecutsnd` to split crums at the cut points, then loops over children applying signed offsets from `makeoffsetsfor3or4cuts`:
```c
tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
ivemodified((typecorecrum*)ptr);
```

**Crucially: no `insertspanf` call follows.** Rearranging V-space does not update the spanfilade.

---

**Kind 5 — Delete V-span crums from a POOM**
Removes existing crum nodes from a document's POOM, via `disown`/`subtreefree`, for the deleted V-range.

```
dodeletevspan [do1.c:158]
  → deletevspanpm [orglinks.c:145]
    → deletend(POOM) [edit.c:31]   ← leaf write
```

`deletend` [edit.c:31-76] calls `makecutsnd`, finds the father crum, then for each child in the deleted range calls `deletecutsectionnd` and dispatches:
```c
case 1:
    disown ((typecorecrum*)ptr);
    subtreefree ((typecorecrum*)ptr);
    break;
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    break;
```

**Crucially: no `insertspanf` call follows.** The spanfilade is never pruned. After deletion, the spanfilade still records that the deleted I-spans belong to this document.

---

**Kind 6 — Insert I→document crums into the spanfilade**
Adds crums to the global `SPAN` enfilade recording which I-spans are referenced by which document (or link endset).

```
docopy [do1.c:45]  ← called by insert, vcopy, create_version, create_link
  → insertspanf(spanf, docisaptr, ispanset, DOCISPAN) [spanf1.c:15]
    → insertnd(SPAN) [insertnd.c:15]   ← leaf write

create_link [do1.c:195]
  → insertendsetsinspanf [do2.c:116]
    → insertspanf(spanf, linkisaptr, fromsporglset, LINKFROMSPAN)
    → insertspanf(spanf, linkisaptr, tosporglset, LINKTOSPAN)
    → insertspanf(spanf, linkisaptr, threesporglset, LINKTHREESPAN)
      → insertnd(SPAN) [insertnd.c:15]   ← leaf write (×3)
```

`insertspanf` [spanf1.c:15-54] uses `prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE])` to encode the document/link address and span type in the ORGLRANGE dimension. For `SPAN` enfilades, `insertnd` [insertnd.c:62-65] skips `makegappm` (no gap-opening needed for the reverse index). This is an **append-only** structure — there is no `deletend` called on the spanfilade anywhere in the codebase.

---

### The Full Picture

| Command | K1: alloc I-space | K2: alloc POOM node | K3: insert POOM crums | K4: rearrange POOM crums | K5: delete POOM crums | K6: insert spanfilade |
|---------|:-:|:-:|:-:|:-:|:-:|:-:|
| **insert** | ✓ | | ✓ | | | ✓ |
| **vcopy** | | | ✓ | | | ✓ |
| **pivot/swap** | | | | ✓ | | |
| **create_document** | | ✓ | | | | |
| **delete** | | | | | ✓ | |
| **create_version** | | ✓ | ✓ | | | ✓ |
| **create_link** | | ✓ | ✓ | | | ✓ |
| **create_node** | | ✓ | | | | |

---

### Structural Observations

**The spanfilade asymmetry.** Kinds 4 and 5 (rearrange, delete) never trigger Kind 6. Only Kinds 3+6 occur together. The spanfilade is a permanently-growing reverse index that accumulates entries from every content addition but is never trimmed when content is removed or rearranged. This is the source of Finding 0057 in `docs/client-api.md`: `find_documents` "may return stale results — documents that once contained the I-addresses but no longer do."

**`create_document` and `create_node` are identical in mechanism.** Both call `createorglingranf` [granf1.c:50] with different hints — `(ACCOUNT, DOCUMENT, 0)` vs `(NODE, NODE, 0)` — and both perform only Kind 2. The hint controls where in the I-space hierarchy the new ISA is allocated, not how it is stored.

**`insert` is the only command that writes new I-space.** `vcopy` reuses existing I-addresses. `create_link` creates a new O-space node but its content (the endsets) is written via POOM crums pointing at already-existing I-spans, not new ones. The granfilade's I-space grows only when `insert` (cmd 0) is called.

**`insert` is the only command that triggers all three persistent structures** (granfilade + POOM + spanfilade) in a single operation.
