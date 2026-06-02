## Question 1 [evidence]

> Does `docreatenewversion` copy the source document's entire content arrangement (full POOM), or can it produce a version whose arrangement contains only a subset of the source's content addresses?

## KB Synthesis

`docreatenewversion` copies a **subset** of the source's POOM — specifically, only the text subspace (`1.x` V-positions). The link subspace (`2.x`) is excluded.

## Mechanism

The call chain is [ST-VERSION-CREATE]/Finding 0043, 0046:

```
docreatenewversion
  → doretrievedocvspanfoo
      → retrievedocumentpartofvspanpm   ← reads cdsp.dsas[V] and cwid.dsas[V]
                                            which start at text position 1, not 0
  → docopyinternal
      → insertpm (POOM, text subspace only)
      → insertspanf (DOCISPAN entries)
```

`retrievedocumentpartofvspanpm` is described in the code itself as "a kluge" — it returns the raw root node's V-dimension displacement and width, which anchors at the text subspace start. Link orgls at `2.x` sit below this displacement and are structurally outside the returned vspan.

## Precise postcondition

From [ST-VERSION-CREATE]/Finding 0043:

> `text_references(version) = text_references(original)` AND `link_references(version) = {}`

The version starts with a full copy of all text content identity from the original, but an **empty link subspace**.

## Consequence for link discovery

Despite the empty POOM link subspace, `find_links` still works on the version [ST-VERSION-CREATE]/Finding 0046, [INT-LINK-VERSION]/Finding 0046. Link discovery operates on shared I-addresses via the spanfilade, not on the POOM link subspace — the text copy is sufficient to inherit all link discoverability.

## What is NOT copied

- Link orgl references (V-positions `2.x`)
- Any content in the type-endpoint subspace (`3.x`)

[ST-VERSION]/Finding 0077 further confirms: `CREATENEWVERSION` allocates no new content I-addresses — it only allocates a new document address and copies existing text I-address spans. The content arrangement of the version is therefore a strict subset of the source: text-subspace POOM entries only.

---

## Code Exploration

## Answer: Does `docreatenewversion` Copy the Full POOM?

**Yes — definitively. `docreatenewversion` always copies the source document's complete POOM. There is no mechanism for producing a version whose arrangement contains only a subset of the source's content addresses.**

---

### Call Chain

#### Entry point: `do1.c:260`

```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr)
```

The function body (lines 260–299) does exactly four things:
1. Creates a new empty document structure via `createorglingranf` [do1.c:277]
2. Retrieves the source document's full POOM span via `doretrievedocvspanfoo` [do1.c:281]
3. Copies all content into the new version via `docopyinternal` [do1.c:293]
4. Closes the new document [do1.c:296]

---

### Step 2 — Full POOM retrieval: `doretrievedocvspanfoo` [do1.c:301]

```c
return (
   findorgl (taskptr, granf, docisaptr, &docorgl, NOBERTREQUIRED)
&& retrievedocumentpartofvspanpm (taskptr, docorgl, vspanptr) );
```

`retrievedocumentpartofvspanpm` [orglinks.c:155] extracts the V-dimension span:

```c
movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);  // [orglinks.c:159]
movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);   // [orglinks.c:160]
```

`cwid.dsas[V]` is the **entire width** of the source document in the V-dimension. No truncation, no selection — the full POOM width is captured and stored in `vspan.width`.

---

### Step 3 — Full copy: `docopyinternal` [do1.c:66]

Called at [do1.c:293] with `vsaptr = &vspan.stream` and `specset = &vspec`, where `vspec.vspanset = &vspan` holds the full source POOM [do1.c:285–288].

```c
if (!specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)) return FALSE;  // [do1.c:74]
if (!findorgl (taskptr, granf, docisaptr, &docorgl, NOBERTREQUIRED)) return FALSE;  // [do1.c:75]
if (!acceptablevsa (vsaptr, docorgl)) return FALSE;                                  // [do1.c:76]
if (!insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)) return FALSE;         // [do1.c:78]
if (!insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)) return FALSE;     // [do1.c:79]
```

#### `specset2ispanset` → `vspanset2ispanset` → `permute` [do2.c:36, orglinks.c:397, orglinks.c:404]

```c
typeispanset *vspanset2ispanset(...) {
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);  // [orglinks.c:401]
}
```

`permute` [orglinks.c:404] iterates every span in the restriction set (the full POOM width) and calls `span2spanset` [orglinks.c:415], which calls `retrieverestricted` [retrie.c:56] to extract **all I-dimension content addresses** that fall within that V-dimension range. No content is excluded.

#### `insertpm` [orglinks.c:75]

```c
for (; sporglset; sporglset = ...) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);   // [orglinks.c:101]
    ...
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // [orglinks.c:130]
    tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);       // [orglinks.c:131]
}
```

Every ispan extracted from the source POOM is inserted into the new version's POOM. The loop runs once per ispan, advances the VSA, and inserts the next — producing an exact structural copy.

#### `insertspanf` [spanf1.c:15]

```c
for (; sporglset; ...) {
    ...
    insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);  // [spanf1.c:51]
}
```

The span forest (I-address index) is also populated for every ispan — again, no filtering.

---

### Conclusion

`docreatenewversion` does **not** support selective or partial copying. The sequence is:

1. `doretrievedocvspanfoo` retrieves **`cwid.dsas[V]`** — the source document's complete V-dimension width [orglinks.c:160]
2. That full width is passed as the restriction to `vspanset2ispanset` → `permute` → `retrieverestricted`, which returns **all** I-dimension content addresses within that range [orglinks.c:401, retrie.c:56]
3. `insertpm` inserts **every** extracted ispan into the new version's POOM [orglinks.c:130]
4. `insertspanf` records **every** corresponding span reference [spanf1.c:51]

There is no code path that filters, restricts, or selects a subset of the source's content addresses during version creation. The new version's content arrangement is always a complete copy of the source document's POOM at the time of the call.
