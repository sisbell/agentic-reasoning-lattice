## Question 1 [evidence]

> Does the udanax-green content-store allocator enforce `#E(a) = 2` exactly for every `a ∈ dom(Σ.C)` (matching R0a-Cor2's link-side strengthening from `≥ 2` to `= 2`), or only the weaker `#E(a) ≥ 2` that the current scaffolding clause records?

## KB Synthesis

## Not answerable from this KB

The notation `#E(a)` and the corollary label "R0a-Cor2" do not appear anywhere in the knowledge base. Neither the `= 2` nor the `≥ 2` form of that constraint is documented in any finding.

What the KB *does* establish about reference counts on I-addresses:

**No minimum-count floor.** The POOM is explicitly a multimap — a single I-address can occupy 1 to N V-positions within a document, with no lower bound greater than 1 \[SS-POOM-MULTIMAP\]. Self-transclusion and cross-document transclusion both create additional mappings to the same I-address without limit \[EC-SELF-TRANSCLUSION, INV-IDENTITY-OVERLAP\].

**No maximum enforced by the allocator.** The granfilade allocator assigns one fresh I-address per byte, monotonically \[INV-MONOTONIC, INV-SINGLE-CHAR-GRANULARITY\], with no constraint on how many downstream references (POOM entries, DOCISPAN entries, link-endset entries) accumulate for any given address.

**Permanence, not cardinality.** The invariants concerning I-addresses speak to immutability and non-reuse \[INV-IADDR-IMMUTABILITY, INV-NO-IADDR-REUSE\], not to a required reference count.

**DOCISPAN entries are per-span, not per-byte, and are append-only** \[SS-DOCISPAN, INV-SPANF-WRITE-ONLY\]. There is no bookkeeping that counts references per address.

If R0a-Cor2 is a clause from a specification document being drafted against this KB, the KB provides no evidence for strengthening the link-side count from `≥ 2` to `= 2`. The implementation is consistent only with `#E(a) ≥ 0` (for any allocated address) or `#E(a) ≥ 1` (for any address currently live in some document's POOM), and the POOM multimap structure actively permits arbitrarily many references per address.

---

## Code Exploration

Now I have enough to give a complete and precise answer. Here it is.

---

## Does udanax-green enforce `#E(a) = 2` exactly, or only `#E(a) ≥ 2`?

**Answer: The code enforces `2 ≤ #E(a) ≤ 3`. The current scaffolding clause `#E(a) ≥ 2` is correct as a lower bound, but R0a-Cor2's strengthening to `= 2` is not enforced — nor can it be, because `docreatelink` is the sole FEBE link-creation path and it unconditionally supports a third endset.**

---

### The "content-store allocator" is not the right locus

The question names the allocator, but the allocator — `findisatoinsertgr` / `findisatoinsertmolecule` in `granf2.c` — is completely endset-agnostic. It only assigns fresh ISA positions:

```c
// granf2.c:130-156 — findisatoinsertgr
bool findisatoinsertgr(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    if (hintptr->subtype == ATOM) {
        ...
        findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);   // granf2.c:142
    } else {
        findisatoinsertnonmolecule (fullcrumptr, hintptr, isaptr); // granf2.c:152
    }
    tumblerjustify(isaptr);
    return (TRUE);
}
```

`findisatoinsertmolecule` [`granf2.c:158-181`] picks the next available address for the link atom (using `LINKATOM = 2` as `atomtype`), then returns. It has no knowledge of endsets, no assertion on their count, and no role in endset insertion whatsoever.

The endset-count constraint — whatever it is — lives entirely in `do2.c` and is invoked from `do1.c`.

---

### The actual endset-insertion chain

The only FEBE path for link creation is:

**`fns.c:createlink` → `do1.c:docreatelink` → `do2.c:insertendsetsinorgl` + `insertendsetsinspanf`**

#### `fns.c:100-112` — FEBE handler

```c
void createlink(typetask *taskptr)
{
  typeisa docisa, linkisa;
  typespecset fromspecset, tospecset, threespecset;

    if (   getcreatelink (taskptr, &docisa, &fromspecset, &tospecset, &threespecset)   // fns.c:107
    && docreatelink (taskptr, &docisa, fromspecset, tospecset, threespecset, &linkisa)){
        putcreatelink (taskptr, &linkisa);
    }else
        putrequestfailed (taskptr);
}
```

Three endpoint specsets are decoded from every `createlink` request. There is no 2-way-only path.

#### `do1.c:195-221` — `docreatelink`

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr, typespecset fromspecset, typespecset tospecset, typespecset threespecset, typeisa *linkisaptr)
{
  tumbler linkvsa, fromvsa, tovsa, threevsa;          // do1.c:198  ← threevsa always declared
  typesporglset fromsporglset, tosporglset, threesporglset;

    return (
         createorglingranf (...)
      && ...
      && specset2sporglset (taskptr, fromspecset,   &fromsporglset,   NOBERTREQUIRED)  // do1.c:214
      && specset2sporglset (taskptr, tospecset,     &tosporglset,     NOBERTREQUIRED)  // do1.c:215
      && specset2sporglset (taskptr, threespecset,  &threesporglset,  NOBERTREQUIRED)  // do1.c:216
      && setlinkvsas (&fromvsa, &tovsa, &threevsa)                                     // do1.c:217
      && insertendsetsinorgl (taskptr, linkisaptr, link,
             &fromvsa, fromsporglset, &tovsa, tosporglset,
             &threevsa, threesporglset)                                                // do1.c:218
      && insertendsetsinspanf (taskptr, spanf, linkisaptr,
             fromsporglset, tosporglset, threesporglset)                               // do1.c:219
    );
}
```

`docreatelink` always allocates a `threevsa` slot and always passes `&threevsa` (non-null) into the endset inserters.

#### `do2.c:169-183` — `setlinkvsas`

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
    tumblerclear (fromvsaptr);
    tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);   // from  → V = 0.1
    tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);   // from  → V = 0.1.1
    tumblerclear (tovsaptr);
    tumblerincrement (tovsaptr, 0, 2, tovsaptr);       // to    → V = 0.2
    tumblerincrement (tovsaptr, 1, 1, tovsaptr);       // to    → V = 0.2.1
    if (threevsaptr) {                                  // always TRUE from docreatelink
        tumblerclear (threevsaptr);
        tumblerincrement (threevsaptr, 0, 3, threevsaptr); // three → V = 0.3
        tumblerincrement (threevsaptr, 1, 1, threevsaptr); // three → V = 0.3.1
    }
    return (TRUE);
}
```

`threevsa` is always initialized to `0.3.1` when called from `docreatelink`.

---

### The enforcement gate — and what it actually checks

#### `do2.c:130-149` — `insertendsetsinorgl`

```c
bool insertendsetsinorgl(typetask *taskptr, tumbler *linkisaptr, typeorgl link,
    tumbler *fromvsa, typesporglset fromsporglset,
    tumbler *tovsa,   typesporglset tosporglset,
    tumbler *threevsa, typesporglset threesporglset)
{
    if (!( insertpm(taskptr, linkisaptr, link, fromvsa, fromsporglset)  // do2.c:132
        && insertpm(taskptr, linkisaptr, link, tovsa, tosporglset))) {  // do2.c:133
            return (FALSE);
    }
    if (threevsa && threesporglset) {                                    // do2.c:136 ← the gate
        if (!insertpm (taskptr, linkisaptr, link, threevsa, threesporglset)){
            return (FALSE);
        }
    }
    return (TRUE);
}
```

#### `do2.c:116-128` — `insertendsetsinspanf`

```c
bool insertendsetsinspanf(typetask *taskptr, typespanf spanfptr, typeisa *linkisaptr,
    typesporglset fromsporglset, typesporglset tosporglset, typesporglset threesporglset)
{
    if (!(
        insertspanf(taskptr,spanfptr,linkisaptr,fromsporglset,LINKFROMSPAN)  // do2.c:119
          &&insertspanf(taskptr,spanfptr,linkisaptr,tosporglset,LINKTOSPAN))) // do2.c:120
            return (FALSE);
    if (threesporglset) {                                                     // do2.c:122 ← the gate
        if(!insertspanf(taskptr,spanfptr,linkisaptr,threesporglset,LINKTHREESPAN)){
            return (FALSE);
        }
    }
    return(TRUE);
}
```

**The enforcement logic is identical in both functions:** from and to are unconditional; the third endset is conditional on `threesporglset` being non-null.

Since `threevsa` is always non-null (from `setlinkvsas`), the effective gate at `do2.c:136` reduces to simply `threesporglset`. So:

| `threespecset` from client | `threesporglset` after `specset2sporglset` | Endsets inserted |
|---|---|---|
| NULL / empty | NULL | `#E(a) = 2` |
| Non-empty specset | Non-null | `#E(a) = 3` |

---

### No upper-bound enforcement exists

There is no assertion, guard, or error path anywhere in `granf2.c`, `do1.c`, `do2.c`, `orglinks.c`, or `spanf1.c` that checks whether the final endset count is exactly 2. The architecture provides exactly three named slots — `LINKFROMSPAN`, `LINKTOSPAN`, `LINKTHREESPAN` — and `insertendsetsinspanf` / `insertendsetsinorgl` can fill one, two, or all three without any count-checking code.

The `domakelink` function at `do1.c:169-193` does produce exactly 2 endsets (it passes `NULL` for `threevsa` and `threesporglset`), but it is **not the FEBE path** — `fns.c:createlink` calls `docreatelink` exclusively.

---

### Conclusion

**The content-store allocator (`granf2.c`) enforces nothing about `#E(a)`.** It is purely an address-allocation mechanism with no endset semantics.

**The insertion layer (`do2.c`) enforces `#E(a) ≥ 2`** — the lower bound the scaffolding clause records. This is correct.

**R0a-Cor2's strengthening to `#E(a) = 2` is not enforced and cannot be derived from the code.** The actual invariant is `2 ≤ #E(a) ≤ 3`. Any link address `a ∈ dom(Σ.C)` created via `docreatelink` with a non-empty third specset will have `#E(a) = 3`, falsifying the `= 2` claim. The scaffolding clause's `#E(a) ≥ 2` is the strongest statement the code actually guarantees.
