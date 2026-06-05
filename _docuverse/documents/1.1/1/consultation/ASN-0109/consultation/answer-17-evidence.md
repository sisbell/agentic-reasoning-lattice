## Question 17 [evidence]

> If a single logical endset was split into multiple sporgl entries at creation time (content spanning non-contiguous I-ranges), does the read return multiple spans, and does the reader see them as one endset or several?

## KB Synthesis

## Endset Read-Back When Split at Creation

**At creation time:** A single input V-span covering content from non-contiguous I-address ranges is automatically split into multiple sporgls — one per contiguous I-address region. The inner loop in `vspanset2sporglset` (`sporgl.c:49-58`) creates a separate sporgl for each I-span returned by `vspanset2ispanset`. [SS-LINK-ENDPOINT/Finding 0037, ST-LINK-CREATE/Finding 0037]

**On retrieval:** Both RETRIEVEENDSETS and FOLLOWLINK use the same `linksporglset2specset` → `span2spanset` → `retrieverestricted` pipeline to convert stored sporgls back to V-addresses. Each sporgl is converted independently, producing one V-span per surviving sporgl. [SS-FOLLOWLINK/Finding 0048, SS-RETRIEVE-ENDSETS/Finding 0035]

**What the reader sees:** The multiple V-spans are returned together as a single endset — one `from-endset` (or `to-endset`) specset containing multiple VSpec entries. The caller sees one endset; that endset has multiple spans. [SS-LINK-ENDPOINT/Finding 0037]

**Two qualifications:**

1. **Silent dropping** — if some I-addresses have no current POOM mapping (deleted content), `retrieverestricted` returns NULL and those sporgls are silently omitted. [INV-ITOV-FILTERING/Finding 0048, EC-LINK-PARTIAL-SURVIVAL/Finding 0037]

2. **Duplication artifact** — multi-span endsets can return duplicate spans (the same span appearing twice). This is a known edge case. [EC-MULTISPAN-LINK-DUPLICATION/Finding 0019, EC-PIVOT-LINK-FRAGMENTATION/Finding 0019]

---

## Code Exploration

Now I have all the pieces to give a complete, code-cited answer. Let me compile it.

---

## Answer: Non-Contiguous I-Ranges in a Single Logical Endset

### Creation: Each I-range becomes a separate crum

When `docreatelink` [do1.c:195] creates a link, the chain is:

```
docreatelink → specset2sporglset [sporgl.c:14] → vspanset2sporglset [sporgl.c:35]
```

`vspanset2sporglset` [sporgl.c:47–58] converts each vspan through `vspanset2ispanset` → `permute` → `span2spanset` [orglinks.c:425]. Each resulting ispan becomes its own `typesporgl` node in the linked list.

Then `insertendsetsinspanf` [do2.c:116] → `insertspanf` [spanf1.c:15] iterates that list:

```c
/* spanf1.c:25 */
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    ...
    insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
}
```

**One `insertnd` call per sporgl** [spanf1.c:51]. Non-contiguous I-ranges → distinct crums in the spanfilade.

The same happens inside `insertpm` [orglinks.c:100–132] for the link's permutation matrix:
```c
/* orglinks.c:100 */
for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
    ...
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
    tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);  /* vsaptr advances */
}
```

Each sporgl's I-range occupies consecutive V-positions in the link's orgl, but they remain physically separate crums.

---

### Retrieval: All crums collected, then grouped by document

`retrieveendsets` [fns.c:350] → `doretrieveendsets` [do1.c:369] → `retrieveendsetsfromspanf` [spanf1.c:190].

Inside `retrieveendsetsfromspanf`, the call chain is:

```c
/* spanf1.c:222–224 */
specset2sporglset (taskptr, specset, &sporglset, NOBERTREQUIRED)
&& retrievesporglsetinrange(taskptr, sporglset, &fromspace, &fromsporglset)
&& linksporglset2specset (taskptr, &((typevspec *)specset)->docisa, fromsporglset, fromsetptr, NOBERTREQUIRED)
```

**Step 1 — `retrievesporglsetinrange` [spanf1.c:237–267]** iterates the input sporglset and calls `retrieverestricted` on the spanfilade for each, accumulating one output sporgl per matching context:

```c
/* spanf1.c:244–264 */
for (; sporglptr; sporglptr = (typesporglset)sporglptr->xxxxsporgl.next) {
    context = retrieverestricted((typecuc*)spanf, (typespan*)sporglptr, SPANRANGE, whichspace, ORGLRANGE, (typeisa*)NULL);
    for (c = context; c;) {
        sporglset = (typesporgl*) taskalloc(taskptr, sizeof(typesporgl));
        contextintosporgl((type2dcontext*)c, (tumbler*)NULL, sporglset, SPANRANGE);
        *sporglsetptr = (typesporglset)sporglset;
        sporglsetptr = (typesporglset*)&sporglset->next;
        tmp = c->nextcontext;
        c = tmp;
    }
    contextfree(context);
}
```

N stored crums (one per non-contiguous I-range) → N contexts → **N sporgls in `fromsporglset`**.

**Step 2 — `linksporglset2specset` [sporgl.c:97–123]** converts sporgls back to specset items. For each sporgl, it calls `linksporglset2vspec` [sporgl.c:127], which calls `sporglset2vspanset` [sporgl.c:141–176]:

```c
/* sporgl.c:158–175 */
for (;;) {
    sporglptr = sporglptr->next;
    if (
       !sporglptr
    || !(sporglptr->itemid == SPORGLID)
    || !tumblereq (&((typesporgl *)sporglptr)->sporgladdress,
                   &((typesporgl *)(*sporglsetptr))->sporgladdress))
        return(0);
    *sporglsetptr = (typesporglset)sporglptr;
    ...
    vspansetptr = ispan2vspanset(taskptr, orgl, &ispan, vspansetptr);
}
```

The loop **groups consecutive sporgls that share the same `sporgladdress`** (same document ISA) into one `typevspec`, with each I-range becoming an additional vspan via `ispan2vspanset` [orglinks.c:389]. The grouping advances `*sporglsetptr` so the outer loop in `linksporglset2specset` skips the already-consumed sporgls.

**Result**: all N sporgls for the same document → **one `typevspec`** with N vspans in its `vspanset`.

---

### Wire encoding: One endset, multiple spans

`putretrieveendsets` [putfe.c:356–362] calls `putitemset` for each endpoint set:

```c
putitemset (taskptr, (typeitemset)fromset);
```

`putitemset` [putfe.c:124–141] emits a count then iterates items. For a `VSPECID`:

```c
/* putfe.c:157–162 */
case VSPECID:
    xuputc (VSPECFLAG, outfile);
    xuputc (WORDELIM, outfile);
    puttumbler (outfile, &((typevspec*)itemptr)->docisa);
    putitemset (taskptr, (typeitemset)((typevspec*)itemptr)->vspanset);
    break;
```

The wire format is: `[VSPECFLAG] [docisa tumbler] [N] [vspan₀ stream] [vspan₀ width] ... [vspanₙ stream] [vspanₙ width]`

---

### Direct answer to both sub-questions

**Does the read return multiple spans?** Yes — `retrieveendsets` returns one `typevspec` whose `vspanset` is a linked list of `typevspan` items, one per originally-non-contiguous I-range (after conversion back through `ispan2vspanset`). The list may be even longer if any I-range maps to multiple non-contiguous V-ranges due to rearrangement.

**Does the reader see them as one endset or several?** **One endset.** `sporglset2vspanset` [sporgl.c:141–176] groups all sporgls with the same `sporgladdress` into a single `typevspec`. The protocol emits one `VSPECFLAG` item per document, with a nested `putitemset` for its vspans. From the client's point of view, the endset is one spec (with document identity) that happens to reference a list of spans — not multiple separate endsets.

The semantic model is: *a single endpoint = one (docisa, vspanset) pair*. Non-contiguous storage fragments are an implementation detail of how the permutation matrix crums are laid out; they collapse back to a single vspec at retrieval time, carrying the full disjoint vspan list inside it.
