## Question 6 [evidence]

> Does the udanax-green link data structure support more than three endsets per link, or is the arity fixed at exactly three (F, G, Θ) throughout the implementation?

## KB Synthesis

The arity is fixed at exactly three throughout the implementation. No path in the KB describes more than three endsets per link.

**Structural evidence:**

- `setlinkvsas()` hardcodes exactly three V-subspace positions — digit-0 values 1 (FROM), 2 (TO), 3 (THREE/type) — with no extensible mechanism [SS-SUBSPACE-CONVENTION, Finding 0038]
- The spanf index registers exactly three ORGLRANGE subspaces: `LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3` [INT-SPORGL-LINK-INDEX]
- `RETRIEVEENDSETS` (opcode 28) "returns three specsets simultaneously: from-endset, to-endset, and three-endset" [SS-RETRIEVE-ENDSETS]
- `FOLLOWLINK`'s `whichend` parameter accepts exactly positions 0.1, 0.2, or 0.3 — hardcoded in `link2sporglset()` [SS-FOLLOWLINK]
- `docreatelink()` signature is `(home_doc, from, to, three)` — a fixed four-argument function [ST-CREATE-LINK]

**Semantic role of the third endset:**

The THREE slot is the *type* endpoint — it references a VSpec in the bootstrap document's type registry at `1.0.2.x` (e.g., JUMP=`1.0.2.2`, QUOTE=`1.0.2.3`, FOOTNOTE=`1.0.2.6`, MARGIN=`1.0.2.6.2`). The type is itself content-addressed, not a numeric enum [SS-LINK-ENDPOINT, Finding 0024].

**Conclusion:** The arity is fixed at three. The implementation has no variable-endset mechanism — every link has exactly a FROM, a TO, and a TYPE (THREE) endset, allocated as hardcoded subspaces in both the POOM and the spanfilade.

---

## Code Exploration

## Link Arity in Udanax-Green: Fixed at Exactly Three

The link arity is **fixed at exactly three endsets (F, G, Θ)**. There is no dynamic or extensible arity anywhere in the implementation. Every layer of the stack — constants, function signatures, retrieval logic, input validation — hardcodes the number 3.

---

### 1. The Three Constants

`backend/xanadu.h` defines exactly three span-type constants:

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
```

There is no `LINKFOURSPAN`, no array, no `NUMENDSETS` constant.

---

### 2. FEBE Handler: Three Specsets, No More

`backend/fns.c:100–112` — `createlink`:

```c
void createlink(typetask *taskptr)
{
    typeisa docisa, linkisa;
    typespecset fromspecset, tospecset, threespecset;
    ...
    if (
       getcreatelink (taskptr, &docisa, &fromspecset, &tospecset, &threespecset)
    && docreatelink (taskptr, &docisa, fromspecset, tospecset, threespecset, &linkisa)){
```

Three separate specset locals. No array, no count parameter, no varargs.

---

### 3. `docreatelink` Signature

`backend/do1.c` — `docreatelink` takes:

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr,
                  typespecset fromspecset,
                  typespecset tospecset,
                  typespecset threespecset,
                  typeisa *linkisaptr)
```

Three named endset parameters. Creation calls:

```c
setlinkvsas (&fromvsa, &tovsa, &threevsa)
insertendsetsinorgl (taskptr, linkisaptr, link,
                     &fromvsa, fromsporglset,
                     &tovsa, tosporglset,
                     &threevsa, threesporglset)
insertendsetsinspanf (taskptr, spanf, linkisaptr,
                      fromsporglset, tosporglset, threesporglset)
```

All three callees accept exactly three endset arguments.

---

### 4. `setlinkvsas` Hardcodes Positions 1, 2, 3

`backend/do2.c` — `setlinkvsas`:

```c
tumblerincrement (fromvsaptr,  0, 1, fromvsaptr);   // F at position 1
tumblerincrement (tovsaptr,    0, 2, tovsaptr);     // G at position 2
tumblerincrement (threevsaptr, 0, 3, threevsaptr);  // Θ at position 3
```

The mantissa values 1, 2, 3 are literal integers, not computed from any variable.

---

### 5. Insertion: Three Explicit Calls, No Loop

`backend/do2.c` — `insertendsetsinspanf`:

```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN)
```

Three unrolled calls. If arity were meant to be variable, this would be a loop over an array.

Similarly in `insertendsetsinorgl`:

```c
insertpm(taskptr, linkisaptr, link, fromvsa,   fromsporglset)
insertpm(taskptr, linkisaptr, link, tovsa,     tosporglset)
insertpm(taskptr, linkisaptr, link, threevsa,  threesporglset)
```

---

### 6. Input Validation Rejects Any `whichend` Outside {1, 2, 3}

`backend/get1.c` — `getfollowlink`:

```c
&& (*whichendptr == 1 || *whichendptr == 2 || *whichendptr == 3)
```

This is an explicit whitelist. A value of 4 would cause the function to return `FALSE` and the follow operation to fail.

---

### 7. Retrieval: Three Independent Code Paths, No Loop

`backend/spanf1.c` — `retrieveendsetsfromspanf`:

```c
fromspace.stream.mantissa[0]  = LINKFROMSPAN;   // 1
tospace.stream.mantissa[0]    = LINKTOSPAN;     // 2
threespace.stream.mantissa[0] = LINKTHREESPAN;  // 3
```

Three separate `retrievesporglsetinrange` calls. The third (Θ) is guarded by `if (threesetptr)` — it is optional at retrieval time, but there is no mechanism to add a fourth.

---

### 8. `dofind` Intersection Logic: Hardwired Three-Way

`backend/spanf2.c` — `intersectlinksets` implements exactly:
- Single-set passthrough (any one of three)
- Two-way intersection (when `linkset3 == NULL`)
- Three-way intersection (nested triple loop)

No four-way path exists.

---

## Verdict

**Link arity is architecturally fixed at 3.** The triad F/G/Θ is not a convention layered on a general N-endset structure — it is the structure. Adding a fourth endset would require:

1. New `LINKFOURSPAN = 4` constant in `backend/xanadu.h`
2. New parameters to `docreatelink`, `insertendsetsinorgl`, `insertendsetsinspanf`, `retrieveendsetsfromspanf`, and the FEBE handler `createlink` in `backend/fns.c`
3. A fourth `setlinkvsas` position in `backend/do2.c`
4. Extending the `whichend` whitelist in `backend/get1.c`
5. A four-way intersection branch in `backend/spanf2.c`
6. Protocol changes in the FEBE wire format

The design mirrors the original Xanadu specification's three-part link (from-set, to-set, type-set), and the C implementation encodes that arity as a structural invariant, not a parameter.
