## Question 16 [evidence]

> When the type endset is read, does it return the I-address registered in the global type namespace (`1.0.2.x`), and is that resolved differently from the source and target content endsets?

## KB Synthesis

## Type Endset Resolution

The KB gives a reasonably clear picture, though one anomaly remains unexplained.

### What the type endset stores

From [SS-LINK-ENDPOINT] Finding 0024, link types are stored as VSpec references to the bootstrap document's type registry at `1.0.2.x` (JUMP=`1.0.2.2`, QUOTE=`1.0.2.3`, etc.). At link creation, this VSpec is converted to I-addresses via `vspanset2sporglset` — so the link orgl at position `0.3` (the THREE endset) contains permascroll I-addresses corresponding to content bytes in the bootstrap document, not enum values or metadata tags.

### Resolution mechanism

From [SS-FOLLOWLINK] Finding 0048, FOLLOWLINK resolves **all three endsets identically**: `link2sporglset()` extracts I-addresses from the link orgl at the requested position (1, 2, or 3), then `linksporglset2specset()` does I-to-V conversion by looking up those I-addresses in the caller-supplied `homedoc`'s POOM. There is no special-casing for the type position.

The critical implication: the type I-addresses live in the **bootstrap document's** POOM, not in the link's home document or endpoint documents. If the caller passes the link's home document as `homedoc`, and that document's POOM doesn't map the bootstrap document's type I-addresses, the type endset is silently filtered to empty by the NULL-drop in `span2spanset()` (Finding 0048, `orglinks.c:446-448`). The caller would need to pass the bootstrap document as `homedoc` to recover meaningful type V-addresses.

### The anomalous empty type endset

[EC-ORPHANED-LINK] Finding 0024 documents that when both source and target content are deleted, `follow_link(link_id, LINK_TYPE)` also returns empty — even though the bootstrap document was never touched. The KB flags this as a bug or undocumented dependency. The FOLLOWLINK mechanism from Finding 0048 provides a plausible explanation: if the test always passes the same `homedoc` (likely the link's home document) for all three endset queries, the type I-addresses will fail I-to-V resolution in that document's POOM regardless of deletion state, because the bootstrap document's content was never in that POOM to begin with.

### Summary

The type endset stores permascroll I-addresses pointing to bootstrap document content. Resolution uses the same I-to-V path as source and target endsets — no architectural difference. The practical difference is that the type I-addresses are resident in the bootstrap document's POOM, so meaningful resolution requires querying against the bootstrap document, not the link's home or endpoint documents. Without that, the universal I-address filtering in `linksporglset2specset()` produces empty results.

---

## Code Exploration

Now I have all the code I need. Let me compile the complete answer with precise citations.

---

## How the Type Endset Is Read: Full Code Trace

### 1. Storage: All Three Endsets Are Treated Identically

`docreatelink` at `do1.c:195` takes all three specsets and processes them through identical steps:

```c
// do1.c:214-219
   specset2sporglset (taskptr, fromspecset,  &fromsporglset, NOBERTREQUIRED)
&& specset2sporglset (taskptr, tospecset,    &tosporglset,   NOBERTREQUIRED)
&& specset2sporglset (taskptr, threespecset, &threesporglset,NOBERTREQUIRED)
&& setlinkvsas (&fromvsa, &tovsa, &threevsa)
&& insertendsetsinorgl (taskptr, linkisaptr, link,
     &fromvsa, fromsporglset, &tovsa, tosporglset, &threevsa, threesporglset)
&& insertendsetsinspanf (taskptr, spanf, linkisaptr,
     fromsporglset, tosporglset, threesporglset)
```

`setlinkvsas` at `do2.c:169` assigns V-addresses within the link's internal V-space:

```c
// do2.c:171-180
tumblerincrement(fromvsaptr, 0, 1, fromvsaptr);
tumblerincrement(fromvsaptr, 1, 1, fromvsaptr);  // 0.1.1
...
tumblerincrement(tovsaptr, 0, 2, tovsaptr);
tumblerincrement(tovsaptr, 1, 1, tovsaptr);      // 0.2.1
...
tumblerincrement(threevsaptr, 0, 3, threevsaptr);
tumblerincrement(threevsaptr, 1, 1, threevsaptr); // 0.3.1
```

The link's internal V-space layout: source at `0.1.1`, target at `0.2.1`, type at `0.3.1`. The type endset has its own slot but no structural privilege.

`insertendsetsinspanf` at `do2.c:116` applies a conditional for the type endset:

```c
// do2.c:118-128
if (!(insertspanf(..., fromsporglset, LINKFROMSPAN)
    &&insertspanf(..., tosporglset,   LINKTOSPAN)))
    return (FALSE);
if (threesporglset) {
    if(!insertspanf(..., threesporglset, LINKTHREESPAN))
        return (FALSE);
}
```

The type endset (`LINKTHREESPAN=3`) is optional in the spanfilade — the `if (threesporglset)` guard allows a link with no type. Source and target have no such guard and are mandatory. This is the **only structural distinction** at creation time.

---

### 2. Retrieval Path Through `dofollowlink`

`dofollowlink` at `do1.c:223`:

```c
return (
   link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
&& linksporglset2specset (taskptr,
     &((typesporgl *)sporglset)->sporgladdress,
     sporglset, specsetptr, NOBERTREQUIRED));
```

The `whichend` parameter (1, 2, or 3) selects the endset. No type-specific branching here.

`link2sporglset` at `sporgl.c:67`:

```c
// sporgl.c:80-87
tumblerclear (&zero);
tumblerincrement (&zero, 0, whichend, &vspan.stream);
tumblerincrement (&zero, 0/*1*/, 1, &vspan.width);
if (context = retrieverestricted((typecuc*)orgl, &vspan, V,
                 (typespan*)NULL, I, (typeisa*)NULL)) {
    for (c = context; c; c = c->nextcontext) {
        sporglptr = (typesporgl *)taskalloc(...);
        contextintosporgl((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);
```

`whichend` directly indexes the V-space position (line 81). `contextintosporgl` at `sporgl.c:205` records the I-address and homedoc into the sporgl:

```c
// sporgl.c:209-211
movetumbler(/*linkid*/&context->context2dinfo.homedoc, &sporglptr->sporgladdress);
movetumbler(&context->totaloffset.dsas[index], &sporglptr->sporglorigin);
movetumbler(&context->contextwid.dsas[index],  &sporglptr->sporglwidth);
```

The `sporgladdress` field carries the **home document ISA** — the document in whose I-space the endset content lives.

---

### 3. The Resolution Branch in `linksporglset2specset`

`linksporglset2specset` at `sporgl.c:97`:

```c
// sporgl.c:105-117
if (iszerotumbler (&((typesporgl *)sporglset)->sporgladdress)) {
    // homedoc is zero → return raw I-span
    ((typeitemheader *)specset)->itemid = ISPANID;
    movetumbler(&((typesporgl *)sporglset)->sporglorigin, &((typeispan *)specset)->stream);
    movetumbler(&((typesporgl *)sporglset)->sporglwidth,  &((typeispan *)specset)->width);
} else {
    linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);
}
```

The branch is determined solely by whether `sporgladdress` (the homedoc) is zero. There is no `whichend`-based branch, no `LINKTHREESPAN` check. **All three endsets go through the same logic.**

`linksporglset2vspec` at `sporgl.c:127`:

```c
// sporgl.c:132-136
specptr->itemid = VSPECID;
movetumbler (homedoc/*&sporglset->sporgladdress*/, &specptr->docisa);
specptr->vspanset = NULL;
sporglset2vspanset (taskptr, homedoc, sporglsetptr, &specptr->vspanset, type);
```

The returned vspec's `docisa` is `homedoc` — the document whose I-space contains the endset content. The commented-out alternative `/*&sporglset->sporgladdress*/` is equivalent: `dofollowlink` passes `sporgladdress` as the `homedoc` argument at `do1.c:230`. Then `sporglset2vspanset` at `sporgl.c:141` calls `ispan2vspanset` to convert the stored I-coordinates back to V-addresses within that document's enfilade.

---

### 4. Does the Type Endset Return `1.0.2.x`?

Not directly as a raw I-address. Here is what actually happens:

**When the type endset input to `docreatelink` is a V-spec pointing to a type document at, say, `1.0.2.1.0.1`:**

1. `specset2sporglset` → `vspanset2sporglset` at `sporgl.c:35`: resolves the V-address to I-coordinates via `findorgl` + `vspanset2ispanset`; stores sporgl with `sporgladdress` = the type document ISA (e.g., `1.0.2.1.0.1`), `sporglorigin` = its I-address, `sporglwidth` = its width.

2. Stored in the link's orgl at V-position `0.3.1`.

3. Retrieved by `link2sporglset(whichend=3)`: finds content at `0.3.1`, builds sporgl with `sporgladdress` = the type document ISA.

4. `linksporglset2specset`: `sporgladdress` is non-zero → calls `linksporglset2vspec`.

5. Returns a **V-spec** with `docisa` = the type document ISA and `vspanset` = the reconstructed V-address in that document.

**The returned type endset is the V→I→V round-trip result** — a V-spec pointing back into whatever document holds the type content. If that document lives in `1.0.2.x`, the returned specset will have a `docisa` in that namespace.

---

### 5. Is the Type Endset Resolved Differently from Source/Target?

**No.** There is no code path that distinguishes `whichend=3` (type) from `whichend=1` or `whichend=2` during retrieval. The entire path — `dofollowlink` → `link2sporglset` → `contextintosporgl` → `linksporglset2specset` → `linksporglset2vspec` → `sporglset2vspanset` — is shared by all three endsets. The only selector is the `whichend` integer, which addresses a V-position in the link's orgl (`0.1.1`, `0.2.1`, or `0.3.1`).

The one structural difference is at **creation** (`do2.c:122`): the type endset is optional (`if (threesporglset)`), so a link with no type endset is legal. Source and target have no such guard and are mandatory. But once stored, the type endset is retrieved through the same resolution machinery.

---

### Summary

| Property | Source (whichend=1) | Target (whichend=2) | Type (whichend=3) |
|---|---|---|---|
| V-address in link | `0.1.1` | `0.2.1` | `0.3.1` |
| Storage path | `specset2sporglset` + `insertendsetsinorgl` + `insertendsetsinspanf` | same | same |
| Optional at creation | no | no | **yes** — `if (threesporglset)` guard at `do2.c:122` |
| Retrieval path | `link2sporglset` + `linksporglset2specset` | same | same |
| Return type | V-spec (if homedoc≠0) or I-span (if homedoc=0) | same | same |
| Resolution of `1.0.2.x` | N/A (typically user document) | N/A | V→I→V round-trip; returned as V-spec with `docisa` in `1.0.2.x` namespace |

The type endset is **not** returned as a raw I-address from the global type namespace. It is returned as a V-spec whose `docisa` reconstructs to the type document — the same format as a source or target V-spec, resolved by the same code. The `1.0.2.x` namespace is semantically significant (it holds the type content), but the retrieval machinery has no awareness of it.
