## Question 2 [evidence]

> Does udanax-green provide any operation that permutes link-subspace V-positions within a document's arrangement (analogous to rearrange for text), or does the implementation treat the link arrangement as append-only with fixed order?

## KB Synthesis

The KB gives a clear answer through three converging threads.

**Link V-positions are assigned append-only**

[SS-LINK-SUBSPACE] (Finding 0052) establishes that `findnextlinkvsa` places the first link at `2.1` and each subsequent link at `vspanreach` — the current document end. Links accumulate in creation order with no mechanism to reorder them. [SS-THREE-LAYER-MODEL] (Finding 0040) explicitly lists the only documented mutation of the link subspace: `DELETEVSPAN(2.x)` removes a POOM entry. Rearrangement is absent from that list.

**REARRANGE is mechanically capable but undesigned for the link subspace**

[ST-REARRANGE] (Finding 0056) shows `rearrangend()` applies `tumbleradd` to V-addresses without subspace guards — the same arithmetic works on 2.x addresses as on 1.x. [PRE-REARRANGE] (Finding 0051) confirms this concretely: a pivot with cross-subspace cuts moved text from 1.x into the 2.x range, demonstrating the backend imposes no subspace check. The inverse — applying cuts entirely within 2.x to permute link order — would succeed mechanically for the same reason.

However, no KB finding documents this as an intended use. The FEBE protocol has no REORDERLINK opcode. [FC-SUBSPACE] (Finding 0054) exists to protect 2.x from collateral shifting during 1.x insertions, not to enable 2.x self-rearrangement.

**What the KB does not cover**

The KB contains no finding testing REARRANGE with cuts entirely within `[2.1, 3.1)`. The behavior is extrapolatable from the mechanics (it would work, permuting link POOM entries) but is not empirically documented.

**Summary:** The link arrangement is append-only by design. DELETEVSPAN is the only documented mutation. REARRANGE could technically permute link V-positions — the backend has no guard — but no such operation exists in the FEBE protocol and no finding tests or describes it.

---

## Code Exploration

I now have all the evidence needed. Here is the complete answer.

---

## Does udanax-green provide a rearrange-equivalent for link-subspace V-positions?

**Short answer: No.** The implementation provides one rearrange primitive — generic at the C level but only ever invoked on the text subspace. Link V-positions in both the document POOM and within link POOMs are treated as fixed or append-only. No FEBE handler, `do*` function, or `*pm` wrapper specifically permutes link subspace positions.

---

### 1. The single rearrange call chain

The entire rearrange capability is a single linear chain with no branching for links:

```
fns.c:159  rearrange(taskptr)
  ↓
do1.c:40   dorearrange → findorgl(granf, docisa) → rearrangepm(docorgl, cutseq)
  ↓
orglinks.c:139  rearrangepm → rearrangend((typecuc*)docorgl, cutseqptr, V)
  ↓
edit.c:78   rearrangend(fullcrumptr, cutseqptr, INT index)
```

`rearrangend` is fully dimension-agnostic — it uses `index` everywhere:

```c
// edit.c:102-103
knives.dimension = index;
// ...
// edit.c:125
tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
```

It could in principle be called with link-subspace cuts. But `rearrangepm` is its **only call site** [orglinks.c:139], and it always passes `V` with the document-level POOM:

```c
// orglinks.c:137-142
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr)
{
    rearrangend((typecuc*)docorgl, cutseqptr, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

There is no `rearrangelinkspm`, no secondary `rearrangend` invocation, and no FEBE handler beyond `rearrange` [fns.c:159-173].

---

### 2. Link endpoint positions inside link POOMs are hardcoded constants

When `docreatelink` [do1.c:195] creates a link, `setlinkvsas` assigns fixed V-positions to the link's three endpoint slots within the **link's own POOM**:

```c
// do2.c:169-183
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
    tumblerclear (fromvsaptr);
    tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);  /* 1   */
    tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);  /* 1.1 */
    tumblerclear (tovsaptr);
    tumblerincrement (tovsaptr, 0, 2, tovsaptr);      /* 2   */
    tumblerincrement (tovsaptr, 1, 1, tovsaptr);      /* 2.1 */
    if (threevsaptr) {
        tumblerclear (threevsaptr);
        tumblerincrement (threevsaptr, 0, 3, threevsaptr);  /* 3   */
        tumblerincrement (threevsaptr, 1, 1, threevsaptr);  /* 3.1 */
    }
    return (TRUE);
}
```

Every link, every time: `from = 1.1`, `to = 2.1`, `three = 3.1` inside the link POOM. These are not derived from any document state; they are literals. Nothing in the codebase ever writes different values here or mutates them after creation.

---

### 3. Link references in document POOMs are placed by sequential append

When a link is created, its ISA is mapped into the containing document's V-space via `findnextlinkvsa` [do2.c:151]:

```c
// do2.c:151-167
bool findnextlinkvsa(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr)
{
  tumbler vspanreach, firstlink;
  typevspan vspan;
    tumblerclear (&firstlink);
    tumblerincrement (&firstlink, 0, 2, &firstlink);  /* link subspace starts at 2.0 */
    tumblerincrement (&firstlink, 1, 1, &firstlink);  /* first slot = 2.1 */

    (void) doretrievedocvspan (taskptr, docisaptr, &vspan);
    tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
    if (tumblercmp (&vspanreach, &firstlink) == LESS)
        movetumbler (&firstlink, vsaptr);  /* no links yet → place at 2.1 */
    else
        movetumbler (&vspanreach, vsaptr); /* append after existing end */
    return (TRUE);
}
```

The function reads the current document V-span reach, then places the new link reference immediately after it — pure sequential append. No insertion, no reordering, no gap-finding.

This is called unconditionally from `docreatelink` [do1.c:211]:

```c
// do1.c:208-213
return (
     createorglingranf (taskptr, granf, &hint, linkisaptr)
  && tumbler2spanset (taskptr, linkisaptr, &ispanset)
  && findnextlinkvsa (taskptr, docisaptr, &linkvsa)  /* always append */
  && docopy (taskptr, docisaptr, &linkvsa, ispanset)
  ...
```

---

### 4. The document V-space boundary that separates text from links

`findvsatoappend` [orglinks.c:29] — used when appending text — draws the boundary explicitly:

```c
// orglinks.c:36-47
tumblerclear (&linkspacevstart);
tumblerincrement (&linkspacevstart, 0, 2, &linkspacevstart);  /* linkspacevstart = 2.0 */
prologuend (ptr, &offset, &grasp, &reach);
if (
   iszerolock ((tumbler*)&ptr->cwid, widsize(POOM))
|| (tumblercmp (&grasp.dsas[V], &linkspacevstart) != LESS)) {
    tumblerincrement (vsaptr, 0, 1, vsaptr);  /* text starts at 1 */
    tumblerincrement (vsaptr, 1, 1, vsaptr);  /* → 1.1            */
```

Text occupies V < `2.0` (subspace `1.n`). Link references in the document occupy V ≥ `2.1`. The `islinkcrum` predicate [orglinks.c:255-261] distinguishes crums inside these two zones:

```c
bool islinkcrum(typecorecrum *crumptr)
{
    if(crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0){
        /* if the whold crum is displaced into link space it is a link crum
           this is true if the tumbler is a 1.n tumbler where n!= 0*/
        return TRUE;
    }
    return FALSE;
}
```

---

### 5. Why `rearrange` on the document POOM does NOT permute link endpoints

The document POOM contains link ISA references in the `2.n` subspace. The `rearrange` FEBE command operates on the full document POOM V-dimension. If a client sent `rearrange` with cuts placed in V ≥ `2.0`, `rearrangend` would shift those crums — it has no text-only guard. But:

- **This is not exposed as a feature.** There is no `rearrangelinks`, no named concept, no test that does this.
- **The link endpoint positions (1.1, 2.1, 3.1) inside the link's own POOM are untouched either way** — they live in a separate granf entry, and `rearrangepm` operates only on the containing document's POOM.
- **The FEBE `rearrange` handler exists for transclusion reordering** (moving text between V-positions in a document), as the surrounding `dorearrange`/`rearrangepm` context makes clear.

---

### Summary

| Concern | Finding | Source |
|---|---|---|
| `rearrangend` itself | Generic, dimension-agnostic | `edit.c:78,102,125` |
| Its only call site | `rearrangepm`, always with `V` and doc POOM | `orglinks.c:137-141` |
| Link endpoint V-positions in link POOM | Hardcoded constants `1.1 / 2.1 / 3.1` | `do2.c:169-183` |
| Link reference placement in doc POOM | Sequential append via `findnextlinkvsa` | `do2.c:151-167` |
| Dedicated "rearrange links" FEBE command | Does not exist | `fns.c` (entire file) |
| Dedicated `do*` or `*pm` for link rearrange | Does not exist | `do1.c`, `orglinks.c` |

**The link arrangement is append-only with fixed internal order.** There is no FEBE operation, `do*` function, or `*pm` wrapper that permutes V-positions in the link subspace. The design mirrors a log: new links extend the V-address space forward via `findnextlinkvsa`'s reach-append pattern, and endpoint slots within each link's own POOM are permanently assigned at the moment of creation.
