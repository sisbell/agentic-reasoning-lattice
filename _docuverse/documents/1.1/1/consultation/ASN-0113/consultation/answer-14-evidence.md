## Question 14 [evidence]

> Does `retrievevspansetpm` derive each subspace's extent from the POOM root displacement and width (`setwispnd`), or does it traverse to the bottom crums and accumulate per-entry widths?

## KB Synthesis

`retrievevspansetpm` uses **`maxtextwid()`** — described as "recursive text-extent traversal" — not the root displacement/width directly.

Here's why the distinction matters:

The root `cdsp.dsas[V]` and `cwid.dsas[V]` maintained by `setwispnd` represent a **bounding box** across all subspaces. For a document with links at `2.x` and text at `1.x`, the root displacement tracks the minimum address (somewhere in the link subspace) and the root width spans from there to the far end of the text subspace. This is exactly the inflated, semantically meaningless value that `retrievedocvspan` (via `retrievevspanpm`) returns — confirmed as a bug in [SS-VSPAN-VS-VSPANSET] / [EC-VSPAN-MISLEADING-SIZE].

`retrievevspansetpm` takes a different path [SS-VSPAN-VS-VSPANSET Finding 0035]:
1. Calls `is1story()` (`tumble.c:237-247`) to test whether the root width spans multiple subspaces
2. If multi-subspace, calls `maxtextwid()` (`orglinks.c:224-245`) — **recursive tree traversal** — to compute the actual text extent independently from the root bounding box
3. Constructs the link span by zeroing `mantissa[1]` (normalization to `0.x` in output) [SS-DUAL-ENFILADE Finding 0038]

The contrast is explicit in [SS-DUAL-ENFILADE Finding 0043]: `retrievedocumentpartofvspanpm` reads `cdsp.dsas[V]` directly (root fields, `setwispnd`-maintained), while `retrievevspansetpm` uses the `is1story`/`maxtextwid` path. That's also why `CREATENEWVERSION` only copies the text subspace — it calls `doretrievedocvspanfoo` which wraps the former, root-reading variant.

---

## Code Exploration

Now I have everything needed for a definitive answer.

---

## How `retrievevspansetpm` Derives Subspace Extents

**Short answer:** It depends on which subspace — and the two paths are fundamentally different. The link subspace reads from the root crum's `setwispnd`-computed fields directly; the text subspace traverses to the bottom crums and accumulates per-entry displacements.

---

### Entry point: `retrievevspansetpm` [orglinks.c:173–221]

```c
bool retrievevspansetpm(typetask *taskptr, typeorgl orgl, typevspanset *vspansetptr)
{
  typecorecrum *ccptr = (typecorecrum *) orgl;
  tumblerclear (&voffset);
  *vspansetptr = NULL;
  if (is1story (&ccptr->cwid.dsas[V])) {          // line 184
      /* ... single-story fast path */
  } else {
      /* ... multi-story: link + text */
  }
}
```

The branch decision is `is1story(&ccptr->cwid.dsas[V])` [line 184], calling `is1story` [tumble.c:237–247], which returns `TRUE` if all `mantissa[1..NPLACES-1]` are zero — i.e., the root's V-space width is a pure first-story tumbler with no link-subspace component.

---

### Path 1 — Single-story (pure text, no links) [lines 184–190]

```c
movetumbler (&ccptr->cdsp.dsas[V], &vspan.stream);  // line 186
movetumbler (&ccptr->cwid.dsas[V], &vspan.width);   // line 187
```

Both stream and width are read **directly from the root crum's `cdsp`/`cwid` fields** — exactly the values that `setwispnd` maintains. No traversal. This is identical to what the simpler `retrievevspanpm` does [orglinks.c:165–172].

---

### Path 2 — Multi-story (text + links) [lines 191–220]

This is where the two subspaces diverge.

#### Link subspace [lines 195–204] — uses root's `setwispnd` fields

```c
movetumbler (&ccptr->cwid.dsas[V], &linkvspan.stream);   // line 197
linkvspan.stream.mantissa[1] = 0;                         // line 198
tumblerjustify(&linkvspan.stream);
movetumbler (&ccptr->cwid.dsas[V], &linkvspan.width);    // line 201
linkvspan.width.mantissa[1] = 0;                          // line 202
tumblerjustify(&linkvspan.width);
```

Both stream and width are extracted from the root's `cwid.dsas[V]` — the `setwispnd`-maintained aggregate — then `mantissa[1]` is zeroed to isolate the link digit. **No tree traversal.**

#### Text subspace [lines 207–212] — traverses to bottom crums

```c
maxtextwid(taskptr, ccptr, &voffset, &maxwid);   // line 207
tumblerclear (&vspan.stream);                     // line 209 — stream always zero
movetumbler (&maxwid, &vspan.width);              // line 210
vspan.width.mantissa[0] = 0;                      // line 211
```

The width is **not** read from the root; it is computed by `maxtextwid`.

---

### `maxtextwid` [orglinks.c:224–245] — the traversal

```c
int maxtextwid(typetask *taskptr, typecorecrum *crumptr, tumbler *voffset, typevspanset *maxwidptr)
{
    if (istextcrum(crumptr)) {
        tumbleradd(voffset, &crumptr->cdsp.dsas[V], &tmpwid);   // line 235
        tumblermax(&tmpwid, maxwidptr, maxwidptr);               // line 236
    } else {
        tumbleradd(voffset, &crumptr->cdsp.dsas[V], &localvoffset);  // line 238
        for (ptr = findleftson(...); ptr; ptr = findrightbro(ptr)) {
            if (!islinkcrum(ptr))                                // line 240
                maxtextwid(taskptr, ptr, &localvoffset, maxwidptr);  // line 241
        }
    }
}
```

The function walks the entire crum subtree recursively:
- **At inner nodes:** accumulates the node's own `cdsp.dsas[V]` into a running `localvoffset` [line 238], passes it down.
- **At text-leaf crums** (`istextcrum` [lines 246–253]: `mantissa[1]==0` and `is1story(cwid)`): computes `tmpwid = voffset + cdsp.dsas[V]` [line 235] and updates a running maximum [line 236].
- **Skips link crums** (`islinkcrum` [lines 255–261]: `mantissa[0]==1` and `mantissa[1]!=0`) entirely [line 240].

The result is the maximum accumulated V-address of any text leaf — effectively the right edge of the text subspace, computed bottom-up from individual crum displacements, **not** from the root's `cwid`.

---

### Why not just read the root?

The comment in the source explains it directly [orglinks.c:192–194]:

```c
/* the link part is simple, just grab the last digit off the wid */
/* the text part we get from a max function that delves into the crums */
/* in both cases we have to remove the first digit of the tumbler... */
```

The root's `cwid.dsas[V]` encodes a mixed multi-story tumbler — its `mantissa[0]` covers the text extent and its `mantissa[1]` covers the link extent. The link part can be extracted by masking. But the text extent cannot be directly read from `mantissa[0]` of the root width, because the link crums also displace into the V-address space in complex ways; `maxtextwid` surgically finds only text leaves and accumulates only their contributions.

---

### Note on the dead code

An earlier version of `retrievevspansetpm` [orglinks.c:266–275, inside `#ifdef UnDEFined`] used `walkorglonvpm` — a full walk that enumerated every span individually. The current active version is an optimisation: link subspace reads the root directly, and only the text subspace still requires traversal.

---

### Summary

| Subspace | Source of extent | Method |
|---|---|---|
| **1-story (text only)** | Root crum `cdsp`/`cwid` | Direct read — `setwispnd` values |
| **Link subspace** (multi-story) | Root crum `cwid` | Direct read + `mantissa[1]` mask |
| **Text subspace** (multi-story) | Bottom-level text crums | Tree traversal in `maxtextwid`, accumulating per-crum `cdsp.dsas[V]`, tracking maximum |

`retrievevspansetpm` does **not** uniformly derive extents from the POOM root. It uses the root's `setwispnd`-maintained fields only for the link subspace (and the degenerate single-story case). For the text subspace of a mixed document, it traverses to the bottom crums and accumulates per-entry widths via `maxtextwid`.
