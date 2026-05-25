## Question 12 [evidence]

> Does `findnextlinkvsa` allocate link V-addresses in a way that would allow a "revised" link to be placed adjacent to its predecessor in the document's link subspace (`2.x`), or are they always strictly monotonic with no spatial relationship?

## KB Synthesis

## Link V-Address Allocation: Strictly Monotonic, No Spatial Relationship

`findnextlinkvsa` allocates link V-addresses in a strictly monotonic, append-only fashion with **no spatial relationship** to predecessors.

### The Mechanism

From [SS-LINK-SUBSPACE] (Finding 0052):
> The first link is placed at V-position `2.1`. Subsequent links are placed at `vspanreach` (the current end of the document extent). Link positions grow monotonically for sequential creation.

From [ST-CREATE-LINK] (Finding 0052):
> `findnextlinkvsa` always places the new link orgl at the current document end (`vspanreach`) or at `2.1` if no links exist yet. Since no POOM entries exist beyond the document end, there is nothing to shift. The "no shifting" behavior of CREATELINK is an emergent property of append-at-end placement, not a fundamental property of the operation.

### Sequential Allocation Pattern

Each new link regardless of its semantic relationship to prior links gets the next append position:

```
Link 1 created  → V-address 2.1
Link 2 created  → V-address 2.2   (vspanreach after link 1)
Link 3 created  → V-address 2.3   (vspanreach after link 2)
```

There is no "revised link" placement concept. CREATELINK has no awareness of prior link semantics — it only reads `vspanreach` and appends.

### Why Adjacency Cannot Be Forced Via Normal Operations

While `insertpm` (the underlying mechanism) technically supports mid-subspace insertion with shifting [ST-CREATE-LINK], `findnextlinkvsa` unconditionally selects `vspanreach`. A "revision" of link L at `2.3` would be allocated at `2.4`, `2.5`, etc. — sequentially after all existing links, with no spatial adjacency to `2.3`.

### V-Address vs. I-Address Distinction

Note that V-addresses (POOM positions) are not stable identifiers — they could in principle be shifted by a forced insertion before them [ST-CREATE-LINK]. The permanent identity of a link is its **I-address** (e.g., `docISA.0.2.N`), which is monotonically allocated per-document [SS-ADDRESS-SPACE, Finding 0065] and immutable [INV-IADDR-IMMUTABILITY]. Any "revision" relationship between links must be modeled at the application level, not the V-address level.

---

## Code Exploration

I have all the information I need. Here is the complete answer.

---

## `findnextlinkvsa`: Link V-Address Allocation Analysis

### The function

**`do2.c:151–167`** — the entire function is eleven lines:

```c
bool findnextlinkvsa(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr)
{
  tumbler vspanreach, firstlink;
  typevspan vspan;
  bool doretrievedocvspan();
    tumblerclear (&firstlink);
    tumblerincrement (&firstlink, 0, 2, &firstlink);
    tumblerincrement (&firstlink, 1, 1, &firstlink);

    (void) doretrievedocvspan (taskptr, docisaptr, &vspan);
    tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
    if (tumblercmp (&vspanreach, &firstlink) == LESS)
        movetumbler (&firstlink, vsaptr);
    else
        movetumbler (&vspanreach, vsaptr);
    return (TRUE);
}
```

### Step 1 — hardcoded floor: `firstlink = 2.1`

`tumblerclear` zeros the tumbler [common.h:71]. Then:

- `tumblerincrement(&firstlink, 0, 2, &firstlink)` [tumble.c:603–607]: because source is zero, takes the fast path → `exp = -0 = 0`, `mantissa[0] = 2`.  
- `tumblerincrement(&firstlink, 1, 1, &firstlink)` [tumble.c:611,621]: `idx` scans to the last nonzero place (mantissa[0]=2 → `idx=0`); adds `bint=1` at `mantissa[idx+rightshift] = mantissa[1]` → `mantissa[1] = 1`.

The `puttumbler` serialization [put.c:36–44] prints leading "0." for each negative `exp`, then `mantissa[0].mantissa[1]...`. With `exp=0, mantissa=[2,1,0,…]` this prints **`2.1`**.

`firstlink` is therefore the hardcoded minimum link address, the bottom of the `2.x` subspace.

### Step 2 — high-water mark: `vspanreach = vspan.stream + vspan.width`

`doretrievedocvspan` [do1.c:312–320] calls `findorgl` then `retrievevspanpm`. `retrievevspanpm` [orglinks.c:165–170] copies the document orgl's `cdsp.dsas[V]` (V-coordinate start) and `cwid.dsas[V]` (V-width) into the vspan struct. These track the total extent of the document in V-space — covering both text and any previously assigned link V-addresses.

`tumbleradd(&vspan.stream, &vspan.width, &vspanreach)` [do2.c:161] computes the address of the first *unoccupied* slot past the document's current V-span: `vspanreach = stream + width`.

### Step 3 — `max(2.1, vspanreach)`

```c
if (tumblercmp (&vspanreach, &firstlink) == LESS)
    movetumbler (&firstlink, vsaptr);      // doc has no link content yet → use 2.1
else
    movetumbler (&vspanreach, vsaptr);     // link content exists → append after it
```

The returned V-address is `max(2.1, vspanreach)`:

- **First link on a fresh document**: the document's V-span ends in the text subspace (e.g., something like `1.x`), which is less than `2.1`, so `firstlink = 2.1` is used.
- **Every subsequent link**: `vspanreach ≥ 2.1` (because the prior link already extended the V-span into `2.x`), so the new link starts exactly where the previous one ended.

### Does `acceptablevsa` impose any constraints?

No. `acceptablevsa` [do2.c:110–113] is a stub:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

No spatial guard is enforced.

### Allocation model: strictly monotonic, no revision ancestry

`findnextlinkvsa` is a pure **append-only, high-water-mark allocator**. Key properties:

| Property | Code evidence |
|---|---|
| All link addresses are ≥ 2.1 | `firstlink = 2.1` floor [do2.c:156–158,162–163] |
| Each new link address ≥ previous link address | `vspanreach = stream + width` always moves forward [do2.c:161] |
| Adjacent (no gaps between sequential links) | New link starts exactly at `vspanreach`, where prior content ended [do2.c:164–165] |
| No spatial relationship to any "predecessor" link | Algorithm has no predecessor argument; takes only `docisaptr` [do2.c:151] |

A "revised" link (one that semantically updates a prior link) receives exactly the same treatment as a brand-new link. `findnextlinkvsa` is called identically in both `domakelink` [do1.c:184] and `docreatelink` [do1.c:211] — neither passes any predecessor address, and neither routine computes one.

### Direct answer

**Links are strictly monotonic.** `findnextlinkvsa` always returns `max(2.1, vspan_end)`. It has no mechanism — and accepts no input — that would allow a revised link to be placed spatially adjacent to, or anywhere near, its predecessor. The link V-address encodes nothing but creation order within the document's `2.x` subspace. Sequential links are contiguous (no gaps), but that is a consequence of the high-water-mark algorithm, not a revision-ancestry signal. A revised link is placed at whatever the document's V-span high-water mark is at the moment of its creation, which reflects how many total link V-units have been allocated previously, not the address of the link it revises.
