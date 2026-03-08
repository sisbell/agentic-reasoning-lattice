## Question 14 [gregory]

> Is there any operation that can change which I-address a given V-position maps to WITHOUT removing and re-inserting the POOM entry — for instance, does REARRANGE modify I-displacements in-place, or does it only adjust V-displacements while leaving I-fields untouched?

## KB Synthesis

**No operation modifies I-address fields in-place. REARRANGE modifies only V-displacements, leaving I-fields untouched.**

The key evidence is in [ST-REARRANGE] (Finding 0056):

> "The operation modifies V-addresses exclusively — it calls `tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index])` which updates the displacement's V-address component. No I-addresses are touched, no content is copied, no new permascroll entries are created."

The POOM bottom crum stores V and I coordinates separately [SS-POOM-BOTTOM-CRUM]:

```
BottomCrum = {
  origin: { dsas[I]: Tumbler,  dsas[V]: Tumbler },
  width:  { dsas[I]: Tumbler,  dsas[V]: Tumbler }
}
```

REARRANGE writes to `cdsp.dsas[V]` only. The `dsas[I]` field is never modified by any displacement operation. This is reinforced by [INV-REARRANGE-IDENTITY] (Finding 0056):

> "The I-address, stored separately, is never touched."

The functional effect of changing which I-address a given V-position maps to is achieved entirely through V-field modification: after a pivot, the crum that formerly covered V[1.3, 1.4) now covers V[1.6, 1.7), so querying V=1.3 hits a different crum with a different I-origin. The observable mapping changes, but through V-shifting, not I-mutation.

To enumerate all four operation classes:

| Operation | POOM I-field | POOM V-field | Entry lifecycle |
|-----------|-------------|-------------|----------------|
| INSERT | Write-once (new entry) | Write-once (new entry) | Created |
| COPY/VCOPY | Write-once (new entry) | Write-once (new entry) | Created |
| DELETE | — | — | Removed via `disown`+`subtreefree` [ST-DELETE] |
| REARRANGE | **Untouched** | Modified in-place | Retained |

The I-address field of any POOM crum is write-once at creation time and never subsequently modified. REARRANGE is the only operation that mutates an existing entry's fields, and it restricts those mutations to the V-dimension exclusively [FC-POOM-MUTABILITY].

---

## Code Exploration

Now I have a complete picture. Let me compile the definitive answer.

---

## Answer

**REARRANGE modifies only V-displacements. I-fields are left completely untouched. No operation in the codebase can change the V→I mapping of an existing POOM entry without removing and re-inserting it.**

Here is the full evidence trail.

---

### 1. The POOM crum structure

Every crum (`typecorecrumhedr`, `typecuc`, `type2dcbc`) carries two fields:

```c
typewid cwid;   // width in each dimension
typedsp cdsp;   // displacement from parent in each dimension
```

Both are `typewid`, defined in `wisp.h:50-54` as:

```c
struct structwid {
    tumbler dsas[MAXLOXIZE];   // MAXLOXIZE = 2
};
```

The two slots are indexed by symbolic constants defined in `wisp.h:19-20`:

```c
#define I  0     // I-space (permascroll address dimension)
#define V  1     // V-space (virtual document position dimension)
```

So `cdsp.dsas[I]` is the I-displacement and `cdsp.dsas[V]` is the V-displacement, both stored per-crum, relative to the parent node's absolute position.

---

### 2. The rearrange call chain

The document-level rearrange entry point is `dorearrange` in `do1.c:34`:

```c
bool dorearrange(typetask *taskptr, typeisa *docisaptr, typecutseq *cutseqptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && rearrangepm (taskptr, docisaptr, docorgl, cutseqptr)
    );
}
```

`rearrangepm` is in `orglinks.c:137-142`:

```c
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr)
{
    rearrangend((typecuc*)docorgl, cutseqptr, V);   // [orglinks.c:139]
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

**`rearrangend` is always called with `index = V`.** This is not incidental; `ndenf.h:15` makes it a structural invariant:

```c
typedef struct structknives {
    INT nblades;
    tumbler blades[MAXCUTS];
    INT dimension;  /* always V, assigned by rearrange2d */   // [ndenf.h:15]
} typeknives;
```

---

### 3. What `rearrangend` actually modifies

`rearrangend` in `edit.c:78-160` does three things:

1. Cuts the enfilade at the given V-positions (`makecutsnd`).
2. Classifies each crum into a section (before cut 0, between cuts, after last cut) via `rearrangecutsectionnd`.
3. For crums that need to move, applies the displacement delta **only to `cdsp.dsas[index]`**:

```c
// edit.c:125
tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
ivemodified((typecorecrum*)ptr);
```

With `index = V`, this line expands to:

```
ptr->cdsp.dsas[V] += diff[i]
```

`ptr->cdsp.dsas[I]` is **never referenced** anywhere in `rearrangend` or `rearrangecutsectionnd` [`edit.c:191-204`].

---

### 4. Are there any other paths that alter I-displacements in-place?

The complete list of code that writes to `cdsp.dsas[I]` or the entire `cdsp` structure:

| Site | What it does | Does it change V→I mapping? |
|------|-------------|----------------------------|
| `insertnd.c:212` `movewisp(origin, &ptr->cdsp)` | First insertion into empty enfilade — sets both I and V | No; first insert creates the mapping |
| `insertnd.c:263` `dspsub(origin, grasp, &new->cdsp, ...)` | Creates a brand-new crum (not modifying existing) | No; establishes new mapping for new crum |
| `makeroom.c:58` `movetumbler(newdsp, &crumptr->cdsp.dsas[index])` | `expandcrumleftward`: adjusts parent dsp when insertion extends to the left | No — compensated by line 65 which shifts all children by the same `base`, preserving absolute positions |
| `makeroom.c:65` `tumbleradd(base, &ptr->cdsp.dsas[index], ...)` | Children shifted to compensate for parent shift above | No — pure relative-encoding adjustment |
| `wisp.c:211` `dspsub(&ptr->cdsp, &mindsp, &ptr->cdsp, ...)` | `setwispnd`: normalizes relative displacements after restructuring | No — subtracts `mindsp` from every child and adds it to the parent (`wisp.c:200`), so absolute addresses are preserved |
| `wisp.c:224` `movewisp(&newdsp, &father->cdsp)` | Writes the recomputed dsp back to the parent in `setwispnd` | No — same normalization invariant |
| `recombine.c:248`, `recombine.c:265` `dspsub(...)` / `dspadd(...)` on `nephew->cdsp` | Node adoption during recombine/split | No — purely restructures the tree topology; absolute addresses unchanged |

The key insight for `setwispnd` (tree normalization, `wisp.c:171`): the routine subtracts `mindsp` from every child and adds `mindsp` to the father's absolute displacement (line 200: `dspadd(&father->cdsp, &mindsp, &newdsp, ...)`). This is a rigid body translation of the representation: **every existing crum's absolute position = sum of ancestor displacements is preserved in both I and V dimensions simultaneously.**

---

### 5. Definitive conclusion

> **REARRANGE modifies only V-displacements (by design and by code), leaving I-fields (`cdsp.dsas[I]`) completely untouched in all crums it touches.**

There is no operation in the codebase — not rearrange, not setwispnd, not recombine, not expandcrumleftward — that changes the absolute V→I mapping of an existing POOM entry without a destroy-and-recreate cycle. The I-address a given V-position maps to can only change by:

1. **Delete** (`deletend`/`deletevspanpm`): removes the crum entirely.
2. **Insert** (`insertnd`/`insertcbcnd`): creates a new crum with both `cdsp.dsas[I]` and `cdsp.dsas[V]` set from scratch (via `dspsub` at `insertnd.c:263` or `movewisp` at `insertnd.c:212`).

The asymmetry is architectural: V-space is the "editable" dimension (content can be moved around in document space), while I-space represents the permanent provenance record (permascroll addresses are immutable once assigned). REARRANGE is implemented to honor exactly this distinction.
