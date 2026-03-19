## Question 17 [gregory]

> For CREATENEWVERSION, the new document's POOM entries point to the same I-addresses as the original — are these entries independent copies in the B-tree, so that subsequent edits to either document's POOM cannot corrupt the other's I-address mappings through shared pointers or aliased crums?

## KB Synthesis

Yes — the version's POOM is a fully independent B-tree. Here is the synthesis across the KB:

## How CREATENEWVERSION builds the version's POOM

The call chain is: `docreatenewversion` → `createorglingranf` (allocates a **new orgl**) → `doretrievedocvspanfoo` (reads source text vspan) → `docopyinternal` → `insertpm` + `insertspanf` [ST-VERSION] [ST-VERSION-CREATE].

`createorglingranf` creates a fresh root node for the version's enfilade tree. `docopyinternal` then calls `insertpm`, which is the same POOM insertion function used by regular COPY. `insertpm` → `insertnd` allocates new bottom crums in the *version's* orgl tree, establishing V→I mappings pointing at the shared I-addresses in the immutable granfilade [PRE-COPY].

**What is shared:** The I-addresses themselves — entries in the granfilade, which is append-only and immutable [INV-IADDR-IMMUTABILITY]. The version and original point to the same bytes in I-space, but through independent POOM trees.

**What is not shared:** The POOM crum nodes. Each document has its own orgl (root pointer), and `insertpm` allocates fresh crums under the version's root. There is no pointer aliasing between the original's POOM tree and the version's POOM tree.

## Why subsequent edits cannot corrupt the other document

[FC-VERSION-ISOLATION] states this explicitly: "edits to the original document modify only the original's POOM. Edits to the version modify only the version's POOM. Neither affects the other."

[ST-DELETE] (Finding 0064) provides the strongest confirmation: `deletevspanpm` calls `deletend` on a single document's orgl, and "other documents that reference the same I-addresses through transclusion are completely unaffected — their POOM mappings remain intact." The POOM is scoped strictly to one orgl.

[SS-POOM-MUTABILITY] confirms the POOM is mutated in-place with no copy-on-write semantics. This design is only safe *because* each document has an independent tree — if crums were shared, in-place mutation would corrupt the other document immediately.

## The one nuance

All crums (original and version) share the same unified disk file and grim reaper cache [SS-UNIFIED-STORAGE] [SS-CACHE-MECHANISM]. This means memory pressure from operating on one document's POOM can evict modified crums from the other to disk. This affects **durability ordering** but not **correctness** — each crum belongs to exactly one orgl, and eviction does not change what V-address maps to what I-address [EC-CROSS-ENFILADE-EVICTION].

**Summary:** The version receives new POOM crum nodes under a new orgl root; only I-addresses (granfilade content) are shared. Edits to either document's POOM are fully isolated — they operate on structurally separate B-trees that happen to leaf into the same immutable I-address space.

---

## Code Exploration

I now have all the information needed to give a complete, cited answer.

---

## Answer: POOM Entries After CREATENEWVERSION Are Fully Independent Copies

**Yes — the new document's POOM crum nodes are independent, freshly allocated structures. No shared pointers or aliased crums exist between the original and the new document's POOM trees.**

Here is the complete traced path, with every claim cited.

---

### 1. Entry Point

**`fns.c:289-300`** — `createnewversion()` calls:
```c
docreatenewversion(taskptr, &originaldocisa, &originaldocisa, &newdocisa)
```

---

### 2. `docreatenewversion` — New POOM Created From Scratch

**`do1.c:260-299`** — Three key steps:

**Step A — allocate an empty POOM for the new document:**
```c
// do1.c:277
if (!createorglingranf(taskptr, granf, &hint, newisaptr))
    return (FALSE);
```
This calls `createorglgr` in **`granf2.c:111-128`**:
```c
locinfo.granstuff.orglstuff.orglptr = createenf(POOM);   // granf2.c:120
```
`createenf(POOM)` (in **`credel.c:492-516`**) allocates a brand-new, empty POOM enfilade — a `typecuc` apex node with one empty bottom `type2dcbc`, no children sharing anything with the original document's POOM. This POOM is stored in the granfilade indexed by the *new* document's ISA. Completely separate from the original's.

**Step B — retrieve original document's V-span:**
```c
// do1.c:281-288
doretrievedocvspanfoo(taskptr, isaptr, &vspan);
vspec.docisa = *isaptr;        // the *original* doc's ISA
vspec.vspanset = &vspan;
```
This constructs a `vspec` whose `docisa` names the original document.

**Step C — populate the new POOM by copying:**
```c
// do1.c:293
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
```

---

### 3. `docopyinternal` → `insertpm`

**`do1.c:66-82`** — `docopyinternal` fetches the *new* document's freshly-created POOM orgl and calls:
```c
// do1.c:78
insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)
```
where `docorgl` is the new document's empty POOM.

**`orglinks.c:75-134`** — `insertpm` iterates over the I-span set from the original document. For each span it calls `unpacksporgl`:
```c
// orglinks.c:101
unpacksporgl(sporglset, &lstream, &lwidth, &linfo);
```

**`sporgl.c:178-203`** — `unpacksporgl` extracts data using `movetumbler` calls:
```c
movetumbler(&((typesporgl *)sporglptr)->sporglorigin, streamptr);   // sporgl.c:185
movetumbler(&((typesporgl *)sporglptr)->sporglwidth, widthptr);     // sporgl.c:186
movetumbler(&((typesporgl *)sporglptr)->sporgladdress, &infoptr->homedoc); // sporgl.c:187
```

**`movetumbler` is defined in `common.h:73` as:**
```c
#define movetumbler(A,B) (*((tumbler *)(B)) = *((tumbler *)(A)))
```
This is a C struct assignment — a **by-value copy** of the entire `tumbler` struct (a fixed-size integer array with no internal pointers). No aliasing is possible.

Then `insertpm` calls:
```c
// orglinks.c:130
insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
```
The I-address data (`lstream`, `lwidth`, `linfo.homedoc`) are all local variables on `insertpm`'s stack, copied from the sporgl by value above.

---

### 4. `insertnd` → `insertcbcnd` — Fresh Crum Allocation

**`insertnd.c:15-111`** — For POOM, `insertnd` calls `makegappm` then `doinsertnd`, which eventually calls `insertcbcnd`.

**`insertnd.c:242-275`** — `insertcbcnd` creates a brand-new crum:
```c
// insertnd.c:260
new = createcrum(0, (INT)father->cenftype);
// ...
// insertnd.c:267
move2dinfo(infoptr, &((type2dcbc *)new)->c2dinfo);
```

**`wisp.h:110`** — `move2dinfo` is:
```c
#define move2dinfo(A,B) movmem((A),(B),sizeof(type2dbottomcruminfo))
```
And `movmem` is `memmove` (`common.h:163`). The struct being copied is:
```c
// wisp.h:107-109
typedef struct struct2dbottomcruminfo {
    tumbler homedoc;
} type2dbottomcruminfo;
```
`homedoc` is a plain `tumbler` value with no internal pointers. The whole thing is blitted by value into the new crum's private storage.

Similarly for span/width:
```c
// insertnd.c:263
dspsub(origin, grasp, &new->cdsp, father->cenftype);
// insertnd.c:266
movewisp(width, &new->cwid);
```
`movewisp` is `memmove(B, A, sizeof(typewisp))` — again, by-value copy into the new crum's own fields.

---

### 5. `createcrum` — Fresh Memory Allocation Every Time

**`credel.c:518-596`** — `createcrum(0, POOM)` → `createcruminternal`:
```c
// credel.c:568
ptr = (typecorecrum *)eallocwithtag(crumsize, CBCTAG);
// credel.c:572-591: all fields zeroed/initialized fresh
ptr->height = crumheight;
ptr->isapex = FALSE;
ptr->modified = TRUE;
ptr->age = NEW;
ptr->leftbroorfather = NULL;
ptr->rightbro = NULL;
clear(&ptr->cdsp, sizeof(ptr->cdsp));
clear(&ptr->cwid, sizeof(ptr->cwid));
clear(&((type2dcbc *)ptr)->c2dinfo, sizeof(...));
```
Each call returns a **uniquely heap-allocated** block. There is no crum pooling, recycling, or sharing between documents' POOM trees.

---

### Summary

The call chain for CREATENEWVERSION is:

```
createnewversion (fns.c:289)
  → docreatenewversion (do1.c:260)
      → createorglingranf  → createenf(POOM)      ← new empty POOM, fresh allocation
      → doretrievedocvspanfoo                      ← reads original doc's V-span
      → docopyinternal (do1.c:66)
          → insertpm (orglinks.c:75)
              → unpacksporgl                        ← movetumbler: by-value copy
              → insertnd (insertnd.c:15)
                  → insertcbcnd (insertnd.c:242)
                      → createcrum(0, POOM)         ← fresh heap allocation
                      → move2dinfo                  ← memmove: by-value copy
                      → movewisp                    ← memmove: by-value copy
```

At no point is a pointer to an original document's crum stored in the new document's POOM. Every crum in the new document's POOM is:
1. **Freshly allocated** by `createcrum` → `eallocwithtag` [`credel.c:568`]
2. **Populated by value copy** via `memmove`/struct-assignment macros [`common.h:73`, `wisp.h:58`, `wisp.h:110`]
3. **Linked only into the new document's tree** via `adopt()` [`genf.c:419`], which sets only sibling/parent pointer fields in the new crums — no cross-document pointers

The I-addresses (stream, width, homedoc) encoded in the new POOM's bottom crums are identical *values* to those in the original's POOM, but they live in wholly independent crum objects. Subsequent edits to either document's POOM — insertions, deletions, splits, recombinations — operate entirely on that document's own crum tree. There is no mechanism by which a mutation in one document's POOM could reach or corrupt the other's crum nodes.
