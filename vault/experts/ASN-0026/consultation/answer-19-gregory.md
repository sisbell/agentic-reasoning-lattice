## Question 19 [gregory]

> The spanfilade indexes I-spans per document via DOCISPAN entries. When a single POOM entry (one contiguous I-span) is split by INSERT into two entries, does the original DOCISPAN entry remain valid for link discovery, or must new DOCISPAN entries be created for the two halves?

## KB Synthesis

The original DOCISPAN entry remains valid. No new entries are needed for the split halves.

**Why:**

INSERT's knife-cut mechanism splits POOM crums in **V-space only**. When a crum covering `[V_a, V_b) → [I_a, I_b)` is cut at position `V_p`, the result is two crums: `[V_a, V_p) → [I_a, I_p)` and `[V_p + width, V_b + width) → [I_p, I_b)`. The I-address range `[I_a, I_b)` is not split — it is merely accessed via two POOM crums instead of one. The underlying permascroll content is unchanged.

DOCISPAN entries index **I-address ranges → documents** [SS-DOCISPAN]. The original DOCISPAN entry, created when the content was first placed via INSERT or COPY, covered `[I_a, I_b)`. After the POOM split, that I-range still exists contiguously and still belongs to the same document. The DOCISPAN entry remains an accurate index: this document contains I-addresses `[I_a, I_b)`.

INSERT adds to the spanfilade only for **newly allocated I-addresses** — the fresh I-addresses for the inserted text get their own new DOCISPAN entry [ST-INSERT, Finding 0036]. The call chain `doinsert → inserttextingranf → docopy → insertspanf(..., DOCISPAN)` creates entries only for the newly inserted ispanset, never touching existing entries.

This is structurally guaranteed by three interlocking properties:

1. **Granfilade immutability** [INV-IADDR-IMMUTABILITY]: Existing I-addresses are never moved, renumbered, or split. The I-span the original DOCISPAN covers remains byte-for-byte identical.

2. **Spanfilade write-only** [INV-SPANF-WRITE-ONLY]: There is no `deletespanf` or `modifyspanf`. INSERT can only add entries, never modify or remove the original.

3. **Content-spanf isolation** [FC-CONTENT-SPANF-ISOLATION]: INSERT's only spanfilade effect is writing new DOCISPAN entries for newly allocated I-spans. POOM restructuring (the knife-cut, shifting, crum creation) occurs entirely in the granfilade and has no spanfilade code path.

The consequence for link discovery: `FINDDOCSCONTAINING` queries against the original I-range will still return this document correctly, even when the content has been fragmented across N POOM crums by subsequent inserts. DOCISPAN coverage is cumulative and I-space-based — it does not require POOM contiguity.

---

## Code Exploration

Now I have all the code I need to trace the full path. Let me give the definitive answer.

---

## Answer: DOCISPAN Entries After a POOM Split

**The original DOCISPAN entry remains valid. No new DOCISPAN entries are created for the split halves.** Here is the full trace.

---

### The INSERT Execution Path

`doinsert` [do1.c:87-123] runs two sequential operations:

```c
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy (taskptr, docisaptr, vsaptr, ispanset));
```

`inserttextingranf` allocates new permascroll space and returns a **single ispan** covering the entire new text [granf2.c:102-107]:

```c
ispanptr->itemid = ISPANID;
movetumbler (&spanorigin, &ispanptr->stream);
tumblersub (&lsa, &spanorigin, &ispanptr->width);
*ispansetptr = ispanptr;
```

`docopy` [do1.c:45-65] then calls **both** the POOM update and the spanfilade update, passing only this new ispanset:

```c
insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)   // do1.c:60
&& insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)  // do1.c:62
```

---

### Where the POOM Gets Split

`insertpm` [orglinks.c:75-134] calls:

```c
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
```
[orglinks.c:130]

`insertnd` [insertnd.c:51-61], for POOM type, calls `makegappm` **before** `doinsertnd`:

```c
case POOM:
    makegappm (taskptr, fullcrumptr, origin, width);
    ...
    bothertorecombine=doinsertnd(fullcrumptr,origin,width,infoptr,index);
```

`makegappm` [insertnd.c:124-172] makes two cuts at the insertion V-address:

```c
movetumbler (&origin->dsas[V], &knives.blades[0]);
findaddressofsecondcutforinsert(&origin->dsas[V], &knives.blades[1]);
knives.nblades = 2;
knives.dimension = V;
makecutsnd (fullcrumptr, &knives);
```

`makecutsnd` → `makecutsbackuptohere` → `slicecbcpm` [ndcuts.c:373-450] is invoked when a POOM leaf is `THRUME` (straddles the knife). It **physically splits** the leaf:

```c
// [ndcuts.c:438-447]
movewisp (&ptr->cwid, &newwid);
for (i = 0; i < widsize(enftype); i++) {/* I really don't understand this loop */
    newwid.dsas[i].mantissa[0] = localcut.mantissa[0];
    tumblerjustify (&newwid.dsas[i]);
}
locksubtract ((tumbler*)&ptr->cwid, (tumbler*)&newwid, (tumbler*)&new->cwid, (unsigned)widsize(enftype));
movewisp (&newwid, &ptr->cwid);
dspadd (&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype);
move2dinfo (&((type2dcbc *)ptr)->c2dinfo, &((type2dcbc *)new)->c2dinfo);
adopt(new,RIGHTBRO,ptr);
```

The loop applies the V-cut position proportionally to **both V and I dimensions** (POOM has `widsize = 2`). The right half's displacement is set to `ptr->cdsp + ptr->cwid`, giving it the correct I-origin. Both halves get the same `homedoc` via `move2dinfo`. The original leaf is physically split into two POOM leaves, each covering half the old I-span and half the old V-span.

Then `makegappm` shifts V-offsets of all crums to the right of the cut [insertnd.c:161-164]:

```c
case 1:
    tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
    ivemodified (ptr);
```

This is a pure V-space adjustment. **The I-dimension offsets (`dsas[I]`) of existing crums are not touched.**

---

### No Spanfilade Update for Existing Crums

`makegappm` contains zero calls to `insertspanf` or any spanfilade update. The only DOCISPAN writes are in `docopy` → `insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)` [do1.c:62], which carries only the **new** ispanset returned by `inserttextingranf`. 

`insertspanf` [spanf1.c:15-54] inserts one spanfilade entry per ispan in that new set:

```c
for (; sporglset; sporglset = ...) {
    ...
    insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
}
```

Existing DOCISPAN entries — covering the I-spans of content that was already in the document — receive **no write**.

---

### Why Existing DOCISPAN Entries Remain Valid

The invariant that protects DOCISPAN validity is the **immutability of permascroll I-spans**.

`finddocscontainingsp` [spanf1.c:151-188] queries the spanfilade indexed by I-span in SPANRANGE:

```c
tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);
tumblerincrement (&docspace.width, 0, 1, &docspace.width);
for (; ispanset; ispanset = ispanset->next) {
    context = retrieverestricted((typecuc*)spanf, &docspace, ORGLRANGE, ispanset, SPANRANGE, (typeisa*)NULL);
    for (c = context; c; c = c->nextcontext) {
        movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);
        beheadtumbler (&docid, &document.address);
```

When the original text [I=A, width=W] was inserted, `insertspanf` wrote one DOCISPAN entry: I-span [A, A+W) → document D. When a subsequent INSERT splits the POOM leaf that covers [A, A+W) into two halves — say covering [A, A+W₁) and [A+W₁, A+W) — this restructuring lives entirely inside the POOM. The spanfilade entry for [A, A+W) → D is untouched.

Link discovery queries the spanfilade with an I-span, finds the covering DOCISPAN entry, and returns the document address. The POOM split does not narrow or invalidate that I-span range in the spanfilade. The query still succeeds.

---

### Summary

| Event | POOM | Spanfilade (DOCISPAN) |
|---|---|---|
| Text inserted at V=X | New leaf: [V=X, I=newtext] | New entry: [I=newtext] → doc |
| Later INSERT at V=Y (within existing content) | `makegappm` splits existing leaf at V=Y; shifts right-half V-offsets | **No change** |
| Link discovery via `finddocscontainingsp` | Not consulted | Finds original DOCISPAN entry; still valid |

The original DOCISPAN entry remains valid for link discovery. The POOM split is structurally invisible to the spanfilade because: (1) DOCISPAN entries are keyed by I-span, not V-span; (2) I-spans are immutable permascroll addresses; (3) `makegappm` only adjusts V-offsets and creates no spanfilade side effects. No new DOCISPAN entries are written for the two POOM halves.
