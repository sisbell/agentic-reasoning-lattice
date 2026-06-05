## Question 18 [evidence]

> Compared to a freshly created empty POOM, does a CREATENEWVERSION document differ by having text-subspace V→I entries copied in, while CREATEDOCUMENT's POOM has zero bottom crums?

## KB Synthesis

Yes, that distinction is correct and the KB entries support it precisely.

**CREATEDOCUMENT's POOM** starts from `createenf(POOM)`, which produces a minimal height-1 tree: one fullcrum (`isapex=TRUE`, `height=1`) containing a single bottom node at height-0 with zero width. There are no V→I mappings — the single bottom crum is a structural placeholder with empty content. [SS-ENFILADE-TREE / Finding 0058]

**CREATENEWVERSION's POOM** is different. The operation calls `doretrievedocvspanfoo` to extract the source document's text-subspace vspan (1.x only, via `retrievedocumentpartofvspanpm`), then passes it to `docopyinternal`, which calls `insertpm` to write actual bottom crums with real V→I mappings into the new document's POOM. The result is a populated tree with text content entries. [ST-VERSION-CREATE / Findings 0043, 0046]

Two additional points follow:

1. The link subspace (2.x) is excluded from the copy — `retrievedocumentpartofvspanpm` reads only the text displacement/width. So the version POOM starts with no link entries, identical to CREATEDOCUMENT in that respect. [FC-SUBSPACE / Finding 0043]

2. If the source is empty, `docopyinternal` copies nothing, and the version's POOM may structurally resemble the initial state — but it still passed through `insertpm`, so the tree shape may differ from the pristine `createenf` output. [SS-ENFILADE-TREE / Finding 0058]

In summary: CREATEDOCUMENT → one zero-width placeholder bottom crum, no content. CREATENEWVERSION (non-empty source) → populated POOM with text V→I bottom crums, no link subspace entries.

---

## Code Exploration

I now have enough to give a complete, cited answer.

---

## Answer

The framing is partially right but contains two inaccuracies the code corrects. Let me trace both paths.

---

### CREATEDOCUMENT — one zero-width bottom crum, not zero crums

`docreatenewdocument` [do1.c:234–241] calls only:

```c
makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
return createorglingranf(taskptr, granf, &hint, isaptr);
```

`createorglgr` [granf2.c:111–128] allocates the POOM via `createenf(POOM)` [granf2.c:120].

`createenf` [credel.c:492–516] does:

```c
fullcrumptr = createcrum(1, POOM);          // apex, height=1
adopt(ptr = createcrum(0, enftype),          // ONE bottom crum, height=0
      SON, (typecorecrum*)fullcrumptr);
ivemodified(ptr);
```

So the new POOM has **exactly one bottom crum** as the apex's left son. Both `cdsp` and `cwid` of that crum are all-zero (fresh from `createcrum`). `isemptyenfilade` [genf.c:97–113] returns TRUE for POOM when both cwid and cdsp are zero locks — confirming "empty," but **not "zero crums."** One placeholder crum exists; it just carries zero V-width and zero V-displacement.

No content, no V→I entries, no `insertpm`, no `insertspanf` — the POOM is structurally present but inert.

---

### CREATENEWVERSION — copies the *entire* V-extent, not just text subspace

`docreatenewversion` [do1.c:260–299]:

**Step 1** — creates the new POOM with `createorglingranf` [do1.c:277], identical to CREATEDOCUMENT: one zero-width bottom crum.

**Step 2** — reads the source document's V-span [do1.c:281–283]:

```c
doretrievedocvspanfoo(taskptr, isaptr, &vspan)
```

This calls `retrievedocumentpartofvspanpm` [orglinks.c:155–162]:

```c
movetumbler(&((typecuc*)orgl)->cdsp.dsas[V], &vspanptr->stream);
movetumbler(&((typecuc*)orgl)->cwid.dsas[V], &vspanptr->width);
```

It reads the **raw apex V-displacement and V-width** of the source POOM with no filtering. The comment in `do1.c:302` says plainly: *"this routine is a kluge not yet kluged."* There is no text-subspace filter here; it returns the full V-range from `cdsp[V]` to `cdsp[V] + cwid[V]`, which spans both link subspace (V < 1.0) and text subspace (V ≥ 1.0) if the source document has both.

**Step 3** — builds a vspec pointing at the source doc ISA and the full V-span [do1.c:285–288], bypasses the bert ownership check, then calls:

```c
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);   // do1.c:293
```

`docopyinternal` [do1.c:66–82]:

```c
specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)  // V→I via spanfilade
insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)        // writes POOM bottom crums
insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)     // V↔I index entries
```

`specset2ispanset` [do2.c:14–46] calls `vspanset2ispanset` on the source POOM to find all I-spans (permascroll addresses) that correspond to the full source V-span — again, no text-subspace filter.

`insertpm` [orglinks.c:75–134] then calls `insertnd` for each I-span, populating the previously-empty bottom crum (via `firstinsertionnd` [insertnd.c:199–218]) with real 2D coordinates:

```c
crumorigin.dsas[I] = lstream;   // permascroll address
crumorigin.dsas[V] = vsaptr;    // V-address in new doc (= source's cdsp[V])
crumwidth.dsas[I]  = lwidth;
crumwidth.dsas[V]  = computed from lwidth;
insertnd(taskptr, orgl, &crumorigin, &crumwidth, &linfo, V);
```

After this, the new document's POOM has live bottom crums with actual (V, I) extents.

---

### Summary of the distinction

| | CREATEDOCUMENT | CREATENEWVERSION |
|---|---|---|
| POOM after creation | 1 bottom crum, zero cwid/cdsp | 1 bottom crum, zero cwid/cdsp |
| `insertpm` called? | No | Yes — `docopyinternal` [do1.c:293] |
| Content of POOM | "empty" (isemptyenfilade=TRUE) | Live (V,I) extents from source |
| V-span copied | — | **Entire** source apex V-extent [orglinks.c:159–160], no text-subspace filter |

The key correction to your framing: **CREATEDOCUMENT does not have "zero bottom crums"** — `createenf` [credel.c:501] always plants exactly one zero-width bottom crum as the apex's son. And CREATENEWVERSION copies the **entire V-span** (link + text subspaces together), not just V≥1.0 text-subspace entries. `retrievedocumentpartofvspanpm` [orglinks.c:155–162] reads the raw apex V-extent with no subspace discrimination.
