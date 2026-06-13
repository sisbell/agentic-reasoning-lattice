## Question 11 [evidence]

> When the system is asked which link endsets touch a given V-region, are the returned endsets emitted as sets of I-address spans (or V-spans after I→V conversion), and never as the link identities they belong to?

## KB Synthesis

Yes — RETRIEVEENDSETS returns endset content as **V-spans** (specsets), never as link identities. Here is the full breakdown.

## RETRIEVEENDSETS returns specsets, not link ISAs

[SS-RETRIEVE-ENDSETS] documents the call chain precisely:

1. The input specset (a V-region) is converted to I-addresses via `specset2sporglset()`
2. Three ORGLRANGE subspaces are searched in the spanfilade: `LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3`
3. Results from `retrievesporglsetinrange()` are converted back to V-addresses via `linksporglset2specset()` — using the **querying document's docid**, not the link's home document

The output is three specsets (from-endset, to-endset, three-endset), each expressed as V-spans in the querying document's address space.

The link identities themselves are **never emitted**. The contrast with FINDLINKSFROMTOTHREE is direct:

| Aspect | FINDLINKSFROMTOTHREE | RETRIEVEENDSETS |
|--------|----------------------|-----------------|
| Input | specset (content region) | specset (content region) |
| Lookup | spanfilade search | spanfilade search |
| Returns | **link ISAs** | **endset specsets** |
| Resolution | — | querying doc's POOM |

## The I→V conversion is the critical step

[INV-ITOV-FILTERING] establishes that this I→V conversion is universal and filtering: unreferenced I-addresses (no current V-position mapping in the querying document's POOM) are **silently dropped** from the result. `span2spanset()` calls `retrieverestricted()` against the POOM; NULL returns cause silent omission [SS-FOLLOWLINK].

This means the returned V-spans reflect only those endset I-addresses that currently have a position in the querying document — they are never raw I-spans passed through verbatim.

## Docid rewriting is implicit

[INT-LINK-VERSION] (Finding 0019) shows an observable consequence: when querying a version, the returned endset specsets report the **version's docid**, not the original document's, even though the link was created against the original. The V-address conversion is always performed relative to the context of the query, not the context of link creation.

## Why link identities are absent

The spanfilade stores `(I-address → link ISA)` entries [SS-SPANF-OPERATIONS], so the link ISAs are consulted internally during the search. But `retrieveendsetsfromspanf()` traverses from I-address matches to the associated link orgls and then reads out the endset I-addresses — it is performing endset resolution, not link enumeration. The caller receives the resolved content locations, not the ISAs used to find them.

To obtain link identities from the same V-region, the caller must use FINDLINKSFROMTOTHREE instead, which returns the link ISA set directly.

---

## Code Exploration

Now I have every piece I need. Here is the complete answer.

---

## Answer

There are two distinct FEBE operations that find things "touching a V-region." They return completely different data types. Reading the code precisely:

---

### `RETRIEVEENDSETS` — returns endset spans, not link identities

**Call chain:** `retrieveendsets` [fns.c:350–362] → `doretrieveendsets` [do1.c:369–374] → `retrieveendsetsfromspanf` [spanf1.c:190–235]

Inside `retrieveendsetsfromspanf` [spanf1.c:190]:

```c
bool retrieveendsetsfromspanf(typetask *taskptr, typespecset specset, typespecset *fromsetptr, typespecset *tosetptr, typespecset *threesetptr)
{
    ...
    specset2sporglset (taskptr, specset, &sporglset, NOBERTREQUIRED)
    && retrievesporglsetinrange(taskptr,sporglset,&fromspace,&fromsporglset)
    && linksporglset2specset (taskptr,&((typevspec *)specset)->docisa, fromsporglset, fromsetptr, NOBERTREQUIRED)
    && retrievesporglsetinrange (taskptr, sporglset, &tospace, &tosporglset)
    && linksporglset2specset (taskptr, &((typevspec*)specset)->docisa, tosporglset, tosetptr, NOBERTREQUIRED)
```

`fromspace`, `tospace`, `threespace` are set using the spantype constants `LINKFROMSPAN`, `LINKTOSPAN`, `LINKTHREESPAN` [spanf1.c:210–217], so the spanfilade retrieval (`retrievesporglsetinrange`) finds the endset I-address records stored at those type positions. The link ISA is in the ORGLRANGE index of the spanfilade — it is used internally for the lookup, but is **not** included in the output.

#### I→V conversion in `linksporglset2specset` [sporgl.c:97–123]

For each sporgl found:

```c
if (iszerotumbler (&((typesporgl *)sporglset)->sporgladdress)) {
    ((typeitemheader *)specset)->itemid = ISPANID;       // raw I-span
    movetumbler(&sporglset->sporglorigin, &ispan->stream);
    movetumbler(&sporglset->sporglwidth,  &ispan->width);
} else {
    linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);
```

`linksporglset2vspec` [sporgl.c:127–137] sets `itemid = VSPECID` and calls `sporglset2vspanset` [sporgl.c:141–176], which calls `ispan2vspanset` → `permute(taskptr, orgl, &ispan, I, vspansetptr, V)` in `orglinks.c` — the I-address range is mapped to V-space before it goes into the result.

**Result type is `typespecset`: a linked list of either `ISPANID` or `VSPECID` items — endset span data only.**

#### Serialization: `putretrieveendsets` [putfe.c:356–362]

```c
int putretrieveendsets(typetask *taskptr, typespecset fromset, typespecset toset, typespecset threeset)
{
    putnumber (taskptr->outp, RETRIEVEENDSETS);
    putitemset (taskptr, (typeitemset)fromset);
    putitemset (taskptr, (typeitemset)toset);
    putitemset (taskptr, (typeitemset)threeset);
}
```

`putitem` [putfe.c:143–180] has only these cases:

```c
case ISPANID:  xuputc ('s', outfile); putspan(...)      // I-span
case VSPANID:  putspan(...)                             // V-span
case VSPECID:  xuputc ('v', outfile); puttumbler(docisa); putitemset(vspanset)
case TEXTID:   puttext(...)
case ADDRESSID: puttumbler(&((typeaddress*)itemptr)->address)
default:       error(...)
```

There is no path through which a link identity enters the output of `RETRIEVEENDSETS`. The switch has no handling for `LINKID` as a standalone case, and link ISAs are consumed internally by `retrievesporglsetinrange` / `sporglset2linksetinrange` and never placed into the `fromset`/`toset`/`threeset` specsets.

---

### `FINDLINKSFROMTOTHREE` — returns link identities, not endset spans

By contrast, `findlinksfromtothree` [fns.c:189–202] → `dofindlinksfromtothree` [do1.c:348–353] → `findlinksfromtothreesp` [spanf1.c:56–103] → `sporglset2linkset` [sporgl.c:222–237] → `sporglset2linksetinrange` [sporgl.c:239–269] returns a `typelinkset` — a list of link ISAs extracted via:

```c
beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
onlinklist (taskptr, linksetptr, &linksa);
```

These items carry `itemid = LINKID`, and `LINKID` is defined as an alias for `ADDRESSID` [xanadu.h:33]:

```c
#define ADDRESSID 5
#define LINKID ADDRESSID
```

Serialized by `putfindlinksfromtothree` [putfe.c:283–288] via `putitem` → `case ADDRESSID: puttumbler(...)` — emitting raw tumbler addresses (link ISAs), no endset content.

---

### Summary

The two operations are complementary and strictly separated at the type level:

| Operation | Takes | Returns | Wire type |
|-----------|-------|---------|-----------|
| `RETRIEVEENDSETS` | V-specset (a V-region) | from/to/three endset **spans** | `ISPANID` (I-span) or `VSPECID` (V-spans after `permute` I→V) |
| `FINDLINKSFROMTOTHREE` | V-specsets per role | **link ISAs** | `ADDRESSID` (raw tumblers) |
| `FOLLOWLINK` | link ISA + end index | endset **spans** | same `ISPANID`/`VSPECID` as above, via same `linksporglset2specset` |

For `RETRIEVEENDSETS` — the operation that answers "which link endsets touch this V-region?" — **yes, the emitted result is exclusively endset spans: either raw I-address spans (when `sporgladdress` is zero [sporgl.c:105–114]) or V-spans produced by I→V conversion via `ispan2vspanset` → `permute` [sporgl.c:157, orglinks.c]. Link identities are never included in the output.** The link ISA lives in the ORGLRANGE dimension of the spanfilade and is used only as a lookup key inside `retrievesporglsetinrange`; it is stripped before the result is built.
