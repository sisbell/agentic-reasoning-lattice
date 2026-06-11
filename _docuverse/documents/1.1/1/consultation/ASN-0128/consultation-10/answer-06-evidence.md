## Question 6 [evidence]

> Does udanax-green preserve any global, cross-document ordering of link/event creation (a system-wide counter, log order, or granfilade structure recoverable at query time), or is arrival order recoverable only within a single document's link chain?

## KB Synthesis

## Cross-Document Creation Ordering in udanax-green

**Short answer: No.** There is no system-wide counter, log, or globally accessible granfilade structure from which cross-document arrival order can be recovered at query time. Ordering is only recoverable within a single document's address subspace.

---

### What the allocation mechanism IS

The granfilade is a single global tree [SS-DUAL-ENFILADE], and all allocations use a stateless query-and-increment mechanism [SS-ADDRESS-SPACE, Finding 0061]: `next_addr = findpreviousisagr(tree, bound) + 1`. This operates on the shared tree every time. In that narrow sense, there is one "counter" — but it is implicitly encoded in the tree state, not stored explicitly.

The critical constraint is that **bounds are per-namespace**. The allocator scopes every search to a parent prefix:

- Text content I-addresses for document D are allocated under `D.3.x` [SS-ADDRESS-SPACE Finding 0077]
- Link orgl I-addresses for document D are allocated under `D.2.x` [SS-ADDRESS-SPACE Finding 0065]
- Document addresses are allocated under the owning account [ST-ADDRESS-ALLOC]

So two concurrent `INSERT` operations on documents D1 and D2 each call `findpreviousisagr` with different upper bounds (`D1.3.x` vs `D2.3.x`), increment independently within those ranges, and produce I-addresses that are numerically incomparable — they live in disjoint tumbler subtrees with no shared ordering.

---

### What INV-MONOTONIC actually covers

[INV-MONOTONIC] holds within each per-document namespace: `time(alloc_a) < time(alloc_b) ∧ same_namespace(a, b) ⟹ iaddr(b) > iaddr(a)`. This lets you reconstruct insertion chronology for text within D1, or for links within D1, but not across D1 and D2.

Finding 0063 shows the only cross-entity interaction: CREATELINK for document D allocates a link orgl that advances the content-range counter *for that same document*, so a subsequent INSERT in D gets a higher I-address. But this interaction is still scoped to one document — it says nothing about events in a different document.

---

### The event loop provides ordering but leaves no trace

[INV-SEQUENTIAL-DISPATCH, INV-ATOMICITY] confirm that the `bed.c` event loop processes all requests in strict serialization order. A total execution order exists. But this order is **not recorded in any persistent data structure**. The granfilade tree shape does reflect insertion order in terms of sibling placement (new crums always adopt as RIGHTBRO [SS-DUAL-ENFILADE Finding 0041]), but [INV-ENFILADE-CONFLUENCE] explicitly states that different insertion orderings produce the same logical query results — the tree structure is not a stable ordering artifact.

---

### No timestamps, no journal

There is no wall-clock timestamp, sequence number, or write-ahead log anywhere in the system [SS-UNIFIED-STORAGE, SS-DURABILITY-BOUNDARY]. Durability is session-level via `writeenfilades()` at daemon shutdown [SS-DURABILITY-BOUNDARY], with no per-operation journal.

---

### Summary

| Scope | Ordering recoverable? | Mechanism |
|---|---|---|
| Text insertions within document D | Yes | I-address order within `D.3.x` |
| Links within document D | Yes | I-address order within `D.2.x` |
| Documents under same account | Yes | Child address order under `account.0.x` |
| Text in D1 vs text in D2 | **No** | Separate namespaces, no shared counter |
| Link in D1 vs link in D2 | **No** | Separate namespaces, no shared counter |
| Any event vs any other event globally | **No** | No timestamp, log, or recoverable total order |

The relevant entries: [INV-MONOTONIC], [SS-ADDRESS-SPACE Findings 0065, 0077], [ST-ADDRESS-ALLOC], [INV-ATOMICITY], [INV-SEQUENTIAL-DISPATCH], [INV-ENFILADE-CONFLUENCE], [SS-DURABILITY-BOUNDARY].

---

## Code Exploration

I now have everything needed to answer comprehensively. Here is the full analysis:

---

## Global Cross-Document Link Ordering in udanax-green

**Short answer: No. Arrival order is recoverable only within a single document's link chain.** There is no system-wide counter, no queryable creation log, and no granfilade traversal that yields creation-time order across different documents.

---

## The Two Global Structures

The backend has exactly two shared, persistent structures, initialized in `entexit.c:42-45`:

```c
granf = (typegranf) createenf (GRAN);
spanf = (typespanf) createenf (SPAN);
```

`granf` is the granfilade (the document/content/link address space). `spanf` is the spanfilade (the cross-document link index by content). Neither encodes global creation order, as shown below.

---

## How a Link Gets Its Addresses

`docreatelink` in `do1.c:195-221` runs this sequence:

```c
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
return (
     createorglingranf (taskptr, granf, &hint, linkisaptr)   // 1. assign ISA
  && tumbler2spanset (taskptr, linkisaptr, &ispanset)
  && findnextlinkvsa (taskptr, docisaptr, &linkvsa)           // 2. assign V-position in host doc
  && docopy (taskptr, docisaptr, &linkvsa, ispanset)          // 3. write link ref into host doc orgl
  && findorgl (taskptr, granf, linkisaptr, &link,NOBERTREQUIRED)
  ...
  && insertendsetsinspanf (taskptr, spanf, linkisaptr, ...)   // 4. write into global spanf
);
```

Every assignment is either scoped to the host document or indexed by content — not by global time.

---

## Step 1: ISA Assignment Is Per-Document

`createorglingranf` → `createorglgr` → `findisatoinsertgr` → `findisatoinsertmolecule` [`granf2.c:158-181`]:

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
    ...
    } else if (hintptr->atomtype == LINKATOM) {
        tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);
        if (tumblercmp (&lowerbound, isaptr) == LESS)
            tumblerincrement (isaptr, 1, 1, isaptr);
        else
            tumblerincrement (&lowerbound , 0, 1, isaptr);
    }
```

`hintptr->hintisa` is `docisaptr` (set by `makehint` at `do1.c:207`). The upper bound is `docisa.0.0.3` (LINKATOM+1=3). The search is bounded entirely within the document's ISA subtree in the granfilade. The first link under document D gets `D.0.2.1`, the second gets `D.0.2.2`, etc.

**There is no global counter.** The granfilade tree is searched only within the namespace of the one document being linked to. A link created in document B cannot affect or observe the counter for document A.

---

## Step 2: V-Address in Host Document Is Also Per-Document

`findnextlinkvsa` [`do2.c:151-167`]:

```c
bool findnextlinkvsa(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr)
{
  tumbler vspanreach, firstlink;
  typevspan vspan;
    tumblerclear (&firstlink);
    tumblerincrement (&firstlink, 0, 2, &firstlink);   // 2
    tumblerincrement (&firstlink, 1, 1, &firstlink);   // 2.1

    (void) doretrievedocvspan (taskptr, docisaptr, &vspan);
    tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
    if (tumblercmp (&vspanreach, &firstlink) == LESS)
        movetumbler (&firstlink, vsaptr);             // use 2.1 (first link slot)
    else
        movetumbler (&vspanreach, vsaptr);            // use end of existing content
    return (TRUE);
}
```

`2.1` is the start of link-space in a document's V-stream (`linkspacevstart` is also built as `2` in `findvsatoappend` at `orglinks.c:37`). Each new link is appended to the end of the host document's current V-span reach. This is purely per-document state.

---

## Step 3: The Spanfilade Is Indexed by Content, Not Time

`insertendsetsinspanf` [`do2.c:116-128`] calls `insertspanf` three times (from/to/three). `insertspanf` [`spanf1.c:15-54`]:

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
...
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
```

The ORGLRANGE coordinate is `spantype.linkISA` (e.g., `LINKFROMSPAN.docA.0.2.1`). The SPANRANGE coordinate is the I-span (permascroll content address). The spanfilade is a 2D enfilade indexed by `(I-span, spantype.linkISA)`. This enables the cross-document query "which links point from/to this content?" — but there is no time axis and no creation-order axis. The `sporglset2linkset` function [`spanf1.c:77-93`] retrieves links by content overlap, not by creation sequence.

---

## Step 4: No System-Wide Counter or Log

`be.c:59-61` reveals the entire logging setup:

```c
febelog = interfaceinput = reallog = logfile = nulllog = fopen ("/dev/null", "a");
clock = time (0);
local = localtime (&clock);
sprintf(buf,"ln%d.%d.%d:%d", ...);
```

The `clock` call is used only to name the debug log file. All log file descriptors are opened to `/dev/null`. There is no persistent event log, no sequence number table, no global monotonic counter written at link creation time.

The BERT table (`bert.c:13-29`) is a transient in-memory hash keyed by tumbler, tracking open documents per connection. It is not a creation-event record and is rebuilt from scratch each process start.

---

## What Is Recoverable Within a Single Document

Within one document, link creation order is recoverable by two correlated structures:

1. **V-stream order**: The host document's POOM orgl stores each link's ISA at its V-position in link-space (V ≥ 2.1). Since `findnextlinkvsa` always appends, traversing the document's V-span from 2.1 upward yields links in creation order.

2. **ISA sequence**: Links under document D get ISAs `D.0.2.1`, `D.0.2.2`, … These are monotonically increasing within the document's granfilade subtree, so ISA order equals creation order within one document.

---

## Summary

| Ordering question | Answer |
|---|---|
| Within one document's link chain | Recoverable: V-address in link-space (V ≥ 2.1) is creation-sequential; ISA sequence is also monotone |
| Across different documents | **Not recoverable**: ISAs are namespaced under each document; the granfilade is organized by address, not time |
| System-wide counter | Does not exist |
| Global event log | Does not exist; all log FDs go to `/dev/null` |
| Granfilade traversal gives global order | No: document A's links (`A.0.2.*`) and document B's links (`B.0.2.*`) live in separate subtrees with no temporal cross-reference |
| Spanfilade gives creation order | No: indexed by I-span (content), not by creation time |

The design is a pure address space: every object's position in the granfilade encodes *what it is and who owns it*, not *when it was created*. Cross-document link ordering was simply not an architectural goal of udanax-green's data model.
