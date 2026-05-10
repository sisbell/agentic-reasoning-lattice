## Question 15 [gregory]

> When an endset specset references content that spans multiple non-contiguous I-address ranges in the source document's POOM, does `vspanset2sporglset` split it into multiple sporgls before link creation, and are all resulting I-spans stored in the link orgl and independently indexed in the spanfilade?

## KB Synthesis

Yes to all three parts.

## Splitting into multiple sporgls

`vspanset2sporglset` always splits a V-span into one sporgl per contiguous I-address region, regardless of how many V-spans were provided as input. The conversion chain is:

V-span → `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` → one I-span per contiguous region → one sporgl per I-span.

When a V-span covers content transcluded from multiple source documents, those source documents contribute non-contiguous I-address ranges in the POOM. The inner loop in `vspanset2sporglset` (`sporgl.c:49-58`) iterates over every I-span returned by the V→I conversion and creates a separate sporgl for each. The front end sees a single contiguous V-selection; the backend decomposes it transparently. [SS-LINK-ENDPOINT] (Finding 0037), [ST-LINK-CREATE] (Finding 0037)

**Concrete example:**
```
Doc C has "AABB" at V 1.1..1.4:
  "AA" transcluded from doc A → I-addresses from A's permascroll
  "BB" transcluded from doc B → I-addresses from B's permascroll

create_link(source = V-span 1.1 width 0.4 in C)

Input:  1 V-span
Output: 2 sporgls:
  sporgl₁: origin=I-addr(A,"AA"), width=0.2, doc=C
  sporgl₂: origin=I-addr(B,"BB"), width=0.2, doc=C
```

## Storage in the link orgl

All resulting sporgls are stored as the link's endset. The link endset is internally `set<Sporgl>`, not `set<VSpan>`. The cardinality of the stored endset may exceed the number of input V-spans — one I-span per contiguous I-address region. [SS-LINK-ENDPOINT] (Finding 0037), [SS-SPORGL]

## Independent indexing in the spanfilade

Yes. `insertendsetsinspanf()` (`do2.c:116-128`) receives the full sporglset for each endpoint type (FROM, TO, THREE) and inserts each sporgl as a separate entry into the spanf index, tagged with the link ISA and endpoint type. The spanf maps: `I-address-range → (link-ISA, endpoint-type)`. Each sporgl produces an independent spanf entry covering its own I-address range.

This is why partial I-address overlap is sufficient for `find_links` to discover a link — each sporgl is indexed independently, so matching any one of them returns the link. [INT-SPORGL-LINK-INDEX] (Finding 0013), [ST-CREATE-LINK] (Finding 0012)

The formal postcondition for `create_link`:
```
link.source_endset = { sporgl(origin=i.start, width=i.width, doc=source_doc)
                       | i ∈ V_to_ISpans(source_doc, source_vspan) }

spanf' = spanf ∪ { i-range → (link_isa, LINKFROMSPAN)
                   | i-range ∈ endset_iranges(link.source) }
       ∪ { i-range → (link_isa, LINKTOSPAN)
                   | i-range ∈ endset_iranges(link.target) }
       (+ THREE endset similarly)
```

---

## Code Exploration

Now I have everything I need. Let me trace the full execution path with all citations.

---

## Answer

### The Short Answer

**Yes on both counts.** When an endset's vspanset references content spanning multiple non-contiguous I-address ranges in the source document's POOM, `vspanset2sporglset` does split it into one sporgl per contiguous I-range. Each resulting sporgl is then independently inserted into the link's POOM orgl **and** independently indexed in the spanfilade. Here is the full traced execution:

---

### Step 1: Entry into link creation

`createlink` in `fns.c:100-112` calls `docreatelink` in `do1.c:195`:

```c
// do1.c:195-221
bool docreatelink(typetask *taskptr, typeisa *docisaptr, typespecset fromspecset, ...)
{
  ...
  && specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)   // line 214
  && specset2sporglset (taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)   // line 215
  && specset2sporglset (taskptr, threespecset,&threesporglset,NOBERTREQUIRED)   // line 216
  && setlinkvsas (&fromvsa, &tovsa, &threevsa)                                  // line 217
  && insertendsetsinorgl (taskptr, linkisaptr, link,
         &fromvsa, fromsporglset, &tovsa, tosporglset, ...)                     // line 218
  && insertendsetsinspanf (taskptr, spanf, linkisaptr,
         fromsporglset, tosporglset, threesporglset)                            // line 219
```

---

### Step 2: `specset2sporglset` dispatches to `vspanset2sporglset`

`sporgl.c:14-33`:

```c
bool specset2sporglset(typetask *taskptr, typespecset specset,
                       typesporglset *sporglsetptr, int type)
{
    ...
    for (; specset; specset = ...) {
        if (itemid == ISPANID) {
            *sporglsetptr = (typesporglset)specset;            // pass through
        } else if (itemid == VSPECID) {
            sporglsetptr = vspanset2sporglset(taskptr,         // line 25
                &((typevspec *)specset)->docisa,
                ((typevspec *)specset)->vspanset,
                sporglsetptr, type);
        }
    }
```

For a client-supplied V-space specset (the normal case), each `VSPECID` entry — including its full `vspanset` list — is passed to `vspanset2sporglset`.

---

### Step 3: `vspanset2sporglset` — the splitting site

`sporgl.c:35-65`:

```c
typesporglset *vspanset2sporglset(typetask *taskptr, typeisa *docisa,
    typevspanset vspanset, typesporglset *sporglsetptr, int type)
{
  typeorgl orgl;
  typesporgl *sporglset;
  typeispanset ispanset;

    ispanset = NULL;
    if (!findorgl(taskptr, granf, docisa, &orgl, type))       // line 44 - find source doc POOM
        return(NULL);
    for (; vspanset; vspanset = vspanset->next) {             // line 47 - for each vspan
        (void) vspanset2ispanset(taskptr, orgl, vspanset,     // line 48 - V→I conversion
                                 &ispanset);
        for (; ispanset; ispanset = ispanset->next) {         // line 49 - for each resulting ispan
            sporglset = (typesporgl *) taskalloc(...);
            sporglset->itemid = SPORGLID;
            movetumbler(docisa, &sporglset->sporgladdress);   // source doc ISA
            movetumbler(&ispanset->stream, &sporglset->sporglorigin); // I-origin
            movetumbler(&ispanset->width,  &sporglset->sporglwidth);  // I-width
            *sporglsetptr = (typesporglset)sporglset;
            sporglsetptr  = (typesporglset *)&sporglset->next;
        }
    }
    return(sporglsetptr);
}
```

The critical structure is the **nested loop** at lines 47–58:

- **Outer loop** (line 47): iterates the vspanset — each client-supplied V-span.
- **`vspanset2ispanset`** (line 48): calls `permute()` in `orglinks.c:404`, which calls `span2spanset()` → `retrieverestricted()`. This walks the POOM enfilade looking for every I-address range that maps to the queried V-span. If the content at that V-address was assembled from three non-contiguous source regions (e.g., copied from I-spans A, B, C into the POOM), `retrieverestricted` returns **three separate context records**, and `permute` converts each into a distinct `typeispan` in `ispanset`.
- **Inner loop** (line 49): allocates **one sporgl per ispan**. So if a single vspan maps to three discontiguous I-ranges, you get three sporgls appended to the sporglset.

---

### Step 4: All sporgls inserted into the link's POOM via `insertendsetsinorgl`

`do2.c:130-148`:

```c
bool insertendsetsinorgl(typetask *taskptr, tumbler *linkisaptr, typeorgl link,
    tumbler *fromvsa, typesporglset fromsporglset, ...)
{
    insertpm(taskptr, linkisaptr, link, fromvsa, fromsporglset)   // line 132
    && insertpm(taskptr, linkisaptr, link, tovsa, tosporglset)    // line 133
```

`insertpm` in `orglinks.c:75-134` iterates the sporglset:

```c
for (; sporglset; sporglset = sporglset->xxxxsporgl.next) {   // line 100
    unpacksporgl(sporglset, &lstream, &lwidth, &linfo);        // line 101
    movetumbler(&lstream, &crumorigin.dsas[I]);                // line 105 - I-stream → origin
    movetumbler(&lwidth,  &crumwidth.dsas[I]);                 // line 109 - I-width
    movetumbler(vsaptr,   &crumorigin.dsas[V]);                // line 113 - V position in link
    ...
    insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V); // line 130
    tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr);            // line 131 - advance V address
}
```

Each sporgl (= each distinct I-range from the source doc) becomes **one crum in the link's POOM**, inserted at a sequentially advancing V-address within the link. The I-addresses are preserved in the crum's `dsas[I]` fields. Three non-contiguous source I-ranges → three crums in the link orgl, placed at consecutive V positions `1.1`, `1.1+w1`, `1.1+w1+w2`, etc.

---

### Step 5: All sporgls indexed independently in the spanfilade via `insertendsetsinspanf`

`do2.c:116-128`:

```c
bool insertendsetsinspanf(typetask *taskptr, typespanf spanfptr,
    typeisa *linkisaptr, typesporglset fromsporglset, ...)
{
    insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)   // line 119
    && insertspanf(taskptr, spanfptr, linkisaptr, tosporglset, LINKTOSPAN)    // line 120
    // optional: insertspanf(..., threesporglset, LINKTHREESPAN)              // line 123
```

`insertspanf` in `spanf1.c:15-54` iterates the sporglset:

```c
for (; sporglset; sporglset = ...) {                       // line 25
    if (itemid == SPORGLID) {
        movetumbler(&sporglset->sporglorigin, &lstream);   // line 31 - I-origin
        movetumbler(&sporglset->sporglwidth,  &lwidth);    // line 32 - I-width
        movetumbler(&sporglset->sporgladdress,&linfo.homedoc); // line 33 - source doc ISA
    }
    movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);    // line 49
    movetumbler(&lwidth,  &crumwidth.dsas[SPANRANGE]);     // line 50
    insertnd(taskptr, (typecuc*)spanfptr,                  // line 51
             &crumorigin, &crumwidth, &linfo, SPANRANGE);
}
```

Again one `insertnd` call per sporgl. Each non-contiguous I-range becomes its own independent entry in the spanfilade, keyed by its I-address range and tagged with the link's ISA and the endset role (LINKFROMSPAN = 1, LINKTOSPAN = 2, LINKTHREESPAN = 3 — set in `crumorigin.dsas[ORGLRANGE]` via `prefixtumbler` at `spanf1.c:22`).

---

### Summary

| Question | Answer | Key site |
|---|---|---|
| Does `vspanset2sporglset` split a vspan that maps to N non-contiguous I-ranges into N sporgls? | **Yes** — inner loop at `sporgl.c:49-58`, one sporgl per `ispan` returned by `vspanset2ispanset` | `sporgl.c:47-58` |
| Are all resulting I-spans stored in the link orgl? | **Yes** — `insertendsetsinorgl` → `insertpm` iterates the full sporglset, one `insertnd` per sporgl | `orglinks.c:100-131` |
| Are all resulting I-spans indexed independently in the spanfilade? | **Yes** — `insertendsetsinspanf` → `insertspanf` iterates the full sporglset, one `insertnd` per sporgl | `spanf1.c:25-51` |

The system makes **no attempt to re-merge** split sporgls at any stage. Each contiguous I-range from the source document ends up as exactly one crum in the link orgl and one crum in the spanfilade, with its original I-address range preserved intact. This means that a link endset referencing V-content assembled from three scattered source regions will create three independently findable spanfilade entries — all pointing to the same link ISA and the same endset role.
