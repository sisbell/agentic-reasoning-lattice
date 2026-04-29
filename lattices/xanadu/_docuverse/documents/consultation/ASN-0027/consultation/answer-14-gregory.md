## Question 14 [gregory]

> When COPY creates a new V→I mapping in the target document, does the target's POOM entry store an independent copy of the I-displacement, or does it share a pointer with the source — i.e., could any mutation of the source POOM corrupt the target's I-address reference?

## KB Synthesis

The target's POOM entry stores an independent copy of the I-displacement. There is no shared pointer.

**Structural evidence:**

The POOM bottom crum type holds its own displacement and width as value fields — `cdsp.dsas[I]` and `cdsp.dsas[V]` — embedded directly in the struct, not as pointers to external data [SS-POOM-BOTTOM-CRUM]. When `insertnd` creates a new crum (the non-extension path at `insertnd.c:252-260`), it allocates a fresh crum and copies the I-address and V-address values into it [ST-VCOPY Finding 0046].

**Behavioral evidence:**

[FC-VERSION-ISOLATION] is the clearest empirical proof: after `CREATENEWVERSION`, edits to the original's POOM do not affect the version's POOM and vice versa. If the two POOMs shared pointer-level I-address references, in-place operations like `tumbleradd` on `ptr->cdsp.dsas[V]` during DELETE or REARRANGE would corrupt both. They don't.

Similarly, [SS-POOM-MUTABILITY] states there are no copy-on-write semantics — each POOM is a distinct mutable tree, which is only coherent if the displacement values are owned by each crum independently.

**DELETE confirms value semantics:**

[ST-DELETE Finding 0053/0055] shows `deletend` applies `tumblersub(&ptr->cdsp.dsas[index], width, ...)` — arithmetic directly on the crum's own displacement field. If displacements were shared references, deleting from one document would silently shift crums in all documents that copied from it. This is explicitly ruled out by [FC-DELETE-CROSS-DOC]: DELETE in document D has zero effect on any other document's POOM mappings.

**Bottom line:**

The I-displacement in the target POOM crum is a copied value, fully owned by the new crum struct. Source POOM mutations cannot corrupt target I-address references. The sharing happens at the I-address *value* level (both POOMs independently record the same tumbler coordinate), not at a memory pointer level.

---

## Code Exploration

I now have all the evidence needed. Here is the complete answer.

---

## COPY and POOM I-Address Storage: Independent Value Copies, No Pointer Sharing

### Call chain through COPY

`docopy` [do1.c:45–65] orchestrates two operations:

```c
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)   // do1.c:60
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)  // do1.c:62
```

`insertpm` in `orglinks.c:75–134` is where the new V→I mapping is built and written into the target's POOM tree. Every value transition in this path uses value-copy semantics.

---

### `insertpm`: Stack-local intermediates, no source references retained

```c
// orglinks.c:100–131
for (; sporglset; sporglset = ...) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);    // → local tumblers
    movetumbler (&lstream, &crumorigin.dsas[I]);             // orglinks.c:105
    movetumbler (&lwidth,  &crumwidth.dsas[I]);              // orglinks.c:109
    movetumbler (vsaptr,   &crumorigin.dsas[V]);             // orglinks.c:113
    ...
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // orglinks.c:130
}
```

`lstream`, `lwidth`, `linfo`, `crumorigin`, `crumwidth` are all **stack-local** to `insertpm`. `unpacksporgl` [sporgl.c:178–203] itself uses `movetumbler` to extract the I-address from the sporgl into those locals:

```c
// sporgl.c:185–187
movetumbler (&((typesporgl*)sporglptr)->sporglorigin, streamptr);
movetumbler (&((typesporgl*)sporglptr)->sporglwidth,  widthptr);
movetumbler (&((typesporgl*)sporglptr)->sporgladdress, &infoptr->homedoc);
```

Once `insertnd` is called, the source sporgl is no longer referenced.

---

### `insertcbcnd`: New crum allocated, all fields deep-copied

The insertion bottoms out in `insertcbcnd` [insertnd.c:242–275]:

```c
new = createcrum (0, (INT)father->cenftype);   // insertnd.c:260 — fresh heap allocation
reserve (new);
adopt (new, SON, (typecorecrum*)father);
dspsub  (origin, grasp, &new->cdsp, ...);      // insertnd.c:263 — computed, stored by value
movewisp(width,          &new->cwid);           // insertnd.c:266 — memmove deep copy
move2dinfo(infoptr, &((type2dcbc *)new)->c2dinfo);  // insertnd.c:267 — memmove deep copy
```

The displacement field `cdsp` is written by `dspsub` [wisp.c:21–24], which calls `locksubtract` — it computes a result and writes it directly into `new->cdsp`. The width field is written by `movewisp` and the home-doc info by `move2dinfo`.

---

### Copy primitive definitions — all value semantics

| Primitive | Definition | Semantics |
|---|---|---|
| `movetumbler(A,B)` | `(*((tumbler*)(B)) = *((tumbler*)(A)))` [common.h:73] | C struct assignment — copies all bytes of the tumbler by value |
| `movewisp(A,B)` | `memmove(B, A, sizeof(typewisp))` [wisp.h:58] | Byte-for-byte deep copy of the entire wisp |
| `move2dinfo(A,B)` | `memmove(B, A, sizeof(type2dbottomcruminfo))` [wisp.h:110] | Byte-for-byte deep copy |
| `dspsub(a,b,c,t)` | `locksubtract(a->dsas, b->dsas, c->dsas, dspsize(t))` [wisp.c:23] | Arithmetic result written to destination |

---

### The `xvartumbler` pointer field: dead code, always NULL

The `tumbler` struct does contain one pointer field [common.h:59–65]:

```c
typedef struct structtumbler {
    humber xvartumbler;      // unsigned char * — a pointer
    char varandnotfixed;
    char sign;
    short exp;
    tdigit mantissa[NPLACES];
} tumbler;
```

`movetumbler`'s struct assignment would shallow-copy this pointer. This would be a shared-pointer aliasing risk **if** `xvartumbler` were ever non-NULL in the COPY path. It isn't:

- Every arithmetic function that produces a new tumbler value sets `xvartumbler = 0` explicitly [tumble.c:456–457]
- `tumblerclear` is `clear(ptr, sizeof(tumbler))` — zeros all bytes including the pointer
- `corediskin.c` (disk deserialization) never sets `xvartumbler`
- The only reference to it as a non-null value is in `tumbleari.c:319`, marked with comment `/* ZZZ ECH 8-26-88 */` — an unfinished 1988 experiment behind no active code path

All tumblers entering the INSERT path through `specset2ispanset` → `insertpm` carry `xvartumbler == 0`. The struct copy propagates NULL, not a shared heap reference.

---

### Conclusion

**The target POOM crum stores a fully independent, value-copied I-address. No pointer is shared with the source.**

The sequence is: sporgl's I-address → `movetumbler` into stack locals → `movetumbler` into `crumorigin`/`crumwidth` → `movewisp`/`dspsub`/`move2dinfo` into freshly allocated crum node. Every transition is a complete byte-for-byte value copy. After `insertpm` returns, the new POOM crum is entirely self-contained. No mutation of the source document's POOM, its sporgl list, or any intermediate structure can reach or corrupt the target crum's `cdsp`/`cwid`/`c2dinfo` fields.
