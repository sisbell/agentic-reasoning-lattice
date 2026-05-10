# Revision Consultation — ASN-0043

**Review:** review-1.md
**Date:** 2026-03-16 21:35

## Summary

6 REVISE items analyzed: 5 internal, 1 consulted (1 nelson, 1 gregory)

## Consultation Results

### Issue 1: Link value immutability is unaddressed

**Category:** BOTH
**Reason:** Whether link endsets are immutable after creation is a design intent question (Nelson) and requires checking whether any code path modifies a link's endsets post-creation (Gregory).

**Nelson question:** After a link is created via MAKELINK, can its endsets (from, to, type) be modified, or is the link value permanently fixed like content under S0?

**Nelson's Answer:**

## Links Are Immutable Once Created

A link's endsets (from, to, type) are **permanently fixed** at creation time. There is no FEBE operation to modify them.

### Evidence from the Protocol

The 17 FEBE commands in XU.87.1 include exactly five link operations:

| Operation | Purpose |
|-----------|---------|
| MAKELINK | Create a link |
| FINDLINKSFROMTOTHREE | Search links |
| FINDNUMOFLINKSFROMTOTHREE | Count matching links |
| FINDNEXTNLINKSFROMTOTHREE | Paginate results |
| RETRIEVEENDSETS | Read endsets |

There is no MODIFYLINK, UPDATELINK, or EDITENDSETS. The only write operation is creation; the rest are read/search.

### Evidence from the Storage Model

Links are I-space entities. I-space is immutable:

> "Content at an I-space address **never changes**." (4/11 via I-space concept)

The entire storage paradigm is append-only:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." (2/14) — Nelson rejects this for Xanadu.

Links have permanent creation-order addresses that never change:

> "The links designated by a tumbler address are in their **permanent order of arrival**." (4/31)

### The Link Lifecycle

A link has exactly two states:

1. **Active** — created via MAKELINK, discoverable via search
2. **Deleted** — "not currently addressable, awaiting historical backtrack functions, may remain included in other versions" (4/9)

Deletion is V-space removal, not I-space destruction — identical to how content deletion works. The deleted link still exists in I-space and in previous versions.

### How to "Change" a Link

To effectively modify a link, the owner would:
1. Delete the old link (V-space removal)
2. Create a new link via MAKELINK with the desired endsets

The old link persists in I-space and historical versions. The new link gets a fresh address in creation order. This is consistent with Nelson's model where nothing is overwritten — you accumulate new state.

### Why This Makes Sense

Link immutability is a direct consequence of the same principle that makes content immutable: **others may have linked to it**. Since links are first-class objects with tumbler addresses, other links can point to them (link-to-link, 4/49-4/51). Modifying a link's endsets after creation would silently change the meaning of every meta-link pointing to it — violating the non-destruction guarantee.

**Gregory question:** Does the udanax-green implementation provide any operation that modifies a link's endsets after creation, or are link values write-once like content bytes?

**Gregory's Answer:**

## KB Synthesis

Links are write-once. No operation in udanax-green modifies a link's endsets after creation.

## Evidence

**Link orgls are permanent in I-space.** [SS-THREE-LAYER-MODEL] (Finding 0040) establishes three independent layers: the link orgl at a permanent I-address (layer 1), spanfilade DOCISPAN entries (layer 2), and the document POOM V-stream entry (layer 3). `CREATELINK` writes all three. No subsequent operation modifies layer 1. The comment is explicit: "Cannot be deleted (permanence axiom P0)."

**Endpoint V-spans are fixed at creation time.** [SS-LINK-ENDPOINT] Finding 0028 states directly: "Link endpoints are immutable V-spans fixed at creation time... These endpoint references never change after link creation." The link stores `{ source: VSpan, target: VSpan, type: Tumbler }` and this record is written once into the link orgl.

**No MODIFYLINK or DELETELINK opcode exists.** [INV-LINK-PERMANENCE] (Finding 0024) confirms: "There is no DELETELINK operation in the FEBE protocol." The KB contains no mention of any modify-link command in the request dispatch table documented in Finding 0042.

**What CAN change is the POOM representation, not the link itself.** `DELETEVSPAN(2.x)` removes the link's entry from a document's POOM [FC-LINK-DELETE-ISOLATION], but this severs the document's reference — it leaves the link orgl, its endsets, and the spanfilade entries entirely intact. [EC-REVERSE-ORPHAN] documents exactly this asymmetry: the link remains discoverable and followable even after POOM removal.

**The link is content-identity-indexed, not position-indexed.** [SS-LINK-ENDPOINT] Finding 0019 clarifies that endsets are *dynamic* in their V-address reporting (they reflect current positions after edits), but this is a computed view derived from the POOM at query time — not a mutation of the stored endset I-spans. The underlying sporgls in the link orgl are unchanged; only the I→V conversion result varies with document state.

**Analogy to content bytes holds.** [INV-CONTENT-IMMUTABILITY] establishes that content identities are never modified or destroyed. Links share this property at the granfilade level: the link orgl is written once by `createorglingranf` and never touched again. The granfilade is append-only [FC-GRANF-ON-DELETE], and link orgls are entries in that same structure.

## Summary

| Layer | Mutable? | Who modifies it |
|-------|----------|-----------------|
| Link orgl (I-space) | **No** — write-once | Only `CREATELINK` |
| Spanfilade endset index | **No** — append-only | Only `CREATELINK` |
| Document POOM (2.x entry) | **Yes** | `DELETEVSPAN(2.x)` |

The endsets stored in the link orgl are fixed at creation. The V-address rendering of those endsets changes as documents are edited (because I→V conversion consults current POOM state), but that is a query-time derivation, not a mutation of the link object itself.

---

## Code Exploration

## Answer: Links Are Write-Once in udanax-green

**Links are immutable after creation. No operation exists to modify a link's endsets.**

---

### Link Creation: `docreatelink()` in `do1.c:195–221`

The only write path for link endsets runs during creation:

1. A new link ISA is allocated via `createorglingranf()` [`do1.c:209`]
2. The link content is copied into the document via `docopy()` [`do1.c:212`]
3. Endsets are stored in the orgl via `insertendsetsinorgl()` [`do2.c:130`]
4. Endsets are stored in the spanfilade via `insertendsetsinspanf()` [`do2.c:116`]

The helper `setlinkvsas()` [`do2.c:169–183`] assigns the three endset VSAs (V-stream addresses 1.1, 2.1, 3.1) as local temporaries during creation only.

---

### All FEBE Link Handlers in `requests.h:1–46`

| Code | Handler | Defined in `fns.c` | Operation |
|------|---------|---------------------|-----------|
| 27 | `CREATELINK` | line 100 | **Write** (one time only) |
| 18 | `FOLLOWLINK` | line 114 | Read |
| 28 | `RETRIEVEENDSETS` | line 350 | Read |
| 29 | `FINDNUMOFLINKSFROMTOTHREE` | line 204 | Read |
| 30 | `FINDLINKSFROMTOTHREE` | line 189 | Read |
| 31 | `FINDNEXTNLINKSFROMTOTHREE` | line 219 | Read |

There is no `SETLINK`, `MODIFYLINK`, `CHANGELINK`, or `DELETELINK` handler — not as an unimplemented stub, not commented out, not anywhere. The handler table is the complete enumeration of supported operations.

---

### Endset Storage Is Not Revisited

`insertendsetsinorgl()` [`do2.c:130`] and `insertendsetsinspanf()` [`do2.c:116`] are called **exclusively from `docreatelink()`** [`do1.c:209–219`]. No other code path calls them. After creation, link data in the granfilade and spanfilade is only ever read — via `dofollowlink()` [`do1.c:223`], `doretrieveendsets()` [`do1.c:369`], and the `dofind*` family [`do1.c:348–362`].

---

### Link Data Structures Confirm Immutability

`typelink` is a `typedef` for `typeaddress` [`xanadu.h:106`, `xanadu.h:98–102`]:

```c
typedef struct structtypeaddress {
    struct structtypeaddress *next;
    typeitemid  itemid;
    typeisa     address;
} typeaddress;
```

This is an identity/address record only. The actual endset content lives in the enfilade structures. There is no "dirty" flag, no revision counter, no update API surface at any layer.

---

### Verdict

**Link endsets are write-once.** The design is consistent with Xanadu's immutability principle: a link is a permanent structural relationship between document fragments. The implementation enforces this not by access control but by simply providing no mutation operations — creation writes endsets into the enfilade, and every subsequent operation is a query.
