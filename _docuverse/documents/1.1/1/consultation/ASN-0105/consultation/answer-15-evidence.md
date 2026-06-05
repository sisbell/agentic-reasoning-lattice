## Question 15 [evidence]

> For a read span that extends beyond the document's current root width, does the operation clamp to the existing content boundary, or does it return content up to the requested width including empty trailing positions?

## KB Synthesis

The KB does not contain a finding that directly tests `retrieve_contents` with a span extending beyond the root width. I cannot give you a definitive answer from the KB alone, but the indirect evidence strongly implies **clamping to existing content**.

The retrieval path is: `doretrievev` → `specset2ispanset` → POOM lookup via `retrieverestricted`. Per [INV-ITOV-FILTERING], the I-to-V conversion layer silently excludes any I-address that has no POOM mapping — `retrieverestricted` returns NULL and the position is dropped without error. V-positions beyond the root width have no POOM entries, so they contribute nothing to the result set.

This is consistent with [EC-SEARCH-SPEC-BEYOND-BOUNDS], which confirms that for `find_links`, out-of-bounds specs are accepted without error and the backend intersects against whatever content remains — clamping, not padding.

The behavior appears to be: **return only content that maps to existing POOM entries, silently ignoring any portion of the requested span beyond the current document extent**. No error, no empty trailing positions — just a shorter result than requested.

That said, the KB has no golden test directly confirming this for retrieve specifically. If this boundary condition is spec-critical, it warrants an explicit finding.

---

## Code Exploration

I now have everything I need. Here is the full analysis with citations.

---

## Answer: Read Span Beyond Document Root Width

**Bottom line:** The operation clamps to existing content. Udanax-green returns only actual content that falls within the requested span — there are no empty trailing positions, because the enfilade model does not represent empty space.

---

### Execution Path

The retrieve entry point is `fns.c:retrievev()`, which calls `doretrievev()` in `do1.c`. That function converts the virtual spec to an ispan via `specset2ispanset()` [do2.c:14], then passes the ispan to `ispan2vstuffset()` [granf2.c:286].

Inside `ispan2vstuffset()` [granf2.c:286–318], the requested ispan is decomposed into `lowerbound` and `upperbound`:

```c
// granf2.c:295–297
movetumbler (&ispanptr->stream, &lowerbound);
tumbleradd(&lowerbound, &ispanptr->width, &upperbound);
context = retrieveinspan ((typecuc*)fullcrumptr, &lowerbound, &upperbound, WIDTH);
```

The critical behavior is inside `retrieveinspan()` [retrie.c:112–136].

---

### The Out-of-Bounds Condition in `retrieveinspan`

```c
// retrie.c:120–127
switch (fullcrumptr->cenftype) {
  case GRAN:
        findcbcinspanseq ((typecorecrum*)fullcrumptr, &offset, spanstart, spanend, &context);
        if (tumblercmp (spanend, &fullcrumptr->cwid.dsas[WIDTH]) == GREATER) {
                c = findlastcbcseq ((typecorecrum*)fullcrumptr);
                oncontextlistseq (&context, c);
        }
        return (context);
```

**Step 1 — normal intersection scan [line 122]:** `findcbcinspanseq()` walks the enfilade and collects every bottom crum (actual content node) whose address range physically overlaps `[spanstart, spanend]`. The intersection test is at [retrie.c:423–430]:

```c
// retrie.c:423–430
bool crumintersectsspanseq(...)
{
    if (iszerotumbler (&crumptr->cwid.dsas[WIDTH])) return(FALSE);
    return ((whereoncrum (crumptr, ..., spanstart, WIDTH) < ONMYRIGHTBORDER)
             && (whereoncrum (crumptr, ..., spanend, WIDTH) >/*=*/ ONMYLEFTBORDER));
}
```

This is standard interval intersection: only crums that actually exist within the span are collected. No phantom crums exist beyond the document boundary.

**Step 2 — explicit out-of-bounds extension [lines 123–126]:** If `spanend` is **strictly greater than** `fullcrumptr->cwid.dsas[WIDTH]` (the root's total width), the code additionally appends the very last crum via `findlastcbcseq()`. That function [retrie.c:138–158] traverses rightward through the tree to the last bottom crum and returns it as a context.

This means: when a span extends past the end, the last real crum is explicitly added to the result list (potentially a second time if it was already found by `findcbcinspanseq`).

---

### Content Clipping in `context2vtext`

Each collected context is processed through `context2vstuff()` [context.c:240] → `context2vtext()` [context.c:277–309]. The clipping logic is:

```c
// context.c:291–307
vtlength = context->contextinfo.granbottomcruminfo.granstuff.textstuff.textlength;
if (tumblercmp (&crumistart, &ispanstart) == LESS) {
    i = tumblerintdiff (&ispanstart, &crumistart);
    vtlength -= i;
}
if (tumblercmp (&crumiend, &ispanend) == GREATER) {
    vtlength -= tumblerintdiff (&crumiend, &ispanend);
}
((typetext *)vstuffset)->length = vtlength > 0 ? vtlength : -vtlength;
```

- **Left-trim [line 294]:** if the crum starts before `ispanstart`, the returned slice begins at `ispanstart`.
- **Right-trim [line 301]:** if the crum ends **after** `ispanend`, the returned slice ends at `ispanend`.

For a crum that ends *before* `ispanend` (i.e., inside the document boundary but the span requests more), neither condition fires on the right side — the crum's full remaining content is returned, with no padding.

Zero-length results are suppressed at [context.c:261]: `if (((typetext *)vstuffset)->length == 0) return (FALSE);`.

---

### What Gets Returned

For a read span `[S, S+W]` where `S+W > doc_width`:

1. All crums whose address ranges intersect `[S, doc_width]` are collected by `findcbcinspanseq`.
2. The last crum is also appended unconditionally by `findlastcbcseq` + `oncontextlistseq` [retrie.c:124–125].
3. Each crum's content is clipped to `[S, S+W]` on the left, but since `S+W` is past the document, no right-clipping occurs for any crum.
4. The returned `vstuffset` contains exactly the content that exists within the document — nothing more.

**There are no empty trailing positions.** Udanax-green's enfilade model only stores content at insertion points. Addresses beyond the last inserted character simply have no crums, so no contexts are returned for them. The response ends at the actual last character of the document, not at the requested span boundary.

---

### One Edge Case to Note

When `spanend > doc_width` AND the requested span also overlaps real content, `findlastcbcseq` appends the last crum a second time (since `findcbcinspanseq` will already have found it). Both contexts pass through `context2vstuff`/`context2vtext` with identical parameters, potentially producing **duplicate content** for the last crum in the returned set. This is a latent defect in `retrieveinspan` [retrie.c:122–126] — the guard for `spanend > doc_width` does not check whether the last crum was already collected.
