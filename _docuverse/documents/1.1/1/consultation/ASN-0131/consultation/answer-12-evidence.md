## Question 12 [evidence]

> Does this region-to-endsets query convert the requested V-region to I-spans via the document's POOM first, then intersect those I-spans against the spanfilade endset index, the same way `find_links` performs its I-address intersection?

## KB Synthesis

Yes, RETRIEVEENDSETS follows the same fundamental V→I→spanfilade pattern as `find_links`, but with several important structural differences.

## The Shared Mechanism

Both operations start with a V-specset, convert it to I-addresses via the document's POOM, then intersect those I-addresses against the spanfilade. This is confirmed directly in [SS-RETRIEVE-ENDSETS]:

> The call chain: `retrieveendsetsfromspanf()` converts the input specset to a **sporglset (V-to-I translation)**, defines three search spaces using ORGLRANGE prefixes (LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3), then for each endset type calls `retrievesporglsetinrange()` which searches the spanfilade with SPANRANGE and ORGLRANGE restrictions.

The V-to-I step uses `specset2sporglset` → `vspanset2ispanset` → `permute()` → `retrieverestricted()`, which walks the document's POOM to produce one I-span per contiguous I-address region [INT-SPORGL-LINK-INDEX]. This is the identical POOM-mediated conversion used by the `find_links` path [SS-FIND-LINKS].

## Differences from `find_links`

| Aspect | `find_links` | RETRIEVEENDSETS |
|--------|-------------|-----------------|
| Spanfilade search dimension | SPANRANGE only (orgl range effectively ignored per [EC-FIND-LINKS-GLOBAL]) | Both SPANRANGE (I-addresses from input) and ORGLRANGE (LINKFROMSPAN/TO/THREE) |
| Returns | Link ISAs | Three resolved V-span specsets (from, to, three endsets) |
| Result conversion | None — raw link IDs | `linksporglset2specset()` converts back to V-coords using the **querying document's docid** |
| Endset perspective | Caller locates links, then follows separately | Returns endpoints already expressed in the querying document's V-space |

## The Critical Docid Rewriting

The last point is the most consequential behavioral difference. RETRIEVEENDSETS resolves the discovered endset I-addresses back to V-positions using the *querying* document's POOM, not the link's home document [INT-SPORGL-LINK-INDEX]. This means if a version shares I-addresses with the original, querying from the version reports endsets with the version's docid — as confirmed empirically in [INT-LINK-VERSION]:

> When queried from a version, endsets report the version's docid rather than the original's.

## Summary

The V-region→I-spans conversion via the document's POOM is confirmed, and those I-spans serve as the SPANRANGE restriction in a spanfilade search — the same mechanism `find_links` uses. RETRIEVEENDSETS extends this with a second ORGLRANGE dimension (endset type selection) and adds a reverse I→V conversion that contextualizes results relative to the querying document.

---

## Code Exploration

Now I have a complete picture. Here is the full answer.

---

## Does `retrieveendsets` Use the Same V→I+Spanfilade Pattern as `findlinksfromtothree`?

**Yes — both paths are structurally identical in their V→I conversion and spanfilade intersection. They differ only in what they extract from the intersection and what post-processing they perform.**

---

### The `retrieveendsets` Execution Path

**Entry point** — `fns.c:350-361`:
```c
bool getretrieveendsets(), doretrieveendsets();
if (getretrieveendsets(taskptr, &specset)
 && doretrieveendsets(taskptr, specset, &fromset, &toset, &threeset))
    putretrieveendsets(taskptr, fromset, toset, threeset);
```

**`doretrieveendsets`** — `do1.c:369-373`: a thin wrapper:
```c
bool doretrieveendsets(typetask *taskptr, typespecset specset, ...)
{
  bool retrieveendsetsfromspanf();
  return retrieveendsetsfromspanf(taskptr, specset, fromsetptr, tosetptr, threesetptr);
}
```

**`retrieveendsetsfromspanf`** — `spanf1.c:190-235` — is where the work happens:

```c
bool retrieveendsetsfromspanf(typetask *taskptr, typespecset specset, ...)
{
  typespan fromspace, tospace, threespace;
  typesporglset sporglset;
  ...
  fromspace.stream.mantissa[0] = LINKFROMSPAN;   // [spanf1.c:210]
  fromspace.width.mantissa[0]  = 1;
  tospace.stream.mantissa[0]   = LINKTOSPAN;     // [spanf1.c:213]
  tospace.width.mantissa[0]    = 1;
  threespace.stream.mantissa[0]= LINKTHREESPAN;  // [spanf1.c:216]
  threespace.width.mantissa[0] = 1;

  if (!(specset2sporglset(taskptr, specset, &sporglset, NOBERTREQUIRED)          // [spanf1.c:222] — step 1: V→I
     && retrievesporglsetinrange(taskptr, sporglset, &fromspace, &fromsporglset) // [spanf1.c:223] — step 2: spanfilade hit
     && linksporglset2specset(taskptr, &((typevspec*)specset)->docisa,           // [spanf1.c:224] — step 3: I→V back
              fromsporglset, fromsetptr, NOBERTREQUIRED)
     && retrievesporglsetinrange(taskptr, sporglset, &tospace, &tosporglset)
     && linksporglset2specset(taskptr, &((typevspec*)specset)->docisa,
              tosporglset, tosetptr, NOBERTREQUIRED)))
        return (FALSE);
  // ... repeat for threespace [spanf1.c:229-233]
```

**Step 1: V→I via POOM** — `sporgl.c:14-65`:

`specset2sporglset` iterates the specset. For a `VSPECID` entry, it calls `vspanset2sporglset` [`sporgl.c:25`], which:
1. Calls `findorgl(taskptr, granf, docisa, &orgl, type)` [`sporgl.c:44`] — fetches the document's POOM from the global granfilade.
2. Calls `vspanset2ispanset(taskptr, orgl, vspanset, &ispanset)` [`sporgl.c:48`] → `permute(taskptr, orgl, vspanset, V, ispansetptr, I)` [`orglinks.c:397-402`].
3. `permute` calls `span2spanset` → `retrieverestricted((typecuc*)orgl, vspan, V, NULL, I, NULL)` [`orglinks.c:435`] — traverses the POOM to map each V-span to its I-span(s).
4. Wraps the resulting I-spans as `SPORGLID` structs tagged with `docisa` [`sporgl.c:50-57`].

**Step 2: Spanfilade intersection** — `spanf1.c:237-267`:

`retrievesporglsetinrange` calls, for each sporgl in the set:
```c
context = retrieverestricted((typecuc*)spanf, (typespan*)sporglptr, SPANRANGE, whichspace, ORGLRANGE, NULL);
```
The **SPANRANGE** key is the I-address from step 1. The **ORGLRANGE** restriction is `whichspace` (the `LINKFROMSPAN`, `LINKTOSPAN`, or `LINKTHREESPAN` range). The function returns all spanfilade crums whose I-address range (SPANRANGE) overlaps the query, restricted to the specific endpoint-type slot on the ORGLRANGE axis.

**Step 3: I→V back-conversion** — `linksporglset2specset` → `sporglset2vspanset` → `findorgl` + `ispan2vspanset` → `permute(I→V)`. The returned specsets are the V-addresses of all link endpoints touching the query region.

---

### The `findlinksfromtothree` Execution Path

**Entry** — `fns.c:189-201` → `do1.c:348-352`:
```c
bool dofindlinksfromtothree(...)
{
  bool findlinksfromtothreesp();
  return findlinksfromtothreesp(taskptr, spanf, fromvspecset, tovspecset, threevspecset, orglrangeptr, linksetptr);
}
```

**`findlinksfromtothreesp`** — `spanf1.c:56-103`:
```c
if (fromvspecset)
    specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED); // [spanf1.c:71] — V→I
if (tovspecset)
    specset2sporglset(taskptr, tovspecset,   &tosporglset,   NOBERTREQUIRED); // [spanf1.c:73]
if (threevspecset)
    specset2sporglset(taskptr, threevspecset,&threesporglset,NOBERTREQUIRED); // [spanf1.c:75]

if (fromvspecset)
    sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN); // [spanf1.c:77]
if (tovspecset)
    sporglset2linkset(taskptr, (typecuc*)spanfptr, tosporglset, &tolinkset, orglrange, LINKTOSPAN);       // [spanf1.c:85]
if (threevspecset)
    sporglset2linkset(taskptr, (typecuc*)spanfptr, threesporglset, &threelinkset, orglrange, LINKTHREESPAN); // [spanf1.c:93]

intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr); // [spanf1.c:100]
```

**Step 1: V→I via POOM** — identical call: `specset2sporglset` → `vspanset2sporglset` → `findorgl` + `vspanset2ispanset` → `permute(V→I)` on the document's POOM. Done once per specset (three times total for from/to/three).

**Step 2: Spanfilade intersection** — `sporglset2linkset` → `sporglset2linksetinrange` — `sporgl.c:239-269`:
```c
prefixtumbler(&orglrange->stream, spantype, &range.stream);  // e.g. LINKFROMSPAN prefix
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, infoptr);
for (c = context; c; c = c->nextcontext) {
    beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);  // extract link ISA from ORGLRANGE
    onlinklist(taskptr, linksetptr, &linksa);
}
```
Same `retrieverestricted(spanf, I-address, SPANRANGE, link-type-range, ORGLRANGE, ...)` call. The difference: it extracts the **ORGLRANGE** offset (link ISA) rather than the SPANRANGE offset (endpoint I-address).

**Step 3: Intersection** — `intersectlinksets` computes `fromlinkset ∩ tolinkset ∩ threelinkset` — links that appear in all three endpoint-type search results.

---

### Side-by-Side Comparison

| | `retrieveendsets` | `findlinksfromtothree` |
|---|---|---|
| **V→I function** | `specset2sporglset` → `vspanset2sporglset` → `findorgl(granf)` + `vspanset2ispanset` | **identical** |
| **POOM call** | `retrieverestricted(orgl, vspan, V, NULL, I, NULL)` in `permute` | **identical** |
| **Spanfilade call** | `retrieverestricted(spanf, I-span, SPANRANGE, endpt-type-range, ORGLRANGE)` | **structurally identical** |
| **Extracted dimension** | SPANRANGE offset → endpoint I-positions, then I→V via POOM | ORGLRANGE offset → link ISAs |
| **Output** | V-address specsets of endpoints touching query region | Link ISA set |
| **V→I conversions** | **One** on the input specset, reused for all three endpoint types | **Three** separate conversions (one per from/to/three specset) |
| **Post-processing** | I→V back-conversion for each endpoint type's result | Set intersection across the three link-ISA lists |

---

### Conclusion

`retrieveendsets` and `findlinksfromtothree` use **the same two-stage mechanism**:

1. **V→I via POOM**: `specset2sporglset` → `vspanset2sporglset` → `findorgl(taskptr, granf, docisa, &orgl)` [`sporgl.c:44`, `granf1.c:17-41`] then `vspanset2ispanset` → `permute` → `retrieverestricted(orgl, V, NULL, I)` [`orglinks.c:397-435`].

2. **I-span intersection against spanfilade**: `retrieverestricted(spanf, I-span, SPANRANGE, endpoint-type-range, ORGLRANGE)` — in `retrievesporglsetinrange` [`spanf1.c:245`] for `retrieveendsets`, and in `sporglset2linksetinrange` [`sporgl.c:259`] for `findlinksfromtothree`.

The difference is in **which axis of the result is read**: `retrieveendsets` reads the SPANRANGE (the I-positions of the endpoints themselves, then converts back to V), while `findlinksfromtothree` reads the ORGLRANGE (the link ISAs that own those endpoints), then intersects three such sets. The V→I POOM translation step is identical in both.
