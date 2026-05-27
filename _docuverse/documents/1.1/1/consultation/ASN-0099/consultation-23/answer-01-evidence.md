## Question 1 [evidence]

> Does the udanax-green implementation contain any code path — present or historically — where content-extension (K.μ⁺ analogue), content-contraction (K.μ⁻ analogue), or provenance-recording (K.ρ analogue) routines could write to the LINKFROMSPAN/LINKTOSPAN/LINKTHREESPAN regions of the spanfilade, even via indirect calls or shared helpers?

## KB Synthesis

## Answer

**No. No content-extension, content-contraction, or provenance-recording routine can write to the LINKFROMSPAN/LINKTOSPAN/LINKTHREESPAN regions of the spanfilade — directly, historically, or via shared helpers.**

---

### The Write Paths into the Spanfilade

The spanfilade has two distinct write functions and four named region constants:

- `insertspanf(..., DOCISPAN)` — type 4, the document-content index. Called by `docopy()` during every INSERT and COPY. [SS-DOCISPAN]
- `insertendsetsinspanf()` — internally calls `insertspanf` with LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3. Called exclusively by `docreatelink()`. [ST-CREATE-LINK], [INT-SPORGL-LINK-INDEX]

These two write paths share `insertspanf()` as a helper, but the **type constant is the discriminator**. Neither INSERT, COPY, DELETE, nor REARRANGE ever passes a LINK* constant.

---

### Content-Extension (INSERT/COPY)

`doinsert()` → `docopy()` → `insertspanf(taskptr, spanf, docisaptr, ispanset, **DOCISPAN**)`.

The DOCISPAN constant is hardcoded at `do1.c:62`. The LINK* constants are never passed. This is confirmed in [FC-CONTENT-SPANF-ISOLATION] and [SS-DOCISPAN] (Finding 0036): "INSERT writes to both granf (new content) and spanf (DOCISPAN index)... content operations do not affect the *link index* portion of spanf."

`doappend()` has the `insertspanf` call commented out entirely — it writes to neither DOCISPAN nor LINK* regions. [EC-APPEND-NO-DOCISPAN]

---

### Content-Contraction (DELETE/REARRANGE)

DELETE (`dodeletevspan` → `deletevspanpm` → `deletend`) writes **only to the document's POOM in granf**. There is no `insertspanf` or `deletespanf` call anywhere in this path. [ST-DELETE], [INV-SPANF-WRITE-ONLY] (Finding 0057): "No `deletespanf`, `removespanf`, or any removal mechanism exists."

REARRANGE (`dorearrange` → `rearrangend`) writes only to V-address displacements in the POOM via `tumbleradd`. No spanfilade writes whatsoever. [ST-REARRANGE], [FC-GRANF-ON-DELETE]

---

### Provenance-Recording (DOCISPAN / K.ρ)

DOCISPAN writes are made by `insertspanf(..., DOCISPAN)` — type 4. The LINK* regions are types 1, 2, 3. Even though `docreatelink()` calls both `docopy()` (which writes DOCISPAN) and `insertendsetsinspanf()` (which writes LINK*), those are **two separate calls with separate type parameters**. [ST-CREATE-LINK] (Finding 0012): "Link creation is a compound state transition that updates both enfilades: (1) granf, (2) document's link subspace via docopy, (3) spanf link index via insertendsetsinspanf."

The provenance path (`docopy` → `insertspanf(..., DOCISPAN)`) never reaches LINK* regions because the constant is fixed at the call site in `do1.c:62`.

---

### Summary

| Operation | Spanfilade write | Region |
|-----------|-----------------|--------|
| INSERT | `insertspanf` | DOCISPAN (4) only |
| COPY | `insertspanf` | DOCISPAN (4) only |
| APPEND | none | — |
| DELETE | none | — |
| REARRANGE | none | — |
| CREATELINK | `insertendsetsinspanf` | LINKFROMSPAN/LINKTOSPAN/LINKTHREESPAN (1,2,3) |

The LINK* spanfilade regions are exclusively modified by `insertendsetsinspanf()`, which is called by one code path only: `docreatelink()`. [FC-CONTENT-SPANF-ISOLATION], [INV-DUAL-ENFILADE-CONSISTENCY]

---

## Code Exploration

I have all the evidence needed. Here is the full answer.

---

## Answer: Content/Contraction/Provenance Paths vs. LINKFROMSPAN/LINKTOSPAN/LINKTHREESPAN

**Short answer: No.** No present or historical code path in udanax-green allows content-extension, content-contraction, or provenance-recording operations to write to the LINKFROMSPAN, LINKTOSPAN, or LINKTHREESPAN regions of the spanfilade. The separation is structurally enforced at the call site, not by a runtime guard.

---

### 1. Definitions

The span type constants are declared in `backend/xanadu.h:35-39`:

```c
/* spanfilade span types */
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```

These four values are the only legal values passed as the `spantype` parameter to `insertspanf` — the single function that writes to the spanfilade. They are distinct, non-overlapping integers.

---

### 2. The Only Spanfilade Write Gate: `insertspanf`

`backend/spanf1.c:15-54`:

```c
bool insertspanf(typetask *taskptr, typespanf spanfptr, typeisa *isaptr,
                 typesporglset sporglset, INT spantype)
{
    ...
    prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
    ...
    insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
    ...
}
```

The `spantype` argument is prefixed directly into the ORGL dimension of the crumb origin at `spanf1.c:22`. There is no runtime validation against the `LINK*SPAN` values. The only protection is that callers always hardcode the constant they pass.

---

### 3. All Content-Extension Callers (K.μ⁺) Hardcode DOCISPAN

**`docopy`** (`backend/do1.c:62`):
```c
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

**`docopyinternal`** (`backend/do1.c:79`):
```c
if (!insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)) return FALSE;
```

**`doinsert`** (`backend/do1.c:87-123`): Never calls `insertspanf` directly. It calls `inserttextingranf` (to allocate content in the granfilade) and then delegates entirely to `docopy` (`do1.c:119`), which carries the hardcoded DOCISPAN.

**`doappend`** (`backend/do1.c:25-32`): The commented-out code at `do1.c:29-31` is historically significant:

```c
return (appendpm (taskptr, docptr, textset)/*&&
   appendpm includes insertspanf!   insertspanf(taskptr,spanf,docptr,textset,DOCISPAN)*/
);
```

This shows the `insertspanf` call was originally explicit with DOCISPAN at the call site and was subsequently folded into `appendpm`. There is no historical variant where append passed a link span type.

---

### 4. Content-Contraction (K.μ⁻) Does Not Write to Spanfilade at All

**`dodeletevspan`** (`backend/do1.c:158-167`):

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
    );
}
```

This function operates exclusively on the granfilade (POOM) via `deletevspanpm`. It never calls `insertspanf`, `insertendsetsinspanf`, or any other spanfilade write function. **Deletion leaves no trace in the spanfilade** — neither in DOCISPAN nor in any link span region.

---

### 5. Provenance Recording (K.ρ) — Version Creation

**`docreatenewversion`** (`backend/do1.c:260-299`) is the closest analogue to K.ρ in the codebase. It:

1. Creates a new orgl via `createorglingranf` (granf only, no spanf write)
2. Retrieves the source document's vspan via `doretrievedocvspanfoo`
3. Calls `docopyinternal` at `do1.c:293` — which writes to the spanfilade with `DOCISPAN` (hardcoded at `do1.c:79`)

No call to `insertendsetsinspanf`. No link span type reaches the spanfilade through this path.

---

### 6. The Only Functions That Write LINK*SPAN to Spanfilade

`insertendsetsinspanf` (`backend/do2.c:116-128`) is the **exclusive gateway** for link span writes:

```c
bool insertendsetsinspanf(typetask *taskptr, typespanf spanfptr, typeisa *linkisaptr,
                          typesporglset fromsporglset, typesporglset tosporglset,
                          typesporglset threesporglset)
{
    if (!(
        insertspanf(taskptr,spanfptr,linkisaptr,fromsporglset,LINKFROMSPAN)
          &&insertspanf(taskptr,spanfptr,linkisaptr,tosporglset,LINKTOSPAN)))
            return (FALSE);
    if (threesporglset) {
        if(!insertspanf(taskptr,spanfptr,linkisaptr,threesporglset,LINKTHREESPAN)){
            return (FALSE);
        }
    }
    return(TRUE);
}
```

A global grep of `insertendsetsinspanf` across all `.c` files returns exactly two call sites:

- `backend/do1.c:191` — inside `domakelink` (two-ended link creation)
- `backend/do1.c:219` — inside `docreatelink` (three-ended link creation)

Neither `domakelink` nor `docreatelink` is reachable from the content-extension, content-contraction, or provenance-recording call chains.

---

### 7. One Subtle Non-Crossing Path in `docreatelink`

`docreatelink` (`do1.c:195-221`) does call `docopy` at `do1.c:212`:

```c
&& docopy (taskptr, docisaptr, &linkvsa, ispanset)
```

This writes the **link's own ISA address** into the spanfilade with DOCISPAN — recording the link as a document-space entity. This is structurally separate from the subsequent call at `do1.c:219` that writes the endpoint metadata with LINK*SPAN types. The two writes go to different orgl-range partitions and use different ISA pointers (`docisaptr` vs. `linkisaptr`). The content-side `docopy` does not cause a link-span write; it registers the link as a DOCISPAN entry in its container document.

---

### 8. Summary Table of All `insertspanf` Call Sites

| Location | Caller function | `spantype` argument | Can reach LINK*SPAN? |
|---|---|---|---|
| `do1.c:62` | `docopy` | `DOCISPAN` (hardcoded) | No |
| `do1.c:79` | `docopyinternal` | `DOCISPAN` (hardcoded) | No |
| `do2.c:119` | `insertendsetsinspanf` | `LINKFROMSPAN` (hardcoded) | Link creation only |
| `do2.c:120` | `insertendsetsinspanf` | `LINKTOSPAN` (hardcoded) | Link creation only |
| `do2.c:123` | `insertendsetsinspanf` | `LINKTHREESPAN` (hardcoded) | Link creation only |

The complete call graph for LINK*SPAN writes is:

```
createlink (fns.c) → docreatelink (do1.c:195) → insertendsetsinspanf (do2.c:116)
                                                    → insertspanf(..., LINKFROMSPAN)  [spanf1.c:15]
                                                    → insertspanf(..., LINKTOSPAN)    [spanf1.c:15]
                                                    → insertspanf(..., LINKTHREESPAN) [spanf1.c:15, optional]

                   → domakelink (do1.c:169) → insertendsetsinspanf (do2.c:116)
                                                    → insertspanf(..., LINKFROMSPAN)
                                                    → insertspanf(..., LINKTOSPAN)
```

No content or provenance path connects to this graph.

---

**Conclusion:** The LINKFROMSPAN, LINKTOSPAN, and LINKTHREESPAN regions of the spanfilade are written only through `insertendsetsinspanf` → `insertspanf`, reachable exclusively from `domakelink` and `docreatelink`. Content extension (`doinsert`/`docopy`/`doappend`), content contraction (`dodeletevspan`), and provenance recording (`docreatenewversion`) are structurally isolated from these paths. The isolation is enforced by hardcoded constants at each call site, not by a runtime guard, and no historical code (including the commented-out `doappend` path at `do1.c:30`) shows a link-span type ever being passed from a content operation.
