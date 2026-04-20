## Question 14 [gregory]

> When REARRANGE moves content via `makeoffsetsfor3or4cuts`, the KB says I-addresses are preserved — but does the implementation copy POOM bottom crums with their original I-displacement and I-width fields untouched, or does it reconstruct them through arithmetic that could theoretically drift?

## KB Synthesis

REARRANGE preserves I-fields by **not touching them at all** — it modifies only the V-component of each POOM crum's displacement in-place. The I-fields are physically untouched memory.

The operative code is `edit.c:125`:

```c
tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index])
```

In the POOM 2D enfilade, `cdsp.dsas` is a two-component displacement array: one index for SPANRANGE (V-dimension) and one for ORGLRANGE (I-dimension). The `rearrangend()` loop applies offsets exclusively to `dsas[SPANRANGE]`. The `dsas[ORGLRANGE]` component (the I-displacement) and `cwid.dsas[ORGLRANGE]` (the I-width) are never referenced in the offset application.

This means:

- **No copying**: crums are mutated in-place, not reconstructed
- **No I-arithmetic**: the I-dimension of each crum is untouched bytes
- **No drift possible**: you can't accumulate arithmetic error on fields you never compute over

[ST-REARRANGE] (Finding 0056) states explicitly: "The operation modifies V-addresses exclusively — it calls `tumbleradd(&ptr->cdsp.dsas[index], ...)` which updates the displacement's **V-address component**. No I-addresses are touched, no content is copied, no new permascroll entries are created."

[INV-REARRANGE-IDENTITY] (Finding 0056) formalizes the consequence: `∀ c ∈ content(doc): i_addr(c, doc_after) = i_addr(c, doc_before)`. The proof obligation is trivial given the above — I-fields are preserved because nothing writes to them.

The only arithmetic involved in REARRANGE is tumbler addition on V-displacements. I-displacements and I-widths are preserved bit-for-bit from before the operation.

---

## Code Exploration

I now have everything needed to give the full answer.

---

## How REARRANGE handles POOM bottom-crum I-address fields

The implementation uses **two different mechanisms** depending on whether a crum exists before the cuts or is created by them. Neither mechanism is a pure field-copy, but only one involves arithmetic reconstruction.

---

### Phase 1 — `makecutsnd` slices crums that straddle cut boundaries

`rearrangend` [edit.c:108–110] calls `makecutsnd`, which walks the tree and eventually calls `slicecbcpm` [ndcuts.c:373] whenever a bottom crum is `THRUME` (straddles) a cut knife. This is the code that creates new crums.

```c
// ndcuts.c:396–447  (slicecbcpm)
tumblersub (cut, &grasp.dsas[index], &localcut);   // localcut = V-distance from crum start to cut
// ...
movewisp (&ptr->cwid, &newwid);                    // copy all widths into newwid
for (i = 0; i < widsize(enftype); i++) {           // widsize(POOM) = WIDSIZEPM = 2 (V and I)
    /* I really don't understand this loop */
    newwid.dsas[i].mantissa[0] = localcut.mantissa[0];   // applies V-cut distance to ALL dims
    tumblerjustify (&newwid.dsas[i]);
}
locksubtract ((tumbler*)&ptr->cwid, (tumbler*)&newwid, (tumbler*)&new->cwid, 2);  // new->cwid = old - split
movewisp (&newwid, &ptr->cwid);                           // ptr->cwid = split
dspadd (&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype);    // new->cdsp = ptr->cdsp + ptr->cwid
move2dinfo (&((type2dcbc *)ptr)->c2dinfo, &((type2dcbc *)new)->c2dinfo);  // copy homedoc
adopt(new, RIGHTBRO, ptr);
```

`widsize(POOM)` is `WIDSIZEPM = 2` [wisp.h:27,60], and `dspsize(POOM)` is `DSPSIZEPM = 2` [wisp.h:26,61]. So `dspadd` [wisp.c:15–17] operates on **both** the V and I components: `lockadd(a->dsas, b->dsas, c->dsas, dspsize(POOM))`.

The new right-half crum's fields after `slicecbcpm`:
- **I-width**: `new->cwid.dsas[I] = old->cwid.dsas[I] − localcut` (arithmetic)
- **I-displacement**: `new->cdsp.dsas[I] = ptr->cdsp.dsas[I] + localcut` (arithmetic via `dspadd`)

The original left-half crum `ptr`:
- **I-width**: set to `localcut` (arithmetic, **modified in place**)
- **I-displacement**: **unchanged** (untouched)

The author's comment at `ndcuts.c:439` — `/* I really don't understand this loop */` — is there in the shipping code. The loop applies `localcut.mantissa[0]` (a V-axis scalar) uniformly to **all** width dimensions, implicitly relying on the invariant that V-width and I-width are always equal in POOM bottom crums. There is no assertion or guard checking this assumption.

---

### Phase 2 — `rearrangend` shifts V-displacement of moved crums

After `makecutsnd` finishes, the rearrangement loop in `rearrangend` [edit.c:113–136] classifies each child and applies offsets:

```c
// edit.c:124–128
case 1:  case 2:  case 3:
    tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
    ivemodified((typecorecrum*)ptr);
    break;
```

Here `index = V`, confirmed by the sole call site in `orglinks.c:139`:

```c
// orglinks.c:139
rearrangend((typecuc*)docorgl, cutseqptr, V);
```

`tumbleradd` modifies only `cdsp.dsas[V]`. For all moved crums:
- **I-displacement** (`cdsp.dsas[I]`): **completely untouched**
- **I-width** (`cwid.dsas[I]`): **completely untouched**

---

### Summary table

| Crum type | I-displacement | I-width |
|---|---|---|
| **Existing crum that moves** (cases 1–3, rearrangend:125) | Preserved verbatim | Preserved verbatim |
| **Left half of split crum** (slicecbcpm:445–446) | Preserved verbatim | Replaced with `localcut` (arithmetic) |
| **New right-half crum** (slicecbcpm:444, 446) | `old_cdsp.dsas[I] + localcut` (arithmetic) | `old_cwid.dsas[I] − localcut` (arithmetic) |

---

### Can the arithmetic theoretically drift?

All arithmetic is exact integer tumbler operations — no floating-point, no rounding, no accumulation error in the IEEE sense.

However, there is a **structural fragility**. The loop at `ndcuts.c:439–442` is a single-scalar operation that conflates V-space and I-space by writing `localcut.mantissa[0]` (a V-axis cut distance) to **both** `newwid.dsas[V]` and `newwid.dsas[I]`. This is only correct if the POOM invariant holds: the V-width of a bottom crum equals its I-width (1 V-unit → 1 I-unit). No assertion enforces this.

If a prior operation (an undetected bug elsewhere) introduced a V/I-width mismatch, `slicecbcpm` would construct incorrect I-displacements for right-half crums — and do so silently, without error. Subsequent operations on the same POOM would propagate the bad I-addresses. There is no re-derivation from the granfilade; the POOM is the authoritative store of the V↔I mapping and there is no cross-check against it during rearrangement.

---

### Bottom line

The KB claim that "I-addresses are preserved" is **accurate for the move step** (phase 2): existing crums that are displaced get only their V-displacement incremented by `diff[i]`, and their I fields are never touched. But it is **incomplete for the slice step** (phase 1): every bottom crum that crosses a cut boundary has its I-width rewritten, and the new right-half crum receives an I-displacement computed by `dspadd(ptr->cdsp, ptr->cwid, new->cdsp, POOM)` [ndcuts.c:446] — pure arithmetic. This arithmetic is correct as long as the V=I alignment invariant holds throughout, which the code assumes but does not verify.
