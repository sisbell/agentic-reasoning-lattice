## Question 20 [evidence]

> If the from-set, to-set, or third-set content is transcluded (COPY) into additional documents after link creation, does FINDLINKSFROMTOTHREE surface the same links through the newly shared I-addresses, and is the returned set stable under REARRANGE that preserves those I-addresses?

## KB Synthesis

**Part 1: Post-creation transclusion extends discoverability**

Yes. FINDLINKSFROMTOTHREE operates entirely in I-address space via the spanfilade — it converts the search specset to I-addresses and checks for intersection with indexed endpoint I-addresses [SS-SPANF-OPERATIONS], [SS-FIND-LINKS]. COPY (vcopy) preserves I-addresses exactly: the destination POOM acquires the same I-addresses as the source [ST-VCOPY], [INV-IADDR-IMMUTABILITY]. The spanfilade is write-only and accumulates entries monotonically [INV-SPANF-WRITE-ONLY] — it is never modified by the COPY itself, but once the new document's POOM contains those I-addresses, searching it converts to the same I-addresses that the link was indexed under at creation time, and the intersection succeeds.

This is confirmed directly: "Transclusion creates shared content identity… the only link-relevant effect is sharing I-addresses, which enables link discovery from the destination document" [INT-LINK-TRANSCLUSION (Finding 0028)]. The timing of the transclusion relative to link creation is irrelevant — the spanfilade index is keyed on I-addresses, not on which documents existed at link creation time.

**Part 2: Stability under REARRANGE**

Yes. REARRANGE modifies only V-address displacements in the POOM (`cdsp.dsas[V]`); I-addresses are never touched [INV-REARRANGE-IDENTITY (Finding 0056)]. The spanfilade is likewise untouched — REARRANGE is in the granf-preserving operation class [FC-CONTENT-SPANF-ISOLATION]. Since find_links converts V-spans to I-addresses before searching, and REARRANGE preserves the complete multiset of I-addresses in every document, the I-address intersection produces identical results before and after any REARRANGE [INV-REARRANGE-LINK-SURVIVAL].

**One caveat on endset representation:** REARRANGE that reorders content already covered by a link's endset can cause endset fragmentation — the same link may appear with duplicated or fragmented V-spans in find_links results [EC-PIVOT-LINK-FRAGMENTATION]. The *set* of link ISAs returned is stable; the *endset geometry* within each result may not be.

---

## Code Exploration

I have enough to write a full, citation-backed answer.

---

## Full Answer

### The Claim: Yes, FINDLINKSFROMTOTHREE surfaces links through newly shared I-addresses, and the result is stable under REARRANGE.

---

### 1. How link end-sets are stored at creation time

`docreatelink` (`do1.c:195–221`) converts the caller's V-spec sets to I-spans before indexing. The chain is:

**`docreatelink` → `specset2sporglset` → `vspanset2sporglset`** (`sporgl.c:35–65`):

```c
if (!findorgl(taskptr, granf, docisa, &orgl, type)) return(NULL);
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);  // V → I via granfilade
    ...
    movetumbler(docisa,          &sporglset->sporgladdress);  // source doc ISA
    movetumbler(&ispanset->stream, &sporglset->sporglorigin); // I-stream
    movetumbler(&ispanset->width,  &sporglset->sporglwidth);  // I-width
```

The resulting sporgl set (I-spans tagged with their home document ISA) is passed to `insertendsetsinspanf` → `insertspanf` (`spanf1.c:15–53`):

```c
movetumbler(&sporglset->sporglorigin, &lstream);  // I-span stream is SPANRANGE key
...
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

Where `crumorigin.dsas[ORGLRANGE]` is the link ISA prefixed with `LINKFROMSPAN` / `LINKTOSPAN` / `LINKTHREESPAN`.

**Result: the spanfilade indexes each link by the I-spans of its end-set content, not by V-addresses.**

---

### 2. What COPY (transclusion) does to the I-address landscape

`docopy` (`do1.c:45–65`):

```c
specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)   // source V → same I-spans
&& insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)       // new V→I entry in target doc's granfilade
&&  insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)   // record: target doc contains these I-spans
```

`insertpm` (`orglinks.c:75–134`) adds a crum to the target document's permutation matrix whose:
- `crumorigin.dsas[I]` = the same I-span as the original content
- `crumorigin.dsas[V]` = the new V-address in the target document

COPY does **not** add new `LINKFROMSPAN`/`LINKTOSPAN`/`LINKTHREESPAN` entries to the spanfilade. The existing link index entries (keyed by I-spans) remain unchanged and are now reachable from both documents.

---

### 3. How FINDLINKSFROMTOTHREE resolves the query

`findlinksfromtothreesp` (`spanf1.c:56–103`) calls `specset2sporglset` on the query's V-spec sets. This calls `vspanset2sporglset` (`sporgl.c:35–65`) which uses `vspanset2ispanset` to convert the **queried document's** V-spans to I-spans via its granfilade — the same V→I resolution used at link-creation time.

Then `sporglset2linkset` (`sporgl.c:222–237`) → `sporglset2linksetinrange` (`sporgl.c:239–269`) calls:

```c
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                              &range, ORGLRANGE, (typeisa*)infoptr);
```

where `range` is the ORGLRANGE prefixed with the desired end-set type (`LINKFROMSPAN`, etc.).

Critically, the homedoc filtering is **explicitly disabled** (`sporgl.c:251–255`):

```c
if (FALSE/*trying to kluge links followable thru versions */
    && ((typeitemheader *)sporglset)->itemid == SPORGLID) {
    infoptr = &linfo;
    movetumbler(&((typesporgl*)sporglset)->sporgladdress, &linfo.homedoc);
  } else
    infoptr = NULL;  // ← always taken
```

The `FALSE&&...` permanently disables the version-filtering path. `infoptr` is always `NULL`. The lookup is a pure I-span match across the entire link ISA space.

**Consequence:** When you issue FINDLINKSFROMTOTHREE with a V-spec pointing into Document B (which transcluded the content from Document A), `vspanset2ispanset` resolves Document B's V-spans to the same I-spans as Document A's content. The spanfilade lookup returns the same links — because the links were indexed by those I-spans, not by which document you query through.

There is also a secondary note at the top-level dispatcher (`fns.c:198`): the `homeset` (orglrange) parameter is passed as `NULL`:

```c
dofindlinksfromtothree(taskptr, fromvspecset, tovspecset, threevspecset,
                        (typeispan*)NULL/*homeset*/, &linkset)
```

`sporglset2linkset` substitutes a `nullhomeset` with `width.mantissa[0] = 100` (`sporgl.c:226–232`), effectively spanning all link ISA space. There is no restriction on which documents' links are surfaced.

---

### 4. REARRANGE stability

`dorearrange` (`do1.c:34–43`) → `rearrangepm` (`orglinks.c:137–142`) → `rearrangend(docorgl, cutseqptr, V)` (`edit.c:78–160`):

```c
tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
                              // ^^^^ index = V — only V-dimension is modified
```

`rearrangend` adjusts only `cdsp.dsas[V]` — the V-displacement of each crum. The `cdsp.dsas[I]` dimension (I-address) is never touched. I-addresses are structurally invariant under REARRANGE.

After REARRANGE, the granfilade maps new V-addresses to the same I-spans. When FINDLINKSFROMTOTHREE runs with the updated V-addresses, `vspanset2ispanset` resolves them via the updated granfilade to the same I-spans, and `sporglset2linksetinrange` finds the same spanfilade entries. The returned link set is identical.

The question's qualifier "REARRANGE that preserves those I-addresses" is therefore unconditionally satisfied — all REARRANGE operations preserve I-addresses, by the V-only axis constraint in `rearrangend`.

---

### Summary of the data flow

| Operation | Spanfilade effect | I-span effect |
|---|---|---|
| `docreatelink` | Adds `LINKFROMSPAN`/`LINKTOSPAN`/`LINKTHREESPAN` entries keyed by I-spans | None |
| `docopy` (transclusion) | Adds `DOCISPAN` entry for target doc; updates target granfilade | Same I-spans now accessible via new V-addresses in target doc |
| `rearrangend` (REARRANGE) | None — spanfilade untouched | None — I-addresses unchanged |
| `findlinksfromtothreesp` | Reads spanfilade by I-span | Resolves query V-spans → I-spans first |

**FINDLINKSFROMTOTHREE surfaces the same links through transcluded copies** because it converts V-specs to I-spans before searching, and the spanfilade is indexed by I-span. **The returned set is stable under REARRANGE** because REARRANGE operates exclusively on the V-axis, leaving both I-addresses and spanfilade link entries unchanged.
