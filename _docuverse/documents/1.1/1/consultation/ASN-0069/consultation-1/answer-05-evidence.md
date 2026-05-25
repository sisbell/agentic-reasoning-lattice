## Question 5 [evidence]

> Does `docreatenewversion` install V-positions in `d_new` that are literally equal as tumblers to the source's content-subspace V-positions, with literally equal I-addresses at each position — or does the V-span extraction via `retrievedocumentpartofvspanpm` rebase, renumber, or otherwise transform V-positions in the new version's arrangement?

## KB Synthesis

## Answer

The V-positions are **literally preserved** — no rebasing, renumbering, or transformation occurs.

**Mechanism:**

`docreatenewversion` calls `doretrievedocvspanfoo`, which delegates to `retrievedocumentpartofvspanpm`. That function reads `cdsp.dsas[V]` (the root's minimum V-address in the text subspace, e.g. `1.1`) and `cwid.dsas[V]` (the width) directly from the source POOM root [ST-VERSION-CREATE Finding 0043]. This vspan is passed to `docopyinternal`, which calls `specset2ispanset` against the *source* document's POOM to convert V-positions → I-addresses, then calls `insertpm` into the (empty) new document [ST-VERSION Finding 0077].

Because the new document is empty, `insertpm` installs each POOM entry at the V-address derived from the source's vspan start — no existing entries exist to shift [ST-INSERT Finding 0052, ST-INSERT Finding 0066]. The result: d_new's POOM contains `(V-tumbler, I-address)` pairs with V-tumblers identical to the source's text-subspace entries and the same I-addresses.

**Observable confirmation:**

- Version vspanset immediately after creation shows `at 1.1 for 0.15` — matching the source text structure [ST-VERSION-CREATE Finding 0043]
- Finding 0032 describes the operation as "equivalent to a full-document vcopy into a new document" — vcopy preserves V-positions when source start equals destination start
- `compare_versions(source, version)` reports all content as shared at matching V-positions in both documents [ST-VERSION-CREATE Finding 0007, INV-TRANSITIVE-IDENTITY]

**What is NOT copied:** The link subspace (internal `2.x` V-positions) is excluded because `retrievedocumentpartofvspanpm` returns only the text-subspace displacement/width, leaving link entries structurally outside the copied vspan [ST-VERSION-CREATE Findings 0043, 0046].

---

## Code Exploration

I now have the complete picture. Here is the full answer.

---

## Does `docreatenewversion` Preserve V-positions and I-addresses Literally?

**Short answer: Yes — V-positions are literally equal, I-addresses are literally equal. No rebasing or renumbering occurs.** Here is the full trace.

---

### Call chain

```
docreatenewversion          [do1.c:260]
  doretrievedocvspanfoo     [do1.c:301]
    retrievedocumentpartofvspanpm  [orglinks.c:155]
  docopyinternal            [do1.c:66]
    specset2ispanset        [do2.c:14]
      vspanset2ispanset     [orglinks.c:397]
        permute             [orglinks.c:404]
          span2spanset      [orglinks.c:425]
            retrieverestricted  [retrie.c:56]
            context2span        [context.c:176]
    findorgl / acceptablevsa
    insertpm                [orglinks.c:75]
    insertspanf
```

---

### Step 1 — Extract source V-positions raw, no transform

`doretrievedocvspanfoo` [do1.c:301] calls `retrievedocumentpartofvspanpm` [orglinks.c:155]:

```c
bool retrievedocumentpartofvspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{ /* this is a kluge*/
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);   // source V-start
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);    // source V-width
    return (TRUE);
}
```

[orglinks.c:157–161] This reads `cdsp.dsas[V]` and `cwid.dsas[V]` from the source document's root orgl node — the literal V-displacement and V-width stored in the POOM root crum. These are the source's actual V-space coordinates, unmodified.

---

### Step 2 — Build vspec referencing source doc and source V-span

Back in `docreatenewversion` [do1.c:285–293]:

```c
vspec.next = NULL;
vspec.itemid = VSPECID;
movetumbler(isaptr, &vspec.docisa);     // source document's ISA
vspec.vspanset = &vspan;               // V-span from source root crum

docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
```

`&vspan.stream` — the source's V-start — is passed as `vsaptr` to `docopyinternal`. This becomes the V-address at which content is installed in `d_new`.

---

### Step 3 — `specset2ispanset`: V-positions in source → I-addresses

`docopyinternal` [do1.c:66] calls `specset2ispanset` [do2.c:14] which, for a `VSPECID` spec, calls:

```c
findorgl(taskptr, granf, &((typevspec*)specset)->docisa, &docorgl, type)
&&
(ispansetptr = vspanset2ispanset(taskptr, docorgl, ((typevspec*)specset)->vspanset, ispansetptr))
```

[do2.c:35–36] — it looks up the **source** document's orgl and calls `vspanset2ispanset` on the source's V-span.

`vspanset2ispanset` [orglinks.c:397] calls `permute` [orglinks.c:404] → `span2spanset` [orglinks.c:425] → `retrieverestricted` [retrie.c:56] → `context2span` [context.c:176].

`context2span` extracts the I-span from each matching POOM leaf crum in the **source** document:

```c
movetumbler(&restrictionspanptr->stream, &lowerbound);
tumbleradd(&lowerbound, &restrictionspanptr->width, &upperbound);
prologuecontextnd(context, &grasp, &reach);
// clamp grasp/reach to [lowerbound, upperbound] in V, propagate clamp to I
movetumbler(&grasp.dsas[idx2], &foundspanptr->stream);   // I-address
tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width); // I-width
```

[context.c:186–211] The output I-spans carry the exact I-addresses from the source's POOM leaf crums. These are the unmodified global istorage addresses of the source content.

---

### Step 4 — `insertpm`: installs those I-addresses in `d_new` at source's V-positions

`insertpm` [orglinks.c:75] receives:
- `vsaptr = &vspan.stream` = source's V-start
- `sporglset` = the I-spans extracted from source

For each I-span:

```c
movetumbler(vsaptr, &crumorigin.dsas[V]);       // V-origin = source V-start
shift = tumblerlength(vsaptr) - 1;
inc = tumblerintdiff(&lwidth, &zero);           // I-width as integer
tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V]);   // V-width
insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr);  // advance for next crum
```

[orglinks.c:113–131]

- `crumorigin.dsas[V]` starts at the source's literal `cdsp.dsas[V]` value.
- `crumorigin.dsas[I]` (packed into `linfo` via `unpacksporgl`) is the I-address extracted from the source's own POOM crum — unmodified.
- V-width is computed as: I-width expressed at digit level `shift = tumblerlength(vsaptr) - 1`. Because `vsaptr` starts at the source's own V-start, `shift` is the same digit level used when that content was originally inserted into the source. So V-widths match.
- For each subsequent I-span, `vsaptr` is advanced by the V-width of the previous crum, placing subsequent crums at the same V-positions they occupied in the source.

`acceptablevsa` [do2.c:110] is a stub that always returns `TRUE` — no validation that could perturb positions.

---

### Conclusion

`docreatenewversion` installs V-positions in `d_new` that are **literally equal as tumblers** to the source's content-subspace V-positions:

1. **V-start is literal**: `retrievedocumentpartofvspanpm` [orglinks.c:159] copies `cdsp.dsas[V]` from the source's root crum directly into `vspan.stream`, which flows unchanged into `vsaptr` in `insertpm` [orglinks.c:113].

2. **I-addresses are literal**: `specset2ispanset` → `context2span` [context.c:206] extracts raw I-addresses from the source's own POOM leaf crums. These are placed into `crumorigin.dsas[I]` in `d_new` without arithmetic modification.

3. **No rebasing, renaming, or renumbering**: there is no subtraction of a "document base address," no per-version offset, no remapping to a local coordinate system. The source's V-addresses propagate as-is.

4. **One conditional subtlety**: V-widths in `d_new` are reconstructed from I-widths via `tumblerincrement(..., shift, inc, ...)` [orglinks.c:117], not copied directly from the source's `cwid.dsas[V]`. If the source had crums with V-widths expressed at different digit levels than `shift = tumblerlength(vspan.stream) - 1`, the reconstructed widths would differ. In practice, for uniformly-inserted content all at the same digit level, the widths match and the mapping is point-for-point identical.
