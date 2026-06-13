## Question 17 [evidence]

> For a multi-span vspec-set covering regions in different documents, are the per-span results merged into a single deduplicated document set, or does the answer preserve which queried span each returned document overlaps?

## KB Synthesis

The KB does not directly document the multi-span FINDDOCSCONTAINING return structure with enough specificity to answer this definitively. Here is what can be inferred from the documented architecture, and where the gap is.

## What the KB establishes

The call chain for FINDDOCSCONTAINING is:

**SpecSet → I-spans (via `specset2ispanset`) → spanfilade query (`finddocscontainingsp`) → Set\<DocISA\>**

The DOCISPAN sub-index is modeled as `Map<ISpan, DocISA>` — it maps I-address ranges to document identities [SS-DOCISPAN]. The query function searches by I-address and returns the set of documents that have ever placed content at those addresses [INV-IADDRESS-PERMANENT].

The critical structural point: `specset2ispanset` converts the entire SpecSet into a flat collection of I-spans before querying the spanfilade [PRE-RETRIEVE-CONTENTS, PRE-RETRIEVE-CONTENTS Finding 0027]. The VSpec identity (which source document a span came from) is not preserved beyond this conversion — sporgls carry the *origin document of the content*, not the VSpec that selected it [SS-SPORGL].

## The implied answer

The architecture points toward a **flat merged result**. The spanfilade does not store or return query-span provenance; it maps I-addresses to DocISAs. When queried against multiple I-spans derived from a multi-document SpecSet, the result would be the union of all matching DocISAs across all queried I-spans — with no indication of which VSpec produced each match.

[INV-SPECSET-ORDER] explicitly covers ordering guarantees for `retrieve` and `vcopy` (operations that concatenate content in VSpec order), but makes no corresponding claim for `find_documents`. The absence is significant: document-set queries are set-valued, not sequence-valued, so per-span attribution would require a different return type than the system's documented model.

## What the KB does not answer

There is no KB entry that directly tests or confirms FINDDOCSCONTAINING behavior with a multi-source SpecSet. Specifically, no finding documents whether:
- The result is annotated with which queried span produced each matching document
- Duplicate DocISAs from overlapping I-address coverage are deduplicated
- The implementation of `finddocscontainingsp` accumulates results from multiple I-spans as a set union

If this distinction matters for spec writing, it requires a new targeted finding against the actual `finddocscontainingsp` + `spanf2.c` code path.

---

## Code Exploration

I have all the evidence needed. Here is the complete answer.

---

## Answer: Merged into a Single Deduplicated Set

The backend returns a **flat, deduplicated list of document ISAs**. Per-span attribution — which queried span caused a given document to appear — is structurally absent from the data type, the accumulation algorithm, and the wire protocol output.

---

### Call Chain

```
FEBE request → fns.c:20  finddocscontaining
             → do1.c:15  dofinddocscontaining
             → do2.c:14  specset2ispanset        ← flattens multi-span input
             → spanf1.c:151  finddocscontainingsp ← accumulates with dedup
             → put.c:216  putfinddocscontaining   ← writes flat list
```

---

### Step 1: The Specset Is Flattened Into a Single ISPanSet

`do1.c:15-23`:
```c
bool dofinddocscontaining(typetask *taskptr, typespecset specset, typelinkset *addresssetptr)
{
  typeispanset ispanset;
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
    && finddocscontainingsp (taskptr, ispanset, addresssetptr));
}
```

`specset2ispanset` (`do2.c:14`) iterates the entire specset — which may contain spans over multiple documents — and converts each VSPECID element to ispans via `vspanset2ispanset` (`orglinks.c:397`). The results are **appended into one flat linked list**. After this call, all per-document structure is gone; `ispanset` is just a sequence of physical (I-space) spans from all queried documents.

`orglinks.c:397-401`:
```c
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl,
    typevspanset vspanptr, typeispanset *ispansetptr)
{
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

Each doc's vspans are permuted to ispans and **chained onto the same `ispansetptr`** — one list for everything.

---

### Step 2: `finddocscontainingsp` Accumulates With Explicit Deduplication

`spanf1.c:151-188`:
```c
bool finddocscontainingsp(typetask *taskptr, typespanset ispanset, typelinkset *addresssetptr)
{
    headptr = addresssetptr;
    *addresssetptr = NULL;
    /* set up docspace = DOCISPAN range */
    for (; ispanset; ispanset = ispanset->next) {             /* each ispan */
        context = retrieverestricted((typecuc*)spanf, &docspace,
            ORGLRANGE, ispanset, SPANRANGE, (typeisa*)NULL);
        for (c = context; c; c = c->nextcontext) {            /* each matching doc */
            movetumbler(&c->totaloffset.dsas[ORGLRANGE], &docid);
            beheadtumbler(&docid, &document.address);
            if (isinlinklist(*headptr, &document.address))    /* ← dedup */
                continue;
            document.itemid = LINKID;
            document.next = NULL;
            addresssetptr = (typelinkset *)onitemlist(taskptr,
                (typeitem*)&document, (typeitemset*)addresssetptr);
        }
        contextfree(context);
    }
    return (TRUE);
}
```

The outer loop at `spanf1.c:170` iterates over **every ispan** (from any queried document). For each, it queries the spanfilade for documents in DOCSPACE that cover that ispan. The inner loop at `spanf1.c:172` processes the hits.

The critical line is `spanf1.c:175`:
```c
if (isinlinklist(*headptr, &document.address))
    continue;
```

`isinlinklist` (`spanf2.c:16-23`) walks the accumulating result list and returns TRUE if the document tumbler is already present:
```c
bool isinlinklist(typelinkset linkset, typeisa *linkisaptr)
{
    for (; linkset; linkset = linkset->next) {
        if (tumblereq(&linkset->address, linkisaptr))
            return (TRUE);
    }
    return (FALSE);
}
```

If a document was already added by a **different** queried ispan, it is silently skipped. Each document can appear at most once in the output. No record is made of which spans triggered its inclusion.

---

### Step 3: The Output Type Has No Attribution Field

`xanadu.h:98-107`:
```c
typedef struct structtypeaddress {
    struct structtypeaddress *next;
    typeitemid  itemid;
    typeisa     address;        /* ← just the document ISA */
} typeaddress;
typedef typeaddress typelink;
typedef typelink *  typelinkset;
```

`typelink` is `{next, itemid, address}`. There is **no slot** for a queried span, no per-entry annotation of any kind. The data structure is physically incapable of carrying attribution even if the algorithm wanted to.

---

### Step 4: The Wire Protocol Is a Flat List

`put.c:216-220`:
```c
int putfinddocscontaining(typetask *taskptr, typeitemset addressset)
{
    fprintf(taskptr->outp, "\ndocuments\n");
    putitemset(taskptr, addressset);
}
```

One `"\ndocuments\n"` header, then a flat item list. No grouping, no span labels.

---

### Summary

For a multi-span vspec-set, the pipeline:

1. **`specset2ispanset`** (`do2.c:14`) converts all vspecs — from any number of documents — into one flat `typeispanset`. Inter-document structure is discarded at this step.
2. **`finddocscontainingsp`** (`spanf1.c:151`) iterates the flat ispanset, queries the spanfilade per ispan, and accumulates results. The `isinlinklist` check at `spanf1.c:175` ensures each document appears **exactly once** regardless of how many queried spans overlap it.
3. The output is a `typelinkset` — a singly-linked list of `typelink` items, each holding only a document ISA tumbler (`address`). No span-to-document mapping is recorded.
4. The FEBE wire response (`put.c:216`) is a single unlabelled document list.

**The result is a merged, deduplicated set of document ISAs. There is no mechanism — in the algorithm, the data type, or the protocol — to recover which queried span caused any particular document to appear.**
