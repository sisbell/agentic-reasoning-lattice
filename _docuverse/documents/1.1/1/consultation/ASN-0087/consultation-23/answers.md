# Revision Consultation — ASN-0063

**Review:** review-23.md
**Date:** 2026-03-22 02:58

## Summary

3 REVISE items analyzed: 2 internal, 1 consulted (1 nelson, 1 gregory)

## Consultation Results

### Issue 2: K.μ⁺_L permits foreign link placement without justification

**Category:** BOTH
**Reason:** None

**Nelson question:** Was link transclusion — placing a link owned by another document into your own document's arrangement, analogous to content transclusion — an intended feature of the design, or should a document's link subspace contain only links it originated?

**Nelson's Answer:**

## Answer: Link Transclusion Was Not Part of the Design

A document's link subspace should contain only links it originated. The evidence is definitive, coming from an explicit statement, architectural asymmetry, and the absence of any mechanism for link transclusion.

### The Explicit Statement

Nelson states directly:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

This is unambiguous. A document's link collection is exactly the set of links created in that document — no more.

### The Byte/Link Asymmetry

Transclusion is defined exclusively for the byte stream. Nelson says:

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

There is no parallel statement for links. The "virtual byte stream" is explicitly about bytes. Links occupy a separate subspace with fundamentally different properties:

| Property | Bytes (1.x subspace) | Links (2.x subspace) |
|----------|---------------------|----------------------|
| Arrangement | Virtual (rearrangeable) | Permanent creation order |
| Transclusion | Yes — "may include bytes from any other document" | No — "only the links of which it is the home document" |
| Addressing | V-stream positions (shift with edits) | Sequential by arrival (never renumber) |

### No Operation Supports It

The FEBE protocol has no mechanism for link transclusion:

- **COPY** places material at a `doc vsa` — a V-stream address, which is a byte-subspace position. It operates on the byte stream, not the link subspace.
- **MAKELINK** creates a *new* link in a specified document. It does not reference or include an existing link.
- **REARRANGE** transposes regions of text. Links are explicitly excluded from rearrangement — they maintain "permanent order of arrival."

There is no "copy link from document A into document B's arrangement" operation.

### Ownership Demands It

The link ownership principle would be violated by transclusion:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

Home document determines ownership. If you could transclude someone else's link into your document's arrangement, it would create an ambiguity: is it still owned by the original home document, or has it become part of yours? Nelson avoids this by making the boundary absolute — a document contains only its own links.

### The Design Provides Alternatives

Rather than transcluding links, the architecture offers three mechanisms that achieve the desired effects:

1. **Link search across transclusions.** When you transclude bytes from another document, `FINDLINKSFROMTOTHREE` discovers all links attached to those bytes — regardless of which document houses the links. You don't need to transclude the links because the bidirectional search finds them automatically.

2. **Create your own links.** If you want a link with similar semantics, create one in your document. Your link, your ownership, your address. This is the natural analog of "making your own annotations."

3. **Link-to-link.** If you want to reference someone else's specific link — not replicate its function, but comment on or group it:

   > "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link." [LM 4/49]

### Why This Is Elegant

Content flows; connections stay put. When Alice transcludes Bob's text, she sees Bob's words in her arrangement. Bob's links to those words are discoverable through search. But Bob's links remain Bob's property at Bob's address. Alice's link subspace contains only links she created.

This preserves the core ownership invariant while still allowing the full web of connections to be visible. The system doesn't need link transclusion because the bidirectional link search mechanism already makes all relevant links discoverable from any vantage point.

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

The search mechanism is designed to efficiently find relevant links across the entire docuverse. Transcluding links would be redundant with this capability and would compromise the clean separation between content arrangement (Vstream, mutable) and link ownership (home document, permanent).

**Gregory question:** Does the udanax-green implementation enforce that a document's link subspace contains only links whose origin matches the document, or does it permit placing foreign-origin links in a document's arrangement?

**Gregory's Answer:**

## KB Synthesis

No, the implementation does not enforce this. The answer is entirely convention, not enforcement.

**What the normal creation path does**

`CREATELINK(home_doc, ...)` allocates the link orgl under `home_doc`'s address space and places the orgl ISA into `home_doc`'s V-position `2.x` via `docopy()` [ST-CREATE-LINK]. Under the allocation rules [SS-ADDRESS-ALLOC], a link's ISA is `home_doc.0.2.N`, making its ancestry explicit. So by construction, a freshly-created link's POOM entry lives in the home document.

**Why enforcement is absent**

The validation stub `acceptablevsa()` in `do2.c:110-113` unconditionally returns `TRUE` [SS-SUBSPACE-CONVENTION, PRE-INSERT, PRE-VCOPY]. The `docopy()` function that actually places I-addresses into a document's POOM performs no type checking and no origin checking. Any I-address — including a link orgl ISA belonging to a foreign document — can be written to any V-position in any document [SS-DUAL-ENFILADE Finding 0011].

**Practical consequence**

A foreign link orgl ISA from document B could be copied into document A's `2.x` subspace via `docopy()` or `VCOPY`, and the backend would accept it silently [PRE-VCOPY]. There is no guard of the form `requires origin(link_isa) == home_doc`. The subspace invariant (`2.x` contains only link orgls homed to this document) is unenforced at every layer.

**What does exist**

The only thing that is enforced is the *address structure*: link ISAs are allocated under their home document's address prefix (via `findisatoinsertmolecule` with a document-scoped bound) [SS-ADDRESS-SPACE Finding 0065]. This makes the home document *derivable* from the ISA by address inspection, but nothing prevents the ISA from being placed in a different document's POOM.

In summary: home-document origin is a structural property of the link's I-address, but there is no runtime enforcement that the document whose 2.x subspace references a link orgl is the same document the ISA is homed under [INV-SUBSPACE-CONVENTION, PRE-ENF0-PLACEMENT-GAP].

---

## Code Exploration

Now I have everything I need. Here is the complete answer.

---

## Does udanax-green enforce that a document's link subspace contains only links whose origin matches the document?

**Short answer: No. The implementation relies on procedural encapsulation, not runtime enforcement. There is no guard that checks link origin when placing into a document's arrangement.**

---

### The `createlink` flow — structural guarantee by construction

`docreatelink` in `do1.c:195-221` is the only entry point for link creation. Its steps establish origin matching **by construction**, not by validation:

**Step 1 — Allocate the link ISA as a structural child of the document** (`do1.c:207-209`):

```c
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
…
createorglingranf (taskptr, granf, &hint, linkisaptr)
```

This routes into `createorglgr` → `findisatoinsertgr` → `findisatoinsertmolecule` (`granf2.c:158-181`). For `LINKATOM`, that function first confirms the document exists in the granfilade (`granf2.c:136` calls `isaexistsgr(fullcrumptr, &hintptr->hintisa)`), then derives the new link ISA from the document's tumbler:

```c
tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);  // granf2.c:171
```

The resulting `linkisaptr` is numerically subordinate to `docisaptr` — its tumbler shares `docisaptr`'s prefix, extended by two components. This makes the link's I-space address structurally "owned by" the document.

**Step 2 — Place the link ISA into the document's link subspace** (`do1.c:211-212`):

```c
findnextlinkvsa (taskptr, docisaptr, &linkvsa)
&& docopy (taskptr, docisaptr, &linkvsa, ispanset)
```

`findnextlinkvsa` (`do2.c:151-167`) computes the next available V-address for a link inside `docisaptr`'s arrangement. It builds `firstlink` as a tumbler in the link subspace (components `0.2.1`, which is a V-address `< 1.0`), then returns either `firstlink` or the current vspan reach + 1, whichever is later.

The link subspace is identified structurally in `islinkcrum` (`orglinks.c:255-261`):

```c
bool islinkcrum(typecorecrum *crumptr)
{
    if(crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0){
        return TRUE;
    }
    return FALSE;
}
```

This is purely a positional test on the V-dimension displacement — no ISA prefix check.

---

### Where enforcement would live — and why it doesn't

The natural place to enforce origin would be `acceptablevsa`, called by `docopy` to validate the target virtual address. It is a complete stub:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);    // do2.c:110-113
}
```

`docopy` itself (`do1.c:45-65`) calls `findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)` — which only checks that `docisaptr` is **write-open** in the BERT table (`bert.c:52-87`). It does not inspect the `ispanset` content being inserted to verify it belongs to `docisaptr`.

---

### The `copy` FEBE command provides no protection either

The FEBE `copy` command (`fns.c:35-47`) calls:

```c
docopy (taskptr, &docisa, &vsa, localspecset)
```

There is nothing in `docopy`, `acceptablevsa`, or any downstream function that validates whether:
- The V-address `vsa` is in the text subspace vs. the link subspace  
- The `localspecset` content has any ISA relationship to `docisa`

A client that could construct a `copy` request with a V-address in the link subspace (`< 1.0`) and a specset referencing a foreign document's link ISA would succeed — the backend would silently place a foreign-origin link reference into the target document's link subspace arrangement.

---

### Summary of the enforcement model

| Mechanism | What it checks | Enforces origin? |
|---|---|---|
| `makehint` + `createorglingranf` | Creates link ISA structurally under `docisaptr` | Yes — but only for the normal `createlink` flow |
| `findnextlinkvsa` | Finds next V-address in link subspace | No origin check |
| `acceptablevsa` (`do2.c:110`) | Stub, always `TRUE` | **No enforcement** |
| `findorgl` with `WRITEBERT` | Document is write-open | Access control only |
| `islinkcrum` (`orglinks.c:255`) | V-address position only | No origin check |
| `docopy` | Access + stub validity | **No origin enforcement** |

The implementation achieves correctness through **procedural atomicity**: `docreatelink` both allocates the link's ISA (deriving it from `docisaptr`) and places it in the document in one operation. There is no separate "place existing link into document" operation exposed at the FEBE level — and therefore no need for a runtime guard. But the guard does not exist; the backend would not refuse a foreign-origin link if one were placed via `docopy`.
