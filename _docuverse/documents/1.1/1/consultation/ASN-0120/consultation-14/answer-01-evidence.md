## Question 1 [evidence]

> When CREATELINK's `vspanset2sporglset`/`permute` walks a source arrangement, does it require or assume the supplied V-span's depth matches the document's content V-position depth, and if a mismatched-depth span is supplied, what I-regions does it actually emit?

## KB Synthesis

## V-Span Depth in `vspanset2sporglset`/`permute`: Synthesis

The KB contains no evidence that this path enforces or assumes any depth/precision match on the supplied V-span. Here is what the KB does tell us about the mechanics and the implications.

---

### The Search Mechanism Is Purely Arithmetic

The V→I conversion chain is: V-span → `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` → `findcbcinarea2d` [SS-VSPAN-TO-SPORGL, ST-LINK-CREATE (Finding 0037)].

`findcbcinarea2d` classifies POOM crums against the query range using `whereoncrum` → `intervalcmp`, which implements the five-way tumbler total order: `TOMYLEFT / ONMYLEFTBORDER / THRUME / ONMYRIGHTBORDER / TOMYRIGHT` [SS-INTERVAL-CMP, SS-WHEREONCRUM]. This comparison is based entirely on numeric magnitude in the tumbler total order — it is indifferent to the exponent or digit count of the query range endpoints.

There is no depth-check gate anywhere in this path. `acceptablevsa()` always returns `TRUE` [PRE-SUBSPACE-CONVENTION (Finding 0010)], and `retrieverestricted` performs no structural validation on its input span.

---

### POOM Crum V-Addresses Have a Specific Precision

From [SS-POOM-BOTTOM-CRUM] (Finding 0076): V-origins in POOM bottom crums use 2-digit tumbler precision (exp=-1), e.g., `1.1`, `1.5`. Text content lives in the `1.x` range (exp=-1 magnitudes like 1.1–1.n), link orgls in the `2.x` range (exp=0 magnitudes like 2.1, 2.2) [SS-SUBSPACE-CONVENTION, SS-DUAL-ENFILADE].

---

### What a Mismatched-Depth Span Emits

The tumbler total order is continuous across exponents [INV-TUMBLER-TOTAL-ORDER (Finding 0031)]. Whether a crum at V-position `1.3` (exp=-1) is captured depends only on whether `1.3` falls numerically inside the query interval:

- A V-span `[1, 2)` (exp=0 boundaries) numerically contains `1.1`, `1.2`, ..., `1.9` in the total order (since `1 < 1.1 < 2`). **Result:** all text-subspace crums in that range are matched; their I-addresses are emitted as sporgls.
- A V-span `[1.01, 1.02)` (exp=-2 boundaries) is a narrow sub-band. **Result:** only crums in that precise band are matched; most text crums are missed.
- A V-span `[0.1, 0.9)` misses all text content at `1.x` since `1.1 > 0.9`. **Result:** no crums matched, empty sporglset.

The key constraint from [SS-TUMBLER] (Finding 0055) about `strongsub`'s exponent guard applies only to arithmetic subtraction (used in DELETE shifting), not to the comparison operations inside `retrieverestricted`. The range search is unaffected by exponent mismatch.

---

### One Structural Caveat: Link Crums at exp=0

Link orgl ISAs live at `2.x` V-positions (exp=0, magnitudes 2.1, 2.2, ...) [SS-LINK-SUBSPACE]. If the supplied V-span happens to numerically encompass these positions (e.g., a span starting at `0` with width `10`), `permute` will emit their I-addresses — which are link orgl ISAs, not permascroll addresses. The downstream `ispanset2vstuffset` would then dereference them as permascroll content, producing garbage. The KB documents this precise failure mode for operations like `compare_versions` and `retrieve_contents` that receive mixed I-address types [PRE-COMPARE-VERSIONS, PRE-RETRIEVE-CONTENTS, EC-RETRIEVE-VSPANSET-BOTH-SUBSPACES].

---

### Summary

The KB does not document any precondition on depth matching for this path. `vspanset2sporglset`/`permute` accepts any V-span and emits I-regions for every POOM crum whose V-position falls numerically within the query interval under the tumbler total order. A shallower span (e.g., integer-valued endpoints at exp=0) will capture a wider band of crums than intended; a deeper span (exp=-2 or finer) will capture a narrower band or nothing at all, depending on numeric overlap. The only consequence of depth mismatch the KB documents is the mixed-I-address-type problem when the query range straddles the text/link subspace boundary [SS-SUBSPACE-CONVENTION, EC-COMPARE-VERSIONS-LINK-CRASH] — the search mechanics themselves raise no error.

---

## Code Exploration

Now I have everything needed. Let me write the complete answer.

---

## Full Answer

### Call chain from CREATELINK to `permute`

`fns.c:100–112` (`createlink`) calls `getcreatelink`, which parses V-spans from the wire via `gettumbler` (`get2.c:71–97`). `gettumbler` reads dot-separated decimal digits up to `NPLACES=16` with no depth constraint — whatever depth the client supplies is accepted verbatim.

`docreatelink` at `do1.c:195–221` calls `specset2sporglset` (`sporgl.c:14`) for each of the three endpoint specsets. For any `VSPECID` item, `specset2sporglset` calls `vspanset2sporglset` (`sporgl.c:35`):

```c
// sporgl.c:44–48
if (!findorgl (taskptr, granf, docisa, &orgl, type)) return (NULL);
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);
```

`vspanset2ispanset` at `orglinks.c:397–402` calls `permute(taskptr, orgl, vspanset, V, ispansetptr, I)`.

`permute` (`orglinks.c:404–422`) iterates and calls `span2spanset` for each V-span. `span2spanset` (`orglinks.c:425–454`) calls:

```c
// orglinks.c:435
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex, (typespan*)NULL, targindex, (typeisa*)NULL);
```

With `span2ptr=NULL`, `retrieverestricted` (`retrie.c:56–85`) clears both `span2start` and `span2end` to zero and calls `retrieveinarea`, which dispatches to `findcbcinarea2d` since the orgl is a POOM (`retrie.c:94–98`).

`findcbcinarea2d` (`retrie.c:229–268`) walks the POOM tree, calling `crumqualifies2d` on each node. `crumqualifies2d` (`retrie.c:270–305`) filters using `whereoncrum` (`retrie.c:345–398`), which computes:

```c
// retrie.c:355–372 (POOM case)
tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
cmp = tumblercmp(address, &left);
...
tumbleradd (&left, &ptr->cwid.dsas[index], &right);
cmp = tumblercmp(address, &right);
```

Every comparison is via `tumblercmp` (`tumble.c:72–85`), which calls `abscmp` (`tumble.c:87–111`), comparing `exp` first then lexicographically scanning the full 16-place `mantissa` array. **There is no depth check anywhere in this path.**

---

### Where the implicit assumption lives

The assumption is in `context2span` at `context.c:176–212`, specifically the clipping logic:

```c
// context.c:191–203
if (tumblercmp (&grasp.dsas[idx1], &lowerbound) == LESS) {
    tumblerincrement (&grasp.dsas[idx2], 0,
        (INT) tumblerintdiff(&lowerbound, &grasp.dsas[idx1]),
        &grasp.dsas[idx2]);
}
if (tumblercmp (&reach.dsas[idx1], &upperbound) == GREATER) {
    tumblerincrement (&reach.dsas[idx2], 0,
        - tumblerintdiff (&reach.dsas[idx1], &upperbound),
        &reach.dsas[idx2]);
}
```

`tumblerintdiff` (`tumble.c:591–597`) subtracts two tumblers and returns `c.mantissa[0]` — the leading digit of the result after `tumblerjustify`. The subtraction goes through `strongsub` (`tumble.c:534–565`):

```c
// tumble.c:548–556
for (i = 0; aptr->mantissa[i] == bptr->mantissa[i]; ++i) {
    --answer.exp;
}
answer.mantissa[0] = aptr->mantissa[i] - bptr->mantissa[i];
for (j = 1; ...) answer.mantissa[j++] = aptr->mantissa[i++];
```

`strongsub` stops at the **first non-equal mantissa position** and subtracts only those digits. `tumblerintdiff` then extracts only `mantissa[0]` of the result. This means:
- `tumblerintdiff(1.8, 1.5.1)` = 3 (stops at mantissa[1]: 8–5=3)
- `tumblerintdiff(1.8, 1.5.3)` = 3 (same — the `.3` sub-position is invisible)

The sub-unit position within a deeper address is silently discarded.

---

### What I-regions are emitted for mismatched depth

Content inserted at depth-2 V-positions has POOM crums where:
- `cdsp.dsas[V]` is a depth-2 tumbler like `1.5` (`mantissa=[1,5,0,...]`)
- `cwid.dsas[V]` is `0.n` (`{exp=-1, mantissa=[n,...]}`) for `n` characters — established in `insertpm` at `orglinks.c:115–117` via `shift = tumblerlength(vsaptr) - 1 = 1` for depth-2 `vsaptr`

#### Shallower span (e.g., depth-1 `[1, 2)` against depth-2 content at `[1.5, 1.8)`)

`span1start = {mantissa=[1,0,...]}`, `span1end = {mantissa=[2,0,...]}`.

`crumqualifies2d`: `whereoncrum` with `address=2.0` vs `left=1.5`: mantissa[0] `2 > 1` → `TOMYRIGHT`. With `address=1.0` vs `left=1.5`: mantissa equal at [0], then mantissa[1] `0 < 5` → `TOMYLEFT`. Both conditions pass: crum qualifies.

`context2span`:
- `grasp.dsas[V]=1.5 > lowerbound=1.0` → NOT LESS → **no start clip**
- `reach.dsas[V]=1.8 < upperbound=2.0` → NOT GREATER → **no end clip**

**Result: the entire I-range of every qualifying crum is emitted.** A depth-1 span `[1, N)` returns the full I-range of all content at depth-2 V-positions `1.x`, without any intra-crum clipping. The fine-grained V-address of each character is ignored.

#### Deeper span (depth-3 `[1.5, 1.5.3)` against depth-2 content at `[1.5, 1.8)` with I-width 3)

`span1start = 1.5`, `span1end = 1.5.3` (`absadd` result: `{mantissa=[1,5,3,...], exp=0}`).

`crumqualifies2d`: `whereoncrum` with `address=1.5.3` vs `left=1.5`: mantissa[2] `3 > 0` → GREATER; vs `right=1.8`: mantissa[1] `5 < 8` → `THRUME`. `whereoncrum` with `address=1.5` vs `left=1.5`: EQUAL → `ONMYLEFTBORDER`. Both conditions pass: crum qualifies.

`context2span`:
- `grasp.dsas[V]=1.5`, `lowerbound=1.5` → EQUAL (not LESS) → no start clip
- `reach.dsas[V]=1.8`, `upperbound=1.5.3` → `tumblercmp(1.8, 1.5.3)`: mantissa[1] `8 > 5` → GREATER → clip end
- `tumblerintdiff(1.8, 1.5.3)`: `strongsub(1.8, 1.5.3)` first diverges at mantissa[1] (8−5=3), yields `{exp=-1, mantissa=[3,...]}`, returns `3`
- `tumblerincrement(&reach.dsas[I], 0, -3, &reach.dsas[I])` → **retreat I-end by 3**

Since I-width = 3, this equals the full range. **Zero-width I-span is emitted.** Crucially, `tumblerintdiff` would return `3` for any `upperbound` of the form `1.5.x` (x=0…9) — the sub-unit value `x` is invisible because `strongsub` stops at the mantissa[1] difference (8−5=3) regardless of mantissa[2].

For a span with both clips, e.g., depth-3 `[1.5.2, 1.5.5)` against the same crum:
- Start clip: `tumblerintdiff(1.5.2, 1.5)` → `strongsub` diverges at mantissa[2] (2−0=2), returns `2` → advance I-start to `s+2`
- End clip: `tumblerintdiff(1.8, 1.5.5)` → diverges at mantissa[1] (8−5=3), returns `3` → retreat I-end to `s+3−3 = s`
- `tumblersub(reach=s, grasp=s+2)` → negative result (sign=1): **logically invalid negative-width I-span**

---

### Downstream fate

**Zero-width spans** propagate via `onitemlist` (`orglinks.c:464`) into the ispanset, become zero-width sporgls, and hit either:
- `unpacksporgl` (`sporgl.c:195–198`): `qerror("zero width in unpacksporgl\n")`
- `insertpm` (`orglinks.c:121–126`): `gerror("crum width 0 in insertpm\n")`

**Negative-width spans** (sign=1 tumbler): `iszerotumbler` returns false (non-zero `mantissa[0]`), so the `iszerotumbler` guards are bypassed. `insertpm` stores a POOM crum with a negative V-width into the link document, silently corrupting the link's endpoint record. `tumblercmp` on a negative-sign tumbler treats it as LESS than all positive tumblers (`tumble.c:83`), so the crum occupies no coherent V-interval — subsequent `link2sporglset`/`dofollowlink` traversals will never retrieve it.

---

### Summary

There is **no depth check** in `vspanset2sporglset`/`permute` — neither at the POOM traversal stage (`crumqualifies2d`/`whereoncrum` use raw `tumblercmp`) nor at the clipping stage. The entire path from `gettumbler` to `insertpm` assumes without enforcement that the supplied V-span depth matches the depth at which content was inserted (depth 2 for normal document content).

With a shallower span, the code emits full I-ranges for all matching crums with no precision clipping. With a deeper span, the sub-unit position is silently discarded by `strongsub`/`tumblerintdiff`, producing either zero-width (end clip only) or negative-width (both clips) I-spans. The former triggers `qerror` in `unpacksporgl` or `insertpm`; the latter silently inserts a structurally invalid crum into the link document's POOM.
