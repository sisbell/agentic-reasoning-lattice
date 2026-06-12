## Question 12 [evidence]

> In correspond.c, is the correspondence test pure I-address interval intersection between the two documents' POOM entries, or does it ever consult the granfilade bytes — meaning two spans with identical text but distinct I-addresses can never correspond?

## KB Synthesis

The correspondence test is pure I-address interval intersection. The granfilade bytes are never consulted.

**The mechanism** — from [INT-SPORGL-VERSION-COMPARE]:

> Version comparison (`compare_versions` / `correspond.c`) uses sporgls to find shared content between documents. Both documents' content is converted to sporgls, then intersection is computed by **I-address** (the `sporglorigin` field). Sporgls with the same I-address origin in both documents represent shared content.

The algorithm reconstructed in [PRE-COMPARE-VERSIONS] (Finding 0015) confirms this five-step pipeline:

1. Retrieve V-spans from both documents
2. Filter to text subspace (V ≥ 1)
3. Convert V-spans to I-spans
4. **Find common I-addresses**
5. Map back to V-spans in each document

Step 4 is set intersection on I-address ranges — no byte comparison, no granfilade read.

**The implication you named is exactly right** — two independently created spans with identical bytes can never correspond. [SS-CONTENT-IDENTITY] (Finding 0018) states this directly:

> Content identity in udanax-green is based on I-addresses (immutable positions in the permascroll), not textual value. Two documents containing identical text created independently do NOT share content identity — `compare_versions` returns an empty result. Identity is determined by *when and where* content was created.

The concrete example from the same finding:
```
Source1: "From source one"  → I-address X
Source2: "From source two"  → I-address Y
compare_versions(source1, source2) → []   # empty even if text were identical
```

[INV-DOC-ISOLATION-IDENTITY] reinforces this as an invariant: `create_document` always allocates I-addresses disjoint from all existing ones, so independently created content is identity-disjoint by construction.

**Why this is structurally enforced, not just a design choice**: [SS-ADDRESS-SPACE] (Finding 0033, 0061) shows that I-address allocation is strictly monotonically increasing and never reuses gaps. Fresh content always lands above the current granfilade maximum. There is no path by which two independent INSERT operations could produce the same I-address, so byte-value equality between independently created spans is irrelevant to the intersection test — they are guaranteed to have non-overlapping I-ranges.

The correspondence predicate is therefore: `spans A and B correspond ↔ I-addresses(A) ∩ I-addresses(B) ≠ ∅`, where that intersection is only non-empty when one document's content was derived from the other via vcopy or versioning [INV-TRANSITIVE-IDENTITY].

---

## Code Exploration

I have read all the relevant code. Here is the full answer.

---

## Correspondence Is Purely I-Address Interval Intersection — Granfilade Bytes Are Never Consulted

The correspondence test in `correspond.c` is purely structural. It operates entirely in the I-address space. Two spans with identical text characters but distinct I-addresses **can never correspond**.

---

### The Full Call Chain

The public entry point is `showrelationof2versions` in `fns.c:250`:

```c
// fns.c:250-261
void showrelationof2versions(typetask *taskptr) {
    if (getshowrelationof2versions(taskptr, &version1, &version2)
     && doshowrelationof2versions(taskptr, version1, version2, &relation))
        putshowrelationof2versions(taskptr, relation);
```

This delegates to `doshowrelationof2versions` in `do1.c:428-449`:

```c
// do1.c:428-449
bool doshowrelationof2versions(...) {
    typeispanset version1ispans = NULL;
    typeispanset version2ispans = NULL;
    typeispanset commonispans = NULL;

    filter_specset_to_text_subspace(taskptr, version1);  // V-address filter only
    filter_specset_to_text_subspace(taskptr, version2);

    return
        specset2ispanset(taskptr, version1, &version1ispans, READBERT)
      && specset2ispanset(taskptr, version2, &version2ispans, READBERT)
      && intersectspansets(taskptr, version1ispans, version2ispans, &commonispans, ISPANID)
      && ispansetandspecsets2spanpairset(taskptr, commonispans, version1, version2, relation);
}
```

There are four steps. None touches bytes.

---

### Step 1: V-spans → I-spans via POOM Lookup (`specset2ispanset`, `do2.c:14`)

```c
// do2.c:34-38
if (!(
    findorgl(taskptr, granf, &((typevspec*)specset)->docisa, &docorgl, type)
  && (ispansetptr = vspanset2ispanset(taskptr, docorgl, ((typevspec*)specset)->vspanset, ispansetptr))
))  return(FALSE);
```

`findorgl` (`granf1.c:17`) looks up the document's POOM in the granfilade by document I-address. It does not read text content — it fetches the POOM root pointer via `fetchorglgr`.

`vspanset2ispanset` (`orglinks.c:397`) is:

```c
// orglinks.c:397-401
typevspanset *ispan2vspanset(typetask *taskptr, typeorgl orgl, typeispan *ispanptr, typevspanset *vspansetptr) {
    return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
}
typeispanset *vspanset2ispanset(...) {
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

`permute` (`orglinks.c:404`) iterates the restriction span set and calls `span2spanset` for each. `span2spanset` (`orglinks.c:425`) calls `retrieverestricted` (`retrie.c:56`), which calls `retrieveinarea` → `findcbcinarea2d` (`retrie.c:229`).

`findcbcinarea2d` walks the POOM tree. Its qualification test `crumqualifies2d` (`retrie.c:270`) is **purely tumbler range comparisons** — `whereoncrum` calls `tumblercmp` on the index coordinates. When a leaf crum qualifies, `makecontextfromcbc` records the crum's displacement and width values (both I and V coordinates). No text string field is read.

The extracted span is produced by `context2span` (`context.c:176`):

```c
// context.c:191-211
if (tumblercmp(&grasp.dsas[idx1], &lowerbound) == LESS)
    tumblerincrement(&grasp.dsas[idx2], 0, tumblerintdiff(&lowerbound, &grasp.dsas[idx1]), &grasp.dsas[idx2]);
if (tumblercmp(&reach.dsas[idx1], &upperbound) == GREATER)
    tumblerincrement(&reach.dsas[idx2], 0, -tumblerintdiff(&reach.dsas[idx1], &upperbound), &reach.dsas[idx2]);
movetumbler(&grasp.dsas[idx2], &foundspanptr->stream);
tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width);
```

This computes the target-index (I or V) coordinate range from the POOM crum's stored displacement — tumbler arithmetic only.

Contrast this with `context2vstuff` / `context2vtext` (`context.c:240-309`), which is where actual text bytes are accessed (via `textstuff.textstring`). That function is only called on the retrieval path (`ispanset2vstuffset` in `granf1.c:57`), never from the correspondence path.

---

### Step 2: I-span Intersection (`intersectspansets`, `correspond.c:145`)

```c
// correspond.c:177-182
for (; set1; set1 = set1->next) {
    for (p = set2; p; p = p->next) {
        if (comparespans(taskptr, set1, p, set3, spantype))
            set3 = &(*set3)->next;
    }
}
```

`comparespans` (`correspond.c:191`) calls `spanintersection` (`correspond.c:210`):

```c
// correspond.c:210-265
bool spanintersection(typespan *aptr, typespan *bptr, typespan *cptr) {
    tumbleradd(&bptr->stream, &bptr->width, &bend);
    if (tumblercmp(&aptr->stream, &bend) >= EQUAL) return(FALSE);
    tumbleradd(&aptr->stream, &aptr->width, &aend);
    if (tumblercmp(&bptr->stream, &aend) >= EQUAL) return(FALSE);
    // ... tumbler min/max arithmetic to compute overlap interval ...
    return(TRUE);
}
```

This is pure interval arithmetic on tumbler values. The I-address ranges are compared numerically. No granfilade lookup of any kind is performed here.

---

### Step 3: Restrict Specsets to Common I-spans (`restrictspecsetsaccordingtoispans`, `correspond.c:18`)

```c
// correspond.c:26-44
restrictvspecsetovercommonispans(taskptr, ispanset, *specset1, &s1);
if (s1 && *specset1) removespansnotinoriginal(taskptr, s1, specset1);
restrictvspecsetovercommonispans(taskptr, ispanset, *specset2, &s2);
if (s2 && *specset2) removespansnotinoriginal(taskptr, s2, specset2);
```

`restrictvspecsetovercommonispans` (`correspond.c:52`) does a `findorgl` (POOM lookup) and calls `ispan2vspanset` (the reverse POOM permutation, again structural only). `removespansnotinoriginal` (`correspond.c:92`) calls `intersectspansets` — again tumbler arithmetic.

---

### Step 4: Pair Construction (`makespanpairsforispan`, `correspond.c:290`)

The loop at `correspond.c:308-344` advances through pairs of V-spans with matched I-widths, producing `typespanpair` records containing two V-stream tumblers and a width. `makespanpair` (`correspond.c:351`) calls `docidandvstream2tumbler` twice — this encodes doc-ID + V-address into a compound tumbler — and copies the width. No text access.

---

### Why Two Spans With Identical Bytes But Distinct I-Addresses Cannot Correspond

The V→I→V pipeline is entirely inside the POOM (the Permutation Object Order Matrix). The POOM is a 2D enfilade indexed by `(V, I)` coordinate pairs — it records, for each V-position in a document, which I-address occupies that position. The POOM does not store text bytes; those live in a separate part of the granfilade, retrievable via `ispan2vstuffset` → `context2vtext` (`context.c:277`), which is never called during correspondence.

In Xanadu's model, an I-address is assigned once at insertion time. It is the permanent, unique identity of that particular insertion event. Two insertions of the character `'A'` at different times produce two different I-addresses. The POOM of a document that contains a copy of a passage records the same I-addresses as the original — that is what makes transclusion work, and what makes correspondence possible. A fresh insertion of identical bytes produces a disjoint I-address range; the intersection at step 2 is empty; the span-pair result is empty.

There is no fallback content comparison. The system never asks "do these bytes match?" — it only asks "do these I-address ranges overlap?"
