## Question 14 [evidence]

> When two requested spans map to I-addresses that are contiguous in I-space, does retrieval merge them into one returned fragment, or preserve the V-span partition from the request?

## KB Synthesis

The KB does not contain explicit evidence to answer this question definitively. Here is what it does establish:

**What the KB says about retrieval structure:**

[INV-SPECSET-ORDER] establishes that retrieval concatenates results in VSpec order — the client receives output corresponding to each VSpec in sequence. The concrete example in [SS-SPECSET] ("quicklazy") shows two VSpecs concatenated, but those spans are not known to be contiguous in I-space.

[SS-GRANF-OPERATIONS] describes `ispanset2vstuffset()` simply as dereferencing I-addresses to content bytes — no merging behavior is described.

[SS-CONTEXT-LIST] (Finding 0078) notes that GRAN enfilade retrieval uses `oncontextlistseq()`, which appends in tree-traversal order. For 1D GRANs, tree order preserves sequential I-address order, so contiguous I-spans would be encountered and appended consecutively — but whether the *output layer* coalesces them is not addressed.

**The closest related evidence:**

[ST-VCOPY-CONTIGUITY] (Finding 0033) shows that contiguous I-address ranges from separate V-span vcopy operations coalesce at the *destination POOM level*, not at retrieval time. [INV-VSPAN-CONSOLIDATION] applies to `retrieve_vspanset` output (POOM span decomposition), not to `retrieve_contents` byte output.

**Conclusion:** The KB does not address whether `ispanset2vstuffset` merges contiguous I-spans from separate VSpecs before returning bytes to the client. The retrieval-layer behavior for this specific case is not answerable from the KB.

---

## Code Exploration

## Answer

**Retrieval preserves the V-span partition from the request — contiguous I-space fragments are NOT merged.**

The evidence is unambiguous across four call layers:

---

### 1. `permute()` iterates per-V-span, never consolidates

`backend/orglinks.c:404–416`:
```c
typespanset *permute(...) {
    /*consolidatespans(restrictionspanset);   ← COMMENTED OUT */
    for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
        targspansetptr = span2spanset(..., restrictionspanset, ...);
    }
}
```

The dead code at line 412 is decisive: `consolidatespans()` would have merged contiguous spans before processing, but it was explicitly disabled. The loop at lines 414–416 processes **each V-span in isolation**, one per iteration.

---

### 2. `span2spanset()` appends without merging

`backend/orglinks.c:425–454`: For each V-span, `span2spanset()` calls `retrieverestricted()` to find matching I-space contexts, then calls `onitemlist()` once per found context to append the result. There is no adjacency check between successive results.

---

### 3. `onitemlist()` is a pure linked-list append

`backend/orglinks.c:534`:
```c
((typeitemheader *)temp)->next = (typeitemheader *)newitem;
```

No coalescence logic. Fragments accumulate as separate list nodes regardless of I-space adjacency.

---

### 4. `incontextlistnd()` sorts but never merges

`backend/context.c:75–111`: The context insertion function maintains sorted order by tumbler position (`whereoncontext()` comparisons at lines 90, 97), but it **only inserts** — there is no code path that checks whether a new context is contiguous with an existing one and merges them.

---

### Conclusion

If a request specifies two V-spans `[A, B]` and `[C, D]` that happen to map to contiguous I-addresses `[i₁, i₂]` and `[i₂, i₃]` (i.e., the I-spans share a boundary), retrieval returns **two separate fragments**, not one merged fragment `[i₁, i₃]`. The V-span boundaries drive the fragment count; I-space contiguity is irrelevant to the output structure.

The commented-out `consolidatespans()` at `backend/orglinks.c:412` confirms this was a conscious design choice — or an abandoned optimization — not an oversight.
