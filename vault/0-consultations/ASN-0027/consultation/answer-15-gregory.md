## Question 15 [gregory]

> If a document's entire text content is deleted and then new text is inserted, the new text gets fresh I-addresses — but does the POOM's V-address numbering restart from 1.1, or does it continue from the shifted position left by the delete?

## KB Synthesis

## V-Address Numbering After Delete-All + Insert

**Short answer:** V-addresses restart from whatever the client specifies (typically 1.1), but there is a crash bug that makes this case non-operational currently.

---

### The POOM Resets to Zero After Delete-All

From [SS-ENFILADE-TREE] / Finding 0058 and [EC-EMPTY-DOC] / Finding 0066:

When all content is deleted, `deletend` Case 1 (`disown + subtreefree`) frees every bottom crum. `setwispnd` then zeroes both fields on the empty root:

```
After delete-all: root.cdsp = 0, root.cwid = 0
```

This is confirmed by [INV-ENFILADE-RELATIVE-ADDRESSING]: "When all children of a 2D enfilade are deleted, `setwispnd` clears both `cdsp` and `cwid` to zero, restoring the empty state."

There is **no accumulated position offset** left over. The POOM is structurally empty.

---

### V-Addresses Are Caller-Specified, Not Auto-Incremented

From [ST-INSERT]: the client provides `vsaptr` (the target V-address) to `doinsert`. There is no internal "next position" counter. The system places content at whatever V-address the caller requests.

After delete-all with an empty POOM (`cdsp=0, cwid=0`), a subsequent `INSERT` at V-position 1.1 would set the first bottom crum's absolute displacement to 1.1, and `setwispnd` would set `root.cdsp = 1.1`. V-numbering **restarts from 1.1**, not from some post-delete shift residual.

---

### The Critical Caveat: Bug 0019

From [EC-EMPTY-DOC] / Finding 0058:

> "Finding 0064 confirms that the empty-after-delete state causes INSERT and VCOPY to crash (Bug 0019) because `firstinsertionnd()` assumes a bottom crum always exists. When `findleftson()` returns NULL (no bottom nodes), the code dereferences a null pointer."

So while the POOM *conceptually* resets to a state from which inserts would start at V:1.1, the implementation currently **crashes** if you attempt this. The delete-all + insert sequence is not operational.

---

### I-Addresses Do Not Restart

Even if the V-numbering resets, the I-addresses for new content do **not** restart. From [INV-MONOTONIC] and [INV-NO-IADDR-REUSE]:

- The granfilade is append-only; `findpreviousisagr` always finds the current maximum
- Deleted I-addresses are never reclaimed
- New inserts after delete-all get I-addresses beyond those of the formerly-deleted content

So: V-space numbering restarts from 1.1 (conceptually), I-space numbering continues monotonically from wherever the granfilade maximum sits — and `compare_versions` between the pre-delete state and the re-inserted content would report **no shared spans** ([INV-DELETE-NOT-INVERSE]).

---

## Code Exploration

---

## Answer

**The V-address numbering restarts from 1.1.** The delete leaves the POOM structurally empty — there is no "shifted position" to continue from, and no high-water mark anywhere in the system.

---

### Trace: The Delete Path

`dodeletevspan` [do1.c:158-167] → `deletevspanpm` [orglinks.c:145-152] → `deletend` [edit.c:31-76].

Inside `deletend`, each crum in the intersection of the delete range is classified by `deletecutsectionnd` [edit.c:235-248]:

- **Case 1** (crum entirely within the deleted range): `disown` + `subtreefree` — the crum is physically removed from the tree.
- **Case 2** (crum to the right of the deleted range): `tumblersub` shifts the crum's displacement left by `width`.

```c
case 1:
    disown ((typecorecrum*)ptr);
    subtreefree ((typecorecrum*)ptr);   // [edit.c:59-60]
    break;
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);  // [edit.c:63]
    break;
```

When the **entire** document content is deleted, every text crum falls into Case 1. No crums survive. Case 2 (the shift that would "leave a position") never fires. After `setwispupwards(father, 1)` [edit.c:74] propagates widths back up, the POOM root's `cwid.dsas[V]` is zero.

`isemptyorgl` [orglinks.c:539-543] confirms the result:

```c
bool isemptyorgl(typeorgl fullcrumptr)
{
    return (
       iszerolock ((tumbler*)&((typecuc*)fullcrumptr)->cwid, widsize(POOM))
    && iszerolock ((tumbler*)&((typecuc*)fullcrumptr)->cdsp, dspsize(POOM)));
}
```

Both `cwid` (width) and `cdsp` (displacement) are zero. The POOM is indistinguishable from `createenf(POOM)` — a fresh, never-used document.

---

### Trace: The Re-insert Path

`doinsert` [do1.c:87-123] calls `docopy(taskptr, docisaptr, vsaptr, ispanset)` [do1.c:119], passing the **client-provided VSA** unchanged.

`acceptablevsa` [do2.c:110-113] is a stub:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

No validation. Any non-zero VSA is accepted.

`docopy` → `insertpm` [orglinks.c:75-134]. The only rejection is zero:

```c
if (iszerotumbler (vsaptr)){
    return (FALSE);   // [orglinks.c:86-91]
}
```

`insertpm` places the VSA directly into the new crum:

```c
movetumbler (vsaptr, &crumorigin.dsas[V]);   // [orglinks.c:113]
...
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // [orglinks.c:130]
```

`insertnd` → `doinsertnd` [insertnd.c:185-197]. After delete-all, `isemptyenfilade(father)` is TRUE, so it calls `firstinsertionnd`:

```c
if (isemptyenfilade (father)) {
    firstinsertionnd (father, origin, width, infoptr);  // [insertnd.c:192-193]
    return(FALSE);
}
```

`firstinsertionnd` [insertnd.c:199-218] creates a new bottom crum (if needed) and places the origin directly:

```c
movewisp (origin, &ptr->cdsp);   // [insertnd.c:212] — client's VSA becomes the crum displacement
movewisp (width, &ptr->cwid);
```

Whatever the client passed as VSA is now the displacement of the first POOM crum. **The POOM has no memory of previous V-addresses.**

---

### The Append Case Is Even More Explicit

For append operations, `appendpm` [orglinks.c:17-27] calls `findvsatoappend` [orglinks.c:29-49]:

```c
if (
   iszerolock ((tumbler*)&ptr->cwid, widsize(POOM))   // empty POOM
|| (tumblercmp (&grasp.dsas[V], &linkspacevstart) != LESS)) {
    tumblerincrement (vsaptr, 0, 1, vsaptr); /* no text in doc */
    tumblerincrement (vsaptr, 1, 1, vsaptr);           // VSA = 1.1
```

When the POOM is empty after delete-all, `iszerolock` on `cwid` is TRUE, and the function explicitly returns **1.1**.

---

### Golden Test Confirmation

The `delete_all_content_simple` golden test records actual backend behavior:

```json
// After insert "Test content" at 1.1:
"before_delete": { "spans": [{ "start": "1.1", "width": "0.12" }] }

// After deleting the entire span:
"after_delete": { "spans": [] }

// After re-inserting "After delete" at 1.1:
"reinsert_vspans": { "spans": [{ "start": "1.1", "width": "0.12" }] }
```

The re-inserted content occupies **1.1 → 1.1+0.12** — identical to the first insertion. The `empty_document_never_filled` baseline shows the same: a fresh document's first insert at 1.1 produces `start=1.1, width=0.13`.

---

### Summary

| Mechanism | Behavior |
|---|---|
| `deletend` case 1 [edit.c:58-60] | Frees all crums when all content is deleted |
| `deletend` case 2 [edit.c:63] | Shifts surviving crums — never fires in total delete |
| `isemptyorgl` [orglinks.c:539] | Confirms POOM is empty after delete-all |
| `acceptablevsa` [do2.c:110-113] | Always returns TRUE — no VSA validation |
| `firstinsertionnd` [insertnd.c:199] | Places client-provided VSA directly into new crum |
| `findvsatoappend` [orglinks.c:41-43] | Explicitly returns 1.1 when POOM is empty |

**The POOM carries no "high-water mark."** After delete-all, it is structurally identical to `createenf(POOM)`. The V-address for the next insert is **entirely determined by the client's argument** — and both the FEBE test harness and the `doappend` path choose 1.1. The numbering restarts at 1.1.
