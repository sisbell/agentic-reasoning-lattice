## Question 10 [evidence]

> When CREATENEWVERSION copies the source's text subspace POOM, does it deep-copy the bottom crums into freshly allocated tree nodes, or does the new version share any tree structure with the source's POOM?

## KB Synthesis

## Answer

CREATENEWVERSION performs a **deep copy** into freshly allocated tree nodes. The two POOMs share no structural nodes.

The mechanism is established by tracing the call chain in [ST-VERSION - Finding 0077]:

> `docreatenewversion` → `doretrievedocvspanfoo` (get source's V-span) → `docopyinternal` → `specset2ispanset` (convert V-spans to I-spans from source POOM) → `insertpm` (write into version's POOM)

The critical path is the `insertpm` call. `insertpm` → `insertnd` creates **new bottom crums** in the version's POOM via the same allocation mechanism used by regular text INSERT [ST-INSERT]. These are freshly allocated crum nodes, not pointers into the source's tree.

This is confirmed structurally by:

- **[FC-VERSION-ISOLATION]**: "Once a version is created via `CREATENEWVERSION`, it is a fully independent document with its own POOM tree. Edits to the original document modify only the original's POOM." A shared structure would not survive independent edits to either document.

- **[SS-POOM-MUTABILITY]**: "There are no copy-on-write semantics, no shadow copies." This explicitly rules out structural sharing.

- **[ST-VERSION-CREATE - Finding 0032]**: "`docreatenewversion` … `createorglingranf`" — a new, separate orgl is allocated for the version, giving it its own root.

**What is shared** is only the I-addresses (permascroll content identity) that the new POOM crums point to — that is precisely how content identity is preserved across versions [INV-TRANSITIVE-IDENTITY]. The POOM tree structure itself (crums, internal nodes) is all freshly allocated.

---

## Code Exploration

I now have all the evidence I need. Let me compile the definitive answer.

---

## CREATENEWVERSION POOM Copy: Deep Copy, No Structural Sharing

**Short answer:** CREATENEWVERSION performs a **complete deep copy**. Every node in the new version's POOM tree — both internal `typecuc` nodes and bottom `type2dcbc` crums — is freshly allocated via `eallocwithtag`. Zero tree structure is shared with the source document's POOM.

---

### Execution Path

#### 1. Entry: `docreatenewversion` — `do1.c:260`

```c
if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan))  // do1.c:281
    return FALSE;
...
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);  // do1.c:293
```

`doretrievedocvspanfoo` extracts the source document's **V-span** — a range descriptor (tumbler addresses) — not tree node pointers. The source POOM tree itself is never passed forward.

---

#### 2. `docopyinternal` — `do1.c:66`

```c
if (!findorgl (taskptr, granf, docisaptr, &docorgl, NOBERTREQUIRED)) return FALSE;  // do1.c:75
...
if (!insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)) return FALSE;  // do1.c:78
```

`docisaptr`/`docorgl` here is the **new document**'s POOM root — not the source's. `insertpm` is called on the new document. The source document is only referenced through the `ispanset` (translated V→I addresses), never through direct tree-node pointers.

---

#### 3. `insertnd` on the new POOM — `insertnd.c:15`

```c
case POOM:
    makegappm (taskptr, fullcrumptr, origin, width);  // insertnd.c:54
    ...
    bothertorecombine=doinsertnd(fullcrumptr,origin,width,infoptr,index);  // insertnd.c:57
    ...
    recombine (fullcrumptr);  // insertnd.c:76
```

`fullcrumptr` is the new document's POOM apex. `makegappm` cuts **the new tree** to make room. `doinsertnd` routes to `insertcbcnd`.

---

#### 4. `insertcbcnd` allocates fresh bottom crums — `insertnd.c:242`

```c
new = createcrum (0, (INT)father->cenftype);    // insertnd.c:260 — FRESH ALLOCATION
reserve (new);
adopt (new, SON, (typecorecrum*)father);         // insertnd.c:262
dspsub (origin, grasp, &new->cdsp, (INT)father->cenftype);
...
move2dinfo (infoptr, &((type2dcbc *)new)->c2dinfo);  // content metadata copied by value
```

Every bottom crum is **newly created**. `move2dinfo` copies the I-span content metadata by value into the new node. No pointer into the source tree is stored.

---

#### 5. `createcrum` → `createcruminternal` → `eallocwithtag` — `credel.c:518`

```c
typecorecrum *createcrum(INT crumheight, INT enftype)  // credel.c:518
{
    ptr = createcruminternal(crumheight, enftype, (typecorecrum*)NULL);
    ...
}

typecorecrum *createcruminternal(INT crumheight, INT enftype, typecorecrum *allocated)  // credel.c:541
{
    ...
    if (!allocated) {
        ptr = (typecorecrum *)eallocwithtag(crumsize, ...);  // credel.c:568 — malloc wrapper
    }
```

Every call to `createcrum` with `allocated=NULL` (which is every call in this path) produces a `malloc`-backed allocation. For POOM bottom crums, `crumsize = sizeof(type2dcbc)` [`credel.c:554`].

---

#### 6. `levelpush` (when POOM tree grows a level) — `genf.c:263`

```c
new=(typecuc *)createcrum ((INT)fullcrumptr->height,(INT)fullcrumptr->cenftype);  // genf.c:279
new->isleftmost = TRUE;
transferloaf (fullcrumptr, new);  // genf.c:282 — moves existing children by pointer rewiring
...
adopt ((typecorecrum*)new, SON, (typecorecrum*)fullcrumptr);  // genf.c:286
```

`levelpush` allocates a new internal `typecuc` node. `transferloaf` (genf.c:296) then moves the children by **pointer rewiring** — it sets `ptr->leftbroorfather = (typecorecrum *)to` and `from->leftson = NULL` — but these children are all **nodes already in the new document's tree**, not the source's. No source node is ever touched.

---

### Why No Structural Sharing

The V-span retrieved from the source at `do1.c:281` is purely an address range (tumblers). `specset2ispanset` (called at `do1.c:74`) converts this into I-span descriptors — again, pure address arithmetic. Neither function returns or stores source tree-node pointers. By the time `insertcbcnd` runs, it only has:
- `father`: a CUC node in the **new** document's tree
- `linfo` (`type2dbottomcruminfo`): content metadata copied by value from the I-span

There is no mechanism by which a source POOM node pointer can reach `createcrum` to be reused.

---

### Summary Table

| Location | What happens | Sharing? |
|---|---|---|
| `do1.c:281` | Source V-span extracted as tumbler address range | No node pointers taken |
| `do1.c:78` | `insertpm` called on **new** document's POOM | — |
| `insertnd.c:260` | `createcrum(0, POOM)` allocates fresh `type2dcbc` | No |
| `credel.c:568` | `eallocwithtag` (malloc) for each new crum | No |
| `genf.c:279` | `createcrum(height, POOM)` allocates fresh `typecuc` for new internal node | No |
| `genf.c:296` | `transferloaf` rewires children of **new** tree only | No |

**Conclusion:** CREATENEWVERSION does a complete deep copy. The new version's POOM tree is entirely independently allocated, bottom-to-apex. No node from the source document's POOM is adopted, referenced, or shared into the new version's tree.
