## Question 14 [evidence]

> Does the link orgl structure contain any field beyond the three endsets (source, target, type) — for instance, an entry in the reserved `3.x` subspace — where a predecessor reference could be stored, or are the three endsets the entirety of a link orgl's structure?

## KB Synthesis

Based on the KB, a link orgl contains exactly three endsets and nothing more is documented.

**What the KB says about link orgl structure:**

[SS-THREE-LAYER-MODEL] states the link orgl "Contains the link's endset references (FROM, TO, TYPE)" — three fields, no others listed.

[SS-FOLLOWLINK] is the most precise: `link2sporglset()` extracts I-addresses from the link orgl "at the requested endset position (0.1, 0.2, or 0.3) via `retrieverestricted()`." The three enumerated positions are:
- `0.1` — FROM (source endpoint)
- `0.2` — TO (target endpoint)
- `0.3` — THREE (type endpoint)

No additional positions are accessed or described anywhere in the KB.

**On the `3.x` subspace specifically:**

The `3.x` V-positions mentioned in [SS-DUAL-ENFILADE / Finding 0038] are positions in the **home document's V-stream**, not inside the link orgl itself. `setlinkvsas()` in `do2.c:169-183` places the link at `2.1` in the document and type endpoint references at `3.1` — these are the document's POOM entries, not the link orgl's internal structure.

[SS-RETRIEVE-ENDSETS / Finding 0035] confirms the three ORGLRANGE subspaces used for spanfilade indexing: `LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3` — which align exactly with the three orgl positions above.

**Conclusion:**

The KB documents only three fields in a link orgl (FROM/TO/THREE at positions 0.1, 0.2, 0.3). No predecessor reference, history field, or `3.x`-subspace-internal field appears anywhere in the KB. Whether the implementation contains unreported fields cannot be answered from the KB; the KB is silent on anything beyond the three endsets.

---

## Code Exploration

I now have a complete picture of the link orgl structure from the code. Here is the full answer.

---

## Answer: The Three Endsets Are the Entirety of a Link Orgl's Structure

No predecessor reference, no fourth field, no reserved subspace beyond `3.x` is stored in the link orgl. The code is unambiguous at every layer.

---

### 1. What a link orgl is

`typeorgl` is defined as `INT *` (`xanadu.h:17`) — a raw pointer to a POOM enfilade (a 2D permutation matrix tree). The granfilade stores a leaf record of type `typegranorgl` (`wisp.h:88-92`) at the link's ISA address:

```c
typedef struct structgranorgl {
    struct structcuc *orglptr;       // pointer to the in-core POOM
    typediskloafptr diskorglptr;     // disk location
    bool orglincore;                 // cache flag
} typegranorgl;
```

This struct has **no predecessor tumbler, no version field, no fourth-endset pointer**. It is purely a caching handle for the POOM.

---

### 2. Creation: an empty POOM

`createorglgr` (`granf2.c:111-128`) creates the link orgl:

```c
locinfo.granstuff.orglstuff.orglptr = createenf (POOM);   // granf2.c:120
locinfo.granstuff.orglstuff.orglincore = TRUE;
locinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = DISKPTRNULL;
insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);
```

It is a freshly allocated, empty POOM enfilade. Nothing else is set.

---

### 3. Population: exactly three endsets, at fixed V-addresses

The entire link call chain in `docreatelink` (`do1.c:195-221`) populates the orgl through exactly one function: `insertendsetsinorgl` (`do2.c:130-149`):

```c
bool insertendsetsinorgl(..., tumbler *fromvsa, ..., tumbler *tovsa, ..., tumbler *threevsa, ...)
{
    if (!( insertpm(taskptr, linkisaptr, link, fromvsa, fromsporglset)
        && insertpm(taskptr, linkisaptr, link, tovsa,   tosporglset))) {
            return (FALSE);
    }
    if (threevsa && threesporglset) {
        if (!insertpm(taskptr, linkisaptr, link, threevsa, threesporglset)){
            return (FALSE);
        }
    }
    return (TRUE);
}
```

Three `insertpm` calls and no others. No additional data is ever inserted into the link's POOM.

---

### 4. The V-addresses where endsets live

`setlinkvsas` (`do2.c:169-183`) computes the three V-addresses:

```c
tumblerclear(fromvsaptr);
tumblerincrement(fromvsaptr, 0, 1, fromvsaptr);   // mantissa[0]=1 → tumbler 1
tumblerincrement(fromvsaptr, 1, 1, fromvsaptr);   // mantissa[1]=1 → tumbler 1.1

tumblerclear(tovsaptr);
tumblerincrement(tovsaptr, 0, 2, tovsaptr);       // mantissa[0]=2 → tumbler 2
tumblerincrement(tovsaptr, 1, 1, tovsaptr);       // mantissa[1]=1 → tumbler 2.1

if (threevsaptr) {
    tumblerclear(threevsaptr);
    tumblerincrement(threevsaptr, 0, 3, threevsaptr);  // → tumbler 3
    tumblerincrement(threevsaptr, 1, 1, threevsaptr);  // → tumbler 3.1
}
```

Per `tumblerincrement` (`tumble.c:599-623`): starting from zero, the first call places `bint` at `mantissa[0]`; the second adds `1` at `mantissa[idx + rightshift]` where `idx=0`, so `mantissa[1]`. Result:

| Endset | V-address (mantissa) | Meaning |
|--------|---------------------|---------|
| from/source | `1.1` | `LINKFROMSPAN = 1` |
| to/target | `2.1` | `LINKTOSPAN = 2` |
| three/type | `3.1` | `LINKTHREESPAN = 3` |

There is **no V=0.x write** into a link orgl, and **no V≥4.x write** anywhere in the codebase.

---

### 5. Retrieval confirms only three endsets exist

`link2sporglset` (`sporgl.c:67-95`) retrieves endset data:

```c
tumblerincrement (&zero, 0, whichend, &vspan.stream);   // sporgl.c:81
tumblerincrement (&zero, 0, 1, &vspan.width);
```

`whichend` is validated at the FEBE protocol layer (`get1.c:71`):

```c
&& (*whichendptr == 1 || *whichendptr == 2 || *whichendptr == 3))
```

The validation explicitly rejects any value outside `{1, 2, 3}`. No fourth endset is defined or retrievable.

---

### 6. Nothing in the POOM node structure either

The POOM upper-crum struct `typecuc` (`enf.h:54-82`) contains standard enfilade tree fields (`isapex`, `height`, `cwid`, `cdsp`, `leftbroorfather`, `rightbro`, `leftson`, etc.) and no dedicated predecessor or version-link field. The content of the POOM is entirely what `insertpm` has placed in V-space.

---

### Conclusion

The link orgl is a POOM enfilade that contains **exactly the three endsets and nothing else**:

- **V = 1.x** — from/source endset  
- **V = 2.x** — to/target endset  
- **V = 3.x** — three/type endset (omitted if `threespecset` is NULL)

V = 0.x is unused in a link orgl (it is text-content space in a *document* orgl, a different thing). V ≥ 4.x is neither written nor readable. The `3.x` subspace is not "reserved" — it is actively used as the third endset. There is no slot anywhere in the granfilade leaf (`typegranorgl`), the POOM node (`typecuc`), or the disk format (`typediskloafhedr`) for a predecessor reference. The three endsets are the complete and total content of a link orgl.
