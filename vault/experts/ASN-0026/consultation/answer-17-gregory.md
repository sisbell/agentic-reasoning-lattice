## Question 17 [gregory]

> After COPY creates shared I-address references between two documents, if the source document DELETEs that content, do the target document's POOM entries still resolve correctly through the granfilade — i.e., is there any reference-counting or liveness check that could invalidate the target's I→content mapping?

## KB Synthesis

Yes, the target document's POOM entries resolve correctly. No, there is no reference-counting or liveness check of any kind.

## What DELETE Actually Does

[FC-DELETE-CROSS-DOC] states this explicitly: DELETE operates on a single document's POOM tree only — `deletend` frees bottom crums from that document's orgl, and other documents' trees are completely separate data structures, untouched. The concrete consequence:

```
D has "ABCD", T transcluded "BC" (sharing I(5.2), I(5.3))

After DELETE "BC" from D:
  POOM(D): V(1.1)→I(5.1)  V(1.2)→I(5.4)    — BC mapping gone from D
  POOM(T): V(2.1)→I(5.2)  V(2.2)→I(5.3)    — UNCHANGED
  Granfilade: I(5.2)="B"  I(5.3)="C"        — content bytes persist
```

## Why the Granfilade Doesn't Care

[FC-GRANF-ON-DELETE] establishes that DELETE is a pure V-space operation — it never calls any granfilade modification function. `dodeletevspan` → `deletevspanpm` → `deletend` all operate exclusively on the POOM (document orgl enfilade). The granfilade is append-only; [INV-NO-IADDR-REUSE] confirms that deleted I-addresses remain allocated in the granfilade tree permanently and continue to influence future allocation (via `findpreviousisagr`).

[INV-IADDR-IMMUTABILITY] makes this a system-wide guarantee: "DELETE frees the POOM bottom crums that *reference* I-addresses, but the I-addresses themselves persist in the granfilade unconditionally."

## No Reference Counting

There is no reference counting, garbage collection, or liveness predicate anywhere. [SS-POOM-MUTABILITY] establishes the architecture: the granfilade is the immutable I-address store, the POOM is the per-document mutable V→I mapping, and these layers are independent. When T's POOM entry at V(2.1) is resolved, it looks up I(5.2) in the granfilade tree — a lookup that succeeds regardless of whether D still references I(5.2).

The only way T's I-address mappings could become unresolvable is if T itself DELETEs them, or if the content were never in the granfilade to begin with. The source document's lifecycle is irrelevant to T's retrieval path.

---

## Code Exploration

Now I have a complete picture. Let me compile the full answer.

---

## Full Analysis: COPY, DELETE, and I→Content Liveness in udanax-green

### The Short Answer

There is **no reference counting and no liveness check** that could invalidate a target document's I→content mapping after a source document deletes content. The target's POOM entries resolve correctly through the granfilade after the source deletes — because DELETE only removes V→I mappings from the *source's* own POOM. It never touches the granfilade, and it never touches any other document's POOM.

---

### Step 1: How COPY Creates Shared I-Addresses

`docopy()` [do1.c:45-65]:

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset) {
    return (
       specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)
    && findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && acceptablevsa(vsaptr, docorgl)
    && insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)
    && insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)
    );
}
```

The key step is `insertpm()` [orglinks.c:75-134]:

```c
for (; sporglset; sporglset = (typesporglset)sporglset->xxxxsporgl.next) {
    unpacksporgl(sporglset, &lstream, &lwidth, &linfo);
    movetumbler(&lstream, &crumorigin.dsas[I]);  // ← raw I-address copied in
    movetumbler(vsaptr,   &crumorigin.dsas[V]);  // ← new V-address in target
    insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
}
```

This inserts a new **2D bottom crum** into TARGET's POOM. The crum's structure is `type2dcbc` [enf.h:108-131]:

```c
struct struct2dcbc {
    /* ... corum header fields ... */
    typewid cwid;               // cwid.dsas[I] = I-width, cwid.dsas[V] = V-width
    typedsp cdsp;               // cdsp.dsas[I] = I-offset, cdsp.dsas[V] = V-offset
    type2dbottomcruminfo c2dinfo;  // just: tumbler homedoc
};
```

And `type2dbottomcruminfo` [wisp.h:107-109]:

```c
typedef struct struct2dbottomcruminfo {
    tumbler homedoc;
} type2dbottomcruminfo;
```

**The POOM bottom crum stores a raw I-address (a tumbler), nothing more.** There is no pointer into the granfilade, no reference count, no epoch number, no validity bit.

The I-address placed into TARGET's crum is the same I-address that SOURCE's POOM references. They share the same I-address by value — two independent POOM trees, each containing a crum that encodes the same I-tumbler range.

---

### Step 2: How DELETE Operates — and What It Doesn't Touch

`dodeletevspan()` [do1.c:158-167]:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr) {
    return (
       findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm(taskptr, docisaptr, docorgl, vspanptr)
    );
}
```

`deletevspanpm()` [orglinks.c:145-152]:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr) {
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`docorgl` is SOURCE's own POOM, obtained from `findorgl(... docisaptr ...)`. DELETE operates exclusively on **SOURCE's POOM** in the V-dimension.

`deletend()` [edit.c:31-76] places two knife cuts at the V-span boundaries, then for each child crum in the deletion zone:

```c
case 1:  // crum fully inside deletion zone
    disown((typecorecrum*)ptr);
    subtreefree((typecorecrum*)ptr);  // ← frees the POOM tree node
    break;
case 2:  // crum is to the right; shift it left
    tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    break;
```

**`subtreefree()` frees the POOM crum node in memory. It does not touch the granfilade.** The granfilade entry at the I-address stored in the freed crum continues to exist unchanged.

There is no call to any granfilade deletion function. Searching the entire source tree confirms there is no `deletegr` or equivalent. The granfilade is purely append-only by design.

---

### Step 3: How the Target Resolves I→Content After the Delete

When TARGET's content is retrieved, the path is:

`doretrievev()` [do1.c:338-346] → `specset2ispanset()` + `ispanset2vstuffset()` [granf1.c:57-74] → `ispan2vstuffset()` [granf2.c:286-318]:

```c
typevstuffset *ispan2vstuffset(typetask *taskptr, typegranf fullcrumptr, typeispan *ispanptr, ...) {
    movetumbler(&ispanptr->stream, &lowerbound);
    tumbleradd(&lowerbound, &ispanptr->width, &upperbound);
    context = retrieveinspan((typecuc*)fullcrumptr, &lowerbound, &upperbound, WIDTH);
    for (temp = context; temp; temp = temp->nextcontext) {
        if (context2vstuff(taskptr, temp, ispanptr, &vstuffset)) {
            *vstuffsetptr = vstuffset;
            ...
        }
    }
}
```

`retrieveinspan()` [retrie.c:112-136] walks the **granfilade** — the global, append-only store — looking for `GRANTEXT` crums whose `WIDTH` range intersects the requested I-span. Since granfilade crums are **never deleted**, and the I-address placed into TARGET's POOM by COPY points to granfilade entries that persist forever, TARGET's retrieval succeeds identically before and after SOURCE's delete.

---

### Step 4: The `homedoc` Field — Is It a Liveness Check?

The only document-identity field in a POOM crum is `c2dinfo.homedoc`. It's checked in `crumqualifies2d()` [retrie.c:270-279]:

```c
if ((crumptr->height == 0) && infoptr && !tumblereq(&infoptr->homedoc, &(((type2dcbc*)crumptr)->c2dinfo.homedoc))) {
    return (FALSE);
}
```

This check triggers only when `infoptr != NULL`. The caller `retrieverestricted()` [retrie.c:77-84] passes `infoptr = NULL` unless `docisaptr` is non-null. And the call site `span2spanset()` [orglinks.c:435] passes `(typeisa*)NULL` for `docisaptr`:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);
```

Furthermore, `findcbcinarea2d()` [retrie.c:244-251] has a DISTRIBUTION guard that calls `gerror()` if `infoptr` is ever non-null:

```c
if (infoptr)
    gerror("!NULL");
```

**The `homedoc` filter is dead code in all normal retrieval paths.** It was apparently intended for a future home-document restriction feature that was never activated.

---

### Conclusion

| Property | Finding | Evidence |
|----------|---------|----------|
| Reference counting | **None** | No refcount field in `type2dbottomcruminfo` [wisp.h:107] or `typegranbottomcruminfo` [wisp.h:100] |
| Granfilade deletion | **Never happens** | `deletend()` [edit.c:31] only modifies the POOM tree; no granfilade delete function exists |
| Cross-document POOM invalidation | **None** | `dodeletevspan()` [do1.c:158] fetches *source's* `docorgl` only; TARGET's POOM is not accessed |
| Liveness bit or epoch | **None** | `type2dcbc.c2dinfo` contains only `homedoc` [wisp.h:107] |
| `homedoc` as liveness check | **Inert** | Passed as NULL in all retrieval call sites [orglinks.c:435]; `gerror()` fired if non-null [retrie.c:249] |
| I-address persistence | **Permanent** | Granfilade is append-only; I-addresses are eternal permascroll positions |

After SOURCE deletes its content:
- SOURCE's POOM loses the V→I crum nodes for those V-addresses [`deletend()`, edit.c:59]
- TARGET's POOM retains its own crum nodes with the same I-addresses — untouched
- The granfilade entries at those I-addresses remain valid and retrievable
- TARGET's RETRIEVE resolves I→content identically, before and after the delete

This is the Xanadu permascroll invariant expressed in code: **content insertion is permanent; document deletion removes only the document's view of that content.** The design has no mechanism to violate it, because there is no mechanism connecting the two documents' POOM trees after the copy completes.
