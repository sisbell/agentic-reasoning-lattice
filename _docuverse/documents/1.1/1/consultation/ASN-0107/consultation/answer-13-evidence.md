## Question 13 [evidence]

> Since `sporglset2linkset` hardcodes the orgl range via the `TRUE||!homeset` override, does the count reflect a global I-address intersection rather than a count scoped to the supplied home document range?

## KB Synthesis

Yes — the count is global in the orgl dimension.

**Call chain:** `FINDNUMOFLINKSFROMTOTHREE` → `findnumoflinksfromtothreesp()` → `findlinksfromtothreesp()` → `sporglset2linkset()`.

At the `sporglset2linkset()` level, the `TRUE||!homeset` guard always fires, replacing whatever orgl range arrived from the caller with the hardcoded `{stream: 0, width: 100}` range [EC-FIND-LINKS-GLOBAL]. The supplied home document range is discarded before the spanfilade search begins.

`FINDNUMOFLINKSFROMTOTHREE` is then just a count of the resulting list [SS-FIND-LINKS / Finding 0035]: it materializes the full match set via `findlinksfromtothreesp()` and linearly walks it. Because the match set was computed against the global orgl range, the count reflects every link whose endpoint I-addresses intersect the query span — across all documents — not just those belonging to the supplied home document.

In short: the count is scoped only in the **span dimension** (I-address intersection) and is unscoped in the **orgl dimension**. Passing a home document orgl range has no effect on the result [PRE-FIND-LINKS / Finding 0069].

---

## Code Exploration

I now have everything I need. Here is the full analysis:

---

## `sporglset2linkset` — Orgl Range Override Analysis

### The Override

`sporgl.c:227`:
```c
if (TRUE||!homeset) {
    tumblerclear (&nullhomeset.stream);
    tumblerclear (&nullhomeset.width);
    nullhomeset.width.mantissa[0] = 100;
    nullhomeset.next = NULL;
    homeset = &nullhomeset;
}
```

`TRUE||!homeset` short-circuits unconditionally. The right-hand operand `!homeset` is never evaluated. Whatever the caller passes as `homeset` — including a real, non-NULL document range — is silently discarded and overwritten with `&nullhomeset`.

The replacement range is a stack-allocated `typeispan` with:
- `stream` = zero tumbler (the origin 0.0)
- `width.mantissa[0] = 100` (the width, first component = 100)

This is then passed as `orglrange` into `sporglset2linksetinrange` at `sporgl.c:235`.

---

### How the orglrange is Used in `sporglset2linksetinrange`

`sporgl.c:256–261`:
```c
if (orglrange) {
    prefixtumbler(&orglrange->stream, spantype, &range.stream);
    prefixtumbler(&orglrange->width, 0, &range.width);
    context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, (typeisa*)infoptr);
} else {
    context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, (typespan*)NULL, ORGLRANGE, (typeisa*)infoptr);
}
```

Because `orglrange` is never NULL after the override (it always points to `nullhomeset`), the `else` branch — which would do a fully unrestricted global search — is **never reached** either. The code always takes the constrained branch, using the synthetic `nullhomeset` as the ORGLRANGE argument to `retrieverestricted`.

So the actual ORGLRANGE constraint on every link spanfilade search is: all I-addresses from `[0.0, 100)` (origin=zero, width=100 in the first tumbler component).

---

### Is This a "Global" I-address Intersection?

**Not in the strict sense.** The override does not produce an unconstrained search (that would require passing `NULL` to `retrieverestricted`, triggering the `else` branch at `sporgl.c:261`). Instead it substitutes a fixed, hardcoded I-space window: origin 0, width 100. Whether this is functionally equivalent to global depends entirely on whether all document I-addresses in a given session fall within that window — which is plausible for small sessions but not guaranteed by the data model.

The more precise characterization: the result is a **fixed-window I-address intersection** covering `[0.0, 100)` in I-space, not a scope derived from the supplied home document, and not a fully unrestricted global search.

---

### The Count Path Specifically (`findnumoflinksfromtothree`)

There are two distinct callsites in `fns.c`, and their treatment of `homeset` diverges:

**Link listing** at `fns.c:198`:
```c
dofindlinksfromtothree(taskptr, fromvspecset, tovspecset, threevspecset,
    (typeispan*)NULL/*homeset*/, &linkset)
```
The `/*homeset*/` comment makes explicit that the homeset received from the protocol is thrown away *before it even enters `sporglset2linkset`*.

**Link counting** at `fns.c:213`:
```c
dofindnumoflinksfromtothree(taskptr, fromvspecset, tovspecset, threevspecset,
    homeset, &numberoflinks)
```
Here the homeset parsed from the protocol **is passed through** — all the way down the chain: `fns.c:213` → `do1.c:359` (`findnumoflinksfromtothreesp`) → `spanf1.c:77/85/93` (`sporglset2linkset`) — and then **discarded at `sporgl.c:227`** by the `TRUE||!homeset` override.

So the count variant correctly wires the homeset through the call stack but is then neutered at the final step. The resulting count does **not** reflect the supplied home document range; it reflects link endpoints whose ORGL dimension falls in `[0.0, 100)` in global I-space.

---

### Summary

| Question | Answer |
|---|---|
| Does `TRUE\|\|!homeset` override the caller's range? | **Yes, unconditionally** — `sporgl.c:227` always fires |
| What orgl range is actually used? | Hardcoded `nullhomeset`: stream=0, width=100 (`sporgl.c:228–232`) |
| Is the search globally unrestricted? | No — it is restricted to I-address window `[0.0, 100)`, not unbounded |
| Does the count reflect the supplied home document scope? | **No** — the homeset is discarded at `sporgl.c:227` even when non-NULL and correctly threaded through by the caller |
| Is the listing path any different? | The listing path (`fns.c:198`) discards homeset even earlier, before `dofindlinksfromtothree` is called |

The `TRUE||` is a classic in-development override — the code was wired to accept and thread a homeset parameter through the entire stack, but at the bottom that parameter was replaced with a hardcoded fallback, making the scoping parameter on all `findlinks*` and `findnumoflinks*` commands inert. The count does not reflect the home document range; it reflects what is visible within that fixed I-space window.
