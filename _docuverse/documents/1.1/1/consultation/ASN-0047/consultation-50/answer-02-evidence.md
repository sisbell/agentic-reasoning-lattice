## Question 2 [evidence]

> Does the udanax-green link-arrangement protocol (e.g., the link-placement pathway invoked alongside `docreatelink`) prevent a single link ISA from being mapped to more than one VSA within the same document, or can the same link appear at multiple link-subspace positions?

## KB Synthesis

## Link ISA to VSA Cardinality Within a Document

The standard link-placement pathway produces **one VSA per link ISA per `docreatelink` call**, but the underlying POOM provides no enforcement preventing multiple mappings.

### What the placement pathway does

`docreatelink` [ST-CREATE-LINK, Finding 0052] follows this sequence for each new link:

1. `createorglingranf()` — allocates a **fresh, unique** link ISA
2. `findnextlinkvsa()` — computes exactly one insertion point: `2.1` for the first link, or `vspanreach` for subsequent ones [SS-LINK-SUBSPACE]
3. `docopy()` — inserts the ISA reference at that **single** position

Because each call allocates a distinct ISA and appends it at the current document end, the protocol naturally produces a 1:1 mapping between link ISAs and link-subspace V-positions for sequential operation.

### Why the POOM doesn't enforce it

The POOM is structurally a **multimap**: a single I-address may appear at multiple V-positions [SS-POOM-MULTIMAP, Finding 0039]. `docopy` performs no duplicate checking [PRE-COPY, Finding 0046] — if the same link ISA were passed to `docopy` twice with different 2.x target positions, both entries would be accepted silently.

Additionally, `acceptablevsa()` is a no-op stub that unconditionally returns `TRUE` [INV-SUBSPACE-CONVENTION, Finding 0010], so no placement guard exists at the storage layer.

### Conclusion

The link-arrangement protocol as implemented (*`docreatelink` → `findnextlinkvsa` → single `docopy`*) yields exactly one VSA per link ISA per invocation. However, this is a **caller-enforced convention**, not a POOM invariant — the same link ISA could be mapped to multiple 2.x positions if `docopy` were called directly with the same ISA twice. The system would accept it, and both V-positions would resolve to the same link orgl on retrieval.

---

## Code Exploration

The citations check out. Here is the complete analysis:

---

## Does the Link-Placement Pathway Prevent a Single Link ISA from Mapping to More Than One VSA?

**Short answer:** A link ISA is always mapped to exactly 2–3 fixed, hardcoded VSA starting positions (never zero, never arbitrary extras). There is no uniqueness guard, but the structure makes collisions impossible by design.

---

### Call Chain

#### 1. `fns.c` — FEBE handler `createlink`

```c
if (
   getcreatelink (taskptr, &docisa, &fromspecset, &tospecset, &threespecset)
&& docreatelink (taskptr, &docisa, fromspecset, tospecset, threespecset, &linkisa)){
    putcreatelink (taskptr, &linkisa);
```

A single `linkisa` is allocated and returned. Everything flows through `docreatelink`.

#### 2. `do1.c:208–221` — `docreatelink` (3-endpoint form)

```c
return (
     createorglingranf (taskptr, granf, &hint, linkisaptr)    // line 209 — one ISA allocated
  && findnextlinkvsa   (taskptr, docisaptr, &linkvsa)         // line 211 — doc-level VSA for the copy
  && docopy            (taskptr, docisaptr, &linkvsa, ispanset)
  && findorgl          (taskptr, granf, linkisaptr, &link, NOBERTREQUIRED)
  && setlinkvsas       (&fromvsa, &tovsa, &threevsa)          // line 217 — hardcoded VSA assignment
  && insertendsetsinorgl (taskptr, linkisaptr, link,
                          &fromvsa, fromsporglset,
                          &tovsa,   tosporglset,
                          &threevsa,threesporglset)           // line 218
  && insertendsetsinspanf(taskptr, spanf, linkisaptr,
                          fromsporglset, tosporglset,
                          threesporglset)                     // line 219
);
```

The ISA is created once (`createorglingranf`), and VSA positions are assigned once (`setlinkvsas`). The same `linkisaptr` is used for both the orgl-insertion and the spanf-insertion.

#### 3. `do2.c:169–182` — `setlinkvsas` — where VSAs are fixed

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
    tumblerclear (fromvsaptr);
    tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);   // fromvsa = 1.1
    tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);
    tumblerclear (tovsaptr);
    tumblerincrement (tovsaptr, 0, 2, tovsaptr);       // tovsa  = 2.1
    tumblerincrement (tovsaptr, 1, 1, tovsaptr);
    if (threevsaptr) {
        tumblerclear (threevsaptr);
        tumblerincrement (threevsaptr, 0, 3, threevsaptr); // threevsa = 3.1
        tumblerincrement (threevsaptr, 1, 1, threevsaptr);
    }
    return (TRUE);
}
```

The three starting VSAs are **literal constants**: 1.1, 2.1, 3.1. This is called exactly once per link. Every link creation produces the same three starting positions regardless of document content or history.

#### 4. `do2.c:130–146` — `insertendsetsinorgl` — three `insertpm` calls, one ISA

```c
bool insertendsetsinorgl(... tumbler *fromvsa, typesporglset fromsporglset,
                             tumbler *tovsa,   typesporglset tosporglset,
                             tumbler *threevsa, typesporglset threesporglset)
{
    if (!( insertpm(taskptr, linkisaptr, link, fromvsa,   fromsporglset)  // line 132
        && insertpm(taskptr, linkisaptr, link, tovsa,     tosporglset)))  // line 133
            return (FALSE);
    if (threevsa && threesporglset)
        if (!insertpm(taskptr, linkisaptr, link, threevsa, threesporglset)) // line 137
            return (FALSE);
```

The **same ISA** (`linkisaptr`) is inserted at three **distinct** starting VSAs. The link gets 2–3 VSA regions, not 1.

#### 5. `orglinks.c:75–133` — `insertpm` — VSA advances sequentially within each region

```c
for (; sporglset; sporglset = sporglset->xxxxsporgl.next) {   // line 100 — loop over endpoints
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
    movetumbler (vsaptr, &crumorigin.dsas[V]);                // line 113 — current VSA
    ...
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V); // line 130
    tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);          // line 131 — advance VSA
}
```

Within each starting VSA (1.1, 2.1, 3.1), if the sporglset contains multiple endpoint items, they are stored at sequential sub-positions with the VSA advancing by width after each. No two items share the same VSA position because the advance happens unconditionally before the next iteration.

#### 6. `spanf1.c:15–54` — `insertspanf` — ISA is prefixed once, outside the loop

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);  // line 22 — once, outside loop
tumblerclear (&crumwidth.dsas[ORGLRANGE]);
for (; sporglset; ...) {                                        // line 25 — loop over endpoints
    ...
    insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE); // line 51
}
```

The ORGL-range coordinate (derived from the ISA) is fixed for the entire call; only the SPAN-range coordinate varies per endpoint item.

---

### The Structural Answer

The protocol does **not** contain an explicit uniqueness guard. There is no lookup before insertion that checks "does this ISA already have a VSA?" Instead, non-duplication is enforced structurally:

| Structural fact | Where it comes from |
|---|---|
| One ISA allocated per link | `createorglingranf` called once at `do1.c:209` |
| Fixed VSA starting positions 1.1 / 2.1 / 3.1 | Hardcoded in `setlinkvsas` at `do2.c:169–182` |
| `setlinkvsas` called exactly once per link | `do1.c:217` — single call site in the `&&`-chain |
| VSA advances after each endpoint, never resets within a region | `orglinks.c:131` — `tumbleradd` unconditional |
| `insertendsetsinorgl` called exactly once per link | `do1.c:218` — single call site |

**A single link ISA is always mapped to exactly 2 or 3 VSA positions** (never just one, never more than three), corresponding to its "from," "to," and optional "three" endpoint roles. The three starting VSAs are the same literal constants for every link ever created. The code does not support placing the same link ISA at any additional or alternative VSA position — there is simply no code path that would cause `setlinkvsas` to be called a second time for the same link, and no path that accepts caller-supplied VSA values.

The same link **can** occupy a range of contiguous VSA addresses within each slot (one address per endpoint item in the sporglset, advancing by width), but the slot origins are always 1.1, 2.1, and 3.1.
