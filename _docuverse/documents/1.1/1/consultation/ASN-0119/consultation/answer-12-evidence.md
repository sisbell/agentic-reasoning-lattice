## Question 12 [evidence]

> After a pivot or swap, do the I-displacement and I-width fields of every affected POOM bottom crum remain byte-for-byte identical to their pre-REARRANGE values while only V-displacement changes?

## KB Synthesis

Yes. After a pivot or swap, the I-displacement and I-width of every affected POOM bottom crum remain byte-for-byte unchanged. Only `cdsp.dsas[V]` (the V-dimension displacement) is modified.

**The mechanism** [ST-REARRANGE, Finding 0056]:

The entire REARRANGE effect is a single `tumbleradd` call:
```c
tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index])
```
where `index` is the V dimension. The I-dimension displacement (`cdsp.dsas[I]`), I-width (`cwid.dsas[I]`), and V-width (`cwid.dsas[V]`) are not referenced anywhere in `rearrangend()`, `makeoffsetsfor3or4cuts()`, or `rearrangecutsectionnd()`.

**Confirmation across three angles:**

1. **Code-level** [ST-REARRANGE]: "No I-addresses are touched, no content is copied, no new permascroll entries are created."

2. **Invariant** [INV-REARRANGE-IDENTITY]: "The I-address, stored separately, is never touched." The multiset of I-addresses in a document is invariant under rearrangement.

3. **Frame condition** [FC-GRANF-ON-DELETE]: REARRANGE is granfilade-preserving — `granf_after(REARRANGE) = granf_before(REARRANGE)`. Since POOM bottom crums encode their I-dimensions from the granfilade allocation, and the granfilade is untouched, those fields cannot change.

**Width fields specifically:** Width (`cwid`) represents crum span size. REARRANGE moves crums but does not split or merge them at the bottom-crum level, so neither `cwid.dsas[V]` nor `cwid.dsas[I]` changes. Only the V-displacement shifts by the offset computed from the cut geometry.

---

## Code Exploration

Good — `orglinks.c:139` confirms `rearrangend` is called with `V` as the index for all pivot/swap operations. I have enough to give a definitive answer.

---

## Answer

### Short answer: I-width is always preserved. I-displacement is preserved *during* the rearrangend loop itself, but MAY be rewritten — at the same absolute value — if `recombine` reorganizes the tree structure afterward.

---

### Data structure

From `wisp.h`:

```c
#define I  0
#define V  1
#define DSPSIZEPM 2   // POOM dsp has 2 components: [I] and [V]
#define WIDSIZEPM 2   // same for wid
```

Every crum carries:
- `cwid.dsas[I]` — I-width
- `cwid.dsas[V]` — V-width  
- `cdsp.dsas[I]` — I-displacement (relative to parent)
- `cdsp.dsas[V]` — V-displacement (relative to parent)

---

### Phase 1 — the rearrangend loop (edit.c:113–135)

All calls to `rearrangend` from production code pass `V` as `index`:

```
backend/orglinks.c:139:  rearrangend((typecuc*)docorgl, cutseqptr, V);
```

The loop that modifies displaced crums is:

```c
// edit.c:124–127
case 1:  case 2:  case 3:
    tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
    ivemodified((typecorecrum*)ptr);
    break;
```

`index = V = 1`, so only `cdsp.dsas[V]` is written. `cdsp.dsas[I]` and `cwid` are never touched. **At this phase, I-displacement and I-width are byte-for-byte unchanged.**

---

### Phase 2 — setwispupwards (edit.c:137)

```c
setwispupwards (father, 1);   // edit.c:137 — "should do nothing, but just on general principles"
```

This calls `setwisp` → `setwispnd` (wisp.c:171–228) up the ancestor chain. `setwispnd` computes the minimum displacement corner across all children:

```c
// wisp.c:193–196
movewisp (&ptr->cdsp, &mindsp);
for (ptr = getrightbro(ptr); ptr; ptr = getrightbro (ptr))
    lockmin ((tumbler*)&mindsp, (tumbler*)&ptr->cdsp, (tumbler*)&mindsp,
             (unsigned)dspsize(ptr->cenftype));
```

`dspsize(POOM) = 2`, so `lockmin` computes the per-dimension minimum across both `dsas[I]` and `dsas[V]`.

If `mindsp ≠ 0`, it re-normalizes:

```c
// wisp.c:209–211
ptr->modified = TRUE;
dspsub(&ptr->cdsp, &mindsp, &ptr->cdsp, (INT)ptr->cenftype);
```

`dspsub` calls `locksubtract` with `loxize = dspsize(POOM) = 2`, subtracting `mindsp.dsas[I]` from `ptr->cdsp.dsas[I]` and `mindsp.dsas[V]` from `ptr->cdsp.dsas[V]`.

**Critical invariant**: Before rearrange, the tree was normalized, meaning `mindsp.dsas[I]` across all siblings was 0. The rearrange loop only touched `cdsp.dsas[V]`, so all `cdsp.dsas[I]` values are identical to pre-rearrange. Therefore `mindsp.dsas[I] = 0` after rearrange, and `dspsub` subtracts zero from every `cdsp.dsas[I]`. **I-displacements are unchanged by this phase.**

`setwispnd` writes back only to `father->cwid` (wisp.c:225) — never to children's `cwid`. **I-width of bottom crums is unchanged.**

---

### Phase 3 — recombine (edit.c:139)

```c
recombine(fullcrumptr);   // edit.c:139
```

`recombinend` (recombine.c:104–131) may reorganize the tree by calling `takeovernephewsnd` → `takenephewnd` or `eatbrossubtreend`. These adopt crums from one parent into another and must re-express their displacements in the new coordinate frame:

**takenephewnd (recombine.c:243, 248):**
```c
dspadd (&bro->cdsp, &nephew->cdsp, &nephew->cdsp, bro->cenftype);  // convert to absolute
...
dspsub (&nephew->cdsp, &me->cdsp, &nephew->cdsp, me->cenftype);    // re-express under new parent
```

**fixdspsofbroschildren (recombine.c:264–265):**
```c
dspadd (&bro->cdsp, &nephew->cdsp, &nephew->cdsp, me->cenftype);
dspsub (&nephew->cdsp, &me->cdsp, &nephew->cdsp, me->cenftype);
```

Both `dspadd`/`dspsub` operate on `dspsize(POOM) = 2` dimensions — both I and V. If a bottom crum is adopted into a new parent (height-1 node), its `cdsp.dsas[I]` is rewritten to express the same absolute I-position relative to the new parent's I-displacement.

**The stored byte value of `cdsp.dsas[I]` changes; the absolute I-position it encodes does not.**

For `cwid.dsas[I]` — `takenephewnd` and `fixdspsofbroschildren` never write to `cwid` of the adopted crums. `expandcrumleftward` (makeroom.c:59) writes only to the *father's* `cwid` and shifts children's `cdsp`, never children's `cwid`. **I-width is never changed by recombine.**

---

### Summary table

| Field | rearrangend loop | setwispupwards | recombine (tree stable) | recombine (crum re-parented) |
|---|---|---|---|---|
| `cdsp.dsas[V]` | **Modified** (edit.c:125) | Re-normalized | unchanged | re-expressed |
| `cdsp.dsas[I]` | **Unchanged** | Subtract 0 → unchanged | unchanged | **Re-expressed** (same absolute value, different relative) |
| `cwid.dsas[I]` | **Unchanged** | Not touched | unchanged | **Unchanged** |
| `cwid.dsas[V]` | **Unchanged** | Not touched | unchanged | **Unchanged** |

---

### Direct answer

**I-width (`cwid.dsas[I]`)**: Byte-for-byte identical after a pivot/swap, unconditionally. No code path in rearrangend, setwispnd, or recombine writes to a child crum's `cwid`.

**I-displacement (`cdsp.dsas[I]`)**: The stored byte value is preserved *if and only if recombine does not re-parent the crum*. If `recombine` moves the crum to a new parent (via `takenephewnd`/`fixdspsofbroschildren`, recombine.c:243–265), the stored relative displacement is rewritten to encode the same absolute I-position under the new parent. The semantic I-mapping is invariant; the raw field bytes are not.

The premise holds cleanly for the rearrangend loop itself (`edit.c:113–135`). It holds globally for I-width. For I-displacement, the invariant is that the *absolute* I-position is preserved, not that the *stored relative field* is byte-identical.
