## Question 14 [evidence]

> For an endset that overlaps the region, is the span returned the portion that touches the region, or the endset's complete I-span as stored in the link orgl regardless of how much of it falls inside the region?

## KB Synthesis

The KB does not contain direct code-level evidence for RETRIEVEENDSETS clipping spans to the intersection boundary, but the available architecture evidence points strongly toward **the complete stored endset span**, not just the overlapping portion.

**Evidence from RETRIEVEENDSETS mechanism** [SS-RETRIEVE-ENDSETS] (Finding 0035): The call chain converts the input specset to I-addresses, then calls `retrievesporglsetinrange()` to search the spanfilade. The results are passed to `linksporglset2specset()` which converts I-addresses back to V-addresses using the *querying document's* docid. Crucially, the finding describes no clipping or intersection-trimming step — the sporgls returned from the spanfilade search are converted wholesale.

**Evidence from FOLLOWLINK** [SS-FOLLOWLINK] (Finding 0048) and [SS-FOLLOW-LINK] (Finding 0028): FOLLOWLINK explicitly returns the complete endset as stored in the link orgl — "There is no filtering, subsetting, or adaptation based on the caller's document or the search that discovered the link." While RETRIEVEENDSETS routes through the spanfilade rather than the link orgl directly, the stored sporgls in the spanfilade were inserted as complete endset spans [INT-SPORGL-LINK-INDEX] (Finding 0013), and the 2D enfilade retrieval (`findcbcinarea2d`) accumulates full leaf nodes [SS-POOM-MULTIMAP] (Finding 0039) — there is no evidence of width truncation at intersection boundaries.

**The V-address resolution step is the effective filter.** [INV-ITOV-FILTERING] (Finding 0048) establishes that unreferenced I-addresses are silently dropped during I-to-V conversion. So even if the returned sporgl covers a wider I-address range than the query, `linksporglset2specset()` will only produce V-spans for those I-addresses that are actually present in the querying document's POOM.

**Summary:** RETRIEVEENDSETS returns the complete stored endset I-span. The intersection with the query region determines *which links are found*, not *how much of their endsets are reported*. The practical filtering happens at V-address resolution time, not at spanfilade search time.

---

## Code Exploration

I now have the complete picture from all relevant functions. Here is the full answer.

---

## Answer: The Complete Endset I-span Is Returned, Not the Clipped Portion

The code returns **the endset's complete I-span as stored in the link orgl**, regardless of how much of it falls inside the query region. The clipping mechanism exists in the codebase but is deliberately not applied in the endset retrieval path.

---

### The Two Code Paths: Clipping vs. No-Clipping

There are two distinct functions for extracting a span from a context node. Their behavior is fundamentally different.

**`context2span` — clips to the query region** (`context.c:176`):
```c
int context2span(typecontext *context, typespan *restrictionspanptr, INT idx1,
                 typespan *foundspanptr, INT idx2)
{
    movetumbler(&restrictionspanptr->stream, &lowerbound);
    tumbleradd(&lowerbound, &restrictionspanptr->width, &upperbound);
    prologuecontextnd(context, &grasp, &reach);

    if (tumblercmp(&grasp.dsas[idx1], &lowerbound) == LESS) {
        // crum starts left of query: advance the idx2 start proportionally
        tumblerincrement(&grasp.dsas[idx2], 0,
            (INT)tumblerintdiff(&lowerbound, &grasp.dsas[idx1]),
            &grasp.dsas[idx2]);
    }
    if (tumblercmp(&reach.dsas[idx1], &upperbound) == GREATER) {
        // crum ends right of query: retreat the idx2 end proportionally
        tumblerincrement(&reach.dsas[idx2], 0,
            -tumblerintdiff(&reach.dsas[idx1], &upperbound),
            &reach.dsas[idx2]);
    }
    movetumbler(&grasp.dsas[idx2], &foundspanptr->stream);
    tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width);
}
```

This function explicitly clips: it computes how far the crum overshoots the restriction on each side and trims the output span in `idx2` by exactly that amount. It is used in the **V→I content-retrieval path** (`vspanset2ispanset` → `permute` → `span2spanset`, `orglinks.c:443`).

**`contextintosporgl` — no clipping, full crum width** (`sporgl.c:205`):
```c
int contextintosporgl(type2dcontext *context, tumbler *linkid, typesporgl *sporglptr, INT index)
{
    sporglptr->itemid = SPORGLID;
    sporglptr->next = NULL;
    movetumbler(/*linkid*/&context->context2dinfo.homedoc, &sporglptr->sporgladdress);
    movetumbler(&context->totaloffset.dsas[index], &sporglptr->sporglorigin);
    ...
    movetumbler(&context->contextwid.dsas[index], &sporglptr->sporglwidth);
}
```

It copies `context->totaloffset` and `context->contextwid` directly — the crum's own stored span, untouched by the restriction bounds. This is used in **every endset retrieval path**.

---

### The Endset Retrieval Path (`doretrieveendsets`)

`doretrieveendsets` (`do1.c:369`) → `retrieveendsetsfromspanf` (`spanf1.c:190`) → `retrievesporglsetinrange` (`spanf1.c:237`):

```c
bool retrievesporglsetinrange(typetask *taskptr, typesporglset sporglptr,
                              typespan *whichspace, typesporglset *sporglsetptr)
{
    for (; sporglptr; sporglptr = ...) {
        context = retrieverestricted(
            (typecuc*)spanf,
            (typespan*)sporglptr, SPANRANGE,   // restriction: query I-span
            whichspace, ORGLRANGE,             // restriction: endset lane (FROM/TO)
            (typeisa*)NULL);

        for (c = context; c;) {
            sporglset = taskalloc(sizeof(typesporgl));
            contextintosporgl((type2dcontext*)c, (tumbler*)NULL, sporglset, SPANRANGE);
            ...
        }
    }
}
```

`retrieverestricted` finds every crum in the spanfilade whose SPANRANGE (I-space) intersects the query I-span **and** whose ORGLRANGE (endset lane) matches. But `contextintosporgl` then extracts from that context its **full crum I-span** — `context->contextwid.dsas[SPANRANGE]` — not the intersection.

Since each link endset is stored as its own crum in the spanfilade (inserted one-at-a-time via `insertspanf`, `spanf1.c:51`: `insertnd(taskptr, spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE)`), the "full crum I-span" equals exactly the complete endset I-span as recorded at link creation time.

---

### The Same Behavior in `dofollowlink`

`dofollowlink` (`do1.c:223`) → `link2sporglset` (`sporgl.c:67`):

```c
bool link2sporglset(typetask *taskptr, typeisa *linkisa, typesporglset *sporglsetptr,
                    INT whichend, int type)
{
    ...
    tumblerincrement(&zero, 0, whichend, &vspan.stream);  // slot: 1=FROM, 2=TO
    tumblerincrement(&zero, 0, 1, &vspan.width);          // one-unit slot width

    if (context = retrieverestricted((typecuc*)orgl, &vspan, V, NULL, I, NULL)) {
        for (c = context; c; c = c->nextcontext) {
            contextintosporgl((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);
            ...
        }
    }
}
```

Same pattern: `retrieverestricted` searches the link's own POOM orgl restricted to V-space slot `[whichend, whichend+1]`, then `contextintosporgl` with `index=I` extracts the **complete I-span of the endset crum** stored there.

---

### Why No Clipping in the Final V-span Output

After `contextintosporgl` produces a sporgl containing the complete endset I-span, `linksporglset2specset` (`sporgl.c:97`) converts it back to V-space via `sporglset2vspanset` → `ispan2vspanset` → `permute` → `context2span`. At this stage `context2span` IS called, but with the restriction set to the full endset I-span itself. Because the restriction exactly matches the stored crum extent, neither clipping condition in `context2span` fires — the output is the complete endset V-span.

---

### Summary

| Path | Function used | Returns |
|------|--------------|---------|
| V→I content retrieval (`vspanset2ispanset`) | `context2span` | **Clipped** I-span: only the portion inside the query |
| Endset retrieval (`retrievesporglsetinrange`, `link2sporglset`) | `contextintosporgl` | **Complete** endset I-span as stored |

For an endset that overlaps the query region, the span returned is the **complete I-span as stored in the link orgl**, not the portion that touches the region. The overlap test (`crumqualifies2d` / `retrieverestricted`) determines *which* endsets are found; `contextintosporgl` then returns their *complete* extents. The proportional clipping of `context2span` (`context.c:191–203`) is strictly a content-retrieval tool — it does not participate in any link-following or endset-enumeration code path.
