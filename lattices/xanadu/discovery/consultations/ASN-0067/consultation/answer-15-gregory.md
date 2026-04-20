## Question 15 [gregory]

> For self-transclusion (copying within the same document), if the target V-position falls within the source V-span being copied, what is the resulting POOM state — does the system snapshot the source mapping before applying shifts, or does the shift from `makegappm` alter the source span mid-operation?

## KB Synthesis

## Self-Transclusion with Target Inside Source Span

The system **snapshots the source mapping before any shifting occurs**. This follows necessarily from the call sequence in `docopy`, combined with the single-threaded execution model.

### Mechanism

`docopy` (`do1.c:45-65`) executes two phases strictly sequentially:

1. **Source read phase**: `specset2ispanset` traverses the POOM to convert the source V-span `[s, s+w)` into I-addresses `i₁..iₙ`. This completes entirely before any modification.

2. **Insertion phase**: `insertpm` → `insertnd` → `makegappm` inserts those I-addresses at target position `t`, constructing a two-blade knife `[t, next_subspace_boundary)` and shifting all POOM entries in that range rightward by `w` [SS-TWO-BLADE-KNIFE, ST-INSERT].

Because the single-threaded event loop guarantees run-to-completion semantics [INV-ATOMICITY, INV-SEQUENTIAL-DISPATCH], `specset2ispanset` returns a complete I-address list before `makegappm` touches any POOM entries. The shift in phase 2 does affect the tail of the source span (entries at `[t, s+w)` move to `[t+w, s+2w)`), but those I-addresses were already captured in phase 1.

### Resulting POOM State

For source span `[s, s+w)` → `i₁..iₙ`, target `t` where `s ≤ t < s+w`:

| V-range | Content | Source |
|---|---|---|
| `[s, t)` | original prefix | unchanged (before knife) |
| `[t, t+w)` | **full copy** of `i₁..iₙ` | newly inserted |
| `[t+w, s+2w)` | original suffix | shifted from `[t, s+w)` |
| `[s+2w, ...)` | remainder | shifted from `[s+w, ...)` |

The copy contains the complete source span (captured before the shift), while the original source span is split at `t` with the copy interleaved.

### Caveat

The KB confirms self-transclusion works generally [EC-SELF-TRANSCLUSION] and that the POOM is a multimap tolerating duplicate I-addresses at multiple V-positions [SS-POOM-MULTIMAP]. However, the specific case of target-within-source is not directly tested — the documented self-transclusion scenario uses a target position *after* the source span (Finding 0028 §2, Finding 0039). The answer above is inferred from the `docopy` call sequence and `makegappm` mechanics, not from a golden test of this exact configuration.

---

## Code Exploration

I have all the evidence needed. Here is the full answer.

---

## Self-Transclusion: Source Snapshot vs. `makegappm` Shifts

### Execution Path

The entry point for copy is `docopy` in `do1.c:45`:

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    ...
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)   // ← line 54
    && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)         // ← line 55
    && acceptablevsa (vsaptr, docorgl)                                   // ← line 56
    && asserttreeisok(docorgl)
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)          // ← line 60
    && insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)       // ← line 62
    ...
```

The answer to the question turns on the ordering of these two calls: **`specset2ispanset` runs at `do1.c:54`, before `insertpm` at `do1.c:60`.**

---

### What `specset2ispanset` does: snapshot in I-space

`specset2ispanset` is defined in `do2.c:14`:

```c
bool specset2ispanset(typetask *taskptr, typespec *specset, typeispanset *ispansetptr, int type)
{
    ...
    for (; specset; ...) {
        if (...VSPECID...) {
            findorgl(taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
            && (ispansetptr = vspanset2ispanset(taskptr, docorgl,
                    ((typevspec *)specset)->vspanset, ispansetptr))
        }
    }
```

This calls `vspanset2ispanset` (`orglinks.c:397`), which calls `permute` → `span2spanset` → `retrieverestricted`. The result is `ispanset`: a list of **I-spans** (permascroll addresses). These are the permanent, document-independent coordinates for the source content — not V-positions.

**This snapshot is complete and frozen before `insertpm` is ever called.**

---

### What `insertpm` + `makegappm` does: V-shift only

`insertpm` in `orglinks.c:75` loops over the pre-computed `ispanset` (passed in as `sporglset`):

```c
for (; sporglset; sporglset = ...) {
    unpacksporgl(sporglset, &lstream, &lwidth, &linfo);   // I-address, I-width
    movetumbler(&lstream, &crumorigin.dsas[I]);           // I-dim: from snapshot
    movetumbler(&lwidth,  &crumwidth.dsas[I]);            // I-dim: from snapshot
    movetumbler(vsaptr,   &crumorigin.dsas[V]);           // V-dim: target position
    ...
    insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // line 130
    tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr);                         // line 131
}
```

`insertnd` (`insertnd.c:15`) is called for the POOM case and immediately calls `makegappm` (`insertnd.c:54`):

```c
case POOM:
    makegappm(taskptr, fullcrumptr, origin, width);  // ← line 54
    ...
    bothertorecombine = doinsertnd(...);             // ← line 57
```

Inside `makegappm` (`insertnd.c:124`), the guard clause first checks whether the target is actually within the document's V-range:

```c
if (iszerotumbler(&fullcrumptr->cwid.dsas[V])
|| tumblercmp(&origin->dsas[V], &grasp.dsas[V]) == LESS
|| tumblercmp(&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);    /* for extensions to bc without calling cut */
```

If the target V-position is within the document (including within the source span), `makegappm` proceeds. It makes cuts, finds the intersection node, and then classifies each child by `insertcutsectionnd` (`edit.c:207`). Nodes that return `case 1` — meaning they are **to the right of the insertion point** — get their V-displacement shifted:

```c
case 1:
    tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);  // line 162
    ivemodified(ptr);
```

This shifts `cdsp.dsas[V]` (the V-displacement) of POOM nodes that are right of the target. It does **not** touch `cdsp.dsas[I]` — I-addresses are untouched.

---

### The Critical Answer

**The system snapshots the source mapping before applying shifts.** Here is why:

1. `specset2ispanset` at `do1.c:54` walks the POOM tree and converts source V-spans to I-spans (permascroll addresses). This produces a fully materialized `ispanset` linked list in task memory.

2. `insertpm` at `do1.c:60` uses this `ispanset` directly. It reads `lstream` and `lwidth` from the pre-computed sporgls — these are the I-coordinates captured before any modification.

3. `makegappm` runs inside `insertnd` and shifts V-displacements of POOM nodes to the right of the insertion point. But the `ispanset` is already in memory; it is not derived from the POOM again. The I-coordinates in the sporgl loop (`lstream`, `lwidth` in `orglinks.c:101–109`) are read from the pre-computed snapshot and are immune to the V-shift.

**When the target V-position falls within the source V-span,** `makegappm` will shift rightward POOM nodes — including nodes that encode the portion of the source span to the right of the insertion point. But because the I-span content was already captured at `do1.c:54`, `insertpm` still inserts the correct permascroll content. After the operation, the part of the original source span that was to the right of the target V-position will occupy a new, shifted V-address in the POOM tree, but the inserted transcluded content correctly references the original permascroll I-addresses.

There is no mid-operation aliasing hazard. The POOM is the mutable structure; the `ispanset` is the immutable content descriptor derived from it before mutation begins.
