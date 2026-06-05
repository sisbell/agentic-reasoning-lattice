## Question 14 [evidence]

> When the type endset references the global type namespace at 1.0.2.x, does a direct read return that type address as a raw I-address span identical in structure to the source and target endsets?

## KB Synthesis

Yes, with one important caveat.

**Structural identity: yes.** The type endset is stored and retrieved through the identical mechanism as source and target endsets.

At link creation, `setlinkvsas()` constructs three V-subspace positions: digit-0 = 1 (FROM), 2 (TO), 3 (THREE) [SS-SUBSPACE-CONVENTION, Finding 0038]. The type VSpec is converted to sporgls via `vspanset2sporglset()`, producing permascroll I-addresses from the bootstrap document's type registry content (1.0.2.x). These are stored in the link orgl at position 0.3 alongside FROM at 0.1 and TO at 0.2. All three positions hold I-address sporgls — identical data format [SS-LINK-ENDPOINT, Finding 0024; INT-SPORGL-LINK-INDEX, Finding 0013].

On retrieval, `link2sporglset()` uses `retrieverestricted()` uniformly at whichever endset position is requested (0.1, 0.2, or 0.3). The resulting sporglset is then fed through `linksporglset2specset()` for I→V conversion. No code path distinguishes the type endset from source or target at the structural level [SS-FOLLOWLINK, Finding 0048; SS-RETRIEVE-ENDSETS, Finding 0035].

**The caveat:** The KB documents an unexplained anomaly — when *both* source and target content is deleted, `follow_link(link_id, LINK_TYPE)` returns empty despite the bootstrap document being unmodified. The KB notes this as "either a bug or an undocumented dependency of type resolution on endpoint resolution" [EC-ORPHANED-LINK, Finding 0024]. The mechanism is not explained by any KB entry. The type endset is structurally identical, but something in the implementation creates an undocumented dependency that the KB cannot resolve from available evidence.

---

## Code Exploration

I now have all the information needed. Let me write the complete answer.

---

## Answer

### What "1.0.2.x" is

The "global type namespace at 1.0.2.x" is a **V-address** in the bootstrap type definitions document, not a raw I-address. From `client.py`:

```python
# client.py:597-608
LINK_TYPES_DOC = Address(1, 1, 0, 1, 0, 1)  # Document 1 (bootstrap doc)
# Local address within doc: version.0.link_subspace.type = 1.0.2.X
JUMP_TYPE = VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 2), Offset(0, 1))])
QUOTE_TYPE = VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 3), Offset(0, 1))])
FOOTNOTE_TYPE = VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 6), Offset(0, 1))])
```

`JUMP_TYPE` is a `VSpec` with `docisa = 1.1.0.1.0.1` and V-span `{stream: 1.0.2.2, width: 0.1}`. The address `1.0.2.x` is a V-position in the link subspace of the bootstrap document, not a permascroll I-address.

---

### Storage Path: VSpec → Sporgl

When `docreatelink` is called with this type endset, `do1.c:216`:

```c
specset2sporglset(taskptr, threespecset, &threesporglset, NOBERTREQUIRED)
```

`specset2sporglset` (`sporgl.c:14-33`) sees a `VSPECID` and calls `vspanset2sporglset` (`sporgl.c:35-65`):

```c
// sporgl.c:50-57
sporglset = (typesporgl *) taskalloc(taskptr, sizeof(typesporgl));
sporglset->itemid = SPORGLID;
movetumbler(docisa, &sporglset->sporgladdress);   // = 1.1.0.1.0.1
movetumbler(&ispanset->stream, &sporglset->sporglorigin);  // I-addr of 1.0.2.x in type doc
movetumbler(&ispanset->width, &sporglset->sporglwidth);
```

The sporgl carries `sporgladdress = 1.1.0.1.0.1` (non-zero provenance) and `sporglorigin` = the permascroll I-address corresponding to V=1.0.2.2 in the type document.

This SPORGLID is inserted into the link's ORGL at V=3.1 via `insertpm` (`orglinks.c:75-134`). `unpacksporgl` (`sporgl.c:184-187`) stores `linfo.homedoc = sporgladdress = 1.1.0.1.0.1`, so the ORGL crum records both the I-address of the type content and its provenance.

---

### What a Direct Read Returns

Via `follow_link(link_id, LINK_TYPE=3)`:

**Step 1**: `link2sporglset` (`sporgl.c:67-95`) queries the link's ORGL at V∈[3,4):

```c
// sporgl.c:80-88
tumblerincrement(&zero, 0, whichend/*=3*/, &vspan.stream);  // V = 3
tumblerincrement(&zero, 0, 1, &vspan.width);
context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, NULL);
// contextintosporgl: sporgladdress = context2dinfo.homedoc = 1.1.0.1.0.1 (non-zero)
```

**Step 2**: `dofollowlink` (`do1.c:223-232`) passes `homedoc = &sporglset->sporgladdress = 1.1.0.1.0.1` into:

```c
linksporglset2specset(taskptr, &sporgl->sporgladdress, sporglset, specsetptr, NOBERTREQUIRED)
```

**Step 3**: The key branch in `linksporglset2specset` (`sporgl.c:105-116`):

```c
if (iszerotumbler(&((typesporgl *)sporglset)->sporgladdress)) {
    // ISPANID path — raw I-span returned
    ((typeitemheader *)specset)->itemid = ISPANID;
    movetumbler(&sporglset->sporglorigin, &((typeispan *)specset)->stream);
    movetumbler(&sporglset->sporglwidth,  &((typeispan *)specset)->width);
} else {
    // VSPECID path — V-spec returned
    linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);
}
```

Because `sporgladdress = 1.1.0.1.0.1` is **non-zero**, the ISPANID branch is **never taken**. `linksporglset2vspec` (`sporgl.c:127-137`) is called:

```c
specptr->itemid = VSPECID;
movetumbler(homedoc, &specptr->docisa);   // docisa = 1.1.0.1.0.1
sporglset2vspanset(taskptr, homedoc, sporglsetptr, &specptr->vspanset, type);
// I→V translation in type doc: recovers V-span ≈ Span(1.0.2.2, 0.1)
```

The result is a **VSpec**, not a raw I-span. The address 1.0.2.x is reconstituted as a V-address in the type document—not returned as a raw I-address span.

---

### Structural Identity with Source and Target Endsets

The structural identity **does hold**: all three endsets go through the identical code path in `linksporglset2specset`. For source and target endsets stored as VSpecs:

- `sporgladdress` = source_docisa / target_docisa (non-zero)
- `linksporglset2specset` → VSPECID path for all three
- Type endset: `{docisa: 1.1.0.1.0.1, vspanset: Span(1.0.2.2, 0.1)}`
- Source endset: `{docisa: source_docisa, vspanset: Span(1.7, 0.4)}`

All three are `typevspec` structs with `itemid = VSPECID`, `docisa`, and `vspanset`. The symmetry is enforced by `setlinkvsas` (`do2.c:169-183`) assigning from/to/type to V-slots 1.1/2.1/3.1 symmetrically, and `insertendsetsinorgl` (`do2.c:130-149`) and `insertendsetsinspanf` (`do2.c:116-128`) treating all three identically.

The ISPANID path at `sporgl.c:105-114` is only reachable when `sporgladdress` is zero—which occurs only when the original endset was a raw ISPANID (not a VSpec) and was stored through the ORGL path with `unpacksporgl` zeroing the homedoc (`sporgl.c:183`).

---

### Empirical Confirmation: Type Endset Returns Empty

The golden test `golden/endsets/retrieve_endsets.json` confirms what happens with `JUMP_TYPE` in practice:

```json
{
  "op": "retrieve_endsets",
  "link": "1.1.0.1.0.1.0.2.1",
  "source": [{"docid": "1.1.0.1.0.1", "spans": [{"start": "1.7", "width": "0.4"}]}],
  "target": [],
  "type": []
}
```

The type endset is **empty**. The `JUMP_TYPE` VSpec (`VSpec(1.1.0.1.0.1, [Span(1.0.2.2, 0.1)])`) references V=1.0.2.2 in the bootstrap document. Because the bootstrap document is either absent or unpopulated at that V-address, `vspanset2ispanset` returns an empty ispanset, no sporgl entries are created, and nothing is stored for the type endset.

The `insertendsetsinorgl` code at `do2.c:136-145` explicitly handles this:

```c
if (threevsa && threesporglset) {
    insertpm(taskptr, linkISA, link, threevsa, threesporglset);
} else {
    fprintf(stderr, "leaving INSERTENDSETSINORGL 4\n");
    // no-op: type endset silently omitted
}
```

---

### Summary

**No**, a direct read does not return the type address as a raw I-address span. It returns a `VSpec` (VSPECID), because the type endset is stored as a SPORGLID with non-zero `sporgladdress` (`= 1.1.0.1.0.1`), and `linksporglset2specset` (`sporgl.c:105`) only produces a raw ISPANID when `sporgladdress` is zero—a condition that cannot occur for VSpec-specified endsets.

**The structure IS identical to source and target endsets**: all three are `typevspec` items with `{docisa, vspanset}`. There is no special-casing for the type endset anywhere in the retrieval path.

**In practice**, the type endset returns **empty** (`[]`) because the bootstrap type document (1.1.0.1.0.1) is not populated with content at V=1.0.2.x in the test harness environment. The system silently omits the type endset when the V→I translation yields nothing.
