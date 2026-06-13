## Question 12 [evidence]

> Is the spanfilade search in FINDDOCSCONTAINING genuinely global across all documents in the docuverse, or does the 2D index's document-origin dimension restrict the traversal to some subtree of the document address space?

## KB Synthesis

## FINDDOCSCONTAINING: Global or Restricted?

The short answer: **genuinely global**, but for different reasons than the `find_links` bypass.

---

### What the KB establishes about the spanfilade's 2D structure

The SPAN enfilade is a 2D B-tree with two address dimensions [SS-ENFILADE-TREE, Finding 0066]:

- **SPANRANGE** — the I-address (content identity) dimension
- **ORGLRANGE** — the orgl origin dimension (carries document or link identity)

DOCISPAN entries are inserted as `insertnd(…, &crumorigin, &crumwidth, &linfo, SPANRANGE)` — the I-address is the SPANRANGE key, and the document ISA (`docisaptr`) is carried as the ORGLRANGE payload [SS-DOCISPAN, Finding 0036].

---

### The `find_links` bypass is an accident; FINDDOCSCONTAINING's globality is intentional

[EC-FIND-LINKS-GLOBAL] / Finding 0069 documents that `sporglset2linkset()` contains a `TRUE||!homeset` guard that hard-codes the ORGLRANGE search to width-100 starting at zero, discarding any caller-supplied document scope. This is a **bug** — the orgl restriction was supposed to work, not be bypassed.

FINDDOCSCONTAINING is structurally different. Its purpose is to answer "which documents anywhere in the docuverse contain these I-addresses?" There is no meaningful ORGLRANGE restriction to apply — the whole point is to scan all document origins. The ORGLRANGE dimension stores document ISAs as *values returned*, not as a *search filter*. The query restricts only SPANRANGE (the I-address) and then collects every matching ORGLRANGE entry, which are the document ISAs.

---

### Observable confirmation of global scope

[EC-STALE-SPANF-REFERENCE] makes this concrete:

> "FIND_DOCUMENTS returns a **superset** of documents currently containing the queried I-addresses"

The superset property arises because the spanfilade is write-only [INV-SPANF-WRITE-ONLY] — DELETE never removes DOCISPAN entries — so stale entries from **any document in the system** accumulate permanently. That stale entries from arbitrary documents persist and show up in results is only possible if the traversal is not scoped to a subtree of the address space.

The formal statement is: `actual_docs(i) ⊆ find_documents(i)` where `actual_docs(i) = {D | ∃ v : poom.D(v) = i}`. The inequality (not equality) is entirely due to stale accumulation, not scoping — if the search were restricted to an address subtree, some live results could also be missed.

---

### The RETRIEVEENDSETS contrast clarifies the architecture

[SS-RETRIEVE-ENDSETS] / Finding 0035 shows that RETRIEVEENDSETS uses ORGLRANGE prefixes (`LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3`) to distinguish link endpoint types during search. FINDDOCSCONTAINING has no equivalent prefix — it uses type-4 (DOCISPAN) and searches the full ORGLRANGE extent, because there is no meaningful partitioning of "which documents" to restrict to.

---

### Summary

| Operation | ORGLRANGE treatment | Why |
|-----------|-------------------|-----|
| `find_links` | Accidentally global (`TRUE\|\|` bug) | Should restrict to specified documents, but doesn't [EC-FIND-LINKS-GLOBAL] |
| RETRIEVEENDSETS | Restricted by type prefix (1/2/3) | Distinguishes FROM/TO/THREE endpoint slots [SS-RETRIEVE-ENDSETS] |
| FINDDOCSCONTAINING | Intentionally global | Document ISA is the *value returned*, not a search filter; purpose is cross-docuverse discovery [EC-STALE-SPANF-REFERENCE, INV-SPANF-WRITE-ONLY] |

The KB does not contain a finding that directly inspects `finddocscontainingsp`'s internal query construction to confirm no ORGLRANGE restriction is applied. What it does confirm is the observable result: FIND_DOCUMENTS returns entries from all documents that have ever copied/inserted the queried I-addresses, regardless of account, session, or version lineage. Any document-origin restriction in the 2D traversal would contradict this.

---

## Code Exploration

I now have a complete, code-traced answer. Here it is.

---

## FINDDOCSCONTAINING: Global Search or Subtree-Restricted?

### Call chain

```
fns.c:20  finddocscontaining()
  do1.c:15  dofinddocscontaining()
    spanf1.c:151  finddocscontainingsp()
      retrie.c:56   retrieverestricted()
        retrie.c:87   retrieveinarea()
          retrie.c:229  findcbcinarea2d()
```

---

### The 2D spanfilade layout

From `wisp.h:15-16`:
```c
#define ORGLRANGE 0   /* "origin-class" dimension */
#define SPANRANGE 1   /* I-space content span dimension */
```

The global `spanf` is a SPAN-type (2D) enfilade. Every leaf crum stores:
- **ORGLRANGE**: a tumbler encoding both the *type* of entry (link-from, link-to, link-three, doc-content) and, encoded inside it, the identity of the specific document or link.
- **SPANRANGE**: the I-space span of the content.

---

### How DOCISPAN entries are keyed in ORGLRANGE

When content is copied into a document (`do1.c:62`):
```c
insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

Inside `insertspanf` (`spanf1.c:22`):
```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```

`prefixtumbler` is defined at `tumble.c:641-651`:
```c
int prefixtumbler(tumbler *aptr, INT bint, tumbler *cptr)
{
    tumblerclear (&temp1);
    temp1.mantissa[0] = bint;         /* temp1 = bint (= DOCISPAN = 4) */
    movetumbler (aptr, &temp2);
    if (!iszerotumbler (&temp2))
        temp2.exp -= 1;               /* shift docisa right one radix place */
    tumbleradd (&temp1, &temp2, cptr);/* cptr = 4 + docisa/base = "4.docisa" */
}
```

So every DOCISPAN entry has ORGLRANGE = `4.docisa`, which lies in the half-open interval **[4, 5)** for any non-zero docisa.

The four span types and their ORGLRANGE ranges are (`xanadu.h:37-40`):
```c
#define LINKFROMSPAN    1   → ORGLRANGE in [1, 2)
#define LINKTOSPAN      2   → ORGLRANGE in [2, 3)
#define LINKTHREESPAN   3   → ORGLRANGE in [3, 4)
#define DOCISPAN        4   → ORGLRANGE in [4, 5)
```

All four types share the same single `spanf` enfilade.

---

### What `finddocscontainingsp` actually queries

`spanf1.c:165-171`:
```c
headptr = addresssetptr;
*addresssetptr = NULL;
clear (&docspace, sizeof(typespan));
tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);  /* stream = 4 */
tumblerincrement (&docspace.width,  0, 1,        &docspace.width);   /* width  = 1 */
for (; ispanset; ispanset = ispanset->next) {
    context = retrieverestricted ((typecuc*)spanf,
                                  &docspace, ORGLRANGE,   /* span1: [4,5) on ORGLRANGE */
                                  ispanset,  SPANRANGE,   /* span2: target content on SPANRANGE */
                                  (typeisa*)NULL);        /* NO homedoc restriction */
```

The `docspace` constraint `[4, 5)` encompasses the ORGLRANGE of **every** DOCISPAN entry in the spanfilade, because `prefixtumbler(docisa, 4)` ∈ [4, 5) for any docisa. There is no per-document filtering: the constraint is a **type selector** (DOCISPAN entries only, excluding types 1–3), not a **document address subtree selector**.

---

### The NULL docisaptr is not optional — it is mandatory

In `retrieverestricted` (`retrie.c:77-83`):
```c
if (docisaptr) {
    movetumbler(docisaptr,&info.homedoc);
    infoptr = &info;
} else {
    infoptr = NULL;
}
temp = retrieveinarea (..., (typebottomcruminfo*)infoptr);
```

With `(typeisa*)NULL`, `infoptr = NULL`. Inside `findcbcinarea2d` (`retrie.c:244-250`):

```c
#ifndef DISTRIBUTION
if(infoptr){
    fprintf(stderr,"not NULL infoptr versions mumble specialcase 11/27/84 shouldent happen till we try something fancier\n");
    gerror("findcbcinarea2d");
}
#else
    if (infoptr)
        gerror("!NULL");
#endif
```

Passing a non-NULL `infoptr` (a document address filter) to `findcbcinarea2d` is a **runtime error in both debug and distribution builds**. The homedoc-filtering code at `retrie.c:274` exists syntactically but can never execute for SPAN-type enfilades. The 1984 comment confirms it was never implemented: *"shouldent happen till we try something fancier."*

---

### How the document address is recovered

After retrieval (`spanf1.c:172-174`):
```c
movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);   /* docid = "4.actualDocISA" */
beheadtumbler (&docid, &document.address);                /* strip leading 4 */
```

`beheadtumbler` (`tumble.c:673-683`) increments `exp` by 1, effectively removing the DOCISPAN prefix and recovering the bare document ISA.

---

### Answer

The FINDDOCSCONTAINING search is **genuinely global across all documents in the docuverse.**

The ORGLRANGE dimension's `[4, 5)` filter is a **type discriminator** — it selects document-content entries (DOCISPAN = 4) and excludes link-endpoint entries (types 1–3) that share the same `spanf` enfilade. Within that type, `prefixtumbler(docisa, 4)` lands in [4, 5) for *every* document, so the traversal covers the entire docuverse without restriction.

No document-address-space subtree restriction is applied, and the code architecture makes it impossible to apply one: passing a non-NULL document address filter to `findcbcinarea2d` triggers `gerror` in both debug and distribution builds (`retrie.c:244-250`). The only dimension that narrows the result is the SPANRANGE filter — the specific I-spans the caller is searching for.
