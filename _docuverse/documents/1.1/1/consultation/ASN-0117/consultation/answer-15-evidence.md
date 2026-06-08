## Question 15 [evidence]

> Does DELETE leave the granfilade entirely untouched, such that the I-addresses underlying the deleted span remain resolvable to their original bytes even though no POOM currently references them?

## KB Synthesis

Yes, unconditionally. DELETE is a pure POOM operation and the granfilade is a strict frame condition for it.

**What DELETE actually touches**

`dodeletevspan` → `deletevspanpm` → `deletend` performs tree surgery on the document's POOM enfilade only: bottom crums within the deletion range are `disown`ed and `subtreefree`d; crums after the range have their V-displacement shifted. No call to any granfilade function exists in that path. [ST-DELETE Finding 0057, FC-GRANF-ON-DELETE Finding 0061]

**The granfilade is append-only by architecture**

The granfilade has no delete operation. `inserttextingranf` allocates I-addresses forward-only; `findpreviousisagr` finds the current maximum and increments. After DELETE, that same `findpreviousisagr` call still finds the "deleted" I-addresses as the highest existing entries and allocates above them — they are never reused. [INV-NO-IADDR-REUSE, INV-MONOTONIC Finding 0061]

**I-addresses remain resolvable**

Because the granfilade is untouched, the bytes at those I-addresses are still there. `ispanset2vstuffset(granf, deleted_ispan)` would still return the original bytes — the permascroll content is permanent. What's gone is only the V→I mapping in the POOM that told you *where in document space* those bytes appeared. [INV-IADDR-IMMUTABILITY Finding 0064]

**Observable consequences**

- `FINDDOCSCONTAINING` still returns the document after deletion (spanfilade also untouched, since `dodeletevspan` has no spanf call). [INV-IADDRESS-PERMANENT Finding 0023, INT-DELETE-SPANF-DIVERGENCE Finding 0057]
- `compare_versions` between pre- and post-delete states reports the deleted span as belonging only to the pre-delete version, because that version's POOM still maps to those I-addresses while the current document's POOM does not. [SS-DUAL-ENFILADE Finding 0023]
- Identity-preserving restoration is possible: `COPY` from any document that still maps those I-addresses (e.g., a version taken before the delete) places them back into the POOM with the same I-addresses, restoring transclusion links and `compare_versions` relationships. [ST-COPY Finding 0064]

**The formal invariant**

```
delete(D, vspan) ⟹
  granfilade_after = granfilade_before          -- bytes permanent
  spanfilade_after = spanfilade_before          -- index permanent
  poom(D)_after = poom(D)_before \ {vspan mappings}  -- only mapping gone
```

[FC-GRANF-ON-DELETE, INV-SPANF-WRITE-ONLY, ST-DELETE Finding 0064]

---

## Code Exploration

I have everything I need. Here is the full answer.

---

## Does DELETE Leave the Granfilade Untouched?

**Yes — DELETE never modifies the granfilade. I-addresses remain valid and resolvable to their original bytes after deletion, regardless of whether any POOM node still references them.**

---

### The DELETE Execution Path

**Entry: `fns.c:333–347`**
```c
void deletevspan(typetask *taskptr)
{
  typeisa docisa;
  typespan vspan;
  bool getdeletevspan(), dodeletevspan();
 
    (void) getdeletevspan (taskptr, &docisa, &vspan);
    putdeletevspan (taskptr);
    if (!dodeletevspan (taskptr, &docisa, &vspan))
        fprintf(stderr,"deletevspan failed \n");
}
```
Parses the request, then delegates entirely to `dodeletevspan`.

---

**`do1.c:158–167` — `dodeletevspan`:**
```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
  bool findorgl(), deletevspanpm();

    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr));
}
```
`findorgl` resolves the document's ISA address to its POOM enfilade root. `deletevspanpm` operates on that POOM root. Neither call writes to the granfilade.

---

**`orglinks.c:145–152` — `deletevspanpm`:**
```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```
The target of `deletend` is `docorgl` — the POOM enfilade — and the dimension is `V` (V-space). The granfilade is not passed, not referenced.

---

**`edit.c:31–76` — `deletend`:**

This is the structural heart of DELETE. The comment at the top of `edit.c` is decisive: there are **two** delete functions in this file:

- **`deleteseq` (`edit.c:16`)** — comment: `/* use with GRAN */`
- **`deletend` (`edit.c:31`)** — comment: `/* use with SPAN and POOM */`

DELETE calls `deletend`, never `deleteseq`. The granfilade has its own separate delete primitive (`deleteseq`) that is never invoked during a document span deletion.

`deletend` operates as follows:
```c
makecutsnd (fullcrumptr, &knives);            // cut the POOM tree at span boundaries
newfindintersectionnd (fullcrumptr, &knives, &father, &foffset);
for (ptr = (typecuc *) findleftson (father); ptr; ptr = next) {
    next = (typecuc *) findrightbro((typecorecrum*)ptr);
    switch (deletecutsectionnd ((typecorecrum*)ptr, &fgrasp, &knives)) {
      case 1:
        disown ((typecorecrum*)ptr);
        subtreefree ((typecorecrum*)ptr);   // free POOM crums inside span
        break;
      case 2:
        tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
        break;                              // adjust offset of boundary crums
    }
}
setwispupwards (father,1);
recombine (father);
```
All mutations are to the POOM enfilade tree: freeing POOM crums inside the deleted region (case 1) or adjusting V-space offsets of crums that straddle the boundary (case 2).

---

**`credel.c:413–431` — `subtreefree` (called from `deletend` case 1):**
```c
void subtreefree(typecorecrum *ptr)
{
    if (ptr->height > 0) {
        for (p = ((typecuc *)ptr)->leftson; p; p = right) {
            disown (p);
            subtreefree (p);
        }
    } else if (ptr->cenftype == GRAN
               && ((typecbc *)ptr)->cinfo.infotype == GRANORGL
               && ((typecbc *)ptr)->cinfo.granstuff.orglstuff.orglincore)
        orglfree (((typecbc *)ptr)->cinfo.granstuff.orglstuff.orglptr);
    freecrum (ptr);
}
```
There is a GRAN path here (`cenftype == GRAN`), but it is **never reached during a POOM delete**. The crums being freed during `deletend` on a POOM orgl are POOM crums — they have `cenftype == POOM`. The `cenftype == GRAN` branch fires only when freeing a GRAN bottom crum that cached a document orgl in memory; that is a different operation entirely.

---

### How Retrieval by I-Address Works (Independent of POOM)

**`retrie.c:33–54` — `retrieve`:**
```c
typecontext *retrieve(typecuc *fullcrumptr, tumbler *address, INT index)
{
    switch (fullcrumptr->cenftype) {
      case GRAN:
            return (findcbcseq ((typecorecrum*)fullcrumptr, &offset, address));
      case SPAN:
      case POOM:
            return (findcbcnd ((typecorecrum*)fullcrumptr, &offset, address, index));
    }
}
```
GRAN retrieval uses `findcbcseq`, which traverses the granfilade purely by tumbler address (I-address), with no reference to any POOM. The granfilade is a self-contained sequential enfilade indexed by I-space. Resolving an I-address requires only the granfilade root (`granf`) and the tumbler — the POOM plays no role.

---

### Conclusion

The answer is **yes, unambiguously**: DELETE leaves the granfilade entirely untouched.

The architectural separation is explicit and intentional. `edit.c` maintains two distinct deletion primitives — `deleteseq` (for GRAN) and `deletend` (for SPAN and POOM) — and the DELETE operation path calls only the latter. No code path from `deletevspan` → `dodeletevspan` → `deletevspanpm` → `deletend` → `subtreefree` ever writes to, frees, or modifies a GRAN crum.

I-addresses are permanent tumbler coordinates into the granfilade. After a DELETE removes all POOM references to a span of content, that content's I-addresses continue to resolve correctly through `retrieve` → `findcbcseq` on the unchanged granfilade. The bytes are still there; only the mapping from V-space to I-space (stored in the POOM) has been severed.
