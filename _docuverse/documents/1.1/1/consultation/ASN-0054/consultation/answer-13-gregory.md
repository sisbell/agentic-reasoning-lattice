## Question 13 [gregory]

> After a sequence of INSERT, DELETE, and COPY operations, can gaps exist in the V-address domain of a document's text subspace — positions with no POOM entry — or is the V-domain always a single contiguous interval from minimum to maximum?

## KB Synthesis

## V-Address Domain Gaps

**Yes, gaps can exist** — but only via deliberate non-adjacent placement, not through normal editing operations.

---

### Why DELETE does not create gaps

DELETE removes the V→I mappings for the deleted range (Case 1: crums entirely within the range are `disown`ed and freed) and shifts all following crums leftward by the deletion width (Case 2: `tumblersub` on V-displacement) [ST-DELETE]. The post-deletion V-domain is `[min, a) ∪ [a+w, max]` where the latter segment shifts to `[a, max−w]`, producing a contiguous result. The `strongsub` exponent guard [SS-TUMBLER] means cross-exponent (cross-subspace) entries are not shifted, but within the text subspace `1.x` all entries share the same exponent, so the shift closes the hole cleanly.

---

### Why INSERT within the existing domain does not create gaps

The two-blade knife [SS-TWO-BLADE-KNIFE] with blades `[insertion_point, next_subspace_boundary)` ensures all crums *after* the insertion point within the same subspace shift rightward by the insertion width [ST-INSERT]. Content placed at position P fills exactly that position; nothing is left unoccupied. Consecutive inserts at adjacent boundaries coalesce via `isanextensionnd` [ST-INSERT Finding 0062], and the enfilade consolidates contiguous regions into a single span [INV-VSPAN-CONSOLIDATION].

---

### How gaps arise

The backend accepts **any** V-position for INSERT or COPY — `acceptablevsa()` unconditionally returns `TRUE` [PRE-INSERT]. The two-blade knife shift only affects crums in `[blade[0], blade[1])`. If you INSERT at V `1.10` when the document's content ends at V `1.5`:

- Existing crums at `[1.1, 1.5]` are all `TOMYLEFT` of blade[0] `= 1.10` → classified case 0, **no shift**
- New content lands at `[1.10, 1.10+w]`
- V-domain becomes `[1.1, 1.5+something] ∪ [1.10, 1.10+w]` — **gap from ~1.5 to 1.10**

The same applies to COPY/VCOPY at an arbitrary non-adjacent target position. The backend does not validate that the target is adjacent to existing content.

When gaps exist, `retrieve_vspanset` returns **multiple spans** within the text subspace rather than one, because `retrievevspansetpm` only consolidates spans that are genuinely contiguous [SS-VSPAN-VS-VSPANSET]. The single-span consolidation in [INV-VSPAN-CONSOLIDATION] is a property of contiguous sequential inserts, not a global guarantee.

---

### Summary

| Operation | Creates gap? | Mechanism |
|-----------|-------------|-----------|
| INSERT within/adjacent to content | No | Shift fills around insertion |
| INSERT beyond content extent | **Yes** | Existing crums TOMYLEFT → no shift; new crum at distant position |
| DELETE | No | Case 2 shift closes the hole |
| COPY within/adjacent | No | Same as INSERT mechanics |
| COPY to non-adjacent position | **Yes** | Same as INSERT beyond extent |

The invariant [INV-VSPAN-CONSOLIDATION] holds only for content that *is* contiguous — it reflects the enfilade's consolidation of adjacent crums, not an enforcement that all insertions produce contiguous output. The backend's gap-prevention is behavioral (callers conventionally insert at the current cursor position) rather than structural.

---

## Code Exploration

Now I have everything I need to give a complete, code-grounded answer.

---

## Answer

The answer is nuanced: **DELETE never creates gaps** — it actively compacts the V-domain. But **INSERT and COPY can create gaps** when given an explicit V-address beyond the current end of content, because the bounds-check guard (`acceptablevsa`) is an unconditional stub.

Here is the full analysis, traced from entry points to leaf operations.

---

### 1. The POOM Data Structure

The POOM (Permutation-Oriented Ordered Map) is a 2D enfilade. Each bottom crum stores:
- `cdsp.dsas[V]` — V-address displacement (position, relative to parent)
- `cwid.dsas[V]` — V-address width (extent)
- `cdsp.dsas[I]`, `cwid.dsas[I]` — corresponding I-space (permascroll) coordinates

The POOM root's `cwid.dsas[V]` encodes the entire V-extent of the document. The question of "gaps" is whether every V-address within that extent maps to a crum entry.

---

### 2. DELETE Does Not Create Gaps — It Compacts

Entry: `dodeletevspan` → `deletevspanpm` → `deletend`

**`dodeletevspan`** [`do1.c:158-167`]:
```c
return (
   findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
);
```

**`deletevspanpm`** [`orglinks.c:145-152`]:
```c
deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
```

**`deletend`** [`edit.c:31-76`] places two knife cuts — one at the deletion start, one at deletion end [`edit.c:40-41`]:
```c
movetumbler (origin, &knives.blades[0]);
tumbleradd (origin, width, &knives.blades[1]);
```

It then iterates every crum in the intersection zone and classifies it via `deletecutsectionnd` [`edit.c:235-248`]:

| Return | Meaning | Action |
|--------|---------|--------|
| `0` | Crum is **left** of the deletion zone | Do nothing |
| `1` | Crum is **inside** the deletion zone | `disown()` + `subtreefree()` — crum removed |
| `2` | Crum is **right** of the deletion zone | **Shift its V-displacement left by the deleted width** |

The critical case 2 is at [`edit.c:63`]:
```c
tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
```

**Every crum to the right of the deleted range has its V-address displacement reduced by exactly the deleted width.** The V-domain closes shut — no gap is ever left behind by DELETE.

---

### 3. INSERT Within Existing Range Does Not Create Gaps

Entry: `doinsert` → `docopy` → `insertpm` → `insertnd` → `makegappm`

**`doinsert`** [`do1.c:87-123`] first allocates the I-space content in the granfilade, then calls `docopy` with the target V-address.

**`makegappm`** [`insertnd.c:124-172`] is the V-space preparation step. It first checks whether the insertion point falls within the current V-extent of the POOM [`insertnd.c:140-143`]:
```c
if (iszerotumbler (&fullcrumptr->cwid.dsas[V])
|| tumblercmp (&origin->dsas[V], &grasp.dsas[V]) == LESS
|| tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);    /* this if for extensions to bc without calling cut*/
```

If the insertion point is **within** the current range (between `grasp` and `reach`), it places two cuts at the insertion point and uses `insertcutsectionnd` to classify each crum. Case 1 crums (those to the right of the insertion point) have their V-displacement **shifted up** by the insertion width [`insertnd.c:162`]:
```c
tumbleradd(&ptr->cdsp.dsas[V],&width->dsas[V],&ptr->cdsp.dsas[V]);
```

New content then fills the opened slot exactly. **No gap.**

---

### 4. INSERT or COPY Beyond the Current End CAN Create Gaps

When the V-address passed to `doinsert` or `docopy` is **at or beyond `reach.dsas[V]`** (the current end of content), `makegappm` hits the third condition above and returns immediately without shifting anything [`insertnd.c:142-143`]:
```c
|| tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);    /* this if for extensions to bc without calling cut*/
```

`insertnd` then proceeds directly to `doinsertnd` → `insertcbcnd`, which places the new crum at the explicitly specified V-address. If that address is strictly greater than `reach.dsas[V]`, the parent's `setwispupwards` call will update the root's `cwid.dsas[V]` to span all the way to the new crum's end — **but no content covers the interval between the old reach and the new crum's start.** A gap exists in the V-domain.

The validation function that was supposed to prevent this is **a no-op stub** [`do2.c:110-113`]:
```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

`docopy` calls `acceptablevsa` before `insertpm` [`do1.c:56`], but since it unconditionally returns `TRUE`, any V-address is accepted — including one that creates a gap.

---

### 5. APPEND Never Creates Gaps

`appendpm` [`orglinks.c:17-27`] always calls `findvsatoappend` to determine the target V-address before calling `doinsert`. The logic [`orglinks.c:44-45`]:
```c
} else if (tumblercmp (&reach.dsas[V], &linkspacevstart) == LESS) {
    movetumbler (&reach.dsas[V], vsaptr); /* no links in doc */
```

inserts new content at exactly `reach.dsas[V]` — the precise end of existing content. This is always contiguous.

---

### Summary

| Operation | V-domain effect | Creates gaps? |
|-----------|----------------|---------------|
| DELETE | Removes crums; shifts all right-side crums left by deleted width [`edit.c:63`] | **No** — compacts |
| INSERT within range | Shifts all right-side crums right by inserted width [`insertnd.c:162`]; new content fills slot | **No** |
| INSERT/COPY at position > current end | `makegappm` skips shifting [`insertnd.c:140-143`]; content placed at explicit position | **Yes** — gap from old `reach` to new crum |
| APPEND | Target is exactly `reach.dsas[V]` [`orglinks.c:45`] | **No** — always contiguous |

**The V-domain is NOT guaranteed to be a single contiguous interval.** DELETE is safe — it compacts aggressively. But INSERT and COPY operate on client-supplied V-addresses, and `acceptablevsa` [`do2.c:110-113`] performs no validation. A client that supplies an explicit V-address beyond the current document end will produce a sparse POOM with unreachable V-addresses between the old end and the new content. The `findvsatoappend` code's awareness of the link subspace boundary [`orglinks.c:39-48`] and its "find the maximum V-address" scan [`orglinks.c:66-67`] further confirm that the system expects V-space can be sparse and navigates it accordingly rather than assuming a single contiguous interval.
