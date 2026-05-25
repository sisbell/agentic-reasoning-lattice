## Question 11 [evidence]

> When `retrieveendsets` resolves a link's three endsets, does it materialize all three (source, target, type) in a single spanfilade traversal or perform three separate `findlinksfromtothreesp`-style searches?

## KB Synthesis

`RETRIEVEENDSETS` performs **three separate spanfilade searches**, not a single unified traversal.

From [SS-RETRIEVE-ENDSETS] (Finding 0035), the call chain in `retrieveendsetsfromspanf()` (`spanf1.c:190-235`) proceeds:

1. **Once:** Convert the input specset to a sporglset (V-to-I translation) — this is the shared SPANRANGE restriction.
2. **Three times:** For each endset type, call `retrievesporglsetinrange()` independently, restricting the ORGLRANGE dimension to a different prefix constant:
   - `LINKFROMSPAN = 1` → source endset
   - `LINKTOSPAN = 2` → target endset
   - `LINKTHREESPAN = 3` → type endset

[INT-SPORGL-LINK-INDEX] confirms the mechanism: the three link endset types occupy separate ORGLRANGE subspaces in the spanfilade, so retrieval requires one query per subspace.

This is architecturally distinct from `FINDLINKSFROMTOTHREE`, which searches for link ISAs that intersect the query. `RETRIEVEENDSETS` instead searches for endpoint I-addresses that fall within the query region, resolving back to V-addresses in the querying document's context via `linksporglset2specset()`.

The V-to-I conversion is done once; the three endset searches are independent and serial. The type endset retrieval is noted as conditional — only fetched if requested.

---

## Code Exploration

I have a complete picture. Here is the full answer:

---

## `retrieveendsets` Traversal Analysis

**Answer: Three separate spanfilade traversals — one per endset type.** The link ISA's sporglset is computed once, but `retrievesporglsetinrange` is called three times independently, each triggering a full 2D enfilade search.

---

### Call Chain

```
fns.c:350   retrieveendsets(taskptr)
fns.c:357     doretrieveendsets(taskptr, specset, &fromset, &toset, &threeset)
do1.c:373       retrieveendsetsfromspanf(taskptr, specset, fromsetptr, tosetptr, threesetptr)
spanf1.c:190      [core logic — see below]
```

`doretrieveendsets` at `do1.c:369-374` is a pure pass-through to `retrieveendsetsfromspanf`. `getretrieveendsets` at `get1.c:185-188` (or `get1fe.c:192-195`) reads one `specset` from the wire and nothing else.

---

### Inside `retrieveendsetsfromspanf` (`spanf1.c:190-235`)

**Step 1 — Three search-space spans constructed once:**

```c
fromspace.stream.mantissa[0]  = LINKFROMSPAN;   // = 1   [xanadu.h:36]
fromspace.width.mantissa[0]   = 1;              // [spanf1.c:210-211]

tospace.stream.mantissa[0]    = LINKTOSPAN;     // = 2   [xanadu.h:37]
tospace.width.mantissa[0]     = 1;              // [spanf1.c:213-214]

threespace.stream.mantissa[0] = LINKTHREESPAN;  // = 3   [xanadu.h:38]
threespace.width.mantissa[0]  = 1;              // [spanf1.c:216-217]
```

These integer discriminators (1, 2, 3) are stored as tumbler values. Each describes a one-unit-wide range in the second (ORGLRANGE) dimension of the spanfilade.

**Step 2 — One `specset2sporglset` call** `[spanf1.c:222]`:

```c
specset2sporglset(taskptr, specset, &sporglset, NOBERTREQUIRED)
```

The input link ISA `specset` is converted to `sporglset` — its internal physical address — **once**, and the same `sporglset` is reused across all three retrieval calls.

**Step 3 — Three calls to `retrievesporglsetinrange` with that same `sporglset`:**

| Traversal | Line | Second-dim filter | Output |
|---|---|---|---|
| 1 — source/from | `spanf1.c:223-224` | `&fromspace` (LINKFROMSPAN=1) | `fromsporglset` → `*fromsetptr` |
| 2 — target/to | `spanf1.c:225-226` | `&tospace` (LINKTOSPAN=2) | `tosporglset` → `*tosetptr` |
| 3 — type | `spanf1.c:229-232` | `&threespace` (LINKTHREESPAN=3) | `threesporglset` → `*threesetptr` |

The from and to traversals are inside the same `if (!(... && ...))` guard (they must both succeed or the function returns `FALSE`). The type traversal is behind a separate `if (threesetptr)` null-check at `spanf1.c:229` — if the caller passes `NULL`, it is skipped entirely.

Via the FEBE protocol path at `fns.c:357`, `doretrieveendsets` is always called with `&threeset` (non-NULL), so in practice **all three traversals execute**.

---

### Inside `retrievesporglsetinrange` (`spanf1.c:237-267`)

For each of the three traversals, this function iterates over every entry in `sporglset` and calls `retrieverestricted` on the global `spanf` enfilade (defined at `corediskout.c:22`, declared `extern` at `xanadu.h:16`):

```c
for (; sporglptr; sporglptr = (typesporglset)sporglptr->xxxxsporgl.next) {
    context = retrieverestricted(
        (typecuc*)spanf,
        (typespan*)sporglptr, SPANRANGE,   // link's own physical address — dim 1
        whichspace,           ORGLRANGE,   // endset-type discriminator — dim 2
        (typeisa*)NULL
    );
    // [spanf1.c:245]
```

`retrieverestricted` at `retrie.c:56-85` computes tumbler bounds from both spans, then calls `retrieveinarea` at `retrie.c:87-110` → `findcbcinarea2d` — a full 2D range search through the spanfilade's internal POOM/SPAN enfilade nodes.

Each call to `retrievesporglsetinrange` is therefore an independent, complete traversal of the spanfilade restricted to:
- dimension 1: the exact span of the link's physical ISA address
- dimension 2: the one-unit range [LINKFROMSPAN,1], [LINKTOSPAN,1], or [LINKTHREESPAN,1]

---

### Why the Storage Layout Requires Three Traversals

When a link is written by `insertendsetsinspanf` at `do2.c:116-127`, each endset is inserted as a **separate** record in `spanf` via `insertspanf` with its own discriminator:

```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset,  LINKFROMSPAN)   // do2.c:119
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,    LINKTOSPAN)     // do2.c:120
insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN)  // do2.c:123
```

There is no single spanfilade record that contains all three endsets in one node. They are disjoint entries distinguished only by the integer type tag in dimension 2. Retrieval therefore requires three independent keyed lookups into the same enfilade structure.

---

### Contrast with `findlinksfromtothreesp`

`findlinksfromtothreesp` at `spanf1.c:56-103` is the **mirror operation**: given three endpoint specsets, find which link connects them. It also makes three spanfilade traversals — but it converts each **input endpoint** to a sporglset (three `specset2sporglset` calls at lines 71, 73, 75), queries each endset lane via `sporglset2linkset` → `sporglset2linksetinrange` → `retrieverestricted` (lines 77, 85, 93), and then **intersects** the three resulting link-ID sets (`intersectlinksets` at `spanf1.c:100`).

`retrieveendsets` is the inverse: one link ISA → three endpoint specsets. Both operations perform three separate spanfilade traversals. The only structural economy in `retrieveendsets` is that `specset2sporglset` runs once (versus three times in `findlinksfromtothreesp`), because there is only one input item rather than three.
