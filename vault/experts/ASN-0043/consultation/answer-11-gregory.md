## Question 11 [gregory]

> A link orgl stores three endsets (source, target, type) each containing I-address spans — is the three-endset structure the minimum necessary representation, or was it designed to be extensible to N endsets, and if so, what constrains it to exactly three?

## KB Synthesis

The three-endset structure is fixed by implementation — not a minimum viable design, but also not designed for N-extensibility. Three specific constraints enforce it.

## What the KB Shows

**The V-subspace encoding is hardcoded to exactly three values.**

`setlinkvsas()` in `do2.c:169-183` constructs link orgl V-addresses by incrementing mantissa[0] to the values 1, 2, and 3 for the FROM, TO, and THREE endpoints respectively [SS-SUBSPACE-CONVENTION Finding 0038]. This is a table of three, not a loop over N. The subspace convention then propagates through the entire stack:

- Internal POOM storage: text at `1.x`, link orgl refs at `2.x`, type endpoints at `3.x`
- Spanfilade indexing constants: `LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3` [SS-RETRIEVE-ENDSETS]
- Link orgl extraction: `link2sporglset()` accepts endset position 1, 2, or 3 [SS-FOLLOWLINK Finding 0048]

**The protocol opcodes assume exactly three parameters.**

`FINDLINKSFROMTOTHREE`, `FINDNUMOFLINKSFROMTOTHREE`, and `RETRIEVEENDSETS` all take three endpoint specsets as separate parameters [SS-FIND-LINKS Finding 0035]. There is no variable-arity endset query.

## Why Three, Not Two

Two endsets (source + target) would be the structural minimum for a link. The third endset exists because **types are content references, not metadata**. Types are VSpecs into a type registry in the bootstrap document (`1.0.2.x`), with a hierarchy encoded in tumbler containment — `1.0.2.6.2` (MARGIN) nests under `1.0.2.6` (FOOTNOTE) [SS-LINK-ENDPOINT Finding 0024]. Storing types as content identity rather than enum flags means type queries can use the same I-address intersection mechanism as source/target discovery. This is architecturally consistent but requires a dedicated endset slot.

## Why Not Four

Nothing in the KB generalizes over N endsets. The tumbler hierarchy could theoretically accommodate digits 4, 5, etc. — nothing about tumbler arithmetic prevents it — but no code path loops or parameterizes over endset count. The naming "THREE" rather than "TYPE" in function names like `findlinksfromtothreesp` is telling: the third slot was conceptualized as "the third argument" rather than "the semantic type field," suggesting the designers might have intended it as a general-purpose third position rather than a locked-in type semantic. But the implementation wires all three slots at the V-subspace encoding level, making the count structurally three.

## Summary

Three is not minimum (two would suffice for bare source-target links) and not extensible (no N-endset generalization exists). It is a fixed architectural commitment: two semantic roles (source, target) plus one general-purpose third slot used for type classification, all wired into the V-subspace digit convention at `setlinkvsas()` and propagated rigidly through the spanfilade indexing and FEBE protocol.

---

## Code Exploration

I have everything needed. Here is the full answer.

---

## The Link Orgl Three-Endset Structure: Minimum Necessary or Extensible to N?

### Short Answer

The three-endset structure is **neither the minimum necessary nor designed for genuine N-way extensibility**. It was designed to stop at three, but incrementally — first two endsets, then a third added later. The implementation is fixed-arity throughout, and a concrete integer-collision barrier prevents a fourth endset without renumbering.

---

### Evidence 1: Two-endset `domakelink` predates `docreatelink`

`do1.c:169-193` contains a function `domakelink` that takes only `fromspecset` and `tospecset`:

```c
bool domakelink(typetask *taskptr, typeisa *docisaptr,
                typespecset fromspecset, typespecset tospecset,
                typeisa *linkisaptr)
```

It calls `setlinkvsas` with `NULL` for the third VSA, and `insertendsetsinorgl`/`insertendsetsinspanf` with `NULL, NULL` for the third endset pair:

```c
  && setlinkvsas (&fromvsa, &tovsa, NULL)                                         // do1.c:189
  && insertendsetsinorgl (... &fromvsa, fromsporglset, &tovsa, tosporglset, NULL, NULL) // do1.c:190
  && insertendsetsinspanf (... fromsporglset, tosporglset, NULL)                   // do1.c:191
```

The public `docreatelink` (`do1.c:195-221`) adds a third endset:

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr,
                  typespecset fromspecset, typespecset tospecset,
                  typespecset threespecset, typeisa *linkisaptr)
```

`domakelink` has no corresponding request code in `requests.h` — it is internal only. The public wire protocol exposes only `CREATELINK=27` which always passes three specsets. This means the codebase preserves the two-endset form as a relic of incremental design, but clients only ever see three.

---

### Evidence 2: The third endset is optional throughout — from and to are the mandatory minimum

`insertendsetsinspanf` (`do2.c:116-128`) makes the from+to pair mandatory and the third conditional:

```c
bool insertendsetsinspanf(..., typesporglset fromsporglset,
                               typesporglset tosporglset,
                               typesporglset threesporglset)
{
  if (!(insertspanf(taskptr,spanfptr,linkisaptr,fromsporglset,LINKFROMSPAN)
      &&insertspanf(taskptr,spanfptr,linkisaptr,tosporglset,LINKTOSPAN)))
        return (FALSE);
  if (threesporglset) {                                           // do2.c:122 — conditional
    if(!insertspanf(taskptr,spanfptr,linkisaptr,threesporglset,LINKTHREESPAN)){
        return (FALSE);
    }
  }
  return(TRUE);
}
```

`insertendsetsinorgl` (`do2.c:130-149`) has the same structure:

```c
  if (threevsa && threesporglset) {                              // do2.c:136 — conditional
        if (!insertpm (taskptr, linkisaptr, link, threevsa, threesporglset))
```

The minimum required for a valid link is two endsets. Three is the current maximum.

---

### Evidence 3: `setlinkvsas` assigns mechanically regular but fixed VSA positions

`do2.c:169-183` assigns V-stream addresses within the link's own orgl:

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
    tumblerclear (fromvsaptr);
    tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);   // 1.1
    tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);
    tumblerclear (tovsaptr);
    tumblerincrement (tovsaptr, 0, 2, tovsaptr);       // 2.1
    tumblerincrement (tovsaptr, 1, 1, tovsaptr);
    if (threevsaptr) {
        tumblerclear (threevsaptr);
        tumblerincrement (threevsaptr, 0, 3, threevsaptr);  // 3.1
        tumblerincrement (threevsaptr, 1, 1, threevsaptr);
    }
    return (TRUE);
}
```

The pattern `N.1` is mechanically regular — a fourth endset would naturally occupy `4.1`. The code checks `if (threevsaptr)` (do2.c:177), meaning the third is genuinely optional and was added as a generalization of the two-endset form. But nothing implements `4.1`.

---

### Evidence 4: The spanfilade integer namespace — `DOCISPAN=4` is the collision barrier

`xanadu.h:36-39` defines the four span type constants:

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```

The spanfilade uses these integers as the leading component of the key for each link record. A fourth link endset type would naturally want `4`, but `DOCISPAN=4` is already allocated to document content spans. This is the **hard structural barrier**: without renaming DOCISPAN (and changing its storage format throughout), there is no free integer for a fourth endset type in the spanfilade key space.

---

### Evidence 5: All query functions are fixed-arity at three

`spanf1.c:56-103`, `fns.c:189-234`, `do1.c:348-367` all encode three-endset queries end-to-end:

- `findlinksfromtothreesp(taskptr, spanfptr, fromvspecset, tovspecset, threevspecset, ...)` — `spanf1.c:56`
- `intersectlinksets(taskptr, linkset1, linkset2, linkset3, *linkset4ptr)` — `spanf2.c:46`

`intersectlinksets` takes exactly three input lists. The naming — `linkset1`, `linkset2`, `linkset3`, `*linkset4ptr` (the output pointer is called "4") — suggests the authors thought of this as "intersecting 3 sets to produce a 4th", not as "intersecting N sets". There is no loop, no count variable, no array of link sets.

---

### Evidence 6: The wire protocol encodes three exactly

`requests.h` defines:

```
#define CREATELINK              27
#define RETRIEVEENDSETS         28
#define FINDNUMOFLINKSFROMTOTHREE 29
#define FINDLINKSFROMTOTHREE    30
#define FINDNEXTNLINKSFROMTOTHREE 31
```

`fns.c:100-112` shows CREATELINK parses exactly three specsets:

```c
void createlink(typetask *taskptr)
{
  typeisa docisa, linkisa;
  typespecset fromspecset, tospecset, threespecset;
  ...
  if (
     getcreatelink (taskptr, &docisa, &fromspecset, &tospecset, &threespecset)
  && docreatelink (taskptr, &docisa, fromspecset, tospecset, threespecset, &linkisa)) {
```

`fns.c:350-362` shows RETRIEVEENDSETS returns exactly three:

```c
void retrieveendsets(typetask *taskptr)
{
  typespecset specset, fromset, toset, threeset;
  ...
  doretrieveendsets (taskptr, specset, &fromset, &toset, &threeset)
  putretrieveendsets (taskptr, fromset, toset, threeset);
```

The wire protocol has no provision for N endsets — not a count field, not a list, not a variadic encoding.

---

### Conclusion

| Constraint | Nature | Source |
|---|---|---|
| Span type integers 1, 2, 3 | Hard-coded constants | `xanadu.h:36-38` |
| `DOCISPAN=4` collision | Integer namespace exhaustion | `xanadu.h:39` |
| `setlinkvsas` VSA assignment | Fixed-arity function, not a loop | `do2.c:169-183` |
| `insertendsetsinspanf`, `insertendsetsinorgl` | Fixed-arity with 3rd conditional | `do2.c:116-149` |
| `intersectlinksets` | Fixed 3-input signature | `spanf2.c:46` |
| FEBE wire protocol | Exactly 3 specsets in/out | `requests.h`, `fns.c:100-112`, `fns.c:350-362` |

**The minimum necessary is two** — `domakelink` (`do1.c:169`) implements a 2-endset link and is structurally valid. The third endset was a semantic addition (the link-type dimension, enabling typed hyperlinks), added incrementally on top of the from/to pair.

**The design was not built for N-way extensibility**. There is no data structure, no loop, no count variable, no variadic encoding that would let a fourth endset be added without touching every layer: the constants, the function signatures, the wire protocol serialization, and the span type integer assignment. The `DOCISPAN=4` collision is the most concrete expression of this: the spanfilade integer key space for link endsets was never reserved — the document content type was immediately assigned the next available integer, closing off the sequence at three.
