## Question 15 [gregory]

> Is the source/target distinction on a link an intrinsic structural asymmetry in the orgl representation, or is it a naming convention over two structurally identical endset slots — could a link be meaningfully "followed" in either direction with equal validity?

## KB Synthesis

The source/target distinction is **a naming convention over two structurally identical endset slots**, not an intrinsic asymmetry. Here's the evidence:

## Storage Structure

The link orgl stores three sub-positions: 0.1 (FROM), 0.2 (TO), and 0.3 (TYPE). Per [SS-DUAL-ENFILADE] Finding 0038, `setlinkvsas()` constructs these by hardcoding digit-0 values of 1, 2, and 3. The FROM and TO slots use exactly the same storage format — both are sporglsets, both indexed in the spanfilade via the same mechanism, distinguished only by their ORGLRANGE subspace constant (LINKFROMSPAN=1 vs LINKTOSPAN=2) per [SS-RETRIEVE-ENDSETS] Finding 0035.

## Symmetric Discovery

[SS-LINK-ENDPOINT] Finding 0005 states both endpoints "participate symmetrically in discovery":

- `find_links(source_specs, NOSPECS)` = links whose **source** I-addresses intersect
- `find_links(NOSPECS, target_specs)` = links whose **target** I-addresses intersect

The search mechanism is identical — both convert V-spans to I-addresses and query the spanfilade. Neither direction has priority.

## Symmetric Traversal

[SS-FOLLOW-LINK] Finding 0028 confirms both are fully traversable:
```
follow_link(L, SOURCE) == L.source_specset
follow_link(L, TARGET) == L.target_specset
```

Per [SS-FOLLOWLINK] Finding 0048, `link2sporglset()` extracts endsets from the link orgl at position 0.1, 0.2, or 0.3 via `retrieverestricted()` — the same code path with a position parameter. There is no code-level asymmetry between retrieving FROM vs TO.

## Where Asymmetry Actually Lives

The only **genuine** structural asymmetry is between the content endsets (0.1, 0.2) and the **TYPE** endset (0.3). Per [SS-ADDRESS-SPACE] Finding 0024, the type slot points to the bootstrap document's type registry (`1.0.2.x`), not to arbitrary content. It occupies its own spanfilade subspace (LINKTHREESPAN=3) and is retrieved conditionally in [SS-RETRIEVE-ENDSETS].

## Conclusion

A link can meaningfully be "followed" in either direction with equal structural validity. The semantic meaning of "source implies origin, target implies destination" is application-level convention, enforced by the link type (e.g., JUMP, QUOTE) and by how the client interprets the two slots — not by any storage asymmetry. The KB contains no evidence that the backend enforces or even models directionality; it simply treats FROM and TO as slot-1 and slot-2 of the same orgl structure.

---

## Code Exploration

Now I have a complete picture. Here is my full answer:

---

## Is source/target a structural asymmetry or a naming convention?

**Both, at different layers — and the answer differs between storage and traversal.**

---

### 1. Creation: Three Parallel Slots, Hardcoded Addresses

In `docreatelink` [`do1.c:195-221`], creating a link calls two key routines:

```c
&& setlinkvsas (&fromvsa, &tovsa, &threevsa)
&& insertendsetsinorgl (taskptr, linkisaptr, link, &fromvsa, fromsporglset,
                        &tovsa, tosporglset, &threevsa, threesporglset)
&& insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset,
                         tosporglset, threesporglset)
```

**`setlinkvsas` assigns fixed, distinct V-addresses to each endset** [`do2.c:169-183`]:

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr) {
    tumblerclear (fromvsaptr);
    tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);   // → 1.x
    tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);   // → 1.1

    tumblerclear (tovsaptr);
    tumblerincrement (tovsaptr, 0, 2, tovsaptr);       // → 2.x
    tumblerincrement (tovsaptr, 1, 1, tovsaptr);       // → 2.1

    if (threevsaptr) {
        tumblerclear (threevsaptr);
        tumblerincrement (threevsaptr, 0, 3, threevsaptr);  // → 3.1
        tumblerincrement (threevsaptr, 1, 1, threevsaptr);
    }
    return (TRUE);
}
```

- **from-endset** → V-address `1.1` in the link's POOM  
- **to-endset** → V-address `2.1`  
- **three-endset** → V-address `3.1`

These addresses are not arbitrary labels — they are hardcoded into the virtual coordinate space of every link's permutation matrix.

---

### 2. Spanfilade: Three Distinct Index Columns

`insertendsetsinspanf` [`do2.c:116-128`] indexes each endset under a different span-type constant:

```c
bool insertendsetsinspanf(...) {
    insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
    && insertspanf(taskptr, spanfptr, linkisaptr, tosporglset, LINKTOSPAN)
    ...
    insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN)
}
```

The constants are defined in `xanadu.h:36-39`:

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```

Inside `insertspanf` [`spanf1.c:22`], the span-type becomes an ORGLRANGE prefix key:

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```

So the spanfilade has **three structurally distinct columns** — one per role — not one combined column with a label attached. The from-endset and to-endset exist in physically separate regions of the spanfilade address space.

---

### 3. Search: The Asymmetry Is Load-Bearing

`findlinksfromtothreesp` [`spanf1.c:56-103`] searches each spanfilade column independently, then intersects:

```c
sporglset2linkset (taskptr, spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
sporglset2linkset (taskptr, spanfptr, tosporglset, &tolinkset, orglrange, LINKTOSPAN);
sporglset2linkset (taskptr, spanfptr, threesporglset, &threelinkset, orglrange, LINKTHREESPAN);
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
```

And in `retrieveendsetsfromspanf` [`spanf1.c:190-235`]:

```c
fromspace.stream.mantissa[0] = LINKFROMSPAN;    // column 1
tospace.stream.mantissa[0] = LINKTOSPAN;         // column 2
threespace.stream.mantissa[0] = LINKTHREESPAN;   // column 3
```

These columns are not interchangeable. A query for "links from A" will not accidentally find "links to A" — they live in distinct ORGLRANGE address regions. **Swapping from/to in a query requires explicitly swapping which column you search.** There is no "reverse link" operation built into the search layer.

---

### 4. Traversal: Fully Symmetric

Despite the structural asymmetry in storage and search, **traversal is entirely symmetric and parameterized**.

`followlink` in `fns.c:114-127` passes `whichend` directly from the client:

```c
void followlink(typetask *taskptr) {
    INT whichend;
    getfollowlink (taskptr, &linkisa, &whichend)
    && dofollowlink (taskptr, &linkisa, &specset, whichend)
}
```

`dofollowlink` [`do1.c:223-232`] forwards it unchanged to `link2sporglset` [`sporgl.c:67-95`]:

```c
bool link2sporglset(typetask *taskptr, typeisa *linkisa, typesporglset *sporglsetptr, INT whichend, int type) {
    ...
    tumblerincrement (&zero, 0, whichend, &vspan.stream);  // queries V-slot whichend
    tumblerincrement (&zero, 0,        1, &vspan.width);   // unit-wide range
    context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, ...);
}
```

`whichend=1` queries the V-range `[1, 2)` → hits the from-endset stored at `1.1`.  
`whichend=2` queries `[2, 3)` → hits the to-endset stored at `2.1`.  
`whichend=3` queries `[3, 4)` → hits the three-endset at `3.1`.

The human-interactive input parser even validates all three explicitly [`get1.c:70-71`]:

```c
getnumber (taskptr, whichendptr)
&& (*whichendptr == 1 || *whichendptr == 2 || *whichendptr == 3)
```

**There is no code in the traversal path that privileges one endset over another.** A client can call `followlink` with `whichend=2` to arrive at the "to" endset, then use `retrieveendsets` to get both endsets and follow again from `whichend=1`. From the traversal machinery's perspective, the three slots are mechanically identical.

---

### Conclusion

The from/to/three distinction is **a genuine structural asymmetry at the representation level**, encoded at two independent levels:

| Layer | How the asymmetry is encoded |
|---|---|
| **POOM (orgl)** | V-addresses `1.1`, `2.1`, `3.1` assigned by `setlinkvsas` |
| **Spanfilade** | ORGLRANGE prefix columns `LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3` set by `prefixtumbler` in `insertspanf` |

It is **not** a naming convention over two structurally identical slots — the slots have distinct addresses baked into both storage structures.

**However**, the traversal operation (`followlink` / `link2sporglset`) is fully agnostic to which slot is "source" and which is "target." Any endset can be retrieved with equal mechanical validity by supplying the corresponding integer `whichend`. A link can be "followed" from the to-endset as easily as from the from-endset — the machinery does not care.

The asymmetry is therefore real and structural, but it is **semantic**, not mechanically enforced in traversal. The labels from/to/three are a contract baked into the storage addresses and search indexes, but the traversal machinery exposes all three slots symmetrically to the caller.
