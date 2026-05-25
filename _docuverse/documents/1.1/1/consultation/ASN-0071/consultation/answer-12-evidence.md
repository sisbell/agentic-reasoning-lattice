## Question 12 [evidence]

> Does FINDDOCSCONTAINING return a document if ANY portion of the queried I-spans overlaps a DOCISPAN entry, or does it require full coverage of the input span?

## KB Synthesis

**Any overlap suffices.** FINDDOCSCONTAINING is an intersection-based search, not a containment check.

The evidence comes from the shared spanfilade mechanism and explicit behavioral observations:

**Same search mechanism as find_links.** [SS-SPANF-OPERATIONS] establishes that `finddocscontainingsp` and `findlinksfromtothreesp` both query the spanfilade using interval intersection. [SS-FIND-LINKS] makes the overlap semantics explicit for find_links: "partial overlap suffices — a search specset that shares even one I-address with a link endpoint will discover that link." FINDDOCSCONTAINING uses `retrieveendsetsfromspanf` / `retrieverestricted` through the same code path.

**Behavioral confirmation.** [INV-IADDRESS-PERMANENT] (Finding 0023) shows the direct case:

```
After delete("Findable" from Dest):
  find_documents("Findable") → [Source, Dest]   # still 2 documents
```

Dest is returned even though "Findable" was deleted from its V-stream. The DOCISPAN entry spans the queried I-address range partially (the original insertion range), and that partial overlap is sufficient. [EC-STALE-SPANF-REFERENCE] reinforces this: `find_documents(i)` returns a superset — `actual_docs(i) ⊆ find_documents(i)` — because any stored DOCISPAN entry overlapping `i` triggers inclusion.

**Index granularity.** [SS-DOCISPAN] (Finding 0047) models the index as `Map<ISpan, DocISA>` where each entry records a contiguous range. The underlying `retrieverestricted` interval comparison ([SS-INTERVAL-CMP]) classifies addresses as TOMYLEFT / THRUME / TOMYRIGHT etc. — returning any entry where the queried range intersects the stored range, not only when the stored range is fully covered.

---

## Code Exploration

I have all the evidence needed. Here is the complete answer.

---

## FINDDOCSCONTAINING: Overlap, Not Full Coverage

**The answer is: ANY overlap is sufficient.** Full coverage of the input span is not required. A document is returned if any portion of any queried I-span overlaps a DOCISPAN entry in the spanfilade.

---

### Call Chain

```
FINDDOCSCONTAINING (FEBE command)
  → finddocscontaining()           [fns.c:20]
  → dofinddocscontaining()         [do1.c:15]
  → finddocscontainingsp()         [spanf1.c:151]
  → retrieverestricted()           [retrie.c:56]
  → retrieveinarea()               [retrie.c:87]
  → findcbcinarea2d()              [retrie.c:229]
  → crumqualifies2d()              [retrie.c:270]  ← where the match test lives
```

---

### Step 1: Specset → Ispanset → Spanfilade Query

`dofinddocscontaining` [do1.c:15–23] converts the input V-spec to an I-span set and passes it on:

```c
return (
   specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
&& finddocscontainingsp (taskptr, ispanset, addresssetptr));
```

`finddocscontainingsp` [spanf1.c:165–182] constructs a `docspace` filter that limits results to DOCISPAN entries (value `4` [xanadu.h:39], distinguished from LINKFROMSPAN=1, LINKTOSPAN=2), then iterates over each input I-span:

```c
tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);  // [spanf1.c:168]
tumblerincrement (&docspace.width, 0, 1, &docspace.width);           // [spanf1.c:169]
for (; ispanset; ispanset = ispanset->next) {
    context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE,
                                   ispanset, SPANRANGE, (typeisa*)NULL);  // [spanf1.c:171]
```

The spanfilade is 2D:
- **ORGLRANGE axis** (index 0 [wisp.h:15]): document identity space — filtered to DOCISPAN entries
- **SPANRANGE axis** (index 1 [wisp.h:16]): I-span space — searched against the input query span

Each matching context yields a document address; duplicates are suppressed by `isinlinklist` [spanf1.c:175].

---

### Step 2: The Matching Predicate — `crumqualifies2d`

The actual per-node test is `crumqualifies2d` [retrie.c:270–305]. It checks both axes independently. For the SPANRANGE axis (the input query I-span vs the stored DOCISPAN I-span):

```c
// Is the query span entirely to the LEFT of this crum? (no overlap)
endcmp = iszerotumbler (span2end) ? TOMYRIGHT
       : whereoncrum (crumptr, offset, span2end, index2);          // [retrie.c:292]
if ( endcmp < ONMYLEFTBORDER)/* <= was < 12/20/84 */ {
    return(FALSE);   // query ends strictly left of stored span     // [retrie.c:293–295]
}

// Is the query span entirely to the RIGHT of this crum? (no overlap)
startcmp = whereoncrum (crumptr, offset, span2start, index2);      // [retrie.c:297]
if( (startcmp > THRUME)) {
    return (FALSE);  // query starts at or after stored span end    // [retrie.c:298–300]
}
```

The constants [common.h:86–90]:
```
TOMYLEFT       = -2   (strictly left of interval)
ONMYLEFTBORDER = -1   (at left border)
THRUME         =  0   (strictly inside)
ONMYRIGHTBORDER=  1   (at right border)
TOMYRIGHT      =  2   (strictly right of interval)
```

**This is a pure overlap test.** A node qualifies unless:
- The query span ends strictly before the stored span's left border (`endcmp < -1` = TOMYLEFT only), OR
- The query span starts at or after the stored span's right border (`startcmp > 0` = ONMYRIGHTBORDER or TOMYRIGHT)

Any partial overlap — including touching the left border — passes the filter.

---

### The 12/20/84 Border-Touch Edit

There is a significant comment at [retrie.c:293]:

```c
if ( endcmp < ONMYLEFTBORDER)/* <= was < 12/20/84 */
```

This says: before 12 December 1984 the condition was `<= ONMYLEFTBORDER` (stricter — a query span ending *exactly on* a stored span's left border would be excluded). The change to `< ONMYLEFTBORDER` made **touching count as overlap**. A query span that ends at the exact start of a DOCISPAN entry now returns that document.

The ORGLRANGE axis uses `<=` [retrie.c:283], but because `docspace` always has width 1, that edge case is inconsequential in practice.

---

### Summary

| Behavior | Result |
|----------|--------|
| Query I-span fully contains stored DOCISPAN | Match |
| Query I-span partially overlaps stored DOCISPAN | Match |
| Query I-span touches stored DOCISPAN left border | Match (post-12/20/84) |
| Query I-span entirely to the left of stored DOCISPAN | No match |
| Query I-span starts at or beyond stored DOCISPAN right border | No match |
| Multiple input spans in ispanset | Each tested independently; results accumulated |

**FINDDOCSCONTAINING returns a document if ANY portion of ANY queried I-span overlaps (or touches) a DOCISPAN entry. Full coverage of the input span by the stored I-span is never checked, nor is full coverage of the stored I-span by the query.**
