## Question 14 [evidence]

> Does CREATELINK index the endset I-spans in the spanfilade via `insertendsetsinspanf`, and does it write a separate spanfilade entry for each of the three endsets (source, target, type)?

## KB Synthesis

Yes on both counts.

**`insertendsetsinspanf` is called**

[ST-CREATE-LINK] (Finding 0012) documents the three-step compound transition:

1. Create link orgl in `granf` via `createorglingranf()`
2. Copy the link's ISA into the document's `2.x` subspace via `docopy()`
3. Index all link endpoints in `spanf` via `insertendsetsinspanf()`

The code reference at `do2.c:116-128` confirms `insertendsetsinspanf()` inserts from/to/three sporglsets.

**Separate spanfilade entries for each of the three endsets**

[INT-SPORGL-LINK-INDEX] (Finding 0013) specifies the mechanism: each endpoint type is converted to a sporglset and inserted into the spanf tagged with the link's ISA and endpoint type. [SS-RETRIEVE-ENDSETS] (Finding 0035) confirms the three endsets occupy distinct ORGLRANGE subspaces:

- `LINKFROMSPAN = 1` (source/from)
- `LINKTOSPAN = 2` (target/to)
- `LINKTHREESPAN = 3` (type)

This is what makes RETRIEVEENDSETS work: it searches each ORGLRANGE prefix independently to return the three endsets separately. [ST-CREATE-LINK] (Finding 0012) notes this write to both enfilades is the only documented compound operation — all other operations touch only one enfilade.

---

## Code Exploration

I now have everything verified from the actual source. Here is the complete answer.

---

## Does CREATELINK Index Endset I-Spans via `insertendsetsinspanf`?

**Yes, unambiguously.** And yes, it calls `insertspanf` separately for each of the three endsets — with a conditional guard on the third.

---

## Execution Path

### 1. Entry: `fns.c:100–112`

```c
void createlink(typetask *taskptr)
{
    if (
       getcreatelink (taskptr, &docisa, &fromspecset, &tospecset, &threespecset)
    && docreatelink (taskptr, &docisa, fromspecset, tospecset, threespecset, &linkisa)){
        putcreatelink (taskptr, &linkisa);
    }else
        putrequestfailed (taskptr);
}
```

`fns.c:108` calls `docreatelink()` with all three specsets (source, target, type).

---

### 2. Core logic: `do1.c:195–221`

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr,
                  typespecset fromspecset, typespecset tospecset,
                  typespecset threespecset, typeisa *linkisaptr)
{
    ...
    && specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)  // line 214
    && specset2sporglset (taskptr, tospecset, &tosporglset, NOBERTREQUIRED)      // line 215
    && specset2sporglset (taskptr, threespecset, &threesporglset, NOBERTREQUIRED)// line 216
    && setlinkvsas (&fromvsa, &tovsa, &threevsa)                                 // line 217
    && insertendsetsinorgl (taskptr, linkisaptr, link,
                            &fromvsa, fromsporglset, &tovsa, tosporglset,
                            &threevsa, threesporglset)                           // line 218
    && insertendsetsinspanf (taskptr, spanf, linkisaptr,
                             fromsporglset, tosporglset, threesporglset)         // line 219
}
```

`do1.c:219` is the direct call to `insertendsetsinspanf`, passing all three sporglsets.

---

### 3. Spanfilade indexing: `do2.c:116–128`

```c
bool insertendsetsinspanf(typetask *taskptr, typespanf spanfptr, typeisa *linkisaptr,
                          typesporglset fromsporglset, typesporglset tosporglset,
                          typesporglset threesporglset)
{
    bool insertspanf();
    if (!(
        insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)  // line 119
      && insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN))) // line 120
        return (FALSE);
    if (threesporglset) {                                                        // line 122
        if (!insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN)) // line 123
            return (FALSE);
    }
    return (TRUE);
}
```

Three separate calls to `insertspanf`, one per endset. The third call (`LINKTHREESPAN`) is **conditional**: it only fires if `threesporglset` is non-NULL (`do2.c:122`). If the caller passes a null type specset, no type-endset entry is written to the spanfilade at all.

---

### 4. Individual entry creation: `spanf1.c:15–53`

```c
bool insertspanf(typetask *taskptr, typespanf spanfptr, typeisa *isaptr,
                 typesporglset sporglset, INT spantype)
{
    prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);  // line 22
    tumblerclear  (&crumwidth.dsas[ORGLRANGE]);
    clear (&linfo, sizeof(linfo));
    for (; sporglset; sporglset = ...) {
        if (itemid == ISPANID) { ... }
        else if (itemid == SPORGLID) { ... }
        else if (itemid == TEXTID) { ... }
        movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);        // line 49
        movetumbler (&lwidth,  &crumwidth.dsas[SPANRANGE]);
        insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE); // line 51
    }
    return (TRUE);
}
```

Each call to `insertspanf` is keyed by `spantype` (`LINKFROMSPAN`, `LINKTOSPAN`, or `LINKTHREESPAN`), which is embedded into the ORGL-range dimension of the 2D crum key at `spanf1.c:22` via `prefixtumbler`. This is what distinguishes the three endsets in the spanfilade's key space. For each I-span item in the sporglset, `insertnd` (`spanf1.c:51`) writes one spanfilade node.

---

## Summary

| Call site | Function | `spantype` arg | Conditional? |
|-----------|----------|----------------|--------------|
| `do2.c:119` | `insertspanf(... fromsporglset, LINKFROMSPAN)` | `LINKFROMSPAN` | No — always |
| `do2.c:120` | `insertspanf(... tosporglset, LINKTOSPAN)` | `LINKTOSPAN` | No — always |
| `do2.c:123` | `insertspanf(... threesporglset, LINKTHREESPAN)` | `LINKTHREESPAN` | **Yes** — only if `threesporglset != NULL` |

The spanfilade uses a 2D key: the ORGL dimension encodes `(link-ISA, spantype)` and the SPAN dimension encodes the I-span address. Each of the three endsets gets its own prefix in the ORGL key space, making the three endset populations independently queryable. This is exactly the structure that `findlinksfromtothreesp` (`spanf1.c:56`) relies on when it calls `sporglset2linkset` with `LINKFROMSPAN`, `LINKTOSPAN`, and `LINKTHREESPAN` separately, then intersects the three result sets (`spanf1.c:77`, `spanf1.c:85`, `spanf1.c:93`, `spanf1.c:100`).
