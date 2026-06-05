## Question 16 [evidence]

> After INSERT shifts text V-positions rightward, does the RETRIEVEDOCVSPAN root width grow by exactly the inserted width n, and does the reported start position remain unchanged?

## KB Synthesis

## Short Answer

For a **text-only document**, yes to both: the root width grows by exactly n and the start position is unchanged. For a **mixed document** (text + links), RETRIEVEDOCVSPAN is already misleading before any INSERT, so the post-INSERT behavior inherits that confusion.

---

## Detailed Synthesis

### What RETRIEVEDOCVSPAN actually reads

[SS-VSPAN-VS-VSPANSET] (Finding 0035): RETRIEVEDOCVSPAN reads the raw root POOM node's V-dimension displacement (`cdsp.dsas[V]`) and width (`cwid.dsas[V]`) directly via `retrievevspanpm()` — no subspace awareness, no processing.

From [SS-ENFILADE-TREE] (Finding 0066): In the 2D POOM enfilade, `root.cdsp` = minimum V-address across all content; `root.cdsp + root.cwid` = maximum extent. Together they form the bounding box.

---

### How INSERT modifies the POOM bounding box

[ST-INSERT] (Finding 0054): The two-blade knife restricts shifting to `[blade[0], blade[1]) = [insertion_point, (N+1).1)`. For INSERT at `1.x`, only entries in `[1.x, 2.1)` are shifted rightward by n. Entries before the insertion point and entries in the link subspace (`2.x`) are untouched.

[ST-INSERT] (Finding 0066): After insertion, `setwispupwards` recalculates `root.cdsp` as the new minimum across children.

**Width:** Content before the insertion is unchanged; content at or after the insertion shifts by n. The new maximum = old maximum + n. Since minimum is unchanged (insertion is not before the document start), `cwid' = cwid + n`. Width grows by exactly n. ✓

**Start position:** `root.cdsp` = minimum V-address. For insertion within or at the document's starting position, the minimum either stays at the old start (if inserting mid-document) or the new content lands at the old start position (if inserting at the very beginning — the new content occupies 1.start, old content shifts to 1.start+n, minimum stays 1.start). Start is unchanged. ✓

---

### Caveat: mixed documents

[SS-VSPAN-VS-VSPANSET] (Finding 0035, Bug 0011): For a document with both text (`1.x`) and links (internally `2.x`), RETRIEVEDOCVSPAN already returns a bounding-box width spanning both subspaces (e.g., `1.1 for 1.2`) — a structurally meaningless value. [FC-SUBSPACE] (Finding 0054) guarantees INSERT at `1.x` does not shift link entries at `2.x`, so the link subspace extent is preserved. But the reported bounding-box width after INSERT still spans both subspaces and remains misleading. For mixed documents, use RETRIEVEDOCVSPANSET to get semantically correct per-subspace extents.

---

## Code Exploration

I now have all the data needed. Let me compile the complete answer with code citations and golden test verification.

---

## Answer

### Short Answer

**Yes on both counts.** After INSERT of n characters, `RETRIEVEDOCVSPAN` reports a root width that grows by exactly n, and the start position (stream) is unchanged. This is confirmed by both source-code analysis and golden-test data.

---

### Code Path: INSERT to POOM to RETRIEVEDOCVSPAN

**1. `doinsert` [do1.c:87–122]** calls `inserttextingranf` (allocates content in the granfilade, producing an I-span set), then:

```c
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy(taskptr, docisaptr, vsaptr, ispanset)  // [do1.c:118–119]
```

**2. `docopy` [do1.c:45–65]** calls `insertpm` with the document's POOM orgl and the V-address `vsaptr`.

**3. `insertpm` [orglinks.c:75–134]** calls `insertnd` on the POOM:

```c
insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // [orglinks.c:130]
tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr);  // advance vsa for next crum [orglinks.c:131]
```

**4. `insertnd` [insertnd.c:15–111]** — for POOM type [insertnd.c:53–61]:

```c
case POOM:
    makegappm(taskptr, fullcrumptr, origin, width);    // [insertnd.c:54]
    setwispupwards(fullcrumptr, 0);
    bothertorecombine = doinsertnd(fullcrumptr, origin, width, infoptr, index);  // [insertnd.c:57]
    setwispupwards(fullcrumptr, 1);    // recalculates wid/dsp up the whole tree [insertnd.c:58]
    break;
```

---

### How Root `cwid` (Width) Grows

**`makegappm` [insertnd.c:124–172]** cuts the POOM at `vsaptr` and shifts every child-crum that is to the RIGHT of the cut point:

```c
case 1:  /* crum is at or right of the insert position */
    tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);  // [insertnd.c:162]
    ivemodified(ptr);
    break;
```

Every crum at V ≥ vsaptr has its V-displacement increased by n. Then `doinsertnd` [insertnd.c:185–197] places the new crum at vsaptr with width n.

**`setwispupwards` → `setwispnd` [wisp.c:171–228]** recalculates each node's width as the maximum reach of its children:

```c
for (ptr = findleftson(father); ptr; ptr = getrightbro(ptr)) {
    lockadd((tumbler*)&ptr->cdsp, (tumbler*)&ptr->cwid, (tumbler*)&tempwid, widsize...);
    lockmax((tumbler*)&newwid, (tumbler*)&tempwid, (tumbler*)&newwid, widsize...);  // [wisp.c:213–214]
}
// ...
movewisp(&newwid, &father->cwid);  // [wisp.c:225]
```

Since the shifted crums now reach n farther in V, the root's `cwid.dsas[V]` increases by exactly n.

---

### How Root `cdsp` (Start Position) Is Unchanged

`setwispnd` [wisp.c:192–203] computes the **minimum** child displacement and bubbles it up:

```c
movewisp(&ptr->cdsp, &mindsp);  // initialize to first child
for (ptr = getrightbro(ptr); ptr; ...) {
    lockmin(&mindsp, &ptr->cdsp, &mindsp, ...);  // find minimum [wisp.c:195]
}
lockiszerop = iszerolock((tumbler*)&mindsp, ...);
if (!lockiszerop) {
    dspadd(&father->cdsp, &mindsp, &newdsp, ...);  // father absorbs minimum [wisp.c:200]
    // children's cdsp adjusted: ptr->cdsp -= mindsp  [wisp.c:211]
} else {
    movewisp(&father->cdsp, &newdsp);  // unchanged [wisp.c:202]
}
```

For any insert at vsaptr ≥ document start:
- Crums to the LEFT of vsaptr are not shifted — the leftmost crum's cdsp stays 0 in its parent's frame.
- `mindsp = 0` → `lockiszerop = TRUE` → parent's `cdsp` unchanged.
- This propagates to the root: root's `cdsp.dsas[V]` does not change.

---

### RETRIEVEDOCVSPAN Reads These Directly

**`doretrievedocvspan` [do1.c:312–319]** → **`retrievevspanpm` [orglinks.c:165–172]**:

```c
bool retrievevspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler(&((typecuc *)orgl)->cdsp.dsas[V], &vspanptr->stream);  // start position
    movetumbler(&((typecuc *)orgl)->cwid.dsas[V], &vspanptr->width);   // width
    return (TRUE);
}
```

It reads the POOM root's `cdsp.dsas[V]` for stream (start) and `cwid.dsas[V]` for width — both fields recalculated by `setwispupwards` after each insert.

---

### Empirical Confirmation: Golden Tests

All four observed cases match the invariants exactly:

| Test | Before insert | Insert | After insert | Width delta |
|------|--------------|--------|--------------|-------------|
| `retrieve_vspan` | empty | "Hello World" (11) at 1.1 | start=1.1, width=0.11 | +11 |
| `insert_vspace_mapping` | start=1.1, width=0.5 | "XY" (2) at 1.3 | start=1.1, width=0.7 | +2 ✓ |
| `insert_middle` | start=1.1, width=0.10 | ", " (2) at 1.6 | start=1.1, width=0.12 | +2 ✓ |
| `multiple_inserts` (3 ops) | 0→6→13→18 | 6, 7, 5 chars | start=1.1 every time | +6, +7, +5 ✓ |

Sources: `golden/documents/retrieve_vspan.json`, `golden/content/insert_vspace_mapping.json`, `golden/content/insert_middle.json`, `golden/content/multiple_inserts.json`.

---

### Conclusion

**Root width grows by exactly n.** `makegappm` [insertnd.c:162] shifts all crums at V ≥ vsaptr rightward by n. The new crum of width n is inserted at vsaptr. `setwispnd` [wisp.c:213–214] computes the new bounding box as max-reach over all children, which is exactly n larger than before.

**Start position is unchanged.** `setwispnd` [wisp.c:195–202] finds the minimum child cdsp; because the leftmost content is never shifted by a mid-document insert, that minimum is 0, so the parent absorbs nothing and every ancestor's cdsp including the root is left unchanged. `retrievevspanpm` [orglinks.c:168] copies the root's unchanged `cdsp.dsas[V]` directly into `vspanptr->stream`.

The only case where the start would change is an insert at a V-address strictly before the document's first character position — which the backend does not prevent (`acceptablevsa` [do2.c:110–113] always returns TRUE), but which normal client code never does since `findvsatoappend` [orglinks.c:29–49] always places vsaptr at or after the document's current lowest V-address.
