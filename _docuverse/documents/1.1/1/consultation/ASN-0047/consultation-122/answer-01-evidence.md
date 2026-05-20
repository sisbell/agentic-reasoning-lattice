## Question 1 [evidence]

> Does udanax-green permit interior link removal from a document's link arrangement, or does the implementation already enforce something like suffix-only contraction — and what mechanism (if any) realises link withdrawal?

## KB Synthesis

## Link Removal in udanax-green

### The mechanism: DELETEVSPAN on the 2.x subspace

Link withdrawal operates through `DELETEVSPAN` targeting V-positions in the link subspace (internally `2.x`). The only enforced precondition is a non-zero width — no guard exists to prevent deletion of link subspace entries [PRE-DELETE, Finding 0040]. The backend accepts link-subspace addresses identically to text-subspace addresses.

### What DELETEVSPAN actually changes

`DELETEVSPAN(2.x)` is a **POOM-only operation**. It removes the V→I mapping for the link orgl ISA from the document's enfilade via `deletend`, but leaves the other two layers untouched [SS-THREE-LAYER-MODEL]:

- **I-space** (link orgl): permanent, unaffected
- **Spanfilade** (DOCISPAN/endset entries): append-only, unaffected
- **POOM** (document V-stream): the 2.x entry is excised

The link remains fully followable via its ISA and discoverable via `find_links` through content-identity intersection — the POOM removal creates a "reverse orphan" [EC-REVERSE-ORPHAN], not a destroyed link.

### Interior removal is permitted — but positions do not compact

Links are allocated sequentially: first link at `2.1`, subsequent links at `vspanreach` [SS-LINK-SUBSPACE]. This gives a contiguous arrangement `2.1, 2.2, 2.3, …` in a freshly linked document.

Interior removal of, say, `2.2` is accepted without error. However, the critical interaction is the **exponent guard in `strongsub`** [FC-SUBSPACE, Finding 0055]:

> DELETE shifts crums after the deletion range via `tumblersub`. But the link displacements (e.g., `2.3`) are at tumbler exponent `exp=0`, while a deletion width of `0.1` is at `exp=-1`. Because `b.exp < a.exp`, `strongsub` returns the minuend unchanged — the surviving link at `2.3` stays at `2.3`.

This is the **accidental arithmetic guard** that Finding 0055 identifies as the incidental mechanism behind subspace isolation for DELETE (contrasted with INSERT's deliberate two-blade knife [SS-TWO-BLADE-KNIFE, FC-SUBSPACE Finding 0054]).

The consequence: interior deletion leaves a **positional gap** — the document's link arrangement becomes sparse (`2.1, 2.3`) rather than re-compacted to (`2.1, 2.2`). There is no suffix-only contraction enforced, and no compaction mechanism exists; positions simply persist or become absent.

### New link allocation after removal

`findnextlinkvsa` uses `vspanreach` (the current document extent end) for all subsequent link allocations [SS-LINK-SUBSPACE]. After interior deletion, new links still append beyond the highest surviving position — they do not fill gaps. The positional sparsity accumulates permanently.

### Summary

| Property | Value |
|----------|-------|
| Interior removal permitted? | Yes — no backend enforcement against it |
| Suffix-only enforcement? | No |
| Mechanism | `DELETEVSPAN` targeting V-address in `2.x` |
| Effect on link object | None — orgl and spanfilade persist (reverse orphan) |
| Effect on remaining link positions | No shift; exponent guard in `strongsub` prevents compaction |
| Effect on future allocation | New links still append at `vspanreach`, gaps are never filled |

---

## Code Exploration

I now have all the verified citations needed. Here is the complete answer.

---

## Interior Link Removal in udanax-green

### 1. No `DELETELINK` Exists in the FEBE Protocol

`requests.h` enumerates every FEBE operation. The complete link-related set is:

```
FOLLOWLINK          18   [requests.h:33]
CREATELINK          27   [requests.h:36]
RETRIEVEENDSETS     28   [requests.h:38]
FINDNUMOFLINKSFROMTOTHREE 29
FINDLINKSFROMTOTHREE      30
FINDNEXTNLINKSFROMTOTHREE 31
```

There is no `DELETELINK`. Link withdrawal is not a named operation in the protocol at all. A client cannot ask the backend to remove a link by identity.

---

### 2. Creation Enforces Strict Suffix Positioning

Every link creation goes through `docreatelink` (`do1.c:195–221`), which calls `findnextlinkvsa` to decide where to plant the new link reference in the document's V-tree:

```c
bool findnextlinkvsa(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr)
{
    tumbler vspanreach, firstlink;
    typevspan vspan;
    tumblerclear (&firstlink);
    tumblerincrement (&firstlink, 0, 2, &firstlink);  /* firstlink = 2.0 */
    tumblerincrement (&firstlink, 1, 1, &firstlink);  /* firstlink = 2.1 */

    (void) doretrievedocvspan (taskptr, docisaptr, &vspan);
    tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
    if (tumblercmp (&vspanreach, &firstlink) == LESS)
        movetumbler (&firstlink, vsaptr);   /* empty doc: start at 2.1 */
    else
        movetumbler (&vspanreach, vsaptr);  /* non-empty: append at reach */
    return (TRUE);
}
```
`do2.c:151–167`

The algorithm is: the next link lands at `max(2.1, current_vspan_reach)`. There is no insertion into an interior position. Links accumulate strictly at the suffix of the document's V-arrangement.

`setlinkvsas` (`do2.c:169–183`) then assigns the three endpoints positions 1.1, 2.1, 3.1 within the link's own address space — fixed ordinal slots within each link's private orgl, not within the document.

---

### 3. The Link Subspace Is Structurally Segregated From Text

`islinkcrum` in `orglinks.c:255–261` identifies link crums by their V-displacement:

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

`istextcrum` (`orglinks.c:246–253`) is the complement: `mantissa[1] == 0` with single-component width. Text and link crums live in disjoint tumbler ranges; `maxtextwid` (`orglinks.c:224–244`) explicitly skips link crums when computing the document's text reach. `retrievevspansetpm` (`orglinks.c:173–221`) returns them as two separate vspans. This segregation is structural, not a guard — it is used for width accounting, not for preventing deletion.

---

### 4. `DELETEVSPAN` Is the Only Mechanism That Can Reach Links — But It's Blind

`dodeletevspan` (`do1.c:158–167`) delegates entirely to `deletevspanpm`:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    typeorgl docorgl;
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
    );
}
```

`deletevspanpm` (`orglinks.c:145–152`):

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

The sole guard is a zero-width check. Then `deletend` (`edit.c:31–76`) is called with arbitrary `(origin, width)`. It accepts any range in any dimension. It cuts two knife planes, classifies each crum as fully inside (disown + free), fully outside (keep), or straddling (trim), and recombines:

```c
case 1:
    disown ((typecorecrum*)ptr);
    subtreefree ((typecorecrum*)ptr);
    break;
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    break;
```
`edit.c:58–65`

**Case 2 is the structural hazard.** Crums that survive to the right of the deleted range have their V-displacement decremented by `width`. This compresses V-space. Any link crums that were placed after a deleted region will shift — their positions in the document V-tree move — while their ISAs and spanfilade endpoint records remain unchanged, pointing to the old absolute addresses.

---

### 5. What This Means for Interior Link Removal

A client targeting a link by its V-position via `DELETEVSPAN`:

- **Mechanically works**: `deletend` has no link-awareness and will disown the targeted crum.
- **Leaves orphaned metadata**: the link's own orgl in the granfilade and its endpoint entries in the spanfilade (`LINKFROMSPAN`, `LINKTOSPAN`, `LINKTHREESPAN`) are not touched. Only the V-reference in the document tree is removed.
- **Corrupts subsequent links**: `case 2` in `deletend` shifts all surviving crums rightward of the deletion, displacing the V-positions of any subsequent link references. The granfilade/spanfilade records for those links still use the original addresses.
- **No guard prevents this**: neither `deletevspanpm` nor `deletend` calls `islinkcrum` or otherwise filters link-range deletion.

There is no explicit suffix-only *contraction* constraint. The enforcement is entirely on the creation side via `findnextlinkvsa`. Deletion is unconstrained by any link-awareness.

---

### Summary

| Dimension | Mechanism | Enforcement |
|---|---|---|
| Link creation | `findnextlinkvsa` — append at `max(2.1, vspan_reach)` | **Hard**: no insertion path exists |
| Link deletion | `DELETEVSPAN` → `deletend` — arbitrary range | **None**: no `DELETELINK`, no guard clause |
| Interior deletion effect | Shifts V-displacements of subsequent crums | **Destructive to subsequent links** |
| Protocol exposure | No `DELETELINK` in `requests.h` | **None exposed to client** |

The implementation realises a **write-once, append-only link arrangement** on the creation side: `findnextlinkvsa` structurally prevents interior insertion. On the removal side, there is no link withdrawal operation at all. `DELETEVSPAN` can mechanically excise any V-range including link positions, but it is semantically blind to links, leaves their metadata orphaned, and corrupts the V-addressing of any links placed after the deleted range. The absence of `DELETELINK` is not an architectural choice documented in the code — it is simply a gap: link withdrawal was never implemented as a first-class operation.
