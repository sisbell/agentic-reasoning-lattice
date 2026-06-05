## Question 14 [evidence]

> Does RETRIEVEENDSETS search the spanfilade to reconstruct the endsets, or does it read the endset spans directly from the link orgl stored in the granfilade?

## KB Synthesis

RETRIEVEENDSETS searches the **spanfilade**, not the link orgl in the granfilade.

[SS-RETRIEVE-ENDSETS] is explicit: the operation works entirely through `retrieveendsetsfromspanf()`. The call chain is:

1. Input specset → sporglset via V-to-I translation (SPANRANGE restriction)
2. Three ORGLRANGE prefix searches in the spanfilade: LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3
3. Results converted back to V-addresses using the **querying document's** docid via `linksporglset2specset()`

This contrasts with FOLLOWLINK [SS-FOLLOWLINK], which reads link endset I-addresses directly from the link orgl stored in the granfilade via `link2sporglset()`, then resolves them through a specified document's POOM.

The key distinction [INT-SPORGL-LINK-INDEX]:

| | RETRIEVEENDSETS | FOLLOWLINK |
|---|---|---|
| Input | V-span region | Link ISA + which-end |
| Lookup | Spanfilade search | Link orgl direct read |
| Returns | All three endsets | One endset |
| Resolution perspective | Querying document | Link's home |

RETRIEVEENDSETS is thus content-identity-based discovery (finds all link endpoints intersecting a region), while FOLLOWLINK is direct object access (reads a known link's stored endpoints). This is why RETRIEVEENDSETS can discover links from transcluded documents — it searches I-space, where shared content identity is the only discriminator [INT-LINK-TRANSCLUSION].

---

## Code Exploration

All citations verified. Here is the answer.

---

## RETRIEVEENDSETS: Spanfilade Search, Not Granfilade Direct Read

**RETRIEVEENDSETS searches the spanfilade to reconstruct the endsets.** It does not read endset spans directly from the link orgl stored in the granfilade. The granfilade is only consulted for coordinate conversion.

---

### Call Chain

#### 1. FEBE Handler — `fns.c:350`

```c
void retrieveendsets(typetask *taskptr)
{
    typespecset specset, fromset, toset, threeset;
    bool getretrieveendsets(), doretrieveendsets();

    if (   getretrieveendsets(taskptr, &specset)
        && doretrieveendsets(taskptr, specset, &fromset, &toset, &threeset)) {
        putretrieveendsets(taskptr, fromset, toset, threeset);
    } else
        putrequestfailed(taskptr);
}
```

`getretrieveendsets` parses the incoming FEBE message into a `specset` (a vspec identifying the link). Then `doretrieveendsets` does all the work.

---

#### 2. Thin Wrapper — `do1.c:369`

```c
bool doretrieveendsets(typetask *taskptr, typespecset specset,
    typespecset *fromsetptr, typespecset *tosetptr, typespecset *threesetptr)
{
    bool retrieveendsetsfromspanf();
    return retrieveendsetsfromspanf(taskptr, specset, fromsetptr, tosetptr, threesetptr);
}
```

`doretrieveendsets` is a pure passthrough. All logic is in `retrieveendsetsfromspanf`.

---

#### 3. Core Logic — `spanf1.c:190`

```c
bool retrieveendsetsfromspanf(typetask *taskptr, typespecset specset,
    typespecset *fromsetptr, typespecset *tosetptr, typespecset *threesetptr)
{
    typespan fromspace, tospace, threespace;
    typesporglset sporglset;
    ...

    fromspace.stream.mantissa[0] = LINKFROMSPAN;   // spanf1.c:210
    fromspace.width.mantissa[0] = 1;

    tospace.stream.mantissa[0] = LINKTOSPAN;       // spanf1.c:213
    tospace.width.mantissa[0] = 1;

    threespace.stream.mantissa[0] = LINKTHREESPAN; // spanf1.c:216
    threespace.width.mantissa[0] = 1;

    if (!(specset2sporglset(taskptr, specset, &sporglset, NOBERTREQUIRED)  // spanf1.c:222
       && retrievesporglsetinrange(taskptr, sporglset, &fromspace, &fromsporglset)  // :223
       && linksporglset2specset(...)
       && retrievesporglsetinrange(taskptr, sporglset, &tospace, &tosporglset)    // :225
       && linksporglset2specset(...)))
        return FALSE;
    ...
}
```

Two distinct operations are happening:

1. **`specset2sporglset` (line 222)** — this converts the incoming vspec (link address) into a sporgl, which *does* involve the granfilade. But this only establishes the link's orgl identity; it does not read the endset content.

2. **`retrievesporglsetinrange` (lines 223, 225, 230)** — this is the actual endset retrieval. It queries the spanfilade for spans at `LINKFROMSPAN`, `LINKTOSPAN`, and `LINKTHREESPAN` stream coordinates.

---

#### 4. Spanfilade Query — `spanf1.c:237`

```c
bool retrievesporglsetinrange(typetask *taskptr, typesporglset sporglptr,
    typespan *whichspace, typesporglset *sporglsetptr)
{
    for (; sporglptr; sporglptr = (typesporglset)sporglptr->xxxxsporgl.next) {
        context = retrieverestricted(
            (typecuc*)spanf,           // spanf1.c:245 — spanf is the spanfilade root
            (typespan*)sporglptr, SPANRANGE,
            whichspace, ORGLRANGE,
            (typeisa*)NULL
        );
        for (c = context; c;) {
            sporglset = (typesporgl*) taskalloc(taskptr, sizeof(typesporgl));
            contextintosporgl((type2dcontext*)c, (tumbler*)NULL, sporglset, SPANRANGE);
            ...
        }
    }
    return TRUE;
}
```

The critical line is **`spanf1.c:245`**: `retrieverestricted` is called with `(typecuc*)spanf` — this is the **spanfilade** global, not the granfilade. The call is a 2D rectangular range query:

- **Dimension 1 (SPANRANGE):** the sporgl address of the link itself (from the orgl converted in step 3.1)
- **Dimension 2 (ORGLRANGE):** `LINKFROMSPAN`, `LINKTOSPAN`, or `LINKTHREESPAN` — the stream coordinate where the endsets are stored

---

### What the Granfilade Actually Does Here

The granfilade is involved only through `specset2sporglset` (`spanf1.c:222`), which converts a vspec into a sporgl. This amounts to: "given this link's tumbler address, find its orgl in the granfilade." The result is a sporgl (a pointer into the spanfilade's orgl dimension) that is then used as the search key for the spanfilade query.

The granfilade does **not** store endset spans directly. Endsets are spans recorded in the spanfilade at specific stream coordinates (`LINKFROMSPAN` = from-endset, `LINKTOSPAN` = to-endset, `LINKTHREESPAN` = three-endset). RETRIEVEENDSETS reconstructs them by traversing the spanfilade enfilade tree via `findcbcinarea2d` (called from `retrieverestricted` → `retrieveinarea`, `retrie.c:87`).

---

### Summary

| Step | Function | File | Data Structure Accessed |
|------|----------|------|------------------------|
| 1 | `retrieveendsets` | `fns.c:350` | (FEBE message parsing) |
| 2 | `doretrieveendsets` | `do1.c:369` | (passthrough) |
| 3 | `retrieveendsetsfromspanf` | `spanf1.c:190` | granfilade (coord conversion only) |
| 4 | `retrievesporglsetinrange` | `spanf1.c:237` | **spanfilade** (endset spans) |
| 5 | `retrieverestricted` → `findcbcinarea2d` | `retrie.c:56,229` | **spanfilade** (B-tree traversal) |

**RETRIEVEENDSETS reconstructs endsets by doing a 2D range query on the spanfilade.** The granfilade's orgl is used only as an address key (to identify *which* link), not as a storage location for the endset spans themselves.
