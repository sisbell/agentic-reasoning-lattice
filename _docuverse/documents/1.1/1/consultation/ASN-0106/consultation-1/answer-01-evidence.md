## Question 1 [evidence]

> For a full-extent document read, does the operation return two V-width spans (the character and link counts) or a fragmented list of mapping blocks reflecting I-discontinuities?

## KB Synthesis

**Full-extent document read returns subspace-based V-spans, not I-discontinuity fragments.**

`RETRIEVEDOCVSPANSET` produces at most two spans — one per occupied subspace — regardless of how fragmented the underlying I-address mapping is [SS-VSPAN-VS-VSPANSET]:

- Text-only document → one span: `{start: 1.1, width: 0.N}`
- Document with text + links → two spans: `{start: 0, width: 0.1}` (link subspace, normalized from internal 2.x) and `{start: 1, width: 1}` (text subspace) [SS-DUAL-ENFILADE, Finding 0038]

The key reason I-discontinuities do not appear is [INV-VSPAN-CONSOLIDATION]: the enfilade consolidates logically contiguous V-space regions into a single span regardless of insertion history. 100 sequential single-character inserts produce `span_count: 1`. Content transcluded from multiple non-contiguous I-address sources still presents as one contiguous V-region within its subspace.

The POOM is precisely the abstraction layer that hides I-space fragmentation behind a consolidated V-space view [SS-POOM-MULTIMAP]. The per-crum POOM tree structure (which does reflect I-address boundaries) is internal — `RETRIEVEDOCVSPANSET` aggregates across all POOM crums via `retrievevspansetpm()`, which tests `is1story()` to detect multi-subspace documents and returns one span per subspace, not one span per bottom crum [SS-VSPAN-VS-VSPANSET, Finding 0035].

**Summary:** Two spans maximum (one per occupied subspace), never fragmented by I-address discontinuities.

---

## Code Exploration

Now I have everything I need to give a definitive answer.

---

## Full-Extent Document Read: What Is Returned

**Short answer: The operation returns V-width aggregate spans — at most two — not a fragmented list of I-space mapping blocks.**

---

### Call Chain for Full-Extent Read

The FEBE handler is `retrievedocvspanset` [`fns.c:129`]:

```c
void retrievedocvspanset(typetask *taskptr)
{
  typeisa docisa;
  typevspanset vspanset;
    if (
       getretrievedocvspanset (taskptr, &docisa)
    && doretrievedocvspanset (taskptr, &docisa, &vspanset))
            putretrievedocvspanset (taskptr, &vspanset);
      else
            putrequestfailed (taskptr);
}
```

It dispatches to `doretrievedocvspanset` [`do1.c:322`]:

```c
bool doretrievedocvspanset(typetask *taskptr, typeisa *docisaptr, typevspanset *vspansetptr)
{
    if (!findorgl (taskptr, granf, docisaptr, &docorgl, READBERT))
            return FALSE;
    if (isemptyorgl (docorgl)) {
            *vspansetptr = NULL;
            return TRUE;
    }
    return retrievevspansetpm (taskptr, docorgl, vspansetptr);
}
```

The core logic is in `retrievevspansetpm` [`orglinks.c:173`].

---

### The Two-Branch Logic in `retrievevspansetpm`

```c
bool retrievevspansetpm(typetask *taskptr, typeorgl orgl, typevspanset *vspansetptr)
{
  typecorecrum *ccptr;
    ccptr = (typecorecrum *) orgl;
    tumblerclear (&voffset);
    *vspansetptr = NULL;
    if (is1story (&ccptr->cwid.dsas[V])) {      /* [orglinks.c:184] */
        /* TEXT-ONLY: single vspan */
        vspan.stream = ccptr->cdsp.dsas[V];      /* [orglinks.c:186] */
        vspan.width  = ccptr->cwid.dsas[V];      /* [orglinks.c:187] */
        putvspaninlist (taskptr, &vspan, vspansetptr);
        return TRUE;
    } else {
        /* TEXT + LINKS: two separate vspans */
        /* link span: grab the mantissa[1] component of the root width */
        linkvspan.stream = ccptr->cwid.dsas[V];  linkvspan.stream.mantissa[1] = 0; /* [orglinks.c:197-199] */
        linkvspan.width  = ccptr->cwid.dsas[V];  linkvspan.width.mantissa[1]  = 0; /* [orglinks.c:201-203] */

        /* text span: walk enfilade tree to find max text V-coordinate */
        maxtextwid(taskptr, ccptr, &voffset, &maxwid);  /* [orglinks.c:207] */
        vspan.stream = zero;
        vspan.width  = maxwid; vspan.width.mantissa[0] = 0;   /* [orglinks.c:211] */

        putvspaninlist (taskptr, &vspan, vspansetptr);    /* [orglinks.c:216] */
        putvspaninlist (taskptr, &linkvspan, vspansetptr); /* [orglinks.c:217] */
        return TRUE;
    }
}
```

**`is1story`** [`tumble.c:237`] tests whether the V-width tumbler has a non-zero value only in `mantissa[0]` — i.e., whether the entire document exists purely in V-story 0 (text space):

```c
bool is1story(tumbler *tumblerptr) {
    for (i = 1; i < NPLACES; i++)
        if (tumblerptr->mantissa[i] != 0)
            return (FALSE);
    return (TRUE);
}
```

V-space encodes the document in a tumbler where `mantissa[0]` is the text extent and `mantissa[1]` is the link extent (the `1.n` subspace — `islinkcrum` at [`orglinks.c:255`] confirms: "if the crum is displaced into link space it is a link crum — true if the tumbler is a `1.n` tumbler where `n != 0`").

---

### Why NOT Fragmented I-Space Mapping Blocks

The result is computed entirely by reading from the **root orgl crum** (`ccptr->cdsp.dsas[V]` and `ccptr->cwid.dsas[V]`) — the enfilade root's aggregate summary values. The function never walks individual leaf crums to emit per-crum I-space coordinates, and never calls `ispan2vspanset` or `vspanset2ispanset`.

The **commented-out predecessor** `walkorglonvpm` [`orglinks.c:277`] (inside `#ifdef UnDEFined`) *would* have fragmented this into per-crum vspans by recursing through the tree:

```c
/* DEAD CODE — inside #ifdef UnDEFined [orglinks.c:263-313] */
int walkorglonvpm(...) {
    if (is1story (&crumptr->cwid.dsas[V])) {
        /* emit one vspan per leaf crum */
        putvspaninlist (taskptr, &vspan, vspansetptr);
    } else {
        /* recurse into children */
        for(ptr = findleftson(...); ptr; ptr = findrightbro(ptr))
            walkorglonvpm(taskptr, ptr, &localvoffset, vspansetptr);
    }
}
```

That dead-code path would have produced one V-span per contiguous I-region — i.e., a fragmented mapping that reflects I-discontinuities. It was abandoned. The live code at [`orglinks.c:173`] replaces it with the two-aggregate-span approach.

---

### Summary

| Operation | Result |
|---|---|
| `retrievedocvspan` → `retrievevspanpm` [`orglinks.c:165`] | **1 V-span**: raw root orgl width (entire V extent, no decomposition) |
| `retrievedocvspanset` → `retrievevspansetpm` [`orglinks.c:173`] | **1 V-span** (text-only doc) or **2 V-spans** (doc with links) |

The two spans in the multi-story case are:
1. **Text span**: `vspan` — covers V-story 0 (characters), width derived from `maxtextwid` tree walk
2. **Link span**: `linkvspan` — covers V-story 1 (link metadata), width taken from `ccptr->cwid.dsas[V].mantissa[1]`

These are **V-space topology regions** (two different tumbler stories), not I-space mapping fragments. I-space fragmentation would require calling `permute` / `ispan2vspanset` to project through the enfilade — that machinery exists in `orglinks.c:389–422` but is not invoked during a document extent query. The result tells you *how wide the document is in V-space*, partitioned by content type (text vs. link), not where those characters live in the permascroll.
