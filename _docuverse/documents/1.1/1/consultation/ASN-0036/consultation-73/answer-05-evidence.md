## Question 5 [evidence]

> In udanax-green, does the link subspace populate V-positions contiguously starting at ordinal 1 (like text), or does it use some other allocation pattern (sparse, keyed, addressed by content)?

## KB Synthesis

## Link Subspace V-Position Allocation

Links occupy the `2.x` subspace with **append-only monotonic allocation starting at `2.1`** — structurally similar to text starting at `1.1`, but with an important behavioral difference.

### Allocation Pattern

**First link:** `findnextlinkvsa()` hardcodes the initial position at `2.1` by incrementing the tumbler to `2.0` then `2.1` [SS-LINK-SUBSPACE, Finding 0052; SS-DUAL-ENFILADE, Finding 0009].

**Subsequent links:** Each new link is placed at `vspanreach` — the current end of the document's V-extent in the link subspace — producing sequential positions `2.2`, `2.3`, etc. [SS-LINK-SUBSPACE, Finding 0052].

So the allocation sequence is contiguous: `2.1`, `2.2`, `2.3`, ... mirroring how text occupies `1.1`, `1.2`, `1.3`, ...

### Key Difference from Text

Text insertion can target *any* interior V-position (triggering shifts of subsequent entries). Links are **always appended at the end** — `findnextlinkvsa` always selects `vspanreach`. The result is that link V-positions are never internally inserted, only appended [ST-CREATE-LINK, Finding 0052].

The `3.x` subspace (link type endpoints) follows the same append pattern, starting at `3.1` [SS-SUBSPACE-CONVENTION, Finding 0038].

### Subspace Isolation Preserved

Because links are always appended beyond existing link entries, the two-blade knife mechanism for INSERT (`blade[1] = (N+1).1`) ensures text insertions at `1.x` never shift link entries at `2.x` [FC-SUBSPACE, Finding 0054].

---

## Code Exploration

I now have everything needed. Here is my full answer.

---

## Link Subspace V-Position Allocation in udanax-green

The link subspace uses **two distinct allocation mechanisms** that must be distinguished: (1) how links are placed in a document's V-space, and (2) how a link's endpoints are indexed within the link's own internal structure.

---

### 1. Document V-Space Placement — Contiguous from V=2.1

`findnextlinkvsa` in `do2.c:151–167` determines where the next link is placed in the document's virtual address space:

```c
bool findnextlinkvsa(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr)
{
  tumbler vspanreach, firstlink;
  typevspan vspan;
  bool doretrievedocvspan();
    tumblerclear (&firstlink);
    tumblerincrement (&firstlink, 0, 2, &firstlink);  // mantissa[0] = 2
    tumblerincrement (&firstlink, 1, 1, &firstlink);  // mantissa[1] = 1 → firstlink = 2.1

    (void) doretrievedocvspan (taskptr, docisaptr, &vspan);
    tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
    if (tumblercmp (&vspanreach, &firstlink) == LESS)
        movetumbler (&firstlink, vsaptr);   // No prior links: start at 2.1
    else
        movetumbler (&vspanreach, vsaptr);  // Links exist: append after content end
    return (TRUE);
}
```

`tumblerincrement` (`tumble.c:599–623`) builds tumblers positionally: `rightshift=0, bint=2` sets the integer part to 2; `rightshift=1, bint=1` sets the fractional part to 1. So `firstlink = 2.1` in tumbler notation.

The logic:
- Fetch the current document V-span (stream + width → reach)  
- If reach < 2.1 → place the link at 2.1 (first link ever)  
- Otherwise → place it immediately after the current content end (contiguous append)

This means **links in document V-space are allocated contiguously**, appended one after another, with the floor being V=2.1. Text content lives below that boundary (V ≥ 1.0 and < 2.0 for text).

---

### 2. Link Endpoint Indexing — Fixed Sparse Keys (1.1 / 2.1 / 3.1)

`setlinkvsas` in `do2.c:169–183` assigns the internal V-addresses for each link's three endpoint roles:

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
    tumblerclear (fromvsaptr);
    tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);
    tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);   // fromvsa  = 1.1

    tumblerclear (tovsaptr);
    tumblerincrement (tovsaptr, 0, 2, tovsaptr);
    tumblerincrement (tovsaptr, 1, 1, tovsaptr);       // tovsa    = 2.1

    if (threevsaptr) {
        tumblerclear (threevsaptr);
        tumblerincrement (threevsaptr, 0, 3, threevsaptr);
        tumblerincrement (threevsaptr, 1, 1, threevsaptr); // threevsa = 3.1
    }
    return (TRUE);
}
```

These are **hardcoded, constant keys** — not a counter, not content-derived. Every single link in the system stores its endpoints at:

| Endpoint | Fixed V-Key |
|----------|-------------|
| FROM     | 1.1         |
| TO       | 2.1         |
| THREE    | 3.1         |

These constants are reflected in `backend/xanadu.h:36–38`:

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
```

They are used when inserting into the spanfilade (`do2.c:119–120`, `spanf1.c:210–217`) and when retrieving endpoint sets from the spanfilade:

```c
// do2.c:119–120
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
  && insertspanf(taskptr, spanfptr, linkisaptr, tosporglset, LINKTOSPAN)

// spanf1.c:210–217
fromspace.stream.mantissa[0] = LINKFROMSPAN;   // key = 1
fromspace.width.mantissa[0] = 1;
tospace.stream.mantissa[0] = LINKTOSPAN;       // key = 2
tospace.width.mantissa[0] = 1;
threespace.stream.mantissa[0] = LINKTHREESPAN; // key = 3
threespace.width.mantissa[0] = 1;
```

---

### 3. How `islinkcrum` Identifies Link Crums

`orglinks.c:255–261` reveals the V-space boundary that separates link crums from text crums in the enfilade:

```c
bool islinkcrum(typecorecrum *crumptr)
{
    if(crumptr->cdsp.dsas[V].mantissa[0] == 1
       && crumptr->cdsp.dsas[V].mantissa[1] != 0)
        return TRUE;   /* 1.n tumbler where n ≠ 0 → link crum */
    return FALSE;
}
```

A crum displaced by a `1.n` V-address (n ≠ 0) is a link crum. This is the internal granfilade representation: the "1" in `1.n` corresponds to the FROM endpoint zone (LINKFROMSPAN = 1). This is consistent with `setlinkvsas` assigning 1.1 to FROM endpoints.

---

### 4. The Execution Path

In `docreatelink` (`do1.c:195–221`):

```c
createorglingranf (taskptr, granf, &hint, linkisaptr)   // allocate link I-address
&& tumbler2spanset (taskptr, linkisaptr, &ispanset)
&& findnextlinkvsa (taskptr, docisaptr, &linkvsa)        // compute V=2.1 or later
&& docopy (taskptr, docisaptr, &linkvsa, ispanset)       // insert link's I-addr at that V
&& findorgl (taskptr, granf, linkisaptr, &link, ...)
&& specset2sporglset (...)                               // resolve endpoint specsets
&& setlinkvsas (&fromvsa, &tovsa, &threevsa)            // hardcode 1.1, 2.1, 3.1
&& insertendsetsinorgl (...)                             // store in orglink poom
&& insertendsetsinspanf (...)                            // store in spanfilade by key
```

There is also a two-endpoint variant `domakelink` (`do1.c:169–193`) that calls `setlinkvsas(..., NULL)` — skipping the THREE endpoint.

---

### Answer

The link subspace uses **neither** pure contiguous-ordinal allocation nor pure content-keyed addressing. It uses a **two-layer scheme**:

- **Document V-space** (where links sit as content): **Contiguous** append, floor at V=2.1. This is structurally similar to text (which also occupies contiguous V-positions), but partitioned above V=2.0 so text and links never overlap.

- **Internal endpoint structure** (within each link): **Fixed sparse keys** by endpoint role — always 1.1 (FROM), 2.1 (TO), 3.1 (THREE), as hardcoded in `setlinkvsas` and the `LINKFROMSPAN/TOSPAN/THREESPAN` constants. No counter increments here; the position is determined entirely by which endpoint role is being stored, not by creation order or content.

This means you cannot infer anything about link identity or order from the V-addresses 1.1/2.1/3.1 — they are type-role slots, not positions in a sequence. The only ordinal structure is at the document level, where each link's I-address occupies one more V-slot appended after the previous link.
