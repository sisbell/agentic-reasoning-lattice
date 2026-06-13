## Question 13 [evidence]

> Does the document whose V-spans were named in the query vspec-set always appear in its own FINDDOCSCONTAINING result, given that INSERT created a DOCISPAN entry for it — and is there any path (e.g., content added via APPEND, whose `insertspanf` call is commented out) by which a document containing the material is silently absent?

## KB Synthesis

## FINDDOCSCONTAINING: Guaranteed Presence vs. Silent Absence

### Short answer

A document is **always present** in its own FINDDOCSCONTAINING result when the queried I-addresses were placed there via INSERT or COPY/VCOPY. It is **silently absent** when the material was added via APPEND — and this is the only caller-visible path for that omission.

---

### Why INSERT guarantees presence

INSERT's call chain is `doinsert` → `inserttextingranf` → `docopy` → `insertpm` + `insertspanf(..., DOCISPAN)`. The final step writes a DOCISPAN entry into the spanfilade mapping the freshly-allocated I-addresses to the document ISA [ST-INSERT / Finding 0036]. Multiple INSERTs accumulate these entries monotonically [INV-INSERT-ACCUMULATE].

The spanfilade is write-only — no delete operation exists anywhere in `spanf1.c` or `spanf2.c` [INV-SPANF-WRITE-ONLY]. Consequently, once the DOCISPAN entry is written it never leaves. Even after a subsequent DELETE removes the V→I mapping from the POOM, the DOCISPAN entry persists and the document continues to appear in FINDDOCSCONTAINING for those I-addresses [INV-IADDRESS-PERMANENT, EC-STALE-SPANF-REFERENCE]. The result set is a **superset** of documents currently showing the content in their V-streams — it never shrinks below the set of documents that ever contained those I-addresses via INSERT or COPY.

VCOPY / CREATENEWVERSION follow the same `docopy` path and therefore also create DOCISPAN entries, giving the same guarantee [ST-COPY, ST-VERSION / Finding 0077].

---

### The silent-absence path: APPEND

APPEND (`doappend`) is the exception. The `insertspanf(taskptr, spanf, docptr, textset, DOCISPAN)` call is **explicitly commented out** in the implementation, accompanied by an uncertain developer comment (`/*zzz dies this put in granf?*/`). No DOCISPAN entry is created for appended content [EC-APPEND-NO-DOCISPAN, FC-APPEND-NO-DOCISPAN].

Consequence: a document containing material placed exclusively via APPEND will **not appear** in FINDDOCSCONTAINING results for that material, even though the content is physically present in the granfilade and accessible via retrieve. The formal postcondition for APPEND is `spanf' = spanf` — the spanfilade is unchanged.

---

### Summary table

| Operation | DOCISPAN created? | Document appears in FINDDOCSCONTAINING? |
|-----------|------------------|----------------------------------------|
| INSERT | Yes | Always (even after DELETE) |
| VCOPY / COPY | Yes | Always |
| CREATENEWVERSION | Yes (via `docopyinternal`) | Always |
| APPEND | **No** | **Never** |
| DELETE (after INSERT) | — (no-op on spanf) | Still yes (stale reference) |

The only path by which a document silently fails to appear for content it holds is APPEND [EC-APPEND-NO-DOCISPAN]. All other placement operations that go through `docopy` write the DOCISPAN entry and the document will be present in FINDDOCSCONTAINING for those I-addresses from that point forward, permanently.

---

## Code Exploration

I have traced all the relevant code paths. Here is the complete answer.

---

## Answer: FINDDOCSCONTAINING Self-Membership and the APPEND `insertspanf` Comment

### How FINDDOCSCONTAINING Works

`finddocscontaining` (`fns.c:20-32`) → `dofinddocscontaining` (`do1.c:15-23`) → `specset2ispanset` + `finddocscontainingsp`.

**`dofinddocscontaining` (`do1.c:15-23`):**
```c
bool dofinddocscontaining(typetask *taskptr, typespecset specset, typelinkset *addresssetptr)
{
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
    && finddocscontainingsp (taskptr, ispanset, addresssetptr));
}
```

**`finddocscontainingsp` (`spanf1.c:151-188`)** is the query engine. It constructs a `docspace` span with stream = `DOCISPAN = 4` (`xanadu.h:39`), width = 1, and for each I-span in the query:

```c
// spanf1.c:167-174
tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);
tumblerincrement (&docspace.width, 0, 1, &docspace.width);
for (; ispanset; ispanset = ispanset->next) {
    context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE,
                                   ispanset, SPANRANGE, (typeisa*)NULL);
    for (c = context; c; c = c->nextcontext) {
        movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);
        beheadtumbler (&docid, &document.address);
```

This is a 2D spanfilade lookup: ORGLRANGE is restricted to the DOCISPAN lane (first digit = 4), and SPANRANGE must overlap the query I-span. The document ISA is recovered by stripping the DOCISPAN prefix with `beheadtumbler`.

**For the document to appear in results**, two things must be true:
1. The query V-spans must resolve to I-spans via the document's POOM (`specset2ispanset` → `vspanset2ispanset` → `permute`).
2. Those I-spans must have DOCISPAN entries in the spanfilade (put there by `insertspanf(..., DOCISPAN)`).

---

### What Creates DOCISPAN Entries

Only `insertspanf` with `spantype = DOCISPAN` creates these entries. `insertspanf` (`spanf1.c:15-54`) prefixes the document ISA with the spantype:

```c
// spanf1.c:22
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```

and stores each I-span's address in `crumorigin.dsas[SPANRANGE]`. This produces the exact entries that `finddocscontainingsp` retrieves.

`insertspanf(..., DOCISPAN)` is called in exactly two places:

| Callsite | Function | Purpose |
|----------|----------|---------|
| `do1.c:62` | `docopy` | Used by INSERT and COPY |
| `do1.c:79` | `docopyinternal` | Used by CREATENEWVERSION |

```c
// do1.c:60-63  (docopy)
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)

// do1.c:78-79  (docopyinternal)
if (!insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)) return FALSE;
if (!insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)) return FALSE;
```

`insertpm` and `insertspanf(DOCISPAN)` are always called together. If INSERT succeeded (POOM entry exists), the DOCISPAN entry was also created. The query will find the document.

---

### The FEBE INSERT Path — Complete Chain

```
insert (fns.c:84)
  → doinsert (do1.c:87)
    → inserttextingranf (do1.c:118)   ← allocates I-space, returns ispanset
    → docopy (do1.c:119)
        → insertpm (do1.c:60)         ← POOM: maps V-addr → I-addr
        → insertspanf DOCISPAN (do1.c:62) ← spanfilade: maps I-addr → docISA ✓
```

The V-spans given to INSERT become POOM entries and DOCISPAN entries simultaneously. Querying those same V-spans goes V → I (via POOM) → docISA (via DOCISPAN). The document is always found.

---

### The APPEND Path — Is There a Silent-Absence Bug?

`doappend` (`do1.c:25-32`) shows a commented-out `insertspanf` call:

```c
bool doappend(typetask *taskptr, typeisa *docptr, typetextset textset)
{
  bool appendpm(),insertspanf(); /*zzz dies this put in granf?*/

    return (appendpm (taskptr, docptr, textset)/*&&
   appendpm includes insertspanf!   insertspanf(taskptr,spanf,docptr,textset,DOCISPAN)*/
    );
}
```

The comment reads: **"appendpm includes insertspanf!"** This is factually correct. Tracing `appendpm` (`orglinks.c:17-27`):

```c
bool appendpm(typetask *taskptr, typeisa *docisaptr, typetextset textset)
{
    if (!findorgl(taskptr, granf, docisaptr, &orglptr, WRITEBERT))
        return(FALSE);
    findvsatoappend((typecorecrum*)orglptr, &vsa);
    return (doinsert(taskptr, docisaptr, &vsa, textset)); // ← calls doinsert
}
```

`appendpm` calls `doinsert` (`orglinks.c:26`), which calls `docopy`, which calls `insertspanf(DOCISPAN)` at `do1.c:62`. The full APPEND chain:

```
doappend (do1.c:25)
  → appendpm (orglinks.c:17)
    → doinsert (orglinks.c:26)         ← same doinsert used by FEBE INSERT
      → docopy (do1.c:119)
          → insertspanf DOCISPAN (do1.c:62) ✓
```

**The commented-out explicit call was redundant, not missing.** Furthermore, it was wrong: it passed `textset` (TEXTID items) as the sporglset. When `insertspanf` handles TEXTID (`spanf1.c:34-42`), it uses the document ISA itself as the SPANRANGE address — not a proper I-space address. `finddocscontainingsp` queries by I-space address, so those entries would never match query I-spans and would be useless noise.

Leaving the commented-out call active would have created incorrect entries and done nothing for correctness. Removing it was right.

---

### Is APPEND Even a FEBE Command?

No. There is no `APPEND` in `requests.h`. `doappend` is only called from `sourceunixcommand` (`xumain.c:144`), the interactive Unix import tool. In the FEBE daemon (`be.c`):

- `init(1)` is called (`be.c:83`), which immediately overwrites: `requestfns[SOURCEUNIXCOMMAND] = nullfun;` (`init.c:72`)
- `sourceunixcommand` is also stubbed as a no-op: `bool sourceunixcommand(typetask *taskptr) { return 0; }` (`be.c:162`)

`doappend` is unreachable from the FEBE protocol.

---

### Summary

**Does the document always appear in its own FINDDOCSCONTAINING result?** Yes. Every FEBE path that inserts content calls `docopy` or `docopyinternal`, which call `insertspanf(DOCISPAN)` paired with `insertpm`. These are the two structures that FINDDOCSCONTAINING queries. If INSERT created a DOCISPAN entry, the document is always found.

**Is there any path where `insertspanf` is silently absent?** No. The commented-out `insertspanf` in `doappend` (`do1.c:29-31`) is not a missing call — the correct DOCISPAN insertion happens through `appendpm → doinsert → docopy → insertspanf`. The explicit call was removed because it was (a) redundant and (b) would have created wrong entries (using TEXTID with doc ISA as SPANRANGE, which `finddocscontainingsp` would never retrieve). The comment "appendpm includes insertspanf!" accurately describes why the explicit call is unnecessary. The APPEND path is also unreachable from FEBE in any case.
