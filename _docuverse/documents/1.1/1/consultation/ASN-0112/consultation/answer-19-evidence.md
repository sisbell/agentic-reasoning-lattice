## Question 19 [evidence]

> Does the bounding span RETRIEVEDOCVSPAN returns for a link-bearing document have a width whose exponent reflects the link subspace's exp=0 magnitude rather than the text subspace's finer-grained exp, given the V-width/I-width exponent encoding difference?

## KB Synthesis

No. The bounding span width stays at exp=-1 (V-space precision), not exp=0.

[SS-INSERT-VWIDTH-ENCODING] documents the encoding rule: V-width exponent is `-(tumblerlength(vsaptr) - 1)`. For any V-address with tumblerlength=2 — whether text at `1.1` or a link orgl at `2.1` — shift=1 and the resulting V-width has exp=-1. The link subspace position `2.1` and the text subspace position `1.1` are both 2-digit tumblers, so both yield the same exponent for their associated widths.

[SS-POOM-BOTTOM-CRUM] confirms this symmetry concretely: both the V-origin and V-width of any bottom crum are encoded at V-space precision (2 digits, exp=-1), regardless of which subspace the crum occupies.

The POOM root's cwid is computed by `setwispnd` as max_reach minus min_grasp — two exp=-1 tumblers, yielding an exp=-1 result. For a mixed document, [EC-VSPAN-MISLEADING-SIZE] / [SS-VSPAN-VS-VSPANSET] show the bounding span is reported as e.g. `1.1 for 1.2`: the width `1.2` is a large exp=-1 value spanning from text subspace start to link subspace reach, not an exp=0 integer. The numeric magnitude grew (bridging the 1.x-to-2.x gap), but the exponent did not change.

The KB has no evidence that the bounding span computation introduces any exponent normalization; the V-width encoding is uniform across subspaces.

---

## Code Exploration

Now I have all the information needed. Let me compile the complete answer with full code citations.

---

## Answer

**Yes.** For a link-bearing document, RETRIEVEDOCVSPAN returns a V-width whose exponent is 0 — the link subspace's coarser magnitude — because `retrievevspanpm` returns the POOM root's `cwid.dsas[V]` raw, and for link-bearing documents that root width is a multi-story tumbler whose leading digit (mantissa[0]) is the link-space component encoded at exp=0.

Here is the full trace.

---

### 1. Call Path: `fns.c → do1.c → orglinks.c`

`fns.c:303-315` — `retrievedocvspan` dispatches to `doretrievedocvspan`:

```c
void retrievedocvspan(typetask *taskptr)
{
    ...
    if (   getretrievedocvspan (taskptr, &docisa)
        && doretrievedocvspan (taskptr, &docisa, &vspan))
            putretrievedocvspan (taskptr, &vspan);
```

`do1.c:312-320` — `doretrievedocvspan` finds the orgl and calls `retrievevspanpm`:

```c
bool doretrievedocvspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return findorgl (taskptr, granf, docisaptr, &docorgl, READBERT)
        && retrievevspanpm (taskptr, docorgl, vspanptr);
}
```

`orglinks.c:165-172` — `retrievevspanpm` copies the root crum's V-fields directly:

```c
bool retrievevspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
    return (TRUE);
}
```

No transformation. The returned width is `cwid.dsas[V]` of the POOM root, verbatim.

---

### 2. How the Root V-Width Is Built: `insertpm`

`orglinks.c:115-117` — When a crum is inserted into the POOM, its V-width is computed from the virtual address (`vsaptr`):

```c
shift = tumblerlength (vsaptr) - 1;
inc = tumblerintdiff (&lwidth, &zero);
tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);
```

`tumble.c:259-262` — `tumblerlength`:

```c
INT tumblerlength(tumbler *tumblerptr)
{
    return (nstories (tumblerptr) - tumblerptr->exp);
}
```

`tumble.c:599-607` — `tumblerincrement` on a zero tumbler sets `exp = -rightshift`:

```c
if (iszerotumbler (aptr)) {
    tumblerclear (cptr);
    cptr->exp = -rightshift;
    cptr->mantissa[0] = bint;
    return(0);
}
```

So the V-width exponent of each crum is `exp = -(tumblerlength(vsaptr) - 1)`.

Concrete examples:

| Content type | vsaptr example | nstories | exp (vsaptr) | shift | V-width exp |
|---|---|---|---|---|---|
| Text at 1.1.5 | [1,1,5] exp=0 | 3 | 0 | 2 | **-2** |
| Link at 2.1 | [2,1] exp=0 | 2 | 0 | 1 | **-1** |
| Link at 2 | [2] exp=0 | 1 | 0 | 0 | **0** |

Text crums get fine-grained V-widths (exp=-2 or more negative); link crums inserted at coarser addresses get exp=0 V-widths.

---

### 3. How V-Widths Combine: `absadd`

`tumble.c:444-485` — `absadd` picks the **greater (less negative, coarser)** exponent for the result:

```c
int absadd(tumbler *aptr, tumbler *bptr, tumbler *cptr)
{
    ...
    if (aptr->exp == bptr->exp) {
        answer.exp = aptr->exp;
        ...
    } else if (aptr->exp > bptr->exp) {
        answer.exp = aptr->exp;        // coarser exp wins
        ...
    } else {
        answer.exp = bptr->exp;        // coarser exp wins
        ...
    }
```

When a link V-width (exp=0) is combined with a text V-width (exp=-2), `absadd` sets the result exp to **0**. The finer text contribution is absorbed into trailing mantissa digits [1, 2, …], but the result exp is the link scale.

---

### 4. Confirmation: The Multi-Story Width Test

`orglinks.c:184` — `retrievevspansetpm` (the *correct* multi-span variant) distinguishes document types by checking `is1story` on the root V-width:

```c
if (is1story (&ccptr->cwid.dsas[V])) { /* if it is just text return that */
```

`tumble.c:237-247` — `is1story` returns TRUE only if mantissa[1..NPLACES-1] are all zero:

```c
bool is1story(tumbler *tumblerptr)
{
    for (i = 1; i < NPLACES; i++)
        if (tumblerptr->mantissa[i] != 0)
            return (FALSE);
    return (TRUE);
}
```

A text-only document's root V-width is 1-story (mantissa has only one non-zero digit, at position 0). A link-bearing document's root V-width is NOT 1-story — mantissa[1] is non-zero.

`orglinks.c:195-211` — When the root is multi-story, `retrievevspansetpm` decomposes it explicitly:

```c
/* link part: keep mantissa[0], zero mantissa[1] */
movetumbler (&ccptr->cwid.dsas[V], &linkvspan.width);
linkvspan.width.mantissa[1] = 0;
tumblerjustify(&linkvspan.width);

/* text part: zero mantissa[0], keep finer digits via maxtextwid */
maxtextwid(taskptr, ccptr, &voffset, &maxwid);
vspan.width.mantissa[0] = 0;
```

- `linkvspan.width` after zeroing mantissa[1] and justifying has exp=0: the **link subspace, coarse scale**.
- The text span comes from walking the crum tree with `maxtextwid`, not from the root V-width directly — because the root V-width's mantissa[1+] does not reliably encode the text extent.

---

### 5. The `islinkcrum` / `istextcrum` Encoding Pattern

`orglinks.c:246-260` — The subspace a crum belongs to is encoded in the displacement tumbler's mantissa:

```c
bool istextcrum(typecorecrum *crumptr)
{
    if(crumptr->cdsp.dsas[V].mantissa[1] == 0 && is1story(&crumptr->cwid.dsas[V]))
        return TRUE;
    return FALSE;
}

bool islinkcrum(typecorecrum *crumptr)
{
    /* if the whole crum is displaced into link space it is a link crum —
       this is true if the tumbler is a 1.n tumbler where n != 0 */
    if(crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0)
        return TRUE;
    return FALSE;
}
```

Text crums: displacement mantissa[1] == 0, width is 1-story (exp=0 fine).  
Link crums: displacement mantissa[1] != 0 (subspace starts at 1.n, i.e., address ≥ 2), width exp tracks the coarser link address.

---

### Summary

**RETRIEVEDOCVSPAN** calls `retrievevspanpm` (`orglinks.c:165`), which copies the POOM root's `cwid.dsas[V]` verbatim into the returned vspan. For a link-bearing document, that root V-width is a multi-story tumbler (mantissa[1] ≠ 0) with exp=0. The leading digit mantissa[0] carries the link-subspace count at the coarsest (exp=0) scale; text content is embedded in mantissa[1+] at finer scales.

**So yes**: the returned width's exponent is 0, reflecting the link subspace's magnitude. The text subspace's finer exp (e.g., -2) is not the dominant exponent — it is absorbed into trailing mantissa positions. A caller reading the returned width's `exp` field sees 0, not the text-level granularity.

**The correct separation** requires `RETRIEVEDOCVSPANSET` → `doretrievedocvspanset` (`do1.c:322`) → `retrievevspansetpm` (`orglinks.c:173`), which explicitly decomposes the root V-width by zeroing mantissa[0] vs. mantissa[1] and using `maxtextwid` to walk the crum tree for the actual text extent.
