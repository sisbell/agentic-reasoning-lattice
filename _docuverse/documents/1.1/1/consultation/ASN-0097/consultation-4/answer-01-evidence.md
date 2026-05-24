## Question 1 [evidence]

> In udanax-green, how is the link subspace of a document arranged — does the V→I map for the link subspace point into the link store's address space, and is it implemented as a separate map or as a typed range within a unified arrangement?

## KB Synthesis

The link subspace is a **typed range within a unified per-document POOM enfilade**, not a separate map. Here is how it works:

## V→I Map Structure

Each document has a single POOM (Permutation Of Ordered Mappings) enfilade that maps V-positions to I-addresses across all three subspaces. The first mantissa digit of the V-address is the sole discriminator: `1.x` = text, `2.x` = link orgl references, `3.x` = link type endpoints [SS-DUAL-ENFILADE, SS-SUBSPACE-CONVENTION, SS-TWO-BLADE-KNIFE].

The enfilade storage is entirely type-agnostic — `insertpm`, `docopy`, `retrieverestricted`, and `permute` treat all V→I entries identically [SS-DUAL-ENFILADE Finding 0011]. There is no runtime type tag. Subspace membership is enforced by convention at the caller level only (`acceptablevsa()` is a stub that always returns TRUE) [PRE-SUBSPACE-CONVENTION].

## What the V→I Map Points To

At V-positions `2.x`, the I-addresses stored are **link orgl ISAs** — addresses like `1.1.0.1.0.1.0.2.1`. These are NOT in a separate "link store" address space; they live in the same global granfilade as text content and document orgls. Link orgls are allocated via `createorglingranf()`, and the resulting ISA is then written into the document's POOM at the next available `2.x` V-position via `docopy()` [SS-DUAL-ENFILADE Finding 0009, SS-ADDRESS-SPACE Finding 0065].

Link I-addresses follow the pattern `account.0.document.0.2.N` where element field `2` scopes the link address under its home document, and `N` is allocated monotonically per document [SS-ADDRESS-SPACE Finding 0065].

## The Two-Enfilade System

Separate from the per-document POOM is the global **spanfilade** (`spanf`), which is an entirely different enfilade mapping I-addresses → link ISAs for discovery purposes. This is the link *search index*, not the per-document V→I map. Only `create_link` writes to both: it updates the document's POOM (inserting the link ISA at `2.x`) AND indexes the link endpoints in the spanfilade [SS-DUAL-ENFILADE Finding 0012, ST-CREATE-LINK].

## Summary

| Layer | Structure | Points to |
|-------|-----------|-----------|
| POOM V→I at `1.x` | Unified POOM (typed range) | Permascroll I-addresses (text bytes) |
| POOM V→I at `2.x` | Unified POOM (typed range) | Link orgl ISAs (in granfilade) |
| Spanfilade | Separate global index | Links discoverable by I-address |

The link subspace is thus a **typed range within the unified per-document POOM**, and its I-addresses point into the same global granfilade address space as all other orgls — there is no distinct link store address space [SS-DUAL-ENFILADE, SS-UNIFIED-STORAGE].

---

## Code Exploration

Now I have everything I need. Let me compose the full answer with precise code citations.

---

## How the Link Subspace Is Arranged in Udanax Green

### Short answer

The V→I map for the link subspace lives inside **the same POOM (permutation matrix enfilade) as the text subspace** — there is no separate map. It is a typed range within a unified arrangement, where the V-address's first mantissa digit (1 vs. 2) indicates subspace membership. When you permute a V-address from the link subspace, you get back the link's **ISA** — its address in the permascroll's I-space — not a text content address.

---

### The Two Subspaces Within One Document Organizer

Every document has exactly one POOM ("orgl"), fetched from the single global `granf` enfilade. Both text characters and link references share that one organizer.

The V-dimension is partitioned by convention on the **first mantissa digit** of the tumbler:

| V-range | First digit | Content |
|---------|-------------|---------|
| 1.1 onward | `mantissa[0] == 1` | Text characters |
| 2.1 onward | `mantissa[0] == 2` | Link references (one per link created in this document) |

The boundary is hard-coded as `linkspacevstart = 2.0` in `findvsatoappend` [`orglinks.c:37`]:

```c
tumblerincrement (&linkspacevstart, 0, 2, &linkspacevstart);   // linkspacevstart = 2
```

The first text insertion on an empty document goes to V = 1.1 [`orglinks.c:42-43`]:

```c
tumblerincrement (vsaptr, 0, 1, vsaptr); /* no text in doc */
tumblerincrement (vsaptr, 1, 1, vsaptr);
```

The first link reference goes to V = 2.1 [`do2.c:156-157`]:

```c
tumblerincrement (&firstlink, 0, 2, &firstlink);   // mantissa[0] = 2
tumblerincrement (&firstlink, 1, 1, &firstlink);   // mantissa[1] = 1  →  2.1
```

Subsequent link references take consecutive positions: the next is at `reach(vspan) + 1` step in the 2.x range.

---

### There Is No Separate V→I Map

`vspanset2ispanset` and `ispan2vspanset` both delegate to a single `permute` function [`orglinks.c:389-422`]:

```c
typevspanset *ispan2vspanset(typetask *taskptr, typeorgl orgl,
                              typeispan *ispanptr, typevspanset *vspansetptr)
{
    return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
}

typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl,
                                 typevspanset vspanptr, typeispanset *ispansetptr)
{
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

`permute` calls `span2spanset` → `retrieverestricted` on the **same orgl** regardless of whether the V-addresses are in the 1.x (text) or 2.x (link) range. There is no branch, no alternative lookup, no separate tree. The two ranges are just different regions of the same POOM.

---

### What the V→I Map Returns for the Link Subspace

When you call `vspanset2ispanset` with a V-span from the 2.x range, the POOM returns the I-address that was stored there by `docopy` during `docreatelink`. That I-address is the **link's ISA** — its tumbler address in the permascroll I-space (e.g. `1.1.0.1.0.1.0.2.1`). It is not a text-content address.

This is set up in `docreatelink` [`do1.c:207-212`]:

```c
createorglingranf (taskptr, granf, &hint, linkisaptr)   // assign link its ISA
&& tumbler2spanset (taskptr, linkisaptr, &ispanset)     // wrap ISA as ispan
&& findnextlinkvsa (taskptr, docisaptr, &linkvsa)       // next V in 2.x
&& docopy (taskptr, docisaptr, &linkvsa, ispanset)      // store ISA at that V
```

`docopy` → `insertpm` → `insertnd`: the link's ISA (I-address) is inserted into the document's POOM at V = 2.1, 2.2, … exactly as text I-addresses are inserted at V = 1.1, 1.2, ….

So yes, the V→I map for the link subspace **does** point into the permascroll I-space — but into the sub-range occupied by link orgls (ISAs of the form `*.0.2.*`), not text atoms.

---

### The Link Organizer Has Its Own Separate V-Space

Each link also has its own POOM (a "link orgl") — distinct from the document organizer. Within the link organizer's private V-space, the FROM/TO/THREE endpoints are stored at fixed local addresses set by `setlinkvsas` [`do2.c:169-183`]:

```c
// FROM endpoint at 1.1
tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);
tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);

// TO endpoint at 2.1
tumblerincrement (tovsaptr, 0, 2, tovsaptr);
tumblerincrement (tovsaptr, 1, 1, tovsaptr);

// THREE endpoint at 3.1
tumblerincrement (threevsaptr, 0, 3, threevsaptr);
tumblerincrement (threevsaptr, 1, 1, threevsaptr);
```

These are inserted into the link orgl (not the document orgl) via `insertendsetsinorgl` [`do2.c:130-148`], which calls `insertpm(taskptr, linkisaptr, link, fromvsa, fromsporglset)`. The I-addresses stored at 1.1, 2.1, 3.1 inside the link orgl are the I-addresses of the content that the link's endpoints point to.

---

### The Spanfilade Is a Separate Index (Not the V→I Map)

For link *search* (finding links from/to a given I-address), Udanax Green maintains a **second global enfilade** called `spanf`. This is a 2D B-tree indexed by `[link-ISA × content-I-address]`, written at link creation time by `insertendsetsinspanf` [`do2.c:116-128`] → `insertspanf` [`spanf1.c:15-54`]. It is not a V→I map — it is a reverse index from content identity to link identity. The dimensions used are named `ORGLRANGE` (link's ISA) and `SPANRANGE` (endpoint I-address).

---

### Summary of the Architecture

```
Document's POOM (single granf node):
  V = 1.x  →  I-addresses of text atoms in permascroll
  V = 2.x  →  I-addresses of link orgls (link ISAs)
                            ↓
                    Link Orgl's POOM (separate granf node):
                      V = 1.1  →  I-address of FROM content
                      V = 2.1  →  I-address of TO content
                      V = 3.1  →  I-address of THREE content

spanf (separate global 2D enfilade):
  [link-ISA × content-I-address]  — search index only, not a V→I map
```

**Answers to your specific questions:**

1. **Does the V→I map for the link subspace point into the link store's address space?** The POOM maps link-subspace V-addresses to the ISAs of link orgls, which live in the permascroll I-space — the same unified address space as text. There is no separate "link store" with its own I-space; links and text share the permascroll.

2. **Separate map or typed range within a unified arrangement?** A typed range within a unified arrangement. The `permute` / `retrieverestricted` machinery is identical for both subspaces. The V-address's first mantissa digit (1 vs. 2) is the only distinguishing marker — a convention enforced by callers, not by the enfilade structure itself.
