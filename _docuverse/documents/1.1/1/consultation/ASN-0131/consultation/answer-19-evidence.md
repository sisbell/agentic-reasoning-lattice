## Question 19 [evidence]

> Is the region-to-endsets search global across all documents — like `find_links` where the orgl range is ignored via the `TRUE||!homeset` override — or does it honor the home-document scope of the queried region?

## KB Synthesis

## RETRIEVEENDSETS Search Scope: Global

The region-to-endsets search is **global across all documents**, but the mechanism differs from the `find_links` bug.

### How the search works

`RETRIEVEENDSETS` searches through `retrieveendsetsfromspanf()`, which:

1. Converts the input specset to a sporglset (V-to-I translation)
2. Defines three ORGLRANGE prefixes: `LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3`
3. Calls `retrievesporglsetinrange()` per endpoint type with both SPANRANGE and ORGLRANGE restrictions

[SS-RETRIEVE-ENDSETS], [INT-SPORGL-LINK-INDEX]

### Why it's global — and why it's different from `find_links`

`find_links` is global because of a code bug: `sporglset2linkset()` contains `TRUE||!homeset` which always fires, replacing the caller's orgl range with a hardcoded width-100 range from zero. [EC-FIND-LINKS-GLOBAL]

`RETRIEVEENDSETS` is global **by design**: its ORGLRANGE dimension is consumed entirely for endpoint-type selection (from=1 / to=2 / three=3), not for home-document scoping. There is simply no bucket in the ORGLRANGE hierarchy used to partition by home document. Any link endpoint — in any document — whose type matches and whose I-addresses intersect the queried region is returned. [SS-RETRIEVE-ENDSETS]

### What is document-scoped: only the output

The one document-aware step is output resolution: `linksporglset2specset()` converts result I-addresses back to V-addresses using the **querying document's** docid. [SS-RETRIEVE-ENDSETS]

This means endsets are expressed relative to the querying context, not the link's home document. But this is a presentation transformation applied after the global search completes — it does not narrow the search itself.

### Summary

| Dimension | `find_links` | `RETRIEVEENDSETS` |
|-----------|-------------|-------------------|
| SPANRANGE (I-address) | Filters correctly | Filters correctly |
| ORGLRANGE (orgl scope) | Ignored via `TRUE\|\|` bug | Used for endpoint-type selection |
| Home-document filter | None (bug) | None (by design) |
| Output resolution | N/A | Querying document's docid |

Both operations return results from all documents that share content identity with the queried region, but `RETRIEVEENDSETS` achieves this through the deliberate use of ORGLRANGE for endpoint-type partitioning, leaving no room for a home-document constraint. [SS-SPANF-OPERATIONS], [EC-FIND-LINKS-GLOBAL]

---

## Code Exploration

Now I have the complete picture. I've traced both code paths through `retrieveendsets` and `findlinksfromtothree` down to the spanfilade retrieval layer. Let me write the full answer.

---

## Answer: Region-to-Endsets Is Global — But For Different Reasons Than `find_links`

Both operations search the entire spanfilade without home-document scoping. The mechanisms differ.

---

### Code Path: `retrieveendsets`

**`fns.c:350-362`** — top-level handler:
```c
void retrieveendsets(typetask *taskptr)
{
  typespecset specset, fromset, toset, threeset;
  bool getretrieveendsets(), doretrieveendsets();

    if (
       getretrieveendsets (taskptr, &specset)
    && doretrieveendsets (taskptr, specset, &fromset, &toset, &threeset)){
        putretrieveendsets (taskptr, fromset, toset, threeset);
     }else
        putrequestfailed (taskptr);
}
```
No `homeset` is ever extracted from the wire or passed downstream. The function signature carries no scope parameter.

**`do1.c:369-374`** — dispatch:
```c
bool doretrieveendsets(typetask *taskptr, typespecset specset, typespecset *fromsetptr, typespecset *tosetptr, typespecset *threesetptr)
{
  bool retrieveendsetsfromspanf();
     return retrieveendsetsfromspanf(taskptr, specset, fromsetptr, tosetptr, threesetptr);
}
```
Again, no scope parameter.

**`spanf1.c:190-235`** — the actual spanfilade query:
```c
bool retrieveendsetsfromspanf(typetask *taskptr, typespecset specset, ...)
{
  typespan fromspace, tospace, threespace;
  ...
  fromspace.stream.mantissa[0] = LINKFROMSPAN;
  fromspace.width.mantissa[0] = 1;

  tospace.stream.mantissa[0] = LINKTOSPAN;
  tospace.width.mantissa[0] = 1;
  ...
  specset2sporglset (taskptr, specset, &sporglset, NOBERTREQUIRED)
  && retrievesporglsetinrange(taskptr, sporglset, &fromspace, &fromsporglset)
  && linksporglset2specset (taskptr, &((typevspec *)specset)->docisa, fromsporglset, fromsetptr, NOBERTREQUIRED)
  ...
}
```

The `fromspace` / `tospace` / `threespace` spans are pure link-type ranges (LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3, each with width=1). They identify **which endpoint type** to look for, not which document owns the link.

**`spanf1.c:237-267`** — `retrievesporglsetinrange`:
```c
context = retrieverestricted(
    (typecuc*)spanf,
    (typespan*)sporglptr,  /* query region in SPANRANGE */
    SPANRANGE,
    whichspace,            /* LINKFROMSPAN/TO/THREE — type band, not doc band */
    ORGLRANGE,
    (typeisa*)NULL         /* ← no home-doc filter */
);
```

The `NULL` for the homeisa argument passes through to `retrieverestricted` with no document-level restriction. The comment at `spanf1.c:245` acknowledges the intentionality:
```c
/* kluge to make links show thru to version &sporglptr->sporgladdress */
```

The ORGLRANGE restriction (`whichspace`) covers the full link-type band across every document in the spanfilade. Because `insertspanf` keys entries as `prefixtumbler(linkisa, spantype, &crumorigin.dsas[ORGLRANGE])` (`spanf1.c:22`), a `fromspace = {LINKFROMSPAN, width=1}` restriction matches **all** links of that type regardless of their document ISA.

**Result: `retrieveendsets` returns endsets from every document in the store.**

---

### Code Path: `findlinksfromtothree` (for comparison)

**`fns.c:197-198`**:
```c
   getfindlinksfromtothree (taskptr, &fromvspecset, &tovspecset, &threevspecset, &homeset)
&& dofindlinksfromtothree (taskptr, fromvspecset, tovspecset, threevspecset, (typeispan*)NULL/*homeset*/, &linkset))
```

The FEBE wire protocol delivers a `homeset`, but it is **explicitly discarded** — replaced with `(typeispan*)NULL` — before `dofindlinksfromtothree` is called. The commented-out name `/*homeset*/` is a fossil showing the original design intent.

Even if a non-NULL `homeset` were passed through, it would be overridden at **`sporgl.c:227`**:
```c
int sporglset2linkset(..., typeispan *homeset, ...)
{
  typeispan nullhomeset;

    *linksetptr = NULL;
    if (TRUE||!homeset) {           /* ← hardcoded override */
        tumblerclear (&nullhomeset.stream);
        tumblerclear (&nullhomeset.width);
        nullhomeset.width.mantissa[0] = 100;  /* orgl range 0..100 */
        nullhomeset.next = NULL;
        homeset = &nullhomeset;
    }
    for (; homeset; homeset = homeset->next) {
        sporglset2linksetinrange (taskptr, spanfptr, sporglset, linksetptr, homeset, spantype);
    }
}
```

The `TRUE||!homeset` condition is always true. The synthesized `nullhomeset` covers orgls 0 through 100 — effectively the entire populated namespace.

---

### Architectural Distinction

| | `retrieveendsets` | `findlinksfromtothree` |
|---|---|---|
| Home-doc parameter in FEBE? | No | Yes (parsed but discarded at `fns.c:198`) |
| Home-doc parameter in `do` layer? | No | Yes (accepted but received as NULL) |
| Override mechanism | `NULL` homeisa to `retrieverestricted` (`spanf1.c:245`) | `TRUE||!homeset` in `sporglset2linkset` (`sporgl.c:227`) |
| Scope | Global (all docs) | Global (all docs) |

**`retrieveendsets` was never architected for home-doc scoping.** No parameter for it exists at any layer — not in `fns.c`, `do1.c`, or `spanf1.c`. The `NULL` to `retrieverestricted` is structural.

**`findlinksfromtothree` was partially architected for home-doc scoping** — the wire protocol and do-layer accept the parameter — but it is disabled in two places: discarded at the FEBE handler (`fns.c:198`) and overridden inside the spanfilade query function itself (`sporgl.c:227`). This is an unfinished implementation.

One notable asymmetry: `findnumoflinksfromtothree` at `fns.c:213` passes `homeset` through instead of nulling it:
```c
&& dofindnumoflinksfromtothree (taskptr, fromvspecset, tovspecset, threevspecset, homeset, &numberoflinks))
```
But since `sporgl.c:227` contains `TRUE||!homeset`, that non-NULL value is still overridden. The inconsistency between `findlinksfromtothree` (nulls it) and `findnumoflinksfromtothree` (passes it) is evidence the codebase is mid-refactor — the `TRUE||` was probably inserted as a temporary global override and never removed.

**Conclusion:** The region-to-endsets search (`retrieveendsets`) is **global across all documents**. It honors no home-document scope. This is not an override of existing scoping logic (as in `find_links`) but a structural absence — the parameter never existed in the `retrieveendsets` stack.
