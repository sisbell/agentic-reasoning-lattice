## Question 19 [gregory]

> The spanfilade DOCISPAN entries are never deleted — but can they be modified in place? If a document's content is rearranged so the same I-addresses map to different V-positions, do the existing DOCISPAN entries remain frozen at their original values, or are they updated?

## KB Synthesis

DOCISPAN entries remain frozen at their original values after REARRANGE. They cannot be modified in place, and there is no need to modify them.

**The spanfilade has no modification operation**

[INV-SPANF-WRITE-ONLY] (Finding 0057) establishes this structurally: `insertspanf`, query functions, and nothing else. No `deletespanf`, no `modifyspanf`, no in-place update exists in `spanf1.c` or `spanf2.c`. The spanfilade is append-only by construction.

**DOCISPAN entries don't record V-positions**

This is the key point. From [SS-DOCISPAN] (Findings 0036, 0047), a DOCISPAN entry is:

```
(ISpan: {start: IAddress, width: Nat}) → DocISA
```

It answers: *"Document D contains content at I-address range α..α+n."* V-positions are not stored. DOCISPAN entries live entirely in I-space.

**REARRANGE changes V-positions only**

[INV-REARRANGE-IDENTITY] (Findings 0016, 0018, 0056) states the multiset of I-addresses in a document is invariant under rearrangement — `tumbleradd` modifies only `cdsp.dsas[V]`, never the I-address component. After a pivot or swap, the document still contains the same I-addresses at the same I-addresses; they just appear at different V-positions.

Because DOCISPAN entries record I-address presence, not V-position, a rearrangement that changes where "ABC" appears in V-space does not change the truth of "Document D contains I-addresses α₁..α₃." The entries remain accurate without modification.

**REARRANGE doesn't touch the spanfilade at all**

[FC-CONTENT-SPANF-ISOLATION] confirms this operationally: REARRANGE calls no spanf function. The only operations that write DOCISPAN entries are INSERT (via `docopy` → `insertspanf(..., DOCISPAN)`) and COPY [ST-INSERT], [ST-COPY].

**Summary**

| Question | Answer |
|----------|--------|
| Can DOCISPAN entries be modified in place? | No — the spanfilade has no modification mechanism ([INV-SPANF-WRITE-ONLY]) |
| Are they updated after REARRANGE? | No — REARRANGE doesn't call any spanf function ([FC-CONTENT-SPANF-ISOLATION]) |
| Do they need updating? | No — they record I-address→DocISA, which REARRANGE doesn't change ([INV-REARRANGE-IDENTITY]) |
| Do they remain valid? | Yes — same I-addresses still present in the document, just at different V-positions |

The design is elegant here: by indexing in I-space rather than V-space, DOCISPAN entries are immune to all V-space mutations. INSERT and COPY add new entries; DELETE, REARRANGE, and VERSION leave the spanfilade untouched ([FC-GRANF-ON-DELETE]).

---

## Code Exploration

I have all the evidence I need. Let me write the complete answer.

---

## DOCISPAN Entries Are Frozen — The Spanfilade Is Append-Only

The answer is definitive: **DOCISPAN entries in the spanfilade are never modified in place.** After a document rearrangement, the existing entries remain frozen at their original I-address values. The V-position changes are recorded exclusively in the POOM (permutation matrix), which the spanfilade neither knows about nor replicates.

---

### How DOCISPAN Entries Are Written

`insertspanf` in `spanf1.c:15` is the sole write path into the spanfilade for content-type entries. For a DOCISPAN, it is called as:

```c
insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)   // do1.c:62
```

Inside `insertspanf` (`spanf1.c:22–51`), each I-span in the `sporglset` becomes one spanfilade crum:

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);   // spanf1.c:22
tumblerclear (&crumwidth.dsas[ORGLRANGE]);                        // spanf1.c:23
// ...
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);             // spanf1.c:49
movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);               // spanf1.c:50
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);  // spanf1.c:51
```

The resulting crum layout:
- **ORGLRANGE** origin = `DOCISPAN.{doc-isa}` = `4.{doc-isa}` (prefixed with the constant 4)
- **ORGLRANGE** width = 0 (a point, not a span — just a document identity marker)
- **SPANRANGE** origin = the I-address (permascroll stream)
- **SPANRANGE** width = the I-span width (permascroll extent)

`insertnd` inserts along the SPANRANGE dimension. This is pure insertion — `insertnd` can only **add** crums, not replace them.

---

### What `dorearrange` Actually Does

`dorearrange` (`do1.c:34–43`) is the document rearrangement entry point:

```c
bool dorearrange(typetask *taskptr, typeisa *docisaptr, typecutseq *cutseqptr)
{
    typeorgl docorgl;
    bool findorgl(), rearrangepm();;

    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && rearrangepm (taskptr, docisaptr, docorgl, cutseqptr)
    );
}
```

`rearrangepm` (`orglinks.c:137–142`) does exactly one structural operation:

```c
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr)
{
    rearrangend((typecuc*)docorgl, cutseqptr, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`rearrangend` (`edit.c:78`) operates on `docorgl` — the **POOM node** for the document — along the **V dimension**. It shifts crum V-offsets inside the POOM to reflect the new ordering. The spanfilade (`spanf`) is **never passed** to `rearrangend`, `deletend`, or any other mutating function.

---

### Comprehensive Audit: What Operations Touch `spanf`

All uses of `spanf` in the codebase:

| Location | Operation | Read/Write |
|---|---|---|
| `do1.c:62` | `insertspanf(spanf, ..., DOCISPAN)` | **write** (insert) |
| `do1.c:79` | `insertspanf(spanf, ..., DOCISPAN)` | **write** (insert) |
| `do1.c:191,219` | `insertendsetsinspanf(spanf, ...)` → `insertspanf` | **write** (insert) |
| `spanf1.c:171` | `retrieverestricted((typecuc*)spanf, ...)` | read |
| `spanf1.c:245` | `retrieverestricted((typecuc*)spanf, ...)` | read |
| `spanf1.c:124` | `findlinksfromtothreesp(spanf, ...)` | read |
| `do1.c:352,359` | `findlinksfromtothreesp(spanf, ...)` | read |

There is **no call to `rearrangend(spanf, ...)`** and **no call to `deletend(spanf, ...)`** anywhere in the codebase. The grep for `spanf.*rearrange` and `rearrange.*spanf` returns only two debug `fprintf` print statements inside `#ifdef UnDeFINed` blocks (`edit.c:96`, `edit.c:153`), which are compiled out.

The same is true for `dodeletevspan` (`do1.c:158–167`): it calls `deletevspanpm` (`orglinks.c:145–152`), which calls `deletend((typecuc*)docorgl, ...)` — again only the POOM, never the spanfilade.

---

### The Structural Reason: Different Dimensions Encode Different Facts

The spanfilade and the POOM encode orthogonal information:

- **POOM** (`docorgl`): maps **V-positions → I-spans** for a single document. This is a mutable 2D enfilade that changes on every insert, delete, and rearrange. It tracks *where* content currently appears in a document.

- **Spanfilade** (`spanf`): maps **I-spans → document ISAs** across all documents. The ORGLRANGE dimension identifies the document (prefixed by span type), the SPANRANGE dimension identifies the permascroll region. This tracks *which* documents have ever incorporated given permascroll content.

These record different semantic facts. The POOM answers: "what is at V-position N in document D?" The spanfilade answers: "which document incorporates I-span S?" The second question has a permanent answer — permascroll content is immutable and never leaves a document's identity once incorporated. Rearranging the V-positions of content does not change the fact that the content belongs to the document.

---

### Consequence: DOCISPAN Entries Persist Through Deletion Too

Because `dodeletevspan` also only modifies the POOM and never the spanfilade, a DOCISPAN entry is not removed even when a V-span is deleted. If you insert content (creating a DOCISPAN entry for that I-span), then delete that V-span from the document, the spanfilade still records the document as containing that permascroll region. `finddocscontainingsp` (`spanf1.c:151`) will still return that document for queries against that I-span.

This means the spanfilade's DOCISPAN entries are **permanent historical provenance records**, not current-state membership records. They accumulate monotonically over the lifetime of the store.
