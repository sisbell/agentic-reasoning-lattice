## Question 1 [evidence]

> In the implementation, does content placement into a document's arrangement strictly precede the reverse-index/provenance recording, so that a state earlier than the recording event always witnessed the containment?

## KB Synthesis

Yes, within the `docopy` call chain, POOM placement strictly precedes spanfilade recording — `insertpm` is called before `insertspanf(..., DOCISPAN)` [ST-INSERT, Finding 0036; SS-DOCISPAN, Finding 0047].

The sequential call chain is:

```
doinsert → inserttextingranf → docopy → insertpm (POOM)
                                      → insertspanf (DOCISPAN)
```

So a hypothetical observer at the intermediate point would see content in the V-arrangement but not yet in the reverse index.

**However, no such observer can exist.** The single-threaded run-to-completion event loop makes the entire operation uninterruptible — no other session or operation can execute between `insertpm` and `insertspanf` [INV-ATOMICITY, INV-SEQUENTIAL-DISPATCH]. The intermediate state is real in code but unreachable externally.

**Three important asymmetries to note:**

1. **APPEND breaks the pattern entirely** — it calls only `insertpm` (or `appendpm`) and never calls `insertspanf`, so POOM placement occurs with no DOCISPAN recording at all [EC-APPEND-NO-DOCISPAN, FC-APPEND-NO-DOCISPAN].

2. **DELETE is the inverse asymmetry** — it removes from the POOM via `deletend` but never touches the spanfilade, creating permanent divergence where the reverse index overclaims [ST-DELETE Finding 0057; INV-SPANF-WRITE-ONLY; INT-DELETE-SPANF-DIVERGENCE].

3. **Crash safety** — if a crash occurs between the two writes before `writeenfilades()` flushes to disk, the on-disk state can be inconsistent in either direction [SS-DURABILITY-BOUNDARY, EC-CRASH-MID-WRITE]. The ordering guarantee holds only for the in-memory, within-session execution path.

---

## Code Exploration

I now have all the evidence needed. Here is the full answer.

---

## Does Content Placement Strictly Precede Reverse-Index Recording?

**Yes — within the `docopy()` call chain, the POOM insertion (document arrangement) is strictly sequenced before the spanfilade insertion (reverse-index/provenance). The invariant holds for that pair.**

But the granfilade write — which allocates the ISA address for the text — happens *before* either, creating a narrow transient state that deserves careful attention.

---

### The Three-Phase Write Sequence

#### Phase 1 — Granfilade write: `do1.c:118`

```c
/* do1.c:117-119 */
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)  /* line 118 */
    && docopy (taskptr, docisaptr, vsaptr, ispanset)                  /* line 119 */
);
```

`inserttextingranf()` calls `inserttextgr()` in `granf2.c`:

```c
/* granf2.c:95-107 */
for (; textset; textset = textset->next) {
    locinfo.infotype = GRANTEXT;
    locinfo.granstuff.textstuff.textlength = textset->length;
    movmem(textset->string, locinfo.granstuff.textstuff.textstring,
           locinfo.granstuff.textstuff.textlength);
    insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);    /* line 99 — bytes into granfilade */
    tumblerincrement (&lsa, 0, textset->length, &lsa);
}
ispanptr = (typeispan *) taskalloc (taskptr, sizeof(typeispan));  /* line 102 */
...
*ispansetptr = ispanptr;   /* line 107 — ispan returned to caller */
```

The raw text bytes are stored in the **granfilade** at a freshly allocated ISA address. The `ispanset` (a content-space span record) is returned. At this moment: **the content exists in the content store but is in no document's arrangement yet.**

#### Phase 2 — POOM insertion (document arrangement): `do1.c:60`

`docopy()` [do1.c:45-65] is a `&&`-chained sequence:

```c
/* do1.c:53-64 */
return (
   specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)  /* 54 */
&& findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)       /* 55 */
&& acceptablevsa (vsaptr, docorgl)                                  /* 56 */
&& asserttreeisok(docorgl)                                          /* 57 */

/* the meat of docopy: */
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)        /* 60 — POOM */

&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)    /* 62 — spanfilade */
&& asserttreeisok(docorgl)                                          /* 63 */
);
```

`insertpm()` [orglinks.c:75] writes the VSA→ISA mapping into the document's POOM enfilade. This is the **document arrangement** — the forward index that makes the content reachable from the document's virtual address space.

#### Phase 3 — Spanfilade insertion (reverse-index): `do1.c:62`

`insertspanf()` [spanf1.c:15] records the ISA→document reverse mapping — given a content-space address, which document owns it at what virtual address. This is the **provenance/reverse-index**.

---

### Does the Invariant Hold?

**For the POOM/spanfilade pair: yes, unconditionally.**

The `&&` short-circuit at `do1.c:60-62` enforces strict ordering. `insertspanf()` is only reached if `insertpm()` returns TRUE. There is no code path where the spanfilade gains an entry without the POOM already recording containment. A state that witnesses the spanfilade entry always already witnessed the POOM entry.

```
insertpm() succeeds   →   insertspanf() runs
insertpm() fails      →   insertspanf() is never reached (short-circuit)
```

The converse asymmetry exists: if `insertpm()` succeeds but `insertspanf()` fails, the POOM has the content with no reverse-index entry. That is a different kind of inconsistency, but it does not violate the stated invariant.

**For the granfilade/POOM pair: there is a genuine transient window.**

At `do1.c:118`, text bytes exist in the granfilade with a valid ISA address. Between line 118 completing and line 119 (`docopy`) completing, the content is allocated in the content store but is not yet in any document's POOM. No spanfilade entry exists either — so the reverse-index invariant itself still holds — but the *content* is "live" in the system without being contained by the document arrangement. Whether this window is observable depends on whether any concurrent reader could query the granfilade by ISA directly during that window. The single-threaded `select`-based event loop in `bed.c` means no concurrent operation can interleave here; the window is not externally observable within a single session.

---

### The `fns.c` Response-Before-Operation Anomaly

There is a separate ordering anomaly in the insert handler worth noting:

```c
/* fns.c:90-92 */
(void) getinsert (taskptr, &docisa, &vsa, &textset);   /* parse */
putinsert (taskptr);                                    /* ACK sent to client */
if (!doinsert (taskptr, &docisa, &vsa, textset))       /* operation executes after ACK */
```

The client receives a success acknowledgment (line 91) **before** `doinsert()` executes (line 92). The commented-out original implementation (fns.c:69-82) correctly sent the response only after `doinsert()` succeeded. This is described inline as a "kluged unix version for speed." This does not affect the internal data-structure ordering question but means the client's perceived state may precede the actual system state change.

---

### Summary

| Step | Call site | Structure written | Phase |
|------|-----------|-------------------|-------|
| 1 | `do1.c:118` via `granf2.c:99` | granfilade (`insertseq`) | content allocated at ISA |
| 2 | `do1.c:60` via `orglinks.c:75` | POOM (`insertpm`) | document arrangement VSA→ISA |
| 3 | `do1.c:62` via `spanf1.c:15` | spanfilade (`insertspanf`) | reverse index ISA→doc VSA |

Content placement into the document arrangement (POOM, step 2) **strictly precedes** reverse-index recording (spanfilade, step 3) — enforced by `&&` short-circuit at `do1.c:60-62`. Any state that has witnessed the spanfilade entry has necessarily already witnessed the POOM containment. The stated invariant holds.
