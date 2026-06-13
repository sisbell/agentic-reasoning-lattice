## Question 17 [evidence]

> Are endset I-addresses that are no longer referenced by any current POOM (DEL5 / ghost-link spans) silently filtered during I→V conversion the way RETRIEVEENDSETS and FOLLOWLINK filter them, and if so does an endset ever come back empty or partial from this query?

## KB Synthesis

Yes, they are silently filtered, and yes, endsets come back empty or partial as a direct consequence.

## The Filtering Mechanism

[INV-ITOV-FILTERING] establishes this as a **universal invariant** of the I→V conversion layer, not operation-specific behavior. Both FOLLOWLINK and RETRIEVEENDSETS share the identical call chain:

```
linksporglset2specset()
  → sporglset2vspanset()
    → ispan2vspanset() → permute() → span2spanset()
      → retrieverestricted()   ← the filter point
```

At `span2spanset()` (`orglinks.c:446-448`), `retrieverestricted()` searches the queried document's POOM for each I-address. If the POOM has no mapping for that address — because the content was deleted — `retrieverestricted()` returns NULL and the I-address is **dropped from the result set with no error, no flag, and no indication to the caller**.

The formal invariant: `∀ op returning V-addresses: v ∈ result(op) → ∃ d, i : poom.d(v) = i`. Nothing that fails this test appears in the output.

## The Three Observable Cases

[EC-GHOST-LINK] (Finding 0048) documents the three outcomes directly:

1. **All endset I-addresses live in the queried document's POOM** → full endset returned
2. **Some unreferenced** → partial endset, only the POOM-resident I-addresses converted to V-spans
3. **All unreferenced** → empty result `[]`, operation returns success (TRUE)

The operation **never fails** due to unreferenced I-addresses. Emptiness is a valid successful result.

## What Actually Causes the I-Address to Become Unreferenced

[EC-DEEPLY-ORPHANED-LINK] clarifies the mechanism: when DELETE removes content, `deletend` Case 1 (`disown` + `subtreefree`) frees the POOM bottom crums mapping those I-addresses. The I-addresses themselves are permanent in the granfilade ([INV-IADDR-IMMUTABILITY]), but the POOM no longer maps any V-position to them. When FOLLOWLINK later calls `retrieverestricted()` for those I-addresses in the home document, there is no POOM entry to find → NULL → silent drop.

## FOLLOWLINK Is POOM-Relative

[SS-FOLLOWLINK] (Finding 0048) adds a critical nuance: FOLLOWLINK takes a `homedoc` parameter. The same link endset can produce different results depending on which document's POOM is queried:

```
Link L has to-endset I-address `a`
Document D1 has poom.D1(1.5) = a  →  FOLLOWLINK(L, TO, D1) returns [1.5]
Document D2 has no mapping for a  →  FOLLOWLINK(L, TO, D2) returns []
```

So whether the result is empty or full is a function of both the link's I-addresses *and* the specific POOM being queried against.

## RETRIEVEENDSETS Shares the Same Path

[SS-RETRIEVE-ENDSETS] confirms that RETRIEVEENDSETS also uses `linksporglset2specset()` for I→V conversion, and crucially rewrites the docid in the result to the **querying document's** context. This means the endset V-spans reported by RETRIEVEENDSETS reflect whatever the querying document's POOM currently maps — unreferenced I-addresses are silently absent from those spans as well.

## Summary

| Condition | FOLLOWLINK result | RETRIEVEENDSETS result |
|-----------|------------------|----------------------|
| All I-addrs in POOM | Full endset spans | Full endset spans |
| Some I-addrs removed | Partial spans (only live ones) | Partial spans |
| All I-addrs removed | `[]` empty, success=true | Empty spans, success=true |

The caller cannot distinguish "endset was empty at creation" from "endset content was deleted" purely from an empty return value — both produce `[]` with a successful operation status. Reconstitution via COPY back into a live document ([EC-GHOST-LINK]) is the only way to restore non-empty endset resolution, since the I-addresses themselves are permanent.

---

## Code Exploration

I have everything I need. Here is the complete analysis:

---

## Are Ghost-Link I-Spans Silently Filtered During I→V Conversion?

**Yes.** Endset I-addresses whose content has been deleted from the target document POOM are silently dropped during I→V conversion — with no error, and no signal to the caller. An endset can come back empty or partial as a result.

---

### What "Ghost-Link" Means Structurally

When content is deleted via `dodeletevspan` [`do1.c:158`] → `deletevspanpm` [`orglinks.c:145`] → `deletend` [`edit.c:31`], the crums for that V-range are physically removed from the POOM tree (`disown`/`subtreefree` at `edit.c:59–60`). Their I-mappings disappear from the POOM.

The link endsets stored in the spanfilade and in the link's own POOM are **never cleaned up** — `docreatelink` [`do1.c:195`] writes endsets into two permanent stores and neither `deletend` nor any other operation touches them:

```c
&& insertendsetsinorgl(...)   // writes I-spans into link's own POOM
&& insertendsetsinspanf(...)  // writes I-spans into spanfilade
```

So after `DELETEVSPAN` removes the pointed-to content, the link's endset I-addresses become ghost references — they name I-positions that no longer have any V-mapping in the target POOM.

---

### The I→V Conversion Path (Shared by Both Queries)

Both `FOLLOWLINK` and `RETRIEVEENDSETS` eventually reach the same I→V conversion:

```
linksporglset2specset  [sporgl.c:97]
  └─ linksporglset2vspec  [sporgl.c:127]
       └─ sporglset2vspanset  [sporgl.c:141]
            └─ ispan2vspanset  [orglinks.c:389]
                 └─ permute(taskptr, orgl, ispanptr, I, vspansetptr, V)  [orglinks.c:404]
                      └─ span2spanset  [orglinks.c:425]
                           └─ retrieverestricted((typecuc*)orgl, restrictionspanptr, I, NULL, V, NULL)
                                └─ retrieveinarea → findcbcinarea2d  [retrie.c:87,229]
```

`findcbcinarea2d` [`retrie.c:229`] walks the POOM tree and calls `crumqualifies2d` [`retrie.c:270`] for each crum. If the target I-region has been deleted, there are **no crums** for that range. The traversal completes without appending anything to `**headptr`. `retrieverestricted` returns `NULL`.

Back in `span2spanset` [`orglinks.c:425`]:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, I, (typespan*)NULL, V, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {   // loop body never executes
    context2span(...);
    nextptr = (typespan *)onitemlist(...);
}
if (!context) {
    return(targspansetptr);   // ← returns unchanged: silent no-op
}
```

When `context` is NULL, `span2spanset` returns `targspansetptr` untouched. No error, no flag. The ghost I-span simply contributes nothing to the output V-span set.

---

### FOLLOWLINK Specifically

`dofollowlink` [`do1.c:223`]:

```c
return (
   link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
&& linksporglset2specset (taskptr, &((typesporgl *)sporglset)->sporgladdress, sporglset, specsetptr, NOBERTREQUIRED));
```

`link2sporglset` [`sporgl.c:67`] looks up the link's own POOM with a V-restriction for the given end (FROM=1, TO=2):

```c
tumblerincrement (&zero, 0, whichend, &vspan.stream);   // V-position = 1.x or 2.x
tumblerincrement (&zero, 0/*1*/, 1, &vspan.width);
if (context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL)) {
    // build sporglset from I-spans stored in the link's own POOM
    ...
    return (TRUE);
} else {
    return (FALSE);   // ← only fails if the link has NO endsets at all
}
```

The link's own POOM always retains the I-spans stored at link creation — they are never deleted. So `link2sporglset` succeeds and returns the original endset I-addresses as a sporglset.

Then `linksporglset2specset` converts those I-spans to V-spans. Ghost I-spans produce no V-spans via the path described above. `linksporglset2specset` **always returns TRUE** [`sporgl.c:121`]; it has no failure path.

Result: `FOLLOWLINK` succeeds, returning a `specset` containing a `VSPECID` item with `vspanset = NULL`.

---

### RETRIEVEENDSETS Specifically

`doretrieveendsets` [`do1.c:369`] → `retrieveendsetsfromspanf` [`spanf1.c:190`]:

```c
if (!(specset2sporglset (...)
&& retrievesporglsetinrange(..., &fromsporglset)   // reads from spanfilade
&& linksporglset2specset (..., fromsporglset, fromsetptr, ...)
&& retrievesporglsetinrange(..., &tosporglset)
&& linksporglset2specset (..., tosporglset, tosetptr, ...))){
    return (FALSE);
}
```

`retrievesporglsetinrange` [`spanf1.c:237`] uses `retrieverestricted` on the spanfilade to recover the endset I-spans — it finds them (the spanfilade was written at link creation and is never pruned). The result is a sporglset with the original endset I-spans.

`linksporglset2specset` then converts them through the same I→V path. Ghost I-spans silently produce no V-spans.

Result: `RETRIEVEENDSETS` succeeds, returning `fromset`/`toset`/`threeset` that are VSPEC items with `vspanset = NULL` for fully-ghosted endsets, or reduced vspansets for partially-ghosted ones.

---

### Empty and Partial Results

**Empty endset**: If every I-span in an endset was deleted from the target POOM, the VSPEC item will have `vspanset = NULL`. The operation returns success. The client receives a VSPECID with a null vspanset.

**Partial endset**: If only some I-spans are ghost (e.g., a link pointed to a range, part of which was later `DELETEVSPAN`'d), only the surviving POOM crums contribute to the V-span list. The returned V-spans are a strict subset of what was originally linked.

There is no signal distinguishing "full endset" from "partial endset" from "empty endset" in the return value. No error, no flag. The I→V silencing is total.

---

### Key Code Locus

| File | Line | Significance |
|------|------|------|
| `edit.c` | 59–60 | `disown`/`subtreefree` — POOM crums physically removed by DELETEVSPAN |
| `sporgl.c` | 83 | `link2sporglset` — retrieves endset I-spans from link's own POOM |
| `sporgl.c` | 141–175 | `sporglset2vspanset` — calls `ispan2vspanset` to do I→V |
| `orglinks.c` | 435 | `span2spanset` — calls `retrieverestricted` for I→V |
| `orglinks.c` | 446–448 | `if(!context) return(targspansetptr)` — silent no-op for ghost spans |
| `sporgl.c` | 121 | `linksporglset2specset` always returns TRUE — no ghost-span error path |

---

### Summary

The filtering is **structural, not intentional**: the POOM simply has no crums for deleted I-ranges, so `retrieverestricted` returns NULL and `span2spanset` silently returns without adding to the output. Both `FOLLOWLINK` and `RETRIEVEENDSETS` share this path via `linksporglset2specset` → `sporglset2vspanset` → `ispan2vspanset` → `permute` → `span2spanset`. An endset **can come back empty** (all ghost → `vspanset = NULL`, success returned) or **partial** (some ghost → `vspanset` is a proper subset of the original). There is no error or distinguishing flag in either case.
