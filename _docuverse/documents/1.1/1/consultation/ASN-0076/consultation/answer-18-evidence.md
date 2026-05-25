## Question 18 [evidence]

> If a link's POOM entry is removed via DELETEVSPAN on subspace `2.x` and a new link is then created at the same V-position, does the new link's `findnextlinkvsa` allocation account for the freed position or skip past the original's I-address?

## KB Synthesis

Two independent allocation mechanisms govern this, and they give different answers.

## V-position allocation: reused

`findnextlinkvsa` computes the next link placement using `vspanreach` — the current end of the document's link subspace extent [SS-LINK-SUBSPACE]. When `DELETEVSPAN(2.1)` removes the only link from the POOM, the link subspace becomes empty. `findnextlinkvsa` then falls into its "no links exist" path and initializes at `2.1` — the same V-position as the deleted entry [SS-LINK-SUBSPACE, ST-CREATE-LINK].

## I-address allocation: skips past the original

This is independent of the POOM. `DELETEVSPAN` removes only the POOM entry; it does not touch the granfilade [FC-GRANF-ON-DELETE, SS-THREE-LAYER-MODEL]. The original link orgl still exists at its I-address in the granf. When `MAKELINK` allocates the new link's I-address, `findpreviousisagr` queries the granfilade, finds the prior link orgl's I-address as the current maximum, and increments by `0.1` [SS-ADDRESS-ALLOC, Finding 0065]. The new link gets a fresh I-address, never the original's [INV-NO-IADDR-REUSE, INV-MONOTONIC].

## Summary

| Layer | After DELETEVSPAN | New link allocation |
|-------|------------------|-------------------|
| POOM (V-position) | `2.1` freed | Reuses `2.1` |
| Granfilade (I-address) | Original orgl persists | Allocates `original + 0.1` |

The new link ends up at the same V-position (`2.1`) but with a distinct, higher I-address — an exact illustration of [EC-REVERSE-ORPHAN] in reverse: the original link's I-space presence outlives its POOM tenure and permanently advances the allocation counter [INV-MONOTONIC, INV-NO-IADDR-REUSE].

---

## Code Exploration

I now have everything I need. Here is the complete answer.

---

## Link Allocation After DELETEVSPAN: V-Address vs I-Address

The answer splits cleanly along the POOM vs granfilade boundary. Deletion is POOM-only; the granfilade entry persists. The two allocation functions behave differently as a result.

---

### What DELETEVSPAN actually does

`dodeletevspan` [`do1.c:158-166`] opens the document's POOM orgl and calls:

```c
findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
```

`deletevspanpm` [`orglinks.c:145-152`] does nothing to the granfilade — it only touches the POOM:

```c
deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
logbertmodified(docisaptr, user);
```

`deletend` [`edit.c:31-76`] makes two cuts in V at `origin` and `origin+width`, then walks the POOM's children and for each child:

- **Case 1** (fully inside deleted range): `disown + subtreefree` — crum removed entirely [`edit.c:59-60`]
- **Case 2** (to the right of deleted range): `ptr->cdsp.dsas[V] -= width` — crum shifted left to close the gap [`edit.c:63`]

Then `setwispupwards(father, 1)` and `recombine(father)` propagate the change upward, decrementing every ancestor's `cwid.dsas[V]` by the deleted width — including the **root crum** of the POOM.

The granfilade entry for the deleted link's I-address is untouched. It remains in the granfilade.

---

### `findnextlinkvsa` — V-address allocation is a compacted high-water mark

[`do2.c:151-167`]:

```c
tumblerclear (&firstlink);
tumblerincrement (&firstlink, 0, 2, &firstlink);   // firstlink.mantissa = [2, 0, ...], exp=0
tumblerincrement (&firstlink, 1, 1, &firstlink);   // firstlink.mantissa = [2, 1, ...], exp=0 → "2.1"

(void) doretrievedocvspan (taskptr, docisaptr, &vspan);
tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
if (tumblercmp (&vspanreach, &firstlink) == LESS)
    movetumbler (&firstlink, vsaptr);
else
    movetumbler (&vspanreach, vsaptr);
```

`tumblerincrement(a, rightshift, bint)` [`tumble.c:599-623`] finds the last non-zero digit position `idx` in `a` and adds `bint` at `idx + rightshift`. For a zero tumbler, sets `exp = -rightshift, mantissa[0] = bint`. Two calls from zero produce `2.1` — the first position in link subspace 2.

`doretrievedocvspan` [`do1.c:312-319`] calls `retrievevspanpm` [`orglinks.c:165-172`]:

```c
movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
```

This reads the POOM **root crum's** raw `cdsp` (displacement) and `cwid` (width) in the V-dimension. After `deletend` + `setwispupwards`, the root's `cwid.dsas[V]` has **already been decremented** by the deleted link's V-width.

Therefore `vspanreach = root_cdsp + root_cwid` is the end of the **compacted** POOM — it has shrunk.

**Scenario: only one link existed at V=2.1, now deleted.**
- Root `cwid.dsas[V]` no longer spans into subspace 2.
- `vspanreach` falls into text space (< 2.1 = `firstlink`).
- The `LESS` branch fires: `vsaptr = firstlink = 2.1`.
- **The freed V-position 2.1 is returned directly.**

**Scenario: multiple links existed; a non-terminal one was deleted.**
- `deletend` case 2 shifts all rightward links' displacements left, closing the gap.
- The POOM is fully compacted; the new high-water mark equals the last remaining link's end.
- `findnextlinkvsa` returns that end — the same address the last link would occupy in the old numbering has been vacated by compaction.

In all cases, `findnextlinkvsa` **accounts for the freed V-position**. It never increments a monotonic counter; it reads the POOM's live root width after compaction.

---

### `createorglingranf` — I-address allocation skips past the original's I-address

[`granf1.c:49-55`] delegates to `createorglgr` [`granf2.c:111-128`], which calls `findisatoinsertgr` [`granf2.c:130-156`].

For `LINKATOM` atoms, `findisatoinsertgr` calls `findisatoinsertmolecule` [`granf2.c:158-181`]:

```c
tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);      // floor = docisa appended with ".0.2"
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
...
} else if (hintptr->atomtype == LINKATOM) {
    tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);
    if (tumblercmp (&lowerbound, isaptr) == LESS)
        tumblerincrement (isaptr, 1, 1, isaptr);          // no links yet: first slot
    else
        tumblerincrement (&lowerbound , 0, 1, isaptr);    // past last existing link
}
```

`findpreviousisagr` [`granf2.c:255-278`] walks the granfilade tree to find the **last existing I-address** below `upperbound = docisa.0.3`.

Because `deletevspanpm` does not remove the original link's granfilade crum, that crum is still present and found by `findpreviousisagr`. It becomes `lowerbound`. The `else` branch fires:

```c
tumblerincrement (&lowerbound , 0, 1, isaptr);
```

From `tumblerincrement` [`tumble.c:599-623`]: finds the last non-zero digit `idx` of `lowerbound`, adds 1 at `idx + 0 = idx`. This produces a new I-address that is `lowerbound + 1` at its most significant varying digit — strictly **greater than** the original link's I-address.

**The new link's I-address skips past the original's I-address.** The granfilade is append-only with respect to existing entries; freed V-space in the POOM does not free I-address space in the granfilade.

---

### Summary

| Dimension | Allocation Function | Behavior after DELETEVSPAN |
|---|---|---|
| **V-address** | `findnextlinkvsa` [`do2.c:151`] | Reads compacted POOM root `cwid` via `retrievevspanpm` [`orglinks.c:165`]; returns the shrunken high-water mark — **the freed V-position is reused** |
| **I-address** | `createorglingranf` → `findisatoinsertmolecule` [`granf2.c:158`] | Reads granfilade for last existing I-address; the deleted link's granfilade entry persists because `deletevspanpm` [`orglinks.c:145`] only touches the POOM — **the new I-address is strictly past the original's** |

The asymmetry is structural: `DELETEVSPAN` is a POOM operation. It compacts V-space (enabling V-address reuse) but leaves the granfilade intact (preventing I-address reuse). The V→I mapping vanishes; the I-address slot accumulates as a permanent record in the granfilade.
