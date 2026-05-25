## Question 6 [evidence]

> Does the udanax-green implementation of compareversions accept link-subspace restrictions, and if so does it produce non-empty results for distinct documents, or does it specialize to content?

## KB Synthesis

## `compare_versions` and Link-Subspace Restrictions

### Short answer

`compare_versions` does **not** filter link-subspace inputs, does **not** produce non-empty results when link-subspace spans are passed — it **crashes** — and is semantically specialized to permascroll content only, though that specialization is missing from the implementation as an explicit filter step.

---

### What the implementation accepts

The backend has no subspace guard at the `compare_versions` entry point. `acceptablevsa()` unconditionally returns `TRUE` [PRE-INSERT, PRE-SUBSPACE-CONVENTION], and `correspond.c` performs no pre-filtering. If a caller passes V-spans that include the link subspace (internally `2.x`, normalized to `0.x` in output), those spans are accepted without error.

### What happens when link-subspace spans are passed

`correspond.c` converts all V-spans to I-spans via the type-agnostic `permute()` path [SS-CONTENT-IDENTITY: Finding 0009]. Link V-spans at `2.x` produce **link orgl ISAs** as their I-addresses — a fundamentally different address space from the permascroll I-addresses produced by text spans at `1.x`.

Link orgl ISAs can never intersect with permascroll I-addresses from another document, because:
- Each link ISA is a unique object identity, not a shareable content origin [SS-CONTENT-IDENTITY: Finding 0015]
- Two documents cannot share a link ISA via transclusion [SS-CONTENT-IDENTITY: Finding 0009]

The `correspond.c` nested-loop structure assumes each I-span matches at most one V-spec. When the intersection is empty, it does not handle that case gracefully — the result is a **backend crash** (Bug 0009) [EC-COMPARE-VERSIONS-LINK-CRASH: Finding 0009; PRE-COMPARE-VERSIONS: Finding 0011].

### For distinct documents specifically

Even for two completely distinct documents that happen to share identical link types or parallel link structures, `compare_versions` including link-subspace spans still crashes. Link ISAs are per-document unique allocations; there is no mechanism by which two independent documents share a link ISA [SS-CONTENT-IDENTITY: Finding 0015].

### What `compare_versions` is semantically specialized to

By design, `compare_versions` answers: *"What text content do these two documents share by common origin?"* [SS-COMPARE-VERSIONS: Finding 0015]. The postcondition is pairs `(span_a, span_b)` satisfying `VSpanToISpan(doc_a, span_a) == VSpanToISpan(doc_b, span_b)` where both I-spans are **permascroll addresses** only.

Finding 0015 explicitly states the correct algorithm requires a missing step:

> **Filter to text subspace only (V >= 1)** before I-span conversion

This step is absent from `correspond.c` [PRE-COMPARE-VERSIONS: Finding 0015]. The subspace isolation that INSERT achieves via a deliberate two-blade knife [SS-TWO-BLADE-KNIFE] and DELETE achieves via an incidental arithmetic guard [FC-SUBSPACE: Finding 0055] has no equivalent in `compare_versions` — it relies entirely on callers not passing link-subspace spans.

### Summary

| Condition | Result |
|-----------|--------|
| Text-only input, distinct documents | Returns shared permascroll I-span pairs (correct) |
| Text-only input, same document | Returns full document as shared [EC-SELF-COMPARISON] |
| Link-subspace spans included | **Backend crash** (Bug 0009) |
| Link-subspace spans, distinct documents | **Crash** — no result produced |

The implementation does not specialize to content by filtering; it specializes by convention [INV-SUBSPACE-CONVENTION], and crashes when that convention is violated.

---

## Code Exploration

I have all the code I need. Here is the complete answer with full source citations.

---

## `compareversions` (SHOWRELATIONOF2VERSIONS): Link-Subspace and Cross-Document Behavior

### 1. Protocol Signature — No VSA Parameter Accepted

`getshowrelationof2versions` [`get1fe.c:124–128`] accepts **exactly two parameters** — two `typespecset` values:

```c
bool getshowrelationof2versions(typetask *taskptr, typespecset *version1ptr, typespecset *version2ptr)
{
    return (
       getspecset (taskptr, version1ptr)
    && getspecset (taskptr, version2ptr));
}
```

There is no VSA (virtual subspace address) restriction parameter in the protocol message at all. The caller cannot pass a subspace filter; the operation decides what subspace to use internally.

---

### 2. Link-Subspace Is Actively Filtered Out — Not Accepted

`doshowrelationof2versions` [`do1.c:428–449`] **strips all link-subspace spans before comparison**:

```c
/* SEMANTIC FIX: Filter to text subspace before comparison.
 * Link references (V < 1.0) are not content with "common origin".
 * See Finding 015 for the semantic definition. */
filter_specset_to_text_subspace(taskptr, version1);   // do1.c:440
filter_specset_to_text_subspace(taskptr, version2);   // do1.c:441
```

The filter function itself [`do1.c:386–411`] walks the vspanset and drops every span where `stream < 1.0`:

```c
for (; vspanset; vspanset = vspanset->next) {
    if (tumblercmp(&vspanset->stream, &text_subspace_start) >= EQUAL) {
        /* keep */
    }
    /* Spans with stream < 1.0 are in link subspace - skip them */  // do1.c:408
}
```

The threshold `text_subspace_start` is 1.0, constructed by `tumblerclear` + `tumblerincrement` [`do1.c:394–395`].

**Conclusion: link-subspace spans (V < 1.0) are silently discarded before the comparison runs. They cannot produce output.**

---

### 3. Why Link Spans Are Excluded

The comment at [`do1.c:377–385`] states the semantic rationale:

> `compare_versions` finds content with "common origin" — shared permascroll identity. Link references at V-position 0.x are document metadata, not transcludable content. They have unique ISAs, not permascroll addresses, so comparing them is semantically undefined.

---

### 4. Cross-Document Results Are Possible — But Only for Shared Permascroll Content

After filtering to text subspace, the pipeline is:

```
version1 (filtered) → specset2ispanset → version1ispans  [do1.c:444]
version2 (filtered) → specset2ispanset → version2ispans  [do1.c:445]
                    intersectspansets → commonispans      [do1.c:446]
ispansetandspecsets2spanpairset → relation spanpairs     [do1.c:447]
```

The final step calls `makespanpair` [`correspond.c:351–361`]:

```c
typespanpair *makespanpair(..., tumbler *doc1, tumbler *start1,
                                tumbler *doc2, tumbler *start2, ...)
{
    docidandvstream2tumbler (doc1, start1, &spanpair->stream1);  // correspond.c:357
    docidandvstream2tumbler (doc2, start2, &spanpair->stream2);  // correspond.c:358
    ...
}
```

`spanpair->stream1` encodes doc1's ISA + V-position; `spanpair->stream2` encodes doc2's ISA + V-position. These can be **different documents**. The operation iterates both specsets simultaneously [`correspond.c:304–343`], advancing through whichever spec/span is shorter — both `spec1->docisa` and `spec2->docisa` are preserved independently.

So: if two distinct documents both transclude the same permascroll range (their text-subspace V-spans both map to the same I-span), `compareversions` **will** return a non-empty span-pair set connecting positions in both.

---

### 5. `acceptablevsa` Is Not Used Here

`acceptablevsa` [`do2.c:110–113`] is a trivially-true stub used by `docopy`, not by `doshowrelationof2versions`:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr) {
    return (TRUE);
}
```

It plays no role in the `compareversions` path.

---

### Summary

| Question | Answer |
|---|---|
| Does `compareversions` accept a link-subspace restriction parameter? | **No.** The protocol takes only two specsets [`get1fe.c:124`]; no subspace parameter exists. |
| Does the implementation process link-subspace spans if they appear in the input? | **No.** `filter_specset_to_text_subspace` strips all V < 1.0 spans at [`do1.c:440–441`] before any I-space conversion. |
| Does it specialize to content (text subspace)? | **Yes.** Only spans with V ≥ 1.0 survive the filter [`do1.c:399`]. |
| Can it produce non-empty results across distinct documents? | **Yes**, if both documents share permascroll content. `makespanpair` [`correspond.c:357–358`] independently encodes `doc1`+`start1` and `doc2`+`start2` in the returned span pair, preserving distinct ISAs. |
