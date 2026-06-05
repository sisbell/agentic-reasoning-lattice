## Question 18 [evidence]

> Must the text VSpec and link VSpec returned together be mutually disjoint in V-space (no overlap in tumbler ranges), and is this disjointness guaranteed by the subspace separator structure rather than checked at retrieval time?

## KB Synthesis

Yes, with an important caveat about enforcement.

## Structural Disjointness

Text spans and link spans are **structurally disjoint by address**: text occupies `1.x`, links occupy `2.x`, and type endpoints occupy `3.x` [SS-DUAL-ENFILADE], [SS-SUBSPACE-CONVENTION]. Because these ranges have different first mantissa digits, the tumbler total order [INV-TUMBLER-TOTAL-ORDER] guarantees all `1.x` addresses are strictly less than all `2.x` addresses — no overlap is geometrically possible within their respective subspaces.

## Disjointness Is Structural, Not Checked at Retrieval

`retrievevspansetpm()` uses `is1story()` to detect whether content spans multiple subspaces and constructs separate spans per subspace [SS-VSPAN-VS-VSPANSET]. It does not validate or enforce disjointness — it merely reads what the POOM contains. Similarly, `findnextlinkvsa()` hardcodes link placement starting at `2.1` [SS-LINK-SUBSPACE], and the INSERT two-blade knife bounds shifts to `[insertion_point, (N+1).1)`, preventing cross-subspace shifts [SS-TWO-BLADE-KNIFE], [FC-SUBSPACE].

## The Catch: Caller-Enforced, Not Storage-Enforced

The disjointness guarantee holds only for **well-formed documents**. `acceptablevsa()` is a no-op stub that always returns `TRUE` [INV-SUBSPACE-CONVENTION]. Findings 0049 and 0051 demonstrate two concrete violation paths:

1. **INSERT at `2.x` with text** — succeeds silently [PRE-ENF0-PLACEMENT-GAP]
2. **REARRANGE with cross-subspace cuts** — moves text into the link subspace [PRE-REARRANGE]

If either violation occurs, `retrievevspansetpm()` would return "text" and "link" spans that are not disjoint.

**Conclusion:** Disjointness is guaranteed by the address separator structure (not by runtime checks) for any document produced by well-formed operations. The two-blade knife [SS-TWO-BLADE-KNIFE] preserves existing disjointness under INSERT, and `findnextlinkvsa()` ensures link placement stays in `2.x` under CREATELINK. But the storage layer enforces nothing — disjointness is a property of the operation discipline, verifiable as a Dafny postcondition on each public operation rather than as a storage-layer invariant [INV-SUBSPACE-CONVENTION].

---

## Code Exploration

I now have all the evidence needed from source code and golden tests. Here is the full answer.

---

## Answer: Text VSpec and Link VSpec Disjointness in V-space

### Short Answer

Yes — the text VSpec and link VSpec returned together are always disjoint in V-space. That disjointness is **structurally imposed by the subspace separator at V=2.0**, not checked at retrieval time. There is no runtime overlap validator anywhere in the retrieval path.

---

### The Subspace Separator

The entire mechanism rests on one invariant: **text lives below V=2.0, links live at or above V=2.1**.

The separator tumbler 2.0 is constructed as:
```c
// orglinks.c:36-37
tumblerclear(&linkspacevstart);
tumblerincrement(&linkspacevstart, 0, 2, &linkspacevstart);  // mantissa[0] = 2
```

This value appears explicitly in `findvsatoappend` [orglinks.c:29-49] where it names the region text must stay below:

```c
if (
   iszerolock((tumbler*)&ptr->cwid, widsize(POOM))
|| (tumblercmp(&grasp.dsas[V], &linkspacevstart) != LESS)) {
    tumblerincrement(vsaptr, 0, 1, vsaptr);  // text starts at 1.x
    tumblerincrement(vsaptr, 1, 1, vsaptr);  // specifically 1.1
} else if (tumblercmp(&reach.dsas[V], &linkspacevstart) == LESS) {
    movetumbler(&reach.dsas[V], vsaptr);     // append after existing text, still < 2.0
} else {
    findnextaddressinvspace(ptr, &grasp, &linkspacevstart, vsaptr);  // find gap below 2.0
}
```

Every path through `findvsatoappend` places text VSAs strictly below `linkspacevstart` (2.0). Text starts at 1.1 = `{mantissa=[1,1]}` and grows upward, but never reaches 2.0.

On the other side, `findnextlinkvsa` [do2.c:151-167] always places links at 2.1 or later:

```c
tumblerclear(&firstlink);
tumblerincrement(&firstlink, 0, 2, &firstlink);  // firstlink = 2.0
tumblerincrement(&firstlink, 1, 1, &firstlink);  // firstlink = 2.1
(void) doretrievedocvspan(taskptr, docisaptr, &vspan);
tumbleradd(&vspan.stream, &vspan.width, &vspanreach);
if (tumblercmp(&vspanreach, &firstlink) == LESS)
    movetumbler(&firstlink, vsaptr);   // start at 2.1
else
    movetumbler(&vspanreach, vsaptr);  // or after existing content
```

Since `firstlink` = 2.1 = `{mantissa=[2,1]}`, and the link VSA only grows from there, the gap [1.x, 2.0) and [2.1, ...) cannot overlap. There is an empty region at exactly 2.0, but functionally text is always ≤ 1.x and links always ≥ 2.1.

---

### Not Checked at Retrieval Time

`acceptablevsa` [do2.c:110-113] is the gate that should validate insertion VSAs. It is a stub:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

No check. No rejection. The comment `/*zzz*/` in `docopy` [do1.c:56] suggests this was always expected to grow but never did.

The retrieval path in `retrievevspansetpm` [orglinks.c:173-221] extracts text and link spans via **structurally different tree-walk methods**, not by comparing their ranges:

- **Link span**: Derived from the root crum's V-width by zeroing `mantissa[1]` and justifying — this extracts the integer component of the total document extent.
- **Text span**: Computed via `maxtextwid()` [orglinks.c:224-245], which recursively walks the tree including only text crums (those where `islinkcrum()` returns false).

```c
// orglinks.c:191-217 (non-1story path)
linkvspan.stream = ccptr->cwid.dsas[V];
linkvspan.stream.mantissa[1] = 0;    // zero out sub-integer component
tumblerjustify(&linkvspan.stream);   // shift to produce the link sentinel

maxtextwid(taskptr, ccptr, &voffset, &maxwid);
vspan.stream = 0 (cleared);
vspan.width = maxwid;
vspan.width.mantissa[0] = 0;         // zero out integer component → fractional width
```

The two results are placed on the list via `putvspaninlist` [orglinks.c:329-387] with no check that their ranges are disjoint. The system trusts the structural guarantee from allocation time.

---

### What the Output Looks Like

Because of the normalization in `retrievevspansetpm`, the returned VSpec pair has a second layer of disjointness in the output encoding:

- **Text span**: `{stream: 0, width: fractional}` — occupies `[0, <1)` in the output
- **Link span**: `{stream: integer≥1, width: integer≥1}` — occupies `[≥1, ≥2)` in the output

Golden test `golden/subspace/createlink_check_text_positions.json` confirms this:
```json
"vspanset_after_first_link": {
    "spans": [
        {"start": "0",  "width": "0.1"},   ← text span (fractional)
        {"start": "1",  "width": "1"}       ← link span (integer range)
    ]
}
```

And `golden/subspace/insert_text_check_link_positions.json` verifies the subspaces are independent — inserting text at 1.3 does not move the link at 2.1:
```json
"link_at_2_1_after": ["1.1.0.1.0.1.0.2.1"],  ← link unmoved
"link_at_2_3_after": []                         ← not shifted
```

Finding 0038 notes the critical normalization caution: the `0.x` representation in output is a **display convention**, not the internal V-address. The internal address is always 2.x.

---

### The Structural Claim Holds — With Known Gaps

The disjointness guarantee is real but has two documented holes:

**Gap 1: FEBE INSERT accepts arbitrary VSAs** (Finding 0049)

`acceptablevsa` always returns TRUE [do2.c:110-113]. A client can call INSERT with a VSA of `2.1` and the backend will place text bytes in the link subspace. Golden tests confirm this works without error. The subspace partition is a **convention**, not an **invariant enforced by the backend**.

**Gap 2: REARRANGE can cross subspace boundaries** (Finding 0051/0050)

`rearrangend` [edit.c:78-160] applies `tumbleradd` offsets computed from cut points with no subspace awareness. Cuts spanning the 2.0 boundary will move text crums into 2.x. This is a structural bypass.

Both gaps are flagged in Findings 0049 and 0051 as violations of content discipline CD0. The system relies on the front-end to honor the convention.

---

### Conclusion

The text VSpec and link VSpec returned by `doretrievedocvspanset` are **always disjoint in V-space** when the document has been constructed using the server-managed allocation functions (`appendpm` → `findvsatoappend` for text; `docreatelink` → `findnextlinkvsa` for links). The disjointness is **guaranteed structurally** by the subspace separator at V=2.0, encoded in those allocation functions. It is **not checked at retrieval time** — `retrievevspansetpm` uses structurally different tree-walk paths for each subspace and trusts the allocation invariant. `acceptablevsa` [do2.c:110-113] is a stub that never rejects any VSA.

The output representation adds a second disjointness layer (text at fractional 0.x, links at integer 1.x in the normalized form), but this is a derived encoding, not the raw V-space structure.

The fundamental architectural decision here is **Option B** from Finding 0009: uniform enfilade storage with V-position overloaded as both a coordinate and a type indicator. The subspace boundary at 2.0 is the implicit type separator baked into the allocation logic, not enforced by any validator.
