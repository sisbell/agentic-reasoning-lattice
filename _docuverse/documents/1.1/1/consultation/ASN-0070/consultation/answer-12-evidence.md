## Question 12 [evidence]

> During I→V conversion via `span2spanset`, what is the exact filtering rule that drops "unreferenced" I-addresses (DEL5) — does it test membership in the target document's POOM only, or scan all open documents?

## KB Synthesis

## I→V Filtering in `span2spanset`: Single-Document POOM Only

The filtering rule tests membership in **the single specified document's POOM only** — it does not scan all open documents.

### The Mechanism

From `[SS-FOLLOWLINK]` (Finding 0048), the call chain is:

```
link2sporglset()          — extracts I-addresses from link orgl (no POOM check here)
  ↓
linksporglset2specset()   — converts I-addresses → V-specs via a specified document
  ↓
span2spanset()            — calls retrieverestricted() against that document's orgl
  ↓
retrieverestricted()      — if NULL returned, I-address silently dropped (orglinks.c:446-448)
```

The drop condition is: `retrieverestricted()` returns NULL when the I-address has no V-position mapping in **that specific document's POOM**. The document in question is the `homedoc` parameter passed to FOLLOWLINK, or the querying document's docid for RETRIEVEENDSETS (`[SS-RETRIEVE-ENDSETS]`).

### Which Document?

- **FOLLOWLINK**: uses the `homedoc` parameter (`dofollowlink()` at `do1.c:227-236`). Postcondition: `followlink(link, whichend, homedoc) = { v | ∃ i ∈ endset(link, whichend) : poom.homedoc(v) = i }` — explicitly scoped to `homedoc`.
- **RETRIEVEENDSETS**: uses the querying document's docid for the `linksporglset2specset()` call (`[SS-RETRIEVE-ENDSETS]`).

### Implication: DEL5 Mismatch

`[EC-GHOST-LINK]` defines DEL5 as `unreferenced(a) ≡ a ∈ dom.ispace ∧ ¬(∃d, v : poom.d(v) = a)` — truly absent from *all* POOMs. But `span2spanset` applies a **weaker, document-local** test: an I-address is filtered if absent from the *queried* document's POOM, regardless of whether it exists in other documents' POOMs. This means the same I-address can produce a V-span when queried from Document A (where it has a mapping) and produce nothing when queried from Document B (where it doesn't), even though it is globally "referenced" in the DEL5 sense.

`[INV-ITOV-FILTERING]` states this as the universal invariant: `∀ op returning V-addresses: v ∈ result(op) → ∃ i : poom.queried_doc(v) = i` — the filter is always single-document-scoped.

---

## Code Exploration

I now have everything needed to answer definitively. Here is the complete trace.

---

## I→V Filtering at `span2spanset`: The DEL5 Drop Rule

### Call Chain

```
linksporglset2vspec()           [sporgl.c:127]
  sporglset2vspanset()          [sporgl.c:141]
    findorgl(granf, homedoc, &orgl)  [sporgl.c:152]
    ispan2vspanset(orgl, ispan) [sporgl.c:157]
      permute(orgl, ispanptr, I, V)  [orglinks.c:393]
        span2spanset(orgl, span, I, V)     [orglinks.c:415]
          retrieverestricted(orgl, span, I, NULL, V, NULL)  [orglinks.c:435]
            retrieveinarea(...)         [retrie.c:83]
              findcbcinarea2d(...)      [retrie.c:97]
                crumqualifies2d(...)   [retrie.c:253]
```

---

### Step 1: Which POOM is searched?

`sporglset2vspanset` [sporgl.c:152] calls:

```c
(void) findorgl (taskptr, granf, homedoc/*&sporglptr->sporgladdress*/, &orgl, type);
```

`homedoc` is the ISA of the **specific target document**. `findorgl` retrieves that document's single POOM from `granf`. The resulting `orgl` is then passed all the way down to `retrieverestricted` as `fullcrumptr` [retrie.c:83].

**Answer to the scope question: only the target document's POOM is searched.** No other open documents are touched.

---

### Step 2: What does `retrieverestricted` do with `docisaptr`?

At `orglinks.c:435`:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                             (typespan*)NULL, targindex, (typeisa*)NULL);
```

The sixth argument — `docisaptr` — is **always `NULL`**. In `retrieverestricted` [retrie.c:77–82]:

```c
if (docisaptr) {
    movetumbler(docisaptr, &info.homedoc);
    infoptr = &info;
} else {
    infoptr = NULL;
}
```

Since `docisaptr = NULL`, `infoptr = NULL`.

---

### Step 3: The `homedoc` check is dead code in production

`findcbcinarea2d` [retrie.c:244–251]:

```c
#ifndef DISTRIBUTION
if(infoptr){
    fprintf(stderr,"not NULL infoptr versions mumble ...\n");
    gerror("findcbcinarea2d");
}
#else
    if (infoptr)
        gerror("!NULL");     /* production: crash if infoptr != NULL */
#endif
```

Passing `infoptr != NULL` **crashes** the production backend. The `homedoc` filter was designed but never enabled — it is permanently unreachable in this call path.

---

### Step 4: The actual filtering — `crumqualifies2d`

[retrie.c:270–305]:

```c
bool crumqualifies2d(typecorecrum *crumptr, typedsp *offset,
    tumbler *span1start, tumbler *span1end, INT index1,
    tumbler *span2start, tumbler *span2end, INT index2,
    type2dbottomcruminfo *infoptr)
{
    if ((crumptr->height == 0) && infoptr &&
        !tumblereq(&infoptr->homedoc, &(((type2dcbc*)crumptr)->c2dinfo.homedoc)))
        return (FALSE);                        /* line 274 — NEVER reached */

    /* Span1 (I dimension) intersection test */
    endcmp = iszerotumbler(span1end) ? TOMYRIGHT
           : whereoncrum(crumptr, offset, span1end, index1);
    if (endcmp <= ONMYLEFTBORDER) return(FALSE);       /* line 283 */
    startcmp = whereoncrum(crumptr, offset, span1start, index1);
    if (startcmp > THRUME) return(FALSE);              /* line 287-289 */

    /* Span2 (V dimension) — span2end=zero → iszerotumbler=TRUE → endcmp=TOMYRIGHT */
    endcmp = iszerotumbler(span2end) ? TOMYRIGHT
           : whereoncrum(crumptr, offset, span2end, index2);  /* line 292 — always TOMYRIGHT */
    if (endcmp < ONMYLEFTBORDER) return(FALSE);
    startcmp = whereoncrum(crumptr, offset, span2start, index2); /* span2start=zero ≤ any V */
    if (startcmp > THRUME) return(FALSE);              /* never fires */

    return(TRUE);
}
```

Because `span2ptr = NULL` at the `retrieverestricted` call site, `retrieverestricted` clears `span2start/span2end` to zero [retrie.c:73–76]. Then in `crumqualifies2d`:
- `iszerotumbler(span2end) = TRUE` → `endcmp = TOMYRIGHT` → the V-dimension end check always passes.
- `span2start = zero` is less than any real V address, so `whereoncrum` returns `TOMYLEFT` or `ONMYLEFTBORDER` ≤ `THRUME` → the V-dimension start check always passes.

**The only active filter is the I-dimension geometric intersection** (lines 282–289): does the query I-span overlap the crum's I range?

---

### Step 5: Zero-result path — the silent drop

Back in `span2spanset` [orglinks.c:439–453]:

```c
context = retrieverestricted(...);
for (c = context; c; c = c->nextcontext) {
    context2span (c, ...);
    nextptr = (typespan*) onitemlist (...);
}
if (!context) {
    return(targspansetptr);   /* orglinks.c:447-448 — return without adding anything */
}
```

If no crum in the target POOM spans the query I-address, `retrieveinarea` returns `NULL`, `context = NULL`, the loop body never executes, and `span2spanset` returns the unchanged output list. **The I-address is silently dropped.**

---

### Summary: The Exact DEL5 Filtering Rule

1. **Scope — target document's POOM only.** `findorgl(granf, homedoc, &orgl)` [sporgl.c:152] obtains the orgl for the single target document. No other open documents are consulted.

2. **Mechanism — pure geometric I-span intersection.** `crumqualifies2d` tests whether the query I-span overlaps the crum's `[cdsp.dsas[I], cdsp.dsas[I] + cwid.dsas[I])` interval. No content, no type, no liveness field is checked.

3. **The `homedoc` per-crum field is dead code.** It exists in `type2dcbc.c2dinfo.homedoc` [corediskin.c:282, corediskin.c:330] and is present on 2D bottom crums in the POOM, but the only code path that would check it (`crumqualifies2d` line 274) is gated on `infoptr != NULL`, and passing `infoptr != NULL` to `findcbcinarea2d` calls `gerror` in both debug and production builds [retrie.c:245–251]. It is permanently unreachable.

4. **DEL5 unreferenced ≡ I-span maps to no crum in the target POOM.** An I-address `a` survives I→V conversion if and only if there exists a crum in the target document's POOM whose I-range covers `a`. If no such crum exists (because DELETE removed it via `deletend` [orglinks.c:149] which calls `rearrangend` [edit.c] to excise the crum), the address is dropped silently at `orglinks.c:447–448`. The spanfilade is not consulted during this drop; it is a strictly structural test against the POOM tree of the one target document.
