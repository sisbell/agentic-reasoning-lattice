## Question 6 [evidence]

> Does the udanax-green link allocator (or ASN-0043's link-store model it synthesizes) carry any `E_doc` notion distinct from `dom(M)` for scoping link home documents, or has document scope always been keyed on the arrangement-function domain?

## KB Synthesis

## Link Allocator Scope: Granfilade ISA Hierarchy, Not `dom(M)`

The KB is unambiguous: document scope for link home-document allocation is keyed on the **granfilade's ISA address structure**, entirely independent of `dom(M)` (the POOM arrangement-function domain).

### How link allocation is scoped

`findisatoinsertmolecule` computes link I-addresses by [SS-ADDRESS-ALLOC / Finding 0065]:

1. Setting `upperbound = docISA.2.3` — bounding the search to the document's link element subspace in the granfilade
2. Calling `findpreviousisagr` on the **granfilade tree** to find the highest existing link I-address below that bound
3. Incrementing to produce the next address

The resulting link I-address has the structure `account.0.document.0.2.element_number` — a permanent tumbler prefix derived from the home document's ISA [SS-LINK-HOME-DOCUMENT, Finding 0025].

### Why `dom(M)` is the wrong abstraction here

`dom(M)` — the current V-addresses mapped in the document's POOM — is **mutable state** [SS-POOM-MUTABILITY]. It contracts on DELETE, expands on INSERT, and reorganizes on REARRANGE. It lives in the POOM enfilade, not the granfilade.

Link address allocation queries the **granfilade** only. The POOM is never consulted during `findisatoinsertmolecule`. As [INV-MONOTONIC / Finding 0061] confirms, the granfilade is append-only and DELETE never touches it — so the address scope is permanent and unaffected by any POOM mutation.

The isolation is per-document and per-element-field, not per-POOM-domain [Finding 0065]:
> "the new link's I-address is strictly greater than all existing link I-addresses in the same document, and independent of link I-addresses in other documents"

### The two concepts in contrast

| Concept | Structure | Mutability | Used for |
|---------|-----------|-----------|----------|
| `dom(M)` (POOM domain) | V-addr set in POOM | Mutable (INSERT/DELETE/REARRANGE) | Content retrieval, V→I conversion |
| Link home-doc scope | ISA prefix in granfilade | Permanent | Link I-address allocation bounds |

### Conclusion

There is no distinct `E_doc` scoping mechanism in the link allocator beyond tumbler containment under the home document's ISA in the granfilade. Document scope for link allocation has always been keyed on the **granfilade address hierarchy** — specifically the `docISA.2.x` prefix range — never on the arrangement-function domain. The POOM domain participates only in link *discovery* (`find_links` via I-address intersection [SS-FIND-LINKS, SS-SPANF-OPERATIONS]), not in link *allocation*.

---

## Code Exploration

---

## `E_doc` vs `dom(M)` in the Link Allocator

**Short answer:** No separate `E_doc` exists. Document scope has always been keyed on a single document ISA tumbler — `homedoc` — which simultaneously serves as both the arrangement-function domain key and the link-ownership scope. The implementation conflates the two roles, and several surviving comments name the tension explicitly.

---

### The only "document scope" field

```c
/* wisp.h:107-109 */
typedef struct struct2dbottomcruminfo {
        tumbler homedoc;
} type2dbottomcruminfo ;
```

Every 2-D bottom crum (SPAN and POOM index) carries exactly this one tumbler. There is no second field, no `edoc`, no `restrictionDoc`, no separate `dom_M`. The word `E_doc` appears nowhere in any source file.

---

### How `homedoc` is written at link-creation time

`createlink` → `docreatelink` [do1.c:195] receives the caller-supplied `docisaptr` and does two things with it that are logically distinct but use the same value:

**1. Bounds the I-address allocation for the new link** [do1.c:207]:
```c
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
createorglingranf (taskptr, granf, &hint, linkisaptr)
```
`makehint` copies `docisaptr` into the hint, which `findisatoinsertmolecule` (granf2.c) uses as the upper-bound ceiling when searching for the next available link I-address. The new link's ISA therefore lives inside `docISA.2.x` — the document's link subspace. This is `dom(M)` reasoning: the domain of this document's arrangement function defines where links can be allocated.

**2. Provides the virtual address to copy into** [do1.c:211-212]:
```c
findnextlinkvsa (taskptr, docisaptr, &linkvsa)
docopy (taskptr, docisaptr, &linkvsa, ispanset)
```
Same `docisaptr` scopes the virtual address search and the copy target.

Then at span-index insertion time [spanf1.c:29 and :33], whichever sporgl variant is in play, the same document ISA lands in `homedoc`:
```c
movetumbler (isaptr, &linfo.homedoc);                               /* spanf1.c:29 */
movetumbler (&((typesporgl *)sporglset)->sporgladdress, &linfo.homedoc);  /* spanf1.c:33 */
```

---

### How `homedoc` is read at follow-link time

`dofollowlink` [do1.c:229-231] extracts `sporgladdress` from the stored sporgl and passes it as `homedoc` to `linksporglset2specset` → `sporglset2vspanset` [sporgl.c:141], where it is used to look up the document's arrangement function:

```c
(void) findorgl (taskptr, granf, homedoc/*&sporglptr->sporgladdress*/, &orgl, type);
                                                                   /* sporgl.c:152 */
…
vspansetptr = ispan2vspanset (taskptr, orgl, &ispan, vspansetptr);
```

`findorgl` retrieves the orgl **for that document** — the orgl *is* the arrangement function M. So `homedoc` is literally the key into the granfilade that returns `M`. There is no intermediate `E_doc` step: `homedoc == dom(M)` by direct lookup.

The commented-out alternative makes the conflation visible. The original form would have read `&sporglptr->sporgladdress` directly; it was replaced with the parameter `homedoc`, which is the same tumbler by the time it arrives but travels through a different binding:
```c
movetumbler (homedoc/*&sporglset->sporgladdress*/, &specptr->docisa);   /* sporgl.c:134 */
```

---

### Three surviving comments name the conceptual seam

| Location | Comment | What it reveals |
|----------|---------|----------------|
| `retrie.c:78` | `&info.homedoc/*shouldberestrictiondoc*/` | Retrieval restriction was always meant to be a named "restrictionDoc" role, not just `homedoc` |
| `sporgl.c:152` | `homedoc/*&sporglptr->sporgladdress*/` | Once considered reading the stored `sporgladdress` directly; switched to the passed-in `homedoc` parameter |
| `sporgl.c:187` | `&infoptr->homedoc /* should be sourcedoc */` | When unpacking a stored sporgl, the field should logically be called "sourcedoc" — i.e., *where the content came from*, not *who owns the link* |

`shouldberestrictiondoc` is the clearest evidence that the designer recognised a scoping concept that is distinct in intent from the arrangement-function domain — but never split them into separate fields.

---

### Insertion grouping also keyed on `homedoc`

The extension test [insertnd.c:305] checks `homedoc` equality before deciding whether a new insertion extends an existing crum or starts a new one:
```c
if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
    return (FALSE);
```
This enforces that all spans belonging to one link home document cluster together in the spanfilade — again, same tumbler in both roles.

---

### What ASN-0043 synthesis implies

Finding 0043 (`findings/0043-createnewversion-copies-text-not-links.md`) documents that `docopy` during `CREATENEWVERSION` reproduces text (subspace `.1.x`) but not links (subspace `.2.x`). The link subspace boundary is derived purely from the document ISA and the `LINKATOM` hint level — there is no external `E_doc` register consulted. The "home document" for a link is simply the document whose ISA was supplied to `docreatelink`, and that same ISA bounds the `.2.x` subspace in `findisatoinsertmolecule`.

---

### Conclusion

The udanax-green link allocator carries no `E_doc` notion distinct from `dom(M)`. Document scope is keyed on the arrangement-function domain throughout: the document ISA tumbler stored in `homedoc` (wisp.h:108) simultaneously **is** the allocation boundary, the arrangement-function lookup key, and the insertion-grouping predicate. The `shouldberestrictiondoc` comment at retrie.c:78 and the `should be sourcedoc` comment at sporgl.c:187 are the clearest evidence that a richer multi-role scoping model was contemplated but never instantiated as separate fields. In every path — allocation (`makehint` → granf2.c), retrieval (`findorgl` at sporgl.c:152), extension testing (insertnd.c:305) — a single document ISA tumbler carries all three roles at once.
