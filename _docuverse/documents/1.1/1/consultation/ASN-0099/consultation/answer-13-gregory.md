## Question 13 [gregory]

> The `sporglset2linkset` function has `TRUE||!homeset` hardcoded, making link search always global — was there ever a working document-scoped mode, and is the hardcoded width of 100 in that path sufficient to cover all possible link I-address ranges, or can it silently truncate results?

## KB Synthesis

## `sporglset2linkset`: Document-Scoped Mode and Width-100 Sufficiency

### Was there ever a working document-scoped mode?

Almost certainly not in the surviving codebase — but one was clearly designed.

The guard `if (TRUE||!homeset)` is textbook debug-disabled code. The intended condition was `if (!homeset)`: supply the default wide range only when the caller provides no homeset. A caller providing a `homeset` (a specific document's ISA as an orgl-range specifier) was supposed to get document-scoped results. The `TRUE||` prefix collapses both branches into always-use-default, permanently defeating the scoping [EC-FIND-LINKS-GLOBAL].

`findlinksfromtothreesp()` in `spanf1.c:56-103` faithfully passes its `orglrange` argument to `sporglset2linkset`, and `dofindlinksfromtothree()` constructs that argument from the caller's `homedocids` parameter. The full plumbing exists; only the final dispatch inside `sporglset2linkset` is broken. The `homedocids` filter in `find_links` is accepted without error and silently ignored [EC-HOMEDOCIDS-FILTER-BROKEN], consistent with this being a latent, never-enabled feature rather than a regressed one.

### Is width 100 sufficient, or does it silently truncate?

It depends on deployment scale. The answer is **no truncation in practice for the test docuverse, but yes truncation is possible in larger deployments**.

The ORGLRANGE dimension stores link ISAs (structured as `node.0.user.0.doc.0.2.link_number`). The range is `[zero_tumbler, zero_tumbler + 100)` — where `100` here is a single mantissa position holding the integer one hundred, not three separate digits. From [SS-TUMBLER] (Finding 0031), each mantissa slot is an `INT`, not a decimal digit.

For a tumbler like `1.1.0.1.0.1.0.2.1`:
```
mantissa = [1, 1, 0, 1, 0, 1, 0, 2, 1, 0, ...]  (mantissa[0] = 1)
```
The tumbler total order compares mantissa lexicographically at the same exponent [INV-TUMBLER-TOTAL-ORDER]. At position 0: `1 < 100`, so this ISA is **inside** the range `[0, 100)`.

**What would fall outside?** Any ISA whose `mantissa[0] ≥ 100` — i.e., a node number of 100 or higher. In the udanax-green test environment (single node `1.x`, few users), `mantissa[0]` is always 1, so the range is adequate. In a docuverse with 100+ nodes, links allocated under those nodes would have `mantissa[0] ≥ 100` and be **silently invisible** to all `find_links` queries — no error, just empty or incomplete results.

The comment "effectively unbounded for any realistic deployment" [EC-FIND-LINKS-GLOBAL] reflects the assumption that the ORGL addressing space stays below 100 at its first digit. For the experiment-scale systems this code was built for, that was true. For a production multi-node docuverse, it is a latent scalability bug.

### Summary

| Question | Answer |
|----------|--------|
| Document-scoped mode ever worked? | No — plumbing exists, `TRUE||` disabled dispatch before it could function |
| Width 100 sufficient for test systems? | Yes — single-node ISAs have `mantissa[0]=1`, well within `[0,100)` |
| Width 100 sufficient at scale? | No — any node with ordinal ≥ 100 produces ISAs outside the range, silently dropped |

---

## Code Exploration

I now have everything needed. Here is the full analysis.

---

## Analysis: `sporglset2linkset` — Document-Scoped Mode and the Width-100 Constant

### 1. The Function: `sporgl.c:222–237`

```c
int sporglset2linkset(typetask *taskptr, typecuc *spanfptr, typesporglset sporglset,
                      typelinkset *linksetptr, typeispan *homeset, INT spantype)
{
  typeispan nullhomeset;

    *linksetptr = NULL;
    if (TRUE||!homeset) {                          // ← always TRUE
        tumblerclear (&nullhomeset.stream);
        tumblerclear (&nullhomeset.width);
        nullhomeset.width.mantissa[0] = 100;       // ← hardcoded limit
        nullhomeset.next = NULL;
        homeset = &nullhomeset;
    }
    for (; homeset; homeset = homeset->next) {
        sporglset2linksetinrange (taskptr, spanfptr, sporglset, linksetptr, homeset, spantype);
    }
}
```

### 2. Was Document-Scoped Mode Ever Working?

**Yes — and it was deliberately disabled, at two separate layers.**

#### Layer 1: `TRUE||!homeset` — `sporgl.c:227`

The condition `TRUE||!homeset` means the `!homeset` branch is **unreachable dead code**. This is not an accident; it's a deliberate short-circuit. If it had read just `!homeset`, the function would use caller-supplied homeset (document scope) when given, or fall back to the global nullhomeset when NULL. The `TRUE||` prefix kills that entirely.

The signature `typeispan *homeset` was designed to accept a caller-specified I-address range restricting which link orgl coordinates to search. That parameter is now always overridden.

#### Layer 2: `fns.c:198` — The FEBE Handler Explicitly Drops the Homeset

At the FEBE protocol boundary, even the parsed homeset from the client is discarded before it reaches the engine:

```c
// fns.c:197-199
   getfindlinksfromtothree (taskptr, &fromvspecset, &tovspecset, &threevspecset, &homeset)
&& dofindlinksfromtothree (taskptr, fromvspecset, tovspecset, threevspecset,
                           (typeispan*)NULL/*homeset*/, &linkset))
```

The comment `/*homeset*/` makes the intent explicit — the variable is parsed, then deliberately replaced with NULL. Note that the `findnumoflinksfromtothree` and `findnextnlinksfromtothree` handlers (`fns.c:213`, `fns.c:230`) do pass `homeset` through — but it is discarded anyway at `sporgl.c:227`.

#### Why Was It Disabled?

Multiple comment threads in the code tell the same story:

- `sporgl.c:251`: `if (FALSE/*trying to kluge links followable thru versions */&&...)`
- `spanf1.c:245`: `(typeisa*)NULL/*kluge to make links show thru to version &sporglptr->sporgladdress*/`
- `sporgl.c:134`: `movetumbler(homedoc/*&sporglset->sporgladdress*/, &specptr->docisa)`

The problem is **versioning**. When a new version of a document is created, it gets a new V-address and eventually a new I-address. If link search were restricted to a specific document I-address, links created against the old version would become invisible to queries on the new version — because the link endpoint's I-address points to the old version's orgl. Making the search unconditionally global is the workaround: you find all links across all versions.

So: document-scoped link lookup was an intended design feature, disabled sometime in the early-to-mid 1980s (the comments use 1984-era datestamps) when versioning made it semantically incorrect. It was never re-enabled.

---

### 3. The Width-100 Constant — `sporgl.c:230`

```c
nullhomeset.width.mantissa[0] = 100;
```

This sets the nullhomeset width tumbler to the value `100` (exp=0, mantissa[0]=100). In `sporglset2linksetinrange` it is passed through `prefixtumbler` twice:

```c
// sporgl.c:257-258
prefixtumbler(&orglrange->stream, spantype, &range.stream);   // → spantype.0
prefixtumbler(&orglrange->width, 0, &range.width);            // → 0.100
```

Tracing `prefixtumbler` (`tumble.c:641–651`) for the width case (aptr={exp=0, mantissa[0]=100}, bint=0):

1. `temp1 = {mantissa[0]=0}` → zero tumbler (bint=0)
2. `temp2 = {exp=0, mantissa[0]=100}`; since non-zero: `temp2.exp -= 1` → `exp=-1`
3. `tumbleradd(zero, {exp=-1, mant[0]=100})` → `{exp=-1, mant[0]=100}` = `0.100`

Adding start (`spantype`) + width (`0.100`) via `absadd` (`tumble.c:444`):
- start: `{exp=0, mant[0]=spantype}`
- width: `{exp=-1, mant[0]=100}`
- result: `{exp=0, mant=[spantype, 100, 0, ...]}` = `spantype.100`

**The ORGLRANGE query interval is `[spantype, spantype.100)`.** This covers all link I-addresses whose orgl key starts with `spantype.D` where `D < 100` (first digit of the link I-address).

#### Does It Truncate?

This depends on what I-addresses are actually generated for links.

When a link is inserted via `insertspanf` (`spanf1.c:22`):
```c
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```

If the link I-address is `A.B.C...`, the orgl key is `spantype.A.B.C...`. The search range `[spantype, spantype.100)` catches all links where `A < 100`.

In udanax-green's allocator, the root node has I-address `1`, accounts are created as `1.0.N` (N=1,2,...), and links/documents under an account are `1.0.N.0.M`. The **first digit `A` is always `1`** (everything descends from the root `1`). Since `1 < 100`, **the threshold is never reached under normal operation**.

#### When Could It Truncate?

Silently, if an I-address namespace were constructed with a first digit ≥ 100. For example, a link I-address `100.0.1.0.1` would produce orgl key `spantype.100.0.1.0.1`. Comparing this to the right boundary `spantype.100`:

```
mantissa: [spantype, 100, 0, 1, 0, 1, ...]  vs  [spantype, 100, 0, 0, ...]
                                   ↑                                ↑
                  mantissa[3]=1               mantissa[3]=0  → GREATER
```

`spantype.100.0.1.0.1 > spantype.100` → the enfilade node is TOMYRIGHT of the range → **silently missed, no error**.

This is a latent hazard, but one that does not trigger in the existing codebase because the Xanadu address allocator always produces addresses under root `1`. The 100 chosen is effectively arbitrary — there is nothing in the code that bounds the first digit of generated I-addresses to stay under 100; it just happens to always be 1.

---

### Summary

| Question | Answer |
|---|---|
| Was document-scoped mode ever working? | Almost certainly yes — it was deliberately disabled at two layers: `TRUE\|\|` in `sporgl.c:227` and `(typeispan*)NULL/*homeset*/` in `fns.c:198`, to avoid links becoming invisible across version boundaries |
| Why disabled? | Versioning: link endpoints reference old-version I-addresses; restricting search by document I-address would lose links after versioning. Global search is the workaround (`sporgl.c:251`, `spanf1.c:245`) |
| Can width=100 truncate? | Not in practice — all standard udanax-green I-addresses have first digit `1` (< 100). But if any I-address with first digit ≥ 100 existed, its links would be silently omitted with no error, no truncation warning, and no indication of missing results |
| Is the threshold tight? | No — there is 99× headroom versus any actual address generated by the allocator, but nothing enforces that the allocator stays below 100 |
