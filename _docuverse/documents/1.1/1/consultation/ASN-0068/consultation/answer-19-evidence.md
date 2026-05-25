## Question 19 [evidence]

> Is the correspondence computation symmetric — does `compare_versions(A, B)` produce the same VSpec pairings as `compare_versions(B, A)` with arguments swapped, or is one document treated as the reference?

## KB Synthesis

## Symmetry of `compare_versions`

The operation is **mathematically symmetric in content but argument-order-sensitive in result form**.

### The Underlying Computation Is Symmetric

`compare_versions` works by converting both documents' text V-spans into permascroll I-addresses (via `correspond.c`'s nested loop), then computing I-address intersection [SS-COMPARE-VERSIONS]. Set intersection is commutative: the set of shared I-address ranges is identical regardless of which document is argument 1 or 2. Neither document is treated as a privileged reference.

[INT-SPORGL-VERSION-COMPARE] confirms: "Both documents' content is converted to sporgls, then intersection is computed by I-address."

### The Result Form Depends on Argument Order

Each result pair is `(span_in_doc_a, span_in_doc_b)` — the first element always comes from the first argument, the second from the second [SS-COMPARE-VERSIONS]:

```
compare_versions(A, B) → [(A: 1.1 for 5, B: 1.1 for 5), ...]
compare_versions(B, A) → [(B: 1.1 for 5, A: 1.1 for 5), ...]
```

The pairs are swapped, but the content they describe is identical.

### Caveat: Result List Ordering

The traversal order through `correspond.c`'s nested loop is not documented in the KB. Swapping arguments would swap the loop nesting (outer vs. inner sporglset), which could change the *order* of pairs in the result list without changing which pairs appear. The KB does not specify this.

### Preconditions Apply Symmetrically

[PRE-COMPARE-VERSIONS] requires both inputs to be text-subspace spans — this constraint applies symmetrically to both arguments. No argument has special status.

**Summary:** `compare_versions(A, B)` and `compare_versions(B, A)` identify the same shared content, but return pairs with first/second elements swapped. The operation has no reference document.

---

## Code Exploration

I now have all the source to give a definitive answer. Here it is.

---

## Symmetry of the Correspondence Computation

### Short answer

The correspondence computation is **symmetric in content** — `compare_versions(A, B)` and `compare_versions(B, A)` discover the same set of corresponding text ranges. But it is **asymmetric in output representation** — swapping arguments swaps the `stream1`/`stream2` roles inside every output `spanpair`. One document is not specially privileged as a "reference"; both are treated as equals.

---

### Call chain

The FEBE handler lives at `backend/fns.c:257`:

```c
if (getshowrelationof2versions(taskptr, &version1, &version2)
 && doshowrelationof2versions(taskptr, version1, version2, &relation))
    putshowrelationof2versions(taskptr, relation);
```

`version1` and `version2` are read in the order they arrive on the wire.

---

### `doshowrelationof2versions` — `backend/do1.c:428-449`

```c
bool doshowrelationof2versions(typetask *taskptr, typespecset version1, typespecset version2, typespanpairset *relation)
{
    filter_specset_to_text_subspace(taskptr, version1);   // do1.c:440
    filter_specset_to_text_subspace(taskptr, version2);   // do1.c:441

    return
        specset2ispanset(taskptr, version1, &version1ispans, READBERT)   // do1.c:444
      && specset2ispanset(taskptr, version2, &version2ispans, READBERT)  // do1.c:445
      && intersectspansets(taskptr, version1ispans, version2ispans,
                           &commonispans, ISPANID)                       // do1.c:446
      && ispansetandspecsets2spanpairset(taskptr, commonispans,
                                        version1, version2, relation);   // do1.c:447
}
```

Each step:

1. **Filter** (lines 440-441) — both documents filtered identically. Symmetric.
2. **V→I conversion** (lines 444-445) — each version converted to ispan space independently. Symmetric.
3. **Ispan intersection** (line 446) — set intersection is commutative: `ispans(A) ∩ ispans(B) = ispans(B) ∩ ispans(A)`. The output `commonispans` is the same set regardless of order. Symmetric.
4. **Pair generation** (line 447) — this is where the only meaningful asymmetry lives (see below).

---

### `ispansetandspecsets2spanpairset` — `backend/do2.c:185-207`

```c
restrictspecsetsaccordingtoispans(taskptr, ispanset, &specset1, &specset2);  // do2.c:196
makespanpairset(taskptr, ispanset, specset1, specset2, pairsetptr);           // do2.c:197
```

`restrictspecsetsaccordingtoispans` (`backend/correspond.c:18-50`) calls `restrictvspecsetovercommonispans` for specset1 and specset2 **independently** (lines 26 and 36). Each version's vspans are filtered by the common ispan set without reference to the other version. Swapping arguments produces swapped-but-equivalent filtered specsets.

---

### `makespanpairsforispan` — `backend/correspond.c:290-349`

This is the core pairing loop:

```c
spec1 = (typevspec *)*specset1ptr;   // correspond.c:304 → always version1 doc
span1 = spec1->vspanset;             // correspond.c:305
spec2 = (typevspec *)*specset2ptr;   // correspond.c:306 → always version2 doc
span2 = spec2->vspanset;             // correspond.c:307

while (span1 && span2 && tumblercmp(iwidth, &sum) == GREATER) {
    cmp = tumblercmp(&span1->width, &span2->width);   // correspond.c:309
    switch (cmp) {
      case LESS:
      case EQUAL:
        *pairsetptr = makespanpair(taskptr,
            &spec1->docisa, &span1->stream,    // doc=version1, stream=version1 position
            &spec2->docisa, &span2->stream,    // doc=version2, stream=version2 position
            &span1->width);                    // correspond.c:313 — width from span1
        // span1 advances, span2 truncated if LESS
        ...
        span1 = span1->next;                   // correspond.c:321
        break;
      case GREATER:
        *pairsetptr = makespanpair(taskptr,
            &spec1->docisa, &span1->stream,
            &spec2->docisa, &span2->stream,
            &span2->width);                    // correspond.c:324 — width from span2
        // span1 truncated, span2 advances
        ...
        span2 = span2->next;                   // correspond.c:328
    }
}
```

Trace what happens with two concrete cases:

| Condition | Width used | Who advances | Who is truncated |
|-----------|-----------|--------------|-----------------|
| `span1->width <= span2->width` (LESS/EQUAL) | `span1->width` | span1 | span2 |
| `span1->width > span2->width` (GREATER) | `span2->width` | span2 | span1 |

In both cases the width is **`min(span1->width, span2->width)`**, and the shorter span always exhausts and advances while the longer is trimmed. This is a symmetric merge — it does not treat one side as the reference.

**Now swap the arguments (B, A instead of A, B):**

- LESS/EQUAL (now `B_width <= A_width`): pair width = `B_width` = `min(A_width, B_width)` ✓ same
- GREATER (now `B_width > A_width`): pair width = `A_width` = `min(A_width, B_width)` ✓ same

The widths are identical. The truncation behavior (shorter span consumes, longer trims) is identical. The same ispan-indexed positions are covered.

The **only difference** is the output struct field order. `makespanpair` at `backend/correspond.c:351-361`:

```c
typespanpair *makespanpair(typetask *taskptr,
    tumbler *doc1, tumbler *start1,    // always from specset1 (first arg)
    tumbler *doc2, tumbler *start2,    // always from specset2 (second arg)
    tumbler *width)
{
    docidandvstream2tumbler(doc1, start1, &spanpair->stream1);  // correspond.c:357
    docidandvstream2tumbler(doc2, start2, &spanpair->stream2);  // correspond.c:358
    movetumbler(width, &spanpair->widthofspan);                 // correspond.c:359
    return (spanpair);
}
```

`stream1` is always the first argument's VSpec address; `stream2` is always the second. Swap the arguments and you get `stream1↔stream2` reversed in every pair.

---

### `spanintersection` symmetry — `backend/correspond.c:210-265`

The ispan intersection function computes `[max(a_start, b_start), min(a_end, b_end))` correctly in all three cases (EQUAL, GREATER, LESS). Despite the 1984 comment `/* these following assignments are clearly wrong 12/4/84 */`, the math checks out:

- GREATER subcase (a_start > b_start, a_end > b_end): `tumblersub(&bend, &aptr->stream, &cptr->width)` = `b_end − a_start` ✓ [correspond.c:243]
- LESS subcase (a_start < b_start, a_end < b_end): `tumblersub(&aend, &bptr->stream, &cptr->width)` = `a_end − b_start` ✓ [correspond.c:255]

This function is symmetric: swapping `a` and `b` produces the same intersection span.

---

### Conclusion

**`compare_versions(A, B)` is symmetric with `compare_versions(B, A)` in all meaningful senses:**

1. The **common ispan set** is identical (set intersection is commutative) [`do1.c:446`]
2. The **width of every pair** is `min(span_A_width, span_B_width)` regardless of order [`correspond.c:309-328`]
3. The **same VSpec addresses** appear in the output — the same text ranges are found to correspond

The **one asymmetry** is representational: `spanpair->stream1` always holds the first-argument document's VSpec, and `spanpair->stream2` always holds the second-argument's VSpec [`correspond.c:357-358`]. Swapping (A, B) → (B, A) swaps stream1 and stream2 in every output pair, but the underlying correspondence (same width, same addresses, same content relationships) is identical.

No document is treated as the "reference" in the matching algorithm. The correspondence is a symmetric join.
