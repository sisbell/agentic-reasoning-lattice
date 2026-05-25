## Question 17 [gregory]

> If DELETEVSPAN is applied to a link's V-position in subspace `2.x` (creating a "reverse orphaned" link), and then new content is inserted whose I-addresses happen to overlap with the deleted link's endset I-spans, does `find_links` on that new content still discover the reverse-orphaned link through the spanfilade — even though the link has no POOM entry in any document?

## KB Synthesis

Yes — with a critical qualification about what "new content is inserted whose I-addresses happen to overlap" can mean in practice.

## The Premise Is Physically Unreachable for INSERT

Fresh INSERT cannot produce I-addresses that overlap with the reverse-orphaned link's endpoint I-spans. I-address allocation is strictly monotonically increasing and addresses are never reused [INV-NO-IADDR-REUSE], [INV-MONOTONIC]. `findisatoinsertmolecule` always queries the granfilade for its current maximum and increments by 1 — since the link's endpoint I-addresses are already in the granfilade, any new INSERT will allocate strictly higher addresses. The overlap scenario is structurally impossible for INSERTed content.

## But VCOPY Can Reach Those I-Addresses

VCOPY (transclusion) copies existing I-addresses into a new document's POOM without allocating new ones [ST-VCOPY]. If content sharing the link's endpoint I-spans is transcluded into any document, `find_links` on that document will discover the reverse-orphaned link.

## The Answer: Yes, the Link Is Discovered via the Spanfilade

This is the defining property of the reverse-orphaned state [EC-REVERSE-ORPHAN]. When DELETEVSPAN removes a link from the 2.x subspace, it modifies only the POOM layer — the link orgl in I-space and the spanfilade entries are completely untouched [SS-THREE-LAYER-MODEL]:

> `DELETEVSPAN(2.x)` → POOM entry removed; I-space link orgl unchanged; spanfilade entries unchanged.

From [INV-SPANF-WRITE-ONLY]: no operation ever removes spanfilade entries. The spanfilade maps `link_endpoint_I-addresses → link_ISA` and this mapping persists indefinitely.

`find_links` operates entirely in I-space via the spanfilade [SS-FIND-LINKS]:

> `find_links(S) = { L | I-addresses(S) ∩ I-addresses(L.source) ≠ ∅ }`

It has no dependency on whether the link has a POOM entry in any document. So if a document's content shares I-addresses with the reverse-orphaned link's endpoint I-spans (via VCOPY of the original content), `find_links` will discover the link.

## Concrete Scenario

```
1. Create link L with source endpoint at I-addresses α₁..α₃
   → spanfilade: α₁..α₃ → (L, LINKFROMSPAN)  [ST-CREATE-LINK]
   → document D POOM: V:2.1 → link ISA  [SS-THREE-LAYER-MODEL]

2. DELETEVSPAN(D, 2.1)
   → D POOM: V:2.1 entry removed
   → spanfilade: α₁..α₃ → (L, LINKFROMSPAN)  UNCHANGED  [FC-LINK-DELETE-ISOLATION]
   → L is now "reverse orphaned"  [EC-REVERSE-ORPHAN]

3. VCOPY α₁..α₃ into new document D'
   → D' POOM: some V-positions mapped to α₁..α₃  [ST-VCOPY]

4. find_links(D', span covering α₁..α₃)
   → converts V-span to I-span α₁..α₃  [INT-SPORGL-LINK-INDEX]
   → spanfilade lookup: α₁..α₃ matches entry for L
   → returns [L]  ✓
```

The link's POOM absence is irrelevant to `find_links` because discovery is purely an I-address intersection query against the spanfilade [SS-SPANF-OPERATIONS], [INT-LINK-TRANSCLUSION]. The reverse-orphaned state does not reduce the link's discoverability — it only removes the link from `retrieve_vspanset` output for its former home document.

---

## Code Exploration

I now have all the code and prior findings needed to answer definitively. Here is the complete analysis.

---

## Answer: Yes — the Reverse-Orphaned Link Is Still Discoverable

The short answer is **yes**: `find_links` on new content whose I-addresses overlap with a reverse-orphaned link's endset I-spans **will** discover the link through the spanfilade. The link has no POOM entry in any document, but that is irrelevant to how link discovery works. Here is the complete code-traced explanation.

---

### Part 1 — What DELETEVSPAN Does and Does Not Touch

`dodeletevspan` in `do1.c:158-167`:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
  bool findorgl(), deletevspanpm();

  return (
     findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
  && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
  /*&& TRUE*/ /* ht stuff */ );
}
```

It calls `deletevspanpm` in `orglinks.c:145-152`:

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

This calls `deletend` on `docorgl` — the document's **POOM enfilade** in granf. It removes the V-to-I crums that cover the specified V-range (in this case, the link's 2.x address).

**Critically: nothing else is called.** There is no call to any spanfilade function. The code path terminates at `deletend` on the POOM.

---

### Part 2 — What the Spanfilade Holds and How It Got There

When `docreatelink` runs in `do1.c:195-221`, it does two things relevant here:

**Step A** — puts the link's ISA into the document's POOM (the entry that DELETEVSPAN later removes):
```c
docopy(taskptr, docisaptr, &linkvsa, ispanset)  // [do1.c:212]
```

**Step B** — inserts the link's endset I-spans into the global spanfilade:
```c
insertendsetsinspanf(taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)  // [do1.c:219]
```

`insertendsetsinspanf` in `do2.c:116-128` calls `insertspanf` three times:
```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN)
```

`insertspanf` in `spanf1.c:15-54` inserts 2D nodes into the spanfilade with:
- **ORGLRANGE axis** = the link ISA tumbler, prefixed with the spantype code (1, 2, or 3)
- **SPANRANGE axis** = the I-address of the endset content

```c
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
...
movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);
movetumbler(&lwidth,  &crumwidth.dsas[SPANRANGE]);
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);  // [spanf1.c:51]
```

These entries encode: *"At I-address `lstream..lstream+lwidth`, link `linkisaptr` has an endset of type `spantype`."*

**DELETEVSPAN never touches these entries.** There is no `deletespanf` function anywhere in the codebase — inspection of `spanf1.c` and every file that calls spanfilade functions confirms only insertion and query functions exist (`insertspanf`, `findlinksfromtothreesp`, `retrieveendsetsfromspanf`, `finddocscontainingsp`, `retrievesporglsetinrange`). The spanfilade is write-once.

---

### Part 3 — How `find_links` Queries the Spanfilade

The call chain: `findlinksfromtothree` [fns.c:189] → `dofindlinksfromtothree` [do1.c:348-353] → `findlinksfromtothreesp` [spanf1.c:56-103].

`dofindlinksfromtothree` in `do1.c:348-353`:
```c
bool dofindlinksfromtothree(typetask *taskptr, typespecset fromvspecset, ...)
{
  bool findlinksfromtothreesp();
  return findlinksfromtothreesp(taskptr, spanf, fromvspecset, tovspecset, ...);
}
```

`findlinksfromtothreesp` in `spanf1.c:56-103`:
```c
if (fromvspecset)
    specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);  // [spanf1.c:71]
...
if (fromvspecset) {
    sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);  // [spanf1.c:77]
    ...
}
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);  // [spanf1.c:100]
```

**Step A: `specset2sporglset`** converts the query V-specset (the new content's V-address in its document) into a sporglset (I-address range). This goes through `vspanset2sporglset` in `sporgl.c:35-65` → `vspanset2ispanset` in `orglinks.c:397-402` → `permute` → `span2spanset` → `retrieverestricted` on the **query document's POOM**. The new content IS in its document's POOM (it was just inserted), so this conversion succeeds. The reverse-orphaned link's POOM deletion is irrelevant here — a different document is being queried.

**Step B: `sporglset2linkset`** in `sporgl.c:222-237` calls `sporglset2linksetinrange` in `sporgl.c:239-269`:

```c
int sporglset2linksetinrange(typetask *taskptr, typecuc *spanfptr,
    typesporglset sporglset, typelinkset *linksetptr,
    typeispan *orglrange, INT spantype)
{
  ...
  for (; sporglset; ...) {
    ...
    context = retrieverestricted(spanfptr,
        (typespan*)sporglset, SPANRANGE,   // restrict by I-address
        &range,              ORGLRANGE,    // restrict by spantype prefix
        (typeisa*)infoptr);
    for (c = context; c; c = c->nextcontext) {
        beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
        onlinklist(taskptr, linksetptr, &linksa);  // collect link ISA
    }
    contextfree(context);
  }
}
```

This calls `retrieverestricted` in `retrie.c:56-85`, which calls `retrieveinarea` → `findcbcinarea2d`, a recursive enfilade walk over the **spanfilade** (not any POOM). The 2D qualification is:
- SPANRANGE must overlap with the query I-addresses (the new content's I-spans)
- ORGLRANGE must fall within the spantype-prefixed range (LINKFROMSPAN, LINKTOSPAN, or LINKTHREESPAN)

If the new content's I-addresses overlap with the reverse-orphaned link's endset I-spans, `findcbcinarea2d` in `retrie.c:229-268` will traverse to those spanfilade bottom-crums — because they are still there — and `crumqualifies2d` in `retrie.c:270-305` will return TRUE. The link ISA is extracted via `beheadtumbler` and placed in the result list.

**No POOM check of any kind appears in this path.** The function never asks "does the link have a 2.x entry in any document's POOM?" It only asks "does the spanfilade contain an entry at this I-address range with this spantype prefix?"

---

### Part 4 — The ORGLRANGE Prefix Namespace Separation

One subtlety worth noting: the spanfilade serves double duty — it indexes both link endsets (LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3) and document transclusion containment (DOCISPAN=4). These do not interfere because `prefixtumbler` in `insertspanf` and the `prefixtumbler`-based range restriction in `sporglset2linksetinrange` ensure that link discovery queries (`spantype=1,2,3`) never accidentally match document containment entries (`spantype=4`), and vice versa. The reverse-orphaned link's entries at `spantype=1,2,3` remain in the spanfilade at their original I-spans, correctly namespaced.

---

### Part 5 — Summary of the Two Enfilades

| Structure | What it stores | Modified by DELETEVSPAN? | Consulted by `find_links`? |
|-----------|---------------|--------------------------|---------------------------|
| **POOM** (per-document orgl in granf) | V→I mapping for document content and links | **Yes** — `deletend` removes the 2.x entry | **Only to convert query V-addresses to I-addresses** (query doc's POOM, not link's home doc) |
| **Spanfilade** (global spanf) | I-address → link ISA mappings, all endset types | **No** — no deletion function exists | **Yes** — the primary mechanism for link discovery |

---

### Conclusion

**Yes, `find_links` will discover the reverse-orphaned link.**

The complete code path for why:

1. `DELETEVSPAN` on a link's 2.x V-position only calls `deletevspanpm` → `deletend` on the document's POOM **[`do1.c:158-167`, `orglinks.c:145-152`]**. The spanfilade is untouched.

2. The link's endset I-spans were permanently inscribed in the spanfilade at creation time via `insertendsetsinspanf` → `insertspanf` → `insertnd` **[`do1.c:219`, `do2.c:116-128`, `spanf1.c:15-54`]**. No deletion function for the spanfilade exists **[`spanf1.c` entire file]**.

3. `find_links` calls `findlinksfromtothreesp` → `sporglset2linkset` → `sporglset2linksetinrange` → `retrieverestricted` on the spanfilade **[`do1.c:348-353`, `spanf1.c:56-103`, `sporgl.c:222-269`]**. This is a pure I-address lookup against the spanfilade. No POOM existence check is performed for the link or its home document at any point in this path.

4. If the new content's I-addresses (obtained by converting V-addresses via the query document's own POOM) overlap with the reverse-orphaned link's endset I-spans, `findcbcinarea2d` **[`retrie.c:229-268`]** will traverse the spanfilade and return the link ISA.

The link's absence from any document's POOM is invisible to this query path. The spanfilade is a permanent, write-only index — it records every link endset ever registered, independent of POOM state. This is confirmed and documented in **Finding 0040** (link removal from POOM, find_links still works) and **Finding 0057** (spanfilade entries not cleaned up on DELETE).
