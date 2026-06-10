## Question 1 [evidence]

> How does udanax-green remove or retract links — strictly one link per operation, or can a single operation (e.g., a vspan delete over the link subspace) excise a contiguous range of link addresses?

## KB Synthesis

Udanax-green has no true link retraction at all — and the partial mechanism that does exist can operate on ranges.

## No Operation Removes Links from the Permanent Layers

[SS-THREE-LAYER-MODEL] and [INV-LINK-PERMANENCE] are unambiguous: there is no `DELETELINK` opcode in the FEBE protocol. Links exist across three independent layers — I-space (link orgl), spanfilade (DOCISPAN/endpoint index), and POOM (document V-stream) — and no operation removes entries from the first two. The link orgls are permanent; the spanfilade is strictly append-only [INV-SPANF-WRITE-ONLY].

## What DELETEVSPAN Actually Does to Links

`DELETEVSPAN` targeting the link subspace (V-position `2.x`) is the only available mechanism, and it affects **only the POOM layer** [FC-LINK-DELETE-ISOLATION]. After a `DELETEVSPAN(2.x)`:

- The link orgl at its I-address: **unchanged**
- The spanfilade DOCISPAN entries: **unchanged**
- The POOM V→I mapping for that link in the home document: **removed**
- `find_links()` searching by content: **still works** (spanfilade intact)
- `follow_link(link_id)`: **still works** (link orgl intact)

The result is what [EC-REVERSE-ORPHAN] calls a "reverse orphan" — the link exists and is fully functional, but no longer appears in the document's `vspanset`.

## Range Deletion: Multiple Links in One Operation

A single `DELETEVSPAN` with a span covering multiple link positions is structurally valid. Link orgls are allocated at `2.1`, `2.2`, `2.3`, etc. [SS-LINK-SUBSPACE]. The `deletend` algorithm [ST-DELETE] processes all POOM crums whose V-positions fall within the deletion range:

- Crums **fully within** the range (Case 1): disowned and freed
- Crums **partially overlapping** the boundary (Case 2/0): shifted or left intact

So `DELETEVSPAN(start=2.1, width=0.3)` would remove the POOM entries for links at `2.1`, `2.2`, and `2.3` in a single call, excising all three from the document's V-stream simultaneously.

The precondition is non-zero width only [PRE-DELETE]; there is no per-link granularity constraint.

## Summary

| Concern | Answer |
|---------|--------|
| True link deletion (remove from I-space / spanfilade) | **Impossible** — no such operation exists |
| Remove link from document POOM | `DELETEVSPAN(2.x)` — works |
| One-at-a-time vs range | Range works — a single `DELETEVSPAN` spanning `[2.1, 2.N)` removes N links from the POOM |
| Post-operation discoverability | Links remain fully discoverable and followable via content identity / direct ID |

The architecture reflects a deliberate design choice: "link permanence" in Xanadu means permanence of the link *object* in the global I-space, not permanence of its association with any particular document's V-stream. [INV-LINK-PERMANENCE]

---

## Code Exploration

I now have the complete picture. Here is the full analysis.

---

## How udanax-green Removes Links

### Short Answer

The `DELETEVSPAN` FEBE operation accepts exactly **one contiguous span** per call (`typevspan` = stream + width). But because link V-addresses in the hosting document are allocated sequentially starting at 2.1, **a single call with sufficient width excises an arbitrary contiguous run of link addresses from the POOM** in one shot. The operation is not limited to one link per call.

---

### Call Chain

```
fns.c:333       deletevspan()        FEBE handler — takes one typespan vspan
do1.c:158       dodeletevspan()      passes typevspan * to deletevspanpm
orglinks.c:145  deletevspanpm()      calls deletend(stream, width, V)
edit.c:31       deletend()           generic range-delete on V-dimension
```

**`fns.c:333-347`** — the FEBE handler:
```c
void deletevspan(typetask *taskptr)
{
  typeisa docisa;
  typespan vspan;          // ONE span: stream + width
    (void) getdeletevspan (taskptr, &docisa, &vspan);
    if (!dodeletevspan (taskptr, &docisa, &vspan))
```

**`do1.c:158-167`** — `dodeletevspan`:
```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
    );
}
```

**`orglinks.c:145-152`** — `deletevspanpm`:
```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr,
                   typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

**`edit.c:31-76`** — `deletend` (generic range-delete on the V-dimension):
```c
int deletend(typecuc *fullcrumptr, tumbler *origin, tumbler *width, INT index)
{
    movetumbler (origin, &knives.blades[0]);       // blade[0] = stream
    tumbleradd (origin, width, &knives.blades[1]); // blade[1] = stream + width
    knives.nblades = 2;
    knives.dimension = index;                       // V-dimension
    makecutsnd (fullcrumptr, &knives);
    ...
    for (ptr = findleftson(father); ptr; ptr = next) {
        switch (deletecutsectionnd(ptr, &fgrasp, &knives)) {
          case 1:
            disown ((typecorecrum*)ptr);
            subtreefree ((typecorecrum*)ptr);     // crum inside range → removed
            break;
          case 2:
            tumblersub (&ptr->cdsp.dsas[index], width, ...); // after range → shifted
            break;
        }
    }
    setwispupwards (father, 1);
    recombine (father);
}
```

`deletend` cuts the enfilade at two positions (`stream` and `stream+width`) and removes **every crum that falls within the range** — it is not a one-element operation. The number of crums removed is however many happen to cover the specified V-interval.

---

### Link V-Address Layout

Links in a hosting document are allocated sequentially by `findnextlinkvsa` [`do2.c:151-167`]:
```c
tumblerclear (&firstlink);
tumblerincrement (&firstlink, 0, 2, &firstlink);  // → [2, 0, ...] exp=0
tumblerincrement (&firstlink, 1, 1, &firstlink);  // → [2, 1, ...] exp=0 = tumbler 2.1

(void) doretrievedocvspan (taskptr, docisaptr, &vspan);
tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
if (tumblercmp (&vspanreach, &firstlink) == LESS)
    movetumbler (&firstlink, vsaptr);   // first link → 2.1
else
    movetumbler (&vspanreach, vsaptr);  // next link → sequential end
```

Each new link is placed at the first available V-address after the document's current POOM reach, with a floor of 2.1. The result is a dense, sequential run: first link at 2.1, second at 2.2, third at 2.3, and so on (Finding 0065, confirmed by golden tests). A single call to `DELETEVSPAN` with stream=2.1 and a width spanning N link slots removes all N of them from the POOM in one operation.

---

### What the Delete Actually Does (and Does Not Do)

`deletevspanpm` calls **only** `deletend` on the document's orgl. Nothing else is touched.

#### Layer 1 — POOM (the document's granf orgl): **Modified**

The V→I mappings for the covered range are cut out of the 2D enfilade. The deleted link addresses no longer appear in `retrieve_doc_vspanset`. This is the only thing the delete changes.

#### Layer 2 — Link orgl in I-space: **Untouched**

The actual link objects — stored in the global granfilade at I-addresses like `doc.0.2.1` — are never touched. `follow_link(link_id)` continues to work because the link orgl persists permanently. This is the "P0 permanence axiom": nothing is ever removed from I-space.

#### Layer 3 — Spanfilade: **Untouched**

`CREATELINK` calls `insertendsetsinspanf` [`do2.c:116-128`] to register the link's endpoint I-addresses. `DELETEVSPAN` has no corresponding call to remove them. No `deletespanf` function exists anywhere in `spanf1.c` or `spanf2.c` (Finding 0057). As a result, `find_links` continues to discover these links through the persistent spanfilade entries even after their POOM entries are gone (Finding 0040).

---

### Subspace Isolation: Text Is Not Disturbed

When a delete targets the link subspace (V ≥ 2.x), text crums (V ≈ 1.x) are not shifted. `deletecutsectionnd` [`edit.c:235-248`] classifies text crums as case 2 (shift), but the actual `tumblersub(2.1, 0.1)` call is a no-op. Tracing through `tumblersub` → `tumbleradd` → `strongsub` [`tumble.c:534-547`]:

```c
int strongsub(tumbler *aptr, tumbler *bptr, tumbler *cptr)
{
    if (bptr->exp < aptr->exp) {
        movetumbler(aptr, cptr);   // returns aptr UNCHANGED
        return(0);
    }
    ...
}
```

The deletion width of a single link slot has exponent `exp = -1`, while the link V-address `2.1` has `exp = 0`. Since `bptr->exp(-1) < aptr->exp(0)`, `strongsub` returns the displacement unchanged. Text crums at 1.x are unaffected for the same reason — they sit at exponent 0, below the 2.x deletion range and therefore classified case 0, not case 2 at all (Finding 0055).

---

### Summary

| Question | Answer |
|---|---|
| How many spans per FEBE call? | Exactly one `typevspan` (stream + width) |
| Can one call cover multiple link addresses? | Yes — width is arbitrary; N consecutive links at 2.1–2.N removed in one call |
| What is the POOM effect? | `deletend` excises the V→I mappings for the entire covered range |
| Are link orgls in I-space deleted? | No — permanent; `follow_link` still works |
| Are spanfilade entries cleaned up? | No — `deletespanf` does not exist; `find_links` still works |
| Does a link-subspace delete shift text entries? | No — `strongsub` exponent guard at `tumble.c:544` prevents it |

There is no atomic "delete link by ISA" operation. A caller who wants to retract a link from the POOM must know the link's V-address in the hosting document and issue `DELETEVSPAN` targeting that address in the 2.x subspace. A single such call can retract one link or an entire contiguous run of links, depending on the specified width. The link objects and discovery index in the spanfilade remain intact regardless.
