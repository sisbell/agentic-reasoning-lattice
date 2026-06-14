## Question 1 [evidence]

> Is a home's interleaved link-allocation frontier `f_d` maintained as a single count readable in one access (e.g. a per-home width/frontier at the enfilade home node), or is it recoverable only by scanning/maxing across the per-type sub-chains homed at that document?

## KB Synthesis

The frontier is recovered by scanning, not stored as a cached field.

[SS-ADDRESS-ALLOC] Finding 0065 and [SS-ADDRESS-SPACE] Finding 0061 are the directly relevant entries. Each MAKELINK call:

1. Computes `upperbound = docISA.2.3` (the upper edge of the document's link subspace)
2. Calls `findpreviousisagr` — a bounded tree traversal that walks the global granfilade to find the highest existing I-address strictly below that bound
3. If the result falls below `docISA.2.2` (no links yet), allocates at `docISA.2.2.1`; otherwise increments the found maximum by `0.1`

Code references from [ST-ADDRESS-ALLOC] Finding 0065: `granf2.c:162–175`.

There is no cached per-home frontier field anywhere. [SS-ADDRESS-SPACE] Finding 0077 states this explicitly: "There is no single global 'next' counter (no Σ.next). Allocation is stateless query-and-increment on different tumbler ranges via `findpreviousisagr`." [INV-MONOTONIC] Finding 0061 confirms: "The allocation is purely derived from current tree state — there is no cached 'next available' pointer."

The same stateless query-and-increment pattern governs text I-address allocation ([SS-ADDRESS-SPACE] Finding 0061), document address allocation ([ST-ADDRESS-ALLOC] Finding 0021), and version address allocation ([ST-ADDRESS-ALLOC] Finding 0068). All of them issue a `findpreviousisagr` call at allocation time rather than maintaining a running frontier.

The practical consequence for the spec: `next_link_iaddr(granf, doc) = max_link_iaddr_under(granf, doc) + 1` is a pure function of the granfilade tree state at the moment of the call. The frontier is implicit in the tree, not explicit in any metadata field at the home node.

---

## Code Exploration

I have everything I need. Let me now synthesize the complete answer from the source.

---

## Answer

`f_d` is **not** maintained as a single stored count, and recovery does **not** require scanning/maxing across per-type sub-chains. The implementation is a third option: a **maintained aggregate at the enfilade apex** (O(1) bounds check) combined with a **type-bounded tree descent** (O(log n)) when the type-specific frontier is needed. Here is the full chain of evidence.

---

### The data structure: `cwid.dsas[WIDTH]` on every crum

Every crum — upper (`typecuc`) and bottom (`typecbc`) — carries a `typewid cwid` field [`enf.h:47`, `enf.h:71`, `enf.h:102`]. For a GRAN (granfilade) enfilade, `typewid` contains a single tumbler slot:

```c
/* wisp.h:12 */
#define WIDTH  0

/* wisp.h:23 */
#define WIDSIZEGR 1

struct structwid {
    tumbler dsas[MAXLOXIZE];   /* wisp.h:50-52 */
};
typedef struct structwid typewid;
```

So each crum in the global granfilade stores one tumbler `cwid.dsas[WIDTH]` — its width in ISA-address space.

The fullcrum (apex, `isapex == TRUE`) stores the **sum of all children's widths** — the total occupied frontier of the entire granfilade.

---

### The aggregate is maintained, not recomputed on demand

`setwispupwards` [`wisp.c:83-111`] is called at the end of every `insertseq` [`insert.c:62-63`]:

```c
/* insert.c:62-63 */
setwispupwards (findfather ((typecorecrum*)ptr),0);
setwispupwards (findfather ((typecorecrum*)new),1);
```

`setwispupwards` walks from the modified node up to the fullcrum, calling `setwisp` on each ancestor. For GRAN enfilades, `setwisp` dispatches to `setwidseq` [`wisp.c:150-168`]:

```c
/* wisp.c:150-168 */
bool setwidseq(typecuc *father)
{
    typecorecrum *ptr;
    typewid sum;
    ...
    clear (&sum, sizeof (sum));
    for (ptr = findleftson (father); ptr; ptr = getrightbro (ptr)){
        widopseq (&sum, &ptr->cwid, &sum);   /* sum += child.cwid */
    }
    if (lockeq (sum.dsas, father->cwid.dsas, (unsigned)widsize(father->cenftype)))
        return (FALSE);
    movewisp (&sum, &father->cwid);          /* store result upward */
    ivemodified ((typecorecrum*)father);
    return (TRUE);
}
```

The loop sums all children; the result is written back into `father->cwid`. This propagates all the way to the fullcrum after every insertion, so the fullcrum's `cwid.dsas[WIDTH]` is always current — it is a maintained aggregate, not a stale snapshot.

---

### Reading the frontier at the apex: one access

`fetchorglgr` [`granf2.c:22-81`] opens with a direct O(1) bounds check against the fullcrum's stored width:

```c
/* granf2.c:31-32 */
if (tumblercmp (&((typecuc*)fullcrumptr)->cwid.dsas[WIDTH], address) == LESS)
    return (NULL);
```

If the requested ISA address exceeds the fullcrum's `cwid.dsas[WIDTH]`, the entry does not exist — no tree traversal needed. The fullcrum's width **is** the frontier of the entire granfilade in O(1).

---

### But this frontier is not type-specific

Text atoms (`TEXTATOM = 1`) and link atoms (`LINKATOM = 2`) are interleaved in the **same** sequential granfilade. There are no separate per-type sub-chains, no separate link-specific frontier field, and no separate link-count register. The fullcrum's `cwid.dsas[WIDTH]` covers all content together.

The type separation lives entirely in the **ISA address structure**. A link orgl homed at document `d` gets an ISA address under `d.0.0.2.*` (from the `atomtype = LINKATOM = 2` passed to `makehint` [`do2.c:78-84`]):

```c
/* do1.c:207 */
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
```

```c
/* xanadu.h:145-146 */
#define TEXTATOM  1
#define LINKATOM  2
```

---

### Recovering the type-specific frontier: tree descent, not full scan

To allocate the next link ISA under document `d`, `docreatelink` [`do1.c:195-221`] calls `createorglingranf` → `createorglgr` → `findisatoinsertgr` → `findisatoinsertmolecule` [`granf2.c:158-181`]:

```c
/* granf2.c:158-181 */
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
    /* upperbound = d.0.0.3 for LINKATOM (atomtype=2, +1=3) */

    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
    /* finds highest existing ISA < upperbound */

    ...
    } else if (hintptr->atomtype == LINKATOM) {
        tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);  /* floor = d.0.0.2 */
        if (tumblercmp (&lowerbound, isaptr) == LESS)
            tumblerincrement (isaptr, 1, 1, isaptr);
        else
            tumblerincrement (&lowerbound , 0, 1, isaptr);   /* new = last + 1 */
    }
```

`findpreviousisagr` [`granf2.c:255-278`] is the key function:

```c
/* granf2.c:255-278 */
int findpreviousisagr(typecorecrum *crumptr, typeisa *upperbound, typeisa *offset)
{
    if (crumptr->height == 0) {
        findlastisaincbcgr ((typecbc*)crumptr, offset);
        return(0);
    }
    for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
        if (
         (tmp= whereoncrum (ptr, (typewid*)offset, upperbound, WIDTH)) == THRUME
        || tmp == ONMYRIGHTBORDER
        || !ptr->rightbro) {
            findpreviousisagr (ptr, upperbound, offset);   /* descend into subtree */
            return(0);
        } else {
            tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);  /* skip left siblings */
        }
    }
}
```

This is a **width-guided tree descent**: at each level it checks `whereoncrum`, and either descends into the containing subtree or adds that sibling's `cwid.dsas[WIDTH]` to the accumulated offset and moves right. This is O(log n) in tree height — not a brute-force scan of all crums, and not a scan of per-type sub-chains.

---

### The V-space link frontier: also not a stored count

After allocating the link's ISA address, `docreatelink` [`do1.c:211`] calls `findnextlinkvsa` to determine where in the document's V-space to place the link reference:

```c
/* do2.c:151-167 */
bool findnextlinkvsa(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr)
{
    tumbler vspanreach, firstlink;
    typevspan vspan;

    tumblerclear (&firstlink);
    tumblerincrement (&firstlink, 0, 2, &firstlink);   /* link subspace floor */
    tumblerincrement (&firstlink, 1, 1, &firstlink);

    (void) doretrievedocvspan (taskptr, docisaptr, &vspan);
    tumbleradd (&vspan.stream, &vspan.width, &vspanreach);   /* end of doc V-span */
    if (tumblercmp (&vspanreach, &firstlink) == LESS)
        movetumbler (&firstlink, vsaptr);
    else
        movetumbler (&vspanreach, vsaptr);
    return (TRUE);
}
```

This reads the document's POOM orgl total V-span (via `doretrievedocvspan` → `retrievevspanpm`), takes its end, and clamps to a minimum link-subspace address. No per-type sub-chain scan — one POOM traversal to get the document's total width.

---

### Summary

| Frontier | Where stored | Cost to read |
|---|---|---|
| Total granfilade content frontier | `fullcrum->cwid.dsas[WIDTH]` [`enf.h:47`, maintained by `setwispupwards`/`setwidseq`] | O(1) — one field read |
| Type-specific link ISA frontier (last link under document D) | **Not stored** — recovered by `findpreviousisagr` with upper bound `d.0.0.3` | O(log n) tree descent using sibling `cwid.dsas[WIDTH]` values |
| V-space link placement frontier | **Not stored** — recovered by reading the document's POOM total V-span | O(log n) POOM traversal |

The global granfilade has **no per-home, per-type link count**. The fullcrum stores only one maintained aggregate covering all content interleaved. Recovering the type-specific link allocation frontier requires `findpreviousisagr` — a type-bounded tree descent that uses each crum's stored `cwid.dsas[WIDTH]` to skip non-containing subtrees efficiently, not a linear scan or max across per-type sub-chains (which don't exist as separate structures).
