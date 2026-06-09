## Question 3 [evidence]

> When CREATELINK's type endset argument resolves (via vspanset2sporglset) to an empty sporgl set, does the implementation reject the call, and if so how — or does it guarantee the type spec can never resolve empty?

## KB Synthesis

The KB does not fully answer this question. Here is what it does and does not establish:

**What is known:**

Zero-width type VSpecs crash. `[PRE-LINK-CREATE]` states the minimum valid endpoint width is 1 and zero-width endpoints produce Bug 0017 (crash). `[PRE-ZERO-WIDTH]` confirms the general rule that zero-width mutation arguments crash while zero-width queries succeed cleanly.

The type endset goes through the same `vspanset2sporglset` path as source/target. `[ST-LINK-CREATE Finding 0037]` confirms `domakelink` uses this path for all three endsets — it iterates each I-span from `vspanset2ispanset` and produces one sporgl per contiguous I-region.

**What is not answerable from the KB:**

There is no KB entry documenting what happens when a *non-zero-width* type VSpec resolves to an *empty* sporgl set — i.e., when the referenced V-span has width > 0 but maps to no content in the POOM (open document not containing the type content, or content deleted). The `[SS-LINK-ENDPOINT Finding 0037]` path would produce an empty sporglset silently, but whether `domakelink` then rejects, crashes, or proceeds with an empty type endset is not established.

The implicit practical guarantee is that types reference the bootstrap document's `1.0.2.x` addresses `[SS-LINK-ENDPOINT Finding 0024]`, which are stable. But whether the implementation enforces this or simply relies on caller convention — as with the subspace invariant `[INV-SUBSPACE-CONVENTION]` — is not documented.

---

## Code Exploration

Now I have everything I need from actual source. Here is the complete answer.

---

## CREATELINK Type Endset: Empty Sporgl Set Handling

### Short answer

The implementation does **not** reject the call. An empty type sporgl set passes silently through two explicit NULL guards and results in a link stored without a type endset. There is no code-level guarantee that the type spec can never resolve empty.

---

### Execution path

#### 1. `docreatelink` — no validation of empty result

`do1.c:195–221` is the core function. It calls `specset2sporglset` for all three endsets in a single `&&` chain:

```c
   && specset2sporglset (taskptr, threespecset, &threesporglset,NOBERTREQUIRED)  // do1.c:216
   && setlinkvsas (&fromvsa, &tovsa, &threevsa)                                  // do1.c:217
   && insertendsetsinorgl (... &threevsa, threesporglset)                        // do1.c:218
   && insertendsetsinspanf (... threesporglset)                                  // do1.c:219
```

There is **no check on `threesporglset` after line 216**. Whatever `specset2sporglset` puts in `threesporglset` — including NULL — is passed directly forward.

---

#### 2. `specset2sporglset` — returns TRUE with NULL for empty input

`sporgl.c:14–33`:

```c
   *sporglsetptr = NULL;                                // sporgl.c:18  — initialized to NULL
   for (; specset; ...)  { ... }                        // sporgl.c:19  — loop skips if specset is NULL/empty
   *sporglsetptr = NULL;                                // sporgl.c:30  — null-terminates (or re-nulls)
   return (TRUE);                                       // sporgl.c:32
```

If `threespecset` is NULL (empty list), the loop never runs. The function returns `TRUE` with `*sporglsetptr == NULL`.

---

#### 3. `vspanset2sporglset` — two distinct outcomes

`sporgl.c:35–65`. Two cases matter:

**Case A — `findorgl` fails** (`sporgl.c:44–46`):
```c
   if (!findorgl (taskptr, granf, docisa, &orgl,type)){
       return (NULL);                                   // sporgl.c:45
   }
```
`vspanset2sporglset` returns NULL. This propagates back through `specset2sporglset:25–27` as `return(FALSE)`, making `docreatelink` fail at `do1.c:216`. This is **document-not-found**, not empty-sporgl-set.

**Case B — `findorgl` succeeds but `vspanset` is empty/non-mapping** (`sporgl.c:47–58`):
```c
   for (; vspanset; vspanset = vspanset->next) {        // sporgl.c:47  — loop skips if vspanset is NULL
       (void) vspanset2ispanset (...);
       for (; ispanset; ispanset = ispanset->next) {    // sporgl.c:49  — inner loop also skips
           sporglset = (typesporgl *) taskalloc (...);  // never reached
           ...
           *sporglsetptr = ...;
       }
   }
   return (sporglsetptr);                               // sporgl.c:64
```
No sporgl items are allocated. `sporglsetptr` is returned unchanged — still pointing to the slot initialized to NULL at `sporgl.c:18`. After `specset2sporglset` null-terminates at line 30, `threesporglset == NULL`. Function returns `TRUE`.

---

#### 4. `insertendsetsinspanf` — explicit NULL guard

`do2.c:116–128`:

```c
   if (threesporglset) {                                // do2.c:122  — guard
       if(!insertspanf(...,threesporglset,LINKTHREESPAN)){
           return (FALSE);
       }
   }
   return(TRUE);                                        // do2.c:127  — returns TRUE if NULL
```

If `threesporglset` is NULL, `insertspanf` is never called. Returns TRUE.

---

#### 5. `insertendsetsinorgl` — explicit NULL guard with debug trace

`do2.c:130–149`:

```c
   if (threevsa && threesporglset) {                    // do2.c:136  — guard on BOTH
       if (!insertpm (taskptr, linkisaptr, link, threevsa, threesporglset)){
           return (FALSE);
       }
   }else{
   #ifndef DISTRIBUTION
       fprintf(stderr,"leaving INSERTENDSETSINORGL 4\n");      // do2.c:142
       fprintf(stderr," threevsa ptr= %x threesporglset ptr = %x ...\n",threevsa, threesporglset);
       dumptumbler(threevsa);
   #endif
   }
   return (TRUE);                                       // do2.c:147
```

If `threesporglset` is NULL, the else-branch fires. In non-DISTRIBUTION builds it prints the pointer values to stderr — **the debug trace at `do2.c:142–144` is a code-level acknowledgment that this path was known and expected during development**. `insertpm` is never called. Returns TRUE.

---

### Summary

| Stage | File:Line | What happens for empty type endset |
|---|---|---|
| `specset2sporglset(threespecset,...)` | `sporgl.c:18–32` | Initializes to NULL, loop skips, returns TRUE |
| `vspanset2sporglset(... vspanset=NULL ...)` | `sporgl.c:47` | Inner loop skips, no sporgls allocated, returns non-NULL pointer (to NULL slot) |
| `docreatelink` checks result | `do1.c:216` | No validation — NULL `threesporglset` passes forward |
| `insertendsetsinspanf` | `do2.c:122` | `if (threesporglset)` guard — skips, returns TRUE |
| `insertendsetsinorgl` | `do2.c:136` | `if (threevsa && threesporglset)` guard — skips, debug-prints, returns TRUE |

**The call is not rejected.** An empty type endset resolves to `NULL`, is explicitly guarded against in both insertion functions, and the link is created and stored without a type endset entry. No guarantee exists in the C code that the type spec can never resolve empty — the debug `fprintf` at `do2.c:142` shows the implementors knew and deliberately accommodated this case.
