## Question 5 [evidence]

> What do udanax-green's link-query operations (find-links-from-to, follow-link, retrieve-endsets) return — link tumbler addresses, spans/spec-sets, or both — and how do results denote endset contents?

## KB Synthesis

## Link Query Return Types

### FINDLINKSFROMTOTHREE — returns link ISA tumblers

The search operation converts input specsets to I-addresses, intersects them against the spanfilade, and returns a **list of link ISA tumblers** (link identifiers). No span data is returned at this stage — only the addresses of matching link orgls. [SS-FIND-LINKS, SS-SPANF-OPERATIONS]

The paginated variant FINDNEXTNLINKSFROMTOTHREE returns the same type with a count and a cursor (itself a link ISA tumbler). FINDNUMOFLINKSFROMTOTHREE returns only the count. [SS-PAGINATE-LINKS]

### FOLLOWLINK — returns a specset (V-address spans)

Given a link ISA tumbler and an endpoint selector (1=FROM, 2=TO, 3=THREE), FOLLOWLINK reads the link orgl's stored I-spans, then converts them to V-address spans using a caller-specified **home document**'s POOM. The result is a **specset** of V-spans in that document's address space. [SS-FOLLOWLINK, SS-FOLLOW-LINK]

The home document context is essential: the same link can yield different V-spans (or empty) depending on which document's POOM is queried. If an endset I-address has no mapping in the home document's POOM, it is silently dropped — producing a partial or empty result without error. [INV-ITOV-FILTERING, EC-GHOST-LINK]

The returned specset reflects the link's **permanent** endpoint as created, not filtered to the discovery context: `follow_link(L, SOURCE) == L.source_specset` regardless of how the link was found. [SS-FOLLOW-LINK]

### RETRIEVEENDSETS — returns three specsets

Given an input specset (a content region), RETRIEVEENDSETS searches the spanfilade by I-address and returns **three specsets simultaneously**: from-endset, to-endset, and three-endset. All three are expressed as V-address spans resolved through the **querying document**'s context (not the link's home document). [SS-RETRIEVE-ENDSETS]

This differs from FOLLOWLINK in its input and resolution perspective:

| Aspect | FOLLOWLINK | RETRIEVEENDSETS |
|--------|-----------|-----------------|
| Input | Link ISA + endpoint selector | Specset (content region) |
| Lookup | Link orgl directly | Spanfilade search |
| Returns | One endset as specset | All three endsets as specsets |
| V-resolution | Caller-specified home doc | Querying document's docid |

### How endset contents are denoted internally

Endsets are stored internally as **sporglsets** — sets of sporgls, each carrying an I-address origin, a width, and a source document ISA. [SS-SPORGL, SS-LINK-ENDPOINT Finding 0037]

A single user-visible V-span input to `create_link` can produce **multiple sporgls** in the stored endset when the V-span covers content transcluded from multiple sources (non-contiguous I-address regions). The cardinality of the stored endset equals the number of contiguous I-address runs in the endpoint content, not the number of V-spans provided. [ST-LINK-CREATE Finding 0037]

When endsets are retrieved (via either FOLLOWLINK or RETRIEVEENDSETS), the sporglset is converted back to V-spans via `linksporglset2specset`, which resolves each sporgl's I-address through the specified document's POOM. Each resolvable sporgl contributes one V-span entry to the returned specset. [SS-FOLLOWLINK, SS-RETRIEVE-ENDSETS]

### Summary

- `find_links` → **link ISA tumblers**
- `follow_link(link_id, endpoint, home_doc)` → **specset** (V-spans in home_doc's space)
- `retrieve_endsets(specset)` → **three specsets** (from/to/three, in querying doc's space)
- Internal endset representation: **sporglsets** (I-address spans with document provenance)
- Returned endset representation: **specsets** (V-address spans, context-dependent)

---

## Code Exploration

Now I have everything I need. Here is the full analysis:

---

## What Link-Query Operations Return in udanax-green

### Overview

There are three link-query operations. Each operates on a different input and returns a different type:

| Operation | Command | Input | Returns |
|---|---|---|---|
| `find_links` | 30 | SpecSet (content to search) | List of link tumbler **addresses** |
| `follow_link` | 18 | Link ISA + whichend | One **SpecSet** (content in that endset) |
| `retrieve_endsets` | 28 | SpecSet (link atoms) | Three **SpecSets** (from, to, type) |

---

### 1. `find_links` — Returns Link Tumbler Addresses

**Call chain:**
- `fns.c:189` `findlinksfromtothree` → `do1.c:348` `dofindlinksfromtothree` → `spanf1.c:56` `findlinksfromtothreesp`

`findlinksfromtothreesp` converts each non-null specset to a sporglset via `specset2sporglset` (`sporgl.c:14`), then queries the spanfilade for links whose endsets intersect the given content:

```c
// spanf1.c:76-99
sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset,
                  orglrange, LINKFROMSPAN);
// ...then intersect fromlinkset, tolinkset, threelinkset
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
```

`sporglset2linkset` (`sporgl.c:222-237`) queries the spanfilade for the ORGLRANGE dimension, then strips the span-type prefix off each result via `beheadtumbler` (`sporgl.c:264`) to recover the bare link ISA.

The result type is `typelinkset` — a linked list of `typelink` (alias `typeaddress`) structs, each holding a `.address` field (a tumbler). `typelink` is defined at `xanadu.h:106-107`:

```c
typedef typeaddress typelink;
typedef typelink * typelinkset;
```

**Wire output** (`putfe.c:283-288`): command code `30~`, then `putitemset`, where each `ADDRESSID` item (`xanadu.h:33`, `LINKID == ADDRESSID`) is written as a plain tumbler (`putfe.c:172-174`):

```c
case ADDRESSID:
    puttumbler(outfile, &((typeaddress *)itemptr)->address);
    break;
```

**Python client** (`client.py:754-757`): reads N tumblers and returns a list of `Address` objects.

**Conclusion:** `find_links` returns **only link tumbler addresses** — the ISAs of the matching link atoms. No span/spec-set content.

---

### 2. `follow_link` — Returns a SpecSet of Endset Content

**Call chain:**
- `fns.c:114-127` `followlink` → `do1.c:223` `dofollowlink`

```c
// do1.c:223-231
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
    return (
       link2sporglset(taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset(taskptr, &((typesporgl *)sporglset)->sporgladdress,
                             sporglset, specsetptr, NOBERTREQUIRED));
}
```

**`link2sporglset`** (`sporgl.c:67-95`): Looks up the link atom's POOM enfilade via `findorgl`, then queries it in the V-dimension at the position corresponding to `whichend`:

```c
// sporgl.c:80-83
tumblerincrement(&zero, 0, whichend, &vspan.stream);  // V position = 0.whichend
tumblerincrement(&zero, 0, 1, &vspan.width);           // width = 0.1
context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, NULL);
```

The three endsets live at V-positions `0.1` (LINK_SOURCE=1), `0.2` (LINK_TARGET=2), `0.3` (LINK_TYPE=3) inside the link's own POOM. These positions were assigned during creation by `setlinkvsas` (`do2.c:169-183`).

Each `retrieverestricted` context result is converted to a sporgl (I-address + home-doc) via `contextintosporgl` (`sporgl.c:205-220`), selecting the I-dimension.

**`linksporglset2specset`** (`sporgl.c:97-123`): Converts sporglset to specset. For each sporgl:

```c
// sporgl.c:105-117
if (iszerotumbler(&((typesporgl*)sporglset)->sporgladdress)) {
    // No home doc — emit raw I-span
    ((typeitemheader*)specset)->itemid = ISPANID;
    movetumbler(&sporglset->sporglorigin, &((typeispan*)specset)->stream);
    movetumbler(&sporglset->sporglwidth, &((typeispan*)specset)->width);
} else {
    // Has home doc — emit VSpec (doc address + V-spans via I→V permutation)
    linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);
}
```

`linksporglset2vspec` → `sporglset2vspanset` → `ispan2vspanset` → `permute` (`orglinks.c:389-422`): performs the I→V coordinate transformation through the document's POOM enfilade.

**Wire output** (`putfe.c:339-343`):
```
18~  <count>~  [s~ <start>~ <width>~ | v~ <docisa>~ <count>~ [<start>~ <width>~]...]  ...
```

- `s~` = ISPANID (raw I-span: start tumbler + width tumbler)
- `v~` = VSPECID (doc ISA tumbler + nested itemset of V-spans)

**Python client** (`client.py:760-766`): returns a `SpecSet` containing `Span` objects (I-spans) or `VSpec` objects (doc + V-spans).

**Conclusion:** `follow_link` returns a **SpecSet of content-addressing spans** — V-spans expressed as VSpecs when a home document is known, raw I-spans otherwise. **Not** link addresses.

---

### 3. `retrieve_endsets` — Returns Three SpecSets

**Call chain:**
- `fns.c:350-362` `retrieveendsets` → `do1.c:369` `doretrieveendsets` → `spanf1.c:190` `retrieveendsetsfromspanf`

```c
// spanf1.c:190-235
bool retrieveendsetsfromspanf(typetask *taskptr, typespecset specset,
    typespecset *fromsetptr, typespecset *tosetptr, typespecset *threesetptr)
```

Input: a specset that identifies link atoms by their V-position in a document (typically V-addresses in the `0.x` link subspace). This is the **inverse** of `follow_link` — given the link's location in the document, retrieve all three endsets at once.

The function:
1. Converts input specset to sporglset via `specset2sporglset` (`sporgl.c:14`)
2. For each of three span-type bands in the spanfilade:

```c
// spanf1.c:209-218
fromspace.stream.mantissa[0] = LINKFROMSPAN;   // = 1
fromspace.width.mantissa[0]  = 1;
tospace.stream.mantissa[0]   = LINKTOSPAN;     // = 2
threespace.stream.mantissa[0] = LINKTHREESPAN; // = 3
```

3. Calls `retrievesporglsetinrange` (`spanf1.c:237-267`) for each band — this queries the spanfilade for all ORGLRANGE entries whose SPANRANGE overlaps the input sporgl and falls within the given span-type band
4. Converts each resulting sporglset back to a specset via `linksporglset2specset`

**Wire output** (`putfe.c:356-362`):
```
28~  <count>~ [...fromset...]  <count>~ [...toset...]  <count>~ [...threeset...]
```

Three consecutive `putitemset` calls for from, to, and three/type endsets.

**Note — bug in `put.c:229`** (non-FEBE interactive mode only): `putretrieveendsets` at `put.c:229` writes `toset` instead of `threeset` for the third section. The FEBE protocol path in `putfe.c:356-362` is correct and outputs all three distinct sets.

**Python client** (`client.py:740-745`): reads three `SpecSet` objects:
```python
def retrieve_endsets(self, specset):
    self.xc.command(28, specset)
    sourcespecs = self.xc.SpecSet()
    targetspecs = self.xc.SpecSet()
    typespecs   = self.xc.SpecSet()
    return sourcespecs, targetspecs, typespecs
```

---

### How Endset Contents Are Denoted

All three operations share the same SpecSet wire encoding (`putfe.c:124-141`, `putfe.c:143-180`):

Each SpecSet is preceded by a count. Each item in the set is one of:

| Wire flag | Type | Fields | Meaning |
|---|---|---|---|
| `s~` | ISPANID | `<stream>~ <width>~` | Raw I-span: start + width tumblers in I-space |
| `v~` | VSPECID | `<docisa>~ <count>~ [<stream>~ <width>~]...` | VSpec: document ISA + list of V-spans |
| (plain tumbler) | ADDRESSID/LINKID | `<tumbler>~` | Link address (only in `find_links` output) |

**VSpec** is the normal endset representation. It binds a document ISA to a set of V-spans within that document, expressing "this range of visible content in this document version." The V-spans are recovered by I→V permutation through the POOM enfilade (`orglinks.c:404`, `permute`).

**I-span** appears when `sporgladdress` is zero — the home document context was not recorded. In that case, the endset is expressed directly in I-space (permascroll coordinates) without a document binding.

---

### Architectural Relationship

The two storage structures divide the responsibilities:

- **Spanfilade** (global): maps (I-span, span-type) → link ISA. Used by `find_links` (search by content → links) and `retrieve_endsets` (search by link position → content).
- **Link POOM** (per-link): maps V-position (0.1/0.2/0.3) → I-spans of endset content. Used by `follow_link` (given link ISA → content).

Both structures are populated simultaneously during `docreatelink` (`do1.c:195-221`) by `insertendsetsinorgl` and `insertendsetsinspanf` (`do2.c:116-148`).
