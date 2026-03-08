## Question 18 [gregory]

> When CREATENEWVERSION copies the text subspace POOM, does it create new bottom crums with identical I-displacement and I-width values (byte-for-byte copies), or does it go through `insertpm` which might split or coalesce entries differently?

## KB Synthesis

## Answer

CREATENEWVERSION goes through `insertpm` — it does **not** create byte-for-byte crum copies.

### The Call Chain

From [ST-VERSION] Finding 0077, the full path is:

```
docreatenewversion
  → createorglingranf          (allocates new doc address; creates empty POOM)
  → doretrievedocvspanfoo      (gets source's text V-span)
  → docopyinternal
      → specset2ispanset       (converts V-spans to I-spans via source's POOM)
      → insertpm               (inserts I-spans into version's fresh POOM)
      → insertspanf            (records DOCISPAN entries)
```

### What insertpm Does

From [ST-VCOPY] Finding 0046, `insertpm` → `insertnd` applies the extension-or-create rule:

- If the new I-span is **contiguous** with the last crum AND shares the same `homedoc` → `isanextensionnd` merges them (extends existing crum width in place)
- Otherwise → new crum created

So the version's POOM structure is determined by the I-space fragmentation of the source's content, not a structural copy of the source's tree.

### Structural Consequences

**Simple source (only text inserts):** The source has one contiguous I-span. This gets inserted via `firstinsertionnd` as one bottom crum in the version's fresh height-1 tree.

**Fragmented source (inserts interrupted by link creation):** From [ST-CRUM-BOUND] Finding 0063, CREATELINK advances the I-address allocator, breaking text contiguity. The source's content spans multiple non-contiguous I-address ranges. These become multiple crums in the version, since `isanextensionnd` fails for non-contiguous I-addresses.

**Crucially**, from [INV-MONOTONIC] Finding 0077: CREATENEWVERSION does **not** advance the content I-address allocator at all (no call to `findisatoinsertgr`). The version's POOM is populated by re-inserting the source's existing I-addresses through the standard copy path — so a subsequent INSERT into the original allocates contiguous I-addresses after the existing content, and `compare_versions` shows a single shared span pair.

### Summary

| Property | Answer |
|----------|--------|
| Path through `insertpm`? | Yes |
| Byte-for-byte crum copy? | No |
| Tree height of new version | Starts at 1, grows with `splitcrumupwards` as I-spans are inserted |
| Crum count | Determined by I-span fragmentation of source; contiguous same-homedoc spans coalesce |
| I-address allocator affected? | No (Finding 0077) |

The version's POOM is semantically equivalent to the source's (same V→I mapping) but may differ structurally — particularly in tree height and crum count — since it's built fresh via the standard insertion path rather than cloned.

---

## Code Exploration

Now I have a complete picture. Let me compile the full answer.

---

## Answer

`CREATENEWVERSION` **does go through `insertpm`**, and the I-displacement/I-width values are **passed directly from the source POOM's bottom crums** — but `insertpm` recomputes the V-widths and `insertcbcnd` may coalesce adjacent crums. Here is the full trace with citations.

---

### Step 1 — `docreatenewversion` obtains a single V-span for the source doc

`docreatenewversion` [do1.c:260–299] calls:

```c
doretrievedocvspanfoo(taskptr, isaptr, &vspan)   // do1.c:281
```

which calls `retrievedocumentpartofvspanpm` [orglinks.c:155–162]:

```c
bool retrievedocumentpartofvspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{ /* this is a kluge*/
    vspanptr->itemid = VSPANID;
    movetumbler(&((typecuc *)orgl)->cdsp.dsas[V], &vspanptr->stream);
    movetumbler(&((typecuc *)orgl)->cwid.dsas[V], &vspanptr->width);
    return (TRUE);
}
```

This reads the **root crum's** `cdsp.dsas[V]` and `cwid.dsas[V]` directly — a single V-span covering the whole document with no traversal of the bottom crums.

Then [do1.c:285–293]:

```c
vspec.docisa = *isaptr;         // source document ISA
vspec.vspanset = &vspan;        // single V-span (whole doc)
...
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
```

---

### Step 2 — `docopyinternal` calls `insertpm`

`docopyinternal` [do1.c:66–82]:

```c
specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)  // line 74
...
insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)        // line 78
```

**Yes, it goes through `insertpm`.**

---

### Step 3 — `specset2ispanset` walks the source POOM crum by crum

`specset2ispanset` [do2.c:14–46] finds the source document's POOM and calls `vspanset2ispanset` [orglinks.c:397]:

```c
return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
```

`permute` → `span2spanset` [orglinks.c:425] calls `retrieverestricted` to walk the source POOM, producing one context per bottom crum. Each context becomes an **ISPANID** span via `context2span` → `onitemlist`, with:
- `stream` = absolute I-address of that bottom crum
- `width` = I-width of that bottom crum

So **the ispanset has one entry per source bottom crum**, and each entry's I-displacement and I-width come directly from the source crum.

---

### Step 4 — `insertpm` processes each I-span into the new POOM

`insertpm` [orglinks.c:75–134], for each entry in the sporglset:

```c
unpacksporgl(sporglset, &lstream, &lwidth, &linfo);     // line 101

movetumbler(&lstream, &crumorigin.dsas[I]);              // I-displacement preserved as-is
movetumbler(&lwidth, &crumwidth.dsas[I]);                // I-width preserved as-is
movetumbler(vsaptr, &crumorigin.dsas[V]);                // V-address is freshly assigned

shift = tumblerlength(vsaptr) - 1;                      // lines 115–117
inc = tumblerintdiff(&lwidth, &zero);
tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V]); // V-width RECOMPUTED

insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // line 130

tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr);          // advance V-address
```

Key observations:

1. **I-displacement** (`crumorigin.dsas[I]`) = `lstream` from `unpacksporgl` — the source crum's absolute I-address, passed through without modification.
2. **I-width** (`crumwidth.dsas[I]`) = `lwidth` from `unpacksporgl` — the source crum's I-width, passed through without modification.
3. **V-width is NOT copied** — it is recomputed from `tumblerlength(vsaptr)` (depth of the new V-address) and `tumblerintdiff(&lwidth, &zero)` (integer size of the I-width). This may produce a different tumbler shape than the source even if the integer values match.

For ISPANID items (the type produced by `specset2ispanset`), `unpacksporgl` [sporgl.c:180–184] sets `homedoc = 0`:

```c
if (((typeitemheader *)sporglptr)->itemid == ISPANID) {
    movetumbler(&((typeispan *)sporglptr)->stream, streamptr);
    movetumbler(&((typeispan *)sporglptr)->width, widthptr);
    tumblerclear(&infoptr->homedoc);   // homedoc zeroed
}
```

---

### Step 5 — Potential coalescing in `insertcbcnd`

`insertnd` → `insertmorend` → `insertcbcnd` [insertnd.c:242] checks `isanextensionnd` [insertnd.c:301–308] before creating each new bottom crum:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    if (!tumblereq(&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq(reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

This coalesces a new insertion into an existing crum if both:
- `homedoc` values match (both zero for ISPANID — this condition is always satisfied between any two source-derived crums)
- The existing crum's reach equals the new insertion's origin in **both V and I dimensions**

Since `vsaptr` advances by exactly `crumwidth.dsas[V]` after each insertion [orglinks.c:131], consecutive crums are always V-adjacent. So **coalescing occurs whenever consecutive source crums are also I-adjacent** (pointing to consecutive permascroll locations). A document whose content was inserted in a single operation will produce a single bottom crum in the new version, not multiple crums.

---

### Summary

| Property | Behavior |
|---|---|
| Goes through `insertpm`? | **Yes** [do1.c:78, orglinks.c:75] |
| I-displacement (`cdsp.dsas[I]`) | **Preserved byte-for-byte** from source crum [orglinks.c:105] |
| I-width (`cwid.dsas[I]`) | **Preserved byte-for-byte** from source crum [orglinks.c:109] |
| V-width (`cwid.dsas[V]`) | **Recomputed** from V-address depth and I-width integer value [orglinks.c:115–117] |
| Coalescing possible? | **Yes** — I-adjacent source crums with shared homedoc (=0) are merged by `isanextensionnd` [insertnd.c:301–308] |

The new version's POOM bottom crums have identical I-displacement and I-width values to the source, but the V-widths are freshly computed, and I-adjacent source crums may be merged into single crums in the copy.
