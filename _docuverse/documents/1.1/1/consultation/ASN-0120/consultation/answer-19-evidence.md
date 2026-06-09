## Question 19 [evidence]

> Once created, can a link's recorded endset I-addresses ever be mutated by any subsequent operation, or are the endsets permanently frozen at the I-addresses captured at creation time (independent of later V-position shifts of the referenced content)?

## KB Synthesis

The endset I-addresses are **permanently frozen at creation time**. No subsequent operation can mutate them.

**The stored representation is I-space sporgls, not V-spans.**

When `domakelink` is called with V-span inputs, `vspanset2sporglset` immediately converts them to sporgls (each carrying an `sporglorigin` I-address, a width, and a source-document ISA) [SS-SPORGL, ST-LINK-CREATE]. These sporgls are written into the link orgl in I-space and never touched again.

`link2sporglset` — the extraction path used by FOLLOWLINK — calls `retrieverestricted` against the link orgl directly to read those stored I-addresses [SS-FOLLOWLINK]. No POOM check occurs during extraction; the I-addresses come straight from the link orgl.

The three-layer model makes this explicit [SS-THREE-LAYER-MODEL]:

> I-space (link orgl): Cannot be deleted. No operation removes from I-space.

No document operation — INSERT, DELETE, REARRANGE, DELETEVSPAN(2.x) — touches the link orgl [FC-LINK-PERSISTENCE, FC-LINK-DELETE-ISOLATION]. There is no DELETELINK or MODIFYLINK operation in the protocol [INV-LINK-PERMANENCE].

**The apparent dynamism in endset V-addresses is entirely a query-time artifact.** When FOLLOWLINK reports that "here" moved from V 1.7 to V 1.13 after an insert [INV-LINK-CONTENT-TRACKING], it is not reading updated storage — it is taking the frozen I-addresses from the link orgl and feeding them through `linksporglset2specset`, which looks them up in the *current* POOM to compute present V-positions [SS-FOLLOWLINK]. The stored I-addresses are the same before and after; only the POOM mapping changes.

This architecture is what allows ghost links [EC-GHOST-LINK]: even when all content is deleted and I-to-V conversion returns empty, the link orgl's I-addresses remain intact in permanent storage, reconstitutable by any future COPY that re-establishes a POOM mapping for those addresses.

---

## Code Exploration

Now I have everything I need. The code is confirmed — here is the definitive answer.

---

## Link Endset I-Addresses Are Permanently Frozen

**Short answer:** Yes, permanently frozen. The endset I-addresses are converted from V-space to I-space exactly once at link creation and are never touched again by any subsequent operation.

---

### 1. Creation: V→I Conversion Happens Once

`docreatelink` in `do1.c:195-221` is the sole entry point for link creation. The key sequence is:

```c
// do1.c:214-219
&& specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
&& specset2sporglset (taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)
&& specset2sporglset (taskptr, threespecset, &threesporglset, NOBERTREQUIRED)
&& setlinkvsas (&fromvsa, &tovsa, &threevsa)
&& insertendsetsinorgl (taskptr, linkisaptr, link, &fromvsa, fromsporglset, ...)
&& insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, ...)
```

`specset2sporglset` converts user-supplied V-spans into **sporglsets** (I-addressed span records). This calls `vspanset2ispanset` [`orglinks.c:397-401`], which calls `permute(taskptr, orgl, vspanptr, V, ispansetptr, I)` — a one-time walk of the document's POOM structure that maps V-positions to their permanent I-addresses.

---

### 2. Storage: Both Indices Record the I-Address, Not V

**In the link's orgl (granfilade)** via `insertpm` [`orglinks.c:75-134`]:

```c
// orglinks.c:105, 109 — I-coordinates stored explicitly
movetumbler (&lstream, &crumorigin.dsas[I]);
movetumbler (&lwidth,  &crumwidth.dsas[I]);
movetumbler (vsaptr,   &crumorigin.dsas[V]);   // V is only for the link-atom's own address
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // line 130
```

The crum stores **both** the V-address of the link atom (`dsas[V]`) and the I-address of the content it references (`dsas[I]`). The `dsas[I]` fields are set from the sporglset — these are the endset I-addresses.

**In the spanfilade** via `insertspanf` [`spanf1.c:15-54`]:

```c
// spanf1.c:27-28, 49-51
movetumbler (&((typeispan *)sporglset)->stream, &lstream);
movetumbler (&((typeispan *)sporglset)->width,  &lwidth);
...
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
movetumbler (&lwidth,  &crumwidth.dsas[SPANRANGE]);
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
```

The spanfilade also records I-addresses (the `SPANRANGE` dimension here is indexed on I-addresses) directly from the sporglset.

---

### 3. Subsequent Operations Do NOT Touch Link Endsets

**`rearrangend`** [`edit.c:78-160`] — called when content is rearranged (V-positions shift). It walks the tree and applies offset diffs with:

```c
// edit.c:125
tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
```

The `index` here is the POOM's V-dimension. This shifts V-positions of content crums — **not** the `dsas[I]` fields of link crums. The link's endset I-addresses (`dsas[I]`) sit in the link's own orgl, which `rearrangend` is never called on for the purpose of updating endsets.

**`rearrangepm`** [`orglinks.c:137-142`] — calls `rearrangend` on the document's POOM only:

```c
// orglinks.c:139
rearrangend((typecuc*)docorgl, cutseqptr, V);
```

This is the document's content orgl, not the link's orgl. The link orgl's I-dimension crums are not visited.

**`deletend`** and **`deletecutsectionnd`** — delete V-ranges from the content tree; they never walk into link orgls to update endsets.

**No `updateendset`, `relink`, or `modifyendset` function exists anywhere in the codebase.** There is no code path that reaches into a stored link crum and changes its `dsas[I]` field after the initial `insertpm` call.

---

### 4. Why This Is Architecturally Correct — and Deliberate

The I-address space is **permanent by design**. I-addresses identify positions in the permascroll — the append-only content log. When content is inserted at a new V-position, the permascroll gains a new I-address; when content is "deleted," its V-address is removed but its I-address in the permascroll persists forever.

Because a link endset's I-addresses refer to permascroll positions rather than V-positions, they **do not need to be updated when V-positions shift**. The V→I conversion at creation time (`permute`, `orglinks.c:404`) is the design's correctness guarantee: once you've recorded where the content lives in I-space, that address is immutable regardless of how many inserts, deletes, or rearrangements subsequently change the content's V-address.

The sporglset in `insertpm` stores both `dsas[V]` (where the link-atom lives in document V-space) and `dsas[I]` (the I-address of the referenced content). When a document operation runs `rearrangend`, it adjusts `dsas[V]` for content crums — but the link orgl's endset crums' `dsas[I]` fields are never in scope for those adjustments.

---

### Summary

| Question | Answer | Key Citation |
|---|---|---|
| Are endsets stored as I-addresses? | Yes | `orglinks.c:105,109`; `spanf1.c:49-50` |
| Is V→I conversion done once at creation? | Yes | `do1.c:214-216`; `orglinks.c:401` |
| Does `rearrangend` update link endsets? | No | `edit.c:125` adjusts `dsas[index]` on content crums only |
| Does any operation mutate endset I-addresses? | No | No such function exists |
| Are endsets frozen at creation I-addresses? | **Yes, permanently** | Architecture: I-space is immutable permascroll |
