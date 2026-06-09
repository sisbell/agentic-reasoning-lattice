## Question 20 [evidence]

> Is a newly created link immediately discoverable by content-region search from ANY document whose POOM shares I-addresses with any of its endsets — including documents other than the home document — confirming that link residence is decoupled from discoverability scope?

## KB Synthesis

**Yes, confirmed — link residence and discoverability scope are fully decoupled.**

## Mechanism

When `CREATELINK` executes, it writes to the spanfilade via `insertendsetsinspanf()`, indexing each endpoint's I-addresses globally [ST-CREATE-LINK]. The spanfilade is a flat `Map<IAddress, Set<LinkISA>>` with no per-document scoping [SS-SPANF-OPERATIONS]. The home document parameter controls only where the link's orgl address is allocated — not where it is findable [SS-LINK-HOME-DOCUMENT].

`find_links` then operates as a pure I-address intersection query against that global index [SS-FIND-LINKS]: `find_links(S) = { L | I-addresses(S) ∩ I-addresses(L.source) ≠ ∅ }`. Any document whose POOM maps V-positions to I-addresses overlapping an endpoint qualifies, regardless of whether it is the home document, a transcluding document, or a version.

## Confirming Evidence

- **Transclusion**: `vcopy(link.source_content, src, dst) ⟹ findable(link, dst)` [INT-LINK-TRANSCLUSION]. The link was not created in `dst`; discoverability follows the shared I-addresses.
- **Versioning**: Versions discover links from the original without copying link POOM entries, solely via shared text I-addresses [INT-LINK-VERSION][ST-VERSION-CREATE].
- **Mixed chains**: Version-then-transclusion and transclusion-then-version both preserve discoverability transitively [INV-LINK-GLOBAL-VISIBILITY][INV-TRANSITIVE-IDENTITY].
- **Implementation reinforcement**: The orgl-range filter in `sporglset2linkset` is disabled by a `TRUE||` guard, making all searches unconditionally global in the orgl dimension [EC-FIND-LINKS-GLOBAL].

## Formal Statement

`∀ link L, doc D : (∃ v : poom.D(v) ∈ endpoint_iaddrs(L)) ⟹ L ∈ find_links(D)` — immediately after creation, since `insertendsetsinspanf` is called atomically within the same `CREATELINK` operation [INV-ATOMICITY].

---

## Code Exploration

I now have all the code I need. Let me trace the complete execution path with exact line citations.

---

## Answer: Link Residence vs. Discoverability in udanax-green

**Yes — link residence and discoverability scope are fully decoupled.** A newly created link is immediately discoverable by content-region search from any document whose POOM shares I-addresses with any of its endsets, including documents entirely unrelated to the home document. Here is the complete code trace.

---

### 1. Link Creation Entry — `fns.c` → `do1.c:195`

The FEBE handler calls `docreatelink` in `do1.c:195`. The "home document" (`docisaptr`) controls only where the link gets a V-address — it does not scope discoverability:

```c
// do1.c:207–219
makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);     // link belongs to home doc
return (
     createorglingranf(taskptr, granf, &hint, linkisaptr) // allocate link ISA
  && tumbler2spanset(taskptr, linkisaptr, &ispanset)
  && findnextlinkvsa(taskptr, docisaptr, &linkvsa)        // next V-slot in HOME DOC
  && docopy(taskptr, docisaptr, &linkvsa, ispanset)       // insert into HOME DOC POOM
  ...
  && insertendsetsinspanf(taskptr, spanf, linkisaptr,     // ← GLOBAL spanfilade
                          fromsporglset, tosporglset, threesporglset)
);
```

Two separate registrations happen:
- `docopy` → `do1.c:212`: puts the link into the **home document's** POOM at `linkvsa`
- `insertendsetsinspanf` → `do1.c:219`: puts the endsets' I-addresses into the **global `spanf`**

The global `spanf` is the decisive structure for discoverability.

---

### 2. V→I Conversion: Endsets Become I-Addresses

Before storing into `spanf`, `specset2sporglset` (`sporgl.c:14`) converts each V-address spec into a "sporgl" carrying an I-address:

```c
// sporgl.c:35–64  (vspanset2sporglset)
if (!findorgl(taskptr, granf, docisa, &orgl, type)) return NULL;
for (; vspanset; ...) {
    vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);  // V→I via source doc's POOM
    for (; ispanset; ...) {
        sporglset->itemid = SPORGLID;
        movetumbler(docisa, &sporglset->sporgladdress);   // records source doc
        movetumbler(&ispanset->stream, &sporglset->sporglorigin);  // I-address
        movetumbler(&ispanset->width,  &sporglset->sporglwidth);
    }
}
```

The I-address is a permascroll address — the same I-span regardless of which document's V-space maps to it.

---

### 3. How Endsets Are Stored in `spanf` — `spanf1.c:15`

`insertspanf` inserts entries keyed by two dimensions:

```c
// spanf1.c:22, 49–51
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);  // key: [linkISA ++ FROM/TO/THREE]
// then for each sporgl in the set:
movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);  // key: I-address of endset
movetumbler(&lwidth,  &crumwidth.dsas[SPANRANGE]);
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

The spanfilade is indexed by **SPANRANGE = I-address**. There is no document identifier used as a search key. The `linfo.homedoc` field (`spanf1.c:29,33,42`) is stored as payload metadata, not as a search dimension.

---

### 4. Link Discovery Search — `sporgl.c:222` and `sporgl.c:239`

The search path `dofindlinksfromtothree` (`do1.c:348`) → `findlinksfromtothreesp` (`spanf1.c:56`) → `sporglset2linkset` (`sporgl.c:222`) → `sporglset2linksetinrange` (`sporgl.c:239`):

```c
// sporgl.c:227 — the homeset parameter is unconditionally overridden:
if (TRUE||!homeset) {          // ← "TRUE||" hard-codes this branch always taken
    nullhomeset.width.mantissa[0] = 100;  // unbounded ORGL range
    homeset = &nullhomeset;
}
```

This is a deliberate override. Any document-scoping intent was explicitly nullified.

Inside `sporglset2linksetinrange` (`sporgl.c:239`), the per-item filter logic for SPORGLID items is also disabled:

```c
// sporgl.c:251–255
if (FALSE/*trying to kluge links followable thru versions*/
    && ((typeitemheader*)sporglset)->itemid == SPORGLID) {
    infoptr = &linfo;
    movetumbler(&sporgl->sporgladdress, &linfo.homedoc);
} else
    infoptr = NULL;   // ← always NULL in practice
```

The comment "trying to kluge links followable thru versions" reveals the historical intent: an attempt to filter by source document was tried and then deliberately removed. `infoptr` is always `NULL`, so `retrieverestricted` at `sporgl.c:259` is called with no document filter:

```c
// sporgl.c:259
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                              &range, ORGLRANGE,
                              (typeisa*)infoptr);  // ← NULL: no homedoc filter
```

The retrieval returns every link in the global `spanf` whose I-address overlaps the query I-address, regardless of which document the link "lives in."

---

### 5. How a Foreign Document's Query Reaches the Link

Suppose link L is created in doc A with endset pointing to permascroll I-address X. Doc B (which shares no POOM overlap at the V-level with doc A) independently contains content that was transcluded from the same permascroll region — so doc B's POOM also maps some V-address to I-address X.

When doc B performs a content-region search:

1. `specset2sporglset` calls `vspanset2sporglset` with `docisa = B`, which uses doc B's POOM to convert V→I, yielding I-address X.
2. `sporglset2linkset` searches the global `spanf` for SPANRANGE = X.
3. The entry for link L is found (it was stored at SPANRANGE = X during creation).
4. Link L's ISA is returned in the result set.

Doc B never opened link L. It never knew L existed. But L is immediately discoverable because the spanfilade index is I-address keyed and globally shared.

---

### 6. BERT Does Not Gate This

`findorgl` in `granf1.c:17` enforces BERT (document-open) checks for write operations and some reads. But `specset2sporglset` is called with `NOBERTREQUIRED` at `do1.c:214–216` during link creation, and the spanfilade search in `sporglset2linksetinrange` also passes `NOBERTREQUIRED` implicitly (via `NULL` infoptr). BERT gates document modification and V-content retrieval; it does not gate traversal of the I-address-keyed link index.

---

### Summary

| Aspect | Code location | Mechanism |
|---|---|---|
| Link residence | `do1.c:211–212` | `findnextlinkvsa` + `docopy` — V-slot in home doc's POOM |
| Endset I-address indexing | `do1.c:219`, `spanf1.c:15` | `insertendsetsinspanf` → `insertspanf` → global `spanf` keyed by I-address |
| Document filter override | `sporgl.c:227` | `if (TRUE\|\|!homeset)` unconditionally discards any doc scope |
| Version-scope kluge removal | `sporgl.c:251` | `if (FALSE ...)` disables per-item doc filter |
| Search key | `sporgl.c:259` | `retrieverestricted` on SPANRANGE (I-address), `infoptr = NULL` |

**Link residence is decoupled from discoverability scope.** The home document determines where the link gets a V-address; the global I-address-keyed spanfilade determines who can find it. Any document whose POOM overlaps with any endset's I-address can discover the link immediately upon creation, without reference to which document the link was created in.

This is the fundamental Xanadu architectural commitment: content identity is anchored in the permascroll (I-address), not in document membership. Links attach to content at the I-address level and are therefore visible across all documents that share that content.
