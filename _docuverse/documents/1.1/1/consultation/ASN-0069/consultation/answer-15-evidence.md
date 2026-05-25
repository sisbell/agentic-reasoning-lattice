## Question 15 [evidence]

> In the new version's POOM, are the V-addresses literally identical to the source's (so V:1.1 in the version corresponds positionally to V:1.1 in the source), or are they rebased/translated relative to the new document's address?

## KB Synthesis

## V-addresses are literally identical at version creation time

The V-addresses in the new version's POOM are not rebased — they are direct copies of the source's V-addresses.

**The mechanism** [ST-VERSION-CREATE, Finding 0043, 0077]:

`docreatenewversion` calls `doretrievedocvspanfoo` → `retrievedocumentpartofvspanpm`, which reads the source root's `cdsp.dsas[V]` (text subspace start, position `1`) and `cwid.dsas[V]` (text width). This vspan — e.g., `{start: 1.1, width: 0.15}` — is passed to `docopyinternal`, which converts it to I-spans via `specset2ispanset` (reading the *source's* POOM) and then calls `insertpm(new_version_doc, vsa=1.1, ispanset)`. The V-address parameter handed to `insertpm` is the same `1.1` from the source.

**Concrete confirmation** [ST-VERSION-CREATE, Finding 0043]:
```
Source vspanset: at 1.1 for 0.15
Version vspanset (immediately after creation): at 1.1 for 0.15
```
Same start, same width, same I-addresses.

**Behavioral consequence** [INT-LINK-VERSION, Finding 0019]:
> Original doc has link at V 1.17 width 0.4; version's `retrieve_endsets` reports the link at V 1.17 in the version's docid context.

The version simply inherits the source's entire V→I mapping for the text subspace. Link subspace (`2.x`) is not copied at all [ST-VERSION-CREATE, Finding 0043], so the version starts with an empty link subspace. After creation, the two POOMs are independent mutable trees [FC-VERSION-ISOLATION] — edits to either shift V-addresses in that document only.

---

## Code Exploration

I now have all the code I need to answer precisely. Let me trace the exact V-address flow:

---

## V-Address Assignment in New Versions: They Are Literally Identical to the Source's

### The complete call chain

**`docreatenewversion`** [do1.c:260–299] is the entry point. The key sequence:

```c
// do1.c:281-283
if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) { return FALSE; }

// do1.c:285-288
vspec.docisa = *isaptr;
vspec.vspanset = &vspan;

// do1.c:293
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
```

The VSA argument to `docopyinternal` is `&vspan.stream` — the source document's own starting V-address.

---

### Step 1: Where does `vspan.stream` come from?

**`doretrievedocvspanfoo`** [do1.c:301–309] calls **`retrievedocumentpartofvspanpm`** [orglinks.c:155–162]:

```c
// orglinks.c:159-160
movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
```

This reads **directly** from the source POOM root's `cdsp.dsas[V]` — the root node's V-axis displacement, which is the absolute V-address of the source document's content start. No translation. This is the raw starting V-address of the source.

---

### Step 2: What does `insertpm` do with `vsaptr`?

**`insertpm`** [orglinks.c:75–134] iterates over each I-span in `sporglset`:

```c
// orglinks.c:101-113
unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
movetumbler (&lstream, &crumorigin.dsas[I]);   // I-axis: permascroll address
movetumbler (&lwidth,  &crumwidth.dsas[I]);    // I-axis: I-span width
movetumbler (vsaptr,   &crumorigin.dsas[V]);   // V-axis: directly from vsaptr
```

At line 113, `vsaptr` (= source's `vspan.stream`) is copied verbatim into `crumorigin.dsas[V]`. Then:

```c
// orglinks.c:115-117
shift = tumblerlength (vsaptr) - 1;
inc = tumblerintdiff (&lwidth, &zero);
tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);
```

The V-width is computed from the I-span's character count (`lwidth`), at the same tumbler depth as `vsaptr`. Then:

```c
// orglinks.c:130-131
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);  // advance for next chunk
```

Each I-span is inserted into the new POOM at `vsaptr`, then `vsaptr` advances by that span's V-width for the next I-span.

---

### Step 3: How `insertnd` stores the V-address

**`insertcbcnd`** [insertnd.c:263]:

```c
dspsub (origin, grasp, &new->cdsp, (INT)father->cenftype);
```

The new crum's `cdsp` is `origin - grasp` — a displacement relative to the parent node's offset. This is normal enfilade coordinate encoding. The absolute V-address of the new crum is still `origin->dsas[V]` = `vsaptr` = the source's starting V-address. No translation occurs here.

---

### The Answer

**The V-addresses in the new version are literally identical to the source's.** Specifically:

1. `retrievedocumentpartofvspanpm` [orglinks.c:159] extracts the source's starting V-address (`cdsp.dsas[V]` of the source POOM root) as `vspan.stream` — no transformation.

2. That value is passed as `vsaptr` to `docopyinternal` [do1.c:293], then forwarded unchanged to `insertpm`.

3. `insertpm` [orglinks.c:113] places `vsaptr` directly into `crumorigin.dsas[V]` for the first I-span. Subsequent I-spans advance from there sequentially, based on their I-span widths.

4. For a single contiguous block of content (a never-edited document), there is one I-span: the entire document maps to a single new POOM crum at exactly `vspan.stream` with width = number of characters. V:1.1 in the source is V:1.1 in the new version.

5. For a document with deletions (gaps in V-space), `specset2ispanset` returns multiple I-spans covering only the surviving content. `insertpm` packs these **contiguously** from `vspan.stream`, advancing `vsaptr` by each chunk's V-width. In this case, deleted V-positions are not preserved as holes — the surviving content is re-packed without gaps, starting at the same V-address. Any content originally at V:1.5 (after a deletion at V:1.3) would now appear at V:1.3 in the new version.

**In short**: the new version starts at the same V-address as the source (`cdsp.dsas[V]`), and content is packed contiguously from there. For an unedited source, V-addresses are bit-for-bit identical. For an edited source, the new version re-packs the surviving content without holes, so post-deletion V-addresses may shift to close the gaps.
