## Question 1 [evidence]

> Does udanax-green validate or normalize the start tumbler of a V-span in a spec-set (e.g., reject starts with zero components or non-position tumblers) before resolving it, or does it accept any boundary tumbler and resolve purely by intersection with bound positions?

## KB Synthesis

The KB gives a clear, consistent answer: **udanax-green performs no normalization or structural validation on V-span start tumblers before resolution. It accepts any tumbler and resolves purely by intersection against current POOM state.**

---

**What validation actually occurs**

The entry point for specset resolution, `specset2sporglset()`, validates only document existence [PRE-SPECSET]:

> The backend's `specset2sporglset()` validates specsets at document granularity only. It checks that the referenced document exists but does not enforce element-level tumbler structure. A specset referencing a valid document but with missing or malformed element fields is accepted without error.

The precondition is strictly: `exists doc : doc_id(tumbler) in created_documents`. No constraint on the element or V-position fields.

---

**The `acceptablevsa()` stub**

For operations that place content at a V-address, the validation hook `acceptablevsa()` is a no-op [PRE-INSERT, Finding 0049, Finding 0011]:

> `acceptablevsa()` in `do2.c:110-113` unconditionally returns `TRUE`, providing no runtime enforcement.

This means even zero-subspace tumblers, link-subspace tumblers, or malformed hierarchical tumblers pass through without rejection. [INT-CLIENT-VALIDATION] notes this is explicitly the design — the backend assumes the caller constructs correct addresses.

---

**Resolution is purely intersection-based**

Once a V-span reaches the POOM, resolution uses `whereoncrum()` [SS-WHEREONCRUM], which classifies the address into five spatial relationships (`TOMYLEFT`, `ONMYLEFTBORDER`, `THRUME`, `ONMYRIGHTBORDER`, `TOMYRIGHT`) relative to existing crum intervals. Crums that don't intersect the query range simply fall into `TOMYLEFT` or `TOMYRIGHT` and are skipped. There is no guard that rejects the input tumbler — addresses with no intersection just produce empty results.

This is confirmed empirically by [EC-SEARCH-SPEC-BEYOND-BOUNDS]:

> When a search spec references positions that no longer exist in the V-stream (e.g., after deletion shrinks the document), `find_links()` does not error. It gracefully intersects with whatever content remains, still finding links on surviving content.

---

**Minimal bounds that do exist**

There are two narrow guards, neither of which constitutes normalization:

1. **Zero tumbler rejection in `insertpm()`** — Finding 0049 cites that `insertpm()` rejects zero tumblers (`iszerotumbler`) and negative tumblers at lines 86–98. But this applies only to the INSERT placement path, not to query/retrieval specsets. [PRE-ZERO-WIDTH] confirms zero-width *retrieval* specsets are accepted and return empty results.

2. **`strongsub` exponent guard** — When V-address arithmetic crosses exponent boundaries, `strongsub` returns the minuend unchanged rather than computing a subtraction [SS-TUMBLER, Finding 0055]. This is an arithmetic no-op, not a validation rejection.

---

**Summary**

The backend accepts any syntactically valid tumbler as a V-span start and resolves by pure POOM intersection. Subspace membership, element-level hierarchical structure, and boundary alignment are caller-enforced conventions with no backend validation. Out-of-range or structurally odd tumblers produce empty results, not errors — except for the narrow case of zero-tumbler placement in INSERT, and zero-width spans in `create_link` (which crash rather than rejecting cleanly) [PRE-ZERO-WIDTH].

---

## Code Exploration

I have all the information needed to give a complete, cited answer.

---

## Answer: V-span Start Tumbler Validation in udanax-green

**Short answer: udanax-green performs almost no validation or normalization of V-span start tumblers before resolving them. The only pre-resolution check is that the `docisa` (document address) must be non-zero. Everything else resolves purely by enfilade intersection arithmetic.**

---

### Execution Path for `retrievev`

The path is:

```
fns.c:retrievev
  → fns.c:getretrievev + doretrievev
    → get2.c:getspecset → getvspec → getspan → gettumbler   [wire parsing]
    → do1.c:doretrievev → do2.c:specset2ispanset              [V→I conversion]
      → orglinks.c:vspanset2ispanset → permute → span2spanset
        → retrie.c:retrieverestricted → retrieveinarea
          → retrie.c:findcbcinarea2d → crumqualifies2d        [intersection test]
```

---

### 1. Wire Parsing — No Shape Validation (`get2.c:71–96`, `228–238`)

`gettumbler` reads the stream and width digits from the wire. It:
- Accepts an optional leading `-` (negative tumblers are not rejected at parse time) [`get2.c:76–77`]
- Adjusts `exp` for leading zeros but performs no structural checks
- Does not reject zero-component tumblers, non-position tumblers, or any particular shape

`getspan` simply calls `getisa` (= `gettumbler`) twice for `stream` and `width` without adding any guards [`get2.c:228–238`]:

```c
bool getspan(typetask *taskptr, typespan *spanptr, char id)
{
    prompt(taskptr, "enter span\n       start=> ");
    if (!getisa(taskptr, &spanptr->stream))
        return(FALSE);
    spanptr->itemid = id;
    prompt(taskptr, "	width=> ");
    if(!(getisa(taskptr, &spanptr->width)))
            return(FALSE);
    return(TRUE);
}
```

---

### 2. The Only Pre-Resolution Check: `docisa != 0` (`do2.c:14–46`)

`specset2ispanset` iterates the specset. When it encounters a `VSPECID` item, it checks **only one thing** — that the document ISA is non-zero [`do2.c:28–32`]:

```c
if (iszerotumbler (&((typevspec *)specset)->docisa))
#ifndef DISTRIBUTION
    qerror ("retrieve called with docisa 0\n");
#else
    gerror("");
#endif
```

If the docisa is non-zero, it immediately proceeds to `findorgl` → `vspanset2ispanset` with no inspection of the V-span's `stream` or `width`.

---

### 3. `acceptablevsa` Is a Permanent Stub (`do2.c:110–113`)

There is a function named `acceptablevsa` that would be the natural place for boundary validation:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

It always returns `TRUE` unconditionally. Furthermore, it is **not called on the read path at all** — it appears only in `docopy` [`do1.c:56`] and `docopyinternal` [`do1.c:76`], not in `doretrievev` [`do1.c:338–346`].

---

### 4. V→I Conversion Passes the Tumbler Directly (`orglinks.c:397–453`)

`vspanset2ispanset` → `permute` → `span2spanset` iterate the V-span list and call `retrieverestricted` with the raw `stream` (start) tumbler and the computed end (`stream + width`). No normalization or shape check occurs in this chain.

`retrieverestricted` [`retrie.c:56–85`] simply copies `span.stream` into `span1start` and `tumbleradd(&span1start, &span1ptr->width, &span1end)` to compute the end — again, no validation.

---

### 5. Resolution Is Purely by Intersection (`retrie.c:270–305`)

The final gate is `crumqualifies2d`. It tests whether a crum's content range intersects the given span using `whereoncrum` + `tumblercmp`. There are two notable edge-case behaviors:

```c
endcmp = iszerotumbler (span1end) ? TOMYRIGHT : whereoncrum (crumptr, offset, span1end, index1);
```

- **Zero-width span** (width == 0): `span1end` = `stream + 0` = `stream` (not zero). Treated normally — a zero-width span selects nothing because the right boundary equals the left.
- **Zero `span1end`** (which would occur if `stream` is zero and width is zero, so both are zero): the `iszerotumbler(span1end)` branch fires and treats the right bound as `TOMYRIGHT`, meaning the span would cover all content. This is the one case where a zero start tumbler could have an effect, but it results in an unbounded match, not a rejection.

For any non-zero start tumbler, `crumqualifies2d` just checks arithmetic intersection and returns `TRUE` if the crum overlaps, regardless of the tumbler's number of components or positional structure.

---

### Summary

| Check | Location | Result |
|---|---|---|
| `docisa` == 0 | `do2.c:28` | `qerror` — rejected |
| V-span `stream` has zero components | — | **Not checked** |
| V-span `stream` is negative | — | **Not checked at parse or resolve time** |
| V-span `stream` is a non-position tumbler | — | **Not checked** |
| `acceptablevsa` | `do2.c:110–113` | Stub, always `TRUE`; not called on read path |
| Resolution logic | `retrie.c:270–305` | Pure intersection arithmetic |

udanax-green accepts any boundary tumbler in a V-span specset and resolves it entirely by intersection with bound positions in the enfilade. The only structural pre-condition enforced is that the document ISA must be non-zero. There is no normalization, no component-count check, and no rejection based on tumbler shape or address space membership.
