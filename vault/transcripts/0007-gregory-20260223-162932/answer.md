## KB Synthesis

Based on the knowledge base, **FOLLOWLINK returns V-addresses from ONLY the single document specified in the `homedoc` parameter**, not from all three documents simultaneously.

Here's why:

## Core Mechanism

`[SS-FOLLOWLINK]` from Finding 0048 reveals the key architectural detail:

> "FOLLOWLINK retrieves link endset I-addresses from the link orgl, then converts them to V-addresses using a **specified document's POOM**. The call chain is: `link2sporglset()` extracts I-addresses from the link orgl... Then `linksporglset2specset()` converts I-addresses to V-addresses by looking them up in the **specified `homedoc`'s POOM**."

The operation explicitly takes a `homedoc` parameter that determines which single document's POOM is consulted for I-to-V conversion.

## Formal Definition

The postcondition is:

```
followlink(link, whichend, homedoc) = { v | ∃ i ∈ endset(link, whichend) : poom.homedoc(v) = i }
```

This states that FOLLOWLINK returns **only those V-addresses from the specified homedoc** where the homedoc's POOM maps to the link's I-addresses.

## Query Context Dependency

`[INT-LINK-VERSION]` Finding 0019 confirms this behavior:

> "The endset docid is rewritten to the queried document's address, even though the link was created against the original. This means **endsets are relative to the query context, not absolute**."

## Concrete Example

For your scenario:
- Document A (original): POOM.A maps V-positions to {i₁, i₂, i₃}
- Document B (transclusion): POOM.B maps V-positions to {i₁, i₂, i₃}  
- Document C (transclusion): POOM.C maps V-positions to {i₁, i₂, i₃}
- Link L has source endset containing {i₁, i₂, i₃}

Then:
- `FOLLOWLINK(L, SOURCE, homedoc=A)` → returns V-addresses from A only
- `FOLLOWLINK(L, SOURCE, homedoc=B)` → returns V-addresses from B only
- `FOLLOWLINK(L, SOURCE, homedoc=C)` → returns V-addresses from C only

## Contrast with find_links

This differs from `find_links`, which discovers the link from **any** of the three documents (because `find_links` works by I-address intersection and searches globally per `[INT-LINK-TRANSCLUSION]`). But FOLLOWLINK is explicitly scoped to a single document for the I-to-V resolution phase.

## Silent Filtering

`[INV-ITOV-FILTERING]` from Finding 0048 adds that if the specified homedoc doesn't actually contain those I-addresses in its POOM, "the I-address is dropped from the result without error" — producing an empty or partial result rather than including V-addresses from other documents.

## Code Exploration

Based on my analysis of the C source code, here is the complete answer to your question:

---

# FOLLOWLINK Returns Creation Document V-Addresses, Not Query Document

## Direct Answer

**When a link's source endset content exists in three documents simultaneously (original + two transclusions sharing the same I-addresses), FOLLOWLINK returns V-addresses ONLY from the document that was used when the link was created, NOT from the document used in the find_links query.**

## Complete Execution Path

### 1. Link Creation (`docreatelink` [do1.c:195-221])

When you create a link, the endsets are specified as V-specs (document + V-spans):

```c
// Line 214-216: Convert V-specs to sporgls (I-spans + document ID)
&& specset2sporglset (taskptr, fromspecset, &fromsporglset,NOBERTREQUIRED)
&& specset2sporglset (taskptr, tospecset, &tosporglset,NOBERTREQUIRED)
&& specset2sporglset (taskptr, threespecset, &threesporglset,NOBERTREQUIRED)
```

In `vspanset2sporglset` [sporgl.c:35-65]:

```c
// Line 53: Store the CREATION document ID permanently in the link
movetumbler (docisa, &sporglset->sporgladdress);
movetumbler(&ispanset->stream,&sporglset->sporglorigin);  // I-address
movetumbler (&ispanset->width, &sporglset->sporglwidth);   // I-width
```

**The sporgl permanently stores: (creation_document_ID, I-address, I-width)**

### 2. Link Following (`dofollowlink` [do1.c:223-232])

When you follow a link:

```c
return (
   link2sporglset (taskptr, linkisaptr, &sporglset, whichend,NOBERTREQUIRED)
&& linksporglset2specset (taskptr,
                          &((typesporgl *)sporglset)->sporgladdress,  // ← creation doc!
                          sporglset, specsetptr, NOBERTREQUIRED));
```

The `homedoc` parameter is `&((typesporgl *)sporglset)->sporgladdress` — **the document ID stored when the link was created.**

In `linksporglset2vspec` [sporgl.c:127-137]:

```c
// Line 134: Use the creation document ID, not any query document
movetumbler (homedoc/*&sporglset->sporgladdress*/, &specptr->docisa);
```

The commented-out code confirms this was explicitly the sporgl's stored address.

In `sporglset2vspanset` [sporgl.c:141-176]:

```c
// Line 152: Retrieve the CREATION document's permutation matrix
findorgl (taskptr, granf, homedoc/*&sporglptr->sporgladdress*/, &orgl,type);
// Line 157: Convert I→V using that specific document's matrix
vspansetptr = ispan2vspanset (taskptr, orgl, &ispan, vspansetptr);
```

Finally, `ispan2vspanset` [orglinks.c:389-394] calls `permute` [orglinks.c:404-422], which uses the creation document's permutation matrix to convert I-addresses back to V-addresses.

### 3. Link Finding (Context)

`dofindlinksfromtothree` [do1.c:348-353] → `findlinksfromtothreesp` [spanf1.c:56-103]:

- Converts query V-specs to I-spans
- Searches for links whose endsets overlap those I-spans
- Returns link ISAs unchanged
- **Does NOT modify the links or their stored document bindings**

## Concrete Example

```
Setup:
- Doc A: "hello" at V=1.1 → I=100.1
- Doc B: Transclude from A → I=100.1 at V=1.5
- Doc C: Transclude from A → I=100.1 at V=1.8  
- Doc D: CREATE_LINK(target → B:V=1.5)

Link stores: target = {doc: B, I-addr: 100.1}

Query:
- FIND_LINKS(target → C:V=1.8)
  → Converts C:V=1.8 → I=100.1
  → Finds link (matches I=100.1)
  → Returns link ISA
  
- FOLLOW_LINK(link, TARGET)
  → Retrieves {doc: B, I-addr: 100.1}
  → Converts using B's matrix: I=100.1 → V=1.5
  → Returns SpecSet(VSpec(B, V=1.5))
  
Result: V=1.5 in document B (creation), NOT V=1.8 in document C (query)
```

## Key Code Citations

| File:Line | Code | Significance |
|-----------|------|--------------|
| sporgl.c:53 | `movetumbler (docisa, &sporglset->sporgladdress)` | Stores creation doc in link |
| do1.c:230 | `&((typesporgl *)sporglset)->sporgladdress` | Passes stored doc as `homedoc` |
| sporgl.c:134 | `movetumbler (homedoc/*&sporglset->sporgladdress*/, &specptr->docisa)` | Uses creation doc for result |
| sporgl.c:152 | `findorgl (taskptr, granf, homedoc/*&sporglptr->sporgladdress*/, &orgl,type)` | Retrieves creation doc's matrix |
| orglinks.c:393 | `return permute(taskptr, orgl, ispanptr, I, vspansetptr, V)` | Converts I→V using creation doc |

## Implications

1. **Link bindings are immutable** — Links permanently point to specific documents chosen at creation time
2. **Transclusion doesn't redirect links** — Finding a link via transcluded content doesn't change where it points
3. **Document-relative semantics** — Links bind to (document, V-address) pairs, not just content identity
4. **No transclusion chasing** — FOLLOWLINK doesn't follow content identity across documents

This behavior is by design: links store explicit document references and always resolve relative to those references, ensuring stable, unambiguous link targets regardless of how the link was discovered.
