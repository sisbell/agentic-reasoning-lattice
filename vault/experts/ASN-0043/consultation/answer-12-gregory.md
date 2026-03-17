## Question 12 [gregory]

> The type endset is itself an I-address span rather than a symbolic label or enumerated value — what was the design reasoning for making link type a content-identity reference on the tumbler line rather than a distinct categorical mechanism?

## KB Synthesis

The KB doesn't record Nelson's stated reasoning directly, but the design rationale is recoverable by synthesis.

**Uniformity of the three-endpoint structure**

The link data structure stores FROM, TO, and THREE as parallel constructs: all three are I-address spans inserted into the POOM at subspaces 2.x, and indexed in the spanfilade [SS-DUAL-ENFILADE, Finding 0038]. Making type a content reference means the link record is a homogeneous triple — no special categorical slot, no metadata field with a different type. The `LINKATOM` element type and `setlinkvsas()` assignment of digits 1, 2, 3 to the three endsets treats them structurally identically [SS-LINK-SUBSPACE].

**Hierarchical typing via tumbler containment**

The type registry in the bootstrap document uses tumbler addresses to encode subtype relationships: MARGIN at `1.0.2.6.2` is hierarchically nested under FOOTNOTE at `1.0.2.6` [SS-LINK-ENDPOINT, Finding 0024]. This is the same containment predicate used everywhere in the address space — truncate and compare [SS-TUMBLER-CONTAINMENT]. A query "find all footnote-family links" becomes an I-address range query, identical mechanically to any other span search. No separate subtyping mechanism is needed because the tumbler total order already provides containment for free [INV-TUMBLER-TOTAL-ORDER].

**The type registry is itself content**

The bootstrap document's type subspace (`1.0.2.x`) participates in the permascroll and content identity system [SS-CONTENT-IDENTITY]. This means the type definitions can be transcluded, versioned, and linked against. A type is not a categorical constant frozen in code; it is a named location in the docuverse. New types are new entries in a document, not schema changes.

**Discoverability symmetry**

Because type is indexed in the spanfilade the same way source and target are, `find_links` can in principle search by type just as it searches by content — passing the type VSpec as the THREE parameter [SS-FIND-LINKS, Finding 0029]. The design intent was that you could ask "find all QUOTE links touching this span" using a single spanfilade query with three simultaneous I-address constraints. The KB notes this is broken in practice [EC-TYPE-FILTER-NONFUNCTIONAL], but the architectural motivation is clear: a uniform three-way content-identity query with no special cases.

**What the KB cannot confirm**

Whether Nelson articulated this reasoning explicitly is not in the KB. The EC-ORPHANED-LINK matrix [Finding 0024] shows anomalous behavior when both endpoints are deleted (type endset also empties, despite the bootstrap document being intact), suggesting the implementation may not have fully realized the design. The design intent appears to be: *everything is content, type hierarchy is address hierarchy, and the link system needs no categorical mechanism outside the tumbler address space itself*.

---

## Code Exploration

Now I have everything I need. Here is the full answer.

---

## Why Endset Type Is an I-Address Span Rather Than a Categorical Mechanism

### The Evidence in the Code

**The type constants** (`xanadu.h:35-39`):

```c
/* spanfilade span types */
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```

Four integers on the same number line. Crucially, `DOCISPAN = 4` sits right alongside the endset types — document content itself uses this same mechanism. There is no separate enum for "link semantics" vs. "content semantics." Every kind of thing in the system occupies a numeric band of address space.

**The type aliases** (`xanadu.h:73-76`):

```c
typedef typespan typevspan;
typedef typevspan * typevspanset;
typedef typespan typeispan;
typedef typeispan * typeispanset;
```

There is no `typeendset`. An endset IS a span, which IS a tumbler pair. The C type system makes no distinction between a document content span and a link endset span. They are the same struct.

---

### How Type Gets Encoded

**`prefixtumbler` (`tumble.c:641-651`)** is the encoding operation:

```c
int prefixtumbler(tumbler *aptr, INT bint, tumbler *cptr)
{
    tumbler temp1, temp2;
    tumblerclear (&temp1);
    temp1.mantissa[0] = bint;
    movetumbler (aptr, &temp2);
    if (!iszerotumbler (&temp2)) /* yuckh! */
        temp2.exp -= 1;
    tumbleradd (&temp1, &temp2, cptr);
}
```

It prepends `bint` as the leading digit of the tumbler: link ISA `L` becomes `1.L` for from, `2.L` for to, `3.L` for three. This is called directly in `insertspanf` (`spanf1.c:22`):

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```

The endset type is baked into the ORGL-range coordinate of every crumb inserted into the spanfilade. Not as a flag. As a coordinate.

**`beheadtumbler` (`tumble.c:673-683`)** is the inverse — it strips the leading digit to recover the bare link ISA from a retrieved coordinate. It's called in `sporgl.c:264`:

```c
beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
```

`prefixtumbler` / `beheadtumbler` are the encode/decode pair. Type is a coordinate prefix, not a field.

---

### How Type Gets Retrieved

**`retrieveendsetsfromspanf` (`spanf1.c:206-217`)** constructs the query windows:

```c
fromspace.stream.mantissa[0] = LINKFROMSPAN;   // = 1
fromspace.width.mantissa[0] = 1;

tospace.stream.mantissa[0] = LINKTOSPAN;       // = 2
tospace.width.mantissa[0] = 1;

threespace.stream.mantissa[0] = LINKTHREESPAN; // = 3
threespace.width.mantissa[0] = 1;
```

To retrieve from-endsets, restrict ORGLRANGE to `[1, 2)`. To-endsets: `[2, 3)`. Three-endsets: `[3, 4)`. These are literal I-address spans passed to `retrieverestricted`, the same function used for all enfilade lookups. There is no conditional branching on type — just a geometric window into address space.

Similarly, `sporglset2linkset` (`sporgl.c:257-258`) prefixes the orglrange with the spantype before querying:

```c
prefixtumbler(&orglrange->stream, spantype, &range.stream);
prefixtumbler(&orglrange->width, 0, &range.width);
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, ...);
```

The type selection is done by coordinate restriction, not by branching on an enum.

---

### The V-Dimension Mirrors It

**`setlinkvsas` (`do2.c:169-183`)** places each endset at a V-address that mirrors its type integer:

```c
tumblerincrement(fromvsaptr, 0, 1, fromvsaptr);   // from at V = 1.1
tumblerincrement(tovsaptr,   0, 2, tovsaptr);     // to   at V = 2.1
tumblerincrement(threevsaptr,0, 3, threevsaptr);  // three at V = 3.1
```

The link's private POOM (permutation matrix) stores from-content at V = 1.x, to-content at V = 2.x, three-content at V = 3.x. The V-space is partitioned by type, using the same numeric values as the ORGL-space partitioning. The "type" is a consistent coordinate convention across both dimensions of the enfilade.

---

### Type as Position, Not Metadata

The deepest confirmation is `islinkcrum` (`orglinks.c:255-261`):

```c
bool islinkcrum(typecorecrum *crumptr)
{
    if(crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0) {
        return TRUE;
    }
    return FALSE;
}
```

The distinction between text content and link data in the POOM is made by inspecting V-coordinate digits — not a flag, not a type field, not an enum. A crum is a "link crum" if its V coordinate has mantissa[0] == 1 and a nonzero second digit. Type IS position. This applies at every layer: in the spanfilade (ORGL bands), in the POOM (V bands), and in the query machinery (coordinate windows).

The optionality of the three-endset (`do1.c:216`, `do2.c:122-126`) is handled the same way: the `[3,4)` band simply isn't populated. An absent type is an empty address range. No "null" enum value is needed. Non-existence of a type is non-existence of content at that coordinate.

---

### The Design Reasoning

The choice follows from three compounding constraints of the Xanadu model:

**1. The POOM has no metadata fields.** A crumb in the enfilade stores only its position and a `homedoc` tumbler (`type2dbottomcruminfo`). There is no field for "endset type." If type must be stored, it must be stored as position. The enfilade's node structure is a pure geometric object.

**2. The spanfilade must answer the query "find all links whose from-endset overlaps this I-span" in a single geometric operation.** If type were a separate categorical field, the query would require two-pass filtering: first retrieve by I-span, then filter by type field. Instead, encoding type as a coordinate prefix on the ORGL dimension means the query is simply: intersect SPANRANGE against the requested content spans, restrict ORGLRANGE to `[1,2)`. Both constraints are handled by a single call to `retrieverestricted`. No secondary filter needed.

**3. Document content, link identity, and link endsets all live in the same indexed structure.** `DOCISPAN = 4` sits on the same number line as `LINKFROMSPAN = 1`, `LINKTOSPAN = 2`, `LINKTHREESPAN = 3`. The spanfilade is a single uniform index over all of them. A query for "what document contains this I-span" restricts ORGLRANGE to `[4,5)`. A query for "what links reference this I-span as a from-endset" restricts to `[1,2)`. The same machinery, the same function call, different numeric window. This uniformity would be broken if link endsets used a categorical mechanism instead of a position in address space.

The from/to/three distinction is not a type system. It is a coordinate convention: endset N occupies the `[N, N+1)` band of address space. What would be a tag or enum value in a conventional system is here a spatial partition, because the Xanadu model has no concept of metadata separate from content — a thing's identity IS its address, and a thing's kind IS which part of the address space it occupies.
