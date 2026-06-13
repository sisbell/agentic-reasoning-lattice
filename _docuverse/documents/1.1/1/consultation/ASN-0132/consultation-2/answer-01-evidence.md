## Question 1 [evidence]

> When a document is forked/versioned (the fork composite), does the operation create new link addresses in the link store, or does it populate only the content subspace, leaving the source-homed link as the sole copy?

## KB Synthesis

VERSION creates **no new link addresses**. It populates only the text subspace of the new document, leaving the source-homed link orgl as the sole copy.

## What VERSION does

[ST-VERSION-CREATE] (Finding 0077) is definitive: `CREATENEWVERSION` performs exactly two effects:

1. Allocates a new **document address** under the source via `createorglingranf` (DOCUMENT hint)
2. Copies **text SPAN entries** from the source's text subspace into the version via `docopyinternal → insertspanf`

It makes **no call to `findisatoinsertgr` for content**, so no new content I-addresses or link orgl I-addresses are allocated.

## What the version's POOM contains

[ST-VERSION-CREATE] (Finding 0043 and 0046) makes the split explicit:

- The version receives **text subspace only** (V-dimension 1.x). `retrievedocumentpartofvspanpm()` extracts only the V-dimension width starting at position 1, structurally excluding the link subspace.
- The version's **link subspace (2.x) is empty** — it has no POOM-level link entries at all.

[FC-GRANF-ON-VERSION] confirms: VERSION modifies the document portion of the granfilade (new doc address) but leaves the content granfilade entirely unchanged.

## How the version still discovers links

Despite having no link POOM entries, [INT-LINK-VERSION] (Finding 0046) explains the emergent behavior: the version shares **text I-addresses** with the source. Since `find_links` operates in I-space via the spanfilade — not via POOM link entries — the same spanfilade entries that index the source's text content also match the version's identical I-addresses. Link discoverability is inherited without any explicit link-copy mechanism.

## The source-homed link is the sole copy

The link orgl lives in I-space at an address under the **source document** (e.g., `source_doc.0.2.1`), per [SS-LINK-HOME-DOCUMENT] and [SS-ADDRESS-SPACE] (Finding 0065). Nothing in VERSION touches the spanfilade's link-endset index entries, the link orgl in the granfilade, or the link's home document address. [INV-LINK-PERMANENCE] and [FC-GRANF-ON-VERSION] together guarantee these are untouched.

**Bottom line:** VERSION is link-neutral at the storage layer. The version's POOM is text-only; the source-homed link orgl is the sole copy; link discoverability from the version is purely a consequence of shared text I-addresses and the content-identity-based spanfilade index [INT-LINK-TRANSCLUSION], [INT-LINK-VERSION].

---

## Code Exploration

I now have all the evidence needed. Let me synthesize the complete answer.

---

## Answer: Fork Does NOT Create New Link Addresses — Text Subspace Only

The fork operation (`CREATENEWVERSION`, command 13) **does not create new link addresses in the link store**. It copies only the text (content) subspace. The source-homed link remains the sole copy in the link V-address store. Here is the full trace.

---

### Entry Point: `fns.c:289–300`

```c
void createnewversion(typetask *taskptr)
{
  typeisa originaldocisa, newdocisa;
    if (
       getcreatenewversion (taskptr, &originaldocisa)
    && docreatenewversion (taskptr, &originaldocisa, &originaldocisa, &newdocisa))
        putcreatenewversion (taskptr, &newdocisa);
```

Both the `isaptr` and `wheretoputit` parameters are the same address (`&originaldocisa`), so the ownership branch fires.

---

### Core Logic: `do1.c:260–298`

```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr,
                        typeisa *wheretoputit, typeisa *newisaptr)
```

**Step 1 — Allocate a new document address** [`do1.c:270–278`]:
```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr, &hint);
} else {
    makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
if (!createorglingranf(taskptr, granf, &hint, newisaptr)) return FALSE;
```

`createorglingranf` allocates a new granfilade organelle for the new document. No link organelle is created here or anywhere in this function. The only `createorglingranf` call is for the document itself.

**Step 2 — Retrieve the source document's V-span** [`do1.c:281–282`]:
```c
if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) return FALSE;
```

This calls `retrievedocumentpartofvspanpm` in `orglinks.c:155–162`:
```c
bool retrievedocumentpartofvspanpm(typetask *taskptr, typeorgl orgl,
                                   typevspan *vspanptr)
{ /* this is a kluge*/
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
    return (TRUE);
}
```

This reads the root POOM crum's V-displacement (`cdsp.dsas[V]`) and V-width (`cwid.dsas[V]`). The **function name says "document part"** and is commented `/* this is a kluge */`. Its implementation is byte-for-byte identical to `retrievevspanpm` at `orglinks.c:165–172`.

The crucial geometric fact: for a document with text content, `cdsp.dsas[V]` == 1 (the text subspace starting position). Links live at V-address **2.x** (internal representation; confirmed by `setlinkvsas` in `do2.c:169–183` which builds tumblers at position `0,2,1` and `0,1,1`), while text lives at **1.x**. Since 1.x < 2.x in tumbler ordering, the span `[stream=1, width=1)` covers V-positions from 1 up to but not including 2 — which is exactly the text subspace. The link subspace at 2.x falls outside this range.

**Step 3 — Copy the vspan into the new document** [`do1.c:284–296`]:
```c
vspec.next = NULL;
vspec.itemid = VSPECID;
movetumbler(isaptr, &vspec.docisa);
vspec.vspanset = &vspan;

addtoopen(newisaptr, user, TRUE, WRITEBERT);
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
```

`docopyinternal` (`do1.c:66–82`) calls `specset2ispanset` → `vspanset2ispanset` → `permute` (`orglinks.c:404`), which walks the source document's POOM looking up the I-addresses stored at those V-positions. Because the vspan covers only 1.x (text), only **text I-spans** (permascroll addresses) are returned — not the link-organelle ISAs stored at 2.x.

Those text I-spans are then inserted into the new document's POOM via `insertpm` and recorded in the spanfilade via `insertspanf(..., DOCISPAN)`.

---

### How Links Are Originally Homed: `do1.c:195–220`

When `docreatelink` runs on the source document:
```c
createorglingranf (taskptr, granf, &hint, linkisaptr)    // new link organelle
&& tumbler2spanset (taskptr, linkisaptr, &ispanset)       // wrap ISA as ispan
&& findnextlinkvsa (taskptr, docisaptr, &linkvsa)         // next 2.x slot in doc
&& docopy (taskptr, docisaptr, &linkvsa, ispanset)        // place ISA at 2.x
&& insertendsetsinspanf (...)                              // record in spanfilade
```

The link organelle's ISA is placed at a V-address in the **source document's 2.x subspace** via `docopy`. `findnextlinkvsa` (`do2.c:151–167`) builds `firstlink = 2.1`:
```c
tumblerclear (&firstlink);
tumblerincrement (&firstlink, 0, 2, &firstlink);  // digit 0 = 2
tumblerincrement (&firstlink, 1, 1, &firstlink);  // digit 1 = 1
```

This 2.x slot is a POOM entry in the source document, not duplicated by the fork.

---

### Empirical Confirmation: Golden Test (Finding 0043)

```
Source document (with link):
  vspanset: at 0 for 0.1    (link subspace, normalized from 2.x)
            at 1 for 1      (text subspace)

After CREATENEWVERSION(source) → version:
  Version vspanset: at 1.1 for 0.15   ← text only
  Source vspanset: at 0 for 0.1, at 1 for 1  ← unchanged
```

The version POOM contains only the text span. The source's link subspace is untouched.

---

### What Happens to Link Discoverability

Even though the fork does not copy the link subspace, `find_links` still works for the version. This is because links are indexed in the **spanfilade** by I-address (`insertendsetsinspanf` in `do2.c:116–128`). The version shares the same text I-spans as the source (that is what `docopyinternal` copies). Since links point to content by I-address, any document containing those I-spans participates in link discovery — but that is a separate channel from the POOM link subspace.

---

### Summary

| Question | Answer | Source |
|---|---|---|
| Does fork create new link organelles? | **No** | `docreatenewversion` calls `createorglingranf` once only, for the document itself [`do1.c:277`] |
| Does fork copy the link subspace (2.x) into the new version's POOM? | **No** | `retrievedocumentpartofvspanpm` returns `stream=1` (text start); 2.x links lie outside this span [`orglinks.c:155–162`] |
| Is the source-homed link the sole copy in the link V-address store? | **Yes** | `findnextlinkvsa` + `docopy` at `linkvsa` write the link ISA into the source document only [`do1.c:211–212`]; fork does not repeat this |
| Are links still findable via the version? | **Yes**, but through a different mechanism: the spanfilade indexes link endsets by I-address; the version inherits the same text I-spans that the links reference [`do2.c:116–128`] |

The `retrievedocumentpartofvspanpm` naming (`/* this is a kluge */`) and its identity with `retrievevspanpm` in code suggests the intended filtering to the "document part" was never properly implemented — but the V-geometry (text at 1.x, links at 2.x, text displacement `cdsp=1`) achieves the correct result anyway: only the text subspace is in range and gets copied.
