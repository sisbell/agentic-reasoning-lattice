## Question 1 [evidence]

> Does udanax-green's RETRIEVEENDSETS always emit exactly three endset slots, and can the link store ever hold links of arity greater than 3 whose extra-slot endsets touch the queried region?

## KB Synthesis

## RETRIEVEENDSETS: Slot Count and Link Arity

**RETRIEVEENDSETS always emits exactly three slots.**

The operation is hardwired to three endpoint types. From [SS-RETRIEVE-ENDSETS] (Finding 0035): it returns `from-endset`, `to-endset`, and `three-endset` simultaneously by searching the spanfilade with three hardcoded ORGLRANGE prefix constants — `LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3`. Each slot is always present in the return structure; any may be an empty specset if no matching links exist. The "three-endset is conditionally retrieved (only if requested)" means the caller can suppress the third search, but the slot still exists structurally.

**The link store has no provision for arity > 3.**

Every architectural layer enforces exactly three endpoint types:

- **Creation** — `docreatelink(home, source_specs, target_specs, type_specs)` takes exactly three endpoint parameters [ST-CREATE-LINK, Finding 0012].
- **Spanfilade indexing** — `insertendsetsinspanf` inserts into exactly three ORGLRANGE subspaces (1/2/3) [INT-SPORGL-LINK-INDEX, Finding 0013; Finding 0035].
- **V-space subspace convention** — three subspaces only: `1`=text, `2`=link reference, `3`=link type endpoint [SS-SUBSPACE-CONVENTION, Finding 0038].
- **Search** — `findlinksfromtothreesp` / `retrieveendsetsfromspanf` iterate over exactly these three constants [SS-RETRIEVE-ENDSETS, Finding 0035].

No finding documents any mechanism for a fourth or higher endpoint slot, any variable-arity link structure, or any ORGLRANGE constant beyond 3. There are no extra-slot endsets that could touch a queried region, because no such slots can be stored.

---

## Code Exploration

I have all the evidence needed. Here is the full analysis:

---

## RETRIEVEENDSETS Arity: Full Code Analysis

### Question 1: Does RETRIEVEENDSETS always emit exactly three endset slots?

**Yes — exactly three, hardcoded throughout the call chain. But the third slot is always a duplicate of the second due to a bug in the output function.**

#### Call chain

**`backend/fns.c:350-362`** — top-level handler:
```c
void retrieveendsets(typetask *taskptr)
{
  typespecset specset, fromset, toset, threeset;
  ...
  if (getretrieveendsets(taskptr, &specset)
  && doretrieveendsets(taskptr, specset, &fromset, &toset, &threeset)) {
      putretrieveendsets(taskptr, fromset, toset, threeset);
  } else
      putrequestfailed(taskptr);
}
```
Three variables, three output parameters — no more.

**`backend/do1.c:369-374`** — thin delegation:
```c
bool doretrieveendsets(typetask *taskptr, typespecset specset,
    typespecset *fromsetptr, typespecset *tosetptr, typespecset *threesetptr)
{
    return retrieveendsetsfromspanf(taskptr, specset, fromsetptr, tosetptr, threesetptr);
}
```

**`backend/spanf1.c:190-235`** — the actual retrieval hardcodes exactly three span spaces using constants loaded from `backend/xanadu.h`:
```c
fromspace.stream.mantissa[0] = LINKFROMSPAN;   // spanf1.c:210
tospace.stream.mantissa[0]   = LINKTOSPAN;     // spanf1.c:213
threespace.stream.mantissa[0] = LINKTHREESPAN; // spanf1.c:216
```
The function then retrieves `fromsporglset`, `tosporglset`, and `threesporglset` from those three fixed span addresses, and converts them to specsets. There is no loop, no variadic, and no fourth retrieve call.

**`backend/put.c:222-230`** — output:
```c
int putretrieveendsets(typetask *taskptr, typespecset fromset,
                       typespecset toset, typespecset threeset)
{
    fprintf(taskptr->outp, "\nfromset\n");
    putitemset(taskptr, fromset);
    fprintf(taskptr->outp, "\ntoset\n");
    putitemset(taskptr, toset);
    fprintf(taskptr->outp, "\nthreeset\n");
    putitemset(taskptr, toset);    // <-- BUG: line 229, should be threeset
}
```

**Bug at `backend/put.c:229`**: the parameter named `threeset` is passed correctly through the entire call chain — retrieved accurately in `retrieveendsetsfromspanf` — but the output function passes `toset` to `putitemset` instead of `threeset`. The client therefore always receives the `toset` content in both the "toset" and "threeset" slots. The actual third endset data, even when non-null, is silently dropped at the wire boundary.

---

### Question 2: Can the link store hold links of arity > 3?

**No. The architecture is structurally capped at three endsets with no overflow path.**

#### Span type constants — `backend/xanadu.h:36-38`

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```

Only three `LINK*SPAN` constants exist. `DOCISPAN=4` is the document-pointer slot, not a fourth endset. There is no `LINKFOURSPAN` or higher.

The spanfilade uses these integer values as the `spantype` key when indexing link endsets. A fourth endset would require a fourth constant to be stored and retrievable.

#### Link creation — `backend/do1.c:195-221`

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr,
    typespecset fromspecset, typespecset tospecset, typespecset threespecset,
    typeisa *linkisaptr)
```

The function signature is fixed at three endset parameters. `insertendsetsinspanf` and `insertendsetsinorgl` are called with those three — no more.

#### Spanfilade insertion — `backend/do2.c:116-128`

```c
bool insertendsetsinspanf(typetask *taskptr, typespanf spanfptr,
    typeisa *linkisaptr,
    typesporglset fromsporglset, typesporglset tosporglset,
    typesporglset threesporglset)
{
    if (!(insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
        && insertspanf(taskptr, spanfptr, linkisaptr, tosporglset, LINKTOSPAN)))
            return(FALSE);
    if (threesporglset) {
        if (!insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN))
            return(FALSE);
    }
    return(TRUE);
}
```

Three possible calls to `insertspanf`, keyed by constants 1, 2, 3. The same three-parameter pattern appears in `insertendsetsinorgl` at `backend/do2.c:130-140`.

#### Retrieval — `backend/spanf1.c:190-235`

`retrieveendsetsfromspanf` looks up exactly three span spaces by the same three constants. Even if a fourth span record existed in the file (which the creation path makes impossible), there is no code that would fetch it. The retrieval is not range-based; it is three explicit constant lookups.

---

### Summary

| Claim | Verdict | Key citation |
|---|---|---|
| RETRIEVEENDSETS always emits exactly 3 slots | **True** | `fns.c:352`, `spanf1.c:210-217`, `put.c:222-230` |
| Third slot contains correct threeset data | **False (bug)** | `put.c:229` passes `toset` instead of `threeset` |
| Link store supports arity > 3 | **False** | `xanadu.h:36-38` (only 3 LINK*SPAN constants), `do2.c:116-128` (fixed 3-param signature) |
| Extra endsets of hypothetical high-arity links could touch queried region | **Impossible** | No creation path, no storage key, no retrieval code for endset 4+ |

The `put.c:229` bug is a confirmed defect: the wire protocol always echoes `toset` as `threeset`. Any link whose third endset differs from its second endset will silently misreport the threeset to all clients.
