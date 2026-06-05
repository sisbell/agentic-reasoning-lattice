## Question 13 [evidence]

> For an empty-after-DELETE document whose POOM tree retains intermediate nodes (levelpull disabled), does RETRIEVEDOCVSPAN return a zero-width span or does the residual tree height affect the reported root width?

## KB Synthesis

**RETRIEVEDOCVSPAN returns zeros (zero displacement, zero width) regardless of residual tree height.**

RETRIEVEDOCVSPAN (opcode 14) reads only two fields from the root node: `cdsp.dsas[V]` and `cwid.dsas[V]`, via `retrievevspanpm()` with no further processing. [SS-VSPAN-VS-VSPANSET] Finding 0035: "reads the raw root node's V-dimension displacement and width directly."

When DELETE removes all bottom crums, `deletend` Case 1 (`disown` + `subtreefree`) frees them, then calls `setwispupwards`. The key is what `setwispnd` does when a node has no children: it clears **both** `cdsp` and `cwid` to zero. [SS-ENFILADE-TREE] Finding 0066 explicitly states: "When all children of a 2D enfilade are deleted, `setwispnd` clears both `cdsp` and `cwid` to zero (`wisp.c:187-189`), restoring the empty state."

The intermediate nodes that remain (because `levelpull` is disabled) are empty structural artifacts — they have `numberofsons = 0` and contribute nothing to the root's widdative fields. The root's `cwid` and `cdsp` are computed bottom-up from actual leaf content, not from tree height. [SS-ENFILADE-TREE] Finding 0058 confirms: "retrieve_vspanset → empty (zero-width)" after delete-all, and [SS-VSPAN-VS-VSPANSET] Finding 0035 documents: "Empty document: RETRIEVEDOCVSPAN returns zeros."

The residual tree height is purely a structural property with no effect on the reported span.

---

## Code Exploration

Now I have everything I need. Let me trace the complete execution path precisely.

---

## Answer: RETRIEVEDOCVSPAN After Full DELETE With levelpull Disabled

**The answer is: RETRIEVEDOCVSPAN returns a zero-width span. The residual tree height does not affect the reported root width.**

Here is the complete code trace supporting that claim.

---

### 1. The Call Chain

`RETRIEVEDOCVSPAN` → `fns.c:303-315` → `doretrievedocvspan` → `retrievevspanpm`

`fns.c:303-315`:
```c
void retrievedocvspan(typetask *taskptr)
{
    ...
    if (
       getretrievedocvspan (taskptr, &docisa)
    && doretrievedocvspan (taskptr, &docisa, &vspan))
        putretrievedocvspan (taskptr, &vspan);
```

`do1.c:312-320`:
```c
bool doretrievedocvspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
  bool findorgl(), retrievevspanpm();

    return
       findorgl (taskptr, granf, docisaptr, &docorgl, READBERT)
    && retrievevspanpm (taskptr, docorgl, vspanptr);
}
```

**Critical observation:** Unlike `doretrievedocvspanset` (`do1.c:330-333`), this function has **no `isemptyorgl` guard**. It calls `retrievevspanpm` unconditionally.

`orglinks.c:165-172`:
```c
bool retrievevspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
    return (TRUE);
}
```

The width returned is a **direct, verbatim read from the root crum's `cwid.dsas[V]` field**. No tree traversal, no height-dependent logic — just a field copy from whatever is stored in the fullcrum. The question therefore reduces to: *what is in `cwid.dsas[V]` of the root after a deletion that empties the document?*

---

### 2. levelpull Is Already Stubbed Out

`genf.c:318-342`:
```c
int levelpull(typecuc *fullcrumptr)
{
/*  typecuc *ptr; */
return(0);
/*
    if (!isfullcrum (fullcrumptr))
    ...
    dspadd (&fullcrumptr->cdsp, &ptr->cdsp, &fullcrumptr->cdsp, fullcrumptr->cenftype);
    disown (ptr);
    fullcrumptr->height--;
    transferloaf (ptr, fullcrumptr);
    setwispupwards (fullcrumptr,1);
    freecrum (ptr);
*/
}
```

The entire body is commented out. `levelpull` returns 0 immediately. This means the existing production behavior **already is** "levelpull disabled" — intermediate nodes are never collapsed regardless of how many children they have. The question's hypothetical is the actual state of the code.

---

### 3. The Deletion Path

`dodeletevspan` (`do1.c:158-167`) calls `deletevspanpm` (`orglinks.c:145-152`):

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    ...
}
```

`deletend` (`edit.c:31-76`) performs the actual tree surgery, then **at line 74**:

```c
setwispupwards (father,1);
recombine (father);
```

`setwispupwards` (`wisp.c:83-111`) climbs from `father` to the root, calling `setwisp` at each level:

```c
for (changed = TRUE; changed && ptr; ptr = father) {
    father = findfather ((typecorecrum*)ptr);
    changed = setwisp ((typecorecrum*)ptr);
    ...
}
```

For POOM nodes, `setwisp` calls `setwispnd` (`wisp.c:171-228`).

---

### 4. setwispnd — The Key Width Propagation Logic

`wisp.c:185-191` — **when a node's last child has been deleted:**

```c
if ((ptr = findleftson (father)) == NULL) {
    /* All children deleted - clear width and mark modified */
    clear (&father->cdsp, sizeof(father->cdsp));
    clear (&father->cwid, sizeof(father->cwid));
    ivemodified((typecorecrum*)father);
    return (TRUE);
}
```

When all leaf crums under `father` are disowned and freed, `findleftson(father)` returns `NULL`, and **both `cwid` and `cdsp` are zeroed unconditionally**. `changed = TRUE` is returned, so `setwispupwards` continues climbing.

`wisp.c:207-225` — **when a node has remaining children (e.g., a retained intermediate node with zero extent):**

```c
clear (&newwid, sizeof(newwid));
for (ptr = findleftson (father); ptr; ptr = getrightbro (ptr)) {
    ...
    lockadd((tumbler*)&ptr->cdsp, (tumbler*)&ptr->cwid, (tumbler*)&tempwid,
            (unsigned)widsize(ptr->cenftype));
    lockmax((tumbler*)&newwid, (tumbler*)&tempwid, (tumbler*)&newwid,
            (unsigned)widsize(ptr->cenftype));
}
...
movewisp (&newwid, &father->cwid);
```

`newwid` is the bounding box: the `lockmax` over `(child->cdsp + child->cwid)` for every child. If an intermediate node has `cdsp = 0` and `cwid = 0` (already zeroed by the level below), then `tempwid = 0`, and `newwid` remains 0. **The parent correctly inherits zero width even when the intermediate child node is still structurally present.**

---

### 5. Complete Trace for a Typical Delete-All Scenario

Assume tree height = 2 before deletion:

```
Root (fullcrum, height 2, cwid = W)
  └── NodeA (height 1, cwid = W)
        ├── Leaf0 (height 0)
        └── Leaf1 (height 0)
```

After `deletend` with a span covering all content:

1. Leaf0 and Leaf1 are `disown`ed and `subtreefree`d. `father = NodeA`.
2. `setwispupwards(NodeA, 1)`:
   - `setwispnd(NodeA)`: `findleftson(NodeA) == NULL` → `NodeA->cwid = 0`, `NodeA->cdsp = 0`. Returns `TRUE`.
   - `setwispnd(Root)`: `findleftson(Root) = NodeA`. `NodeA->cdsp = 0`, `NodeA->cwid = 0` → `tempwid = 0` → `newwid = 0` → `Root->cwid = 0`.

With levelpull disabled, NodeA is **not removed** — `Root` still has NodeA as a child. But `Root->cwid = 0` regardless.

`retrievevspanpm` reads `Root->cwid.dsas[V] = 0` and returns:

```
stream = Root->cdsp.dsas[V]   (also 0 after deletion)
width  = Root->cwid.dsas[V]   = 0
```

---

### 6. Conclusion

**RETRIEVEDOCVSPAN returns a zero-width span.** The residual tree height left by disabled `levelpull` has no effect on the reported root width, because:

- Width is read directly from the root's `cwid.dsas[V]` field by `retrievevspanpm` (`orglinks.c:169-170`).
- After deletion, `setwispupwards` (`wisp.c:83-111`) propagates zeroed widths from the deleted level all the way up to the root through `setwispnd` (`wisp.c:171-228`).
- `setwispnd` correctly zeroes a node whether its children are all gone (`wisp.c:185-191`) or are structurally present but have zero extent (`wisp.c:207-215`).
- The retained intermediate nodes (due to `levelpull` being stubbed out at `genf.c:321`) have their own widths zeroed by the time `setwispnd` runs on their parent, so the root's width calculation sees zero from each retained intermediate node regardless.

The tree structure (height, number of intermediate nodes) is invisible to `retrievevspanpm`; it only reads the cached width at the root, and that cached value is correctly maintained at zero by `setwispupwards` after every deletion.
