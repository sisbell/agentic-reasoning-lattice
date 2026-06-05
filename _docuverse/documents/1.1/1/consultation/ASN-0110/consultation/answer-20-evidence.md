## Question 20 [evidence]

> What invariant guarantees the returned endsets reference content by I-address identity, so the result is stable under INSERT/DELETE/REARRANGE shifts of the V-positions used to phrase the query?

## KB Synthesis

The stability guarantee rests on four interlocking invariants across three architectural layers.

## The Core Invariant Chain

**Links store I-addresses, not V-addresses, as their durable anchor.**

When `domakelink` creates a link, the caller's V-spans are immediately converted to I-addresses via `vspanset2sporglset` → `vspanset2ispanset` → `permute`. The resulting I-addresses are stored permanently in the link orgl in I-space [SS-THREE-LAYER-MODEL, ST-LINK-CREATE]. The link orgl is never modified after creation — it is in the permanent, append-only I-space layer.

**INV-IADDR-IMMUTABILITY** [Finding 0030, 0064] then guarantees: I-addresses, once allocated, never change. INSERT allocates *fresh* addresses; it never reassigns existing ones. DELETE frees POOM entries but leaves I-space untouched. So the I-addresses stored in the link orgl at creation time are the same I-addresses that will be there when the endset is later retrieved.

**INSERT, DELETE, and REARRANGE are all frame-condition-preserving with respect to I-space:**

- INSERT [FC-INSERT-IADDR]: Does not modify any pre-existing content's I-address. V-positions shift, I-addresses do not.
- DELETE [ST-DELETE, Finding 0064]: Operates exclusively on the POOM (V→I mappings). The granfilade — where I-addresses live — is append-only; `deletevspanpm` has no code path touching it.
- REARRANGE [INV-REARRANGE-IDENTITY]: Modifies only `cdsp.dsas[V]` (V-dimension displacement). I-addresses are never touched.

**Endset retrieval is dynamic V-address resolution from stable I-addresses.**

FOLLOWLINK and RETRIEVEENDSETS both use the same two-phase path [SS-FOLLOWLINK, Finding 0048]: (1) read the permanent I-addresses from the link orgl via `link2sporglset` → `retrieverestricted` on I-space, then (2) resolve those I-addresses to *current* V-positions by querying the queried document's current POOM via `linksporglset2specset` → `span2spanset`. Phase 1 is pure I-space lookup — immutable. Phase 2 is a live POOM query that reflects all edits that have occurred.

**INV-ITOV-FILTERING** [Finding 0048] closes the loop: if a link's endset I-address has no current POOM mapping (because content was deleted), `retrieverestricted` returns NULL and that I-address is silently dropped. The result is exactly "surviving content that was originally linked" — [INV-LINK-CONTENT-TRACKING, Finding 0019] states this explicitly as the central invariant.

## Summary

The endset returned under V-position shifts is stable because:

1. The endset's durable form is a set of I-addresses in the permanent link orgl [SS-THREE-LAYER-MODEL]
2. No operation modifies existing I-addresses [INV-IADDR-IMMUTABILITY]
3. INSERT/DELETE/REARRANGE are all frame-condition-preserving on I-space [FC-INSERT-IADDR, ST-DELETE Finding 0064, INV-REARRANGE-IDENTITY]
4. Retrieval dynamically re-derives V-positions from those stable I-addresses against the current POOM [SS-FOLLOWLINK]
5. Unreachable I-addresses (deleted content) are filtered at query time rather than corrupting the stored endset [INV-ITOV-FILTERING]

The V-addresses in a returned endset will shift after an INSERT before the linked region — but they shift because the POOM shifted, not because the endset changed. The *identity* of what the endset refers to (which bytes in the permascroll) is invariant.

---

## Code Exploration

Now I have the actual line numbers verified. Here is the complete answer.

---

## The Endset I-Address Stability Invariant

The invariant is established at a single chokepoint in `sporgl.c` and enforced throughout the entire storage/retrieval pipeline. The guarantee has two parts: *what gets stored* and *what gets read back*.

---

### Part 1 — Storage: V-spans are atomized into I-spans before the link is written

`docreatelink` [do1.c:214–216] converts each endset specset to a sporglset:

```c
specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
specset2sporglset (taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)
specset2sporglset (taskptr, threespecset,&threesporglset, NOBERTREQUIRED)
```

`specset2sporglset` [sporgl.c:14–33] dispatches to `vspanset2sporglset` for every `VSPECID` item [sporgl.c:25].

**The critical transformation is in `vspanset2sporglset` [sporgl.c:35–65]:**

```c
(void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);  // [sporgl.c:48]
for (; ispanset; ispanset = ispanset->next) {
    sporglset->itemid = SPORGLID;
    movetumbler (docisa, &sporglset->sporgladdress);             // [sporgl.c:53]
    movetumbler (&ispanset->stream, &sporglset->sporglorigin);   // [sporgl.c:54]
    movetumbler (&ispanset->width,  &sporglset->sporglwidth);    // [sporgl.c:55]
```

Line 48 calls `vspanset2ispanset` [orglinks.c:397–401], which calls `permute(..., V, ..., I)` [orglinks.c:401] — querying the source document's permutation matrix in V-space and returning results in I-space. The V-spans the caller gave disappear here. What remains — stored in `sporgladdress`/`sporglorigin`/`sporglwidth` — is the document I-address plus I-coordinate extent. Those are permanent content identifiers, unaffected by subsequent edits to V-positions.

The sporglset is written into the link document's permutation matrix by `insertendsetsinorgl` → `insertpm` [orglinks.c:75–134]. `insertpm` unpacks the sporgl [orglinks.c:101] and explicitly places the I-span into `crumorigin.dsas[I]` [orglinks.c:105] and `crumwidth.dsas[I]` [orglinks.c:109], while placing the intra-link V-position (`fromvsa`/`tovsa`) into `crumorigin.dsas[V]` [orglinks.c:113]. The tree is indexed on V [orglinks.c:130]:

```c
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
```

So the link's internal matrix maps V (which endset slot: from=1, to=2, three=3) → I (what content identity).

---

### Part 2 — Retrieval: the matrix is queried in V then results extracted in I

`dofollowlink` [do1.c:228–231] calls `link2sporglset` then `linksporglset2specset`.

**`link2sporglset` [sporgl.c:67–95]** constructs a V-span for the requested endset slot [sporgl.c:81–82] and queries:

```c
context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL);
// [sporgl.c:83]
```

The two index parameters are the invariant pivot: the restriction axis is `V` (find the crum at this intra-link V-slot), and the target axis is `I` (return the I-coordinate from that crum). This call traverses the link's permutation matrix and returns the stored I-spans.

`contextintosporgl` is then called with `I` [sporgl.c:86]:

```c
contextintosporgl ((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);
```

which reads from `context->totaloffset.dsas[I]` [sporgl.c:211] and `context->contextwid.dsas[I]` [sporgl.c:219], and stores the home-document address from `context->context2dinfo.homedoc` [sporgl.c:209]. The sporgl returned at this point contains only I-coordinates — the source document's V-positions at link-creation time are nowhere in the output.

---

### Part 3 — Final resolution: I-spans translated to current V-spans on demand

`linksporglset2specset` [sporgl.c:97–123] calls `linksporglset2vspec` [sporgl.c:116], which calls `sporglset2vspanset` [sporgl.c:136].

**`sporglset2vspanset` [sporgl.c:141–176]:**

```c
(void) findorgl (taskptr, granf, homedoc, &orgl, type);       // [sporgl.c:152]
movetumbler (&sporglptr->sporglorigin, &ispan.stream);         // [sporgl.c:155]
movetumbler (&sporglptr->sporglwidth,  &ispan.width);          // [sporgl.c:156]
vspansetptr = ispan2vspanset (taskptr, orgl, &ispan, vspansetptr); // [sporgl.c:157]
```

`ispan2vspanset` [orglinks.c:389–393] calls `permute(..., I, ..., V)` [orglinks.c:393], querying the source document's *current* permutation matrix in I-space and returning V-spans. This is the moment INSERT/DELETE/REARRANGE are "absorbed": those operations update V-positions in the source document's permutation matrix, but I-addresses never change. So whatever V-position the content occupies now — after any number of edits — is what the endset resolves to.

A same-document consistency check is embedded in the loop [sporgl.c:163]:

```c
!tumblereq (&sporglptr->sporgladdress,
            &((typesporgl *)(*sporglsetptr))->sporgladdress)
```

This ensures all sporgls in a set point to the same home document before using its permutation matrix.

---

### Summary

The invariant is:

| Step | Location | What happens |
|---|---|---|
| V → I conversion | `vspanset2sporglset` [sporgl.c:48] | V-spans discarded; I-spans computed via `permute(V→I)` |
| I + docisa stored in sporgl | [sporgl.c:53–55] | Content identity frozen at link-creation time |
| I-span written into link matrix | `insertpm` [orglinks.c:105, 109] | Stored in `crumorigin.dsas[I]`, not `dsas[V]` |
| Retrieval extracts I | `retrieverestricted(..., V, ..., I, ...)` [sporgl.c:83] | V-slot lookup, I-result |
| I → V resolution at query time | `ispan2vspanset` via `sporglset2vspanset` [sporgl.c:157] | Current permutation matrix resolves I → present V |

INSERT/DELETE/REARRANGE operate on the source document's V-coordinates [orglinks.c:130, 139, 149]. They leave I-addresses unchanged. Since endsets are stored as I-addresses with a document I-address as home reference, they remain stable across all structural edits. The current V-position of any endset is computed fresh at follow-time from the document's live permutation matrix, never cached.
