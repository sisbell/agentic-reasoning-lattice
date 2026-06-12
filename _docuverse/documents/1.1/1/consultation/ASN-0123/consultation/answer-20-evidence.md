## Question 20 [evidence]

> If the source document is itself modified between two successive CREATENEWVERSION calls, do the two resulting versions' POOMs snapshot different V→I mappings while their document addresses remain siblings (`.0.1`, `.0.2`) under the same source — i.e., is the sibling numbering ordered strictly by creation time rather than by content state?

## KB Synthesis

Yes to all three, and the mechanisms are distinct enough to be worth separating.

---

## 1. Two CREATENEWVERSION calls snapshot different V→I mappings if the source is modified between them

`docreatenewversion` is atomic: it reads the source POOM at call time via `doretrievedocvspanfoo`, then copies the current text subspace (1.x V→I mappings only) into the new orgl via `docopyinternal` [ST-VERSION-CREATE, Finding 0032]. That copy is immediately independent — edits to the source affect only the source's POOM, not the version's [FC-VERSION-ISOLATION].

So:

```
t1: CREATENEWVERSION(source)  →  version1.poom = snapshot of source.poom at t1
    INSERT into source         →  source.poom changes
t2: CREATENEWVERSION(source)  →  version2.poom = snapshot of source.poom at t2
```

`version1.poom ≠ version2.poom` whenever any INSERT, DELETE, or REARRANGE happened between the calls. `compare_versions(version1, version2)` would report only the I-addresses present in both snapshots as shared [SS-COMPARE-VERSIONS].

Note: both versions inherit link discoverability from the source for whatever text I-addresses they captured, but neither has link subspace entries in its own POOM [ST-VERSION-CREATE, Finding 0043].

---

## 2. Both version addresses are siblings under the source document

The version address allocation follows the child-depth rule: `version_address ∈ children(source_doc)` for owned documents [SS-VERSION-ADDRESS, Finding 0068]. Two successive versions of the same source both get addresses with the source's address as their prefix:

```
source:    1.1.0.1.0.1
version1:  1.1.0.1.0.1.1   (first child)
version2:  1.1.0.1.0.1.2   (next sibling)
```

These are siblings in the address hierarchy, which is structurally how the system encodes "version of" vs. "independent copy" [SS-VERSION-ADDRESS, Finding 0032].

---

## 3. Sibling numbering is ordered strictly by creation time, not content state

The allocator is a stateless query-and-increment on the granfilade tree [SS-ADDRESS-ALLOC, Finding 0068]:

1. `findpreviousisagr` finds the highest existing address under the source
2. Increment by 1 → the new version address

The allocator inspects only the granfilade's current maximum child address — it has no knowledge of what content was copied, how much changed, or whether the new version is "bigger" or "smaller" than the prior one. The sequence `.1`, `.2`, `.3` is purely chronological.

This is guaranteed by [INV-MONOTONIC] (Finding 0068): "Version address allocation is monotonically increasing within each document's version namespace... The sequence `.1`, `.2`, `.3` under a document never reuses a previously allocated version address." Deleted versions leave their address permanently in the granfilade, so the next allocation continues past them.

---

**Bottom line:** Sibling address = creation order. POOM content = source state at creation time. The two properties are orthogonal — the allocator does not look at content, and the POOM copy does not influence addressing.

---

## Code Exploration

I now have everything needed for a complete, code-grounded answer.

---

## Answer

### Short answer

**Yes on both counts.** The two versions receive POOM snapshots of whichever V→I state the source document held at the exact moment each call was made, and their document addresses are sequentially numbered children of the source (`D.1`, `D.2`) — allocated strictly by creation order with no dependence on content state.

---

### 1. POOM snapshot is taken at call time

The execution path in `docreatenewversion` [`do1.c:260–299`]:

```c
// do1.c:281–293
if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) {
    return FALSE;
}
vspec.vspanset = &vspan;
...
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
```

`doretrievedocvspanfoo` calls `retrievedocumentpartofvspanpm` [`orglinks.c:155–162`]:

```c
bool retrievedocumentpartofvspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{ /* this is a kluge*/
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
    return (TRUE);
}
```

This reads the **live root fields** of the source document's POOM enfilade: `cdsp.dsas[V]` (stream start) and `cwid.dsas[V]` (total V-space width). It is a direct field read, not a snapshot stored somewhere stable.

When the source is modified between the two calls — via `doinsert` → `docopy` → `insertpm` → `insertnd` [`orglinks.c:130`] — `insertnd` restructures the POOM tree, updating `cwid.dsas[V]` to reflect the new total V-width. The second CREATENEWVERSION call therefore reads a different (expanded) `cwid.dsas[V]`, and `docopyinternal` populates the second new version's POOM with a V-span that includes the newly inserted content.

The golden test `modify_original_after_version.json` confirms this behavior empirically:
- Version (`1.1.0.1.0.1.1`) was created before `" modified"` was appended to original
- Version contents: `"Original text"` — frozen at creation time
- Original contents after: `"Original text modified"`

If instead the version had been created *after* the modification, its POOM would have captured `"Original text modified"`. This is exactly the divergence the question describes: two successive CREATENEWVERSION calls on a source that is modified in between will produce two versions with distinct V→I mappings.

---

### 2. Sibling numbering is strictly creation-time ordered

`docreatenewversion` [`do1.c:270–277`] calls:

```c
makehint (DOCUMENT, DOCUMENT, 0, isaptr, &hint);
// ...
if (!createorglingranf(taskptr, granf, &hint, newisaptr)) { ... }
```

`makehint` [`do2.c:78–84`] stores `supertype = DOCUMENT (3)`, `subtype = DOCUMENT (3)`.

`createorglingranf` → `createorglgr` → `findisatoinsertgr` → `findisatoinsertnonmolecule` [`granf2.c:203–242`]:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;  // DOCUMENT==DOCUMENT → depth=1

// Scan for highest existing child below upperbound
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);

if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    // First version ever: D.1
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
} else {
    // Nth version: truncate to hintlength+1, increment
    tumblertruncate (&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr);
}
```

`findpreviousisagr` traverses the granfilade tree scanning for the **highest existing address** below the `upperbound` (`hintisa` + 1 at depth 0). It is a tree scan of which document-ISA entries exist — it reads granfilade structure, **not** POOM content. Modifications to a document via `insertpm` operate on the POOM (the enfilade embedded in the granfilade entry), not on the granfilade tree structure used for ISA address lookups. Therefore insertions into the source have no effect on the counter.

`tumblerincrement` [`tumble.c:599–623`]:

```c
cptr->mantissa[idx + rightshift] += bint;  // rightshift=depth=1
```

For source `D` = `[..., last_digit]` at mantissa position `idx`, this appends a new digit at `idx+1`. The Nth version appends `N` at that position.

The golden test `version_address_allocation.json` confirms the exact addresses:

| Operation | Address |
|---|---|
| `create_document doc1` | `1.1.0.1.0.1` |
| `create_version from doc1` | `1.1.0.1.0.1.1` |
| `create_version from doc1` (again) | `1.1.0.1.0.1.2` |
| `create_version from doc2` | `1.1.0.1.0.2.1` |
| `create_version from version1` | `1.1.0.1.0.1.1.1` |

The two versions of `doc1` are `D.1` and `D.2` — siblings under `D`, numbered strictly by which was created first. (The question's `.0.1`/`.0.2` notation is slightly off; the real addresses are `D.1`/`D.2` — a single digit appended, not two, because `depth=1` for the `DOCUMENT→DOCUMENT` hint.)

---

### Summary

The address counter (`findisatoinsertnonmolecule`) scans for the highest existing version child and increments by 1. It is completely blind to the source's content state. Whether the source has 0 bytes or 1,000,000 bytes of new insertions between call 1 and call 2, the second call gets `D.2`.

What *does* change between the two calls is what `retrievedocumentpartofvspanpm` reads from `orgl->cwid.dsas[V]`: the total V-width of the source POOM at that moment. If the source grew, the second version's POOM is initialized with a larger V-span via `docopyinternal`, capturing the V→I mapping as it stood when the call was made.

So: **yes, the sibling numbering is ordered purely by creation time; and yes, each version's POOM is an independent snapshot of the source's V→I state at the instant of that specific call.**
