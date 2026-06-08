## Question 2 [evidence]

> Does udanax-green ever construct or store link values with more than three endsets, and does it assign any meaning to slots past the third?

## KB Synthesis

Based on the KB, udanax-green constructs and stores exactly **three** endsets per link, with no fourth slot and no meaning assigned past the third.

**The three-slot structure is consistent across every layer:**

- **V-subspace**: `setlinkvsas()` hardcodes three subspace positions with mantissa[0] values 1 (FROM), 2 (TO), and 3 (TYPE). No fourth position is constructed. [SS-SUBSPACE-CONVENTION / Finding 0038]

- **FOLLOWLINK access path**: `link2sporglset()` accepts endset positions `0.1`, `0.2`, or `0.3` only. The KB records no handling beyond `0.3`. [SS-FOLLOWLINK / Finding 0048]

- **Spanfilade indexing**: `insertendsetsinspanf()` receives sporglsets for each endpoint type tagged with `LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3`. The ORGLRANGE constants stop at 3. [SS-RETRIEVE-ENDSETS / Finding 0035, INT-SPORGL-LINK-INDEX / Finding 0013]

- **RETRIEVEENDSETS (opcode 28)**: Returns exactly three specsets simultaneously — from, to, and three. The three-endset is described as conditionally retrieved ("only if requested"), but there is no fourth. [SS-RETRIEVE-ENDSETS]

- **FINDLINKSFROMTOTHREE / FINDNUMOFLINKSFROMTOTHREE**: Both operations take from/to/three parameters — the naming convention itself reflects the three-slot limit. [SS-FIND-LINKS / Finding 0035]

The "three" endpoint (often called `type` or `three`) references a type registry in the bootstrap document at `1.0.2.x` [SS-LINK-ENDPOINT / Finding 0024]. It is semantically the link's type classification, not a free-form third endpoint.

**Nothing in the KB documents a fourth slot, a fourth ORGLRANGE constant, a fourth access position, or any design intent for additional endsets.**

---

## Code Exploration

---

## Does udanax-green ever construct or store links with more than three endsets?

**No.** The codebase enforces a hard ceiling of three endsets at every level — type constants, function signatures, input validation, and storage. Here is the complete trace.

---

### 1. The only defined endset constants

`backend/xanadu.h:36-39`:

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```

There is no `LINKFOURSPAN` or any higher constant. `DOCISPAN` (4) is **not a link endset** — it is a distinct stream slot used in the spanfilade to record which documents *contain* a given piece of content (see `backend/spanf1.c:168`). It occupies a parallel structural position in the spanfilade but belongs to a completely different semantic domain: document containment, not link endsets.

---

### 2. Two link-creation functions — both capped at three

**`domakelink()`** (`do1.c:169`) creates a two-endset link. The third parameter to every downstream call is `NULL`:

```c
// do1.c:190-191
&& insertendsetsinorgl(taskptr, linkisaptr, link,
    &fromvsa, fromsporglset, &tovsa, tosporglset, NULL, NULL)
&& insertendsetsinspanf(taskptr, spanf, linkisaptr,
    fromsporglset, tosporglset, NULL)
```

**`docreatelink()`** (`do1.c:195`) creates a three-endset link. Its signature accepts exactly three `typespecset` arguments — `fromspecset`, `tospecset`, `threespecset` — and passes all three downstream:

```c
// do1.c:218-219
&& insertendsetsinorgl(taskptr, linkisaptr, link,
    &fromvsa, fromsporglset, &tovsa, tosporglset, &threevsa, threesporglset)
&& insertendsetsinspanf(taskptr, spanf, linkisaptr,
    fromsporglset, tosporglset, threesporglset)
```

There is no function that accepts a fourth endset. The C function signatures enforce the limit at compile time.

---

### 3. Storage functions: the third endset is conditional, the fourth does not exist

**`insertendsetsinspanf()`** (`do2.c:116-128`) writes endsets into the spanfilade. It takes three sporglset parameters and guards the third with a null check:

```c
bool insertendsetsinspanf(typetask *taskptr, typespanf spanfptr,
    typeisa *linkisaptr,
    typesporglset fromsporglset,
    typesporglset tosporglset,
    typesporglset threesporglset)
{
  if (!(insertspanf(taskptr,spanfptr,linkisaptr,fromsporglset,LINKFROMSPAN)
        && insertspanf(taskptr,spanfptr,linkisaptr,tosporglset,LINKTOSPAN)))
      return (FALSE);
  if (threesporglset) {
      if(!insertspanf(taskptr,spanfptr,linkisaptr,threesporglset,LINKTHREESPAN))
          return (FALSE);
  }
  return(TRUE);
}
```

No fourth parameter, no fourth insertion, no fourth constant.

**`insertendsetsinorgl()`** (`do2.c:130-149`) mirrors this exactly for the orgl (order layer), guarding the third endset pair with:

```c
if (threevsa && threesporglset) {
    if (!insertpm(taskptr, linkisaptr, link, threevsa, threesporglset))
        return (FALSE);
}
```

---

### 4. Retrieval is capped at three

**`retrieveendsetsfromspanf()`** (`spanf1.c:190-217`) reconstructs the three endsets from storage using `LINKFROMSPAN`, `LINKTOSPAN`, `LINKTHREESPAN` — and nothing higher. The function signature exposes exactly three output pointers:

```c
bool retrieveendsetsfromspanf(typetask *taskptr,
    typespecset specset,
    typespecset *fromsetptr,
    typespecset *tosetptr,
    typespecset *threesetptr)
```

`doretrieveendsets()` (`do1.c:369`) simply delegates to it. The FEBE response formatter `putretrieveendsets()` (`put.c:222`) also takes exactly three sets.

---

### 5. Runtime input validation enforces 1–3

**`getfollowlink()`** (`get1.c:63-74`) validates user-supplied endset numbers at the protocol boundary:

```c
if (!(
   getnumber(taskptr, whichendptr)
&& (*whichendptr == 1 || *whichendptr == 2 || *whichendptr == 3)))
    return (FALSE);
```

A client requesting endset 4 is rejected here before any backend function is called.

---

### Summary

udanax-green never constructs, stores, or retrieves a link with more than three endsets. The limit is enforced simultaneously at:

| Layer | Location | Mechanism |
|---|---|---|
| Constants | `xanadu.h:36-38` | Only `LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3` defined |
| Creation API | `do1.c:195`, `do1.c:169` | Function signatures accept at most three endset arguments |
| Spanfilade write | `do2.c:116` | Third endset conditional on null; no fourth parameter exists |
| Orgl write | `do2.c:130` | Same pattern |
| Spanfilade read | `spanf1.c:190` | Three output pointers, three constants, nothing beyond |
| Protocol input | `get1.c:71` | Hard validation: `whichend` ∈ {1, 2, 3} |

`DOCISPAN=4` is not a fourth link endset slot. It is a structurally adjacent but semantically orthogonal stream value used to index document containment in the spanfilade, not link directionality.
