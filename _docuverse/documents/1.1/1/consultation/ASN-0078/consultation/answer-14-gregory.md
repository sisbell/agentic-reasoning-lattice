## Question 14 [gregory]

> `insertendsetsinspanf` indexes link endsets in the spanfilade — does it create one spanfilade entry per endset, one per I-span within each endset, or one entry covering all three endsets, and what key structure distinguishes source/target/type entries?

## KB Synthesis

`insertendsetsinspanf` creates **one spanfilade entry per I-span within each endset**, and distinguishes source/target/type via ORGLRANGE subspace tags.

## Granularity: Per I-span per endset

`insertendsetsinspanf` receives three sporglsets — one each for from, to, and type — and calls `insertspanf` once per endset type [INT-SPORGL-LINK-INDEX, Finding 0013, `do2.c:116-128`]. `insertspanf` then iterates over the sporglset linked list and makes **one `insertnd` call per `typeispan` struct** [SS-DOCISPAN, Finding 0047, `spanf1.c:15-53`].

A single user-visible V-span can produce **multiple I-spans** when the spanned content is transcluded from multiple sources. For example, a V-span covering "AABB" where "AA" came from document A and "BB" from document B produces two sporgls → two spanfilade entries for that endset [ST-LINK-CREATE, Finding 0037, `sporgl.c:49-58`].

So for a link with a simple (single-source) endset:
- From endset: 1 spanfilade entry  
- To endset: 1 spanfilade entry  
- Type endset: 1 spanfilade entry  
Total: 3 entries

For a link whose from-endset spans content from N discontiguous I-address regions: N + 1 + 1 = N+2 entries.

## Key structure: ORGLRANGE subspace tags

The spanfilade is a 2D enfilade with two dimensions [SS-RETRIEVE-ENDSETS, Finding 0035]:
- **SPANRANGE** (dimension 0): the I-address content range — keys on the content identity
- **ORGLRANGE** (dimension 1): the link type/origin — distinguishes which endset type an entry belongs to

The three endpoint types occupy separate ORGLRANGE subspaces with hardcoded prefix values:
| Endset | ORGLRANGE value |
|--------|----------------|
| LINKFROMSPAN | 1 |
| LINKTOSPAN | 2 |
| LINKTHREESPAN | 3 |

Each spanfilade entry maps `(I-address range, endset-type prefix) → link ISA`. When RETRIEVEENDSETS searches, it restricts the ORGLRANGE dimension to one of these three prefixes per endset type [SS-RETRIEVE-ENDSETS, `spanf1.c:190-235`].

This is the same structure FINDLINKSFROMTOTHREE uses — it searches all three endset types by intersecting the query I-addresses against the SPANRANGE dimension, collecting links tagged with LINKFROMSPAN, LINKTOSPAN, or LINKTHREESPAN respectively [INT-SPORGL-LINK-INDEX, Finding 0035].

---

## Code Exploration

I now have everything needed. Here is the complete answer.

---

## `insertendsetsinspanf`: Granularity and Key Structure

### Function location

`insertendsetsinspanf` is defined at `backend/do2.c:116-128`:

```c
bool insertendsetsinspanf(typetask *taskptr, typespanf spanfptr, typeisa *linkisaptr,
    typesporglset fromsporglset, typesporglset tosporglset, typesporglset threesporglset)
{  bool insertspanf();
  if (!(
    insertspanf(taskptr,spanfptr,linkisaptr,fromsporglset,LINKFROMSPAN)
      &&insertspanf(taskptr,spanfptr,linkisaptr,tosporglset,LINKTOSPAN)))
        return (FALSE);
  if (threesporglset) {
    if(!insertspanf(taskptr,spanfptr,linkisaptr,threesporglset,LINKTHREESPAN)){
        return (FALSE);
     }
  }
  return(TRUE);
}
```

It makes **three separate calls** to `insertspanf` — one per endset role — passing the endset-type discriminant as the last argument.

---

### How many spanfilade entries are created?

**One entry per I-span within each endset**, not one per endset and not one covering all three.

`insertspanf` [`backend/spanf1.c:15-53`] iterates over the sporglset and calls `insertnd` once per element:

```c
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    // extract lstream, lwidth from element ...
    movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
    movetumbler (&lwidth,  &crumwidth.dsas[SPANRANGE]);
    insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
                                                          // ^^^ one call per element
}
```

[`spanf1.c:25-52`]

So for a link whose source endset covers three I-spans, the spanfilade receives **three FROM entries, N TO entries, M THREE entries** — one crum per I-span per role.

---

### Key structure distinguishing source / target / type

The spanfilade is a 2D structure (defined in `backend/wisp.h:15-16`):

```c
#define ORGLRANGE 0    // dimension 0: "orgl" axis — the link identity
#define SPANRANGE 1    // dimension 1: "span" axis — the I-span content position
```

Each inserted crum carries a 2D origin and width (`typewid crumorigin`, `typewid crumwidth`), each with two tumbler components.

**ORGLRANGE dimension (dim 0) — link identity + endset role:**

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);   // spanf1.c:22
tumblerclear  (&crumwidth.dsas[ORGLRANGE]);                       // spanf1.c:23
```

`prefixtumbler` [`backend/tumble.c:641-651`] prepends the integer `spantype` as the high component of the tumbler:

```c
int prefixtumbler(tumbler *aptr, INT bint, tumbler *cptr)
{
  tumbler temp1, temp2;
    tumblerclear (&temp1);
    temp1.mantissa[0] = bint;          // high component = spantype
    movetumbler (aptr, &temp2);        // then shift in the link ISA
    if (!iszerotumbler (&temp2))
        temp2.exp -= 1;
    tumbleradd (&temp1, &temp2, cptr); // result = spantype.linkISA
}
```

The three endset roles are assigned these integers [`backend/xanadu.h:36-38`]:

```c
#define LINKFROMSPAN    1     // source endset
#define LINKTOSPAN      2     // target endset
#define LINKTHREESPAN   3     // type/three endset
```

So the ORGLRANGE key is: **`spantype . linkISA`** — the endset-type integer forms the most-significant component, followed by the link's ISA tumbler. Width is zeroed out (`tumblerclear`), making each link ISA a point in the ORGLRANGE axis.

**SPANRANGE dimension (dim 1) — I-span content position:**

```c
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);   // spanf1.c:49
movetumbler (&lwidth,  &crumwidth.dsas[SPANRANGE]);    // spanf1.c:50
```

`lstream` and `lwidth` are the I-span's stream address and width, extracted from the sporglset element (an `ISPANID`, `SPORGLID`, or `TEXTID` item). This is the content axis: it records *where in I-space* this endset I-span lives.

**Payload (`linfo.homedoc`):** stores the link ISA (or for SPORGL items, the sporgl's home document), available during retrieval.

---

### Lookup confirms the structure

`retrieveendsetsfromspanf` [`spanf1.c:190-235`] inverts the lookup by constructing ORGLRANGE probes that are single-unit intervals at position 1, 2, or 3:

```c
fromspace.stream.mantissa[0] = LINKFROMSPAN;    // = 1
fromspace.width.mantissa[0]  = 1;

tospace.stream.mantissa[0]   = LINKTOSPAN;      // = 2
tospace.width.mantissa[0]    = 1;

threespace.stream.mantissa[0] = LINKTHREESPAN;  // = 3
threespace.width.mantissa[0]  = 1;
```

Each probe retrieves all spanfilade crums whose ORGLRANGE component falls within `[role, role+1)`, meaning all entries for that endset role regardless of which link they belong to. The link ISA is then read out of the ORGLRANGE key component.

---

### Summary

| Question | Answer |
|---|---|
| Entries per link | One **per I-span per endset role** (not one per endset, not one total) |
| FROM entries | ORGLRANGE key = `1.linkISA`, SPANRANGE key = I-span stream/width |
| TO entries | ORGLRANGE key = `2.linkISA`, SPANRANGE key = I-span stream/width |
| THREE entries | ORGLRANGE key = `3.linkISA`, SPANRANGE key = I-span stream/width |
| Discriminant | High tumbler component of ORGLRANGE: 1=source, 2=target, 3=type |
| Width on ORGLRANGE | Always zero (point, not range) — link ISA is a unique address |
| Payload | `linfo.homedoc` = link ISA (or SPORGL home document) |

The design gives O(log n) lookup in either direction: given an I-span you can find all links that include it (any role) by probing SPANRANGE; given a link ISA you can enumerate its endsets by probing ORGLRANGE. The `LINKFROMSPAN`/`LINKTOSPAN`/`LINKTHREESPAN` prefix is the sole structural distinction between source, target, and type entries — there is no separate index or sub-tree per role.
