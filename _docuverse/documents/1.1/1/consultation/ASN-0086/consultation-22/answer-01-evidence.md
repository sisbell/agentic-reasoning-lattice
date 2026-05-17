## Question 1 [evidence]

> Does udanax-green's link-emission path ever produce link addresses at element-field depth ≥ 3, or are all link addresses always at depth 2 (siblings within `A_{a₁}`)?

## KB Synthesis

## Link Address Depth: Always Depth 2, Never ≥ 3

The KB provides a clear answer: link addresses emitted by the system are **always at element-field depth 2** (one `.0.` separator below the document address), producing siblings within the `docAddr.0.2.N` namespace. No mechanism exists to produce addresses at depth ≥ 3.

### Evidence from the address structure

[SS-ADDRESS-SPACE] Finding 0065 defines the canonical structure:

```
account.0.document.0.element_field.element_number
```

For document `1.1.0.1.0.1`:
- First link: `1.1.0.1.0.1.0.2.1`
- Second link: `1.1.0.1.0.1.0.2.2`

The `.0.` before `2` is the one depth-crossing separator. The element number (`1`, `2`, …, `N`) is a **scalar integer story** — it grows monotonically without adding hierarchy.

### The allocation mechanism enforces sibling-only emission

[SS-ADDRESS-ALLOC] Finding 0065 specifies the code path (`findisatoinsertmolecule`):

1. `upperbound = tumblerincrement(docISA, 2, LINKATOM+1)` → bounds the search to `docAddr.0.3` (the text element field boundary).
2. First link: allocated at `docAddr.0.2.1`.
3. Every subsequent link: `lowerbound + 0.1` — incrementing the **last story** by 1.

The increment `+ 0.1` (adding 1 to the terminal story) never appends a new story level. An address like `docAddr.0.2.100` is the 100th link — still at the same depth, with element number 100 as a single multi-digit story value, not a deeper address `docAddr.0.2.0.something`.

### The upper bound enforces confinement

All link I-addresses must satisfy: `docAddr.0.2.1 ≤ addr < docAddr.0.3`.

An address at depth ≥ 3 relative to the element field (e.g., `docAddr.0.2.0.M`) would technically be numerically less than `docAddr.0.3` and within the search range — but `findpreviousisagr` only finds such an address if it was previously allocated there. Since the allocator only ever calls `tumblerincrement(lowerbound, 0, 1)` (rightshift=0, terminal increment), it cannot produce a deeper address.

### Invariant summary

| Property | Source |
|---|---|
| Links allocated via `makehint(DOCUMENT, ATOM, LINKATOM, …)` → depth 2 from doc | [SS-ADDRESS-ALLOC] Finding 0065, [SS-ADDRESS-SPACE] Finding 0065 |
| Allocation increments terminal story only (`+0.1`), never adds a story | [INV-MONOTONIC] Finding 0065 |
| All link addresses are siblings: `docAddr.0.2.1`, `.0.2.2`, …, `.0.2.N` | [SS-LINK-HOME-DOCUMENT] Finding 0025 |
| Upper bound `docAddr.0.3` prevents crossing into text element space | [SS-ADDRESS-SPACE] Finding 0065 |

The emission path is structurally incapable of producing depth ≥ 3 addresses because the increment operation is `lowerbound + 0.1` — a flat scalar growth — and the allocation is bounded to the `[docAddr.0.2.1, docAddr.0.3)` range. All link addresses remain siblings within `A_{a₁}`.

---

## Code Exploration

I now have all the evidence needed for a complete, code-cited answer.

---

## Answer: Link Endpoint Depth in udanax-green

**The link-emission path never produces link endpoint addresses at depth ≥ 3. All link endpoint VSAs within a link document are always exactly depth 2.**

---

### The Sole Source: `setlinkvsas`

Every link creation — two-endpoint (`domakelink`) or three-endpoint (`docreatelink`) — passes through `setlinkvsas` [do2.c:169–183]:

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
    tumblerclear (fromvsaptr);
    tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);   // mantissa[0] = 1
    tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);   // mantissa[1] = 1  → fromvsa = 1.1

    tumblerclear (tovsaptr);
    tumblerincrement (tovsaptr, 0, 2, tovsaptr);       // mantissa[0] = 2
    tumblerincrement (tovsaptr, 1, 1, tovsaptr);       // mantissa[1] = 1  → tovsa = 2.1

    if (threevsaptr) {
        tumblerclear (threevsaptr);
        tumblerincrement (threevsaptr, 0, 3, threevsaptr);   // mantissa[0] = 3
        tumblerincrement (threevsaptr, 1, 1, threevsaptr);   // mantissa[1] = 1  → threevsa = 3.1
    }
    return (TRUE);
}
```

`tumblerincrement` [tumble.c:599–623]: when called on a non-zero tumbler with `rightshift=1`, it finds the last non-zero mantissa index `idx` and writes `cptr->mantissa[idx + 1] += bint`. For the second call on each endpoint (starting from `mantissa[0]=N, exp=0`): `idx=0`, so `mantissa[0+1]=mantissa[1]=1`. This produces a two-component, depth-2 tumbler.

The hardcoded VSAs are:
- **from-endpoint**: `1.1` — mantissa = `[1, 1, 0, ...]`, exp = 0
- **to-endpoint**: `2.1` — mantissa = `[2, 1, 0, ...]`, exp = 0
- **three-endpoint**: `3.1` — mantissa = `[3, 1, 0, ...]`, exp = 0

All depth 2. No other values are ever assigned here.

`setlinkvsas` is called in exactly two places:
- `domakelink` [do1.c:189]: two-endpoint link
- `docreatelink` [do1.c:217]: three-endpoint link

There is no third call site, no override path, no conditional that produces alternative VSAs.

---

### Insertion Preserves Depth 2

The VSAs are passed to `insertpm` [orglinks.c:75–134] via `insertendsetsinorgl` [do2.c:130–149]:

```c
insertpm(taskptr, linkisaptr, link, fromvsa, fromsporglset)
insertpm(taskptr, linkisaptr, link, tovsa,   tosporglset)
insertpm(taskptr, linkisaptr, link, threevsa, threesporglset)
```

Inside `insertpm` [orglinks.c:113–131]:
```c
movetumbler(vsaptr, &crumorigin.dsas[V]);              // store vsaptr as V-origin
shift = tumblerlength(vsaptr) - 1;                     // shift = 2 - 1 = 1
inc   = tumblerintdiff(&lwidth, &zero);                // endpoint width as integer
tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V]);  // crum V-width at mantissa[1]
...
tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr);        // advance vsaptr for next span
```

For `fromvsa = 1.1`: `tumblerlength = nstories(1.1) - exp = 2 - 0 = 2`, so `shift = 1`. The V-width is placed at `mantissa[1]`, giving `crumwidth = 0.w` (depth 2).

The advance: `1.1 + 0.w = 1.(1+w)` — still depth 2. After `k` spans with width `w`: `fromvsa = 1.(1 + k·w)`. No matter how many spans are stored, the endpoint VSA within the link document stays at depth 2.

---

### Retrieval Also Confirms Depth 2

`link2sporglset` [sporgl.c:67–95] uses a depth-1 search range to retrieve endpoint spans:

```c
tumblerincrement(&zero, 0, whichend, &vspan.stream);  // stream = [whichend] — depth 1
tumblerincrement(&zero, 0/*1*/, 1, &vspan.width);     // width  = [1]        — depth 1
// ... retrieverestricted(orgl, &vspan, V, NULL, I, ...) — range [whichend, whichend+1)
```

The range `[whichend, whichend+1)` — e.g., `[1, 2)` for from-endpoints — captures all positions starting with first component `whichend`, **including** depth-3 positions like `1.1.something` if they existed. They don't, because the creation path never produces them.

In `sporglset2linksetinrange` [sporgl.c:239–269], the key retrieved from the spanfilade's ORGLRANGE is `prefixtumbler(linkisa, spantype)` = `spantype.linkisa`. The `beheadtumbler` [sporgl.c:264] strips the `spantype` prefix:

```c
beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
```

`beheadtumbler` [tumble.c:673–683] does `++exp` then zeros `mantissa[0]` if `exp` was 0, reducing the depth by 1. Result: `linksa = linkisa` — the link ISA, which is distinct from the link endpoint VSA and is always at depth `nstories(docISA) + 3`.

---

### Conclusion

**All link endpoint VSAs are hardcoded at depth 2 by `setlinkvsas` [do2.c:169–183] and remain at depth 2 through insertion.** The three field positions within every link document are:

| Endpoint | VSA | Depth |
|----------|-----|-------|
| from     | `1.1` (and advancing to `1.k`) | 2 |
| to       | `2.1` (and advancing to `2.k`) | 2 |
| three    | `3.1` (and advancing to `3.k`) | 2 |

There is no code path — no condition, no alternative function, no recursive structure — that produces a depth-3 link endpoint VSA. The `setlinkvsas` ceiling is the only place where these addresses are minted, and it is structurally incapable of producing a three-component result.

The three endpoint fields are not siblings within a single `A_{a₁}`: they occupy different first-level subspaces (`A_1`, `A_2`, `A_3`). Each sub-tree holds only one depth of content. Going deeper into any of them — to, say, `1.1.1` — would require a different `tumblerincrement` call with `rightshift=2` on the final advance, which never occurs.
