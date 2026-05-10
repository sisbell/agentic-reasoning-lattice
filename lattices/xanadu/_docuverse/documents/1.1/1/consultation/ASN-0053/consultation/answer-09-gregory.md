## Question 9 [gregory]

> When two spans are adjacent in tumbler space (the end of one equals the start of the next), under what conditions can they be merged into a single span, and when does the exponent difference between their width tumblers prevent merging?

## KB Synthesis

## Span Merging: Conditions and Exponent Constraints

### When Spans Can Be Merged

The POOM uses `isanextensionnd` as the merging gate [ST-INSERT, Finding 0062]. Two adjacent spans coalesce into one crum when **both** conditions hold:

1. **Same provenance** — the `homedoc` field on both sides matches (I-address origin document is identical)
2. **Exact boundary equality** — `reach(span1) == origin(span2)` as raw tumblers in both V and I dimensions, where `reach = tumbleradd(start, width)`

Sequential insertions within a single subspace naturally satisfy this. Each new character's origin equals the previous crum's reach, so typing "ABCDE" one character at a time still produces a single consolidated crum after the first-insert split [INV-VSPAN-CONSOLIDATION]. The `ONMYRIGHTBORDER` classification from `whereoncrum` [SS-WHEREONCRUM] bypasses knife-cutting entirely when the insertion point equals a crum's reach, routing directly to the extension check.

### When Exponent Difference Prevents Merging

**The fundamental constraint** comes from `strongsub` [SS-TUMBLER, Finding 0055]:

```
strongsub(a, b) : b.exp < a.exp  ==>  returns a unchanged
```

This is not just a DELETE artefact — it defines which tumbler pairs can participate in arithmetic. Specifically:

**Cross-subspace adjacency is arithmetically impossible.** Text-subspace V-addresses (1.x, exp = −1 per [SS-INSERT-VWIDTH-ENCODING]) produce widths at exp = −1. Link-subspace V-addresses (2.x, exp = 0) occupy a different exponent domain. When `tumbleradd(1.x_address, width_exp=-1)` is computed, the result stays within the exp = −1 domain — it can never produce a tumbler that `tumblereq`-equals `2.1` (exp = 0). The boundary at `2.1` is unreachable by addition from below using fractional widths.

This asymmetry is confirmed in two places:
- **INSERT isolation** [SS-TWO-BLADE-KNIFE, FC-SUBSPACE Finding 0054]: `findaddressofsecondcutforinsert` places `blade[1]` at `(N+1).1` — a deliberate structural guard ensuring shifts stay within the `N.x` subspace
- **DELETE isolation** [FC-SUBSPACE Finding 0055]: `strongsub(2.1, width_exp=-1)` returns `2.1` unchanged — an *incidental* arithmetic guard, not intentional design

**The practical consequence for merging:** A span ending at the top of the text subspace (reach approaching `2.0` in exp = −1 representation) and a span starting at `2.1` (exp = 0) can never satisfy `tumblereq(reach, origin)` — even if their numeric values were adjacent — because the exponent mismatch makes them distinct tumblers. The same applies to the 2.x/3.x boundary.

**Within a single subspace**, exponent consistency is maintained by [SS-INSERT-VWIDTH-ENCODING]: V-width exponent is computed as `-(tumblerlength(vsaptr) - 1)`, so all V-addresses of the same digit length get same-exponent widths. Sequential insertions at 1.x (all 2-digit V-addresses, exp = −1) produce widths all at exp = −1, making `tumbleradd(start, width)` produce reaches in the same exponent domain as subsequent origins — enabling exact tumbler equality and successful merging.

### Summary Table

| Scenario | Merge possible? | Reason |
|---|---|---|
| Sequential text insertions at 1.x | Yes | Same exponent domain; reach equals next origin exactly [ST-INSERT] |
| Sequential link insertions at 2.x | Yes | Same exponent domain [SS-LINK-SUBSPACE] |
| Text span (1.x) adjacent to link span (2.x) | No | Exponent gap; `strongsub` guard prevents cross-domain arithmetic [FC-SUBSPACE] |
| Different `homedoc` (e.g., two transclusions) | No | `isanextensionnd` homedoc check fails [ST-INSERT] |
| CREATELINK between two text insertions | No | Link orgl allocation advances I-address counter, breaking I-space contiguity [ST-CRUM-BOUND, Finding 0063] |

---

## Code Exploration

I now have a complete picture. Here is the full answer.

---

## Span Merging in Tumbler Space: When Exponent Differences Block the Merge

### The Two Merge Sites

There are exactly two active code paths that test whether two adjacent spans can be merged:

**1. `isanextensionnd` — merge at the enfilade level** (`insertnd.c:301–309`)

Called from `insertcbcnd` (`insertnd.c:242–275`) before creating a new bottom crum. If an existing crum's *reach* exactly equals the new insertion *origin*, the new span's width is simply added to the existing crum rather than creating a new crum:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    typedsp grasp, reach;
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

`lockeq` (`wisp.c:261–267`) calls `tumblereq` per dimension. `tumblereq` (`tumble.c:24–36`) requires **field-for-field exact match**: same `xvartumbler`, `varandnotfixed`, `sign`, `exp`, and all 16 mantissa bytes.

**2. `putvspaninlist` — merge at the vspan-list level** (`orglinks.c:329–387`)

Called when assembling the output list of V-spans from retrieved contexts. It tests adjacency using `tumblercmp`:

```c
tumbleradd (&spanptr->stream, &spanptr->width, &newspanend);  // line 343
tumbleradd (&ptr->stream, &ptr->width, &oldspanend);          // line 344
spancmp = tumblercmp (&spanptr->stream, &oldspanend);         // line 345
if (!spancmp) {
    tumbleradd (&ptr->width, &spanptr->width, &ptr->width);   // merge
    return(0);
}
// ... and symmetrically:
spancmp = tumblercmp (&ptr->stream, &newspanend);             // line 351
if (!spancmp) {
    movetumbler (&spanptr->stream, &ptr->stream);
    tumbleradd (&spanptr->width, &ptr->width, &ptr->width);   // merge
    return(0);
}
```

There is also `cleanupvspanlist` (`orglinks.c:297–312`) using `tumblereq`, but it is inside `#ifdef UnDEFined` and is dead code.

---

### The Gate: `abscmp` Refuses Equality Across Different Exponents

`tumblercmp` (`tumble.c:72–85`) dispatches to `abscmp` for positive tumblers. The first thing `abscmp` does:

```c
static INT abscmp(tumbler *aptr, tumbler *bptr)   // tumble.c:87
{
    if (aptr->exp != bptr->exp) {
        if (aptr->exp < bptr->exp) {
            return(LESS);      // tumble.c:93
        } else {
            return(GREATER);   // tumble.c:96
        }
    }
    // only if exps match: compare mantissa digit by digit
    ...
    return (EQUAL);
}
```

**If two tumblers have different `exp` fields, `abscmp` returns LESS or GREATER — never EQUAL — regardless of what the mantissa digits are.** This is the gating condition. Two spans are adjacent but unmergeable the moment their boundary tumblers carry different `exp` values.

---

### How `absadd` Determines the Endpoint's Exponent

The endpoint of a span is computed by `tumbleradd` → `functiontumbleradd` → `absadd` (`tumble.c:444–484`):

```c
if (aptr->exp == bptr->exp) {
    answer.exp = aptr->exp;                    // exps match: trivial
    ansmant[0] = amant[0] + bmant[0];
    i = j = 1;
} else if (aptr->exp > bptr->exp) {           // stream coarser than width
    answer.exp = aptr->exp;                    // endpoint takes stream's exp
    temp = aptr->exp - bptr->exp;
    while (i < temp) { ansmant[j++] = amant[i++]; }
    ansmant[j++] = amant[i++] + bmant[0];
    i = 1;
} else {                                       // width coarser than stream
    answer.exp = bptr->exp;                    // endpoint takes WIDTH's exp
    temp = bptr->exp - aptr->exp;
    while (i <= temp) { ansmant[j++] = bmant[i++]; }
}
while (j <= NPLACES - 1) { ansmant[j++] = bmant[i++]; }
```

The rule is simple: **`endpoint.exp = max(stream.exp, width.exp)`** (less negative wins, since `exp ≤ 0` always — enforced by `tumblercheck` at `tumble.c:174`).

Note also the asymmetry in case 3 (`b.exp > a.exp`): when the *width* is coarser than the *stream*, `absadd` copies only from `bptr` (the width), completely ignoring `aptr` (the stream). The endpoint equals the width itself. This is the lossy case and is rarely reached in normal document operations.

---

### How Width Exponents Are Created in `insertpm`

The V-dimension width for a POOM insertion is set in `orglinks.c:115–117`:

```c
shift = tumblerlength (vsaptr) - 1;
inc   = tumblerintdiff (&lwidth, &zero);
tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);
```

`tumblerlength` (`tumble.c:259–262`) = `nstories - exp`. For a simple integer vsaptr (exp=0, nstories=1): `shift = 0`, so `width.exp = 0`. For a two-story vsaptr like `1.2` (exp=0, nstories=2): `shift = 1`, so `width.exp = -1`.

Because vsaptr.exp = 0 and width.exp = -shift ≤ 0, we always have `stream.exp ≥ width.exp`, landing in case 1 or case 2 of `absadd`. The resulting endpoint has `endpoint.exp = stream.exp`. Sequential insertions through `insertpm` are self-consistent: each endpoint becomes the next stream, with the same exp.

---

### When the Exponent Difference Actually Blocks Merging

The dangerous case arises from **cutting operations**. `findaddressofsecondcutforinsert` (`insertnd.c:174–183`) creates a sub-address one level finer than the insertion position:

```c
int findaddressofsecondcutforinsert(tumbler *position, tumbler *secondcut)
{
    tumblerclear (&zero);
    tumblerincrement (position, -1, 1, secondcut);     // rightshift = -1 !
    beheadtumbler (position, &intpart);
    tumblerincrement(secondcut, 0, -tumblerintdiff(&intpart,&zero), secondcut);
    tumblerincrement (secondcut, 1, 1, secondcut);
}
```

The `tumblerincrement` with `rightshift = -1` produces `secondcut.exp = position.exp + 1` — a finer exponent. Called from `makegappm` (`insertnd.c:124–172`) every time the POOM must be split to make room for a new insertion. After a cut, crums within the split subtree carry cdsp/cwid tumblers at this finer resolution.

Scenario where two logically adjacent spans cannot merge:

1. Span A was inserted via `insertpm` at vsaptr `S` (exp=0) with width W (exp=0). Its endpoint in the POOM crum is at exp=0, mantissa=`[S[0]+W[0], ...]`.
2. An earlier deletion triggered `makegappm` / `findaddressofsecondcutforinsert`, creating a cut at a sub-address with `exp = -1`.
3. Span B's origin crum was placed at that sub-address, giving its stream `exp = -1`.
4. Endpoint of A has exp=0; stream of B has exp=−1. `abscmp` at `tumble.c:92–97` sees `0 ≠ -1` and returns GREATER — never EQUAL. Merge is blocked.

The same failure occurs in `isanextensionnd`'s `lockeq`/`tumblereq` check: the `exp` fields don't match, so the bit-level comparison fails at `tumble.c:31` (`if (a->exp != b->exp) return FALSE`), and no extension is granted.

---

### Summary

| Condition | Merge result |
|-----------|-------------|
| `stream1.exp == width1.exp == stream2.exp` | Merge succeeds (exps match, mantissas checked) |
| `stream1.exp > width1.exp` (normal POOM case) | `endpoint.exp = stream1.exp`; merge succeeds if `stream2.exp` matches |
| `width1.exp > stream1.exp` (rare) | `endpoint.exp = width1.exp`; stream is *ignored* by `absadd`; merge succeeds only if `stream2 == width1` |
| `endpoint.exp ≠ stream2.exp` (from cuts/splits) | **`abscmp` returns LESS or GREATER — never EQUAL — at `tumble.c:92–97`. Merge is unconditionally blocked.** |

The structural invariant is this: `abscmp` treats the `exp` field as the *magnitude class* of a tumbler. A tumbler with `exp = -1` lives in a strictly finer hierarchical stratum than one with `exp = 0`, and the two strata can never be equal by definition. This is semantically correct for Xanadu's hierarchical address space, but it means any operation that introduces crum addresses at a finer exp — principally the cut machinery in `findaddressofsecondcutforinsert` — creates span boundaries that are opaque to the adjacency test, preventing merging even when the spans are numerically contiguous.
