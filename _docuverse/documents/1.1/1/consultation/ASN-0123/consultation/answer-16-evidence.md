## Question 16 [evidence]

> What exactly does `doretrievedocvspanfoo` use as the boundary to exclude the link subspace when extracting the text-only span for copying — a fixed cut at V=2.0, or the actual extent of subspace `1.x` — and what happens if the source's text subspace is empty?

## KB Synthesis

## What `doretrievedocvspanfoo` uses as its boundary

The answer is neither a fixed cut at V=2.0 nor a scan of the actual text extent — it reads the POOM root's raw V-dimension displacement and width fields directly.

### Mechanism

`doretrievedocvspanfoo` (at `do1.c:305-313`) delegates immediately to `retrievedocumentpartofvspanpm()` (at `orglinks.c:155-162`). That function reads two fields from the document's POOM root crum:

- `cdsp.dsas[V]` — the root's V-dimension displacement, which points to the start of the text subspace (position `1.x`)
- `cwid.dsas[V]` — the root's V-dimension width, covering only the text extent

The returned single vspan is `[cdsp.dsas[V], cdsp.dsas[V] + cwid.dsas[V])`. [SS-DUAL-ENFILADE (Finding 0043)]

This is **not** a fixed cut at V=2.0. It is a structural consequence of how the POOM root's V-dimension fields are maintained: text insertions at `1.x` are what cause `cdsp.dsas[V]` to land at `1` and `cwid.dsas[V]` to track the text width. Link entries at `2.x` are structurally outside this interval — they live at a higher V-position than `cdsp + cwid` — so they are excluded automatically without any explicit boundary computation. The code comment in Finding 0046 describes this function as "a kluge," confirming it is a direct read of internal structural state, not a semantically aware extraction. [SS-VSPAN-VS-VSPANSET (Finding 0035)], [ST-VERSION-CREATE (Finding 0046)]

The contrast with `retrievevspansetpm()` is instructive: that function uses `is1story()` to explicitly detect and partition subspaces. `retrievedocumentpartofvspanpm` does no such test — it just copies the root's V-dimension extent, which happens to cover only text because that's what was put there. [SS-VSPAN-VS-VSPANSET (Finding 0035)]

### What happens when the text subspace is empty

From [SS-ENFILADE-TREE (Finding 0066)]: when all children of a 2D enfilade are deleted, `setwispnd` at `wisp.c:187-189` clears **both** `cdsp` and `cwid` to zero. So for a document that never had text, or one from which all text was deleted, the root holds `cdsp.dsas[V] = 0` and `cwid.dsas[V] = 0`.

`retrievedocumentpartofvspanpm` returns this zero-extent span. `docopyinternal` called with a zero-width vspan copies nothing. The result is a new document address allocated with no content — an empty version. [EC-EMPTY-DOC (Finding 0007)] confirms this edge case works: versioning an empty document succeeds and the version is also empty.

Note that there are two distinct empty states (never-filled vs. delete-everything) which have different internal tree structures [EC-EMPTY-DOC (Finding 0058)], but both produce `cwid.dsas[V] = 0` at the root after `setwispnd` runs, so both produce the same zero-width vspan from `doretrievedocvspanfoo`.

---

## Code Exploration

I now have a complete picture. Let me consolidate the full answer.

---

## Answer

### 1. What boundary does `doretrievedocvspanfoo` use?

**Neither a fixed cut at V=2.0 nor the actual extent of subspace 1.x. It returns the raw total V-extent of the document — text and links combined — without any boundary logic at all.**

The call chain is:

**`do1.c:301-308`** — `doretrievedocvspanfoo`:
```c
bool doretrievedocvspanfoo(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{ /* this routine is a kluge not yet kluged*/
  typeorgl docorgl;
  bool findorgl(), retrievedocumentpartofvspanpm();
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, NOBERTREQUIRED)
    && retrievedocumentpartofvspanpm (taskptr, docorgl, vspanptr) );
}
```

**`orglinks.c:155-162`** — `retrievedocumentpartofvspanpm`:
```c
bool retrievedocumentpartofvspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{ /* this is a kluge*/
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
    return (TRUE);
}
```

`cdsp.dsas[V]` is the POOM root crum's V-dimension displacement (start address) and `cwid.dsas[V]` is its V-dimension cumulative width. Both are raw values from the enfilade root — the total spanning all inserted content. No filtering is applied.

The "documentpart" in the name is aspirational. The body is byte-for-byte identical to `retrievevspanpm` at `orglinks.c:165-172`:

```c
bool retrievevspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
    return (TRUE);
}
```

They are completely identical. The intended subspace separation was never written.

---

### 2. The V-address subspace layout

The link subspace boundary matters here. From `findnextlinkvsa` at `do2.c:151-167`, the first link V-address is built as:

```c
tumblerincrement (&firstlink, 0, 2, &firstlink);  // mantissa[0] = 2 → tumbler = 2
tumblerincrement (&firstlink, 1, 1, &firstlink);  // mantissa[1] = 1 → tumbler = 2.1
```

The first link position is `2.1`. If the current document extent (stream + width) is already past `2.1`, the next link goes beyond it. So in V-space: text lives around `1.x`, links start at `2.1` or later.

The code that *does* properly separate the subspaces is `retrievevspansetpm` at `orglinks.c:173-219`, which:
- Checks `is1story(&ccptr->cwid.dsas[V])` — if the width has only one tumbler digit, the document is text-only [`orglinks.c:184`]
- If multi-story (has text and links), extracts the link subspace by zeroing `mantissa[1]` of `cwid` [`orglinks.c:198-203`]
- Extracts the text subspace via `maxtextwid` [`orglinks.c:207`], which recursively walks the tree skipping `islinkcrum` nodes [`orglinks.c:240`]

`doretrievedocvspanfoo` bypasses all of this and calls `retrievedocumentpartofvspanpm` instead.

---

### 3. What happens if the source text subspace is empty?

`retrievedocumentpartofvspanpm` **always returns `TRUE`** and blindly copies whatever `cdsp.dsas[V]` and `cwid.dsas[V]` happen to hold. There is no empty-document check.

Three cases:

**Case A — document is completely empty:** `cdsp.dsas[V]` and `cwid.dsas[V]` are zero tumblers. The function sets `stream = 0`, `width = 0`, returns `TRUE`. The caller (`docreatenewversion` at `do1.c:281-293`) then calls `docopyinternal` with this zero-width vspan. That reaches `specset2ispanset` → `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted`, which finds no I-addresses in a zero-width span. The new version is created but has no content copied into it.

Contrast with `doretrievedocvspanset` at `do1.c:322-336`, which **does** guard for this:
```c
if (isemptyorgl (docorgl)) {
    *vspansetptr = NULL;  /* Empty document returns empty vspanset */
    return TRUE;
}
```
`doretrievedocvspanfoo` has no analogous guard.

**Case B — document has text that was all deleted:** Same as Case A; the root crum retains the last extent but the enfilade may have no bottom crums for that range. `retrieverestricted` returns empty context.

**Case C — document has only links, no text:** `cwid.dsas[V]` reflects the link subspace extent only (rooted at `2.1`). `retrievedocumentpartofvspanpm` returns that span as the text span. `docopyinternal` then attempts to copy the link subspace into the new version, passing link ISAs (document ISAs like `1.1.0.x.x.x`) through `specset2ispanset` as if they were text I-addresses. The V→I lookup via `vspanset2ispanset`/`permute` will retrieve those link ISAs and `insertpm` will insert them at the target V-address in the new document — reproducing the link references without the text, with no error raised.

---

### 4. The admitted design status

Both functions are labeled kluges:

- `do1.c:302`: `/* this routine is a kluge not yet kluged*/`
- `orglinks.c:156`: `/* this is a kluge*/`

The phrase "kluge not yet kluged" means: this is a temporary placeholder that *knows* it needs to be corrected to actually isolate the document (text) part of the V-span, but the correction has not been written. The function name promises subspace separation; the body delivers nothing of the kind.

`acceptablevsa` at `do2.c:110-113` — the V-address range validator called by `docopyinternal` — is equally stubbed:
```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

So there is no boundary check at any layer in the copy path. Whatever span `retrievedocumentpartofvspanpm` returns — zero, text-only, links-only, or combined — is passed unchanged through the entire pipeline.
