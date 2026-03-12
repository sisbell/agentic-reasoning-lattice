## Question 19 [gregory]

> For a link whose target endset spans a region that has been partially deleted (some I-addresses still in V-streams, others orphaned), FOLLOWLINK returns only the surviving portion after I→V filtering — was partial endset resolution an acceptable design outcome, or should the system have signaled incompleteness to the caller?

## KB Synthesis

The KB describes the behavior precisely but is silent on whether it reflects considered design intent or an oversight. Here's what I can synthesize:

**What the system actually does**

FOLLOWLINK silently drops I-addresses with no current POOM mapping via `span2spanset` / `retrieverestricted` returning NULL [INV-ITOV-FILTERING, SS-FOLLOWLINK]. The caller receives a partial result with no flag indicating incompleteness. From [EC-GHOST-LINK]: three result states exist (full, partial, empty), and all three return `works: true`.

**The case that partial resolution is the intended design**

The architecture treats V-space as a mutable projection over a permanent I-space. I-addresses never die [INV-CONTENT-IMMUTABILITY, INV-NO-IADDR-REUSE]. A "deleted" endpoint is not destroyed — it is merely unreferenced in the queried document's POOM at this moment. [EC-GHOST-LINK] notes explicitly: "Reconstitution is always possible since I-addresses are permanent (P0)." The design appears to say: the link is pointing at real, permanent content; the current V-view of that content is simply incomplete. Returning what's visible is honest.

This is internally consistent with [EC-LINK-PARTIAL-SURVIVAL]: "The link validity predicate is per-I-span, not per-endset." Each I-span is independently valid. A partial result isn't a defective result — it's the correct answer about which pieces of the endpoint are *currently visible*.

**The case for signaling incompleteness**

The silent filtering makes FOLLOWLINK unable to distinguish between two structurally different situations:

- A link created with a narrow endpoint (was always small)
- A link whose endpoint was wider but is now partially orphaned

A caller cannot tell whether it received the full intended span or a truncated remnant. This matters for any application that needs to reason about link integrity or display "broken link" UI. The KB records no mechanism for a caller to ask "how many I-spans are in the endset vs. how many resolved."

**My read**

The silence is a design choice consistent with the whole system's philosophy — V-space is ephemeral, I-space is the ground truth. Signaling incompleteness would require the system to hold an opinion about what the "intended" extent of an endset was at creation time versus now, which would mean tracking that original extent separately. The system doesn't do this anywhere; permanence means you always get the current truth, not a diff from some prior state.

The real cost of this choice shows up in [PRE-FOLLOWLINK]: "The operation succeeds even when all endset I-addresses are unreferenced, returning an empty result." Empty success and partial success are treated identically to full success. For the Xanadu model, that's arguably correct — the permanent record has not changed, only the current document arrangement has. For practical application developers, it's a footgun.

**Bottom line**: Partial endset resolution appears to be an acceptable outcome *within the Xanadu permanence model*, not a signal that needs to propagate. But the system provides no affordance for distinguishing a whole endpoint from a fragment, which is a real expressiveness gap any spec should acknowledge as a known limitation rather than designed behavior.

Relevant entries: [SS-FOLLOWLINK], [INV-ITOV-FILTERING], [EC-GHOST-LINK], [EC-LINK-PARTIAL-SURVIVAL], [INV-CONTENT-IMMUTABILITY], [INV-LINK-PERMANENCE], [PRE-FOLLOWLINK], [EC-ORPHANED-LINK].

---

## Code Exploration

I now have enough confirmed source to give a thorough answer. Here it is.

---

## FOLLOWLINK and Partial Endset Resolution — A Code-Level Analysis

### The Execution Path

`followlink()` [fns.c:114–127] is the entry point:

```c
void followlink(typetask *taskptr)
{
  typeisa linkisa;
  typespecset specset;
  INT whichend;
  bool getfollowlink(), dofollowlink();

    if (
       getfollowlink (taskptr, &linkisa, &whichend)
    && dofollowlink (taskptr, &linkisa, &specset, whichend)){
        putfollowlink (taskptr, specset);
      }else
        putrequestfailed (taskptr);
}
```

The chain is: `getfollowlink` → `dofollowlink` → `putfollowlink`, or `putrequestfailed`. The protocol has exactly two outcomes: **success with a specset** or **request failed**. There is no third response type for "partial success."

`dofollowlink()` [do1.c:223–232]:

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
  typesporglset sporglset;
  bool link2sporglset(), linksporglset2specset();

    return (
       link2sporglset (taskptr, linkisaptr, &sporglset, whichend,NOBERTREQUIRED)
    && linksporglset2specset (taskptr,&((typesporgl *)sporglset)->sporgladdress, sporglset, specsetptr, NOBERTREQUIRED));
}
```

Two steps, short-circuited with `&&`:
1. **`link2sporglset()`** — reads the link's own enfilade to extract the endset as I-spans.
2. **`linksporglset2specset()`** — converts those I-spans to V-spans in the target document.

---

### Step 1: Extracting the Endset as I-spans

`link2sporglset()` [sporgl.c:67–95]:

```c
tumblerclear (&zero);
tumblerincrement (&zero, 0, whichend, &vspan.stream);  // V-position = whichend
tumblerincrement (&zero, 0, 1, &vspan.width);          // V-width = 1
if (context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL)) {
    for (c = context; c; c = c->nextcontext) {
        sporglptr = (typesporgl *)taskalloc(taskptr, sizeof(typesporgl));
        contextintosporgl((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);
        *sporglsetptr = (typesporglset)sporglptr;
        sporglsetptr = (typesporglset *)&sporglptr->next;
    }
    contextfree (context);
    return (TRUE);
} else{
    return (FALSE);    // ← fails if NO crums found at this V-position
}
```

This queries the **link's own enfilade** — not the target document — for I-addresses stored at V-position `whichend`. This step is asking "what I-spans does this link say its endset is?" It does not filter by whether those I-spans are currently visible anywhere. As long as the link exists and has a non-empty endset recorded at V-position `whichend`, this succeeds and returns I-spans.

---

### Step 2: Converting I-spans to V-spans (where partial deletion bites)

`linksporglset2specset()` [sporgl.c:97–123] always returns `TRUE` [line 122]:

```c
    return (TRUE);
```

Regardless of what happened inside. It calls `linksporglset2vspec()` [sporgl.c:127–137] → `sporglset2vspanset()` [sporgl.c:141–176] → `ispan2vspanset()` [orglinks.c:389–394] → `permute()` [orglinks.c:404–422] → `span2spanset()` [orglinks.c:425–454].

`span2spanset()` is where the partial deletion is silently swallowed:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
    context2span(c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist(taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
if(!context){           // ← NULL = no V-stream mapping for this I-span
    return(targspansetptr);   // ← return silently, contributing nothing
}
```

When `retrieverestricted()` returns `NULL` for a given I-span (because that I-span is no longer mapped into any V-stream — it is orphaned), the `for`-loop body never executes. The `if(!context)` branch [orglinks.c:446–448] returns with `targspansetptr` unchanged, adding **nothing** to the vspanset. No error, no flag, no log even in the debug build.

`permute()` [orglinks.c:404–422] loops over all I-spans in the restriction set, calling `span2spanset()` for each. If some return content and others silently return nothing, the caller sees only the content-returning ones:

```c
for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset,
                                  restrictionindex, targspansetptr, targindex);
}
return (save);    // ← returns the accumulated (possibly partial) set
```

---

### The Two Cases

**Case A — Total orphaning:** Every I-span in the endset has no V-stream mapping. `link2sporglset()` still succeeds (the link's own enfilade is intact). But then `linksporglset2specset()` will produce a `specset` containing a `VSPECID` entry whose `vspanset` is `NULL`. The caller receives a success response with an empty span set. (Or, if the link document itself no longer has any crums at V-position `whichend`, `link2sporglset()` fails at [sporgl.c:93] and the caller gets `REQUEST_FAILED`.)

**Case B — Partial orphaning:** Some I-spans still have V-mappings, others do not. `link2sporglset()` extracts all I-spans (they are intact in the link's enfilade). `linksporglset2specset()` iterates all sporgl entries. For orphaned I-spans, `span2spanset()` silently contributes nothing. For surviving I-spans, `span2spanset()` appends their corresponding V-spans. The returned `specset` contains **only the surviving portion**. `linksporglset2specset()` returns `TRUE`. `dofollowlink()` returns `TRUE`. `putfollowlink()` is called. **The caller has no way to detect that the result is incomplete.**

---

### Was This an Acceptable Design Outcome?

The code is unambiguous: **partial endset resolution was the implemented behavior, and incompleteness was never signaled.** The question is whether this was a conscious design decision or an oversight.

**The case that it was intentional:**

The Xanadu model treats I-addresses as permanent and V-streams as transient views. A link's endset is stored as I-spans in the link's own enfilade — permanent by construction. What `FOLLOWLINK` returns is "the current V-stream manifestation of those I-addresses." From this perspective, returning only the surviving portion is semantically correct: the system answers "here is where this endset appears right now," and if part of it appears nowhere, that part simply does not appear. This mirrors the general Xanadu philosophy that V-stream visibility is a property of a document's current state, not of the content itself.

The code structure supports this reading. `span2spanset()` at [orglinks.c:446–448] has an explicit `if(!context)` branch — it is not an omission, it is a handled case. The author knew it could happen and chose to return silently.

**The case that incompleteness signaling was missing:**

The FEBE protocol has no mechanism to report incompleteness. `putfollowlink()` transmits a `specset`; `putrequestfailed()` signals total failure. There is no middle response. Callers cannot distinguish:
- "This link had a 3-span endset and all 3 were resolved"
- "This link had a 3-span endset; 2 were resolved; 1 was orphaned"

`linksporglset2specset()` [sporgl.c:122] always returns `TRUE`, even when every `ispan2vspanset()` call produced an empty set. The result is structurally indistinguishable from a fully resolved one.

For any application relying on link integrity — transclusion auditing, citation completeness, referential consistency — the silent partial result is a protocol gap. The system provides no warranty of completeness and no mechanism to request one.

**The verdict from the code:**

The design treated "partial endset resolution" as a normal outcome of the I→V filtering step, consistent with the Xanadu model's distinction between permanent I-addresses and dynamic V-visibility. The system was not built to *promise* that every I-span in a link's endset would be reachable as a V-span at follow time. That would have required either a completeness guarantee on the I-stream (that no content ever truly disappears) or a richer protocol response type.

What the code does **not** do is give the caller tools to detect or respond to incompleteness. That is an omission — not necessarily a design error given the model, but a gap in the protocol surface. A system built on top of this would need to implement its own completeness check by fetching the endset's raw I-spans separately (via a different query path) and comparing against what `FOLLOWLINK` returned. The FEBE protocol as implemented offers no shortcut for this.

**Specific citations:**

| Claim | File:Line |
|---|---|
| Only two protocol outcomes: success or request-failed | `fns.c:124–126` |
| `link2sporglset` fails only if link's own enfilade is empty at `whichend` | `sporgl.c:83,92–93` |
| `linksporglset2specset` always returns TRUE | `sporgl.c:122` |
| Orphaned I-span silently contributes nothing to vspanset | `orglinks.c:446–448` |
| `permute` accumulates partial sets without error | `orglinks.c:414–416` |
| No incompleteness flag exists anywhere in `dofollowlink` chain | `do1.c:228–231` |
