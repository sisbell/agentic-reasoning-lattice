## Question 1 [evidence]

> When a link is withdrawn from a document's arrangement and later re-arranged (or when links are removed and re-added), does the implementation preserve each link's original V-position/order-of-arrival, or can a link end up at a different position?

## KB Synthesis

## Link V-Position Preservation

The short answer: **link V-positions are not preserved after removal.** The implementation uses append-only placement, and removal creates a permanent "reverse orphan" state rather than a reusable slot.

---

### How link positions are assigned

From [SS-LINK-SUBSPACE] and [ST-CREATE-LINK]: `findnextlinkvsa()` places every new link at `vspanreach` — the current end of the document's extent — or at `2.1` if the link subspace is empty. This is a pure append mechanism with no position-reuse logic.

### What removal actually does

From [SS-THREE-LAYER-MODEL] and [EC-REVERSE-ORPHAN]: `DELETEVSPAN(2.x)` removes only the POOM entry. The link orgl in I-space and spanfilade entries are untouched. The link enters a **reverse-orphan** state — discoverable via `find_links` and followable via `follow_link`, but absent from `retrieve_vspanset`. The I-address is permanent [INV-LINK-PERMANENCE].

### Behavior on re-add

`CREATELINK` always allocates a **new** link orgl (new I-address via `createorglingranf`) and places it via `findnextlinkvsa`. If the removed link was the only one, `vspanreach` yields `2.1` again — same position number, but a **different link object**. The original reverse-orphan link and the new link coexist independently. There is no mechanism to re-insert an existing link orgl at any V-position.

### REARRANGE on the link subspace

From [INV-REARRANGE-IDENTITY] and [PRE-REARRANGE] (Finding 0051): REARRANGE does change link V-positions — the cut-point offset arithmetic applies uniformly to `2.x` entries. I-addresses are preserved, but arrival order can be permuted. There is no guard preventing cross-subspace pivots either [EC-REARRANGE-CROSS-SUBSPACE].

### Summary

Order-of-arrival is encoded once at creation via append-at-end placement and is not recoverable after removal. A "re-added" link is always a new object at the current tail of the `2.x` subspace; the original link persists as a reverse orphan [EC-REVERSE-ORPHAN] at the I-space and spanfilade layers indefinitely.

---

## Code Exploration

Now I have everything I need from direct code reads. Let me compose the complete answer.

---

## Link V-Position Preservation: Does Re-Insertion Preserve Order-of-Arrival?

**Short answer: No.** V-positions are ephemeral. ISAs are eternal. The two must not be confused.

---

### How a Link Gets Its V-Position (First Creation)

`docreatelink` [do1.c:195–221] is the entry point. The critical call is at line 211:

```c
findnextlinkvsa (taskptr, docisaptr, &linkvsa)
```

`findnextlinkvsa` [do2.c:151–167] computes the next available V-position by reading the document's **current total content span** and placing the new link immediately after its end:

```c
(void) doretrievedocvspan (taskptr, docisaptr, &vspan);
tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
if (tumblercmp (&vspanreach, &firstlink) == LESS)
    movetumbler (&firstlink, vsaptr);   // no content yet — start at default
else
    movetumbler (&vspanreach, vsaptr);  // place after whatever is already there
```

There is **no lookup into history**. The function sees only the live POOM state. The resulting `linkvsa` is then handed to `docopy` [do1.c:45–65] → `insertpm` [orglinks.c:75–134], which writes that coordinate into the POOM node [orglinks.c:113]:

```c
movetumbler (vsaptr, &crumorigin.dsas[V]);
```

---

### How a Link's V-Position Is Destroyed on Withdrawal

`dodeletevspan` [do1.c:158–167]:

```c
findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
```

`deletevspanpm` [orglinks.c:145–152] calls directly into the enfilade tree surgery:

```c
deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
```

`deletend` in `edit.c` cuts and compacts the tree. After it returns, the V-coordinate is gone. **No record of it is saved anywhere.** The V-space is compacted around the gap.

---

### What Happens on Re-Insertion?

There is no "re-insert the same link" operation. The FEBE protocol provides `copy` — which calls `findnextlinkvsa` again [do1.c:211]. It sees the **current** document end and places the link there. If the document shrank (due to deletions), the new position may be numerically earlier than the original. If other content was added, it may be later. Either way, it is **not** the original position.

The link's **ISA** (its identity) never changes. The granfilade still knows the link object at its original address. But the **V-coordinate in the containing document's POOM** is freshly computed from nothing but current state.

---

### Special Case: `docreatenewversion` *Does* Preserve V-Positions

`docreatenewversion` [do1.c:260–299] is different. It copies the entire content span at the **same V-coordinates**:

```c
doretrievedocvspanfoo (taskptr, isaptr, &vspan)          // get source V-span
...
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec) // copy at same stream start
```

`docopyinternal` → `insertpm` [do1.c:66–82, orglinks.c:113] uses `&vspan.stream` — the original document's starting V-address — as its `vsaptr`. So **new versions inherit the full V-layout of their source**, including link positions. But this is a structural copy, not a re-insertion.

---

### What `setlinkvsas` Tells Us About Link-Internal Structure

`setlinkvsas` [do2.c:169–183] assigns the link's own internal endset V-coordinates:

```c
tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);  // from-end at local V=1.1
tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);
tumblerincrement (tovsaptr, 0, 2, tovsaptr);      // to-end at local V=2.1
tumblerincrement (tovsaptr, 1, 1, tovsaptr);
```

These are the internal coordinates *within the link object's own orgl*. They are **fixed constants**, not computed from history. Every link gets the same internal layout.

---

### Summary Table

| Property | V-Position in Parent Doc | ISA (Link Identity) |
|---|---|---|
| **Assigned by** | `findnextlinkvsa` — live state | `findisatoinsertmolecule` — sequential |
| **Preserved on deletion** | NO — `deletend` compacts V-space | YES — ISA is immutable |
| **Preserved on re-insertion** | NO — fresh call to `findnextlinkvsa` | YES — same object |
| **Preserved across `createnewversion`** | YES — copied at original coordinates | YES |
| **Order-of-arrival encoded** | Only at time of first insertion | Permanently |
| **Code location** | do2.c:151–167, orglinks.c:113 | granf2.c:158–181 |

---

### Conclusion

The implementation encodes order-of-arrival in **two separate ways that can diverge**:

1. **ISA sequence** (granf2.c:158–181): immutable, sequential, never recycled. This is the true permanent record of creation order.

2. **V-position in a document's POOM** (do2.c:151–167 → orglinks.c:113): ephemeral presentation coordinate. It reflects the document's state at the moment of insertion. If a link is withdrawn via `dodeletevspan` [do1.c:158] and later re-copied into the same document, `findnextlinkvsa` will compute a **new** coordinate based on whatever the document's current content span is. The original V-position is not stored, not searched for, and not restored.

The only operation that preserves V-positions faithfully is `docreatenewversion` [do1.c:293], which bulk-copies the source document's full V-layout into the new container — but that is structural inheritance, not re-insertion.
