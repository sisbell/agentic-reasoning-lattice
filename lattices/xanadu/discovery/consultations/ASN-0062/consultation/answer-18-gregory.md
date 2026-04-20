## Question 18 [gregory]

> After a copy places content at V-position `v` in the target, does `find_documents_containing` immediately return the target document for those I-addresses, or is there any scenario (analogous to APPEND's missing `insertspanf` call) where the DOCISPAN entry is not created?

## KB Synthesis

**Yes — COPY always creates DOCISPAN entries immediately.** There is no scenario analogous to APPEND's omission.

## The Standard Path

All document placement operations that use `docopy` follow the same call chain [ST-INSERT, Finding 0036]:

```
docopy → insertpm (POOM update)
       → insertspanf(..., DOCISPAN) (spanfilade update)
```

This covers:
- **INSERT** (`doinsert` → `inserttextingranf` → `docopy`)
- **VCOPY/COPY** (`docopy` directly)
- **CREATENEWVERSION** (`docopyinternal` → `insertspanf`) [ST-VERSION-CREATE, Finding 0046]

After any of these, `find_documents_containing` returns the target document immediately [ST-INSERT, Finding 0036]:
> `∀ α ∈ new_i_addresses: doc ∈ FINDDOCSCONTAINING(α)`

## The One Exception: APPEND

APPEND (`doappend`) has the `insertspanf(taskptr, spanf, docptr, textset, DOCISPAN)` call explicitly **commented out** — the code comment reads `/*zzz dies this put in granf?*/` [EC-APPEND-NO-DOCISPAN, Finding 0036]. Content added via APPEND is not discoverable through `find_documents`.

## Granularity of DOCISPAN Creation

For COPY specifically, the number of DOCISPAN entries created equals `|ispanset(source_content)|` — one per contiguous I-address run, not per byte [ST-COPY, Finding 0047]. Copying fragmented content (e.g., transcluded from multiple sources) creates multiple entries. Copying contiguous content creates exactly one.

## Monotonicity

Once created, DOCISPAN entries are never removed [INV-SPANF-WRITE-ONLY, Finding 0057]. DELETE does not call any spanfilade function — it modifies only the POOM [ST-DELETE, Finding 0057]. So after COPY, the target document remains discoverable for those I-addresses permanently, even if the content is later deleted from the document's V-stream [INV-IADDRESS-PERMANENT, Finding 0023].

---

## Code Exploration

---

## Answer

**`docopy` unconditionally calls `insertspanf(DOCISPAN)` — there is no scenario analogous to the APPEND omission.**

---

### The COPY Path

`docopy` [do1.c:45–65] is the canonical copy implementation:

```c
return (
   specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)   // V → I
&& findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)        // open target
&& acceptablevsa (vsaptr, docorgl)                                  // always TRUE [do2.c:112]
&& asserttreeisok(docorgl)
/* the meat of docopy: */
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)         // place in POOM
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)     // ← DOCISPAN index [do1.c:62]
&& asserttreeisok(docorgl)
);
```

The `insertspanf(..., DOCISPAN)` call at `do1.c:62` is present, uncommented, and runs immediately after `insertpm`. It is **not** analogous to the APPEND situation.

The FEBE `copy` handler at `fns.c:35–47` simply delegates to `docopy`:
```c
if (getcopy(taskptr, &docisa, &vsa, &localspecset)
&&  docopy(taskptr, &docisa, &vsa, localspecset))
    putcopy(taskptr);
```

No interleaving, no alternative path.

---

### What `insertspanf(DOCISPAN)` Does

`insertspanf` [spanf1.c:15–54]:
1. Computes `crumorigin.dsas[ORGLRANGE]` = `prefixtumbler(docisa, DOCISPAN=4, ...)` [line 22] — this encodes the target document's ISA in the ORGL dimension with span-type prefix `4`.
2. For each I-span in `ispanset`, sets `crumorigin.dsas[SPANRANGE]` = the I-address and calls `insertnd` [line 51] to insert a crum into the spanfilade.
3. **Always returns `TRUE`** [line 53], including if `sporglset` is empty.

`finddocscontainingsp` [spanf1.c:151–188] queries this index by:
- Setting `docspace.stream` = DOCISPAN (= 4) via `tumblerincrement(..., 0, DOCISPAN, ...)` [line 168]
- Calling `retrieverestricted(spanf, &docspace, ORGLRANGE, ispanset, SPANRANGE, ...)` [line 171] for each I-span

This directly reads the crums written by `insertspanf` in `docopy`. The target document is discoverable **immediately** after the `copy` call returns.

---

### The APPEND Contrast

`doappend` [do1.c:25–32] reads:

```c
return (appendpm (taskptr, docptr, textset)/*&&
   appendpm includes insertspanf!  insertspanf(taskptr,spanf,docptr,textset,DOCISPAN)*/
);
```

The `insertspanf` call is **commented out** in `doappend`. The author's inline note "appendpm includes insertspanf!" is the justification. Tracing the chain: `appendpm` [orglinks.c:17–27] → `doinsert` [do1.c:87–123] → `docopy` [do1.c:45–65] → `insertspanf`. So the DOCISPAN call *does* happen via `docopy` even for APPEND, but the code comment and the omission in `doappend` itself create the misleading impression of a gap. Finding 0036 documents this surface reading.

---

### Edge Cases That Could Suppress the DOCISPAN Entry

The only scenarios where `insertspanf` is not reached in `docopy` are:

1. **`specset2ispanset` fails** [do1.c:54] — the source V-address can't be resolved to I-addresses (e.g., document not open, invalid V-address). The entire operation fails; `docopy` returns FALSE.
2. **`findorgl` fails** [do1.c:55] — the target document doesn't exist or isn't open for write (`WRITEBERT`). Copy fails entirely.
3. **`insertpm` fails** [do1.c:60] — `insertpm` returns FALSE if `vsaptr` is zero [orglinks.c:86–91]. Copy fails entirely.
4. **`ispanset` is empty** — `insertspanf` iterates over `sporglset` [spanf1.c:25]; if the list is empty (e.g., source V-spans resolve to zero I-spans), the loop never executes. `insertspanf` returns TRUE but no crum is inserted. This is a vacuous copy (nothing was placed in the POOM by `insertpm` either), not a partial success.

In none of these cases does `insertpm` succeed while `insertspanf` is skipped. There is no "half-written" state analogous to INSERT writing content to the granfilade but APPEND failing to register it in the spanfilade. The `&&` chain in `docopy` is structurally correct: `insertpm` and `insertspanf` are both required steps, both in the same chain, with no alternative execution path that could omit the second.

---

### Conclusion

After a successful `copy` placing content at V-position `v` in the target document, `find_documents_containing` **immediately** returns the target document for those I-addresses. The DOCISPAN entry is created by `insertspanf` [do1.c:62] as the final step of `docopy`, in a single atomic operation within one FEBE request [bed.c event loop]. There is no scenario analogous to APPEND's missing call where the POOM is updated but the spanfilade index is not.
