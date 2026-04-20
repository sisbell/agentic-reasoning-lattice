## Question 18 [gregory]

> For the granfilade write that stores the inserted text, does `doinsert` create a single leaf node containing all N bytes of the insertion, or does the `MAXBCINLOAF=1` constraint mean each byte gets its own bottom crum, with the tree growing by N leaves per INSERT?

## KB Synthesis

A single INSERT of N bytes (where N ≤ 950) creates **one leaf node** containing all N bytes. The `MAXBCINLOAF=1` constraint and the per-byte granularity of I-addresses are orthogonal concerns.

**What `MAXBCINLOAF=1` actually constrains:**

`MAXBCINLOAF=1` means each height-1 node in the granfilade holds exactly one bottom crum (height-0 node). The "one entry" is one *text atom* (`typegrantext`), not one byte. [SS-UNIFIED-STORAGE] is explicit: "Leaf nodes for text content (`GRANTEXT` type) hold up to 950 bytes (`GRANTEXTLENGTH`)." [SS-GRAN-MB-ONE] explains this creates a degenerate pass-through layer at height-1, not per-byte storage.

**What actually happens during INSERT:**

`doinsert` calls `inserttextingranf`, which allocates a fresh `typegrantext` atom containing all N bytes via a single `insertseq` call. [ST-INSERT / Finding 0031] confirms this: `tumblerincrement(&lsa, 0, textset->length, &lsa)` advances by the total length in one step, producing a single contiguous I-span. [SS-DOCISPAN / Finding 0047] independently confirms this: "inserting 10 contiguous bytes creates 1 DOCISPAN entry, not 10" — because `insertspanf` receives one `typeispan` struct covering the entire range.

**The resulting tree change:**

One INSERT → one new bottom crum (containing the atom with all N bytes) → adopted as right sibling under a height-1 node → `splitcrumupwards` checks if that height-1 node now has 2 children → since `MAXBCINLOAF=1`, it does trigger a split. So a single INSERT causes tree structural work (one split, possibly a `levelpush` at the fullcrum), but always yields exactly one new leaf, not N leaves.

**The per-byte granularity is I-address granularity, not storage granularity.** Each of the N bytes gets its own I-address [INV-SINGLE-CHAR-GRANULARITY], but they are all packed into one `typegrantext` atom in one bottom crum. The comment "so text will fit" in `enf.h` signals the intent: the atom is large enough that one atom per crum is workable storage.

---

## Code Exploration

---

## Answer: One Leaf Per INSERT, Not One Leaf Per Byte

`MAXBCINLOAF=1` is a **tree fan-out limit** at the bottom level, not a constraint on how many bytes each leaf holds. A single `doinsert` of N bytes creates **one new bottom crum** containing all N bytes. Here is the complete trace.

---

### Step 1 — `doinsert` calls `inserttextingranf`

`doinsert` [do1.c:118]:
```c
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy (taskptr, docisaptr, vsaptr, ispanset)
```

`inserttextingranf` [granf1.c:44-47] is a one-line wrapper:
```c
bool inserttextingranf(...) {
    bool inserttextgr();
    return (inserttextgr (taskptr, granfptr, hintptr, textset, ispansetptr));
}
```

---

### Step 2 — `inserttextgr` packs all bytes into one `locinfo` and calls `insertseq` once

`inserttextgr` [granf2.c:83-109]:
```c
for (; textset; textset = textset->next) {
    locinfo.infotype = GRANTEXT;
    locinfo.granstuff.textstuff.textlength = textset->length;
    movmem(textset->string, locinfo.granstuff.textstuff.textstring,
           locinfo.granstuff.textstuff.textlength);
    insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);         // [granf2.c:99]
    tumblerincrement (&lsa, 0, textset->length, &lsa);
}
```

The outer `for` loop iterates over linked `typetext` segments in `textset`. A single FEBE INSERT produces one segment. `insertseq` is called **once**, with all N bytes packed into the single `locinfo` struct. There is no per-byte loop.

---

### Step 3 — The leaf (`typecbc`) holds a `typegrantext` of up to 950 bytes

The bottom crum struct [enf.h:84-107]:
```c
struct structcbc {
    ...
    typegranbottomcruminfo  cinfo;    // ONE record, not an array
};
```

`typegranbottomcruminfo` [wisp.h:100-104]:
```c
typedef struct structgranbottomcruminfo {
    typegranstuff granstuff;   // union: typegrantext OR typegranorgl
    INT infotype;
} typegranbottomcruminfo;
```

`typegrantext` [wisp.h:74-78]:
```c
typedef struct structgrantext {
    char textstring[GRANTEXTLENGTH];   // 950 bytes
    unsigned textlength;
} typegrantext;
```

`GRANTEXTLENGTH = 950` [common.h:115]:
```c
#define GRANTEXTLENGTH  950
```

Each leaf node has **one** `cinfo` slot (a union, not an array), and that slot's text buffer holds up to **950 bytes**.

---

### Step 4 — `insertseq` creates one new leaf, not N leaves

`insertseq` [insert.c:17-70]:

**Path A — pack into existing leaf** (if adjacent leaf has room):
```c
if (info->infotype == GRANTEXT
 && ptr->cinfo.infotype == GRANTEXT
 && ptr->cinfo.granstuff.textstuff.textlength < GRANTEXTLENGTH) {
    if (!fillupcbcseq (ptr, &nextaddress, info)) {
        ivemodified ((typecorecrum*)ptr);
        return(0);                        // no new crum at all
    }
}
```

If all N bytes fit into the existing leaf, `fillupcbcseq` returns FALSE ("not overflowing"), `ivemodified` is called, and the function returns with **zero new crums created**.

**Path B — create one new leaf** (existing leaf is full or has different type):
```c
new = createcrum (0, (INT)ptr->cenftype);   // one new typecbc, height=0
adopt (new, RIGHTBRO, (typecorecrum*)ptr);
...
moveinfo (info, &((typecbc *)new)->cinfo);  // copy ALL N bytes in
```

`moveinfo` [wisp.h:117] is `movmem(A, B, sizeof(typebottomcruminfo))` — it copies the full `typegranbottomcruminfo` (with all N bytes in `textstring`) into the new leaf in a single shot. **One new leaf, holding all N bytes.**

---

### Step 5 — What does `MAXBCINLOAF=1` actually control?

`MAXBCINLOAF=1` [enf.h:27], comment: `/* so text will fit */`:
```c
#define MAXBCINLOAF    1        /* so text will fit *//* as you wish */
```

Used in `toomanysons` / `roomformoresons` [genf.c:244,260]:
```c
return (ptr->numberofsons > (ptr->height > 1
    ? MAXUCINLOAF
    : (is2dcrum(...) ? MAX2DBCINLOAF : MAXBCINLOAF)));
```

When `ptr->height == 1` (an interior node whose children are bottom crums), the max fan-out is `MAXBCINLOAF=1`. This means each height-1 internal node has at most **1 leaf child** — it is a structural tree balance parameter, not a byte-per-leaf constraint.

The comment "so text will fit" explains *why* 1 was chosen: a leaf node must hold the full `typegrantext[950]` in memory. If the fan-out were higher (e.g. 6 like `MAXUCINLOAF`), each "loaf" (disk block) would need to pack 6 such records, making disk blocks very large. Setting fan-out to 1 at the bottom means each leaf lives alone in its block and can use all available space for its 950-byte text buffer.

The consequence is that every INSERT of new text immediately triggers `splitcrumupwards` [insert.c:48] because the height-1 parent jumps from 1 to 2 sons (exceeding `MAXBCINLOAF=1`), propagating splits up the tree to maintain balance. But this is a structural bookkeeping effect, not a content effect.

---

### Summary

| Question | Answer |
|---|---|
| Does `doinsert` create 1 leaf for N bytes? | **Yes** — when the adjacent leaf is full or absent, `insertseq` creates exactly 1 `typecbc` and copies all N bytes in via `moveinfo` [insert.c:52] |
| Does `MAXBCINLOAF=1` mean each byte gets its own leaf? | **No** — it is the fan-out limit for height-1 internal nodes (max 1 leaf child per interior node), chosen so a single text record fits in one disk block |
| How much can one leaf hold? | Up to **950 bytes** (`GRANTEXTLENGTH` [common.h:115]) stored in `typegrantext.textstring` |
| Can INSERT produce zero new leaves? | **Yes** — if the adjacent leaf is a GRANTEXT crum with room, `fillupcbcseq` packs bytes in without allocating any new crum [insert.c:34-41] |

**The tree grows by at most 1 leaf per INSERT** (all N bytes in one `typecbc`), not by N leaves. `MAXBCINLOAF=1` forces every new leaf to be the sole child of a new height-1 parent, which triggers structural splits up the tree, but does not fragment the text content into per-byte leaves.
