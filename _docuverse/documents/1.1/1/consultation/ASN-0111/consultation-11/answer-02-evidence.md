## Question 2 [evidence]

> Does udanax-green permit a link to carry more than three endsets, or is the three-endset cap enforced such that no reachable state contains an `N > 3` link?

## KB Synthesis

The three-endset cap is structurally enforced — no reachable state can contain a link with N > 4 endsets, because the ceiling is exactly three and is hard-coded at every layer.

**Creation is fixed-arity.** `docreatelink` / `domakelink` accept exactly three sporglset parameters (FROM, TO, THREE) and pass them to `insertendsetsinspanf` as three independent calls. There is no variadic endset API. [ST-CREATE-LINK], [SS-LINK-ENDPOINT Finding 0028]

**The spanfilade index has exactly three endset type slots.** The ORGLRANGE dimension uses three named constants: `LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3`. These are the only values ever written or queried. [SS-SPORGL-LINK-INDEX Finding 0035]

**The V-space subspace allocation also encodes exactly three.** `setlinkvsas()` hardcodes digit-0 values of 1 (from), 2 (to), and 3 (type endpoint) — a fixed structural tripling. [SS-DUAL-ENFILADE Finding 0038], [FC-SUBSPACE Finding 0038]

**The retrieval interface enforces three.** RETRIEVEENDSETS returns exactly three specsets simultaneously. FOLLOWLINK accepts a `whichend` parameter constrained to positions 1, 2, or 3. FINDLINKSFROMTOTHREE, FINDNUMOFLINKSFROMTOTHREE, and FINDNEXTNLINKSFROMTOTHREE all encode "three" in their names and signatures. [SS-RETRIEVE-ENDSETS], [SS-FOLLOW-LINK]

**Links are immutable after creation.** No post-creation operation modifies a link's endsets. [SS-LINK-ENDPOINT Finding 0028], [INV-LINK-PERMANENCE]

In summary: the three-endset structure is not a soft convention but a hard schema — creation, indexing, and retrieval all assume exactly three slots and provide no path to exceed that count.

---

## Code Exploration

I have everything needed. Here is the full answer.

---

## Does udanax-green permit links with more than three endsets?

**No. The three-endset cap is absolute and structurally enforced throughout the call chain. No reachable state contains an N > 3 link.**

---

### 1. The constants define exactly three endset slots

`backend/xanadu.h:36-38`:
```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
```

There is no `LINKFOURSPAN` or any higher constant anywhere in the codebase. These are the only symbolic names for endset positions, and every layer of the implementation uses them exclusively.

---

### 2. The wire protocol parses exactly three endsets — by name

`backend/get1.c:46-61` — `getcreatelink`:
```c
bool getcreatelink(typetask *taskptr, typeisa *docisaptr,
    typespecset *fromspecsetptr, typespecset *tospecsetptr,
    typespecset *threespecsetptr)
{
    prompt (taskptr, "home document=> ");
    if (!getisa (taskptr, docisaptr))         return (FALSE);
    prompt (taskptr, "fromset\n");
    if (!getspecset (taskptr, fromspecsetptr)) return (FALSE);
    prompt (taskptr, "toset\n");
    if (!getspecset (taskptr, tospecsetptr))   return (FALSE);
    prompt (taskptr, "threeset\n");
    if (!getspecset (taskptr, threespecsetptr))return (FALSE);
    return (TRUE);
}
```

The function signature takes three positional specset pointers. There is no length field, no loop, no variadic argument. A fourth endset cannot be expressed on the wire.

---

### 3. Endset index validation rejects anything outside {1, 2, 3}

`backend/get1.c:63-74` — `getfollowlink`:
```c
if (!(
   getnumber (taskptr, whichendptr)
&& (*whichendptr == 1 || *whichendptr == 2 || *whichendptr == 3)))
    return (FALSE);
```

If a client sends endset index 4, the boolean short-circuits to `FALSE` and the request fails. No data is fetched; no mutation occurs.

---

### 4. Both creation paths cap at three — structurally, not conditionally

`backend/do1.c:169-221` contains the two link-creation functions:

**`domakelink`** (do1.c:169-193) — two endsets, third explicitly `NULL`:
```c
&& setlinkvsas (&fromvsa, &tovsa, NULL)
&& insertendsetsinorgl (taskptr, linkisaptr, link,
       &fromvsa, fromsporglset, &tovsa, tosporglset, NULL, NULL)
&& insertendsetsinspanf (taskptr, spanf, linkisaptr,
       fromsporglset, tosporglset, NULL)
```

**`docreatelink`** (do1.c:195-221) — the public FEBE path, three endsets:
```c
&& setlinkvsas (&fromvsa, &tovsa, &threevsa)
&& insertendsetsinorgl (taskptr, linkisaptr, link,
       &fromvsa, fromsporglset, &tovsa, tosporglset, &threevsa, threesporglset)
&& insertendsetsinspanf (taskptr, spanf, linkisaptr,
       fromsporglset, tosporglset, threesporglset)
```

Neither function takes a count or a list. The maximum number of endsets that can be passed is three; the function signatures enforce this at compile time.

---

### 5. VSA assignment hardcodes indices 1, 2, 3 — no loop, no generalization

`backend/do2.c:169-183` — `setlinkvsas`:
```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
    tumblerclear (fromvsaptr);
    tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);   /* slot 1 */
    tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);
    tumblerclear (tovsaptr);
    tumblerincrement (tovsaptr, 0, 2, tovsaptr);        /* slot 2 */
    tumblerincrement (tovsaptr, 1, 1, tovsaptr);
    if (threevsaptr) {
        tumblerclear (threevsaptr);
        tumblerincrement (threevsaptr, 0, 3, threevsaptr); /* slot 3 */
        tumblerincrement (threevsaptr, 1, 1, threevsaptr);
    }
    return (TRUE);
}
```

The function assigns tumbler-space addresses for slots 1, 2, and optionally 3. There is no slot 4 — not conditionally, not in a loop, not reachable by any argument.

---

### 6. The spanfilade insertion is a fixed three-branch switch — no generalization

`backend/do2.c:116-128` — `insertendsetsinspanf`:
```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
  && insertspanf(taskptr, spanfptr, linkisaptr, tosporglset, LINKTOSPAN)
...
if (threesporglset) {
    insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN)
}
```

Three explicit calls. No loop. No array of endsets. The spanfilade records for a link are one-to-one with LINKFROMSPAN, LINKTOSPAN, and (optionally) LINKTHREESPAN — a link with a fourth endset cannot exist in the spanfilade because there is no code path that would write it.

The granfilade orgl layer is identical — `insertendsetsinorgl` (do2.c:130-149) calls `insertpm` exactly three times, with the third conditional on both `threevsa` and `threesporglset` being non-NULL.

---

### Conclusion

The three-endset cap is not a single runtime guard — it is a structural property of the entire system. Every layer enforces it independently:

| Layer | Enforcement | Location |
|---|---|---|
| Wire protocol | Parses exactly 3 named specsets | `get1.c:46-61` |
| Endset index validation | Whitelist `{1,2,3}` | `get1.c:70-71` |
| Link creation signatures | Fixed-arity, no count param | `do1.c:169,195` |
| VSA assignment | Hardcoded slots 1, 2, 3 | `do2.c:169-183` |
| Spanfilade insertion | Three explicit `insertspanf` calls | `do2.c:116-128` |
| Granfilade insertion | Three explicit `insertpm` calls | `do2.c:130-149` |
| Symbolic constants | Only `LINKFROMSPAN/TOSPAN/THREESPAN` defined | `xanadu.h:36-38` |

No reachable code path creates, stores, or retrieves a link with N > 3 endsets. The cap is hard-baked into the function signatures, the constant table, and the call structure — not a policy check that could be bypassed, but an architectural fact of how the system is assembled.
