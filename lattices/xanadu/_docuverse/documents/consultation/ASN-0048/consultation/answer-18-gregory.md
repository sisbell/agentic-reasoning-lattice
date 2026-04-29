## Question 18 [gregory]

> When a COPY operation inserts transcluded content into a document (reusing existing I-addresses rather than allocating new ones), does the target POOM's `insertpm` follow the exact same code path as text INSERT — including `makegappm` shifting and `isanextensionnd` coalescing — or is there a separate insertion path for copied content?

## KB Synthesis

Yes, COPY follows the exact same POOM insertion code path as text INSERT. The KB is explicit on both points.

## Same code path: `insertpm` → `insertnd` → `makegappm`

[ST-INSERT] Finding 0052 states directly:

> INSERT, COPY, and CREATELINK all share the same POOM insertion mechanism: `insertpm` → `insertnd` → `makegappm`.

The `docopy()` call chain is confirmed in [ST-INSERT] Finding 0036 (`do1.c:45-65`): `docopy` → `insertpm` → `insertnd` → `makegappm`. The shifting behavior — classifying crums via `insertcutsectionnd` and applying `tumbleradd` to entries in the shift region `[blade[0], blade[1])` — is identical for COPY and INSERT.

## `isanextensionnd` coalescing applies, but with a `homedoc` constraint

[ST-VCOPY] Finding 0046 confirms that `isanextensionnd` runs during COPY:

> The function `isanextensionnd()` checks two conditions: (1) the new mapping has the same `homedoc` as an existing crum, and (2) the new mapping starts exactly where the existing crum ends (contiguous in both V and I dimensions). If both hold, the existing crum's width is extended in place.

The critical difference from text INSERT: `homedoc` must match. Since COPY reuses I-addresses that originated in another document, the `homedoc` field encodes the I-address origin document. Consecutive COPYs from **different** source documents will never coalesce even if they land at contiguous V-positions, because `isanextensionnd` fails on the homedoc check. COPYs from the **same** source document will coalesce if V- and I-contiguity both hold.

## Summary

| Property | Text INSERT | COPY |
|----------|-------------|------|
| `insertpm` → `insertnd` → `makegappm` | ✓ | ✓ |
| `makegappm` shifting of subsequent crums | ✓ | ✓ |
| `isanextensionnd` coalescing | ✓ (same homedoc = same doc) | ✓ (only if homedoc matches) |
| Allocates new I-addresses | ✓ | ✗ (reuses existing) |

The POOM layer is completely agnostic to whether I-addresses are fresh or reused — it operates on `(V-position, I-address)` pairs and applies the same structural logic either way. The distinction between INSERT and COPY is entirely at the layer above: INSERT calls `inserttextingranf` to mint new I-addresses, while COPY receives them from `specset2ispanset` on the source document. [INV-IADDR-PROVENANCE]

---

## Code Exploration

## COPY vs INSERT: POOM Insertion Code Path Analysis

**Short answer: COPY and INSERT converge to the same `insertpm` code path.** The only divergence is upstream I-address sourcing. Everything from `insertpm` onward — including `makegappm` shifting and `isanextensionnd` coalescing — is identical.

---

### Entry Points (fns.c)

**INSERT** handler (`fns.c:84`):
```
insert() → doinsert() → inserttextingranf() [allocates new I-addrs] → docopy()
```

**COPY** handler (`fns.c:35`):
```
copy() → docopy() [directly, with source I-addrs from specset]
```

`doinsert` in `do1.c` calls `inserttextingranf` to mint new I-addresses, then calls `docopy` with the result. The COPY handler calls `docopy` directly with the source document's existing I-addresses. **Both converge into `docopy`.**

---

### docopy — Shared Spine (do1.c:45–65)

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
  ...
  return (
    specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
    && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && acceptablevsa (vsaptr, docorgl)
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)   // do1.c:60
    && insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
    ...
  );
}
```

`docopy` does not inspect whether the I-spans are newly allocated or transclusion-reused. It calls `insertpm` identically in both cases.

---

### insertpm — Iterates I-spans (orglinks.c:75–134)

For each I-span in the sporglset, `insertpm` calls:

```c
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // orglinks.c:130
```

`crumorigin` encodes both the V-position (`vsaptr`) and the I-address (`lstream`). There is no branch on "is this transcluded content?" — both INSERT and COPY hit this line identically.

---

### insertnd — Gap-making and Dispatch (insertnd.c:15–76)

```c
case POOM:
    makegappm (taskptr, fullcrumptr, origin, width);   // insertnd.c:54
    ...
    bothertorecombine = doinsertnd(fullcrumptr, origin, width, infoptr, index);  // insertnd.c:57
    break;
```

`makegappm` is called unconditionally for POOM nodes, regardless of whether content is text or transclusion.

---

### makegappm — V-address Shifting (insertnd.c:124–172)

`makegappm` finds elements after the insertion point and shifts their V-addresses:

```c
case 1:
    tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);  // insertnd.c:162
    ivemodified (ptr);
    break;
```

`findaddressofsecondcutforinsert` (`insertnd.c:174`) computes the boundary for which elements need shifting. Both INSERT and COPY trigger this path for any non-extension insertion.

---

### insertcbcnd — isanextensionnd Coalescing (insertnd.c:242–275)

```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {  // insertnd.c:250
        dspadd (&ptr->cwid, width, &ptr->cwid, ...);                // insertnd.c:251
        ivemodified (ptr);
        ...
        return(FALSE);  // coalesced — no new crum created
    }
}
// else: createcrum(), adopt()
```

`isanextensionnd` (`insertnd.c:301–309`) checks two conditions:
1. `infoptr->homedoc` matches the existing crum's home document
2. The existing crum's reach equals the new insertion's origin (contiguity)

For a COPY of content from document X into document Y, the `homedoc` of the incoming I-spans is X. If the POOM already contains a crum from X reaching to exactly the right I-address, coalescing fires and the existing crum is widened rather than a new one created. This is the **same coalescing logic** used when inserting adjacent text via INSERT — the only difference is what `homedoc` the I-addresses carry.

---

### Full Execution Stack (both operations)

```
insert()/copy()
  └─ docopy()                          do1.c:45
       └─ insertpm()                   orglinks.c:75
            └─ insertnd()              insertnd.c:15
                 ├─ makegappm()        insertnd.c:54   ← V-address shifting
                 └─ doinsertnd()       insertnd.c:57
                      └─ insertmorend()
                           └─ insertcbcnd()            insertnd.c:242
                                ├─ isanextensionnd()   insertnd.c:250  ← coalescing
                                └─ createcrum()/adopt()               ← new crum
                 └─ recombine()        insertnd.c:76   ← tree rebalancing
```

---

### Conclusion

COPY does **not** have a separate POOM insertion path. From `insertpm` downward, transcluded content follows the exact same code — `makegappm` shifting (`insertnd.c:54,162`), `isanextensionnd` coalescing (`insertnd.c:250–309`), and `recombine` rebalancing (`insertnd.c:76`) — as text INSERT.

The sole architectural difference is upstream: INSERT calls `inserttextingranf` to allocate fresh I-addresses in the granfilade before entering `docopy`; COPY enters `docopy` directly with pre-existing source I-addresses. Once inside `docopy`, both are structurally indistinguishable.
