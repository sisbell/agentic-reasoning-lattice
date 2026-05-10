## Question 17 [gregory]

> After DELETE removes all text content from a document but leaves links in the `0.2.x` subspace untouched, what does `retrievevspansetpm` return — an empty specset, a specset containing only the link subspace spans, or a bounding span that incorrectly implies text content exists?

## KB Synthesis

After deleting all text (1.x subspace), `retrievevspansetpm` returns a specset containing **only the link subspace spans**, reported at their actual internal `2.x` positions — not the normalized `0.x` form that appears when text is also present.

The evidence for this is direct:

**[SS-DUAL-ENFILADE], Finding 0038** documents the exact behavior:
> `retrievedocvspanset` output (document has links only, no text):
> ```
> [{"start": "2.1", "width": "0.1"}]
> Links reported at actual internal position 2.x
> ```
> Contrast with the mixed case:
> ```
> [{"start": "0", "width": "0.1"}, {"start": "1", "width": "1"}]
> Links normalized from 2.x → 0.x when document also has text
> ```

**[SS-ADDRESS-SPACE], Finding 0024** confirms with a concrete scenario:
> After deleting all text from a document containing a link:
> ```
> vspanset: [{start: "2.1", width: "0.1"}]   # link still present
> retrieve_contents: [{"link_id": "1.1.0.1.0.1.0.2.1"}]
> ```

The mechanism: `retrievevspansetpm()` calls `is1story()` to detect multi-subspace content. When text is absent, the text extent is zero and the output path that normalizes link positions to `0.x` (via `maxtextwid()`) is bypassed. The link span is reported at its raw stored position `2.x`.

This rules out both alternative answers:
- Not an **empty specset** — the link subspace is unaffected by text deletion ([SS-THREE-LAYER-MODEL], [FC-SUBSPACE], Finding 0055)
- Not a **bounding span** — that's the behavior of `RETRIEVEDOCVSPAN` (opcode 14), not `retrievevspansetpm` ([SS-VSPAN-VS-VSPANSET], Finding 0035)

One practical implication: the same link appears as `"start": "0"` when the document has text and as `"start": "2.1"` when all text is deleted ([EC-VSPAN-NORMALIZATION]). Code that hardcodes the `0.x` address for a link will break after the document's text is fully deleted.

---

## Code Exploration

Now I have a complete picture. Here is the full analysis.

---

## What `retrievevspansetpm` Returns After All Text Is Deleted

### Setup: the two subspaces

**`istextcrum`** (`backend/orglinks.c:246–253`) identifies text crums as those whose V-displacement has `mantissa[1] == 0` (a simple, single-story address) and whose width is also single-story:

```c
bool istextcrum(typecorecrum *crumptr)
{
    if(crumptr->cdsp.dsas[V].mantissa[1] == 0  && is1story(&crumptr->cwid.dsas[V])){
        return TRUE;
    }
    return FALSE;
}
```

**`islinkcrum`** (`backend/orglinks.c:255–261`) identifies link crums as those at V-displacements of the form `1.n` (mantissa[0]==1, mantissa[1]!=0):

```c
bool islinkcrum(typecorecrum *crumptr)
{
    if(crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0){
        return TRUE;
    }
    return FALSE;
}
```

**`is1story`** (`backend/tumble.c:237–247`) returns TRUE only when all `mantissa[1..NPLACES-1]` are zero — i.e. the tumbler is a simple integer with no sub-digits:

```c
bool is1story(tumbler *tumblerptr)
{
    INT i;
    for (i = 1; i < NPLACES; i++)
        if (tumblerptr->mantissa[i] != 0)
            return (FALSE);
    return (TRUE);
}
```

### What DELETE does to the POOM

`dodeletevspan` (`backend/do1.c:158–167`) calls through to `deletevspanpm` → `deletend` (`backend/edit.c:31–76`). Inside `deletend`, every child crum in the deleted range gets classified by `deletecutsectionnd`:

```c
case 1:
    disown ((typecorecrum*)ptr);
    subtreefree ((typecorecrum*)ptr);   // edit.c:59–60
    break;
```

After the loop, `setwispupwards(father, 1)` propagates updated widths to the root, and `recombine(father)` restructures. When ALL text crums have been freed this way, only link crums (with their `1.n` V-addresses) remain as children of the root POOM crum. The root's `cwid.dsas[V]` is now recomputed to span only those link crums' extents.

### The branch decision in `retrievevspansetpm`

`retrievevspansetpm` (`backend/orglinks.c:173–221`) first checks:

```c
if (is1story (&ccptr->cwid.dsas[V])) { /* if it is just text return that */
```

With only link crums remaining, the root's `cwid.dsas[V]` must encode their positions, which have non-zero `mantissa[1]` (they are `1.n` addresses). Therefore `is1story` returns **FALSE**, and the function always enters the `else` branch — regardless of how much text content has been deleted.

### Inside the `else` branch: two spans are always produced

**Link span (lines 195–204):** Built directly from the root POOM's `cwid.dsas[V]` by zeroing `mantissa[1]` and justifying:

```c
linkvspan.itemid = VSPANID;
movetumbler (&ccptr->cwid.dsas[V], &linkvspan.stream);
linkvspan.stream.mantissa[1] = 0;
tumblerjustify(&linkvspan.stream);
movetumbler (&ccptr->cwid.dsas[V], &linkvspan.width);
linkvspan.width.mantissa[1] = 0;
tumblerjustify(&linkvspan.width);
```

This correctly extracts the link subspace portion of the total V-width. It is non-zero and reflects the actual links.

**Text span (lines 207–216):** `maxtextwid` is called with `&maxwid`:

```c
maxtextwid(taskptr, ccptr, &voffset, &maxwid);
vspan.itemid = VSPANID;
tumblerclear (&vspan.stream);
movetumbler (&maxwid, &vspan.width);
vspan.width.mantissa[0] = 0;
```

`maxwid` is declared at line 176 (`tumbler maxwid;`) but **never initialized** — only `voffset` receives a `tumblerclear` at line 182. Inside `maxtextwid` (`orglinks.c:224–244`), the root is not a text crum, so the function traverses its children:

```c
for(ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro (ptr)){
    if(ptr && !islinkcrum(ptr)){/* only look for text or overlapping stuff */
        maxtextwid(taskptr, ptr, &localvoffset, maxwidptr);
    }
}
```

All remaining children are link crums, so `islinkcrum(ptr)` is true for every one of them. The `maxwidptr` accumulator is **never written**. `maxwid` retains whatever uninitialized stack contents it had. Then `vspan.width.mantissa[0]` is forced to `0`, but `mantissa[1..NPLACES-1]` remain as garbage.

**Both spans are unconditionally added** (`orglinks.c:216–217`):

```c
putvspaninlist (taskptr, &vspan, vspansetptr);
putvspaninlist (taskptr, &linkvspan, vspansetptr);
return (TRUE);
```

### Answer

After DELETE removes all text content but leaves link crums in the `0.2.x` subspace, `retrievevspansetpm` returns **neither an empty specset, nor just the link subspace spans**. It returns:

> **A two-element specset: (1) a link span correctly representing the link subspace, plus (2) a broken text span derived from the uninitialized local variable `maxwid`.**

The decisive code path is:

| Step | Location | Effect |
|------|----------|--------|
| `is1story(ccptr->cwid.dsas[V])` → FALSE | `orglinks.c:184` | Link content's multi-level address forces `else` branch |
| `maxtextwid(...)` | `orglinks.c:207` | Traverses tree, skips all link crums, never writes `maxwid` |
| `maxwid` never initialized | `orglinks.c:176` | `vspan.width` is uninitialized stack data |
| `vspan.width.mantissa[0] = 0` | `orglinks.c:211` | Only the first mantissa slot is zeroed; others remain garbage |
| `putvspaninlist` × 2 | `orglinks.c:216–217` | Both the garbage text span and the valid link span are appended |

The third option — **a bounding span that incorrectly implies text content exists** — is the closest of the three offered answers: the text span has `stream=0` and a width with `mantissa[0]=0` but potentially non-zero garbage in `mantissa[1+]`, which, depending on stack contents, could encode a non-zero width and falsely imply text content at V-address 0. This is a defect in `retrievevspansetpm`: there is no guard or base case for the situation where `maxtextwid` finds nothing, and the accumulator tumbler is left uninitialized.
