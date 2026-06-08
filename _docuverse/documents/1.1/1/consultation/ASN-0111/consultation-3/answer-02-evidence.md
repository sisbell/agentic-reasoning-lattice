## Question 2 [evidence]

> In the udanax-green implementation and the ASN-0043 foundations, what distinct structural treatments does the type slot receive relative to the from/to connective slots, beyond mandatory non-emptiness (L3) and coverage-identity-without-dereference (L8)?

## KB Synthesis

From the KB, the type slot receives several structural treatments distinct from the from/to connective slots:

---

## 1. Distinct V-subspace segregation within the link orgl

The type endset occupies V-subspace **3.x** within the link orgl's internal POOM structure, while from/to endsets are placed at **2.x**. `setlinkvsas()` hardcodes digit-0 values 2 and 3 respectively: "type endpoints by incrementing digit 0 to 3 (yielding `3.1`, etc.)." [SS-DUAL-ENFILADE Finding 0038, FC-SUBSPACE Finding 0054]

This is not merely a labeling convention — the two-blade knife mechanism enforces subspace isolation at insert time, so the type slot is structurally insulated from from/to slot shifts. [SS-TWO-BLADE-KNIFE, FC-SUBSPACE]

---

## 2. Target domain restricted to the bootstrap registry

From/to spans are unconstrained with respect to document identity. The type slot is specifically bound to the bootstrap document's type registry: `link.type : VSpec` where `VSpec.docid = bootstrap_doc ∧ VSpec.spans ⊆ addresses(1.0.2.*)`. Types are content references into a specific, privileged system document rather than arbitrary user content. [SS-LINK-ENDPOINT Finding 0024]

---

## 3. Hierarchical subtype ordering via tumbler containment

The type registry encodes a subtype relation directly in address structure: MARGIN at `1.0.2.6.2` is contained under FOOTNOTE at `1.0.2.6`. This enables type-family queries via address-range matching ("find all footnote-family links") — a structural capability with no analogue for from/to connective spans. From/to content has no such intrinsic prefix hierarchy. [SS-LINK-ENDPOINT Finding 0024]

---

## 4. Spanfilade ORGLRANGE dimension at LINKTHREESPAN=3

The spanfilade indexes each endset type under a distinct ORGLRANGE prefix: LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3. Although all three get separate dimensions, the type slot's dimension is the one that is **non-functional in practice** — `find_links` with a type specset returns empty results even when matching links exist. The type dimension is structurally registered but operationally inert. [SS-RETRIEVE-ENDSETS Finding 0035, EC-TYPE-FILTER-NONFUNCTIONAL Finding 0029]

---

## 5. Anomalous liveness coupling to from/to endpoints

When both from and to endpoints are fully orphaned (all content deleted), `follow_link(link_id, TYPE)` also returns empty — despite the type referencing the immutable bootstrap document that was never touched. This is marked as anomalous (`*`) in the orphan behavior matrix and has no symmetric explanation from the type slot's own content state. It suggests an undocumented resolution dependency on connective endpoint liveness not present for individual from/to queries. [EC-ORPHANED-LINK Finding 0024]

---

In sum: the type slot is structurally distinct in its **subspace address** (3.x vs 2.x), its **target domain constraint** (bootstrap registry), its **hierarchical subtype semantics** (tumbler containment for range queries), its **non-functional search dimension**, and its **anomalous ghost-coupling** to connective liveness. The first three are design-level distinctions; the last two are implementation deviations from the intended structural model.

---

## Code Exploration

Now I have enough information from the source to give a complete answer.

---

## Structural Treatments of the Type Slot vs From/To in udanax-green

The question excludes L3 (non-emptiness) and L8 (coverage-identity-without-dereference). Here are the remaining distinct structural treatments:

---

### 1. Conditional Existence vs Unconditional Existence

The type slot is the **only slot that can be structurally absent** from a link orgl. From and to are always stored. Three independent guards enforce this asymmetry:

**`insertendsetsinorgl`** (do2.c:130–148):
```c
bool insertendsetsinorgl(... tumbler *fromvsa, typesporglset fromsporglset,
                             tumbler *tovsa, typesporglset tosporglset,
                             tumbler *threevsa, typesporglset threesporglset)
{
    if (!( insertpm(taskptr, linkisaptr, link, fromvsa, fromsporglset)
        && insertpm(taskptr, linkisaptr, link, tovsa, tosporglset)))    // unconditional
            return (FALSE);
    if (threevsa && threesporglset) {                                   // CONDITIONAL
        if (!insertpm(taskptr, linkisaptr, link, threevsa, threesporglset)){
            return (FALSE);
        }
    }
```

**`insertendsetsinspanf`** (do2.c:116–128):
```c
    insertspanf(taskptr,spanfptr,linkisaptr,fromsporglset,LINKFROMSPAN)
    && insertspanf(taskptr,spanfptr,linkisaptr,tosporglset,LINKTOSPAN)  // unconditional
    ...
    if (threesporglset) {                                               // CONDITIONAL
        insertspanf(taskptr,spanfptr,linkisaptr,threesporglset,LINKTHREESPAN);
    }
```

From/to always go through `insertpm` and `insertspanf` unconditionally. The type slot gets a NULL guard. A link can exist without a type slot but cannot exist without from or to.

---

### 2. Two-Slot Link Creation Path (domakelink vs docreatelink)

There are two separate link creation functions. `domakelink` (do1.c:169–193) explicitly passes NULL for the type:

```c
&& setlinkvsas (&fromvsa, &tovsa, NULL)                       // do1.c:189
&& insertendsetsinorgl(..., &fromvsa, fromsporglset,
                            &tovsa, tosporglset,
                            NULL, NULL)                       // do1.c:190
```

`docreatelink` (do1.c:195–221) includes the type:

```c
&& setlinkvsas (&fromvsa, &tovsa, &threevsa)                  // do1.c:217
&& insertendsetsinorgl(..., &fromvsa, fromsporglset,
                            &tovsa, tosporglset,
                            &threevsa, threesporglset)        // do1.c:218
```

There is no `makefrom` or `maketo` variant — no creation path exists that omits from or to. The asymmetry is architectural: from/to are constitutive of the link; type is augmentative.

---

### 3. V-Address Ordinal Assignment in the Link Orgl

`setlinkvsas` (do2.c:169–183) explicitly assigns ordinal positions:

```c
tumblerclear(fromvsaptr);
tumblerincrement(fromvsaptr, 0, 1, fromvsaptr);  // digit 0 = 1
tumblerincrement(fromvsaptr, 1, 1, fromvsaptr);  // → V-position 1.1

tumblerclear(tovsaptr);
tumblerincrement(tovsaptr, 0, 2, tovsaptr);      // digit 0 = 2
tumblerincrement(tovsaptr, 1, 1, tovsaptr);      // → V-position 2.1

if (threevsaptr) {
    tumblerclear(threevsaptr);
    tumblerincrement(threevsaptr, 0, 3, threevsaptr);  // digit 0 = 3
    tumblerincrement(threevsaptr, 1, 1, threevsaptr);  // → V-position 3.1
}
```

The type slot occupies V-position **3.1** within the link orgl — the third ordinal subspace, after from (1.1) and to (2.1). This is not just a numeric tag; it places type content into a distinct subspace of the link orgl's V-dimension, meaning V→I lookups for type content are bounded to the [3.0, 4.0) interval, entirely non-overlapping with the from and to subspaces.

---

### 4. Spanfilade Discrimination Tag

The three slots receive distinct integer constants for spanfilade indexing (xanadu.h:35–39):

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
```

In `findlinksfromtothreesp` (spanf1.c:56–103), these constants discriminate which endpoint dimension is being searched:

```c
sporglset2linkset(..., fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);   // 1
sporglset2linkset(..., tosporglset,   &tolinkset,   orglrange, LINKTOSPAN);     // 2
sporglset2linkset(..., threesporglset,&threelinkset,orglrange, LINKTHREESPAN);  // 3
```

The tag ensures that a content address stored in the type slot of one link cannot accidentally match as the from/to slot of another, even if the I-addresses happen to coincide. This is a structural discriminator within the unified spanfilade index.

---

### 5. `whichend` Protocol Validation Includes Type, But Conditionally

`getfollowlink` (get1.c:63–74) enforces:
```c
getnumber(taskptr, whichendptr)
&& (*whichendptr == 1 || *whichendptr == 2 || *whichendptr == 3)
```

All three endpoints are traversable via FOLLOWLINK. But `link2sporglset` (sporgl.c:67–95) uses `whichend` as the V-position digit:
```c
tumblerincrement(&zero, 0, whichend, &vspan.stream);  // sporgl.c:81
```

For a two-slot link (created via `domakelink`), following `whichend=3` will find nothing at V-position 3.x — `retrieverestricted` returns NULL and `link2sporglset` returns FALSE. The from/to slots (1 and 2) are guaranteed to be present; the type slot (3) may legitimately be absent. This is not guarded at the protocol layer — the caller must tolerate a failed FOLLOWLINK on end 3.

---

### Summary

| Property | From (end 1) | To (end 2) | Type (end 3) |
|----------|-------------|-----------|-------------|
| V-position in link orgl | 1.1 | 2.1 | 3.1 |
| Spanfilade tag | LINKFROMSPAN=1 | LINKTOSPAN=2 | LINKTHREESPAN=3 |
| Storage guard | None | None | `if (threevsa && threesporglset)` |
| Required by creation | Yes (both paths) | Yes (both paths) | No (domakelink omits it) |
| FOLLOWLINK may return empty | Never | Never | Yes (2-slot link) |

The type slot is the **third ordinal subspace** of the link orgl's V-dimension, held under LINKTHREESPAN in the spanfilade, conditionally absent from both the POOM store and the spanfilade index, with no creation path that enforces its presence. From and to are unconditional structural requirements; the type slot is a structural optional — present when provided, absent otherwise, discriminated by both V-ordinal and spanfilade tag.
