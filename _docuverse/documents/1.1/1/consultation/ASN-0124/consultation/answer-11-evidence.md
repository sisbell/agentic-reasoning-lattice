## Question 11 [evidence]

> When FINDDOCSCONTAINING returns its result, does each entry consist solely of a document address, or does it also report the specific I-address span (or V-span within the returned document) that overlaps the queried material?

## KB Synthesis

FINDDOCSCONTAINING returns document addresses only — a set of DocISAs. It does not include the matching I-address span or any V-span within the returned documents.

The evidence for this is consistent across several KB entries:

**Return type is a set of documents:** [INT-DELETE-SPANF-DIVERGENCE] formalizes the return type directly: `actual_docs(i) ⊆ find_documents(i)` where `actual_docs(i) = {D | ∃ v : poom.D(v) = i}`. The result is a set of document identifiers D, not a set of (document, span) pairs.

**Callers must do I-to-V conversion themselves:** [EC-STALE-SPANF-REFERENCE] states that "consumers of FIND_DOCUMENTS must post-filter via I-to-V conversion (INV-ITOV-FILTERING from Finding 0048) to distinguish live from stale results." If the result already included V-spans, this separate conversion step would be unnecessary.

**What the DOCISPAN index stores:** [SS-DOCISPAN] describes the spanfilade type 4 index as mapping I-address ranges to document ISAs (`insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)`). The stored value is `docisaptr` — the document address — not a (document, V-span) pair.

**Described behavior is purely document-set:** [ST-DELETE] (Finding 0023) states: "the I-address association is preserved — `FINDDOCSCONTAINING` results are unchanged" after deletion, meaning the operation simply tracks *which* documents ever held the I-addresses. [FC-CONTENT-SPANF-ISOLATION] (Finding 0018) similarly describes the result as "`FINDDOCSCONTAINING` still finds the content via any remaining document" — just membership, no position.

The consequence of this design is the stale-reference gap documented in [EC-STALE-SPANF-REFERENCE]: a document can appear in FINDDOCSCONTAINING results even after its content has been deleted, because the spanfilade is write-only [INV-SPANF-WRITE-ONLY]. To find the actual V-position of the matching content in a returned document, the caller must separately invoke I-to-V conversion through that document's POOM, which will silently drop any I-addresses that no longer have V-mappings [INV-ITOV-FILTERING].

---

## Code Exploration

I now have the complete picture. Let me write the full answer.

---

## FINDDOCSCONTAINING Result Format: Document Addresses Only

The result of FINDDOCSCONTAINING (command 22) contains **bare document addresses and nothing else**. Each entry is a single tumbler identifying the document. No I-address span, no V-span overlap, and no intersection geometry of any kind is reported.

Here is the complete traced call chain.

---

### 1. Top-level handler — `fns.c:20-32`

```c
void finddocscontaining(typetask *taskptr)
{
  typespecset specset;
  typelinkset addressset;
  ...
    if (
       getfinddocscontaining (taskptr, &specset)
    && dofinddocscontaining (taskptr, specset, &addressset))
        putfinddocscontaining (taskptr, (typeitemset)addressset);
```

The output accumulator is `addressset`, typed as `typelinkset`. It is passed to `putfinddocscontaining` cast to `typeitemset`.

---

### 2. Worker — `do1.c:15-23`

```c
bool dofinddocscontaining(typetask *taskptr, typespecset specset, typelinkset *addresssetptr)
{
  typeispanset ispanset;
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
    && finddocscontainingsp (taskptr, ispanset, addresssetptr));
}
```

Converts the input V-specset to an I-span set, then delegates to the spanfilade query.

---

### 3. Spanfilade query — `spanf1.c:151-188`

This is the core. The spanfilade is indexed by two coordinates: the **ORGL range** (document ID, prefixed with the `DOCISPAN` constant = 4) and the **SPAN range** (the I-address the document holds). `retrieverestricted` is called with `docspace` (the DOCISPAN bucket) on the ORGL axis and the queried `ispanset` on the SPAN axis:

```c
context = retrieverestricted(
    (typecuc*)spanf,
    &docspace,    // ORGL range: DOCISPAN bucket
    ORGLRANGE,
    ispanset,     // SPAN range: queried I-addresses
    SPANRANGE,
    (typeisa*)NULL);
```

For each matching context `c`, the code extracts **only the document address** from the ORGL coordinate:

```c
movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);   // spanf1.c:173
beheadtumbler (&docid, &document.address);               // spanf1.c:174
```

`beheadtumbler` (`tumble.c:673-683`) strips the leading DOCISPAN prefix digit (the `4.` head) from the tumbler, leaving only the bare document address.

The `document` variable is `typelink` — which has only three fields: `next`, `itemid`, `address`. The itemid is set to `LINKID`:

```c
document.itemid = LINKID;     // spanf1.c:177
document.next = NULL;
addresssetptr = (typelinkset *) onitemlist(taskptr, (typeitem*)&document, (typeitemset*)addresssetptr);
```

**The SPAN range data — the actual I-address interval the document holds — is present in `c->totaloffset.dsas[SPANRANGE]` but is never read.** It is silently discarded.

---

### 4. `LINKID` is `ADDRESSID` — `xanadu.h:33`

```c
#define LINKID ADDRESSID
```

Both are the integer constant `5`. `typelink` is defined as `typedef typeaddress typelink` (`xanadu.h:106`), and `typeaddress` is:

```c
typedef struct structtypeaddress{
    struct structtypeaddress *next;
    typeitemid itemid;
    typeisa address;        // one tumbler, the document address
} typeaddress;
```

There is no width, span, or overlap field in this struct.

---

### 5. Wire encoding — `putfe.c:349-354` and `putfe.c:168-174`

```c
int putfinddocscontaining(typetask *taskptr, typeitemset addressset)
{
    putnumber (taskptr->outp, FINDDOCSCONTAINING);   // command echo: 22
    putitemset (taskptr, addressset);
}
```

`putitemset` counts items and writes the count, then calls `putitem` for each. For `ADDRESSID` (= `LINKID`):

```c
case ADDRESSID:
    puttumbler (outfile, &((typeaddress *)itemptr)->address);  // putfe.c:173
    break;
```

One tumbler per entry — the document address. Nothing else.

---

### 6. Python client confirms — `client.py:780-785`

```python
def find_documents(self, specset):
    self.xc.command(22, specset)
    docids = []
    for i in range(self.xc.Number()):   # read count
        docids.append(self.xc.Address())  # read one tumbler per entry
    return docids
```

Reads back N bare `Address` objects. No span parsing of any kind.

---

### Conclusion

FINDDOCSCONTAINING returns a flat list of **document addresses** (tumblers). Each entry is one tumbler identifying a document that the spanfilade records as having once indexed some part of the queried I-addresses. There is no I-address sub-range, no overlapping interval width, and no V-span within the returned document — only the document identity.

The overlapping span data is geometrically present in the spanfilade context (`c->totaloffset.dsas[SPANRANGE]`) during the query at `spanf1.c:171-181`, but the code never extracts it. To learn *which portion* of a returned document overlaps the queried material, a subsequent `RETRIEVEDOCVSPANSET` + V→I conversion, or a `SHOWRELATIONOF2VERSIONS`-style call, would be required. FINDDOCSCONTAINING itself is purely a set-membership oracle: it tells you *which* documents, not *where* within them.
