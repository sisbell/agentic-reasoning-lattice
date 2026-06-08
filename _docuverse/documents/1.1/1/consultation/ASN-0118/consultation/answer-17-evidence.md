## Question 17 [evidence]

> When multiple documents already share the I-addresses being copied, does the new target's COPY make those documents' links discoverable from the target via I-address overlap in find_links?

## KB Synthesis

Yes, unambiguously. The answer follows directly from three interlocking mechanisms.

**COPY places shared I-addresses into the target's POOM.** [ST-VCOPY, ST-COPY] COPY does not allocate fresh I-addresses — it references existing ones in the target document's POOM. After the operation, the target's POOM maps V-positions to the same I-addresses already held by the other documents.

**`find_links` is purely I-address based.** [SS-FIND-LINKS] The operation converts the query specset to I-addresses via the target's POOM, then searches the spanfilade for links whose endpoint I-addresses intersect. The search has no awareness of which document(s) previously held those I-addresses or how many now share them.

**The spanfilade link index was populated at link creation time.** [ST-CREATE-LINK, SS-SPANF-OPERATIONS] When a link was originally created, `insertendsetsinspanf` indexed the endpoint I-addresses → link ISA in the spanfilade. That index entry persists permanently [INV-SPANF-WRITE-ONLY]. No subsequent COPY updates this index — COPY writes only to DOCISPAN (the document-discovery sub-index), not the link sub-index [FC-CONTENT-SPANF-ISOLATION, ST-COPY].

The invariant is stated explicitly: `∀ link, doc :: content_ids(link.source) ∩ content_ids(doc) ≠ ∅ ⟹ findable(link, doc)` [INV-LINK-GLOBAL-VISIBILITY]. As soon as COPY places the I-addresses in the target, this condition is satisfied.

Prior sharing history is irrelevant. Whether zero or a thousand other documents already share those I-addresses, the new target becomes able to discover all associated links through `find_links` the moment COPY completes. [INT-LINK-TRANSCLUSION]

---

## Code Exploration

I have all the evidence I need. Here is the full answer.

---

## When Multiple Documents Share I-Addresses: Link Discoverability via `find_links`

**Short answer: Yes.** When a COPY deposits source I-addresses into the target document's POOM and spanfilade, those same I-addresses become the search keys for `find_links`. Because the spanfilade query has no per-document filter, any link registered against those I-addresses — regardless of which document created it — is returned. This is the intended transclusional mechanism.

---

### Step 1 — COPY assigns source I-addresses unchanged to the target

`docopy` [do1.c:45–65]:

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)   // [do1.c:54]
    && findorgl (...)
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)          // [do1.c:60]
    && insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)       // [do1.c:62]
    );
}
```

`specset2ispanset` [do2.c:14–46] walks the **source** document's POOM via `vspanset2ispanset` to convert source V-spans → permascroll I-spans. The `ispanset` that comes out is the I-address range of the source content.

`insertpm` [orglinks.c:75–134] places those I-addresses **unchanged** into the target document's POOM:

```c
unpacksporgl (sporglset, &lstream, &lwidth, &linfo);        // [orglinks.c:101]
movetumbler (&lstream, &crumorigin.dsas[I]);                // [orglinks.c:105]
movetumbler (&lwidth, &crumwidth.dsas[I]);                  // [orglinks.c:109]
movetumbler (vsaptr, &crumorigin.dsas[V]);                  // [orglinks.c:113]
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V); // [orglinks.c:130]
```

The I-axis (`crumorigin.dsas[I]`, `crumwidth.dsas[I]`) receives the source I-addresses verbatim. The V-axis gets the target's V-address. There is no new I-address allocation.

`insertspanf` [spanf1.c:15–54] then registers those same I-spans in the **global spanfilade**:

```c
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);  // [spanf1.c:49]
movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);    // [spanf1.c:50]
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE); // [spanf1.c:51]
```

The ORGLRANGE axis [spanf1.c:22] encodes the **target document's ISA** prefixed by `DOCISPAN`. The SPANRANGE axis encodes the I-span. So after a copy, the global spanfilade has entries from every document that has ever referenced those I-spans — the original source, the new copy, and any prior copies.

---

### Step 2 — `find_links` searches by I-address with no document filter

`dofindlinksfromtothree` [do1.c:348–353] is a thin wrapper:

```c
bool dofindlinksfromtothree(typetask *taskptr, typespecset fromvspecset, ...)
{
    return findlinksfromtothreesp(taskptr, spanf, fromvspecset, ...);  // [do1.c:352]
}
```

`findlinksfromtothreesp` [spanf1.c:56–103] converts the query V-spec to I-addresses:

```c
specset2sporglset (taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);  // [spanf1.c:71]
sporglset2linkset (taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);  // [spanf1.c:77]
```

`specset2sporglset` walks the **calling document's** POOM to produce I-spans. Those become the SPANRANGE restriction for the spanfilade lookup.

Inside `sporglset2linkset` [sporgl.c:222–237]:

```c
int sporglset2linkset(..., typeispan *homeset, INT spantype)
{
  typeispan nullhomeset;
    if (TRUE||!homeset) {        // [sporgl.c:227] — the TRUE|| forces this branch always
        tumblerclear (&nullhomeset.stream);
        tumblerclear (&nullhomeset.width);
        nullhomeset.width.mantissa[0] = 100;   // [sporgl.c:230] — wide-open ORGLRANGE
        ...
        homeset = &nullhomeset;
    }
    sporglset2linksetinrange (taskptr, spanfptr, sporglset, linksetptr, homeset, spantype);
}
```

The `TRUE||!homeset` condition at [sporgl.c:227] means **even if a non-null `homeset` document filter is passed in, it is silently overridden with the wide-open range** (`width.mantissa[0] = 100`). No caller can restrict results to a single document through this path.

`sporglset2linksetinrange` [sporgl.c:239–269] then issues the retrieval:

```c
prefixtumbler(&orglrange->stream, spantype, &range.stream);   // [sporgl.c:257]
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, (typeisa*)infoptr);  // [sporgl.c:259]
for (c = context; c; c = c->nextcontext) {
    beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);  // [sporgl.c:264]
    onlinklist (taskptr, linksetptr, &linksa);
}
```

The spanfilade is queried: SPANRANGE = the I-span from the calling document's POOM; ORGLRANGE = wide-open (width 100). The result is every link ISA whose registered endpoint I-span overlaps the query I-span. There is no constraint on which document owns the link.

---

### The Full Picture

Given:
- Document A originally inserted text → got permascroll I-span X
- Document B copied from A → B's POOM maps B's V-addresses → I-span X; spanfilade records B→X
- Document C also copied from A → same, for C→X
- A link L was created with FROM endpoint pointing at A's content in I-span X → link L is registered in the spanfilade under X with prefix `LINKFROMSPAN`

When you call `find_links(from=B's content)`:
1. B's POOM is walked: B's V-span → I-span X
2. Spanfilade queried: SPANRANGE = X, ORGLRANGE = wide-open
3. Link L's registration matches (its FROM I-span is X)
4. L is returned — **even though L was created against document A**

Likewise for C. All three documents see L when queried for links from their copies of X.

---

### Why This Is Intentional

The comment at [sporgl.c:245] ("kluge to make links show thru to versions") and the explicit `docreatenewversion` path in [do1.c:260–298] — which uses `docopyinternal` [do1.c:66–82] to carry source I-addresses into new versions — confirm this is the design goal. I-address identity **is** the transclusion mechanism. Links registered against a permascroll I-span are discoverable from any document that holds a copy of content at that I-span. The spanfilade is a global index by I-address, and the `TRUE||` at [sporgl.c:227] ensures no caller can accidentally narrow that to a single document scope.
