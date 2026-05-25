## Question 20 [evidence]

> When correspondence pairs are reported, are they constrained by the caller-supplied specset bounds on BOTH documents (intersection filtered to both windows), or only on the first document with the second reported in full?

## KB Synthesis

Correspondence pairs are constrained by the caller-supplied specset bounds on **both** documents simultaneously. The result is a bilateral intersection.

[ST-SPECSET-COMPARE] (Finding 0003) is the definitive entry:

> `compare(specset_A, specset_B)` reports only identity overlaps between content referenced by specset_A **and** content referenced by specset_B. Content in either document but outside the specified spans does not appear in results.
>
> Formally: `shared_regions(compare(ss_A, ss_B)) ⊆ {c | c in content_ids(ss_A) ∩ content_ids(ss_B)}`

The concrete example from that entry confirms it: comparing only the "middles" of two documents (neither of which shares content) returns no pairs — even though both documents share prefix and suffix content that would appear in an unwindowed comparison.

[SS-COMPARE-VERSIONS] (Finding 0015) describes the algorithm consistent with this:

1. Retrieve V-spans from both documents (each input specset bounds its respective document)
2. Filter to text subspace only
3. Convert V-spans to I-spans
4. Find common I-addresses (intersection of both I-span sets)
5. Map back to V-spans in each document

Step 4 intersects the I-spans derived from **both** windows, so a pair `(span_a, span_b)` only appears if the shared I-addresses fall within the specset window for doc_a *and* the specset window for doc_b.

The postcondition from [ST-COMPARE-VERSIONS]: each pair satisfies `VSpanToISpan(doc_a, span_a) == VSpanToISpan(doc_b, span_b)`, and the result is complete — every shared I-address range within the intersection of both windows appears in exactly one pair.

---

## Code Exploration

I have traced the complete call chain. Here is the full answer.

---

## Correspondence Pair Reporting: Both Specset Windows Are Applied Symmetrically

**Answer: Caller-supplied specset bounds constrain BOTH documents. The filtering is fully symmetric.**

---

### Call Chain

```
fns.c:256       showrelationof2versions
do1.c:428          doshowrelationof2versions
do2.c:196-197         ispansetandspecsets2spanpairset
correspond.c:18           restrictspecsetsaccordingtoispans  ← filters BOTH
correspond.c:267          makespanpairset
```

---

### Step 1 — Build Common I-Space (`do1.c:443–447`)

```c
specset2ispanset(taskptr, version1, &version1ispans, READBERT)    // caller window1 → I
specset2ispanset(taskptr, version2, &version2ispans, READBERT)    // caller window2 → I
intersectspansets(taskptr, version1ispans, version2ispans, &commonispans, ISPANID)
ispansetandspecsets2spanpairset(taskptr, commonispans, version1, version2, relation)
```

Each caller specset is first translated to I-space via `vspanset2ispanset` (`do2.c:36`). The intersection of the two I-span sets — `commonispans` — represents only the content addresses that fall within **both** caller-specified windows simultaneously.

---

### Step 2 — Restrict Both Specsets (`correspond.c:18–50`)

```c
// For specset1 (doc1):
restrictvspecsetovercommonispans(taskptr, ispanset, *specset1, &s1);   // line 26
if (s1 && *specset1) removespansnotinoriginal(taskptr, s1, specset1);  // line 29-30

// For specset2 (doc2):
restrictvspecsetovercommonispans(taskptr, ispanset, *specset2, &s2);   // line 36
if (s2 && *specset2) removespansnotinoriginal(taskptr, s2, specset2);  // line 39-40
```

Both sides receive identical treatment. There is no asymmetry in the code.

---

### Step 3 — `restrictvspecsetovercommonispans` (`correspond.c:52–90`)

For each ispan in `commonispans`, for each vspec in the specset, this calls:

```c
ispan2vspanset(taskptr, versionorgl, ispanset, &docvspanset)  // correspond.c:74
```

`ispan2vspanset` at `orglinks.c:389–393` calls `permute(..., I, ..., V)`, mapping the I-address back to a V-address in that document's coordinate space.

---

### Step 4 — `removespansnotinoriginal` (`correspond.c:92–135`)

This function intersects the ispan-projected V-addresses with the caller's original specset:

```c
if (intersectspansets(taskptr,
        ((typevspec *)new)->vspanset,    // ispan-mapped V-range
        ((typevspec *)old)->vspanset,    // caller's original specset for this doc
        &newspanset, VSPANID))           // line 116
```

Done for **both** documents. The reported V-span for each document is therefore:

```
reported_span(docN) = ispan_to_vspan(commonContent, docN)  ∩  callerSpecset(docN)
```

---

### Step 5 — Pair Up (`correspond.c:267–288`, `290–348`)

`makespanpairset` iterates over `commonispans` and advances through the already-filtered `specset1`/`specset2` in lockstep (`makespanpairsforispan`), consuming equal widths from both sides. The output span pairs are bounded by whatever survived filtering in both specsets.

---

### Conclusion

Correspondence pairs are **constrained by the caller-supplied specset bounds on both documents**. The `commonispans` is derived from the intersection of both caller windows in I-space (`do1.c:446`), and then `restrictspecsetsaccordingtoispans` applies `removespansnotinoriginal` symmetrically to both specsets (`correspond.c:29-30`, `39-40`), further clipping each document's reported spans back to within the caller's original V-space bounds. There is no code path where one document's window is honored and the other is reported in full.
