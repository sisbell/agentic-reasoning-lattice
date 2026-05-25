## Question 1 [evidence]

> Does udanax-green's COMPAREVERSIONS implementation constrain restriction span widths to ordinal displacements at the document's V-position depth (width = δ(n, m)), or does it accept widths with actionPoint ≥ 2 more generally?

## KB Synthesis

The KB does not contain sufficient information to answer this question definitively.

The relevant entries for COMPAREVERSIONS are [SS-COMPARE-VERSIONS] (Finding 0015) and [PRE-COMPARE-VERSIONS] (Findings 0009, 0011, 0015). These document:

- The semantic mechanism: V-spans → I-spans via `vspanset2ispanset`, followed by I-span intersection in `correspond.c`, mapped back to V-span pairs
- The documented precondition: input V-spans must be restricted to the text subspace (`V >= 1.0`)
- The crash behavior when link-subspace spans are included ([EC-COMPARE-VERSIONS-LINK-CRASH])

[SS-SPAN] (Finding 0031) establishes that span widths are tumblers with no documented format constraint beyond being valid tumblers, and [SS-INSERT-VWIDTH-ENCODING] (Finding 0076) documents that V-widths are precision-encoded relative to V-address depth — but neither entry addresses COMPAREVERSIONS specifically.

The KB contains no findings examining whether `correspond.c` or its `retrieverestricted` call path enforces width constraints to ordinal displacements at document V-position depth, or accepts widths with higher actionPoint values. That implementation detail was not captured in the extraction findings.

---

## Code Exploration

I now have all the evidence needed for a complete answer.

---

## COMPAREVERSIONS Width Constraints: Verdict

**COMPAREVERSIONS does NOT constrain restriction span widths to ordinal displacements at the document's V-position depth. It accepts any width unconditionally — including widths with actionPoint ≥ 2 or any other actionPoint value.**

---

### The Code Path

`COMPAREVERSIONS` is protocol request code 10 (`SHOWRELATIONOF2VERSIONS`) [`requests.h:27`].

It dispatches to `showrelationof2versions` via `requestfns[SHOWRELATIONOF2VERSIONS]` [`init.c`], with handler body [`fns.c:250-261`]:

```c
void showrelationof2versions(typetask *taskptr)
{
  typespecset version1, version2;
  typespanpairset relation;
  bool getshowrelationof2versions(), doshowrelationof2versions();

    if (getshowrelationof2versions (taskptr, &version1, &version2)
     && doshowrelationof2versions (taskptr, version1, version2, &relation))
        putshowrelationof2versions (taskptr, relation);
    else
        putrequestfailed (taskptr);
}
```

---

### 1. Input Parsing: No Width Validation

`getshowrelationof2versions` [`get1fe.c:124-129`]:

```c
bool getshowrelationof2versions(typetask *taskptr, typespecset *version1ptr, typespecset *version2ptr)
{
    return (
       getspecset (taskptr, version1ptr)
    && getspecset (taskptr, version2ptr));
}
```

Both version specsets (carrying their V-spans, with stream + width tumblers) are read off the wire without any check on width depth, actionPoint, or relationship to V-position.

---

### 2. `acceptablevsa` is a Stub: Always TRUE

This function is called elsewhere to validate VSAs. Its body at [`do2.c:110-113`]:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

**No validation of any kind.** Any tumbler width passes.

---

### 3. Execution: Only Text-Subspace Filtering, No Width Check

`doshowrelationof2versions` [`do1.c:428-449`]:

```c
bool doshowrelationof2versions(typetask *taskptr, typespecset version1, typespecset version2, typespanpairset *relation)
{
    /* SEMANTIC FIX: Filter to text subspace before comparison.
     * Link references (V < 1.0) are not content with "common origin". */
    filter_specset_to_text_subspace(taskptr, version1);
    filter_specset_to_text_subspace(taskptr, version2);

    return
        specset2ispanset(taskptr, version1, &version1ispans, READBERT)
      &&    specset2ispanset(taskptr, version2, &version2ispans, READBERT)
      &&    intersectspansets(taskptr, version1ispans, version2ispans, &commonispans, ISPANID)
      &&    ispansetandspecsets2spanpairset(taskptr, commonispans, version1, version2, relation)
    ;
}
```

The `filter_specset_to_text_subspace` call at `do1.c:420-424` copies widths **unchanged** — it only gates on stream ≥ 1.0. The width tumbler passes through unmodified regardless of which mantissa position its value occupies.

---

### 4. V→I Conversion: No Depth Constraint

`vspanset2ispanset` [`orglinks.c:397-402`] delegates to `permute` → `span2spanset` → `retrieverestricted` [`retrie.c:56-85`]:

```c
typecontext *retrieverestricted(typecuc *fullcrumptr, typespan *span1ptr, INT index1, ...)
{
    movetumbler (&span1ptr->stream, &span1start);
    tumbleradd (&span1start, &span1ptr->width, &span1end);   /* retrie.c:65 */
    ...
    temp = retrieveinarea (fullcrumptr, &span1start, &span1end, index1, ...);
    return(temp);
}
```

The width is used directly in `tumbleradd` to compute the span end. There is no guard, normalization, or rejection based on which mantissa position the width occupies.

---

### 5. Where the Ordinal-Depth Constraint Does Exist: INSERT, Not COMPAREVERSIONS

The ordinal-displacement normalization appears only in `insertpm` [`orglinks.c:114-117`]:

```c
/*I'm suspissious of this shift <reg> 3/1/85 zzzz*/
shift = tumblerlength (vsaptr) - 1;
inc = tumblerintdiff (&lwidth, &zero);
tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);
```

Here, `tumblerlength` [`tumble.c:259-262`] = `nstories(vsaptr) - vsaptr->exp` gives the depth of the V-address. The stored POOM crum V-width is forced to mantissa position `tumblerlength - 1`, which is exactly the ordinal displacement at V-position depth (width = δ at the right depth). This is enforced **at write time**, not at read/query time.

---

### Conclusion

| Phase | Width Constraint? | Source |
|-------|-------------------|--------|
| Protocol input parsing | None | `get1fe.c:124-129` |
| VSA acceptance check | Unconditionally TRUE | `do2.c:110-113` |
| Text subspace filter | Stream only; width copied unchanged | `do1.c:420-424` |
| V→I permutation / retrieval | None; `tumbleradd` used directly | `retrie.c:65` |
| INSERT (insertpm) | **Enforced**: shift = tumblerlength(vsa)-1 | `orglinks.c:115-117` |

**COMPAREVERSIONS accepts widths with actionPoint ≥ 2 — or any actionPoint — without restriction.** The ordinal-displacement constraint (`width = δ(n, m)` at V-position depth) exists only in the `insertpm` path that writes POOM crums. Since all content was inserted through `insertpm`, the stored data in the enfilade will have the correct ordinal widths. But COMPAREVERSIONS makes no attempt to verify this property on its input spans — it will silently accept a width at the wrong depth and produce a result (likely empty, or over-broad) without error.
