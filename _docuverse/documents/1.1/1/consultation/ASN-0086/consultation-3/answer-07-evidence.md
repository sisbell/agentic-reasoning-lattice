## Question 7 [evidence]

> When udanax-green resolves whether two links share a type — for example, when answering type-membership queries or matching against a designated retraction type — does it compare type endsets by literal value (endset-sequence equality) or by computed coverage (set-equality on address coverages)?

## KB Synthesis

The KB does not contain direct evidence of a type-membership comparison or retraction-type matching operation, so I can only synthesize from adjacent structural facts.

**What the KB establishes:**

Link types are stored as VSpec references to the bootstrap document's type registry at `1.0.2.x`. When a link is created, its THREE endset is converted via `vspanset2sporglset` to I-spans and indexed in the spanfilade under `LINKTHREESPAN=3` [SS-LINK-ENDPOINT, ST-LINK-CREATE]. All link endpoint operations go through I-address space, not V-span comparison [ST-FIND-LINKS].

The type hierarchy — e.g., MARGIN (`1.0.2.6.2`) nested under FOOTNOTE (`1.0.2.6`) — is designed to be queried via **tumbler address-range containment**, not literal endset equality [SS-LINK-ENDPOINT/Finding 0024]: "type queries like 'find all footnote-family links' via address-range matching." This is coverage-based: a range query on `[1.0.2.6, 1.0.2.7)` would match both FOOTNOTE and MARGIN type endsets.

**The critical limitation:**

The type filter in `find_links` is non-functional — it returns empty even when matching links exist [EC-TYPE-FILTER-NONFUNCTIONAL]. The orgl-range scoping in the spanfilade search is also effectively disabled [EC-FIND-LINKS-GLOBAL]. So the *intended* mechanism (I-address range matching for type hierarchy) cannot be empirically confirmed to work.

**Bottom line:**

The KB strongly points to **I-address coverage matching** (intersection/containment, not literal sequence equality) as the intended design. Literal V-span comparison is inconsistent with how every other endpoint operation works in the system. But because type filtering is broken in the implementation, this answer describes the intended architecture rather than observed behavior.

---

## Code Exploration

I now have a complete, verified picture from the actual source. Here is the full answer.

---

## How udanax-green Resolves Link Type Membership

**Answer: Computed coverage — address-range overlap in the spanfilade. There is no literal endset-sequence comparison anywhere in the type-matching path.**

---

### Data Model

Each link has three endsets — FROM, TO, and THREE. The THREE endset is the "type endset." In the spanfilade, every endset is stored with a prefix digit that encodes its role:

- `LINKFROMSPAN = 1` — from-endset
- `LINKTOSPAN = 2` — to-endset
- `LINKTHREESPAN = 3` — type-endset

These constants are defined in `backend/xanadu.h` (used throughout `spanf1.c`, `sporgl.c`).

---

### Storage: `insertspanf` — spanf1.c:15–54

When a link is created via `docreatelink` (`do1.c:195–221`), its endsets are stored in the spanfilade through `insertendsetsinspanf` (`do2.c:116–128`), which calls `insertspanf` once per endset role. At `spanf1.c:22`:

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```

`prefixtumbler` (`tumble.c:641–651`) shifts the link's own address into subdigit position and inserts `spantype` as the leading mantissa digit. The result is an ORGLRANGE address of the form `3.link_address` for the type-endset. The endset's covered internal-address range is stored as the SPANRANGE key at `spanf1.c:51`:

```c
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
```

So in the spanfilade, a type-endset occupies the 2-D cell:
- **SPANRANGE** = the internal spans the type-endset covers
- **ORGLRANGE** = `3.link_address`

---

### Query: `findlinksfromtothreesp` — spanf1.c:56–103

When a client calls `findlinksfromtothree` (`fns.c:189–202`) with a type specset, the chain is:

```
fns.c:198  dofindlinksfromtothree
do1.c:348  → findlinksfromtothreesp
```

In `findlinksfromtothreesp`, the type specset (third argument) is converted to a sporglset (internal address representation) and then:

```c
sporglset2linkset(taskptr, (typecuc*)spanfptr, threesporglset, &threelinkset,
                  orglrange, LINKTHREESPAN);   // spanf1.c:93
```

---

### Retrieval: `sporglset2linksetinrange` — sporgl.c:239–269

For each internal span of the query type specification, the function builds an ORGLRANGE restriction:

```c
prefixtumbler(&orglrange->stream, spantype, &range.stream);    // sporgl.c:257
prefixtumbler(&orglrange->width, 0, &range.width);             // sporgl.c:258
context = retrieverestricted(spanfptr, (typespan*)sporglset,
           SPANRANGE, &range, ORGLRANGE, (typeisa*)infoptr);   // sporgl.c:259
```

This calls the enfilade's `retrieverestricted` with:
- **SPANRANGE** query: the internal address range of the type-endset being matched against
- **ORGLRANGE** restriction: the LINKTHREESPAN prefix band (`3.0…` to `4.0…`)

`retrieverestricted` returns all enfilade crums whose SPANRANGE **overlaps** the query range and whose ORGLRANGE falls within the prefix band. Link addresses are extracted from the returned contexts at `sporgl.c:264`:

```c
beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
onlinklist(taskptr, linksetptr, &linksa);
```

This is **interval overlap on address coverage** — the enfilade's native operation — not sequence equality.

---

### Intersection: `intersectlinksets` — spanf2.c:46–120

After separately collecting the three candidate link-address sets (from-endset matches, to-endset matches, type-endset matches), the system intersects them at `spanf2.c:98` and `spanf2.c:109–110`:

```c
if (tumblereq(&temp1->address, &temp2->address))  { … }

if (tumblereq(&temp1->address, &temp2->address)
 && tumblereq(&temp2->address, &temp3->address)) { … }
```

`tumblereq` (`tumble.c:24–36`) is a field-by-field comparison of tumbler structs. **It is comparing link addresses** (which link objects appear in all three result sets) — not endset sequences.

---

### `acceptablevsa` is a stub — do2.c:110–113

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

No type validation is performed at the VSA level. The only filter is the spanfilade coverage query above.

---

### Summary

| Stage | Function | File:Lines | Comparison |
|---|---|---|---|
| Endset storage | `insertspanf` | spanf1.c:22,51 | No comparison; stores coverage range keyed by prefixed address |
| Type query dispatch | `findlinksfromtothreesp` | spanf1.c:93 | Passes LINKTHREESPAN to retrieval |
| Retrieval filter | `sporglset2linksetinrange` | sporgl.c:257–259 | **Interval overlap** via `retrieverestricted` on SPANRANGE ∩ ORGLRANGE |
| Result intersection | `intersectlinksets` | spanf2.c:98,109 | Literal tumbler equality on **link addresses** only |

**Two links share a type if and only if their type-endsets have overlapping address coverage with the query type specification.** The system never compares endset sequences directly. The enfilade's address-range retrieval mechanism is the sole arbiter of type membership — it is set-equality on address coverages, not endset-sequence equality.
