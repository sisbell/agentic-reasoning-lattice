## Question 11 [gregory]

> When a link's source endset spans I-addresses `[i, i+5)` and a DELETE removes the content at `[i+2, i+4)` from the only document containing it, does `RETRIEVEENDSETS` for that link still return the full original I-span `[i, i+5)`, or does it return only the portions `[i, i+2)` and `[i+4, i+5)` that remain reachable through some POOM?

## KB Synthesis

## Answer

`RETRIEVEENDSETS` returns only the two surviving portions — not the full original span. Here is the reasoning:

**What the spanfilade retains (permanently)**

The link's source endset was indexed in the spanfilade when the link was created. That entry covers I-addresses `[i, i+5)`. Because the spanfilade is write-only [INV-SPANF-WRITE-ONLY], the entry persists after DELETE. The granfilade content bytes at those I-addresses also persist permanently [INV-IADDR-IMMUTABILITY].

**What DELETE actually changes**

DELETE operates only on the target document's POOM [ST-DELETE, FC-GRANF-ON-DELETE]. It calls `deletend`, which frees the bottom crums mapping I-addresses `[i+2, i+4)` to V-positions via `disown` + `subtreefree`. Since this was the *only* document containing those I-addresses, those I-addresses are now unreferenced in any POOM anywhere. The spanfilade entry is unchanged.

**The I-to-V conversion filter**

Both FOLLOWLINK and RETRIEVEENDSETS share the same I-to-V conversion path: `linksporglset2specset()` → `span2spanset()` → `retrieverestricted()` [INV-ITOV-FILTERING, SS-FOLLOWLINK]. At `span2spanset()`, `retrieverestricted()` searches the target document's POOM for each I-address. When it returns NULL (no POOM entry), the I-address is **silently dropped** — no V-span is generated, no error is raised [SS-FOLLOWLINK, Finding 0048].

For the surviving portions `[i, i+2)` and `[i+4, i+5)`, the POOM still has valid mappings (those bytes were not deleted), so they convert successfully to V-spans.

**Result**

RETRIEVEENDSETS returns **two separate V-spans** corresponding to `[i, i+2)` and `[i+4, i+5)` — not the original single contiguous span. The deleted middle portion is silently absent. This is precisely the partial survival mechanism documented in [EC-LINK-PARTIAL-SURVIVAL]: "each I-span in a link endset independently tracks its content, so partial survival is possible."

The formal statement from [INV-ITOV-FILTERING] governs this: `∀ op returning V-addresses: v ∈ result(op) → ∃ d, i : poom.d(v) = i`. Since no POOM in any document maps `[i+2, i+4)` to any V-position, no V-address for that range can appear in the result.

---

## Code Exploration

Now I have all the pieces. Let me compile the definitive answer.

---

## Answer

**`RETRIEVEENDSETS` returns only the surviving portions `[i, i+2)` and `[i+4, i+5)` — not the full original I-span `[i, i+5)`.** The deleted gap `[i+2, i+4)` vanishes from the result because the I→V conversion step uses the current POOM state, and the deleted content has no V-position mapping anywhere.

Here is the complete traced execution.

---

### Step 0: The Critical Misread of the API

The first thing to clarify: `RETRIEVEENDSETS` does **not** take a link ISA as its argument. It takes a **content specset** — a document region. `getretrieveendsets` [get1.c:185–188] just calls `getspecset`, and the golden tests confirm this:

```python
doc_span = SpecSet(VSpec(source_opened, [Span(Address(1, 1), Offset(1))]))
session.retrieve_endsets(doc_span)   # whole-document V-span, not link address
```

This means: "find all link endsets that overlap this document region." The specset is converted to I-spans through the current POOM before the spanfilade is queried.

---

### Step 1: What DELETE Does (and Doesn't Do)

`dodeletevspan` [do1.c:158–167]:
```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr) {
    return (
       findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm(taskptr, docisaptr, docorgl, vspanptr)
    /*&& TRUE*/ /* ht stuff */ );
}
```

`deletevspanpm` [orglinks.c:145–152]:
```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr) {
    if (iszerotumbler(&vspanptr->width)) return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

DELETE calls `deletend` only on the **document's POOM** (in `granf`). It removes the V→I mapping for `[i+2, i+4)`. The link's endset entry in the **spanfilade** is never touched — no `deletespanf` function exists anywhere in `spanf1.c` or `spanf2.c` (confirmed by Finding 0057).

**After DELETE:**
- Document POOM: maps V-positions to `[i, i+2)` and `[i+4, i+5)`. The gap `[i+2, i+4)` has no V-mapping.
- Spanfilade: still contains the link endset crum `ORGLRANGE = 1.L` (LINKFROMSPAN + link ISA L), `SPANRANGE = [i, i+5)`.

---

### Step 2: RETRIEVEENDSETS Entry Point

`retrieveendsets` [fns.c:350–362] → `doretrieveendsets` [do1.c:369–374] → `retrieveendsetsfromspanf` [spanf1.c:190–235].

---

### Step 3: The Spanfilade Query

Inside `retrieveendsetsfromspanf`, three things happen:

**3a. Convert the query specset to I-spans** via `specset2sporglset` [sporgl.c:14–33]:

```c
specset2sporglset(taskptr, specset, &sporglset, NOBERTREQUIRED)
```

For a VSPEC like `(doc_D, V-range)`, this calls `vspanset2sporglset` [sporgl.c:35–65], which calls `vspanset2ispanset` → `permute` on the document's POOM to get the I-spans currently accessible in that V-range.

After the DELETE, the document's POOM maps the queried V-region to only **`[i, i+2)` and `[i+4, i+5)`** — the gap `[i+2, i+4)` produces nothing.

So `sporglset` contains two entries: sporglorigin=`i`, sporglwidth=`2` and sporglorigin=`i+4`, sporglwidth=`1`.

**3b. Search the spanfilade** via `retrievesporglsetinrange` [spanf1.c:237–267]:

```c
context = retrieverestricted((typecuc*)spanf, (typespan*)sporglptr, SPANRANGE,
                              whichspace, ORGLRANGE, (typeisa*)NULL);
```

Where `whichspace` = `{stream.mantissa[0]=LINKFROMSPAN=1, width.mantissa[0]=1}` = ORGLRANGE range `[1.0…, 2.0…)`.

The spanfilade crum for link L's from-endset has:
- `ORGLRANGE = prefixtumbler(L, LINKFROMSPAN)` = `1.L` — **within `[1.0…, 2.0…)` ✓**
- `SPANRANGE = [i, i+5)`

Does `[i, i+5)` overlap `[i, i+2)` (first query)? **Yes** — intersection `[i, i+2)`.  
Does `[i, i+5)` overlap `[i+4, i+5)` (second query)? **Yes** — intersection `[i+4, i+5)`.

The crum qualifies both times (via `crumqualifies2d` [retrie.c:270–305]). The link L is found.

**3c. Extract the full crum range** via `contextintosporgl` [sporgl.c:205–220]:

```c
contextintosporgl((type2dcontext*)c, (tumbler*)NULL, sporglset, SPANRANGE);
// -> sporglptr->sporglorigin = context->totaloffset.dsas[SPANRANGE] = i
// -> sporglptr->sporglwidth  = context->contextwid.dsas[SPANRANGE]  = 5
```

`fromsporglset` gets the **full** endset range: `sporglorigin=i`, `sporglwidth=5` = `[i, i+5)`. The spanfilade returns the stored crum's complete range, not an intersection of it with the query.

---

### Step 4: I→V Conversion Filters the Deleted Gap

`linksporglset2specset` [sporgl.c:97–123] → `sporglset2vspanset` [sporgl.c:141–176] → `ispan2vspanset` [orglinks.c:389–394]:

```c
typevspanset *ispan2vspanset(..., typeorgl orgl, typeispan *ispanptr, typevspanset *vspansetptr) {
    return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
}
```

`permute` [orglinks.c:404–422] calls `span2spanset` which calls `retrieverestricted` on the document's POOM with the I-span `[i, i+5)` in the I-dimension to find corresponding V-spans.

The document's POOM after DELETE:
- V→I: some V-range A maps to `[i, i+2)`
- V→I: some V-range B maps to `[i+4, i+5)`
- `[i+2, i+4)` → **no V-mapping** (removed by `deletend`)

`permute` walks the POOM and finds crums overlapping `[i, i+5)` in the I-dimension. It returns:
- V-range A (for `[i, i+2)`)
- V-range B (for `[i+4, i+5)`)
- **Nothing** for `[i+2, i+4)` — no crum exists for it.

---

### Step 5: Observed Behavior (Golden Test Confirmation)

`golden/endsets/endsets_after_source_delete.json` records the analogous experiment (deleting from the *beginning* of a linked region rather than the middle, producing one surviving span rather than two):

```json
"before": { "spans": [{ "start": "1.7", "width": "0.10" }] },
"after":  { "spans": [{ "start": "1.7", "width": "0.4"  }] }
```

Link was on "right here" (10 chars). DELETE removed "right " (6 chars). The endset shrunk to only "here" (4 chars). The deleted content simply vanishes from the endset — the link does not "break" but does contract.

For a **middle** deletion (`[i+2, i+4)` removed from `[i, i+5)`), the same mechanism produces **two disjoint spans** rather than one: the link is not broken but is split, exactly as Finding 0019 §3 ("Pivot Operations Fragment Link Endsets") shows for rearrangements.

---

### Summary of the Call Chain

```
RETRIEVEENDSETS(doc_V_span)
  fns.c:350    retrieveendsets()
  do1.c:373    doretrieveendsets() -> retrieveendsetsfromspanf()
  spanf1.c:222   specset2sporglset(doc_V_span)
                   sporgl.c:48  vspanset2ispanset() via doc POOM
                   -> after delete: I-spans = [i,i+2) + [i+4,i+5)
  spanf1.c:223   retrievesporglsetinrange(I-spans, LINKFROMSPAN)
                   retrie.c:56  retrieverestricted(spanf, SPANRANGE=[i,i+2), ORGLRANGE=1.*)
                     -> finds crum: SPANRANGE=[i,i+5), ORGLRANGE=1.L  [OVERLAP]
                   retrie.c:56  retrieverestricted(spanf, SPANRANGE=[i+4,i+5), ORGLRANGE=1.*)
                     -> finds same crum again
                   -> fromsporglset = {origin=i, width=5} (full endset, unrestricted)
  spanf1.c:224   linksporglset2specset(homedoc, fromsporglset=[i,i+5))
                   sporgl.c:157  ispan2vspanset([i,i+5), doc_POOM)
                     orglinks.c:393  permute(POOM, [i,i+5), I->V)
                     -> [i,i+2)   maps to V-range A  [EXISTS in POOM]
                     -> [i+2,i+4) maps to nothing     [DELETED, absent from POOM]
                     -> [i+4,i+5) maps to V-range B  [EXISTS in POOM]
  RESULT: two V-spans — V-range A and V-range B
```

---

### Conclusion

`RETRIEVEENDSETS` returns **`[i, i+2)` and `[i+4, i+5)` expressed as V-addresses** — the portions that remain reachable through the document's current POOM. It does **not** return the full original I-span `[i, i+5)`.

The mechanism is:
1. **The spanfilade is never cleaned up** (`insertspanf` has no inverse; `dodeletevspan` [do1.c:158–167] touches only the POOM via `deletend` [orglinks.c:149]). The full `[i, i+5)` endset crum persists.
2. **The query converts the caller's content to current I-spans** via `vspanset2ispanset` on the live POOM. After deletion, only `[i, i+2)` and `[i+4, i+5)` are returned from the POOM — the gap produces nothing.
3. **Both surviving fragments overlap the stored crum** `[i, i+5)` → the link is found.
4. **The returned full crum `[i, i+5)` is then converted back to V-spans** via `ispan2vspanset` on the same live POOM. The gap `[i+2, i+4)` has no V-position anywhere → it is absent from the result.

The link survives the delete. Its endset adapts to reflect only the currently accessible content. The deleted content is simply invisible — no V-position for it exists in any POOM.
