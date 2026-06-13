## Question 16 [evidence]

> When the queried vspec-set covers a single contiguous V-span that maps to non-contiguous I-addresses (e.g., due to a CREATELINK allocation gap), does `vspanset2sporglset` split it into multiple sporgls, and is the result the union of documents matching ANY fragment or only those matching ALL fragments?

## KB Synthesis

**Yes, it splits. The result uses ANY-fragment (union) semantics.**

## Splitting behavior

When `vspanset2sporglset` processes a V-span that maps to non-contiguous I-addresses, it produces one sporgl per contiguous I-address region. The mechanism is:

1. `vspanset2ispanset` calls `permute` → `span2spanset` → `retrieverestricted`, which walks the POOM B-tree over the requested V-range and accumulates every context entry that falls within it [SS-POOM-MULTIMAP]. If the POOM has two crums covering the same V-range but mapping to non-contiguous I-address regions (as happens after INSERT "ABC" → CREATELINK → INSERT "DEF" per [INT-LINK-INSERT]), both crums are returned as separate context entries.

2. `vspanset2sporglset` then iterates over every `typeispan` in the returned ispanset via its inner loop (`sporgl.c:49-58`) and creates a separate sporgl for each [ST-LINK-CREATE, Finding 0037]. The front end provides one V-span; the backend emits N sporgls, one per contiguous I-region.

The CREATELINK gap case is a direct instance of this: text inserted before and after a `createorglingranf` call ends up in two separate I-address ranges (e.g., `I.1–I.3` and `I.2.1–I.2.4`), but a V-span covering both is entirely contiguous in V-space. `vspanset2ispanset` faithfully discovers both POOM crums, and `vspanset2sporglset` emits two sporgls [INV-MONOTONIC, Finding 0063].

## Downstream matching semantics: ANY-fragment (union)

All downstream operations that consume the resulting sporglset use non-empty intersection — i.e., a result is included if it matches **any** fragment, not all:

**`find_links`:** The precondition for a link to appear is `I-addresses(query) ∩ I-addresses(link.endpoint) ≠ ∅` [SS-FIND-LINKS, Finding 0028]. Each sporgl's I-address range is searched against the spanfilade independently via `retrievesporglsetinrange`, and results are accumulated. A link whose endpoint overlaps with fragment 1 (e.g., "ABC") but not fragment 2 (e.g., "DEF") will still be returned.

**`find_documents` / DOCISPAN:** The spanfilade is queried per I-span; any document indexed for any of the I-address fragments is returned [SS-DOCISPAN, Finding 0047]. There is no "AND across all fragments" gate — `insertspanf` creates independent entries per I-span, and `finddocscontainingsp` returns the union of matching documents.

**`retrieve_endsets`:** The same call chain applies: specset → sporglset → `retrievesporglsetinrange` per I-span [SS-RETRIEVE-ENDSETS, Finding 0035]. Results from all I-spans are unioned.

## Summary

A single contiguous V-span over a CREATELINK-gapped document becomes N sporgls (one per POOM crum within the V-range). All subsequent spanfilade-based operations treat these N sporgls independently and accumulate results — a document or link matching any one fragment is included in the output. This is the standard content-identity intersection model: `result ⊇ ∅` iff any I-address in the query matches, not all.

---

## Code Exploration

I have the full picture. Here is the complete answer.

---

## Answer: `vspanset2sporglset` — Splitting and Semantics

### 1. Does it split? Yes, unconditionally.

`vspanset2sporglset` is defined in `backend/sporgl.c:35`. The splitting happens in its inner loop:

```c
// sporgl.c:47-58
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);
    for (; ispanset; ispanset = ispanset->next) {
           sporglset = (typesporgl *) taskalloc (taskptr, sizeof(typesporgl));
           sporglset->itemid = SPORGLID;
           sporglset->next = NULL;
           movetumbler (docisa, &sporglset->sporgladdress);
           movetumbler(&ispanset->stream,&sporglset->sporglorigin);
           movetumbler (&ispanset->width, &sporglset->sporglwidth);
           *sporglsetptr = (typesporglset)sporglset;
           sporglsetptr = (typesporglset *)&sporglset->next;
    }
}
```

**`vspanset2ispanset`** (`orglinks.c:397`) calls `permute(taskptr, orgl, vspanptr, V, ispansetptr, I)` (`orglinks.c:401`), which calls `span2spanset` (`orglinks.c:425`) for each V-span. `span2spanset` calls `retrieverestricted` on the granfilade and collects every I-region that intersects the V-span (via `context2span` + `onitemlist`).

If a single contiguous V-span was allocated across two non-contiguous I-regions (e.g., because a `CREATELINK` consumed I-space in between), `retrieverestricted` returns two context entries, and `permute` appends two `typeispan` nodes to `ispanset`.

The inner loop at `sporgl.c:49` then creates **one `typesporgl` per ispan** — so a V-span that maps to N non-contiguous I-fragments produces N sporgls in the output list. The comment at `sporgl.c:60-63` confirms the return value is the pointer to the last allocated sporgl's `next` field, for linked-list chaining.

---

### 2. Union or intersection? **Union (ANY fragment)**, within a single endpoint.

The sporglset flows into `sporglset2linkset` → `sporglset2linksetinrange` (`sporgl.c:222–269`):

```c
// sporgl.c:250-268
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    // ...
    context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, ...);
    for (c = context; c; c = c->nextcontext) {
        beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
        onlinklist(taskptr, linksetptr, &linksa);   // ← union accumulation
    }
    contextfree(context);
}
```

`onlinklist` (`spanf2.c:26-43`) appends a link to the list and only skips it if it is already present (dedup), never intersects:

```c
// spanf2.c:38-43
for (temp = *linksetptr; nextlink = temp->next; temp = nextlink) {
    if (tumblereq(&temp->address, linkisaptr))
        return(0);   // deduplicate only
}
temp->next = linkset;
```

So every link touching **any** I-fragment of the sporglset is collected into the endpoint's linkset. The semantics are **union: a link is included if it touches ANY fragment**.

---

### 3. The `intersectlinksets` intersection is across endpoints, not across fragments.

In `findlinksfromtothreesp` (`spanf1.c:56`):

```c
// spanf1.c:70-100
if (fromvspecset)
    specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
if (tovspecset)
    specset2sporglset(taskptr, tovspecset, &tosporglset, NOBERTREQUIRED);
if (threevspecset)
    specset2sporglset(taskptr, threevspecset, &threesporglset, NOBERTREQUIRED);
if (fromvspecset) {
    sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
    if (!fromlinkset) { *linksetptr = NULL; return(TRUE); }   // early exit, not AND
}
if (tovspecset) {
    sporglset2linkset(taskptr, (typecuc*)spanfptr, tosporglset, &tolinkset, orglrange, LINKTOSPAN);
    ...
}
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);  // spanf1.c:100
```

`intersectlinksets` (`spanf2.c:46`) intersects **across** the FROM, TO, and THREE endpoint linksets — i.e., a link must appear in all non-null endpoint lists. But each individual endpoint linkset was already built as a union over all I-fragments from `sporglset2linksetinrange`.

---

### 4. `finddocscontaining` does not use `vspanset2sporglset` at all.

`dofinddocscontaining` (`do1.c:15`) calls `specset2ispanset` (`do2.c:14`) — which goes through `vspanset2ispanset` → `permute` directly, without the sporgl layer — and then calls `finddocscontainingsp` (`spanf1.c:151`):

```c
// spanf1.c:170-182
for (; ispanset; ispanset = ispanset->next) {
    context = retrieverestricted((typecuc*)spanf, &docspace, ORGLRANGE, ispanset, SPANRANGE, ...);
    for (c = context; c; c = c->nextcontext) {
        movetumbler(&c->totaloffset.dsas[ORGLRANGE], &docid);
        beheadtumbler(&docid, &document.address);
        if (isinlinklist(*headptr, &document.address))
            continue;                    // dedup only
        addresssetptr = (typelinkset *)onitemlist(taskptr, ...);
    }
    contextfree(context);
}
```

Again, strictly additive (union). A document is included if the spanfilade reports it contains **any** ispan fragment.

---

### Summary

| Behavior | Answer | Key Code |
|---|---|---|
| Does `vspanset2sporglset` split one V-span into multiple sporgls when it maps to non-contiguous I-addresses? | **Yes** — one sporgl per I-span fragment | `sporgl.c:49-58` |
| How are fragments from the same endpoint combined? | **Union (ANY)** — `onlinklist` appends, never intersects | `sporgl.c:264`, `spanf2.c:38-43` |
| Where is intersection performed? | **Across endpoints** (FROM ∩ TO ∩ THREE) only | `spanf1.c:100`, `spanf2.c:46-120` |
| Does `finddocscontaining` use `vspanset2sporglset`? | **No** — uses `specset2ispanset` directly; result is also union | `do1.c:21`, `spanf1.c:170-182` |

The result of querying a V-span that maps to two non-contiguous I-fragments is always the **union**: all documents (or links) touching **any** fragment are returned. There is no ALL/intersection across I-fragments within a single endpoint or query span.
