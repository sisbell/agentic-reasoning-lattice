## Question 1 [evidence]

> In udanax-green, does any link-placement path other than the MAKELINK-equivalent ever set a document's first link-subspace V-position at depth ≥ 3, or is the link-subspace depth always 2?

## KB Synthesis

## Link-Subspace V-Position Depth

The KB describes exactly one link-placement path, and it always produces depth-2 V-positions.

**The only link-placement path** is `docreatelink()` → `findnextlinkvsa()` → `docopy()` [ST-CREATE-LINK, SS-DUAL-ENFILADE, SS-LINK-SUBSPACE].

`findnextlinkvsa()` (do2.c:151-167) initializes the first link at `2.1` — a 2-digit tumbler — then places subsequent links at `vspanreach`, which is the current end of the link-subspace extent [SS-LINK-SUBSPACE]. Since existing links are at `2.1`, `2.2`, `2.3`…, `vspanreach` returns `2.N+1` — still depth 2. The algorithm only increments the second digit; it never introduces additional subspace hierarchy.

`setlinkvsas()` (do2.c:169-183) confirms the same pattern: FROM endpoint at `2.1`, TO at a sequential `2.x`, TYPE endpoint in subspace `3.x` — all depth 2 [SS-SUBSPACE-CONVENTION, Finding 0038].

**No other link-placement path exists in the KB.** The KB does document two violation paths that can place content at arbitrary V-positions in the `2.x` subspace — INSERT with no subspace guard [PRE-ENF0-PLACEMENT-GAP] and REARRANGE with cross-subspace cuts [PRE-REARRANGE, Finding 0051] — but these are convention violations that place non-link bytes there, not link orgl ISAs. They could in principle produce a depth-3 V-address (e.g., `2.1.3`) in the link subspace, but the KB records no observed instance of this, and it would violate INV-SUBSPACE-CONVENTION rather than constituting a legitimate link placement.

**Conclusion:** The link-subspace V-position depth is always 2 (`2.N`) for any well-formed link-placement operation. Depth ≥ 3 in the link subspace is not achievable through any intended path and is only theoretically reachable via the two documented convention-violation routes.

---

## Code Exploration

I have all the evidence. Here is the complete answer.

---

## Link-Subspace V-Position Depth in udanax-green

**Short answer:** The link-subspace depth is always exactly 2 for all endpoint positions. The link-body (host-document) position is also depth 2 by default, but `findnextlinkvsa` contains one branch that can return a deeper result under specific preconditions.

---

### The Only Two Link-Placement Paths

There are exactly two functions that create links: `domakelink` and `docreatelink`. Checking all C source files:

- **`docreatelink`** [do1.c:195] — called from `fns.c:108` (the sole FEBE `createlink` handler)
- **`domakelink`** [do1.c:169] — defined but **never called** from any C source file (absent from all `.c` files except its own definition)

No other code path places links. The `copy` FEBE handler [fns.c:35] and `doinsert` [do1.c:87] write content to arbitrary VSAs but are content-placement paths, not link-placement paths.

---

### Endpoint V-Positions: Hardcoded Depth 2

Both functions call `setlinkvsas` [do2.c:169-183] for the within-link endpoint positions:

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
    tumblerclear (fromvsaptr);
    tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);   // mantissa[0]=1
    tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);   // mantissa[1]=1
    tumblerclear (tovsaptr);
    tumblerincrement (tovsaptr, 0, 2, tovsaptr);       // mantissa[0]=2
    tumblerincrement (tovsaptr, 1, 1, tovsaptr);       // mantissa[1]=1
    if (threevsaptr) {
        tumblerclear (threevsaptr);
        tumblerincrement (threevsaptr, 0, 3, threevsaptr);  // mantissa[0]=3
        tumblerincrement (threevsaptr, 1, 1, threevsaptr);  // mantissa[1]=1
    }
    return (TRUE);
}
```

Each endpoint tumbler has exactly **two non-zero mantissa entries** (indices 0 and 1). By `nstories` [tumble.c:249-257]:

```c
INT nstories(tumbler *tumblerptr) {
    for (i = NPLACES; i > 0 && tumblerptr->mantissa[--i] == 0;);
    return (i + 1);
}
```

`nstories` = 2 for all three. By `tumblerlength` [tumble.c:259-262]:

```c
INT tumblerlength(tumbler *tumblerptr) {
    return (nstories(tumblerptr) - tumblerptr->exp);
}
```

With `exp = 0`, `tumblerlength` = 2 for all three endpoints. The three endpoint V-positions are invariantly:

| Endpoint | mantissa[0] | mantissa[1] | Depth |
|----------|-------------|-------------|-------|
| `fromvsa` | 1 | 1 | **2** |
| `tovsa`   | 2 | 1 | **2** |
| `threevsa`| 3 | 1 | **2** |

This is identical in both `domakelink` [do1.c:189] and `docreatelink` [do1.c:217]. There is no path that passes a non-NULL `threevsaptr` with anything other than the result of `setlinkvsas`.

---

### Link-Body V-Position in the Host Document: Depth 2 by Default, With a Caveat

Both paths also call `findnextlinkvsa` [do2.c:151-167] to find where to place the link body in the hosting document:

```c
bool findnextlinkvsa(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr)
{
    tumbler vspanreach, firstlink;
    typevspan vspan;

    tumblerclear (&firstlink);
    tumblerincrement (&firstlink, 0, 2, &firstlink);   // mantissa[0]=2
    tumblerincrement (&firstlink, 1, 1, &firstlink);   // mantissa[1]=1

    (void) doretrievedocvspan (taskptr, docisaptr, &vspan);
    tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
    if (tumblercmp (&vspanreach, &firstlink) == LESS)
        movetumbler (&firstlink, vsaptr);   // branch A: use firstlink
    else
        movetumbler (&vspanreach, vsaptr);  // branch B: use vspanreach
    return (TRUE);
}
```

**Branch A** (normal): `firstlink` is mantissa[0]=2, mantissa[1]=1 → depth 2. This executes whenever the document's V-span hasn't yet reached the link subspace boundary, which is the case for any freshly created document with text-only content at typical depth-1 positions.

**Branch B** (edge case): returns `vspanreach = vspan.stream + vspan.width`. The active `absadd` [tumble.c:444-485] is **positional addition without carry**: it adds mantissa entries slot-by-slot. The result's depth = `max(depth(stream), depth(width))`. So if a client had previously placed content at a depth-3 V-position (via the `copy` or `insert` FEBE handlers with a deep VSA), `vspanreach` could be depth ≥ 3 and `findnextlinkvsa` would return that to `docreatelink` as the link-body placement position.

However, this is not a separate "link-placement path" — it is the same `docreatelink`/`domakelink` path responding to prior state. The `acceptablevsa` guard [do2.c:110-113] provides no protection:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);   // unconditional
}
```

---

### Conclusion

1. **There is no link-placement path other than `docreatelink` and `domakelink`** in the entire codebase. `domakelink` is additionally dead code at the FEBE level — it has no caller.

2. **All link endpoint V-positions** (from/to/three, inside the link object) are **invariantly depth 2**, hardcoded in `setlinkvsas` [do2.c:169-183], with no variation across any code path.

3. **The link-body V-position** in the hosting document is **depth 2 by default** (`firstlink`, branch A of `findnextlinkvsa`). It can be depth ≥ 3 only if a client has previously pushed the document's V-span past 0.2.1 via non-link content placement. This requires deliberate external action; no automatic system path creates this situation, and it affects `docreatelink` and `domakelink` equally — it is not a distinct path.

4. The link-subspace boundary is the same constant in both `findnextlinkvsa` [do2.c:156-158] and in the link-subspace detection logic in `orglinks.c`: V-positions with mantissa[0] ≥ 2 are the link zone. The depth-2 architecture is consistent throughout.
