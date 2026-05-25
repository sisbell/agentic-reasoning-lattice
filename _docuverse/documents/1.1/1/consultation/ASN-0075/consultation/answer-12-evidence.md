## Question 12 [evidence]

> Does SHOWRELATIONOF2VERSIONS / `correspond.c` return only shared I-spans, or does it also enumerate the I-spans present in one document's POOM but absent from the other?

## KB Synthesis

`SHOWRELATIONOF2VERSIONS` / `correspond.c` returns **only shared I-spans** — it is strictly a common-origin finder, not a diff engine.

The operation produces a list of **ordered pairs** `(span_a, span_b)` where both spans map to the same permascroll I-address range. I-spans present in only one document produce no output entry whatsoever — they are neither flagged as "unique to A" nor enumerated as absent from the other.

From [SS-COMPARE-VERSIONS] / [ST-COMPARE-VERSIONS] (Finding 0015):

> answers the question: "What text content do these two documents share by common origin?" … The result is complete: every shared permascroll address range appears in exactly one pair.

The concrete example in [ST-INSERT] (Finding 0030) is explicit: after inserting "XY" into a document, `compare_versions` reports shifted spans for pre-existing content but **no span for positions 1.3–1.4** (the new "XY") because those I-addresses have no counterpart in the prior version.

The postcondition is:

```
result = { (span_a, span_b) | VSpanToISpan(doc_a, span_a) == VSpanToISpan(doc_b, span_b) }
```

Nothing more. Content unique to either document is simply absent from the result set.

---

## Code Exploration

I now have a complete, code-verified answer.

---

## Answer: SHOWRELATIONOF2VERSIONS Returns Only Shared I-Spans

`SHOWRELATIONOF2VERSIONS` returns **only** the I-spans that are shared between the two versions. I-spans present in one document's POOM but absent from the other are silently discarded — they never appear in the output.

---

### The Critical Evidence

#### Step 1 — `doshowrelationof2versions` computes an intersection, explicitly

`backend/do1.c:428-449`:

```c
bool doshowrelationof2versions(typetask *taskptr, typespecset version1, typespecset version2, typespanpairset *relation)
{
  typeispanset version1ispans = NULL;
  typeispanset version2ispans = NULL;
  typeispanset commonispans = NULL;          // <— named "common", not "all" or "union"
  ...
    specset2ispanset(taskptr, version1, &version1ispans, READBERT)
  &&  specset2ispanset(taskptr, version2, &version2ispans, READBERT)
  &&  intersectspansets(taskptr, version1ispans, version2ispans, &commonispans, ISPANID)
  &&  ispansetandspecsets2spanpairset(taskptr, commonispans, version1, version2, relation)
  ;
}
```

The output variable is named `commonispans` and the function called is `intersectspansets` — not a union, not a set-difference. The semantic intent is encoded in both the name and the call.

#### Step 2 — `intersectspansets` uses a nested pairwise loop that only keeps overlapping regions

`backend/correspond.c:177-188`:

```c
for (; set1; set1 = set1->next) {
    for (p = set2; p; p = p->next) {
        if (comparespans (taskptr, set1, p, set3, spantype))
            set3 = &(*set3)->next;
    }
}
return (TRUE);
```

For each pair (s1, s2), `comparespans` is called. It allocates a result span and calls `spanintersection`. If `spanintersection` returns FALSE (no overlap), the allocation is freed and the pair is **dropped** — `do1.c` analog at `correspond.c:203-206`:

```c
tfreeexplicit (taskptr, (char*)*span3);
*span3 = NULL;
return (FALSE);
```

I-spans that are in version1 but have no overlap with any span in version2 simply never match in the inner loop — they produce no output.

#### Step 3 — `spanintersection` is a pure geometric overlap function

`backend/correspond.c:210-265`:

```c
bool spanintersection(typespan *aptr, typespan *bptr, typespan *cptr)
{
  tumbler aend, bend;
    tumbleradd (&bptr->stream, &bptr->width, &bend);
    if (tumblercmp (&aptr->stream, &bend) >= EQUAL)
        return (FALSE);          // a starts at or after b ends → no overlap
    tumbleradd (&aptr->stream, &aptr->width, &aend);
    if (tumblercmp (&bptr->stream, &aend) >= EQUAL)
        return (FALSE);          // b starts at or after a ends → no overlap
    // ... compute the overlapping sub-region ...
    return (TRUE);
}
```

This is a textbook interval-intersection test using tumbler arithmetic. It computes `[max(a.start, b.start), min(a.end, b.end)]`. There is no code path here or anywhere in the call chain that enumerates the **difference** (spans in one but not the other).

#### Step 4 — The NULL guard confirms: no shared spans → empty result, not enumeration of either side

`backend/correspond.c:163-168` (inside `intersectspansets`):

```c
if (!set1 || !set2) {
    return (TRUE);   // empty intersection, not an error
}
```

And `backend/do2.c:190-194` (inside `ispansetandspecsets2spanpairset`):

```c
if (ispanset == NULL) {
    *pairsetptr = NULL;
    // → returns TRUE, caller gets empty result
}
```

When `commonispans` is NULL (no overlap whatsoever), the output `relation` is set to NULL. The spans unique to version1 or version2 are never visited.

---

### Summary

The operation performed is:

```
output = { (vspan_in_v1, vspan_in_v2) : their I-spans overlap }
```

It is a **bilateral overlap map** — "what text do these two documents share, and where does it sit in each?". It is **not** a diff or a set-difference. I-spans that exist in version1's POOM but have no counterpart in version2, and vice versa, are completely invisible in the output. The function answers "where do these versions agree on content origin?" — not "what is different between them?"
