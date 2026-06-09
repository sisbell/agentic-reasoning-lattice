## Question 12 [evidence]

> Given EC-FIND-LINKS-GLOBAL — that `sporglset2linkset` overrides the orgl filter with `TRUE||!homeset` and a hardcoded width of 100 — does the home-set criterion actually constrain which links are returned, or is it silently ignored so the search is always global?

## KB Synthesis

The home-set criterion is **silently ignored**. The search is always global.

[EC-FIND-LINKS-GLOBAL] documents the mechanism directly: `sporglset2linkset()` contains the guard `if (TRUE||!homeset)`, which always evaluates true regardless of the caller's intent. The consequence is that whatever orgl-range argument is passed through by `findlinksfromtothreesp()` gets discarded and replaced with a hardcoded range of `{stream: 0, width: 100}` starting at tumbler zero — effectively unbounded for any real deployment.

[EC-HOMEDOCIDS-FILTER-BROKEN] confirms the observable consequence: passing a `homedocids` filter to `find_links` produces identical results to an unfiltered call. The filter is syntactically accepted without error but has no semantic effect.

The correct predicate for what the implementation actually delivers is:

```
find_links(from, to, three, homedocids) = {link ∈ all_links | endpoint_iaddrs(link) ∩ query_iaddrs ≠ ∅}
```

The `homedocids` parameter drops out entirely. The only dimension that actually filters results is the span dimension (I-address content matching). The orgl dimension — which was supposed to scope searches to specific documents — is permanently disabled by the `TRUE||` dead-code guard.

---

## Code Exploration

I now have everything needed for a precise answer. Here is the full analysis:

---

## EC-FIND-LINKS-GLOBAL: Does the Home-Set Criterion Constrain Link Results?

**Short answer: No. The home-set criterion is silently discarded at two independent points in the call chain, before it can constrain anything.**

---

### The Two Abandonment Points

#### Abandonment 1 — `fns.c:198`: NULL is passed explicitly

```c
// fns.c:196-199
if (
   getfindlinksfromtothree (taskptr, &fromvspecset, &tovspecset, &threevspecset, &homeset)
&& dofindlinksfromtothree (taskptr, fromvspecset, tovspecset, threevspecset, (typeispan*)NULL/*homeset*/, &linkset))
```

The protocol handler reads `homeset` off the wire via `getfindlinksfromtothree` into a local variable — then immediately throws it away. `dofindlinksfromtothree` receives `(typeispan*)NULL` with the comment `/*homeset*/` acknowledging that the actual value was not forwarded. This is not accidental omission: the comment records that the parameter exists but was suppressed.

#### Abandonment 2 — `sporgl.c:227`: `TRUE||!homeset` is an unconditional override

Even if a non-NULL `orglrange` somehow arrived — via a direct internal call, say — it would be destroyed here:

```c
// sporgl.c:222-237
int sporglset2linkset(typetask *taskptr, typecuc *spanfptr, typesporglset sporglset,
                      typelinkset *linksetptr, typeispan *homeset, INT spantype)
{
  typeispan nullhomeset;

    *linksetptr = NULL;
    if (TRUE||!homeset) {                        // always true — short-circuit evaluation
        tumblerclear (&nullhomeset.stream);
        tumblerclear (&nullhomeset.width);
        nullhomeset.width.mantissa[0] = 100;     // hardcoded synthetic range
        nullhomeset.next = NULL;
        homeset = &nullhomeset;                  // overwrites caller's pointer
    }
    for (; homeset; homeset = homeset->next) {
        sporglset2linksetinrange (taskptr, spanfptr, sporglset, linksetptr, homeset, spantype);
    }
}
```

`TRUE||!homeset` short-circuits: the right-hand side is never evaluated regardless of the value of `homeset`. The `if` body always executes, manufacturing a synthetic `nullhomeset` and rebinding the local `homeset` to it. Whatever the caller provided is unreachable from this point forward.

---

### What the Synthetic Range Actually Does

The `nullhomeset` is not a "match everything" range. It has:
- `stream` = all-zeros tumbler (i.e., orgl address 0)
- `width.mantissa[0]` = 100

This means the filter that reaches `sporglset2linksetinrange` is the range `[0, 100)` — the first 100 orgl positions. In `sporglset2linksetinrange`:

```c
// sporgl.c:256-262
if (orglrange) {
    prefixtumbler(&orglrange->stream, spantype, &range.stream);
    prefixtumbler (&orglrange->width, 0, &range.width);
    context = retrieverestricted (spanfptr, (typespan*)sporglset, SPANRANGE,
                                 &range, ORGLRANGE, (typeisa*)infoptr);
} else {
    context = retrieverestricted (spanfptr, (typespan*)sporglset, SPANRANGE,
                                 (typespan*)NULL, ORGLRANGE, (typeisa*)infoptr);
}
```

Because `nullhomeset` is never NULL, the `else` branch (a true all-orgl search) is unreachable. The `if` branch fires with the synthetic `[0,100)` range. In a development or test system with fewer than 100 documents this is functionally indistinguishable from global, but it is architecturally distinct — and wrong.

---

### The Downstream Function is Correctly Structured

`sporglset2linksetinrange` (the function that actually calls `retrieverestricted`) is well-designed: it checks `if (orglrange)` and would correctly apply a caller-supplied filter. But it is never given the chance to do so, because its only caller — `sporglset2linkset` — has already overwritten the parameter.

---

### Call Chain Summary

```
fns.c:189      findlinksfromtothree()
  fns.c:197      getfindlinksfromtothree(...)   → populates homeset from wire
  fns.c:198      dofindlinksfromtothree(..., NULL /*homeset*/, ...)
                                                  ↑ homeset discarded here
    do1.c:352      findlinksfromtothreesp(..., orglrangeptr=NULL, ...)
      spanf1.c:77    sporglset2linkset(..., orglrange=NULL, ...)
        sporgl.c:227   if (TRUE||!homeset)        ← unconditional
        sporgl.c:230   nullhomeset.width = 100    ← synthetic range fabricated
        sporgl.c:232   homeset = &nullhomeset     ← caller's value overwritten
        sporgl.c:235   sporglset2linksetinrange(..., homeset=&nullhomeset, ...)
          sporgl.c:256   if (orglrange)            ← always true (never NULL)
          sporgl.c:259   retrieverestricted(..., range=[0,100), ORGLRANGE, ...)
```

---

### Conclusion

The home-set criterion is **silently ignored**. It is abandoned once in the FEBE handler (`fns.c:198`, commented-out) and again inside `sporglset2linkset` (`sporgl.c:227`, unconditional `TRUE||`). Every link query uses the hardcoded synthetic range `[0, 100)` in orgl-space. In any realistic test environment this behaves as global, but the architectural promise — that the client can restrict link search to a home-set of documents — is completely unimplemented.
