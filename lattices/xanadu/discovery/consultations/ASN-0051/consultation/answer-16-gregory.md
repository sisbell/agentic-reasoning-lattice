## Question 16 [gregory]

> When a link's endset references I-addresses shared by three documents (original, version, and transclusion target), and the original document deletes that content, does `find_links` still discover the link from both the version and the transclusion target independently — confirming that link discovery is purely I-address intersection against the spanfilade with no provenance tracking back to the creating document?

## KB Synthesis

Yes — both the version and the transclusion target independently discover the link after the original's deletion, and the mechanism is purely I-address intersection with no provenance tracking.

## Why deletion from the original doesn't affect the other documents

DELETE modifies only the originating document's POOM [ST-DELETE, Finding 0064]. The V-to-I mappings for α are removed from O's POOM, but [FC-DELETE-CROSS-DOC] establishes the frame condition explicitly: `∀ D' ≠ D : delete(D, vspan) ⟹ poom(D') = poom_before(D')`. The version's POOM and the transclusion target's POOM are unchanged.

## Why the spanfilade still indexes the link

The spanfilade is write-only [INV-SPANF-WRITE-ONLY]. No `deletespanf` function exists anywhere in `spanf1.c` or `spanf2.c`. The entries mapping α → link L, written by `insertendsetsinspanf` during `docreatelink`, persist unconditionally. DELETE has no call path into any spanfilade removal function [ST-DELETE, Finding 0057]:

> `DELETE (dodeletevspan → deletevspanpm → deletend)` — no code path touches the link orgl or spanfilade entries.

The invariant: `spanf_entries_after(DELETE) = spanf_entries_before(DELETE)`.

## How discovery works from V and T

`find_links` converts the query specset to I-addresses, then intersects against the spanfilade [SS-FIND-LINKS, Finding 0028]. Since V and T both retain POOM entries mapping V-positions to α, their content spans successfully convert to α, the spanfilade intersection returns link L, and the link is found. The original's deletion is irrelevant to either query.

This is confirmed by [INV-LINK-GLOBAL-VISIBILITY]:

> A link created in any document is discoverable from every document in the system that shares the linked content's identity.

And [INT-LINK-VERSION, Finding 0046]:

> Version creates text I-address sharing, and `find_links` operates in I-space via the spanf index — shared I-addresses cause the version to "inherit" link discoverability.

## No provenance tracking back to the creating document

This is confirmed by [EC-FIND-LINKS-GLOBAL] and [PRE-FIND-LINKS, Finding 0069]. The `sporglset2linkset()` function contains a `TRUE||!homeset` guard that permanently overrides whatever orgl-range (document-scoping) parameter the caller passes, replacing it with a hardcoded unbounded range. The orgl dimension filter — which was designed to restrict results to a particular document's links — is disabled. All `find_links` calls are effectively global searches in the orgl dimension, filtered only on the span dimension (I-address content matching).

The result: link discovery is exactly `{L | endpoint_iaddrs(L) ∩ query_iaddrs ≠ ∅}` — pure I-address set intersection against the spanfilade — with no regard for which document originally created the link or which document's POOM currently contains those I-addresses.

## Summary

After O deletes content at α:
- O's POOM: α unmapped → `find_links(O content)` returns `[]`
- V's POOM: α still mapped → `find_links(V content)` returns `{L}` ✓
- T's POOM: α still mapped → `find_links(T content)` returns `{L}` ✓
- Spanfilade: α → L entry intact, forever

Both documents independently confirm the link. The discovery requires only that the querying document's V-positions still map to α (providing the I-address for the spanfilade lookup) and that the spanfilade entry exists — neither of which is affected by O's deletion.

---

## Code Exploration

---

## Answer

**Yes — confirmed.** `find_links` discovers the link independently from both the version and the transclusion target after the original deletes that content. Link discovery is purely I-address intersection against the spanfilade with no provenance tracking. Here is the complete code-traced proof.

---

### 1. What the Spanfilade Stores at Link Creation

`docreatelink` [`do1.c:195-221`]:
```c
specset2sporglset(taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
insertendsetsinspanf(taskptr, spanf, linkisaptr, fromsporglset, tosporglset, ...)
```

`insertspanf` [`spanf1.c:15-54`] — for each SPORGLID item in the sporglset:
```c
movetumbler(&((typesporgl *)sporglset)->sporglorigin, &lstream);   // I-address start
movetumbler(&((typesporgl *)sporglset)->sporglwidth,  &lwidth);    // I-address width
movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);                // SPANRANGE key
// ORGLRANGE key = spantype-prefixed link ISA
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

The spanfilade crum stores `(I-address range) → (link ISA)`. No V-address is stored. No creating-document identifier is stored in the key.

---

### 2. What DELETE Does — and Does Not Do

`dodeletevspan` [`do1.c:158-167`] → `deletevspanpm` [`orglinks.c:145-152`]:
```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`deletend` is called on `docorgl` — the *original document's own POOM* (2D enfilade in granf), operating in the `V` dimension. There is no call to any spanf function. There is no `deletespanf` function anywhere in the codebase (confirmed in Finding 0057 — the spanfilade is write-only).

**Effect:** The original document's V→I mapping for the deleted span is removed. The spanfilade entry `(I₁..I₂) → L` is permanently intact.

---

### 3. How find_links Converts the Query to I-Addresses

`dofindlinksfromtothree` [`do1.c:348-353`] → `findlinksfromtothreesp` [`spanf1.c:56-103`]:
```c
if (fromvspecset)
    specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
```

`specset2sporglset` → `vspanset2sporglset` [`sporgl.c:35-65`]:
```c
if (!findorgl(taskptr, granf, docisa, &orgl, type)) return NULL;
for (; vspanset; vspanset = vspanset->next) {
    vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);  // V→I via THIS doc's POOM
    // package as sporgls...
}
```

`docisa` here is the ISA of the **requesting document** — version V, or transclusion target T. `findorgl` retrieves *that document's* granfilade POOM. `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` maps V-positions to I-addresses using *that document's* POOM.

V's POOM was written at `docreatenewversion` time [`do1.c:260-298`] via `docopyinternal` which called `insertpm` — mapping V_v → I₁..I₂. T's POOM was written at `docopy` time mapping V_t → I₁..I₂. Neither POOM was touched by O's `deletevspanpm`. Both still map their V-addresses to I₁..I₂.

---

### 4. The Homedoc Provenance Filter Is Permanently Disabled

`sporglset2linksetinrange` [`sporgl.c:239-268`]:
```c
infoptr = &linfo;
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    if (FALSE/*trying to kluge links followable thru versions */
        && ((typeitemheader *)sporglset)->itemid == SPORGLID) {
        infoptr = &linfo;
        movetumbler(&((typesporgl *)sporglset)->sporgladdress, &linfo.homedoc);
    } else
        infoptr = NULL;        // ← always executed — infoptr is ALWAYS NULL
    context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                                 &range, ORGLRANGE, (typeisa*)infoptr);  // NULL always
```

The guard `if (FALSE && ...)` is dead code. The branch that would load a `homedoc` into `linfo` is unreachable. `infoptr` is always `NULL`.

The comment records a deliberate design choice: an attempt to filter by source document was tried ("trying to kluge links followable thru versions") and then abandoned by hardcoding `FALSE`.

The downstream enforcement point is `findcbcinarea2d` [`retrie.c:274-280`]:
```c
if ((crumptr->height == 0) && infoptr
    && !tumblereq(&infoptr->homedoc, &(((type2dcbc *)crumptr)->c2dinfo.homedoc))) {
    return (FALSE);
}
```

With `infoptr == NULL`, the `&& infoptr` short-circuits to false and the homedoc equality check is **never reached**. The spanfilade traversal returns every crum whose I-address range intersects the query, regardless of which document was the "source" when the link was created.

---

### 5. State After O Deletes Its Content

| Data Structure | State |
|---|---|
| O's POOM (granf) | V→I entry for deleted span: **removed** by `deletend` |
| V's POOM (granf) | V→I entry for same I₁..I₂: **intact** — different `docorgl` pointer |
| T's POOM (granf) | V→I entry for same I₁..I₂: **intact** — different `docorgl` pointer |
| Spanfilade entry | `SPANRANGE[I₁..I₂] → L (LINKFROMSPAN)`: **intact, permanent** |

`find_links` queried with V's V-addresses: V's POOM maps V_v → I₁..I₂ → sporglset non-empty → spanfilade query succeeds → **L found**.

`find_links` queried with T's V-addresses: T's POOM maps V_t → I₁..I₂ → sporglset non-empty → spanfilade query succeeds → **L found**.

`find_links` queried with O's (now-deleted) V-addresses: O's POOM has no mapping → `vspanset2ispanset` returns nothing → sporglset empty → nothing queried → **L not found** (not because of a provenance check, but because the V→I translation returns an empty set).

---

### Conclusion

The answer to both parts of the question is **yes**:

1. **`find_links` discovers the link from both V and T independently after O deletes the content.** The delete modifies only O's POOM. The spanfilade is permanent and untouched. V's and T's POOMs remain intact, so their V→I conversion still produces I₁..I₂, which the spanfilade matches to L.

2. **This confirms that link discovery is purely I-address intersection against the spanfilade with no provenance tracking.** The one code path that could have introduced provenance filtering — the `infoptr`/homedoc check at `sporgl.c:251` — is permanently dead via `if (FALSE && ...)`. The spanfilade stores I-address ranges as keys; retrieval is purely geometric intersection in I-space. No "creating document", "current hosting document", or "version lineage" participates in the query.

The author's own comment at `sporgl.c:251` — *"trying to kluge links followable thru versions"* — is the fossil record of the moment this property was explicitly chosen: the filter was attempted, found to break cross-transclusion link discovery, and disabled.
