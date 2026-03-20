## Question 18 [gregory]

> If a bottom crum's V-displacement is stored as a relative offset from its parent, how is the absolute V-position reconstructed during retrieval — does the traversal accumulate displacements additively down the tree path, and does the same accumulation apply independently to the I-dimension?

## KB Synthesis

Yes to both parts. The accumulation is additive down the tree path, and it applies independently to each dimension.

## Traversal Accumulation

During retrieval, the tree traversal maintains a running `offset` parameter that accumulates ancestral displacements. At each node, `prologuend` computes the node's absolute grasp as:

```
grasp = offset + ptr->cdsp   (retrie.c:334-339)
```

That computed grasp becomes the new `offset` passed to the node's children. This is precisely the invariant captured in [INV-ENFILADE-RELATIVE-ADDRESSING]:

```
absolute_grasp(node) = absolute_grasp(parent) + node.cdsp
absolute_grasp(root) = root.cdsp
```

`setwispnd` maintains this by absorbing the minimum child displacement into the parent after each modification [SS-ENFILADE-TREE Finding 0066]:

1. Find `mindsp = min(children.cdsp)` across all children
2. `root.cdsp += mindsp` (parent absorbs the new minimum)
3. Each child: `child.cdsp -= mindsp` (children become relative to the new root)

## Both Dimensions, Independently

The POOM `cdsp` field is a multi-dimensional structure: `cdsp.dsas[V]` (SPANRANGE) and `cdsp.dsas[I]` (ORGLRANGE). The same additive accumulation occurs for each dimension in the `dsas` array independently and simultaneously [SS-POOM-BOTTOM-CRUM Finding 0076].

A POOM bottom crum stores both:
- `origin.dsas[V]` — V-address (typically 2 tumbler digits, e.g., `0.5`)
- `origin.dsas[I]` — I-address (typically 6–9 tumbler digits, e.g., `0.0.0.0.0.0.0.0.11`)

Both are relative offsets from their ancestors in their respective address spaces. Retrieval accumulates both independently along the same path.

## GRAN vs POOM Asymmetry

This relative-addressing scheme is **specific to 2D enfilades** (POOM and SPAN). The 1D GRAN enfilade uses a different scheme: root displacement is always zero, and `setwidseq` sums widths without displacement tracking [SS-ENFILADE-TREE Finding 0066]. For GRAN retrieval, no offset accumulation is needed — positions are absolute.

The `isemptyenfilade` function reflects this: for POOM/SPAN it checks both `cdsp = 0` AND `cwid = 0`; for GRAN it checks only `cwid = 0` [EC-EMPTY-DOC Finding 0066].

---

## Code Exploration

---

## How Absolute V-Position Is Reconstructed During Retrieval

### Data Layout

`wisp.h` defines both `typedsp` and `typewid` as the same struct:

```c
struct structwid {
    tumbler dsas[MAXLOXIZE];   /* MAXLOXIZE = 2 */
};
typedef struct structwid typewid;
typedef typewid typedsp;
```

For POOM (the 2D enfilade that maps V↔I), `wisp.h:18-21` defines the indices:

```c
#define I  0
#define V  1
```

And `DSPSIZEPM = 2`, `WIDSIZEPM = 2`. Every crum stores `cdsp` (displacement) and `cwid` (width) covering **both** I and V slots.

The comment block at `wisp.h:29-43` makes the storage model explicit:

```
**                    wid             dsp
**   gr:  |           WIDTH           WIDTH
**   sp:  |         ORGLRANGE         ORGLRANGE
**        |           SPANRANGE         SPANRANGE
**   pm:  |             I                     I
**        |               V                     V
```

And a critical note for GRAN: _"Note that dsp's of gr are not stored on crums themselves, but are discovered thru tree walking"_. For POOM/SPAN, dsps **are** stored on each crum.

---

### The Retrieval Entry Point

`retrie.c:33-54` — `retrieve()` initialises the accumulator to zero and dispatches:

```c
typecontext *retrieve(typecuc *fullcrumptr, tumbler *address, INT index)
{
  typedsp offset;
        clear (&offset, sizeof(typedsp));       // both dsas[I] and dsas[V] zeroed
        switch (fullcrumptr->cenftype) {
          case GRAN:
                return (findcbcseq ((typecorecrum*)fullcrumptr, &offset, address));
          case SPAN:
          case POOM:
                return (findcbcnd ((typecorecrum*)fullcrumptr, &offset, address, index));
```

---

### POOM/SPAN: Additive Accumulation via `findcbcnd` + `prologuend`

`retrie.c:208-227` — `findcbcnd()`:

```c
typecontext *findcbcnd(typecorecrum *father, typewid *offsetptr, tumbler *address, INT index)
{
        if ((cmp = whereoncrum (father, offsetptr, address, index)) < ONMYLEFTBORDER || cmp > THRUME)
                return (NULL);

        if (father->height != 0) {
                prologuend (father, offsetptr, &grasp, (typedsp*)NULL);   // accumulate
                for (ptr = findleftson ((typecuc*)father); ptr; ptr = getrightbro (ptr))
                        if (retr = findcbcnd (ptr, &grasp, address, index))   // recurse with new base
                                break;
        } else { /* FOUND IT! */
                retr = makecontextfromcbc ((typecbc*)father, offsetptr);
        }
        return (retr);
}
```

At each interior node the accumulator advances by one step via `prologuend`.

`retrie.c:334-339` — `prologuend()`:

```c
int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach)
{
        dspadd (offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);   // grasp = offset + cdsp
        if (reach)
                dspadd (grasp, &ptr->cwid, reach, (INT)ptr->cenftype);
}
```

`wisp.c:15-18` — `dspadd()`:

```c
int dspadd(typedsp *a, typewisp *b, typedsp *c, INT enftype)
{
        lockadd (a->dsas, b->dsas, c->dsas, (unsigned)dspsize(enftype));
}
```

`wisp.c:269-273` — `lockadd()`:

```c
int lockadd(tumbler *lock1, tumbler *lock2, tumbler *lock3, unsigned loxize)
{
        while (loxize--)
                tumbleradd (lock1++, lock2++, lock3++);
}
```

For POOM, `dspsize(POOM) = DSPSIZEPM = 2` (`wisp.h:27`), so `lockadd` iterates **twice** — once for `dsas[I=0]`, once for `dsas[V=1]` — calling `tumbleradd` on each independently. Both I and V accumulators advance by exactly `crum->cdsp.dsas[I]` and `crum->cdsp.dsas[V]` at every level.

The `whereoncrum` check at `retrie.c:356-372` similarly reconstructs the absolute bound inline:

```c
case POOM:
    tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
    tumbleradd (&left, &ptr->cwid.dsas[index], &right);
```

`index` selects the dimension for the bounds test (V or I), but it is only a comparison — the underlying accumulation in `prologuend` always processes both.

---

### The Same Pattern in Area Retrieval

`retrie.c:252-265` — `findcbcinarea2d()` applies the identical accumulation for each qualifying interior node:

```c
if (crumptr->height != 0) {
        dspadd (offsetptr, &crumptr->cdsp, &localoffset, (INT)crumptr->cenftype);
        findcbcinarea2d (findleftson ((typecuc*)crumptr), &localoffset, ...);
} else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
```

---

### The Bottom Crum Adds Its Own `cdsp`

`context.c:151-174` — `makecontextfromcbc()` receives the *parent's* accumulated offset, then adds the leaf's own displacement:

```c
typecontext *makecontextfromcbc(typecbc *crumptr, typewid *offsetptr)
{
        ...
        movewisp(offsetptr, &context->totaloffset);          // copy parent accumulation
        movewisp(&crumptr->cwid, &context->contextwid);
        ...
        if (crumptr->cenftype != GRAN)
            dspadd(&context->totaloffset, &crumptr->cdsp,    // add leaf's own cdsp
                   &context->totaloffset, (INT)crumptr->cenftype);   // context.c:167
```

The `totaloffset` stored in the returned `typecontext` is therefore:

> **totaloffset = Σ(cdsp for every node on the root-to-leaf path)**

Both I and V slots accumulate via the same `dspadd` call — the leaf adds its own V-displacement in `dsas[V=1]` alongside its I-displacement in `dsas[I=0]`.

---

### GRAN Is Different

For granfilade (sequential text), no `cdsp` is stored on crums. `findcbcseq()` at `retrie.c:191-206` accumulates by summing sibling **widths** instead:

```c
for (; getrightbro (ptr); ptr = ptr->rightbro) {
        if (whereoncrum (ptr, offsetptr, address, WIDTH) <= THRUME)
                break;
        dspadd (offsetptr, &ptr->cwid, offsetptr, (INT)ptr->cenftype);  // add width, not cdsp
}
```

`dspsize(GRAN) = DSPSIZEGR = 1`, so only `dsas[WIDTH=0]` is touched. There is no V-dimension in GRAN.

---

### Summary

| Dimension | Mechanism | What accumulates |
|-----------|-----------|-----------------|
| POOM V (`dsas[1]`) | `prologuend → dspadd → lockadd` (loxize=2) | Each ancestor's `cdsp.dsas[V]` additively down root-to-leaf, then leaf's own `cdsp.dsas[V]` in `makecontextfromcbc` |
| POOM I (`dsas[0]`) | Same single `lockadd` call, first iteration | Each ancestor's `cdsp.dsas[I]` identically in parallel |
| GRAN WIDTH (`dsas[0]`) | `findcbcseq` sibling-width walk, loxize=1 | Sibling `cwid.dsas[WIDTH]` to the left; no stored `cdsp` |

**Both I and V are accumulated additively in lock-step by the same `lockadd` loop** — there is no separate pass for each dimension. The loop iterates `dspsize(POOM) = 2` times, hitting `dsas[0]` then `dsas[1]`, and each `tumbleradd` operates independently on its own tumbler. The final absolute V-position emerges in `context->totaloffset.dsas[V=1]` after all levels are visited.
