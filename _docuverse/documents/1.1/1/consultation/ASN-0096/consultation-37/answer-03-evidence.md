## Question 3 [evidence]

> Does udanax-green's link-discovery mechanism (the index/lookup structures querying link endsets) admit link addresses as query inputs, or is the query domain restricted to content addresses?

## KB Synthesis

The query domain is restricted to permascroll content addresses. Link orgls ISAs are not valid query inputs.

**The spanf index structure**

The `spanf` enfilade is keyed by permascroll I-addresses and maps them to link ISAs [SS-SPANF-OPERATIONS, SS-DUAL-ENFILADE]:

```
SpanEnfilade = Map<permascroll_IAddress, Set<LinkISA>>
```

When a link is created, `insertendsetsinspanf` indexes the *endpoint content's* I-addresses — derived from `vspanset2sporglset` which converts V-spans to sporgls carrying permascroll origins — as keys. The link's own ISA is a *value* in this map, not a key [ST-CREATE-LINK, SS-SPORGL].

**Why link ISAs are not query inputs**

`find_links` works by converting the query specset to permascroll I-addresses, then performing set intersection against the spanf index [SS-FIND-LINKS]. [INT-LINK-RETRIEVAL] states this explicitly:

> "This only works with permascroll I-addresses from the text subspace (1.x). Searching with link ISAs from 2.x is meaningless — link orgls are not indexed by other link ISAs."

The two I-address sorts are structurally disjoint: permascroll addresses (content-bearing, shared via transclusion) vs. link orgl ISAs (unique identity tokens, stored in the element subspace of their home document) [SS-CONTENT-IDENTITY, Finding 0009]. The spanf contains no entries keyed by link ISAs, so a search using a link ISA as the query span would return an empty intersection [PRE-FIND-LINKS, Finding 0069].

**The lookup path for known link ISAs**

When you *have* a link ISA and want its endsets, the correct operation is FOLLOWLINK — which goes directly to the link orgl in `granf` via `findorgl`, bypassing the spanf entirely [SS-FOLLOWLINK]. This is a different code path from `find_links`.

In summary: the spanf is a content-identity index (`permascroll_addr → links`), and link discovery is strictly content-address-driven. Link ISAs appear only as output values, never as query keys.

---

## Code Exploration

I now have everything needed to answer with full source citations. Here is my complete analysis:

---

## Does the Link-Discovery Mechanism Admit Link Addresses as Query Inputs?

**Short answer:** No. The spanfilade-based link-discovery mechanism (`findlinksfromtothree`) operates exclusively on content addresses. Link addresses are *outputs* of that mechanism, never inputs. The complementary operation — querying by link address — uses a structurally separate mechanism (granfilade/POOM) that bypasses the spanfilade entirely.

---

### 1. The Spanfilade Storage Layout

The key constants (`xanadu.h:36-39`):
```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```

When a link is created, `docreatelink` (`do1.c:195-220`) calls `insertendsetsinspanf` → `insertspanf` (`spanf1.c:15-54`) for each endpoint. Inside `insertspanf`:

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);  // spanf1.c:22
// ...for each sporgl:
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);            // spanf1.c:49
movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);              // spanf1.c:50
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);  // spanf1.c:51
```

This reveals the 2D spanfilade layout for each link endpoint entry:

| Axis | Value | Meaning |
|---|---|---|
| `ORGLRANGE` | `LINKFROMSPAN.linkISA` (i.e. `1.linkISA`) | which endpoint of which link |
| `SPANRANGE` | I-span of endpoint content | permascroll address of referenced content |
| 2D crum bottom info (homedoc) | docISA of the endpoint content source | provenance document |

The link ISA is stored in `ORGLRANGE` (as output), and the endpoint content is stored in `SPANRANGE` (as key).

A separate entry is made by `docopy` (called from `docreatelink` at `do1.c:212`) via `insertspanf` with `DOCISPAN=4`:
- `ORGLRANGE` = `4.docISA` (the home document)
- `SPANRANGE` = the link ISA's permascroll I-span (the link itself as a one-unit I-range)

This DOCISPAN entry is queried only by `finddocscontainingsp` (the "which documents contain this content" path), not by link discovery.

---

### 2. The Link-Discovery Mechanism: `findlinksfromtothree`

Entry path: `findlinksfromtothree` (`fns.c:189`) → `dofindlinksfromtothree` (`do1.c:348-352`) → `findlinksfromtothreesp` (`spanf1.c:56-103`).

```c
bool findlinksfromtothreesp(typetask *taskptr, typespanf spanfptr,
    typespecset fromvspecset, typespecset tovspecset, typespecset threevspecset, ...)
{
    if (fromvspecset)
        specset2sporglset (taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);  // spanf1.c:71
    // ...
    sporglset2linkset (taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset,
                       orglrange, LINKFROMSPAN);  // spanf1.c:77
```

The input specsets are `typespecset`, which can contain:
- `ISPANID` — raw permascroll I-spans (content addresses)
- `VSPECID` — `(docISA, vspanset)` pairs: virtual addresses inside a named document

`specset2sporglset` (`sporgl.c:14-33`) converts these: for `VSPECID` it calls `vspanset2sporglset` → `vspanset2ispanset`, traversing the document's POOM to yield I-space content coordinates.

`sporglset2linksetinrange` (`sporgl.c:239-269`) then queries the spanfilade:
```c
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                             &range, ORGLRANGE, (typeisa*)infoptr);  // sporgl.c:259
// ...
beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);  // sporgl.c:264 — strips endpoint-type prefix
onlinklist (taskptr, linksetptr, &linksa);                 // sporgl.c:265 — collects link ISA
```

`retrieverestricted` (`retrie.c:56-85`) → `retrieveinarea` → `findcbcinarea2d` (`retrie.c:229-268`): finds 2D spanfilade crums where:
- `SPANRANGE` overlaps the query sporgl (the content I-address)
- `ORGLRANGE` falls in the endpoint-type range (e.g. `1.x` for LINKFROMSPAN)

The result: the ORGLRANGE coordinates of matching crums — i.e., `LINKFROMSPAN.linkISA` values — are stripped of their prefix and collected as link ISAs.

**The query domain is entirely content addresses.** Link ISAs are the output extracted from `ORGLRANGE`.

---

### 3. The Link Traversal Mechanism: `followlink`

Entry path: `followlink` (`fns.c:114`) → `dofollowlink` (`do1.c:223-232`) → `link2sporglset` (`sporgl.c:67-95`).

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
    return (
       link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)  // do1.c:229
    && linksporglset2specset (...));
}
```

```c
bool link2sporglset(typetask *taskptr, typeisa *linkisa, typesporglset *sporglsetptr,
                    INT whichend, int type)
{
    if (!findorgl (taskptr, granf, linkisa, &orgl, type)) ...    // sporgl.c:77 — uses granf, not spanf
    tumblerincrement (&zero, 0, whichend, &vspan.stream);         // sporgl.c:81
    tumblerincrement (&zero, 0/*1*/, 1, &vspan.width);            // sporgl.c:82
    if (context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, NULL)) {  // sporgl.c:83
```

This is the structural inverse:
- Input: a link ISA (`linkisaptr`)  
- Mechanism: `findorgl(granf, linkISA)` — looks up the link's own orgl in the **granfilade**, not the spanfilade
- Query: `retrieverestricted(orgl, &vspan[whichend], V, NULL, I, NULL)` — queries the link's POOM for V-position `whichend` (0.1 = FROM, 0.2 = TO, 0.3 = THREE) and retrieves the corresponding I-spans of endpoint content
- Output: the content specset at that endpoint

This mechanism never touches the spanfilade. It navigates the link's internal POOM structure directly, using the fixed V-addresses set by `setlinkvsas` (`do2.c:169-183`):
```c
tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);  // do2.c:172 — FROM at 0.1.1
tumblerincrement (tovsaptr, 0, 2, tovsaptr);       // do2.c:175 — TO at 0.2.1
tumblerincrement (threevsaptr, 0, 3, threevsaptr); // do2.c:179 — THREE at 0.3.1
```

---

### 4. Can a Link Address Appear as Query Input to the Spanfilade?

Indirectly, yes — but not for link discovery. Because a link in udanax-green IS a document (it has its own orgl in the granfilade), a link ISA can be used as the `docISA` field of a `VSPECID` in a specset. If you supply V-spans in the 0.1.x range, `vspanset2ispanset` would traverse the link's POOM to resolve those to the I-spans of the link's own FROM endpoint content. Then `sporglset2linksetinrange` would search the spanfilade for *other links* whose endpoints overlap that same content.

This is not querying for the link itself — it's using the link as an indirect handle to navigate to the content it references, then using that content address as the actual query. The link ISA never appears as a SPANRANGE key in this path.

The only place the link ISA appears as a SPANRANGE key in the spanfilade is from the `DOCISPAN=4` entries created by `docopy` (`do1.c:212` → `insertspanf` with `DOCISPAN`). Those entries are indexed under `ORGLRANGE = 4.docISA` and are queried only by `finddocscontainingsp` for the "find documents" operation — not by the link-discovery mechanism.

---

### 5. Structural Summary

The two index structures implement mutually inverse operations:

| Mechanism | Index | Query domain | Output |
|---|---|---|---|
| `findlinksfromtothree` (link discovery) | Spanfilade | Content address (I-span or V-spec) | Link ISAs from ORGLRANGE |
| `followlink` (link traversal) | Granfilade / link POOM | Link ISA (direct) | Content I-spans from POOM V-slots |

**The query domain of the link-discovery mechanism is restricted to content addresses.** A link ISA cannot be directly submitted to the spanfilade as a discovery query. To start from a known link address and reach other links, you must first traverse the granfilade to extract the endpoint content, then submit that content to the spanfilade. The two index structures are structurally asymmetric and are navigated in opposite directions.
