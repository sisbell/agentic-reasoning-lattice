## Question 2 [evidence]

> Is retraction realized as a single K.λ step `Nullify(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1,#a))})` that emits a new link `b` — addressable in `Σ'` — whose endsets are `∅` (from), a to-endset targeting the link address `a`, and a type endset, none of which cover content?

## KB Synthesis

The question cannot be answered from the KB. No KB entry describes "retraction" as a named operation, and the `K.λ` formalism with `Nullify` / `Emit_R` does not appear anywhere in the findings.

What the KB *does* allow me to say about the proposed mechanism:

**The from-endset = ∅ component is feasible.** [SS-LINK-ENDPOINT] Finding 0005 confirms `find_links(NOSPECS, target_specs)` is a valid call — a link can be created with no source endpoint specified.

**The to-endset targeting link address `a` is mechanically possible but semantically anomalous.** Link `a` occupies V-position `2.x` in its home document [SS-LINK-SUBSPACE], and its ISA is the I-address stored there. A to-endset pointing at that V-position would reference the link's ISA — a link orgl ISA, not a permascroll address. From [SS-CONTENT-IDENTITY] Finding 0009, link orgl ISAs "represent object identity — they are unique references, not shareable content." They occupy a categorically different I-address sort from permascroll addresses.

**"None covering content" follows from the above** — a to-endset referencing a link ISA at `2.x` would not intersect permascroll I-addresses, making the retraction link invisible to `compare_versions` (which only operates over permascroll I-addresses [PRE-COMPARE-VERSIONS]) and undiscoverable via content-based `find_links` [SS-FIND-LINKS].

**The proposed width `δ(1, #a)` is the minimum that avoids the zero-width crash.** [PRE-ZERO-WIDTH] documents that zero-width endpoints crash the backend (Bug 0017); width ≥ 1 is required for link creation.

**However, whether the proposed formula correctly models retraction as the system intends** cannot be determined from the KB. The KB establishes [INV-LINK-PERMANENCE] — links have no `DELETELINK` operation and exist forever — so any "retraction" could only be a semantic convention carried by a meta-link, not a mechanical deletion. Whether Xanadu's design specifies exactly the `Nullify(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1,#a))})` formulation is outside the KB's scope.

---

## Code Exploration

I now have all the code I need. Here is my full answer.

---

## Is Retraction Realized as `Nullify(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1,#a))})`?

**Short answer: No.** There is no retraction operation — no `nullify`, no `retract`, no `Nullify` — anywhere in udanax-green. The formal model you describe is not an implemented primitive; it is what *would* be needed at the client level to realize retraction using the general `createlink` machinery. Below is the full code trace.

---

### 1. No Retraction Operation in the Dispatch Table

`fns.c` is the top-level dispatch layer. Its complete set of operations [fns.c:20–432] is:

```
finddocscontaining, copy, insert, createlink, followlink,
retrievedocvspanset, rearrange, retrievev, findlinksfromtothree,
findnumoflinksfromtothree, findnextnlinksfromtothree, navigateonht,
showrelationof2versions, createnewdocument, createnewversion,
retrievedocvspan, deletevspan, retrieveendsets, xaccount,
createnode_or_account, myopen, myclose, quitxanadu
```

No entry for `retract`, `nullify`, or anything semantically equivalent. Searching every `.c` and `.h` file under `backend/` finds zero occurrences of "retract", "nullify", or "RETR" in any non-retrieval context. The operation simply does not exist.

---

### 2. What `createlink` / `docreatelink` Actually Does

The only path that creates a link is:

```
fns.c:100 createlink()
  → do1.c:195 docreatelink(taskptr, &docisa, fromspecset, tospecset, threespecset, &linkisa)
```

`docreatelink` [do1.c:195–221]:
1. `createorglingranf` — allocates a fresh ISA (`linkisaptr`) for the new link in the granfilade [do1.c:209]
2. `tumbler2spanset` — makes an I-span from the link's own ISA [do1.c:210]
3. `findnextlinkvsa` — finds the next free V-slot in the link subspace of `docisa` [do1.c:211]
4. `docopy` — installs the link's ISA into the document's POOM at that slot [do1.c:212]
5. `specset2sporglset` × 3 — converts from/to/three specsets to sporglsets [do1.c:214–216]
6. `setlinkvsas` — assigns fixed internal V-slots for the three endsets [do1.c:217]
7. `insertendsetsinorgl` — stores endsets in the link's own POOM [do1.c:218]
8. `insertendsetsinspanf` — stores endsets in the global spanfilade for link-following queries [do1.c:219]

The formal model's `Emit_R` is exactly a call to `docreatelink` with `fromspecset = NULL`, a `tospecset` targeting `a`, and a `threespecset` naming the retraction type. Below I verify each component.

---

### 3. Empty From-Endset (∅) — Mechanically Handled, Not Enforced

**`specset2sporglset` with NULL** [sporgl.c:14–33]:

```c
bool specset2sporglset(typetask *taskptr, typespecset specset,
                       typesporglset *sporglsetptr, int type) {
    *sporglsetptr = NULL;             // [sporgl.c:18] initialise output to NULL
    for (; specset; specset = ...) { // [sporgl.c:19] loop never executes if specset=NULL
        ...
    }
    *sporglsetptr = NULL;             // [sporgl.c:30]
    return (TRUE);                    // [sporgl.c:32] returns TRUE
}
```

Passing `fromspecset = NULL` produces `fromsporglset = NULL` and returns `TRUE`. No crash, no error.

**`insertpm` with NULL sporglset** [orglinks.c:75–134]:

```c
if (iszerotumbler (vsaptr)) {       // [orglinks.c:86] guard check
    return (FALSE);
}
...
logbertmodified(orglisa, user);      // [orglinks.c:99] marks doc modified
for (; sporglset; sporglset = ...) { // [orglinks.c:100] loop: 0 iterations if NULL
    unpacksporgl(...);
    insertnd(...);
}
return (TRUE);
```

`fromvsa` is set by `setlinkvsas` [do2.c:169–173]:

```c
tumblerclear (fromvsaptr);
tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);  // mantissa[0] = 1
tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);  // mantissa[1] = 1 → "1.1"
```

`fromvsa = (mantissa[0]=1, mantissa[1]=1)` is non-zero, so the guard at [orglinks.c:86] passes. The loop runs zero times. `insertnd` is never called. Returns `TRUE`. **No POOM entry is written for the from-endset.**

**`insertspanf` with NULL sporglset** [spanf1.c:15–53]:

```c
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]); // [spanf1.c:22]
for (; sporglset; sporglset = ...) { // [spanf1.c:25] loop: 0 iterations
    ...
    insertnd(taskptr,...,SPANRANGE);
}
return (TRUE);
```

No entry written to the global spanfilade for `LINKFROMSPAN=1`. Returns `TRUE`.

**Net result: a link with a genuinely empty from-endset can be created.** It will have no `LINKFROMSPAN` entries in either the link's POOM or the spanfilade. Such a link cannot be found by a `findlinksfromtothree` query that specifies a from-set; it can only be found by its to-set or three-set.

---

### 4. To-Endset Targeting Link Address `a` — `{(a, δ(1,#a))}`

`δ(1, #a)` denotes a span of unit width at the ISA level of `a`. In udanax-green terms, this is a one-crum I-span over `a`'s ISA.

**Two ways to express this as a specset:**

**(a) As an ISPANID (direct I-span):** Pass an ispan with `stream = a.isa`, `width = 1-at-ISA-depth`. `specset2sporglset` [sporgl.c:20–22] handles ISPANID directly:

```c
if (((typeitemheader *)specset)->itemid == ISPANID) {
    *sporglsetptr = (typesporglset)specset;  // use directly as sporglset
    ...
}
```

**(b) As a VSPECID (V-span in document):** Link `a`'s V-slot within `d_retr` is allocated by `findnextlinkvsa` [do2.c:151–167]:

```c
tumblerclear (&firstlink);
tumblerincrement (&firstlink, 0, 2, &firstlink);  // mantissa[0] = 2
tumblerincrement (&firstlink, 1, 1, &firstlink);  // mantissa[1] = 1 → "2.1"
```

Links start at V ≥ "2.1" in the document's POOM. A vspec targeting that V-span would be converted by `vspanset2sporglset` [sporgl.c:35–65] through `vspanset2ispanset → permute` [orglinks.c:397–422] into a sporglset backed by the link's ISA.

Either form is accepted by `docreatelink`. The to-endset sporglset is then stored at `tovsa = (mantissa[0]=2, mantissa[1]=1)` inside the link's POOM, and in the global spanfilade at `LINKTOSPAN=2` [xanadu.h:37].

---

### 5. Type Endset — The `threespecset`

`setlinkvsas` [do2.c:177–182]:

```c
tumblerclear (threevsaptr);
tumblerincrement (threevsaptr, 0, 3, threevsaptr);  // mantissa[0] = 3
tumblerincrement (threevsaptr, 1, 1, threevsaptr);  // mantissa[1] = 1 → "3.1"
```

The three-endset is stored at `LINKTHREESPAN=3` [xanadu.h:38]. `insertendsetsinspanf` [do2.c:122–127] guards insertion:

```c
if (threesporglset) {
    if (!insertspanf(..., linkisaptr, threesporglset, LINKTHREESPAN)) {
        return (FALSE);
    }
}
```

A non-null `threespecset` is stored; a null one is silently skipped. The type endset for "retraction" would need to be supplied by the client — there is no built-in type code or registry for retraction in the backend.

---

### 6. "None Cover Content" — Correct, But for Structural Reasons

The V-space within a document's POOM separates:

- **Text crums** — `istextcrum` [orglinks.c:246–253]: `cdsp.dsas[V].mantissa[1] == 0` (integer V-positions)
- **Link crums** — `islinkcrum` [orglinks.c:255–261]: `mantissa[0] == 1 && mantissa[1] != 0` (positions in the 1.n sub-range in the link's local frame)

The V-space filter in `filter_vspanset_to_text_subspace` [do1.c:386–411] explicitly excludes link-subspace addresses from version comparison:

```c
/* Link references at V-position 0.x are document metadata, not
 * transcludable content. They have unique ISAs, not permascroll addresses,
 * so comparing them is semantically undefined. */       // [do1.c:379–382]
```

`findnextlinkvsa` allocates link slots at V ≥ "2.1" (mantissa[0]=2), which is past the text subspace (V ≥ 1.0 by `filter_vspanset_to_text_subspace`'s criterion). A to-endset targeting `a`'s link slot is addressing document metadata, not transcludable content. The from-endset is empty (∅). The type endset targets a type-descriptor structure. **None of the three endsets of the proposed retraction link cover content**, consistent with the formal model.

---

### 7. New Link `b` Is Addressable in `Σ'`

`createorglingranf` [do1.c:209] assigns a fresh permanent ISA to the new link. `putcreatelink(taskptr, &linkisa)` [fns.c:109] returns it to the FEBE client. The link is immediately addressable by its ISA in the evolved state `Σ'`. This part of the formal model is correct.

---

### Verdict

The formal step `Nullify(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1,#a))})` is **not realized in the backend**. It is absent from the dispatch table [fns.c:20–432]. The machinery that would underlie it — `docreatelink` with `fromspecset = NULL`, a to-specset targeting `a`, and a type specset — works mechanically (the NULL sporglset paths in `specset2sporglset`, `insertpm`, and `insertspanf` all return TRUE without crashing or writing entries), but:

1. No FEBE message type for retraction is defined. No `get_retract` / `do_retract` / `put_retract` triple exists.
2. No semantic enforcement distinguishes a link that happens to have an empty from-endset from a retraction link. The backend does not know what "retraction" means.
3. The `threespecset` (type endset) that would mark the link as a retraction must be chosen and enforced entirely by client convention.

Retraction, if realized at all, would be a **client-level protocol convention** built on `createlink` — not a K.λ primitive in the backend. The backend provides the substrate but not the semantic. The step as formalized does not exist in the implementation.
