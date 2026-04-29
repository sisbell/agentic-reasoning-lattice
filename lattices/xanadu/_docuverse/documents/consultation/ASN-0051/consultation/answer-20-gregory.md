## Question 20 [gregory]

> When a link has a source endset spanning I-addresses `[i, i+10)` and a COPY transcludes only `[i+3, i+7)` into a target document, does `find_links` on the target document match L because the partial I-address overlap is sufficient, and does the returned endset for L show all three endsets (source, target, type) in full or only the overlapping portion of the queried endset?

## KB Synthesis

## Short answer

Yes, the partial overlap suffices for `find_links`. The **stored** endsets are always complete and immutable; what you get back when *resolving* them depends on which document context is used for I→V conversion.

---

## Part 1: Does partial overlap match?

Yes. `find_links` uses non-empty I-address intersection as its sole criterion:

> `find_links(S) = { L | I-addresses(S) ∩ I-addresses(L.source) ≠ ∅ }`

[SS-FIND-LINKS] (Finding 0028) gives the canonical example: a link on "DEF" (`I.4–I.6`) is discovered by a document containing only "EF" (`I.5–I.6`). Partial overlap is sufficient; there is no minimum-coverage threshold.

In the question's case: source endset is `[i, i+10)`, target POOM has `[i+3, i+7)`. Intersection is `[i+3, i+7)` ≠ ∅ → L is found. [SS-FIND-LINKS], [INT-LINK-TRANSCLUSION]

---

## Part 2: What the endsets show

Two distinct questions are embedded here: what is *stored* vs. what is *returned* in a given resolution context.

### Stored endsets: always complete

The link orgl contains the full endsets as specified at `create_link` time. No operation modifies them. [INV-LINK-PERMANENCE], [SS-LINK-ENDPOINT] (Finding 0028):

> "Link endpoints are immutable V-spans fixed at creation time."

All three endsets — source `[i, i+10)`, target, type — are stored in full and never trimmed.

### Resolved endsets: filtered by POOM context

[SS-FOLLOWLINK] (Finding 0048) describes the actual mechanism:

> `link2sporglset()` extracts I-addresses from the link orgl. Then `linksporglset2specset()` converts I-addresses to V-addresses by looking them up in the specified `homedoc`'s POOM. If an I-address has no POOM mapping, it is **silently dropped** — no V-span is added to the result.

This is the universal I→V filtering invariant [INV-ITOV-FILTERING]:

> `∀ op returning V-addresses: v ∈ result(op) → ∃ d, i : poom.d(v) = i ∧ i ∈ dom.ispace`

So the resolution outcome depends on context:

| Call | Context | Source endset returned |
|------|---------|----------------------|
| `follow_link(L, SOURCE, source_doc)` | source doc POOM has all `[i, i+10)` | Full `[i, i+10)` |
| `follow_link(L, SOURCE, target_doc)` | target doc POOM has only `[i+3, i+7)` | Partial: only those 4 bytes |
| `retrieve_endsets(target_vspan)` | resolves in target's V-space | Only `[i+3, i+7)` portion |

[SS-RETRIEVE-ENDSETS] (Finding 0035) makes the context-dependence explicit:

> "Key: endsets are resolved in terms of the querying document's V-space, not the link's home document."
> "The same link endset can produce different V-address results (or empty results) depending on which document context is used."

### The `follow_link` full-endset behavior in Finding 0028

[SS-FOLLOW-LINK] states: "Even when a link is found via partial I-address overlap, `follow_link` returns the full endpoint as it was specified at link creation time." This holds when the resolution context is the **source/home document** (which has all the I-address POOM mappings). The FEBE-level `follow_link` call uses the link's home document as resolution context by default, so the client sees the complete original specset — `retrieve_contents` on that result returns the full "hyperlink text" (14 chars), not the 4-char "link" that enabled discovery.

### Target and type endsets

These are unaffected by the partial transclusion. Their I-addresses live in other documents' POOMs. Resolution of the target endset depends on whether the target document is open and has those POOM mappings; the type endset resolves against the bootstrap document. Neither is filtered or shortened by the fact that only a partial source endset was transcluded. [SS-LINK-ENDPOINT], [FC-LINK-PERSISTENCE]

---

## Summary

- **Discovery**: `find_links` on the target matches L — partial I-address overlap `[i+3, i+7) ∩ [i, i+10)` is non-empty, which is sufficient. [SS-FIND-LINKS]
- **Stored endsets**: All three (source, target, type) are stored in full in the link orgl, permanently and immutably. [INV-LINK-PERMANENCE]
- **Resolved source endset from target doc**: Only the 4-byte overlapping portion `[i+3, i+7)` is returned, because only those I-addresses have V-position mappings in the target's POOM. The remaining `[i, i+3)` and `[i+7, i+10)` are silently dropped. [SS-FOLLOWLINK], [INV-ITOV-FILTERING]
- **Resolved source endset from source doc**: The full 10-byte range `[i, i+10)` is returned. [SS-FOLLOW-LINK]
- **Target and type endsets**: Returned in full, subject to their own document's POOM state, unaffected by the partial transclusion. [SS-LINK-ENDPOINT]

---

## Code Exploration

I have now traced the complete execution path through the source. Here is the full answer.

---

## Answer: `find_links` with Partial I-address Overlap

### Part 1 — Does `find_links` match L?

**Yes. Partial I-address overlap is sufficient.**

The call chain is:

```
find_links (fns.c:189)
  → dofindlinksfromtothree (do1.c:348-353)
  → findlinksfromtothreesp (spanf1.c:56-103)
  → sporglset2linkset (sporgl.c:222-237)
  → sporglset2linksetinrange (sporgl.c:239-269)
  → retrieverestricted (retrie.c:56-85)
  → findcbcinarea2d (retrie.c:229-268)
  → crumqualifies2d (retrie.c:270-305)
```

**Step-by-step:**

1. **V-to-I translation.** `findlinksfromtothreesp` converts the target-document V-spec (the range that covers the transcluded content) to I-spans via `specset2sporglset` → `vspanset2sporglset` → `vspanset2ispanset`. Because COPY preserves I-addresses, the target document's V-range maps to exactly `[i+3, i+7)` in permascroll space.

2. **Spanfilade query.** `sporglset2linksetinrange` (sporgl.c:239-269) calls:

   ```c
   prefixtumbler(&orglrange->stream, spantype, &range.stream);  // range = LINKFROMSPAN prefix
   context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, infoptr);
   ```

   - SPANRANGE restriction = `[i+3, i+7)` (the transcluded I-span)
   - ORGLRANGE restriction ≈ `[LINKFROMSPAN=1, LINKFROMSPAN+1=2)`

3. **The overlap test.** The match decision lives in `crumqualifies2d` (retrie.c:270-305):

   ```c
   endcmp = iszerotumbler(span1end) ? TOMYRIGHT : whereoncrum(crumptr, offset, span1end, index1);
   if (endcmp <= ONMYLEFTBORDER) return FALSE;     // query ends before crum starts
   startcmp = whereoncrum(crumptr, offset, span1start, index1);
   if (startcmp > THRUME) return FALSE;            // query starts after crum ends
   ```

   This is a standard half-open interval intersection test: a crum at `[i, i+10)` qualifies if the query endpoint `i+7` is after `i` (endcmp = THRUME, not ONMYLEFTBORDER or TOMYLEFT) **and** the query start `i+3` is before `i+10` (startcmp = THRUME ≤ THRUME). Both conditions hold. The crum qualifies.

4. **ORGLRANGE check.** The stored crum's ORGLRANGE was set during `insertspanf` (spanf1.c:22):
   ```c
   prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
   ```
   This gives `1.linkISA` — a sub-address under digit `1` = LINKFROMSPAN. The query range `[1, 2)` covers all `1.x` addresses, so the ORGLRANGE check passes for link L's crum.

5. **Result extraction.** The matching crum's ORGLRANGE address `1.linkISA` is stripped of the prefix via `beheadtumbler` (sporgl.c:264) and added to the link set. `find_links` returns L's ISA.

---

### Part 2 — What does the returned endset show?

**`find_links` itself returns only link ISA tumblers. No endset data is in the response.**

The return type is `typelinkset` (spanf2.c:122-135), which is a linked list of `typelink` records containing only an `address` tumbler — just the link's ISA. The from/to/type endsets are absent from the `find_links` response.

**When endsets are retrieved after `find_links`:**

**Via `follow_link(L, whichend)` → `dofollowlink` (do1.c:223-232):**

```c
link2sporglset(taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
```

`link2sporglset` (sporgl.c:67-95) opens **L's own POOM** (the link document's permutation matrix) and queries it at V-position `whichend`:

```c
findorgl(taskptr, granf, linkisa, &orgl, type);
tumblerincrement(&zero, 0, whichend, &vspan.stream);  // e.g., 1 = LINKFROMSPAN
tumblerincrement(&zero, 0, 1, &vspan.width);
context = retrieverestricted((typecuc*)orgl, &vspan, V, NULL, I, NULL);
```

This returns the I-spans stored at that V-position — which were written during link creation by `insertendsetsinorgl` → `insertpm` (do1.c:218, do2.c:130-148, orglinks.c:75-133). Those I-spans are the **full original from-endset `[i, i+10)`**, not clipped to `[i+3, i+7)`.

`follow_link` returns the from-endset (`LINK_SOURCE=1`) as a V-spec covering `[i, i+10)` in the source document. The target endset and type endset are each returned in full via `LINK_TARGET=2` and `LINK_TYPE=3`.

**Via `retrieve_endsets` → `retrieveendsetsfromspanf` (spanf1.c:190-235):**

Called with the home document's text content V-span, this queries the spanfilade for crums whose SPANRANGE overlaps the queried content and whose ORGLRANGE is in `[LINKFROMSPAN, LINKFROMSPAN+1)`, `[LINKTOSPAN, LINKTOSPAN+1)`, and `[LINKTHREESPAN, LINKTHREESPAN+1)` separately.

When a crum matches, `contextintosporgl` (sporgl.c:205-220) extracts the context's coordinates:

```c
movetumbler(&context->totaloffset.dsas[SPANRANGE], &sporglptr->sporglorigin);  // crum start = i
movetumbler(&context->contextwid.dsas[SPANRANGE], &sporglptr->sporglwidth);    // crum width = 10
```

These are the **full crum dimensions** — not clipped to the query window. The crum for L's from-endset has SPANRANGE = `[i, i+10)`, so `sporglorigin = i` and `sporglwidth = 10` regardless of the `[i+3, i+7)` query that found it.

`linksporglset2specset` → `sporglset2vspanset` → `ispan2vspanset` then translates this full I-span back to V-space in the source document.

---

### Summary

| Question | Answer | Citation |
|----------|--------|----------|
| Does partial I-overlap suffice to match? | **Yes** — `crumqualifies2d` uses interval intersection | retrie.c:282-300 |
| What does `find_links` return? | **Link ISA addresses only** — no endset data | spanf2.c:122-135 |
| Source endset from `follow_link` | **Full original span `[i, i+10)`** — unclipped | sporgl.c:67-95 |
| Target & type endsets from `follow_link` | **Full original spans** — unclipped | sporgl.c:67-95, do2.c:130-148 |
| What `retrieve_endsets` extracts | **Full crum SPANRANGE** — `totaloffset + contextwid`, not intersection | sporgl.c:205-220, spanf1.c:248-264 |

**The overlap `[i+3, i+7)` is a discovery filter only.** It determines which links are found via the spanfilade. But once a link is found, all three endsets (source `[i, i+10)`, target, type) are returned in their full, creation-time form from either the link's own POOM (`follow_link`) or the spanfilade crum coordinates (`retrieve_endsets`). No clipping to the queried overlap occurs at any level.
