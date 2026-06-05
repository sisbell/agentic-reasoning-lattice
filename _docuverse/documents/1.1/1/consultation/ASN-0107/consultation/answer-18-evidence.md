## Question 18 [evidence]

> When content is transcluded via COPY into a new document, does the count for a from/to/type query against that new document's V-span increase because the shared I-addresses now overlap additional spanfilade endset entries?

## KB Synthesis

**Yes, the count increases — and the mechanism is pure I-address intersection, not new spanfilade entries.**

When COPY places content into the new document, `docopy` does two things [SS-DOCISPAN, Finding 0036]:
1. Updates the destination POOM via `insertpm` — mapping new V-positions to the source's existing I-addresses
2. Creates DOCISPAN entries in the spanfilade via `insertspanf(..., DOCISPAN)` — making content findable via `find_documents`

Crucially, step 2 writes DOCISPAN entries (document-content index), **not** new link endset entries. The link endset entries were written to the spanfilade when the link was originally created via `insertendsetsinspanf` [SS-SPANF-OPERATIONS, Finding 0012].

The count increase happens because `find_links` / FINDNUMOFLINKSFROMTOTHREE converts the query V-span to I-addresses and intersects against the spanfilade link index [SS-FIND-LINKS, Finding 0028]:

```
find_links(S) = { L | I-addresses(S) ∩ I-addresses(L.endpoint) ≠ ∅ }
```

Since COPY shares I-addresses (not copies them), the new document's V-span now maps to I-addresses already indexed as link endpoints. The spanfilade finds those pre-existing entries.

This is the stated interaction property [INT-LINK-TRANSCLUSION, Finding 0004, 0028]: "When content with a link is transcluded to another document, the link can be found from the copy." FINDNUMOFLINKSFROMTOTHREE is a wrapper that executes the full `findlinksfromtothreesp()` search and counts results [SS-FIND-LINKS, Finding 0035] — so it sees the same expanded result set.

**Summary:** The spanfilade link index doesn't grow. The new document's POOM grows (new V→I mappings), and those I-addresses happen to intersect pre-existing link endset entries in the spanfilade, causing the query count to increase.

---

## Code Exploration

I now have everything needed for a complete, precise answer. Here it is:

---

## Answer: COPY Does Not Increase the from/to/type Query Count — But the Mechanism Is Critical to Understand

### Setup: what docopy does to the spanfilade

`docopy` [do1.c:45-65] performs two writes:

```c
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)       // do1.c:60
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)   // do1.c:62
```

`insertpm` writes V→I mappings into the destination document's POOM (orgl), so the new V-span in the destination document resolves to the same permascroll I-addresses as the source.

`insertspanf(DOCISPAN=4)` [spanf1.c:15-54] writes crums into the global spanfilade with:
- `ORGLRANGE = prefixtumbler(docisaptr, 4, ...)` — the destination document ISA prefixed with `4`
- `SPANRANGE = lstream` — the shared I-span range

### The spanfilade's strict ORGLRANGE prefix partition

From `xanadu.h` and `tumble.c:641-651`:

```c
#define LINKFROMSPAN    1    // xanadu.h:36
#define LINKTOSPAN      2    // xanadu.h:37
#define LINKTHREESPAN   3    // xanadu.h:38
#define DOCISPAN        4    // xanadu.h:39
```

```c
int prefixtumbler(tumbler *aptr, INT bint, tumbler *cptr)
{
    tumblerclear(&temp1);
    temp1.mantissa[0] = bint;          // first component = integer prefix
    movetumbler(aptr, &temp2);
    if (!iszerotumbler(&temp2))
        temp2.exp -= 1;                // shift isa down one level
    tumbleradd(&temp1, &temp2, cptr);  // result = (bint . isa)
}
```

Every entry in the global spanfilade is keyed on ORGLRANGE by `prefixtumbler(isa, type)`. This creates four numerically non-overlapping regions:

| Type | ORGLRANGE region |
|------|-----------------|
| LINKFROMSPAN=1 | `[1.0, 2.0)` |
| LINKTOSPAN=2 | `[2.0, 3.0)` |
| LINKTHREESPAN=3 | `[3.0, 4.0)` |
| DOCISPAN=4 | `[4.0, 5.0)` |

These regions are disjoint by construction. A tumbler comparison (`tumblercmp`) between any two entries in different regions always separates them.

### The from/to/type query path

`dofindnumoflinksfromtothree` [do1.c:355] → `findnumoflinksfromtothreesp` [spanf1.c:105] → `findlinksfromtothreesp` [spanf1.c:56] → `sporglset2linkset` [sporgl.c:222] → `sporglset2linksetinrange` [sporgl.c:239].

Inside `sporglset2linksetinrange` [sporgl.c:256-259]:

```c
prefixtumbler(&orglrange->stream, spantype, &range.stream);
prefixtumbler(&orglrange->width, 0, &range.width);
context = retrieverestricted(spanfptr,
    (typespan*)sporglset, SPANRANGE,   // restrict I-span axis to query I-spans
    &range, ORGLRANGE,                 // restrict ORGLRANGE to spantype prefix
    (typeisa*)infoptr);
```

The `spantype` passed here is always `LINKFROMSPAN=1`, `LINKTOSPAN=2`, or `LINKTHREESPAN=3` (from `findlinksfromtothreesp` [spanf1.c:77, 85, 93]). The ORGLRANGE constraint therefore falls in `[1.x, 1.x+width)`, `[2.x, ...]`, or `[3.x, ...]` — all numerically below `4.0`.

DOCISPAN crums sit at ORGLRANGE ≥ `4.0`. `retrieverestricted` returns only crums within the specified range; DOCISPAN crums are structurally unreachable from these queries. After `retrieverestricted` returns, `beheadtumbler` [tumble.c:673] strips the prefix to recover the link ISA [sporgl.c:264] — but DOCISPAN crums are never reached to be beheaded.

**The DOCISPAN entries written by COPY are therefore invisible to from/to/type link count queries. The count does not increase due to them.**

### What does happen after COPY

The question hints at a related effect that *is* real. After `docopy`:

1. The destination document's POOM contains V→I mappings for the transcluded V-span, pointing to the **same permascroll I-addresses** as the source document's corresponding content.

2. When a from/to/type query is issued against the destination document's V-span, `specset2sporglset` [sporgl.c:14] → `vspanset2sporglset` [sporgl.c:35] uses the destination document's POOM to convert V→I, yielding those shared I-addresses.

3. `sporglset2linksetinrange` searches the spanfilade with these I-addresses under LINKFROMSPAN (or TO or THREE). It finds any existing link-endpoint crums that already indexed those I-addresses — the same crums that would have been found querying the original document's corresponding V-span.

The count against the new document's V-span therefore equals the count against the equivalent content in the original document. Not because DOCISPAN entries leaked into the query, but because both POOMs resolve to the same I-space, and link associations are stored in I-space under prefixes 1–3.

### Note: orgl range is ignored anyway

Finding 0069 documents that `sporglset2linkset` [sporgl.c:227] contains `if (TRUE||!homeset)` — the `TRUE||` short-circuits the condition unconditionally, so even the `orglrange` document-scoping parameter is discarded and replaced with a `width=100` full-space range. The ORGLRANGE restriction that actually works is only the `spantype` prefix enforced in `sporglset2linksetinrange` [sporgl.c:257-259]. This makes the partition by prefix the only real filter — and it is reliable, because the four prefix values (1, 2, 3, 4) are hardcoded constants that are numerically ordered and never overlap.

### Direct answer to the question

**No.** COPY adds DOCISPAN entries (prefix `4`) to the global spanfilade. The from/to/type query restricts ORGLRANGE to the prefix of the requested endpoint type (1, 2, or 3 via `sporglset2linksetinrange`). DOCISPAN entries are numerically outside those ranges and are never returned. The count does not increase because of them.

What COPY *does* do: it installs V→I mappings in the destination document's POOM. Those mappings cause the from/to/type query against the new document's V-span to discover the same link endpoints that are discoverable from the original document's equivalent content — because both paths converge on the same I-addresses in permascroll space, and LINKFROMSPAN/TO/THREE entries in the spanfilade are keyed on I-addresses, not on which document currently holds that content.
