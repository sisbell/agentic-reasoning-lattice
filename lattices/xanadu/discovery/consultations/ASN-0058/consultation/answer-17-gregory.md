## Question 17 [gregory]

> When `recombinend` merges POOM bottom crums during rebalancing, under what conditions can two adjacent crums with contiguous V-ranges but non-contiguous I-ranges be merged — or does the merge only redistribute crums between siblings without combining their V→I mappings?

## KB Synthesis

Rebalancing via `recombinend` operates exclusively at the **B-tree structural level** and never combines the V→I content of bottom crums. The two merge mechanisms [ST-REBALANCE-2D] both transfer crum nodes as atomic units:

- **Full merge** (`eatbrossubtreend`): transfers all children from one sibling node to another, then frees the donor. The children moved are entire subtrees — each bottom crum's `{origin.dsas[V], origin.dsas[I], width.dsas[V], width.dsas[I]}` quad remains exactly as created.
- **Nephew stealing** (`takenephewnd`): moves individual child crums between siblings via `takeovernephewsnd`. Again, each bottom crum moves as an atomic unit.

The merge guard `ishouldbother` [INV-ENFILADE-OCCUPANCY] checks only whether `dest->numberofsons + src->numberofsons <= max_children(height, type)`. It is purely a node-count predicate — it has no visibility into the V or I content of those nodes.

So two adjacent bottom crums with contiguous V-ranges but non-contiguous I-ranges can absolutely end up under the same parent after rebalancing, but they remain two separate crums. Their V→I mappings are never inspected or fused by any rebalance code path.

The only mechanism that actually combines V→I content into a single crum is `isanextensionnd` during INSERT [ST-INSERT, Finding 0062]. That check requires:

1. Same `homedoc` as the existing crum
2. New content's I-address origin equals the existing crum's I-reach (i.e., I-space contiguity)
3. The existing crum's V-reach equals the insertion point (i.e., V-space contiguity, the ONMYRIGHTBORDER case)

All three must hold simultaneously. Two crums with non-contiguous I-ranges fail condition 2 — `isanextensionnd` returns FALSE, and they are never fused regardless of how they are arranged in the B-tree by rebalancing.

The consequence [SS-POOM-BOTTOM-CRUM, INV-IADDR-PROVENANCE]: each bottom crum's I-address range reflects the provenance of the content at insertion time. Transcluded content from different source documents, or content inserted in non-contiguous I-address batches (e.g., after a CREATELINK [EC-GRAN-MB-ONE, Finding 0063 / INT-LINK-INSERT]), permanently occupies separate crums. Rebalancing can co-locate them under a common parent, but it cannot erase the I-space discontinuity between them.

---

## Code Exploration

I now have everything I need from the actual source. Here is the full answer:

---

## `recombinend`: POOM Crum Merging During Rebalancing

### Short Answer

**Two adjacent crums with contiguous V-ranges but non-contiguous I-ranges can be merged freely** — and vice versa. `recombinend` **never checks V→I range contiguity** as a precondition for merging. The only conditions that gate a merge are capacity and reservation status. What the merge operation actually does is **redistribute children (sub-crums) between siblings**, not combine the V→I mapping of two bottom crums into one.

---

### 1. Entry Point: `recombine` Dispatcher

`recombine.c:22-34` — both SPAN and POOM enfilades route through `recombinend`:

```c
case SPAN:
        recombinend (father);
        break;
case POOM:
        recombinend (father);
```

---

### 2. `recombinend` — The Rebalancing Loop

`recombine.c:104-131`:

```c
int recombinend(typecuc *father)
{
        if (father->height < 2  || !father->modified)   // [112]
                return(0);
        for (ptr = getleftson (father); ptr; ptr=(typecorecrum *)getrightbro (ptr)){
                recombinend (ptr);                       // [115] recurse down first
        }

        getorderedsons (father, sons);                   // [118] sort by diagonal
        n = father->numberofsons;
        for (i = 0; i < n-1; i++) {
                for (j = i+1; sons[i] && j < n; j++) {
                        if(i != j && sons[j] && ishouldbother(sons[i],sons[j])){  // [122]
                                takeovernephewsnd (&sons[i], &sons[j]);           // [123]
                        }
                }
        }
        if (father->isapex)
                levelpull (father);
}
```

**Key structural observation:** The function only acts on crums of `height >= 2`. Bottom crums (height 0) are never candidates for this merging loop — they are the *targets* of the children being redistributed. The comment in line 112 also gates on `modified`; an unmodified subtree is skipped entirely.

---

### 3. The Merge Gate: `ishouldbother`

`recombine.c:150-163` — this is the **complete and entire** decision function:

```c
bool ishouldbother(typecuc *dest, typecuc *src)
{
        ++noishouldbother;
        if(src->numberofsons == 0){
                if(src->sonorigin.diskblocknumber == DISKPTRNULL){
                        check(src);
                }else{
                        return(FALSE);   // [157] src is on disk only, skip
                }
        }
        if (dest->age == RESERVED || src->age == RESERVED)
                return (FALSE);          // [161] either crum is locked, skip
        return (dest->numberofsons + src->numberofsons <= (dest->height>1 ? MAXUCINLOAF : MAX2DBCINLOAF)
                && randomness(.3));      // [162]
}
```

The capacity constants (`enf.h:26-28`):
```c
#define MAXUCINLOAF      6   // max sons for interior crums
#define MAX2DBCINLOAF    4   // max sons for 2D bottom crums
```

**There is no V-range check. There is no I-range check. There is no `homedoc` check.** The sole structural condition is `numberofsons(dest) + numberofsons(src) <= capacity`.

The `randomness(.3)` call (`recombine.c:132-147`) is also permanently disabled — it unconditionally returns `TRUE`:

```c
bool randomness(float probability)
{
  static float i = 0;
  return(TRUE);    // [135] — actual logic commented out below
  /* i += probability; ... */
}
```

---

### 4. What Merging Actually Does: Children Are Redistributed, Not V→I Mappings Combined

The merge operations work at the **interior crum level**, moving child sub-crums from one parent into another. They never directly manipulate or combine the V→I mappings stored in bottom crums.

#### Full merge: `eatbrossubtreend` (`recombine.c:205-233`)

When `dest->numberofsons + src->numberofsons <= MAXUCINLOAF` (line 179), all of `bro`'s children are physically transplanted into `me`:

```c
makeroomonleftnd (me, &offset, &bro->cdsp, &grasp);  // [215] expand me's displacement envelope
fixdspsofbroschildren (me, bro);                      // [216] re-relativize bro's children's cdsp to me
getleftson(bro)->leftbroorfather = getrightmostbro(getleftson(me)); // [217] relink
getrightmostbro(getleftson(me))->rightbro = getleftson(bro);       // [218]
bro->leftson->isleftmost = FALSE;                                   // [219]

me->numberofsons += bro->numberofsons;  // [221]
...
disown (bro);
freecrum (bro);                         // [227-228] delete bro entirely
```

`fixdspsofbroschildren` (`recombine.c:259-268`) re-expresses each child's displacement relative to `me` rather than `bro`:

```c
for (nephew = getleftson (bro); nephew; nephew=(typecorecrum *)getrightbro(nephew)){
        dspadd (&bro->cdsp, &nephew->cdsp, &nephew->cdsp, me->cenftype);  // abs = bro + rel
        dspsub (&nephew->cdsp, &me->cdsp,  &nephew->cdsp, me->cenftype);  // new_rel = abs - me
}
```

This is purely a coordinate re-expression — the V and I widths (`cwid.dsas[V]`, `cwid.dsas[I]`) of the children are unchanged. The children retain their individual V→I mappings intact.

#### Partial merge: `takeovernephewsnd` (`recombine.c:165-203`)

When combined count exceeds `MAXUCINLOAF`, children are adopted one at a time until `me` is full:

```c
getorderedsons (bro, sons);          // [184] sort bro's children diagonally
n = bro->numberofsons;
for (i = 0; i < n && roomformoresons(me); i++) {
        ptr = sons[i];
        takenephewnd (me, ptr);      // [189] move one child at a time
}
```

`takenephewnd` (`recombine.c:235-257`) moves a single nephew, re-relativizing its displacement:

```c
dspadd (&bro->cdsp, &nephew->cdsp, &nephew->cdsp, bro->cenftype); // [243] abs coords
adopt (nephew, RIGHTMOSTSON, me);                                   // [244]
prologuend (nephew, &bro->cdsp, &nephewsgrasp, NULL);              // [245]
makeroomonleftnd (me, &offset, &nephew->cdsp, &grasp);             // [247]
dspsub (&nephew->cdsp, &me->cdsp, &nephew->cdsp, me->cenftype);    // [248] me-relative
```

Again: nephew's `cwid` (its own V and I spans) is never touched. Only its `cdsp` origin is re-expressed.

---

### 5. Ordering for Merge Attempts: Diagonal Sort

`recombine.c:270-279` — `getorderedsons` sorts children by the **sum of both displacement dimensions**:

```c
tumbleradd(&v[i]->cdsp.dsas[0], &v[i]->cdsp.dsas[1], &tarray[i]);  // [298] I + V
```

This places crums in a diagonal order across the 2D space. Notably:
- This is used to **select which pairs to try merging** and **which children to adopt first** in `takeovernephewsnd`
- It is **not a contiguity test** — two crums that are diagonally close may have no contiguous range in either I or V dimension
- The commented-out `break` statements (`recombine.c:124-125`) show a former design where only the first successful merge per pass was performed; now **all pairs are tried**

---

### 6. Contrast: Where Contiguity IS Checked

The only place range contiguity is enforced is during **insertion**, in `isanextensionnd` (`insertnd.c:301-309`):

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
        if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
                return (FALSE);       // [305] homedoc must match
        prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
        return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));  // [308]
}
```

This checks **both** dimensions (`dspsize` for POOM = 2): `reach[I] == origin[I]` **and** `reach[V] == origin[V]`. Only when both dimensions are contiguous AND the `homedoc` matches will a new insertion extend an existing bottom crum rather than create a new one.

`insertnd.c:249-258` uses this: if `isanextensionnd` returns true, it widens the existing crum (`dspadd` on `cwid`); otherwise it creates a fresh crum. So **bottom crums in a POOM accumulate only strictly contiguous V×I ranges during insertion**.

---

### 7. The Critical Distinction

| Phase | V-range contiguity check | I-range contiguity check | `homedoc` check |
|---|---|---|---|
| **Insertion** (`insertnd.c:301`) | Yes — both dims via `lockeq` | Yes — both dims via `lockeq` | Yes — `tumblereq` |
| **Rebalancing** (`recombine.c:150`) | **No** | **No** | **No** |

This means:

- During insertion, each bottom crum accumulates only a strictly contiguous V×I rectangular region, with a single `homedoc` (source document identity).
- During rebalancing, `recombinend` **does not examine the ranges of bottom crums at all**. It only looks at the `numberofsons` count of interior crums when deciding whether to merge.

**The merge never combines two bottom crums into one.** It moves interior crums (which contain bottom crums as their children) between sibling interior crums. The bottom crums themselves — and their V→I mappings — remain untouched and un-merged. A bottom crum with a non-contiguous I-range relative to its neighbor will never have those ranges fused; the rebalancing is blind to that structure.

### 8. Summary

`recombinend` merges during rebalancing under exactly these conditions (`recombine.c:160-162`):

1. Neither crum is `RESERVED`
2. Their combined `numberofsons` fits within `MAXUCINLOAF` (6) or `MAX2DBCINLOAF` (4) depending on height

That is all. **V-range contiguity, I-range contiguity, and `homedoc` identity are all invisible to `recombinend`.** What it redistributes are interior crum nodes; their children (bottom crums) carry V→I mappings that were locked in at insertion time and are never re-examined or combined during rebalancing. Two bottom crums with contiguous V-ranges but non-contiguous I-ranges will never be fused — not because `recombinend` rejects the merge, but because `recombinend` never operates on bottom crums directly at all.
