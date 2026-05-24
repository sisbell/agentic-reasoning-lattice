## Question 5 [evidence]

> When udanax-green's allocator processes two consecutive bare retractions targeting the same address, does it produce one link-store entry or two?

## KB Synthesis

The KB does not contain any information about "bare retractions." That term does not appear in any of the 78 findings, and there is no operation in the documented FEBE protocol or backend implementation that corresponds to it.

The KB describes DELETE (`DELETEVSPAN`), which removes V-to-I mappings from the POOM but never writes to or removes from the spanfilade [INV-SPANF-WRITE-ONLY], [ST-DELETE]. If "bare retraction" is intended to mean something else — a link creation variant, an undo mechanism, or a protocol message — those are also absent from the KB.

This question is not answerable from the knowledge base as given.

---

## Code Exploration

I now have a complete picture. Here is my full answer:

---

## Answer: Bare Retractions and Link-Store Entries

### Terminology Not Found in Source

The term **"bare retraction"** does not appear anywhere in the udanax-green C source code. A full search of `backend/` confirms zero matches for "retract" or "retraction" as identifiers or keywords. The closest analogous operation is `DELETEVSPAN` (request code 12, `requests.h:29`).

---

### The Actual Deletion Path

Two consecutive `deletevspan` calls targeting the same V-address trace this path:

**1. `fns.c:333–347`** — `deletevspan()` dispatches:
```c
(void) getdeletevspan(taskptr, &docisa, &vspan);
putdeletevspan(taskptr);
if (!dodeletevspan(taskptr, &docisa, &vspan)) ...
```

**2. `do1.c:158–167`** — `dodeletevspan()` calls into the POOM:
```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    ...
    findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm(taskptr, docisaptr, docorgl, vspanptr)
}
```

**3. `orglinks.c:145–152`** — `deletevspanpm()` — **this is the complete function**:
```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

**4. `edit.c:31–76`** — `deletend()` cuts the POOM at `[origin, origin+width]` and removes/shifts crums by case:
- **Case 1** (`edit.c:58–60`): `disown` + `subtreefree` — removes crums that lie entirely within the deleted span
- **Case 2** (`edit.c:62–63`): `tumblersub(&ptr->cdsp.dsas[V], width, ...)` — shifts crums that follow the deleted span

---

### Critical Observation: No Spanfilade Writes

`deletevspanpm` calls **only** `deletend` (on the POOM/orgl) and `logbertmodified`. It never calls `insertspanf` or `insertendsetsinspanf`. Those functions are the only writers to the spanfilade (the link store):

- `insertspanf` (`spanf1.c:15–54`): called from INSERT and CREATE_LINK paths
- `insertendsetsinspanf` (`spanf1.c`, via `do1.c:191`, `do1.c:219`): called only from link creation

The granfilade allocator — `findisatoinsertgr` (`granf2.c:130–156`) — is also not involved in deletion. It only runs during INSERT and CREATE_LINK.

---

### What Happens on the Second Call

The **first** `deletevspan` at address V removes the POOM crums in `[V, V+width]`. The `deletecutsectionnd` function (`edit.c:235–248`) returns case 1 for those crums, which are then disowned and freed.

The **second** `deletevspan` at the same address constructs identical knife blades at `[V, V+width]` (`edit.c:40–43`):
```c
movetumbler(origin, &knives.blades[0]);
tumbleradd(origin, width, &knives.blades[1]);
```
But since those crums no longer exist, `deletecutsectionnd` returns 0 for all remaining crums. No crums are freed or shifted. **The second call is a structural no-op on the POOM.**

---

### How Many Link-Store Entries?

**Zero** — for both calls combined. `deletevspan` does not write to the spanfilade. There is no mechanism in udanax-green by which deletion creates entries in the link store. Two consecutive deletions at the same V-address produce:

| Call | POOM effect | Spanfilade entries created |
|---|---|---|
| First `deletevspan` | Removes crums at [V, V+width] (`edit.c:58–60`) | **0** |
| Second `deletevspan` | No-op (crums already gone) | **0** |

---

### Hypothetical: If Retractions Were Link-Typed

For completeness: if udanax-green did record deletions as spanfilade entries, the answer would be **two**, not one. `insertcbcnd` (`insertnd.c:242–275`) merges a new insertion into an existing crum only via `isanextensionnd` (`insertnd.c:301–309`), which requires:

```c
return (lockeq(reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
```

Two insertions at the **same** origin do not satisfy this condition — the reach of the first equals `origin + width`, not `origin` itself. They would create **two** distinct crums, not one. Deduplication of overlapping same-address entries is not implemented.

---

### Summary

udanax-green's allocator does not process "bare retractions" because that concept does not exist in the implementation. The term does not appear in any source file. The deletion operation (`deletevspan` → `deletevspanpm` → `deletend`) modifies only the POOM and writes nothing to the spanfilade. Two consecutive deletions at the same address produce **zero link-store entries** — the second deletion is also a no-op on the POOM because the crums are already gone. The hypothetical case of link-typed retractions inserted into the spanfilade would produce two entries (not one) because `isanextensionnd`'s adjacency check does not merge same-origin entries.
