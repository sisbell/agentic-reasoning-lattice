## Question 11 [evidence]

> When `compare_versions` (SHOWRELATIONOF2VERSIONS) runs on two documents, does it traverse both POOMs to compute I-address intersection, or does it query the spanfilade DOCISPAN entries for both documents and intersect there?

## KB Synthesis

`compare_versions` traverses both **POOMs**, not the spanfilade DOCISPAN entries.

**The mechanism:**

1. Retrieve V-spans from both documents (via `retrievedocumentpartofvspanpm` or equivalent).
2. Convert each document's V-spans to I-addresses through the POOM enfilade via `vspanset2sporglset` → `vspanset2ispanset` → `permute` → `retrieverestricted`. This is a live POOM traversal producing sporgls (I-address + provenance). [INT-SPORGL-VERSION-COMPARE]
3. `correspond.c` runs a nested loop over the two sporgl sets, intersecting on `sporglorigin` (I-address). [SS-COMPARE-VERSIONS]
4. Matches are mapped back to V-spans in each document for the result.

**Why not DOCISPAN?**

The spanfilade DOCISPAN sub-index maps `I-address → {DocISA}` and answers "which documents contain this content?" — that is the `FINDDOCSCONTAINING` operation. [SS-DOCISPAN] DOCISPAN is also a superset of current POOM associations (stale entries persist after DELETE) [INV-SPANF-WRITE-ONLY], so it would yield incorrect intersection results.

**The precondition consequence:**

This POOM-traversal path is why including the link subspace in the inputs crashes. Link orgls at V-position `2.x` produce link ISA I-addresses, which live in a different address space from permascroll addresses. `correspond.c`'s nested loop assumes a uniform I-address space and has no handler for empty intersections. [PRE-COMPARE-VERSIONS], [EC-COMPARE-VERSIONS-LINK-CRASH]

---

## Code Exploration

All key claims verified against the actual source. Here is my answer.

---

## How `SHOWRELATIONOF2VERSIONS` Finds Shared Content

**Short answer:** It traverses both POOMs — not the spanfilade. V-space specs are converted to I-space (I-addresses) by walking each document's granfilade tree; those two ISPAN sets are then intersected in I-space. The spanfilade is never queried.

---

### Entry Point

`showrelationof2versions` [fns.c:250-261] parses two version specsets, then delegates:

```c
if (getshowrelationof2versions(taskptr, &version1, &version2)
 && doshowrelationof2versions(taskptr, version1, version2, &relation))
    putshowrelationof2versions(taskptr, relation);
```

---

### Core: `doshowrelationof2versions` [do1.c:428-449]

```c
filter_specset_to_text_subspace(taskptr, version1);   // drop V < 1.0 (link metadata)
filter_specset_to_text_subspace(taskptr, version2);

return
    specset2ispanset(taskptr, version1, &version1ispans, READBERT)  // V→I via POOM
  &&    specset2ispanset(taskptr, version2, &version2ispans, READBERT)  // V→I via POOM
  &&    intersectspansets(taskptr, version1ispans, version2ispans, &commonispans, ISPANID)  // I-space intersection
  &&    ispansetandspecsets2spanpairset(taskptr, commonispans, version1, version2, relation) // back to span pairs
  ;
```

Four steps:

---

### Step 1 — Filter to Text Subspace [do1.c:437-441]

Removes any V-space spans with `stream < 1.0` (link-subspace metadata). Only V ≥ 1.0 content enters comparison.

---

### Step 2 — V→I Conversion via POOM Traversal

`specset2ispanset` [do2.c:14-46] — for each VSPEC in the specset:

```c
findorgl(taskptr, granf, &vspec->docisa, &docorgl, READBERT)   // [do2.c:35]
&& (ispansetptr = vspanset2ispanset(taskptr, docorgl, vspec->vspanset, ispansetptr))  // [do2.c:36]
```

It looks up the document's root in the **granfilade** (`granf`), then calls:

- `vspanset2ispanset` [orglinks.c:397] → `permute(orgl, vspans, V, …, I)` [orglinks.c:404]
- `permute` iterates each V-span, calls `span2spanset` [orglinks.c:414-416]
- `span2spanset` [orglinks.c:425-454] calls:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, V, NULL, I, NULL);
```

- `retrieverestricted` [retrie.c:56-85] computes 2D tumbler bounds for the query region, then calls `retrieveinarea` [retrie.c:87-110], which dispatches on `cenftype`:

```c
case SPAN:
case POOM:
    findcbcinarea2d(crumptr, …);   // [retrie.c:97]
```

- `findcbcinarea2d` recursively walks the POOM tree — `getrightbro` across siblings, `findleftson` into children, `crumqualifies2d` to prune nodes outside the V-span bounds. At `height == 0` (leaf), it calls `makecontextfromcbc` to emit a context record carrying both V and I coordinates.

- Back in `span2spanset`, each context is decoded with `context2span` to produce an ISPAN, appended to the output list via `onitemlist`.

**This traversal happens once per document, using that document's own POOM tree.** The spanfilade is not touched.

---

### Step 3 — I-Space Intersection

`intersectspansets` [correspond.c:145-189] computes geometric overlap between the two ISPAN sets — tumbler-range intersection, O(n²) nested loop with `comparespans`. Result is the set of I-addresses that appear in both documents.

---

### Step 4 — Map Common ISPANs Back to Span Pairs

`ispansetandspecsets2spanpairset` [do2.c:185-207] — for each common ISPAN:

- `restrictvspecsetovercommonispans` [correspond.c:52-77] queries **each document's granfilade again** via `ispan2vspanset` (the reverse permute, I→V) to find the V-positions where that I-address appears in each version.
- `makespanpairset` [correspond.c:267-288] packages the results as `(V-span-in-doc1, V-span-in-doc2)` pairs.

---

### Does It Query DOCISPAN Entries in the Spanfilade?

**No.** DOCISPAN entries are written to the spanfilade during `doinsert` [do1.c:50-88] via `insertspanf` [spanf1.c], so the spanfilade knows which I-addresses belong to which documents. But `SHOWRELATIONOF2VERSIONS` never calls `findorgl(spanf, …)` or any spanfilade lookup. The entire comparison goes through `granf` (the per-document POOM trees).

---

### Summary

| Question | Answer |
|---|---|
| Traverses both POOMs? | **Yes** — `findcbcinarea2d` recursively walks each document's granfilade tree during V→I conversion |
| Queries spanfilade DOCISPAN entries? | **No** — spanfilade is for link queries only; version comparison never touches it |
| Mechanism for shared content | V→I via POOM traversal → I-space tumbler intersection → I→V back-conversion → span pair output |

Shared content is defined as: content whose **I-address (permascroll address) falls in both documents' POOM trees**. The POOMs encode V↔I mappings for each document, and the intersection happens purely at the I-address level.
