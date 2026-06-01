## Question 1 [evidence]

> When `docreatenewversion` is invoked on a document that is itself a version with edits not present in its ancestor, does the vspan retrieval (`doretrievedocvspanfoo`) copy the immediate source's current content including those edits, or the ancestor's original content?

## KB Synthesis

`docreatenewversion` copies the **immediate source's current content, including all edits**.

The mechanism is straightforward from the KB:

**Step 2 reads current POOM state.** `doretrievedocvspanfoo` delegates to `retrievedocumentpartofvspanpm`, which reads `cdsp.dsas[V]` and `cwid.dsas[V]` directly from the source document's POOM root node [ST-VERSION-CREATE, Finding 0043]. The POOM is mutable and reflects all prior INSERT/DELETE/REARRANGE operations in-place [SS-POOM-MUTABILITY]. There is no reference back to any ancestor state.

**Version isolation is per-document.** Each document — including versions-of-versions — has its own independent POOM tree [FC-VERSION-ISOLATION]. Edits applied to the intermediate version modified only that version's POOM, leaving all other documents untouched. So when `docreatenewversion` is called on it, the POOM it reads is that version's current edited state.

**Step 3 copies those I-addresses.** `docopyinternal` calls `specset2ispanset` against the source's current POOM to resolve V-spans to I-addresses, then `insertspanf` records them in the new document [ST-VERSION, Finding 0077]. The result: `references(new_version) = references(source_at_call_time)` [ST-VERSION-CREATE, Finding 0032].

The ancestor's original content is not consulted at any point. There is no "original state" pointer — only the current POOM, which is the authoritative representation of a document's text content.

---

## Code Exploration

I now have the full picture. Here is my answer.

---

## Answer: `docreatenewversion` copies the immediate source's **current** content, including its edits

Every claim below is traced from actual source lines.

---

### The call chain in `docreatenewversion` [do1.c:260–299]

```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr)
```

`isaptr` is the source document. The new version (`newisaptr`) is a blank orgl created at [do1.c:277]. Then:

**Line 281:**
```c
if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) { return FALSE; }
```

`isaptr` is passed directly as the document to retrieve from — it is the **immediate source**, not any ancestor.

**Lines 285–293:**
```c
vspec.next = NULL;
vspec.itemid = VSPECID;
movetumbler(isaptr, &vspec.docisa);   // docisa = the source document's ISA
vspec.vspanset = &vspan;

addtoopen(newisaptr, user, TRUE, WRITEBERT);
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
```

The `vspec` holds a reference to `isaptr` as the doc to query, paired with the vspan returned from `doretrievedocvspanfoo`.

---

### What `doretrievedocvspanfoo` actually returns [do1.c:301–309]

```c
bool doretrievedocvspanfoo(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{ /* this routine is a kluge not yet kluged */
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, NOBERTREQUIRED)
    && retrievedocumentpartofvspanpm (taskptr, docorgl, vspanptr) );
}
```

`findorgl` opens `isaptr`'s POOM (the source document's current enfilade tree). Then `retrievedocumentpartofvspanpm` is called on that orgl.

---

### What `retrievedocumentpartofvspanpm` reads [orglinks.c:155–162]

```c
bool retrievedocumentpartofvspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{ /* this is a kluge */
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);  // line 159
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);   // line 160
    return (TRUE);
}
```

This reads directly from the **root crum** of the POOM enfilade:
- `cdsp.dsas[V]` — the V-space displacement (starting address) of the root crum
- `cwid.dsas[V]` — the V-space width of the root crum

(`V` is defined as index `1` in `wisp.h:20`, i.e., the virtual-address dimension of the POOM.)

The root crum is a **bounding node** maintained live by the enfilade machinery.

---

### How edits update the root crum: `setwispnd` [wisp.c:171–228]

Every call to `insertpm` → `insertnd` → `setwispupwards` propagates changes up to the root via `setwisp` → `setwispnd` [wisp.c:130–131]:

```c
case POOM:
    return (setwispnd ((typecuc*)ptr));
```

`setwispnd` computes a fresh bounding box by scanning all children [wisp.c:207–215]:

```c
for (ptr = findleftson (father); ptr; ptr = getrightbro (ptr)) {
    lockadd((tumbler*)&ptr->cdsp, (tumbler*)&ptr->cwid,
            (tumbler*)&tempwid, (unsigned)widsize(ptr->cenftype));
    lockmax((tumbler*)&newwid, (tumbler*)&tempwid,
            (tumbler*)&newwid, (unsigned)widsize(ptr->cenftype));
}
```

And writes the result back [wisp.c:224–225]:
```c
movewisp (&newdsp, &father->cdsp);
movewisp (&newwid, &father->cwid);
```

Therefore: after each insert (each `doinsert` or `docopy` call on the source document), the root crum's `cwid.dsas[V]` is updated to span the new maximum V-address. **All edits the source has accumulated are captured in the root crum's current `cwid`.**

---

### How `docopyinternal` uses the vspec [do1.c:66–82]

```c
bool docopyinternal(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    if (!specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)) return FALSE;
    ...
    if (!insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)) return FALSE;
```

`specset2ispanset` [do2.c:14–46] processes the `vspec` it received, which holds `docisa = isaptr`. It calls:

```c
findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
&& (ispansetptr = vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr))
```

[do2.c:35–36]

This opens `isaptr`'s POOM **a second time** and calls `vspanset2ispanset` → `permute` [orglinks.c:404] to translate the V-span into I-spans. The traversal uses `isaptr`'s current POOM state, so every crum that was added by later edits is consulted. The resulting ispans represent the complete set of permanent storage addresses (`I`-addresses) currently mapped by `isaptr`.

Those ispans are then inserted into the new version's POOM via `insertpm` [do1.c:78].

---

### Notable implementation detail: both "kluge" functions are identical

`retrievedocumentpartofvspanpm` and `retrievevspanpm` have identical bodies [orglinks.c:155–172]:

```c
bool retrievedocumentpartofvspanpm(...) { /* this is a kluge */
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
}

bool retrievevspanpm(...) {
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
}
```

The name "document part" implies the original design intent was to return only the text subspace (V ≥ 1.0), excluding the link metadata region (V < 1.0). That distinction was never implemented — both functions return the full V-bounding-box of the root crum. This is what the comment "kluge not yet kluged" [do1.c:302] refers to.

---

### Conclusion

`docreatenewversion` copies the **immediate source's current content, including all edits** made to it since it was created. It does **not** use the ancestor's original content. Here is why:

1. `doretrievedocvspanfoo` [do1.c:281] reads `isaptr`'s root crum via `retrievedocumentpartofvspanpm` [orglinks.c:159–160], which returns the root crum's live `cdsp.dsas[V]` / `cwid.dsas[V]`.

2. The root crum's `cwid.dsas[V]` is maintained as a bounding box over all inserted child crums by `setwispnd` [wisp.c:207–225], propagated after every `insertnd` via `setwispupwards`. Post-ancestor edits expand this bounding box.

3. The `vspec` passed to `docopyinternal` [do1.c:293] carries `docisa = isaptr`, so the V→I permutation in `specset2ispanset` [do2.c:35–36] traverses `isaptr`'s **current** POOM — the one that includes all edits.

4. The resulting I-spans (covering all content in `isaptr` right now) are installed into the new version's POOM via `insertpm`.

There is no ancestry walk, no snapshot of an earlier state, and no reference to anything beyond the source document's live in-memory (or on-disk-loaded) POOM tree at the moment `docreatenewversion` is called.
