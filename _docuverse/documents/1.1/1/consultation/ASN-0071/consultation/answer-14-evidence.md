## Question 14 [evidence]

> Since APPEND has the `insertspanf` call commented out, will FINDDOCSCONTAINING ever return a document whose content was added solely via APPEND, even when that content exactly matches the query?

## KB Synthesis

No. A document whose content was added solely via APPEND will never be returned by FINDDOCSCONTAINING, regardless of how precisely the query content matches.

The mechanism is straightforward. FINDDOCSCONTAINING queries the DOCISPAN sub-index of the spanfilade — the index built by `insertspanf(..., DOCISPAN)` calls [SS-DOCISPAN]. INSERT creates DOCISPAN entries because it routes through `docopy()`, which calls `insertspanf` as its final step [ST-INSERT, SS-DOCISPAN Finding 0036]. APPEND does not: the `insertspanf` call is explicitly commented out in `doappend()` with the note `/*zzz dies this put in granf?*/` [ST-APPEND-NO-DOCISPAN, FC-APPEND-NO-DOCISPAN].

Since the spanfilade is write-only and append-only [INV-SPANF-WRITE-ONLY] — there is no insertion path other than `insertspanf` — content placed exclusively via APPEND leaves no trace in the DOCISPAN sub-index. FINDDOCSCONTAINING has nothing to match against.

The content does exist in the granfilade (it is retrievable via V-address), but discoverability via content identity is entirely determined by spanfilade entries. The two are independent [FC-CONTENT-SPANF-ISOLATION]. No entry in DOCISPAN means no result from FINDDOCSCONTAINING, full stop.

---

## Code Exploration

I now have everything I need from the source. Here is the full answer:

---

## Answer

**Yes — FINDDOCSCONTAINING will return a document whose content was added solely via APPEND, even though the `insertspanf` call in `doappend` is commented out.**

The comment is not disabling `insertspanf`; it is explaining that the call is *redundant* because it already happens transitively. The comment text makes this explicit:

```c
/* do1.c:25-32 */
bool doappend(typetask *taskptr, typeisa *docptr, typetextset textset)
{
  bool appendpm(),insertspanf(); /*zzz dies this put in granf?*/

    return (appendpm (taskptr, docptr, textset)/*&&
       appendpm includes insertspanf!   insertspanf(taskptr,spanf,docptr,textset,DOCISPAN)*/
    );
}
```

The annotation literally reads **"appendpm includes insertspanf!"** — it is documentation of the transitive call, not a note about removal.

---

### The Full Call Chain: APPEND → spanfilade

```
APPEND
 └─ doappend [do1.c:25]
     └─ appendpm [orglinks.c:17]
         └─ findvsatoappend + doinsert [orglinks.c:25-26]
             └─ doinsert [do1.c:87]
                 └─ inserttextingranf + docopy [do1.c:118-119]
                     └─ docopy [do1.c:45]
                         └─ insertspanf [do1.c:62]  ← CONTENT INDEXED
```

Specifically:

- `appendpm` [orglinks.c:26] calls `doinsert(taskptr, docisaptr, &vsa, textset)`
- `doinsert` [do1.c:119] calls `docopy(taskptr, docisaptr, vsaptr, ispanset)`
- `docopy` [do1.c:62] calls `insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)`

`docopy` is the function that always writes to the spanfilade. The comment in `doappend` was written to explain exactly this: the direct `insertspanf` call (which would have been a *second* invocation at the `doappend` level) is not needed because `docopy` already calls it.

---

### How FINDDOCSCONTAINING Searches

```
FINDDOCSCONTAINING
 └─ dofinddocscontaining [do1.c:15]
     └─ specset2ispanset + finddocscontainingsp [do1.c:21-22]
         └─ finddocscontainingsp [spanf1.c:151]
             └─ retrieverestricted(spanf, ...) [spanf1.c:171]  ← QUERIES SPANFILADE
```

`finddocscontainingsp` [spanf1.c:151] iterates over the query's ispan set and for each entry calls:

```c
/* spanf1.c:171 */
context = retrieverestricted((typecuc*)spanf, &docspace, ORGLRANGE,
                              ispanset, SPANRANGE, (typeisa*)NULL);
```

This queries the spanfilade directly — the same structure that `insertspanf` writes to. It retrieves all documents (`ORGLRANGE`) whose content spans (`SPANRANGE`) overlap the query, then extracts document addresses from `c->totaloffset.dsas[ORGLRANGE]` [spanf1.c:173].

---

### Conclusion

The spanfilade is populated by `insertspanf` [spanf1.c:15], which is called by `docopy` [do1.c:62], which is called unconditionally by `doinsert` [do1.c:119], which is called by `appendpm` [orglinks.c:26], which is called by `doappend` [do1.c:29]. The commented-out code in `doappend` was a *proposed redundant second call* that was never needed. `FINDDOCSCONTAINING` queries the spanfilade via `retrieverestricted` [spanf1.c:171] and will find any document whose content was indexed there — including content added solely via APPEND.
