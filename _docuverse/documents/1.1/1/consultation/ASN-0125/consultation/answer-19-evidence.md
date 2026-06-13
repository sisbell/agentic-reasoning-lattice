## Question 19 [evidence]

> Is the type namespace at `1.0.2.x` extensible at runtime — could a client register a "supersedes" link type there without backend changes — and does the backend ever interpret a type endset's content, or is the type purely an opaque I-span that only conventions among clients give meaning to?

## KB Synthesis

Two distinct questions; they have clean answers from the KB.

---

## 1. Runtime extensibility of `1.0.2.x`

**Yes, structurally extensible — but subject to BERT write access on the bootstrap document.**

The type endset of a link is stored as an ordinary VSpec referencing content in the bootstrap document (doc 1) at the `1.0.2.x` address range [SS-LINK-ENDPOINT, Finding 0024]. Nothing in the storage layer distinguishes this content from any other permascroll content. Adding a new type like "supersedes" at `1.0.2.7` would require:

1. Opening the bootstrap document with WRITEBERT access.
2. INSERT-ing content there (or placing a VSpec reference there).
3. Using the resulting I-addresses as the "three" (type) endset when calling `create_link`.

However, the backend enforces no constraint that a type endset must point into `1.0.2.x` at all. Because the type position is an opaque I-span (see below), a client can supply any content I-addresses — from their own documents, from any permascroll location — as the type. The `1.0.2.x` registry is a client-side convention, not a backend enforcement boundary. A "supersedes" type created in a client's own document would be indistinguishable to the backend from a type registered in the bootstrap document.

The only practical constraint is whether the bootstrap document is writable. The KB does not document any special protection on doc 1 beyond the ordinary BERT access control machinery [PRE-OPEN-DOC, SS-BERT]. Since BERT is cooperative, not enforced [INT-BERT-FEBE], a compliant client with appropriate BERT tokens could extend `1.0.2.x`; a non-compliant client could create types anywhere.

---

## 2. Backend interpretation of the type endset

**Never. The type endset is entirely opaque to the backend.**

The "three" position in a link orgl is stored and indexed identically to the "from" and "to" positions. Concretely [INT-SPORGL-LINK-INDEX, Finding 0035]:

- All three endsets are stored as I-spans (sporgls) in the spanfilade under different ORGLRANGE tags: `LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3`.
- Retrieval via RETRIEVEENDSETS treats all three symmetrically — no special path exists for the type dimension.
- The backend never dereferences the type I-addresses to read their content or interpret their meaning.

The most direct evidence is [EC-TYPE-FILTER-NONFUNCTIONAL]: type-based `find_links` filtering returns empty results even when unfiltered search finds links of those exact types. If the backend had any semantic awareness of type content, this path would work. Its failure confirms the backend has no investment in type semantics whatsoever.

The KB states it explicitly [SS-LINK-ENDPOINT, Finding 0024]: "Link types are content references, not metadata — they participate in the same address/identity system as all other content." The type hierarchy encoded by tumbler containment (`1.0.2.6.2` inside `1.0.2.6`) is meaningful only to clients doing address-range matching on the type endset — the backend sees it as bytes at I-addresses, nothing more.

---

**In short:** The type system is a pure convention among clients. The backend stores, indexes, and returns the type endset as an opaque I-span. A client can register new types anywhere in the address space — including outside `1.0.2.x` — without any backend changes, as long as it can satisfy the BERT protocol for writing to wherever it chooses to anchor those types.

---

## Code Exploration

I now have a complete picture of the code. Here is the full answer.

---

## Is `1.0.2.x` Extensible at Runtime? Does the Backend Interpret the Type Endset?

### What `1.0.2.x` Is

`1.0.2.x` is a **V-space address convention inside the bootstrap document**, defined entirely in the Python client. From `febe/client.py:597-608`:

```python
# Link type addresses - types are in document 1's link subspace (0.2)
# Full address format: 1.1.0.1.0.1.0.2.X where X is the type number
LINK_TYPES_DOC = Address(1, 1, 0, 1, 0, 1)  # Document 1 (bootstrap doc)

# Local address within doc: version.0.link_subspace.type = 1.0.2.X
JUMP_TYPE     = VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 2),    Offset(0, 1))])
QUOTE_TYPE    = VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 3),    Offset(0, 1))])
FOOTNOTE_TYPE = VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 6),    Offset(0, 1))])
MARGIN_TYPE   = VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 6, 2), Offset(0, 1))])
```

There is no corresponding constant, enumeration, lookup table, or registry anywhere in the C backend. No `.h` or `.c` file references these V-address values. The `1.0.2.x` namespace exists only in client-layer convention.

---

### The Backend Has No Concept of Link Types

`xanadu.h:35-39` defines the only type-adjacent constants in the backend:

```c
/* spanfilade span types */
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```

These are **slot discriminators** — numeric prefixes prepended to the ORGLRANGE dimension of spanfilade crums so the three endsets can be stored and retrieved independently. They say nothing about what values the type endset (slot 3) is allowed to contain.

---

### The Type Endset Is Treated Identically to From/To at Every Layer

**Creation — `docreatelink` [`do1.c:195-221`]:**

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr,
    typespecset fromspecset, typespecset tospecset, typespecset threespecset,
    typeisa *linkisaptr)
{
    ...
    && specset2sporglset (taskptr, fromspecset,   &fromsporglset, NOBERTREQUIRED)
    && specset2sporglset (taskptr, tospecset,     &tosporglset,   NOBERTREQUIRED)
    && specset2sporglset (taskptr, threespecset,  &threesporglset,NOBERTREQUIRED)
    && setlinkvsas (&fromvsa, &tovsa, &threevsa)
    && insertendsetsinorgl (taskptr, linkisaptr, link,
           &fromvsa, fromsporglset, &tovsa, tosporglset, &threevsa, threesporglset)
    && insertendsetsinspanf (taskptr, spanf, linkisaptr,
           fromsporglset, tosporglset, threesporglset)
```

All three specsets go through exactly the same `specset2sporglset` call with `NOBERTREQUIRED`. There is no validity check on what the type specset points to.

**V-space slot assignment — `setlinkvsas` [`do2.c:169-183`]:**

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
    tumblerclear(fromvsaptr);
    tumblerincrement(fromvsaptr, 0, 1, fromvsaptr);   // 1.x
    tumblerincrement(fromvsaptr, 1, 1, fromvsaptr);   // 1.1
    tumblerclear(tovsaptr);
    tumblerincrement(tovsaptr, 0, 2, tovsaptr);       // 2.x
    tumblerincrement(tovsaptr, 1, 1, tovsaptr);       // 2.1
    if (threevsaptr) {
        tumblerclear(threevsaptr);
        tumblerincrement(threevsaptr, 0, 3, threevsaptr);  // 3.x
        tumblerincrement(threevsaptr, 1, 1, threevsaptr);  // 3.1
    }
```

The type endset's I-addresses are stored at V-position `3.1` within the link orgl — just another positional slot, carrying no semantic weight.

**Spanfilade insertion — `insertendsetsinspanf` [`do2.c:116-128`]:**

```c
bool insertendsetsinspanf(...)
{
    if (!(insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
        && insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN)))
            return (FALSE);
    if (threesporglset) {
        if (!insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN))
                return (FALSE);
    }
```

The type endset goes into the spanfilade under key `LINKTHREESPAN = 3`. `insertspanf` [`spanf1.c:15-54`] prepends this integer as a tumbler prefix (`prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE])`) and inserts the crum. No content inspection occurs.

**Link search — `findlinksfromtothreesp` [`spanf1.c:56-103`]:**

```c
if (threevspecset)
    specset2sporglset(taskptr, threevspecset, &threesporglset, NOBERTREQUIRED);
...
if (threevspecset) {
    sporglset2linkset(taskptr, (typecuc*)spanfptr, threesporglset,
                      &threelinkset, orglrange, LINKTHREESPAN);
```

When you call `find_links(..., typespecs=JUMP_TYPE)`, the backend converts your type specset to I-spans and does an address-overlap search in the LINKTHREESPAN slot of the spanfilade. The actual text content at those I-addresses is never fetched. Type filtering is purely I-address intersection, not content inspection.

**Follow — `dofollowlink` [`do1.c:223-231`] and `link2sporglset` [`sporgl.c:67-95`]:**

```c
bool link2sporglset(..., INT whichend, ...)
{
    tumblerincrement(&zero, 0, whichend, &vspan.stream);   // whichend = 1, 2, or 3
    tumblerincrement(&zero, 0, 1, &vspan.width);
    if (context = retrieverestricted((typecuc*)orgl, &vspan, V, NULL, I, NULL)) {
        for (c = context; c; c = c->nextcontext) {
            contextintosporgl((type2dcontext*)c, NULL, sporglptr, I);
```

Following the type endset (`whichend = LINK_TYPE = 3`) is identical to following from or to. The orgl is queried at V-position 3, the result is returned as opaque I-spans. The backend never reads what is stored at those addresses.

**Endset retrieval — `retrieveendsetsfromspanf` [`spanf1.c:190-235`]:**

```c
fromspace.stream.mantissa[0]  = LINKFROMSPAN;   // 1
tospace.stream.mantissa[0]    = LINKTOSPAN;     // 2
threespace.stream.mantissa[0] = LINKTHREESPAN;  // 3
...
retrievesporglsetinrange(taskptr, sporglset, &threespace, &threesporglset)
&& linksporglset2specset(taskptr, ..., threesporglset, threesetptr, NOBERTREQUIRED)
```

Three endsets retrieved symmetrically from three spanfilade slots. The type endset is returned as-is.

---

### Extensibility: Yes, Without Backend Changes

The `1.0.2.x` namespace is extensible at runtime because:

1. **The backend enforces no type whitelist.** `specset2sporglset` [`sporgl.c:14-33`] accepts any `VSPECID` or `ISPANID` specset and converts it to I-addresses. There is no check against known type values.

2. **Type lookup is I-address intersection.** When searching by type, `sporglset2linksetinrange` [`sporgl.c:239-269`] calls `retrieverestricted` on the spanfilade with the given sporglset as the SPANRANGE restriction. A "supersedes" type's I-addresses would be found and intersected just as JUMP_TYPE's are.

3. **The type endset's content is never fetched or decoded.** Neither `insertspanf`, `sporglset2linkset`, `link2sporglset`, nor `retrieveendsetsfromspanf` ever call `inserttextingranf` or any read of the actual stored characters.

A client wanting to register "supersedes" needs only to:
- Pick a V-address in any accessible document, e.g. `Address(1, 0, 2, 10)` in `LINK_TYPES_DOC`
- Build `SUPERSEDES_TYPE = VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 10), Offset(0, 1))])`
- Use it as the `typespecs` argument to `create_link`

The backend stores the corresponding I-address in the LINKTHREESPAN slot and indexes it in the spanfilade. `find_links(typespecs=SUPERSEDES_TYPE)` will correctly find those links. The content at that V-address need not even exist for the type matching to work — the backend only looks at I-addresses, not the content they denote.

**The one runtime constraint:** All clients using the new type must agree on the same I-addresses. If `1.0.2.10` in `LINK_TYPES_DOC` was never written, it has no permanent I-address yet, and two clients that independently insert content at that V-address will get different I-addresses. Coordination on the bootstrap document's content is the client-layer convention that gives `1.0.2.x` its meaning — the backend is silent on all of this.

---

### Summary

| Question | Answer | Key evidence |
|----------|--------|-------------|
| Is `1.0.2.x` defined in the backend? | No | No C file references these V-addresses |
| Is the type endset validated against known types? | No | `specset2sporglset` [`sporgl.c:14`] accepts any specset; `docreatelink` [`do1.c:214-216`] treats it identically to from/to |
| Does type filtering read content? | No | `sporglset2linkset` [`sporgl.c:222`] does pure I-address intersection via `retrieverestricted` |
| Can a client add a new type without backend changes? | Yes | Any V-span in any open document is a valid type endset; the backend stores and indexes it as opaque I-addresses |
| Is the type an opaque I-span? | Yes | Every path — create, follow, retrieve endsets, find links — treats the type slot identically to the from and to slots; content is never read |
