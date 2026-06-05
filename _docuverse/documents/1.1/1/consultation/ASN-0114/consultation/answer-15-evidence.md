## Question 15 [evidence]

> Are unreferenced I-addresses (DEL5 — those in no current POOM) silently filtered from the returned spec-set the way FOLLOWLINK filters them during I→V conversion, or is the raw stored endset returned regardless of current reachability?

## KB Synthesis

Unreferenced I-addresses are **silently filtered**. The raw stored endset is never returned directly — every FOLLOWLINK response passes through an I→V conversion that drops any I-address with no current POOM mapping.

The mechanism is documented in [INV-ITOV-FILTERING] and [SS-FOLLOWLINK]:

`link2sporglset()` extracts the endset I-addresses from the link orgl without consulting any POOM. At that stage, all stored I-addresses are present regardless of reachability. The filtering happens in the second phase: `linksporglset2specset()` → `span2spanset()` → `retrieverestricted()` searches the queried document's POOM for each I-address. When `retrieverestricted()` returns NULL (no current V-position mapping), the I-address is silently dropped — no V-span added, no error raised.

This is a **universal invariant** of the I→V conversion layer, not a FOLLOWLINK-specific behavior. [INV-ITOV-FILTERING] states it holds for RETRIEVEENDSETS via the identical `linksporglset2specset()` path.

The observable result ([EC-GHOST-LINK]):
- All endset I-addresses live → full spec-set returned
- Some unreferenced → partial spec-set, only live addresses converted
- All unreferenced → empty `[]`, operation still succeeds (success, not error)

The permanent layer (granfilade) retains the raw I-addresses forever per [INV-IADDR-IMMUTABILITY], so reconstitution is always possible — copying content back into a document restores POOM mappings and makes those I-addresses resolvable again.

---

## Code Exploration

All citations verified. Here is the complete answer.

---

## FOLLOWLINK and Unreferenced I-Addresses: Silently Filtered

**Yes — unreferenced I-addresses are silently filtered during I→V conversion.** The raw stored endset is never returned as-is. Only I-addresses that map to live V-addresses in the current POOM survive.

---

### Execution Path

**1. FEBE entry** — `backend/fns.c:114-127`, `followlink()`:

```c
void followlink(typetask *taskptr)
{
    if (   getfollowlink(taskptr, &linkisa, &whichend)
        && dofollowlink(taskptr, &linkisa, &specset, whichend))
        putfollowlink(taskptr, specset);
    else
        putrequestfailed(taskptr);
}
```

Calls `dofollowlink()`, which in turn calls `link2sporglset()` (extracts the raw I-spans from the link endset) then `linksporglset2specset()` (converts each I-span to a spec). Nothing is filtered yet at this level.

**2. Conversion chain** — through `sporglset2vspanset()` → `ispan2vspanset()` (orglinks.c:389) → `permute()` (orglinks.c:404) → `span2spanset()` for each I-span.

**3. The filtering point** — `backend/orglinks.c:425-454`, `span2spanset()`:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr,
                              restrictionindex, (typespan*)NULL,
                              targindex, (typeisa*)NULL);   // line 435
for (c = context; c; c = c->nextcontext) {
    context2span(c, ...);
    nextptr = (typespan *)onitemlist(...);
}
if (!context) {
    return(targspansetptr);   // line 446-448: silent drop
}
```

`retrieverestricted()` is called with the I-span as restriction and `V` as target index. If the I-address has no mapping in the current POOM — because the content at that I-location was deleted, never written, or is otherwise unreachable — `retrieverestricted()` returns `NULL`. The `for` loop body never executes. The `if (!context)` guard at line 446 then **returns the target span-set unchanged**, silently skipping this I-address. No error, no placeholder, no indication.

**4. Why retrieverestricted returns NULL for orphaned I-addresses** — `backend/retrie.c:229-268`, `findcbcinarea2d()`:

```c
for (; crumptr; crumptr = getrightbro(crumptr)) {
    if (!crumqualifies2d(crumptr, offsetptr,
                         span1start, span1end, index1,
                         span2start, span2end, index2, ...)) {
        continue;      // line 253-254
    }
    // only qualifying crumbs build contexts
    context = makecontextfromcbc(...);
    incontextlistnd(headptr, context, index1);
}
```

`crumqualifies2d()` (retrie.c:270) checks whether a crum's address range intersects both the I-span restriction and the V-span target range. If no crumbs in the enfilade cover the queried I-address in the V dimension — i.e., no POOM currently references it — every crum fails qualification, the loop builds no contexts, and `headptr` is left `NULL`.

---

### Summary

| Stage | What happens |
|-------|-------------|
| `link2sporglset()` | Raw I-span endset extracted from link — no filtering |
| `span2spanset()` (`orglinks.c:446`) | If `retrieverestricted()` returns `NULL` for an I-span, that span is **silently dropped** |
| `findcbcinarea2d()` (`retrie.c:252-264`) | Only crumbs qualifying in both I and V dimensions generate contexts |
| Caller | Sees a spec-set containing only I-addresses with live V-address mappings |

The behavior is identical in structure to FOLLOWLINK's I→V conversion: **the enfilade itself performs the reachability filter**. An I-address in no current POOM generates no qualifying crumbs, `retrieverestricted()` returns `NULL`, and `span2spanset()` silently passes over it at `backend/orglinks.c:446-448`. The raw stored endset is never exposed to the caller.
