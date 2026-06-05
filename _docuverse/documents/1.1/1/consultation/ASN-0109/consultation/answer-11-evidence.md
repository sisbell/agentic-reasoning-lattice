## Question 11 [evidence]

> When RETRIEVEENDSETS reads a link by its address, does it return all three endsets (source/from, target/to, type) as distinct I-address spans, and in what order are they delivered?

## KB Synthesis

RETRIEVEENDSETS and FOLLOWLINK are distinct operations — the distinction is important here.

**RETRIEVEENDSETS** [SS-RETRIEVE-ENDSETS] takes a *content specset* (V-span of a region), not a link address. It searches the spanfilade and returns all three endsets simultaneously: from-endset, to-endset, and three-endset. The three endset types are searched independently using separate ORGLRANGE subspace prefixes — LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3 — so they come back as three distinct specsets. The three-endset is conditionally retrieved (only if requested). All results are resolved into the *querying document's* V-space via `linksporglset2specset`, not as raw I-addresses.

**FOLLOWLINK** [SS-FOLLOWLINK] is what actually reads a link *by its address* (ISA). It returns *one* endset at a time — whichever endpoint (position 0.1, 0.2, or 0.3) the caller requests — and resolves it through a specified `homedoc`'s POOM. I-addresses with no current POOM mapping are silently dropped [INV-ITOV-FILTERING].

So: RETRIEVEENDSETS delivers all three endsets in a single call (from → to → type order by ORGLRANGE numbering), but it is content-search-driven. FOLLOWLINK delivers one endset per call, link-address-driven.

---

## Code Exploration

Now I have everything needed for a complete, cited answer.

---

## RETRIEVEENDSETS: Endset Return Order and Structure

### Short Answer

Yes — RETRIEVEENDSETS returns all three endsets as distinct I-address spans. The delivery order is: **fromset → toset → threeset**, where "three" is the type/context endset.

---

### Call Chain

```
bed.c:xanadu()  [dispatch table]
  → fns.c:retrieveendsets()
      → get1.c:getretrieveendsets()     [reads the input specset]
      → do1.c:doretrieveendsets()       [thin wrapper]
          → spanf1.c:retrieveendsetsfromspanf()  [core logic]
      → putfe.c:putretrieveendsets()    [binary FEBE output]
```

---

### Endset Constants

Defined in `backend/xanadu.h:35-39`:

```c
/* spanfilade span types */
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```

These are the discriminators stored in `typespan.stream.mantissa[0]` when endsets are inserted into the spanfilade. Insertion order is confirmed by `do2.c:116-126`:

```c
bool insertendsetsinspanf(...)
{
    if (!(
        insertspanf(taskptr,spanfptr,linkisaptr,fromsporglset,LINKFROMSPAN)    // [do2.c:119]
          &&insertspanf(taskptr,spanfptr,linkisaptr,tosporglset,LINKTOSPAN)))  // [do2.c:120]
            return (FALSE);
    if (threesporglset) {
        if(!insertspanf(taskptr,spanfptr,linkisaptr,threesporglset,LINKTHREESPAN)){ // [do2.c:123]
            return (FALSE);
        }
    }
```

The three endsets are stored at spanfilade offsets 1, 2, and 3 respectively.

---

### Retrieval Logic — `spanf1.c:190-234`

`retrieveendsetsfromspanf` constructs three probe spans, each with width=1, at the offsets corresponding to the three endset types:

```c
fromspace.stream.mantissa[0] = LINKFROMSPAN;    // [spanf1.c:210]
fromspace.width.mantissa[0] = 1;

tospace.stream.mantissa[0] = LINKTOSPAN;        // [spanf1.c:213]
tospace.width.mantissa[0] = 1;

threespace.stream.mantissa[0] = LINKTHREESPAN;  // [spanf1.c:216]
threespace.width.mantissa[0] = 1;
```

It then retrieves them in this order — **from and to are mandatory** (joined with `&&` inside one `if`); the three endset is retrieved in a separate conditional block:

```c
if (!(specset2sporglset (taskptr, specset, &sporglset, NOBERTREQUIRED)
&& retrievesporglsetinrange(taskptr,sporglset,&fromspace,&fromsporglset)     // [spanf1.c:223]
&& linksporglset2specset (..., fromsporglset, fromsetptr, ...)               // [spanf1.c:224]
&& retrievesporglsetinrange (taskptr, sporglset, &tospace, &tosporglset)     // [spanf1.c:225]
&& linksporglset2specset (..., tosporglset, tosetptr, ...))){                // [spanf1.c:226]
        return (FALSE);
}
if (threesetptr) {                                                           // [spanf1.c:229]
      temp = (retrievesporglsetinrange(taskptr, sporglset, &threespace, &threesporglset)
          && linksporglset2specset(..., threesporglset, threesetptr, ...));
    return(temp);
}
```

If from or to retrieval fails, the function returns `FALSE` immediately — three is never attempted. The three endset is conditional on `threesetptr != NULL`. In `fns.c:352`, `threeset` is a stack-local variable and `&threeset` is always passed, so in normal FEBE operation `threesetptr` is always non-NULL and all three endsets are always retrieved.

---

### Wire Encoding — `putfe.c:356-362`

The binary FEBE output (used by both `backend` and `backenddaemon` per `Makefile:35-38`) is:

```c
int putretrieveendsets(typetask *taskptr, typespecset fromset, typespecset toset, typespecset threeset)
{
        putnumber (taskptr->outp, RETRIEVEENDSETS);     // [putfe.c:358]
        putitemset (taskptr, (typeitemset)fromset);     // [putfe.c:359]
        putitemset (taskptr, (typeitemset)toset);       // [putfe.c:360]
        putitemset (taskptr, (typeitemset)threeset);    // [putfe.c:361]
}
```

Three distinct itemsets are emitted on the wire: fromset, toset, threeset — in that order, each as a full `typeitemset` (list of I-address spans).

---

### Bug in `put.c` (text/debug path only)

`put.c:222-230` is compiled only into `xumain` (the text-mode interactive binary, `Makefile:32`), not into the daemon. It has a copy-paste bug:

```c
fprintf (taskptr->outp, "\nthreeset\n");
putitemset (taskptr, toset);    // [put.c:229] — BUG: should be threeset
```

`toset` is emitted twice; `threeset` is never output. This does **not** affect the FEBE protocol daemon — `putfe.c` is correct — but it means the `xumain` debug interface silently drops the type endset.

---

### Summary

| Endset | Spanfilade Offset (mantissa[0]) | Wire Position | Code |
|--------|--------------------------------|---------------|------|
| from (source) | `LINKFROMSPAN = 1` | 1st itemset | `xanadu.h:36`, `spanf1.c:210`, `putfe.c:359` |
| to (target)   | `LINKTOSPAN = 2`   | 2nd itemset | `xanadu.h:37`, `spanf1.c:213`, `putfe.c:360` |
| three (type)  | `LINKTHREESPAN = 3`| 3rd itemset | `xanadu.h:38`, `spanf1.c:216`, `putfe.c:361` |

All three are returned as distinct I-address spans. The delivery order is **from, to, three** — matching the insertion order in `do2.c:119-123`. The `put.c` text-output path has a bug that drops threeset, but the live FEBE binary protocol (`putfe.c`) is correct.
