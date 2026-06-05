## Question 12 [evidence]

> Does the span returned by RETRIEVEDOCVSPAN derive its start position from the 2D POOM root's displacement coordinate (tracked via `setwispnd`), and is that displacement guaranteed to equal the minimum V-address of any current POOM bottom crum?

## KB Synthesis

**Yes to both, with one qualification.**

**RETRIEVEDOCVSPAN reads root.cdsp directly**

`RETRIEVEDOCVSPAN` calls `retrievevspanpm()` which copies the raw root node's `cdsp.dsas[V]` and `cwid.dsas[V]` without further processing [SS-VSPAN-VS-VSPANSET, Finding 0035; code at `orglinks.c:165-172`]. No subspace filtering or tree traversal occurs — it is a straight read of the root fields.

**root.cdsp.dsas[V] is guaranteed to equal the minimum V-address in the POOM**

This is the defining invariant of 2D enfilades. `setwispnd` after every modification: (1) finds `mindsp = min(child.cdsp)`, (2) adds it to the parent's `cdsp`, (3) subtracts it from each child's `cdsp`, making children relative. The result is `root.cdsp = absolute minimum address in the subtree` [INV-ENFILADE-RELATIVE-ADDRESSING; SS-ENFILADE-TREE Finding 0066; `wisp.c:171-228`].

**The qualification: which subspace is the minimum?**

Because text occupies V-addresses `1.x` and links occupy `2.x`, and `1 < 2` in tumbler order, the minimum is always the text subspace start. This is why `cdsp.dsas[V]` points to position `1` [SS-DUAL-ENFILADE, Finding 0043]. The link subspace at `2.x` is structurally *above* the recorded displacement — the root's `cdsp` reflects the text minimum, not the link positions.

For a document with both text and links, `root.cwid` bridges the full range from `1.x` to `2.x`, producing the misleading bounding-box width documented in [EC-VSPAN-MISLEADING-SIZE].

**Empty document edge case:** An empty POOM has `cdsp = 0` and `cwid = 0` — both zero simultaneously signals emptiness for 2D enfilades [EC-EMPTY-DOC, Finding 0066].

---

## Code Exploration

I now have everything needed to write the full answer. Here it is:

---

## Does RETRIEVEDOCVSPAN's start derive from the POOM root's displacement, and does that equal the minimum V-address of any bottom crum?

**Short answer: Yes to both, with a full traceable code chain.**

---

### Part 1 — The Call Chain to `cdsp.dsas[V]`

`RETRIEVEDOCVSPAN` dispatches through three layers before reading any field:

**`fns.c:303–315`** — `retrievedocvspan` is the top-level handler:
```c
void retrievedocvspan(typetask *taskptr) {
  typeisa docisa;
  typevspan vspan;
  ...
  if (getretrievedocvspan(taskptr, &docisa)
   && doretrievedocvspan(taskptr, &docisa, &vspan))
      putretrievedocvspan(taskptr, &vspan);
```

**`do1.c:312–319`** — `doretrievedocvspan` resolves the document's POOM enfilade root via `findorgl`, then delegates:
```c
bool doretrievedocvspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr) {
  typeorgl docorgl;
  ...
  return
     findorgl(taskptr, granf, docisaptr, &docorgl, READBERT)
  && retrievevspanpm(taskptr, docorgl, vspanptr);
}
```

**`orglinks.c:165–172`** — `retrievevspanpm` is where the span is constructed. It reads exactly two fields from the root (`typecuc *`) and puts them directly into `vspanptr`:
```c
bool retrievevspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr) {
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler(&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);  // start
    movetumbler(&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);   // width
    return (TRUE);
}
```

`vspanptr->stream` (the start position) is literally `root->cdsp.dsas[V]` — no arithmetic, no indirection. The redundantly-named `retrievedocumentpartofvspanpm` at `orglinks.c:155–162` (called by the old `doretrievedocvspanfoo` path) is byte-for-byte identical.

---

### Part 2 — Is `root->cdsp.dsas[V]` Guaranteed to Equal the Minimum V-Address?

**Yes**, because `setwispnd` enforces this as a structural invariant at every node, and `setwispupwards` propagates the invariant to the root after every mutation.

#### The `setwispnd` invariant (`wisp.c:171–228`)

For a POOM node, `setwispnd` normalises children's displacements so that the **minimum direct-child `cdsp` is always zero**, absorbing that minimum into the parent:

```c
// Step 1: find minimum child displacement (wisp.c:192–195)
movewisp(&ptr->cdsp, &mindsp);
for (ptr = getrightbro(ptr); ptr; ptr = getrightbro(ptr))
    lockmin((tumbler*)&mindsp, (tumbler*)&ptr->cdsp, (tumbler*)&mindsp,
            (unsigned)dspsize(ptr->cenftype));

// Step 2: absorb into parent (wisp.c:198–202)
if (!lockiszerop) {
    somethingchangedp = TRUE;
    dspadd(&father->cdsp, &mindsp, &newdsp, (INT)father->cenftype); // newdsp = parent + mindsp
} else {
    movewisp(&father->cdsp, &newdsp);
}

// Step 3: subtract minimum from each child (wisp.c:208–212)
for (ptr = findleftson(father); ptr; ptr = getrightbro(ptr)) {
    if (!lockiszerop) {
        ptr->modified = TRUE;
        dspsub(&ptr->cdsp, &mindsp, &ptr->cdsp, (INT)ptr->cenftype); // child -= mindsp
    }
    ...
}

// Step 4: commit (wisp.c:224–225)
movewisp(&newdsp, &father->cdsp);
movewisp(&newwid, &father->cwid);
```

**Invariant maintained**: after each call, `min(direct_child.cdsp) = 0`. Children's absolute V-addresses are preserved because any gain in `father->cdsp` is exactly offset by the subtraction from each child.

#### Recursive implication for the root

Addresses in the POOM are accumulated top-down: absolute V-address of a bottom crum = `root->cdsp.dsas[V]` + (sum of all intermediate `cdsp.dsas[V]` values from root to leaf). Because `setwispnd` zeroes the minimum at every level:

- The minimum-address bottom crum has `cdsp.dsas[V] = 0` at every ancestor level
- Its absolute V-address = `root->cdsp.dsas[V]` + 0 + 0 + … + 0

Therefore `root->cdsp.dsas[V]` **is** the minimum absolute V-address of any bottom crum.

#### `setwispupwards` ensures the root is always current (`wisp.c:83–111`)

```c
for (changed = TRUE; changed && ptr; ptr = father) {
    father = findfather((typecorecrum*)ptr);
    changed = setwisp((typecorecrum*)ptr);
    ...
}
```

This walks from the modified node up to the root, calling `setwispnd` at each level. When `ptr` is the root, `findfather(root) = NULL`, the loop calls `setwispnd(root)` and then exits cleanly.

**`insertnd` (`insertnd.c:53–61`)** calls `setwispupwards` in the POOM branch both before and after the actual insert:
```c
case POOM:
    makegappm(taskptr, fullcrumptr, origin, width);
    checkspecandstringbefore();
    setwispupwards(fullcrumptr, 0);    // line 56 — pre-insert normalise
    bothertorecombine = doinsertnd(fullcrumptr, origin, width, infoptr, index);
    setwispupwards(fullcrumptr, 1);    // line 58 — post-insert propagation
    break;
```

Within the recursive descent of `doinsertnd → insertmorend → insertcbcnd`, setwispupwards is also called at multiple levels:

- **`insertmorend` `insertnd.c:236`**: `setwispupwards(father, 1)` after each recursive call
- **`insertcbcnd` `insertnd.c:253`**: `setwispupwards(father, 1)` on extension
- **`insertcbcnd` `insertnd.c:270–271`**: `setwispupwards(new, 0)` then `setwispupwards(father, 1)` for new leaf

The comment on `insertnd.c:235` — `/*setwispupwards(ptr,1);*/ /* was done in insertcbcnd*/` — confirms that setwispupwards is already handled at the leaf level; the `insertmorend` call at line 236 exists to cover the return path.

---

### Edge case: `makegappm` guard

`makegappm` (`insertnd.c:140–143`) short-circuits if the insertion point is outside the current span:
```c
if (iszerotumbler(&fullcrumptr->cwid.dsas[V])       // empty
 || tumblercmp(&origin->dsas[V], &grasp.dsas[V]) == LESS   // before current min
 || tumblercmp(&origin->dsas[V], &reach.dsas[V]) != LESS)  // at or after max
    return(0);    /* this if for extensions to bc without calling cut */
```

When `origin < grasp` (inserting at a new minimum V-address), `makegappm` returns 0 without calling its own `setwispupwards`. However, `insertnd` still calls `setwispupwards(fullcrumptr, 1)` at line 58 after `doinsertnd`, so the root's `cdsp.dsas[V]` is still recalculated. In practice this case is also avoided by the FEBE protocol: `findnextlinkvsa` (`do2.c:151–167`) always computes the next VSA as `stream + width` of the current document span, ensuring all inserts append beyond the current maximum.

---

### Summary

| Claim | Code location | Verdict |
|---|---|---|
| `vspanptr->stream` = `root->cdsp.dsas[V]` | `orglinks.c:169` | **Yes, directly** |
| `setwispnd` normalises so min child `cdsp` = 0 | `wisp.c:192–225` | **Yes, invariant enforced** |
| Root's `cdsp.dsas[V]` = absolute minimum V-address of any bottom crum | Recursive application of above | **Yes, by induction on tree depth** |
| `setwispupwards` propagates to root after every insert | `insertnd.c:58`, `insertmorend:236`, `insertcbcnd:253,270,271` | **Yes** |

The displacement returned as `stream` by RETRIEVEDOCVSPAN is `root->cdsp.dsas[V]`, maintained by `setwispnd` to equal the minimum V-address of any current POOM bottom crum. The guarantee is structural (enforced at every node in every modification path), not merely conventional.
