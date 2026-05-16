## Question 7 [evidence]

> What is the structural form of the root node in udanax-green's granfilade — single-component, multi-component, or otherwise — and is there a single canonical root or multiple?

## KB Synthesis

## Granfilade Root Node Structure

The granfilade has a **single canonical root** — the fullcrum — stored at a fixed on-disk location (`GRANFDISKLOCATION` in `enf.enf`). [SS-UNIFIED-STORAGE]

### Form of the root node

The root is a single `typecorecrum` node with `isapex=TRUE` and a `height` field. Its structural properties differ from the 2D enfilades (POOM, SPAN) in one critical way: **the GRAN root's `cdsp` displacement is always zero**. While POOM/SPAN roots track the minimum address across all content (making `cdsp` non-zero after the first insertion), GRAN uses `setwidseq` (width-summation) rather than `setwispnd` (min-tracking). Absolute addressing is thus implicit in the GRAN — children's displacements are absolute, not relative to a root minimum. [SS-ENFILADE-TREE, Finding 0066]

### Initial state

`createenf(GRAN)` produces:
- Height-1 fullcrum (`height=1, isapex=TRUE, numberofsons=1`)
- One bottom node (`height=0`, `infotype=GRANNULL`, zero width)

[SS-ENFILADE-TREE, Finding 0058]

### Growth

Height increases monotonically via `levelpush` (triggered by overflow at the fullcrum). `levelpull` — which would collapse the tree — is disabled and returns 0 immediately. So the root's height never decreases. [SS-ENFILADE-TREE, Finding 0058]

### Fan-out

The root follows GRAN branching rules:
- At height > 1: up to `MAXUCINLOAF = 6` children
- At height = 1: bottom crums hold exactly **one entry each** (`MAXBCINLOAF = 1`)

This makes the height-1 layer effectively a pass-through, and the granfilade is always at least one level taller than a comparable POOM for the same leaf count. [SS-GRAN-MB-ONE], [SS-ENFILADE-BRANCHING]

### Single vs. multiple roots

There is exactly **one** granfilade root. All document orgls, link orgls, permascroll content, and version addresses live in this single B-tree, with hierarchical structure enforced by address-range scoping during allocation rather than by separate trees. [SS-UNIFIED-STORAGE], [SS-ADDRESS-SPACE]

---

## Code Exploration

Now I have everything I need. Here is the complete answer, citing every claim to source.

---

## Root Node Structure of udanax-green's Granfilade

### TL;DR

The granfilade has a **single canonical root** — a single `typecuc` node marked `isapex=TRUE` — not multiple roots and not a multi-component compound root. It is **one-dimensional** (one wid/dsp slot, keyed by `WIDTH`). The root starts at `height=1` with one GRANNULL child, and grows taller in place as content is added.

---

### 1. The Root Type: `typecuc` with `isapex=TRUE`

The granfilade root is a `typecuc` (core upper crum). The `isapex` bit is the canonical root marker:

```c
// enf.h:176
#define isfullcrum(x) ((bool)((typecorecrum *)(x))->isapex)
```

The `typecuc` struct (`enf.h:54-82`) contains:
- `isapex BIT` — TRUE for the root, FALSE for all other nodes
- `height` — starts at 1, grows as the tree deepens
- `cenftype` — set to `GRAN` (=1, `enf.h:12`)
- `isleftmost BIT` — TRUE for root (it has no siblings)
- `leftbroorfather` — NULL for root (no parent)
- `leftson` — pointer to leftmost child in core
- `numberofsons` — count of immediate children
- `cwid` — cumulative wid (tumbler range covered by this subtree)
- `sonorigin` — disk pointer for paged-out children

The macro `weakfindfather` (`common.h:195`) confirms the root is parentless: when `isapex` is true, the fast-path returns NULL immediately, bypassing any pointer dereference.

---

### 2. Creation: Single Apex, One Initial Child

`createenf(GRAN)` in `credel.c:492-516` constructs the root:

```c
typecuc *createenf(INT enftype)
{
  typecuc *fullcrumptr;
  typecorecrum *ptr;

  fullcrumptr = (typecuc *) createcrum(1, enftype);  // height=1
  fullcrumptr->cenftype = enftype;
  fullcrumptr->isapex = TRUE;
  fullcrumptr->isleftmost = TRUE;
  adopt(ptr = createcrum(0, enftype), SON, (typecorecrum*)fullcrumptr);
  if (enftype == GRAN) {
      ((typecbc *)ptr)->cinfo.infotype = GRANNULL;
  }
  ivemodified(ptr);
  return (fullcrumptr);
}
```

The initial structure is:

```
fullcrum (typecuc, height=1, isapex=TRUE, cenftype=GRAN)
  └─ leftson (typecbc, height=0, infotype=GRANNULL)
```

The root has exactly **one child** at creation — a `typecbc` (core bottom crum) at height=0 with `infotype=GRANNULL` (`wisp.h:68`), a sentinel meaning "empty slot."

There is **no multi-component compound root**. The commented-out block immediately following (`credel.c:506-514`) shows a discarded alternative that would have called `levelpush` immediately and created a two-level structure for `GRAN`, but it was not used.

---

### 3. Single Canonical Root: the Global `granf`

There is exactly **one granfilade root**, held in the global variable:

```c
// xanadu.h:13-14
#define typegranf INT *   /* temp -- INT for alignment */
extern typegranf granf;

// corediskout.c:21
typegranf granf;
```

It is initialized once during startup in `entexit.c:41-46`:

```c
if (initenffile()) {
    initkluge ((typecuc**)&granf, (typecuc**)&spanf);  // load from disk
} else {
    granf = (typegranf) createenf (GRAN);              // create fresh
    spanf = (typespanf) createenf (SPAN);
}
```

All content in the entire system — every user's documents, every orgl, every piece of text — lives inside this single tree, keyed by tumbler address. The `typegranf INT *` typedef is explicitly marked temporary (`/* temp -- INT for alignment */`); the actual type used throughout is `typecuc *`.

---

### 4. One-Dimensional Width

The granfilade is **one-dimensional**, using a single wid/dsp slot:

```c
// wisp.h:12-13, 23-24
#define WIDTH   0
#define WIDSIZEGR  1
#define DSPSIZEGR  1
```

Every lookup passes `WIDTH` as the dimension index (e.g., `fetchorglgr` in `granf2.c:31,34`: `tumblercmp(&fullcrumptr->cwid.dsas[WIDTH], address)` and `retrievecrums(fullcrumptr, address, WIDTH)`). This contrasts with the spanfilade (2 dims: `ORGLRANGE`, `SPANRANGE`) and the POOM (2 dims: `I`, `V`).

---

### 5. Root Identity Is Stable; Height Grows In Place

The root node is **not replaced** as the tree grows. When a node overflows (`toomanysons` in `genf.c:239-245`), `levelpush` is called (`genf.c:263-294`):

```c
int levelpush(typecuc *fullcrumptr)
{
  typecuc *new;
  ...
  new = (typecuc *)createcrum((INT)fullcrumptr->height, (INT)fullcrumptr->cenftype);
  new->isleftmost = TRUE;
  transferloaf(fullcrumptr, new);               // move children to new internal node
  fullcrumptr->height++;                        // root height increments in place
  adopt((typecorecrum*)new, SON, (typecorecrum*)fullcrumptr);  // new node becomes root's son
  ...
}
```

The apex (`fullcrumptr`) keeps its identity — only its `height` field increments. The global `granf` pointer never changes after initialization.

---

### 6. Disk Persistence Confirms Single Root

`writeenfilades()` in `corediskout.c:69-88` writes the granfilade to a fixed disk location:

```c
temporgl.cinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = GRANFDISKLOCATION;
temporgl.cinfo.granstuff.orglstuff.orglptr = (typecuc *)granf;
((typecuc *)granf)->leftbroorfather = (typecorecrum *)&temporgl;
orglwrite (&temporgl);
```

There is one `GRANFDISKLOCATION` slot. The whole granfilade is a single tree written and read back at that address.

---

### Summary

| Property | Value |
|---|---|
| Root type | `typecuc` (core upper crum), `height` starts at 1 |
| Root marker | `isapex=TRUE` (`enf.h:32`), tested via `isfullcrum` (`enf.h:176`) |
| Number of roots | **One** — the global `granf` (`xanadu.h:14`, `corediskout.c:21`) |
| Initial children | One `typecbc` child with `infotype=GRANNULL` (`credel.c:501-504`) |
| Dimensions | **One** (`WIDTH=0`, `WIDSIZEGR=1`, `wisp.h:12,23`) |
| Root identity over time | Stable — height grows in place via `levelpush` (`genf.c:285`) |
| Disk location | Fixed `GRANFDISKLOCATION`, single slot (`corediskout.c:75`) |
