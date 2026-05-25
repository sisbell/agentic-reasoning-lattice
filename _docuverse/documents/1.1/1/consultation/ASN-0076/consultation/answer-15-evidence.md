## Question 15 [evidence]

> Does the link orgl structure include a type field separate from the type endset, that could distinguish an "original" link from a "revision-of" link?

## KB Synthesis

Not fully answerable from the KB — but the relevant structure is documented.

## Link Orgl Structure

The KB describes link orgls as having exactly **three endset positions**, accessed at positions 0.1, 0.2, and 0.3 via `retrieverestricted()` [SS-FOLLOWLINK, Finding 0048]:

- **0.1** — FROM (source endpoint)
- **0.2** — TO (target endpoint)  
- **0.3** — THREE (type endpoint)

The "type" is **not** a separate metadata field — it IS the third endset. It points to a VSpec in the bootstrap document's type registry at `1.0.2.x` [SS-LINK-ENDPOINT, Finding 0024]:

| Type | Address |
|------|---------|
| JUMP | `1.0.2.2` |
| QUOTE | `1.0.2.3` |
| FOOTNOTE | `1.0.2.6` |
| MARGIN | `1.0.2.6.2` |

Internally, `setlinkvsas()` constructs these three subspace positions as `1.x`, `2.x`, and `3.x` in the document's V-stream [SS-DUAL-ENFILADE, Finding 0038]. No fourth field or separate metadata slot is described anywhere in the KB.

## On "Revision-Of" Links

The KB documents no such type in the registry, and no structural field in the link orgl beyond the three endsets. If a "revision-of" relationship needed to be expressed, the mechanism would be to register it in the bootstrap document type hierarchy (the tumbler containment in `1.0.2.*` allows subtype relationships) and point the THREE endset there — but this is not documented as existing.

**Bottom line:** The link orgl has no type field separate from the THREE endset. Whether a "revision-of" entry exists in the type registry is not answerable from the KB.

---

## Code Exploration

Now I have everything I need to answer the question precisely.

---

## Does the link orgl structure include a type field separate from the type endset?

**No.** The link orgl structure has no type field of any kind — neither a separate "link kind" field nor anything that would distinguish an "original" link from a "revision-of" link. Here is what the code actually contains, layer by layer.

---

### Layer 1: The granfilade bottom crum (`typegranbottomcruminfo`)

`wisp.h:100-104`:
```c
typedef struct structgranbottomcruminfo {
    typegranstuff granstuff;
    INT infotype;
} typegranbottomcruminfo;
```

`wisp.h:68-71`:
```c
#define GRANNULL             0
#define GRANTEXT             1
#define GRANORGL             2
```

The `infotype` field distinguishes text crums from orgl crums — it is always `GRANORGL` (2) for a link. There is no finer-grained type. The struct `typegranorgl` inside `granstuff.orglstuff` (`wisp.h:88-92`) has only `orglptr`, `diskorglptr`, and `orglincore` (a memory-management flag). No link-kind field.

When `createorglgr` creates a link orgl (`granf2.c:111-128`), it sets exactly:
```c
locinfo.infotype = GRANORGL;              // granf2.c:119
locinfo.granstuff.orglstuff.orglptr = createenf(POOM);  // granf2.c:120
locinfo.granstuff.orglstuff.orglincore = TRUE;           // granf2.c:122
locinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = DISKPTRNULL; // granf2.c:123
```

Nothing more. No type tag.

---

### Layer 2: The orgl itself — a POOM enfilade

The orgl is a POOM (permutation matrix) enfilade (`typeorgl` is `INT *`, effectively `typecuc *` — `xanadu.h:17`). Its bottom crums are `type2dcbc` (`enf.h:109-131`), and their payload is:

`wisp.h:107-110`:
```c
typedef struct struct2dbottomcruminfo {
    tumbler homedoc;
} type2dbottomcruminfo;
```

One field: `homedoc`. No link type. No kind flag.

---

### Layer 3: What is stored inside the link orgl's POOM

`insertendsetsinorgl` (`do2.c:130-148`) calls `insertpm` three times — for `fromsporglset`, `tosporglset`, and optionally `threesporglset`. The V-addresses used are set by `setlinkvsas` (`do2.c:169-183`):

```c
fromvsa  = 1.1     // tumblerincrement to dimension 0=1, dimension 1=1
tovsa    = 2.1     // tumblerincrement to dimension 0=2, dimension 1=1
threevsa = 3.1     // tumblerincrement to dimension 0=3, dimension 1=1
```

The V-address position (1.x vs 2.x vs 3.x) encodes the endset *role* (from/to/three), but this is purely positional. The POOM crums themselves have only `homedoc`. There is no stored "link type" field anywhere in the POOM tree.

---

### Layer 4: The typehint — creation-time only, not stored

`docreatelink` (`do1.c:195-221`) calls:
```c
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);  // do1.c:207
```

`typehint` (`xanadu.h:148-153`):
```c
typedef struct {
    INT supertype;
    INT subtype;
    INT atomtype;
    typeisa hintisa;
} typehint;
```

This is passed to `createorglingranf` → `createorglgr` → `findisatoinsertgr` (`granf2.c:130-156`) purely to compute the ISA address where the new link orgl is inserted. The hint is **not stored**; it evaporates after insertion. It affects only *where* in the granfilade the link lives, not any metadata stored in the orgl.

---

### Summary

| Location | Fields | Link type field? |
|---|---|---|
| `typegranbottomcruminfo` (`wisp.h:100-104`) | `granstuff` union + `infotype` | No — `infotype` is `GRANORGL` only |
| `typegranorgl` (`wisp.h:88-92`) | `orglptr`, `diskorglptr`, `orglincore` | No |
| `type2dbottomcruminfo` (`wisp.h:107-110`) — POOM crums | `homedoc` only | No |
| `typehint` (`xanadu.h:148-153`) | `supertype`, `subtype`, `atomtype`, `hintisa` | Not stored |

**The link orgl structure has no type field and no mechanism to distinguish an "original" link from a "revision-of" link.** The only variation encoded at creation time is the ISA address, which derives from the `typehint` supertype/subtype combination — but that controls *placement* in the tumbler hierarchy, not a retrievable type tag. Once stored, all link orgls look structurally identical: a POOM with endsets at V-positions 1.x, 2.x, and 3.x.
