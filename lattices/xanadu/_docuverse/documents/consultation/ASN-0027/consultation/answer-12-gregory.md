## Question 12 [gregory]

> After DELETE shifts a POOM entry's V-position leftward via `tumblersub`, can any subsequent operation (INSERT, COPY, REARRANGE) restore the original V-position, or is the pre-delete V-address layout permanently lost?

## KB Synthesis

After DELETE shifts a surviving POOM entry's V-displacement leftward via `tumblersub`, the original V-position **can** be numerically restored by a subsequent INSERT or COPY. But whether the full pre-delete layout is restored depends on the operation used.

## Mechanics of the Shift

From [ST-DELETE] (Finding 0053/0055): DELETE subtracts the deletion width from the V-displacement of every POOM entry after the deletion range, using `tumblersub` → `strongsub`. The `strongsub` exponent guard means only same-exponent entries shift; cross-subspace entries are immune [FC-SUBSPACE].

The shift is pure arithmetic: `vpos_after = vpos_before - delete_width`.

## INSERT/COPY Restoration

[ST-INSERT] (Finding 0054) shows that INSERT at position `P` of width `w` shifts all POOM entries in `[P, subspace_boundary)` **rightward** by `+w` via `tumbleradd`. This is arithmetically the inverse of the DELETE shift.

If you INSERT (or COPY) at the same position and with the same width as the deleted span:
- All surviving entries that were shifted left by `-w` are shifted right by `+w`
- Their V-displacements return to their pre-delete values

**So yes — V-positions of surviving entries are restorable.**

## I-Address Restoration: The Critical Distinction

[INV-DELETE-NOT-INVERSE] establishes that DELETE+INSERT is NOT a true inverse:
- INSERT allocates **fresh I-addresses** (`next_iaddr(granf) + 1`) — never reuses old ones [INV-NO-IADDR-REUSE]
- The V-positions are numerically restored, but the I-addresses in the gap differ

[ST-COPY] documents the alternative: COPY shares **existing** I-addresses via `insertpm`. If you COPY from a version (or any document) that still references the original I-addresses:
- V-positions of surviving entries are restored (same INSERT-style shift)
- The new POOM entries in the gap reference the original I-addresses
- Full V+I layout is restored — [INV-IADDR-IMMUTABILITY] confirms the original I-addresses still exist in the granfilade ([FC-GRANF-ON-DELETE]: DELETE never touches the granfilade)

## REARRANGE

[ST-REARRANGE] only permutes existing POOM entries; it creates no new ones. It cannot restore deleted content — there are no POOM entries to rearrange back. It also cannot shift entries to arbitrary target positions since offsets are computed from cut geometry, not absolute targets.

## The Deeply Orphaned Case

[EC-DEEPLY-ORPHANED-LINK] (Finding 0053, corrected by 0055) notes that if DELETE somehow pushed a same-exponent entry's V-position **negative**, that entry becomes invisible but still exists in the POOM tree. A subsequent INSERT cannot rescue it: INSERT's knife only shifts entries at `>= insertion_point`, and a negative V-position is below any positive insertion point. The entry remains unreachable. However, Finding 0055 clarifies this negative-shift scenario is prevented for cross-subspace entries by the `strongsub` exponent guard.

## Summary

| Goal | INSERT | COPY (from original I-addresses) | REARRANGE |
|------|--------|----------------------------------|-----------|
| Restore V-positions of surviving entries | ✓ | ✓ | ✗ |
| Restore deleted content at original V-positions | ✓ (new I-addrs) | ✓ (original I-addrs) | ✗ |
| Restore original I-addresses in the gap | ✗ | ✓ | ✗ |
| Full pre-delete layout (V + I) | ✗ | ✓ | ✗ |

The only path to complete identity-preserving restoration is COPY from a document that retained the original I-addresses (typically a version created before the DELETE). This is the design intent of CREATENEWVERSION as documented in [ST-VERSION-CREATE] and [INV-DELETE-NOT-INVERSE] — "undo" in Xanadu is not INSERT but COPY-from-version.

---

## Code Exploration

Now I have a complete picture. Let me trace through all the relevant paths carefully.

---

## Answer

### The Delete Mechanism

`dodeletevspan` [do1.c:158–167] calls `deletevspanpm` [orglinks.c:145–152], which calls `deletend` [edit.c:31–76].

Inside `deletend`, for every POOM crum that lies **entirely to the right** of the deleted span (case 2 in `deletecutsectionnd` [edit.c:235–248]):

```c
// edit.c:63
tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
```

This subtracts the deleted span's `width` from each surviving crum's V-displacement, collapsing the gap. Crums that fall **inside** the deleted span (case 1) are permanently removed:

```c
// edit.c:59–60
disown ((typecorecrum*)ptr);
subtreefree ((typecorecrum*)ptr);
```

The V→I bindings for those disowned crums no longer exist anywhere.

---

### Can INSERT Restore the Original V-Position Layout?

`doinsert` [do1.c:87–123] → `docopy` → `insertpm` [orglinks.c:75–134] → `insertnd` [insertnd.c:15–111] → `makegappm` [insertnd.c:124–172].

Inside `makegappm`, for every crum that lies at or after the insertion point (case 1 from `insertcutsectionnd`):

```c
// insertnd.c:162
tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
```

This is the **exact inverse** of `tumblersub` — it shifts surviving crums rightward by `width`. So if an INSERT is placed at the original `origin` address with the same `width`:

1. `makegappm` opens the gap.
2. All crums that were shifted leftward by the delete are shifted rightward by the same amount.
3. Their V-addresses are restored to what they were before the delete.

**The relative V-address layout of surviving content is geometrically restored.**

However, there is a guard in `makegappm` [insertnd.c:140–143]:

```c
if (iszerotumbler (&fullcrumptr->cwid.dsas[V])
|| tumblercmp (&origin->dsas[V], &grasp.dsas[V]) == LESS
|| tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);
```

This means `makegappm` is skipped if the insertion point is **outside** the current document V-range (`grasp` to `reach`). After a delete, if the deleted region was at the end of the document and nothing follows it, the insertion point may fall outside this range — and no gap-opening occurs. In that case V-addresses of other content are unaffected (there are none after).

---

### Can COPY Restore the Original V-Position Layout?

`docopy` [do1.c:45–65] calls `insertpm` directly, which calls `insertnd` → `makegappm`. The gap-opening mechanics are **identical to INSERT**. COPY at the original V-address with the same width also geometrically restores the V-layout of all surviving crums.

Note: `acceptablevsa` [do2.c:110–113] — the function that checks whether a V-address is acceptable for insertion — is a stub that **always returns TRUE**:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

There is no validation preventing re-use of a previously-deleted V-address.

---

### Can REARRANGE Restore the Original V-Position Layout?

`dorearrange` [do1.c:34–43] → `rearrangepm` [orglinks.c:137–142] → `rearrangend` [edit.c:78–160].

`rearrangend` computes offsets via `makeoffsetsfor3or4cuts` [edit.c:164–184], using `tumblersub` and `tumbleradd` on the cut positions, then applies them to surviving crums:

```c
// edit.c:124–126
tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
```

REARRANGE can move surviving crums to **any V-positions**, including ones previously occupied before a delete. So yes, rearrange can in principle restore any set of V-addresses for surviving content — but only for content that still exists. It cannot resurrect deleted entries.

---

### Is the Pre-Delete V-Address Layout Permanently Lost?

There are two separate questions here:

**1. V-positions of surviving content**: NOT permanently lost. Any of INSERT, COPY, or REARRANGE can restore the V-positions of surviving entries:
- INSERT/COPY at the original `origin` with the same `width` inverts the `tumblersub` via `tumbleradd` [insertnd.c:162], exactly restoring prior positions.
- REARRANGE can move any surviving content to any V-address.

**2. The original V→I bindings of deleted content**: PERMANENTLY LOST. The disowned POOM crums [edit.c:59–60] are freed. The V→I mapping that specified *which permascroll I-spans* sat at those V-addresses is destroyed and cannot be recovered by any subsequent operation. INSERT/COPY at the same V-address places *new* I-span references there — not the originals.

---

### Summary

| Operation | Restores V-positions of surviving content | Restores original V→I binding of deleted content |
|-----------|------------------------------------------|--------------------------------------------------|
| INSERT at original VSA, same width | **Yes** — `makegappm` inverts the `tumblersub` [insertnd.c:162] | **No** — new I-spans, not original content |
| COPY at original VSA, same width | **Yes** — same path as INSERT | **No** — copied I-spans, not original binding |
| REARRANGE (with correct cut positions) | **Yes** — arbitrary V-address reassignment [edit.c:124–126] | **No** — only moves surviving crums |

The `tumblersub` applied by DELETE [edit.c:63] to surviving crums is **arithmetically reversible** — `tumbleradd` of the same `width` at the same `origin` exactly undoes it. But the V→I bindings for the deleted crums are gone. The `disown`/`subtreefree` [edit.c:59–60] is not reversible: the pre-delete V-address layout, in the sense of *which content was at which V-address*, is permanently lost the moment the crums are freed.
