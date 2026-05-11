## Question 2 [evidence]

> Does the udanax-green implementation ever permit (or actively prevent) an arrangement entry whose V-position lies in the text subspace from mapping to an I-address allocated in the link subspace (or vice versa), and is there code that enforces or assumes V/I subspace alignment?

## KB Synthesis

## V/I Subspace Alignment: Permission, Prevention, and Assumptions

### Short answer

The implementation **never enforces** V/I subspace alignment. It is a caller-maintained convention with no runtime checks. Several code paths **assume** alignment and produce silent corruption or crashes when it is violated. One structural mechanism (the two-blade knife) **incidentally prevents V-position shifts from crossing** subspace boundaries during INSERT, but this is not a placement guard.

---

### What the convention requires

By convention [SS-SUBSPACE-CONVENTION]:
- V=1.x entries must map to **permascroll I-addresses** (text content)
- V=2.x entries must map to **link orgl ISAs**
- V=3.x entries must map to **link type endpoint ISAs**

The I-address ranges are structurally distinct too: text I-addresses live under `doc.3.x`, link orgl ISAs under `doc.2.x` [SS-ADDRESS-SPACE, Finding 0065].

---

### Is misalignment permitted?

**Yes, completely.** The storage layer is type-agnostic end-to-end [SS-DUAL-ENFILADE, Finding 0011]:

- `acceptablevsa()` in `do2.c:110-113` unconditionally returns `TRUE` — the stub intended to enforce placement was never implemented [PRE-INSERT, Finding 0049; PRE-SUBSPACE-CONVENTION, Finding 0010]
- `insertpm`, `docopy`, `retrieverestricted`, and `permute` treat all V→I mappings identically
- I-addresses have no runtime type tag — both permascroll addresses and link orgl ISAs are untyped tumblers [SS-DUAL-ENFILADE, Finding 0011]

Experimentally confirmed violation paths:
1. **INSERT at V=2.1 with text** succeeds and is retrievable [PRE-INSERT, Finding 0049]
2. **REARRANGE** with cross-subspace cuts moves text from 1.x to 2.x [PRE-REARRANGE, Finding 0051; SS-SUBSPACE-CONVENTION]
3. **VCOPY** of a mixed vspanset copies link ISAs into text positions [PRE-VCOPY, Finding 0010]

---

### Code that assumes alignment (and breaks when violated)

| Location | Assumption | Failure mode |
|---|---|---|
| `ispanset2vstuffset` | All I-addresses are permascroll | NULL/garbage bytes for link ISAs [SS-DUAL-ENFILADE, Finding 0011] |
| `correspond.c` (compare_versions) | Input V-spans → permascroll I-addresses | Crash/abort when link-subspace spans included [EC-COMPARE-VERSIONS-LINK-CRASH; PRE-COMPARE-VERSIONS] |
| `findnextlinkvsa` (`do2.c:151-167`) | Link positions always at 2.x | Hardcodes link placement; no guard against pre-existing text there [SS-LINK-SUBSPACE] |
| `doinsert` element type | TEXTATOM content targets 1.x | Sets TEXTATOM hint but V-position is unchecked [PRE-ENF0-PLACEMENT-GAP, Finding 0049] |

---

### The one structural mechanism: the two-blade knife

The closest thing to an alignment enforcement is `findaddressofsecondcutforinsert()` in `insertnd.c:174-183` [SS-TWO-BLADE-KNIFE; FC-SUBSPACE, Finding 0054]:

For any INSERT at `N.x`, the second knife blade is always `(N+1).1`. This restricts the **shift region** to `[N.x, (N+1).1)`, so:
- INSERT at 1.x shifts only entries in [1.x, 2.1) — leaves 2.x entries unshifted
- INSERT at 2.x shifts only entries in [2.x, 3.1) — leaves 1.x entries unshifted

**But this is a shift guard, not a placement guard.** It prevents existing correctly-placed entries from being displaced across boundaries; it does nothing to prevent a caller from placing a link ISA at 1.x in the first place.

DELETE's subspace isolation is even more incidental — it depends on `strongsub`'s exponent guard returning cross-subspace entries unchanged, not on any deliberate design [FC-SUBSPACE, Finding 0055; INT-DELETE-SUBSPACE-ASYMMETRY].

---

### Summary

No code actively prevents a POOM entry at V=1.x from mapping to a link-orgl I-address or vice versa. The convention is maintained entirely by caller discipline. The spec must model subspace membership as a **precondition on every V-position-accepting operation** (`requires vpos.head == 1` for text, `requires vpos.head == 2` for links), with proof obligations that each well-formed operation preserves it — because the implementation provides no enforcement [INV-SUBSPACE-CONVENTION; PRE-ENF0-PLACEMENT-GAP].

---

## Code Exploration

I now have everything I need from the source. Let me compose the full answer.

---

## V/I Subspace Alignment in udanax-green

### Short Answer

Udanax-green **never validates** that a V-position and its corresponding I-address occupy compatible subspaces. Subspace separation is enforced only through the *path by which content reaches the arrangement*: text takes one path, link references take another. Nothing prevents a caller from using `docopy` to install a mismatched (V-subspace, I-subspace) arrangement entry. The only active filtering happens post-insertion, during version comparison (Bug 009 semantic fix).

---

### 1. Subspace Topology

**`backend/orglinks.c:29-48`** — `findvsatoappend` divides the V-space at 2.0:

```c
tumblerclear (&linkspacevstart);
tumblerincrement (&linkspacevstart, 0, 2, &linkspacevstart);   // linkspacevstart = 2
```

- V < 2.0 → **text subspace**. Text is appended here.
- V ≥ 2.0 → **link subspace**. Link-object ISAs are referenced here.

Within a *link object's own* permutation matrix, the three endpoint sets have fixed V-addresses. **`backend/do2.c:169-183`** — `setlinkvsas`:

```c
tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);  // 1
tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);  // 1.1  (FROM)

tumblerincrement (tovsaptr, 0, 2, tovsaptr);      // 2
tumblerincrement (tovsaptr, 1, 1, tovsaptr);      // 2.1  (TO)

tumblerincrement (threevsaptr, 0, 3, threevsaptr); // 3
tumblerincrement (threevsaptr, 1, 1, threevsaptr); // 3.1  (THREE)
```

`istextcrum` and `islinkcrum` [**`orglinks.c:246-261`**] label individual crums inside the enfilade for width-computation purposes only:

```c
bool istextcrum(typecorecrum *crumptr)
{
    if(crumptr->cdsp.dsas[V].mantissa[1] == 0 && is1story(&crumptr->cwid.dsas[V]))
        return TRUE;
    return FALSE;
}

bool islinkcrum(typecorecrum *crumptr)
{
    // "if the whold crum is displaced into link space it is a link crum
    //  this is true if the tumbler is a 1.n tumbler where n!= 0"
    if(crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0)
        return TRUE;
    return FALSE;
}
```

These classifications drive `maxtextwid` [**`orglinks.c:224-245`**] — they are read-only labels for structural traversal, **not insertion guards**.

---

### 2. The Gate That Does Not Exist: `acceptablevsa`

Every insertion operation — `docopy` [**`do1.c:53-64`**] and `docopyinternal` [**`do1.c:74-81`**] — calls `acceptablevsa` before writing to the arrangement:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);                      // do2.c:110-113
}
```

Unconditional `TRUE`. No subspace check, no range check, no type check. This is the only V-address validation call in both copy paths, and it validates nothing.

---

### 3. `insertpm`: Cross-Subspace Insertion Is Silent

**`backend/orglinks.c:75-134`** — `insertpm` takes a V-address (`vsaptr`) and an I-address (`lstream`/`lwidth`, unpacked from `sporglset`) as separate inputs, then installs them together in the arrangement:

```c
for (; sporglset; ...) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
    movetumbler (&lstream, &crumorigin.dsas[I]);   // I-address from content
    movetumbler (&lwidth,  &crumwidth.dsas[I]);
    movetumbler (vsaptr,   &crumorigin.dsas[V]);   // V-address from caller
    ...
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
}
```

There is no comparison of `vsaptr` against `lstream`. No check that both come from the same subspace. The arrangement entry is written unconditionally. The only guard is [**`orglinks.c:86-98`**] that rejects a zero or negative V-address entirely — a range check, not a subspace check.

---

### 4. `permute` / `vspanset2ispanset` / `ispan2vspanset`: Conversion Is Blind

**`orglinks.c:389-422`**:

```c
typevspanset *ispan2vspanset(...) {
    return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
}
typeispanset *vspanset2ispanset(...) {
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
typespanset *permute(...) {
    for (; restrictionspanset; ...) {
        targspansetptr = span2spanset(...);
    }
    return (save);
}
```

`permute` simply walks the enfilade and translates spans from one coordinate space to the other. It has no awareness of subspace membership. If the arrangement contains a cross-subspace entry — text V-address mapping to a link ISA — `permute` will happily return the translated span.

---

### 5. How Separation Is *Actually* Maintained

Subspace alignment is preserved structurally by two routing functions that are always called before insertion, not by any validation gate:

- **`findvsatoappend`** [**`orglinks.c:29-49`**] — always places new text at V < 2.0.
- **`findnextlinkvsa`** [**`do2.c:151-167`**] — always places link-object ISAs at V ≥ 2.1.

These ensure that the *normal* operations (`doappend`, `domakelink`, `docreatelink`) never produce cross-subspace entries. But both functions merely compute a V-address and return it; they impose no barrier on callers who specify their own V-address through `docopy` directly.

`docreatelink` [**`do1.c:195-221`**] illustrates the design: `findnextlinkvsa` finds the correct V-address for the link reference, then hands that address to `docopy`, which calls `acceptablevsa` (always TRUE), then `insertpm` (no subspace check). The invariant lives entirely in the *choice of address*, not in any downstream guard.

---

### 6. One Post-Hoc Filter: Version Comparison

The only code that actively enforces a subspace boundary is the Bug 009 semantic fix in **`do1.c:386-449`**:

```c
typevspanset filter_vspanset_to_text_subspace(typetask *taskptr, typevspanset vspanset)
{
    tumblerclear(&text_subspace_start);
    tumblerincrement(&text_subspace_start, 0, 1, &text_subspace_start);  // 1.0

    for (; vspanset; vspanset = vspanset->next) {
        if (tumblercmp(&vspanset->stream, &text_subspace_start) >= EQUAL) {
            // keep — text subspace
        }
        // V < 1.0 — drop ("link subspace" per the fix comment)
    }
    return result;
}

bool doshowrelationof2versions(...) {
    filter_specset_to_text_subspace(taskptr, version1);
    filter_specset_to_text_subspace(taskptr, version2);
    ...
}
```

This is not a prevention of cross-subspace arrangement entries; it is a selective reader that ignores V < 1.0 spans when computing version relationships. Its comment acknowledges the semantic issue: content at those V-positions "have unique ISAs, not permascroll addresses, so comparing them is semantically undefined."

---

### Summary

| Code site | Role | Subspace validation? |
|---|---|---|
| `acceptablevsa` [do2.c:110] | V-address gate before `insertpm` | None — always returns `TRUE` |
| `insertpm` [orglinks.c:75] | Writes (V, I) crum into arrangement | None — V and I paired directly |
| `permute` [orglinks.c:404] | V↔I conversion via arrangement | None — pure traversal |
| `findvsatoappend` [orglinks.c:29] | Selects V-address for text append | Ensures V < 2.0, not a guard |
| `findnextlinkvsa` [do2.c:151] | Selects V-address for link reference | Ensures V ≥ 2.1, not a guard |
| `setlinkvsas` [do2.c:169] | Assigns endpoint V-addresses in link objects | Hard-codes 1.1 / 2.1 / 3.1, not a guard |
| `istextcrum`/`islinkcrum` [orglinks.c:246] | Labels crums | Read-only, used for width computation only |
| `filter_vspanset_to_text_subspace` [do1.c:386] | Version-comparison filter | Active post-hoc filter only for `doshowrelationof2versions` |

**Conclusion:** Udanax-green assumes V/I subspace alignment; it does not enforce it. Subspace separation is maintained by the convention that only `findvsatoappend` and `findnextlinkvsa` determine V-addresses for the canonical operations. Nothing in `insertpm`, `acceptablevsa`, `docopy`, or the V↔I conversion layer would detect or reject an arrangement entry that maps a text V-position to a link I-address or vice versa. The architecture trusts the insertion paths rather than validating the resulting arrangement structure.
