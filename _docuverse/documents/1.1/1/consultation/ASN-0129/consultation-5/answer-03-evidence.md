## Question 3 [evidence]

> What primitive tumbler operations does the read path actually perform when testing whether an address falls within a span and when deriving a link's home document and chain position from its address (field extraction around the `.0.3` link subspace? last-component increment? tumbler addition for span upper bounds?), and does any read operation enumerate the document or content store domains rather than only testing membership against them?

## KB Synthesis

## Read-Path Tumbler Operations

### Span Membership Testing

Every span membership check follows a two-step pattern:

**Step 1 — compute the reach:**
`tumbleradd` (exposed as `dspadd` in `retrie.c:334-339`) computes `grasp = offset + cdsp` and then `reach = grasp + cwid`. The span's upper bound is always derived by addition, never stored directly [SS-WHEREONCRUM].

**Step 2 — five-way classification:**
`intervalcmp(left, right, address)` at `tumble.c:144-160` calls `tumblercmp` twice — once against the left border, once against the right — returning TOMYLEFT / ONMYLEFTBORDER / THRUME / ONMYRIGHTBORDER / TOMYRIGHT. `whereoncrum` wraps this for POOM node traversal, and `findcbcinarea2d` in `retrie.c:229-268` uses the result to decide whether to recurse into a subtree or skip it [SS-INTERVAL-CMP, SS-WHEREONCRUM].

The primitive total order `tumblercmp` (`tumble.c:72-85`) underpins all of this: sign comparison first, then `abscmp` which compares exponents then mantissa digits lexicographically [SS-TUMBLER, INV-TUMBLER-TOTAL-ORDER].

### Home Document and Chain Position Derivation

**Field extraction — `tumblertruncate` + `tumblereq`:**
The containment check is `tumblertruncate(&A, tumblerlength(&B), &truncated)` followed by `tumblereq(&truncated, &B)`. To verify that link address `1.1.0.1.0.1.0.2.1` belongs to document `1.1.0.1.0.1`, the read path truncates to `tumblerlength` of the document address and compares [SS-TUMBLER-CONTAINMENT, PRE-ADDRESS-ALLOC]. The zero-separator convention is semantic metadata encoded in the digit stream — there is no runtime "field splitter"; containment is purely prefix length matching.

**Account-level prefix — `tumbleraccounteq`:**
Version allocation uses `tumbleraccounteq(isaptr, wheretoputit)` to distinguish owned from unowned documents — this is another form of prefix comparison, not a new primitive [SS-ADDRESS-SPACE Finding 0068, ST-VERSION-OWNERSHIP].

**Regarding the `.0.3` subspace bound:**
The upper bound `docISA.0.2.3` (or structurally equivalent) is constructed on the **write/allocation path** via `tumblerincrement(&hintptr->hintisa, 2, atomtype + 1, &upperbound)` at `granf2.c:162` — for LINKATOM (atomtype=1), this produces the bound one element-type field above the link subspace. The pure **read path** for a point lookup (`findorgl` by known ISA) navigates the B-tree with `whereoncrum` without needing to reconstruct this bound. The bound only materialises when `findpreviousisagr` executes the bounded search during allocation [SS-ADDRESS-ALLOC Finding 0065, ST-ADDRESS-ALLOC].

**Regarding last-component increment:**
`tumblerincrement` with rightshift=0 is **allocation arithmetic**, not a read primitive. On the read path you compare against existing addresses; you do not increment them. Chain position (link number N in `docISA.0.2.N`) is not extracted by any documented read API — addresses are treated as opaque ordered tokens for comparison and containment, not parsed into field components [SS-TUMBLER Finding 0031].

### Domain Enumeration

No standard read operation enumerates the full document or content store domain. All reads are bounded range queries navigated via B-tree:

- **`findcbcinarea2d`** descends only into subtrees whose `whereoncrum` classification is not TOMYLEFT or TOMYRIGHT — irrelevant subtrees are pruned at every level [SS-CONTEXT-LIST Finding 0078].
- **`FINDDOCSCONTAINING`** / `finddocscontainingsp` queries the DOCISPAN sub-index by I-address range — a targeted search in the spanfilade, not a scan of all documents [SS-DOCISPAN].
- **`findlinksfromtothreesp`** is the closest case: the orgl dimension filter is dead code (`TRUE||!homeset` makes it unconditionally use a hardcoded width-100 range), so it is effectively an unbounded orgl-dimension scan. But the span dimension (I-address) still filters via the B-tree, and the tree navigates directly to qualifying nodes rather than visiting every leaf [EC-FIND-LINKS-GLOBAL Finding 0069, PRE-FIND-LINKS].
- **`doretrievedocvspanfoo`** scans the entire POOM of a single document, but this is bounded to that one document's subtree, not the whole content store [ST-VERSION-CREATE Finding 0032].

**Summary of primitives on the read path:**

| Operation | Tumbler Primitives Used |
|---|---|
| Span membership | `tumbleradd` (reach = start + width), `tumblercmp` via `intervalcmp` |
| B-tree node traversal | `whereoncrum`: `dspadd` (grasp), `tumbleradd` (reach), `tumblercmp` |
| Containment check | `tumblerlength`, `tumblertruncate`, `tumblereq` |
| Account prefix equality | `tumbleraccounteq` (structured prefix comparison) |
| Sorted result accumulation | `intervalcmp` via `whereoncontext` in `incontextlistnd` [INV-RETRIEVAL-V-SORTED] |

The `.0.3` field boundary, last-component increment, and `tumblerincrement` belong to the allocation (write) path; the read path encounters them only as stored upper bounds already in the tree, compared against via `tumblercmp`.

---

## Code Exploration

I now have all the source evidence needed. Let me compile the full answer.

---

# Tumbler Operations on the Read Path — Full Analysis

## 1. Testing Whether an Address Falls Within a Span

The central function is `whereoncrum` [`retrie.c:345`]. Every tree-walk during retrieval calls it per crum. The exact sequence depends on the enfilade type.

### For POOM (permutation matrix) and SPAN crums

```c
case SPAN:
case POOM:
    tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);   // retrie.c:356
    cmp = tumblercmp(address, &left);                                    // retrie.c:357
    if (cmp == LESS)   return(TOMYLEFT);                                 // retrie.c:358
    if (cmp == EQUAL)  return(ONMYLEFTBORDER);                          // retrie.c:360
    tumbleradd(&left, &ptr->cwid.dsas[index], &right);                  // retrie.c:364
    cmp = tumblercmp(address, &right);                                   // retrie.c:365
```

Four primitive operations per crum:
1. **`tumbleradd(offset, cdsp, &left)`** — absolute left boundary: running offset + crum displacement.
2. **`tumblercmp(address, left)`** → TOMYLEFT / ONMYLEFTBORDER / (falls through).
3. **`tumbleradd(left, cwid, &right)`** — absolute right boundary: left + crum width (the *upper-bound add*).
4. **`tumblercmp(address, right)`** → THRUME / ONMYRIGHTBORDER / TOMYRIGHT.

### For GRAN (granfilade) crums

```c
case GRAN:
    tumbleradd(&offset->dsas[WIDTH], &ptr->cwid.dsas[WIDTH], &right);   // retrie.c:352
    return(intervalcmp(&offset->dsas[WIDTH], &right, address));          // retrie.c:353
```

No displacement step (GRAN doesn't use `cdsp` for the first axis). `intervalcmp` [`tumble.c:144`] is:

```c
cmp = tumblercmp(address, left);   // tumble.c:148
if (cmp == LESS)  return(TOMYLEFT);
if (cmp == EQUAL) return(ONMYLEFTBORDER);
cmp = tumblercmp(address, right);  // tumble.c:154
if (cmp == LESS)  return(THRUME);
if (cmp == EQUAL) return(ONMYRIGHTBORDER);
else               return(TOMYRIGHT);
```

### `tumblercmp` implementation [`tumble.c:72`]

```c
INT tumblercmp(tumbler *aptr, tumbler *bptr)
{
    if (iszerotumbler(aptr)) { ... check bptr sign ... }
    if (iszerotumbler(bptr)) { ... check aptr sign ... }
    if (aptr->sign == bptr->sign)
        return(aptr->sign ? abscmp(bptr,aptr) : abscmp(aptr,bptr));   // flip for negative
    return(aptr->sign ? LESS : GREATER);
}
```

And `abscmp` [`tumble.c:87`] compares `exp` first, then scans the mantissa array slot-by-slot from index 0 (most significant) until a difference is found or all `NPLACES` slots are exhausted.

### Upper-bound computation: `tumbleradd`

`functiontumbleradd` [`tumble.c:365`] dispatches on sign to `absadd` [`tumble.c:444`] or `strongsub`/`weaksub`. `absadd` aligns the two mantissas by their `exp` fields, concatenates them digit-by-digit (no carries — tumblers are not carried-addition numbers), and returns a justified result. This is the *only* operation used to compute span upper bounds; no increment or subtraction is needed on the upper-bound side.

---

## 2. Deriving a Link's Home Document and Chain Position

### The `.0.3` subspace boundary — only a write-side artifact

`findisatoinsertmolecule` [`granf2.c:158`] computes the exclusive upper bound for link ISAs:

```c
tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
// atomtype = LINKATOM = 2, so atomtype+1 = 3
// rightshift = 2, bint = 3
// last-nonzero-idx of docisa + 2 → upperbound = docisa.0.3
```

`tumblerincrement` [`tumble.c:599`] finds the index of the last non-zero mantissa slot, adds `bint` at `idx + rightshift`. Starting from a 4-slot docisa like `1.1.0.1` (last nonzero at slot 3), `rightshift=2` puts `3` into slot 5 → `1.1.0.1.0.3`. This upper bound is used only during *insert*, to call `findpreviousisagr` and seat the new link ISA below it.

**The read path never sees `.0.3` as a field to extract.** It is never used as an input to any retrieval function.

### Link creation: where link ISAs actually land

For the first link under `docisa` [`granf2.c:165–176`]:
```c
if (tumblerlength(&hintptr->hintisa) == tumblerlength(&lowerbound)) {
    tumblerincrement(&lowerbound, 2, hintptr->atomtype, isaptr);  // docisa.0.2
    tumblerincrement(isaptr, 1, 1, isaptr);                        // docisa.0.2.1 (last-nonzero+1 shift)
}
```

Subsequent links use `tumblerincrement(&lowerbound, 0, 1, isaptr)` — adds 1 at `idx+0` (i.e., the last non-zero slot), yielding `docisa.0.2.2`, `docisa.0.2.3`, … So link ISAs live in the `[docisa.0.2.1, docisa.0.3)` interval, serially at the last component.

### Following a link: home-document extraction

`dofollowlink` [`do1.c:223`]:
```c
link2sporglset(taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
&& linksporglset2specset(taskptr, &((typesporgl*)sporglset)->sporgladdress,
                         sporglset, specsetptr, NOBERTREQUIRED)
```

`link2sporglset` [`sporgl.c:67`]:
```c
findorgl(taskptr, granf, linkisa, &orgl, type);    // point-lookup in granfilade
tumblerclear(&zero);
tumblerincrement(&zero, 0, whichend, &vspan.stream);   // mantissa[0] = whichend (1, 2, or 3)
tumblerincrement(&zero, 0, 1,        &vspan.width);    // mantissa[0] = 1
context = retrieverestricted((typecuc*)orgl, &vspan, V, NULL, I, NULL);
```

The two `tumblerincrement`-from-zero calls build the V-span `[whichend, whichend+1)`. This is the *only* tumbler arithmetic on the link side of follow-link; there is no decomposition of the link ISA. The `whichend` values are LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3 [`xanadu.h:36–38`].

`retrieverestricted` [`retrie.c:56`] then computes `span1end` as:
```c
tumbleradd(&span1start, &span1ptr->width, &span1end);   // retrie.c:65
```
→ `tumbleradd({whichend}, {1}, &end)` = `{whichend+1}`. The subsequent tree walk uses `whereoncrum` exactly as described in §1, on the V-axis (index=V=1) of the link's POOM.

### Home document: read from crum, not computed from ISA

`contextintosporgl` [`sporgl.c:205`]:
```c
movetumbler(&context->context2dinfo.homedoc, &sporglptr->sporgladdress);
movetumbler(&context->totaloffset.dsas[I],   &sporglptr->sporglorigin);
movetumbler(&context->contextwid.dsas[I],    &sporglptr->sporglwidth);
```

The `homedoc` is a field in the POOM's `type2dbottomcruminfo` (`c2dinfo.homedoc`), stored at insertion time by `insertspanf` [`spanf1.c:33`]:
```c
movetumbler(&((typesporgl*)sporglset)->sporgladdress, &linfo.homedoc);
```

**The home document is never derived by arithmetic on the link ISA during reading.** It is stored directly in the bottom crum and read out via `movetumbler`. No tumbler addition, subtraction, or field stripping is performed on the link's own address to find the document it belongs to.

### Chain position (from/to/three) in the spanfilade

When `sporglset2linksetinrange` [`sporgl.c:239`] identifies a link via the spanfilade, it calls:
```c
beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
```

`beheadtumbler` [`tumble.c:673`]:
```c
movetumbler(aptr, &temp);
++temp.exp;                          // shift the entire mantissa one position left (discard first digit)
if (aptr->exp == 0)
    temp.mantissa[0] = 0;
tumblerjustify(&temp);
movetumbler(&temp, bptr);
```

This strips the leading spantype prefix (1, 2, or 3) from the spanfilade ORGLRANGE key, recovering the raw link ISA. The prefix was placed there at insert time by `prefixtumbler` [`tumble.c:641`]:
```c
temp1.mantissa[0] = bint;           // spantype digit
temp2.exp -= 1;                     // shift docisa right by one story
tumbleradd(&temp1, &temp2, cptr);   // concatenate
```

Similarly, `finddocscontaining` [`spanf1.c:174`] calls `beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &document.address)` to strip the DOCISPAN=4 prefix and recover the document ISA.

So the tumbler operations around the spanfilade ORGLRANGE axis are:
- **At insert**: `prefixtumbler` → `exp -= 1` + `tumbleradd`.
- **At read**: `beheadtumbler` → `exp += 1` + `tumblerjustify`.

---

## 3. Does Any Read Operation Enumerate the Document or Content Store Domain?

**No read operation enumerates the full granfilade domain.**

`fetchorglgr` [`granf2.c:22`] is a pure point lookup:
```c
if (tumblercmp(&((typecuc*)fullcrumptr)->cwid.dsas[WIDTH], address) == LESS)
    return(NULL);                                                 // fast reject: address beyond tree
context = retrievecrums((typecuc*)fullcrumptr, address, WIDTH);  // walk to the exact slot
if (!tumblereq((tumbler*)&context->totaloffset, address)) {      // exact-match check
    crumcontextfree(context);
    return(NULL);
}
```

It calls `tumblercmp` once as a fast reject against the tree's total width, then walks to the leaf and verifies with `tumblereq` (field-by-field equality of all `NPLACES` mantissa slots plus sign/exp [`tumble.c:24`]).

`findpreviousisagr` [`granf2.c:255`], which walks the granfilade to find the highest ISA below an upper bound, **is called only from `findisatoinsertgr`** during insert operations. No read-path function calls it.

**Bounded range scans do occur**, but they are always constrained by caller-provided spans:

- `retrieveinarea` → `findcbcinarea2d` [`retrie.c:229`]: walks all crums that `crumqualifies2d` accepts — a 2D intersection test within the given `[span1start, span1end) × [span2start, span2end)` box.
- `retrieveinspan` → `findcbcinspanseq` [`retrie.c:307`]: scans within `[spanstart, spanend)`.
- `finddocscontaining` → issues `retrieverestricted(spanf, &docspace, ORGLRANGE, ispanset, SPANRANGE, NULL)` where `docspace` covers `[DOCISPAN, DOCISPAN+1) = [4,5)` in the ORGLRANGE axis, constrained further by the caller's `ispanset` on the SPANRANGE axis. This collects all document ISAs whose content overlaps the given spans — it enumerates *matching* documents within the caller's constraint, not the full domain.

The granfilade (content/document store) is never scanned as a whole. Every access either exits immediately (width comparison), walks to an exact point (`retrievecrums`/`findcbcseq`), or scans within a caller-bounded span rectangle (`findcbcinarea2d`/`findcbcinspanseq`).

---

## Summary Table

| Operation | Tumbler primitives used | Enumerates? |
|---|---|---|
| Span membership per crum (POOM/SPAN) | `tumbleradd`×2, `tumblercmp`×2 | No — membership only |
| Span membership per crum (GRAN) | `tumbleradd`×1, `tumblercmp`×2 via `intervalcmp` | No |
| Span upper-bound computation | `tumbleradd(stream, width, &end)` | N/A |
| Granfilade point lookup (`fetchorglgr`) | `tumblercmp` (fast reject), `tumblereq` (exact match) | No |
| Follow-link: chain position select | `tumblerincrement`×2 from zero → V-span `[whichend, whichend+1)` | No |
| Follow-link: home doc extraction | `movetumbler` from `c2dinfo.homedoc` (no arithmetic) | No |
| Spanfilade key strip (`beheadtumbler`) | `++exp` + `tumblerjustify` | N/A |
| Spanfilade key build (`prefixtumbler`) | `exp -= 1` + `tumbleradd` | N/A |
| `finddocscontaining` | bounded 2D scan; `beheadtumbler` per hit | Within caller span only |
| `.0.3` subspace bound (write only) | `tumblerincrement(&docisa, 2, 3, &ub)` | Write-only, not read |
