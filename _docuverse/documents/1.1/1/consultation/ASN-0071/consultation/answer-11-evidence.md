## Question 11 [evidence]

> When FINDDOCSCONTAINING receives a vspec-set, does it first resolve V-addresses to I-spans via the caller's POOM before querying the spanfilade, and what happens if the caller's POOM has no entry for part of the input vspec?

## KB Synthesis

## FINDDOCSCONTAINING: V-to-I Resolution and Missing POOM Entries

### Yes — V-addresses are resolved via the caller's POOM first

FINDDOCSCONTAINING follows the same two-phase pattern documented for RETRIEVEENDSETS and FINDLINKS [SS-RETRIEVE-ENDSETS, SS-FIND-LINKS]:

1. The input vspec-set is converted to an I-span set via the caller's document POOM — using `specset2ispanset` → `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted`
2. Those I-addresses are used to query the DOCISPAN sub-index of the spanfilade [SS-DOCISPAN]

The intermediate representation is sporgls carrying both the I-address origin and the source document ISA [SS-SPORGL, SS-VSPAN-TO-SPORGL].

### What happens when the POOM has no entry for part of the vspec

`retrieverestricted` returns NULL for any V-position that has no POOM mapping [SS-FOLLOWLINK / Finding 0048]. Those positions are **silently dropped** — no I-addresses are generated for the missing ranges, and no error is raised. The operation proceeds using only the I-addresses that were successfully resolved.

This is consistent with [EC-SEARCH-SPEC-BEYOND-BOUNDS]: when a search spec references positions that no longer exist in the V-stream, `find_links` (same conversion path) does not error — it intersects with whatever content remains.

The formal property from [INV-ITOV-FILTERING] captures the general principle, though it's stated for I-to-V direction: all operations that pass through the `span2spanset`/`retrieverestricted` path silently filter out unresolvable addresses.

### Consequence: stale results possible

Because the spanfilade is write-only [INV-SPANF-WRITE-ONLY], FINDDOCSCONTAINING may return documents that once contained the I-addresses but whose POOM no longer maps them — even if the I-addresses resolved successfully from the caller's POOM [EC-STALE-SPANF-REFERENCE, INT-DELETE-SPANF-DIVERGENCE]. The result is a superset: `actual_docs(i) ⊆ find_documents(i)`.

---

## Code Exploration

I now have all the source verified. Here is the complete answer.

---

## FINDDOCSCONTAINING: V→I Resolution and Missing POOM Entries

### Question 1: Does FINDDOCSCONTAINING resolve V-addresses to I-spans via a POOM before querying the spanfilade?

**Yes, unconditionally.** The V→I conversion is the first thing `dofinddocscontaining` does, before the spanfilade is ever touched.

**Call chain:**

```
finddocscontaining          [fns.c:20]
  → dofinddocscontaining    [do1.c:15]
      → specset2ispanset     [do2.c:14]   ← V→I conversion
      && finddocscontainingsp [spanf1.c:151] ← spanfilade query (only if conversion succeeded)
```

`dofinddocscontaining` uses short-circuit `&&` evaluation `[do1.c:20-22]`:

```c
// do1.c:20-23
return (
   specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
&& finddocscontainingsp (taskptr, ispanset, addresssetptr));
```

If V→I conversion fails, the spanfilade is never queried.

**The conversion path through `specset2ispanset` [do2.c:14]:**

For each item in the spec-set, the function branches on type. For `VSPECID` items `[do2.c:27]`:

```c
// do2.c:34-38
if (!(
  findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
&& (ispansetptr = vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr)))){
       return (FALSE);
}
```

- `findorgl` `[do2.c:35]` looks up the **document's own ORGL** (its granfilade node) using `docisa` from the vspec — this is the POOM for that document.
- `vspanset2ispanset` `[do2.c:36]` calls `permute(V→I)` `[orglinks.c:401]`, which iterates each V-span calling `span2spanset` `[orglinks.c:415]`, which calls `retrieverestricted` on the ORGL `[orglinks.c:435]` to perform the actual V-address lookup.

**Clarification on "caller's POOM":** The POOM used is not the calling session's POOM. It is the POOM belonging to the document identified by `docisa` embedded in each vspec item. The granfilade (`granf`) maps document addresses to their ORGLs; `findorgl` fetches the ORGL for `vspec->docisa` specifically.

`ISPANID` items in the spec-set are passed through without conversion `[do2.c:24-26]` — a spec-set can mix I-spans and V-spans; the V-spans are resolved while I-spans are used directly.

---

### Question 2: What happens when the POOM has no entry for part of the input vspec?

There are **two distinct failure modes** depending on which lookup fails.

---

#### Case A: The document itself is not found in the granfilade

`findorgl` `[granf1.c:17]` calls `checkforopen(isaptr, type, user)` `[granf1.c:22]`. If the document is not open/accessible, `checkforopen` returns ≤0 and `findorgl` returns `FALSE` `[granf1.c:35]`. Similarly, if `fetchorglgr` returns a NULL ORGL `[granf1.c:39-40]`, `findorgl` returns `FALSE`.

This propagates immediately up the `&&` chain:
- `findorgl` → FALSE `[granf1.c:35 or 40]`
- `specset2ispanset` → `return (FALSE)` `[do2.c:37]`
- `dofinddocscontaining` → FALSE `[do1.c:20-22]`
- `finddocscontaining` → `putrequestfailed (taskptr)` `[fns.c:30-31]`

**Result: the entire request fails immediately.**

---

#### Case B: The document ORGL is found, but a specific V-span has no POOM mapping

In `span2spanset` `[orglinks.c:425]`, `retrieverestricted` is called on the ORGL with the V-span as the restriction:

```c
// orglinks.c:435
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                             (typespan*)NULL, targindex, (typeisa*)NULL);
```

If the V-span does not appear in the POOM, `retrieverestricted` returns `NULL`. The code then:

```c
// orglinks.c:439-448
for (c = context; c; c = c->nextcontext) {   // loop body never executes
    context2span (c, ...);
    nextptr = (typespan *) onitemlist (...);
}
if (!context) {
    return (targspansetptr);   // return accumulator pointer unchanged
}
```

The for-loop doesn't iterate. The `if(!context)` check at `[orglinks.c:446]` returns `targspansetptr` unchanged `[orglinks.c:447]` — the unresolvable V-span contributes **no I-spans** to the output set.

`permute` then continues to the next span in the restriction set `[orglinks.c:414]`. Processing continues silently.

The partial I-span set (containing only the successfully-resolved spans) is passed to `finddocscontainingsp` `[spanf1.c:151]`, which queries the spanfilade and **always returns `TRUE`** `[spanf1.c:187]` regardless of how many matches it finds — including zero.

**Result: the unmapped V-span is silently dropped. No error is returned. `finddocscontaining` sends back whatever documents contain the *successfully-resolved* I-spans, with no indication that part of the query was unresolvable.**

---

### Summary Table

| Scenario | Where it fails | Return path | Client sees |
|---|---|---|---|
| Document `docisa` not open/accessible | `findorgl` `[granf1.c:35]` | `putrequestfailed` `[fns.c:31]` | REQUEST FAILED |
| Document in granfilade but `fetchorglgr` → NULL | `findorgl` `[granf1.c:40]` | `putrequestfailed` `[fns.c:31]` | REQUEST FAILED |
| Document found; V-span not in POOM | `retrieverestricted` → NULL `[orglinks.c:435]`; `if(!context)` `[orglinks.c:446]` | Silent omission, processing continues | Partial results, TRUE |

The design draws a hard line between "document not accessible" (a protocol error) and "V-address not mapped" (a silent empty set). The latter is treated as a normal case, not a fault — `span2spanset` at `[orglinks.c:446-448]` is the gate that absorbs the missing entries without propagating any error.
