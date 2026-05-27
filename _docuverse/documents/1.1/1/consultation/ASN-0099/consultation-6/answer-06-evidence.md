## Question 6 [evidence]

> What does the udanax-green implementation do when a FINDLINKS-equivalent query nominates V-positions outside dom(M(d)) — reject with an error, silently filter to in-domain positions, or rely on the caller to pre-validate?

## KB Synthesis

The implementation silently filters to in-domain positions — no error is returned, and the caller is not required to pre-validate.

## Mechanism

The `find_links` call chain converts V-positions to I-addresses before searching the spanfilade:

```
V-specset → specset2ispanset → vspanset2ispanset → permute → span2spanset → retrieverestricted (POOM)
```

At `retrieverestricted`, each V-position is looked up in the document's POOM. When a V-position has no mapping in dom(M(d)) — either never populated or removed by DELETE — `retrieverestricted` returns NULL. `span2spanset` drops that address silently rather than raising an error [SS-FOLLOWLINK / Finding 0048, `orglinks.c:446-448`]. The result is zero I-addresses contributed by that position.

With no I-addresses, the intersection with link endpoint I-addresses in the spanfilade is empty for that position. The overall `find_links` call still succeeds; it returns whatever links matched the surviving in-domain I-addresses.

## Direct Evidence

[EC-SEARCH-SPEC-BEYOND-BOUNDS] / Finding 0029 confirms this experimentally: a search spec referencing positions beyond the current document extent (after content was deleted) neither errors nor hangs — it "gracefully intersects with whatever content remains." The backend clips the effective search to the current V-stream extent.

[PRE-FIND-LINKS] / Finding 0029 formalizes this: `find_links(spec) ≠ ∅ → ∃ overlap(spec ∩ V-stream, link.endpoint ∩ V-stream)`. Positions outside dom(M(d)) contribute nothing to that overlap.

## Why No Validation is Enforced

[PRE-SPECSET] / Finding 0001 establishes the validation boundary: `specset2sporglset()` checks only that the referenced document exists. It does not validate V-position membership or element-level structure. [SS-SUBSPACE-CONVENTION] / Finding 0010 further confirms `acceptablevsa()` always returns TRUE, meaning even cross-subspace V-positions pass through unchallenged.

## Summary

Out-of-domain V-positions are silently filtered during the V-to-I conversion step. The operation completes successfully with an empty or reduced match set. Responsibility for querying meaningful V-positions lies entirely with the caller — consistent with the system's general convention-over-enforcement philosophy [SS-SUBSPACE-CONVENTION / Finding 0011].

---

## Code Exploration

I have all the evidence I need. Here is my complete answer.

---

## What udanax-green does with out-of-domain V-positions in FINDLINKS

**Short answer: silently filters to empty — no rejection, no error, no pre-validation requirement.**

The implementation has three layers relevant to this question. I traced each one.

---

### Layer 1 — The `acceptablevsa` stub (`do2.c:110-113`)

The one function whose name suggests V-address validation:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

`do2.c:110-113`. It is an unconditional stub. It was never implemented. More importantly, **it is not called on the FINDLINKS path at all** — only `docopy` (`do1.c:56`) and `docopyinternal` (`do1.c:76`) call it, both for the COPY operation. FINDLINKS bypasses it entirely.

---

### Layer 2 — The FINDLINKS dispatch chain

`fns.c:189-202` — `findlinksfromtothree()`:

```c
if (
   getfindlinksfromtothree (taskptr, &fromvspecset, &tovspecset, &threevspecset, &homeset)
&& dofindlinksfromtothree (taskptr, fromvspecset, tovspecset, threevspecset, (typeispan*)NULL, &linkset))
    putfindlinksfromtothree (taskptr, linkset);
  else
    putrequestfailed (taskptr);
```

`do1.c:348-353` — `dofindlinksfromtothree()` delegates immediately to `findlinksfromtothreesp()` with no validation:

```c
bool dofindlinksfromtothree(typetask *taskptr, typespecset fromvspecset, ...)
{
  bool findlinksfromtothreesp();
    return findlinksfromtothreesp(taskptr, spanf, fromvspecset, tovspecset, threevspecset, orglrangeptr, linksetptr);
}
```

`spanf1.c:56-103` — `findlinksfromtothreesp()` converts each specset to a sporglset, then queries the spanfilade:

```c
if (fromvspecset)
    specset2sporglset (taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);   // line 71
if (tovspecset)
    specset2sporglset (taskptr, tovspecset, &tosporglset, NOBERTREQUIRED);       // line 73
if (threevspecset)
    specset2sporglset (taskptr, threevspecset, &threesporglset, NOBERTREQUIRED); // line 75
if (fromvspecset) {
    sporglset2linkset (taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, ...);
    if (!fromlinkset) {
        *linksetptr = NULL;
        return (TRUE);   // early short-circuit: empty from-set → return empty
    }
}
```

Note the early-return at `spanf1.c:78-82`: if the from-endpoint yields an empty sporglset, the function returns `TRUE` with `*linksetptr = NULL` immediately — it does not error. The same pattern repeats for to-set (`spanf1.c:86-90`) and three-set (`spanf1.c:94-98`).

---

### Layer 3 — The V-to-I conversion: where out-of-domain positions disappear

`specset2sporglset` routes through `do2.c:14-46` → `vspanset2ispanset` at `orglinks.c:397-402`:

```c
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl, typevspanset vspanptr, typeispanset *ispansetptr)
{
  typespanset *permute();
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

`permute()` at `orglinks.c:404-422` iterates the V-spans and calls `span2spanset()` for each.

`span2spanset()` at `orglinks.c:425-435` does the actual work:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex, (typespan*)NULL, targindex, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
if (!context) {
    return(targspansetptr);   // empty context → return unchanged pointer, nothing added
}
```

If `retrieverestricted` returns no context, `span2spanset` returns immediately having added nothing to the output spanset. **No error. No FALSE return. Silently no-ops.**

---

### Layer 4 — Why `retrieverestricted` returns empty for out-of-domain spans

`retrie.c:56-85` — `retrieverestricted()` unpacks the span bounds and calls `retrieveinarea()`, which calls `findcbcinarea2d()`.

`retrie.c:229-268` — `findcbcinarea2d()` iterates the POOM enfilade crums and calls `crumqualifies2d()` for each:

```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (crumptr, offsetptr, span1start, span1end, ...))
        continue;        // skip non-qualifying crums
    ...
}
```

`retrie.c:270-305` — `crumqualifies2d()` applies two boundary tests:

```c
endcmp = iszerotumbler (span1end) ? TOMYRIGHT : whereoncrum (crumptr, offset, span1end, index1);
if ( endcmp <= ONMYLEFTBORDER) {
    return(FALSE);   // query span ends before this crum starts → skip   (line 283-285)
}
startcmp = whereoncrum (crumptr, offset, span1start, index1);
if ( startcmp > THRUME ) {
    return(FALSE);   // query span starts after this crum ends → skip    (line 287-290)
}
```

The POOM enfilade only contains crums for V-addresses that actually exist in the document. If a queried V-span is entirely outside dom(M(d)), every crum in the tree will fail one of these tests — none qualify — `findcbcinarea2d` accumulates zero contexts — `retrieverestricted` returns `NULL`.

There is no explicit check against the document's V-extent (`cwid.dsas[V]` / `cdsp.dsas[V]`, read out in `orglinks.c:159-160`). The filtering emerges implicitly from the enfilade structure: crums that don't exist for those positions simply are not there.

---

### Summary

| What happens | Answer |
|---|---|
| Explicit rejection / error on out-of-domain V-positions? | **No.** No code path returns `FALSE` or calls `gerror` for this reason. |
| `acceptablevsa` validates bounds? | **No.** It is an unconditional `return TRUE` stub (`do2.c:110-113`), and is not called on the FINDLINKS path. |
| Caller required to pre-validate? | **No.** The protocol accepts any V-specset. |
| What actually happens? | **Silent empty-result filtering.** `crumqualifies2d` (`retrie.c:283-290`) rejects every crum not intersecting the queried span; an out-of-domain span matches nothing; `span2spanset` returns an empty spanset; `sporglset2linkset` returns an empty link set; `findlinksfromtothreesp` returns `TRUE` with `*linksetptr = NULL`. |

The design is permissive by construction. The retrieval layer (`findcbcinarea2d` / `crumqualifies2d`) is the sole enforcer of spatial containment, and it enforces it by producing empty results rather than errors. A FINDLINKS query nominating V-positions outside dom(M(d)) succeeds — it just finds no links.
