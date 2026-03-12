## Question 12 [gregory]

> The type endset references I-addresses at `1.0.2.x` in the global type namespace — what types were defined or envisioned, and does the type endset point to actual stored content in the granfilade (like a type name string) or to a conventionally assigned address?

## KB Synthesis

The KB has partial answers here — let me synthesize what's known and flag the gap.

## What Types Were Defined

From [SS-LINK-ENDPOINT] Finding 0024, the known type registry in the bootstrap document (doc 1) at `1.0.2.x`:

| Type     | Address     | Notes |
|----------|-------------|-------|
| JUMP     | `1.0.2.2`   | — |
| QUOTE    | `1.0.2.3`   | — |
| FOOTNOTE | `1.0.2.6`   | Parent of MARGIN |
| MARGIN   | `1.0.2.6.2` | Subtype of FOOTNOTE via containment |

The hierarchy is structural: MARGIN is a subtype of FOOTNOTE because `1.0.2.6.2` is contained within the tumbler range `1.0.2.6.*`, enabling range-match queries like "find all footnote-family links" [SS-LINK-ENDPOINT / Finding 0024].

## Content vs. Conventional Address

The KB is explicit that these are VSpec references that "participate in the same address/identity system as all other content" and are "content references, not metadata" [SS-LINK-ENDPOINT Finding 0024]. However, **the KB does not have a finding that confirms what is actually stored at those granfilade addresses** — whether there are actual content bytes (e.g., type name strings like "jump") or whether the addresses serve purely as identity tokens with no associated bytes.

What the KB does establish:

- The `link.type` field is a VSpec pointing into the bootstrap document's `1.0.2.*` subspace
- `QUOTE_TYPE` and `MARGIN_TYPE` are constructed in `febe/client.py` as VSpec objects referencing the bootstrap document [SS-LINK-ENDPOINT Finding 0024]
- Type endpoints occupy V-subspace `3.x` internally (`setlinkvsas()` increments digit 0 to 3 for type endpoints) [SS-SUBSPACE-CONVENTION Finding 0038]
- Type queries via address-range matching would work if type ISAs are indexed in the spanfilade — but whether bootstrap type addresses have DOCISPAN entries is not confirmed

## The Honest Answer

The design intent is clear: types are content-addressed objects in the bootstrap document, enabling type-based queries through the same I-address intersection mechanism used for source/target endpoint search. The tumbler containment hierarchy gives you subtype queries "for free" through range filtering.

Whether the bootstrap document actually contains readable text at those addresses (e.g., strings describing the link types) or just minimal placeholder content with assigned addresses — **the KB does not have a finding that resolves this**. This would require examining what `doinsert` (or equivalent bootstrapping code) places at `1.0.2.x` during system initialization.

---

## Code Exploration

Now I have everything I need. Let me compile the full answer.

---

## The Type Endset and `1.0.2.x` Addresses

### What the "Three Set" Is

When `docreatelink` is called [`do1.c:195`], it accepts a `threespecset` — the type endset — alongside the from/to specsets:

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr,
    typespecset fromspecset, typespecset tospecset,
    typespecset threespecset, typeisa *linkisaptr)
```

All three endsets are stored in two places:
1. **In the link's own POOM (orgl)** via `insertendsetsinorgl` [`do1.c:218`], at fixed V-positions assigned by `setlinkvsas`
2. **In the global spanfilade** via `insertendsetsinspanf` [`do1.c:219`], tagged with span type `LINKTHREESPAN=3` [`xanadu.h:38`]

`setlinkvsas` assigns positions within the link's POOM [`do2.c:169-183`]:
```c
// from endset → position 0.1
// to   endset → position 0.2
// three (type) endset → position 0.3
tumblerincrement (threevsaptr, 0, 3, threevsaptr);
tumblerincrement (threevsaptr, 1, 1, threevsaptr);
```

These are positions within the **link's own orgl**, not the home document's address space.

---

### How the Type Specset Is Converted to Storage

`specset2sporglset` [`sporgl.c:14-33`] converts a VSpec to a sporgl (span + origin reference). For a type VSpec pointing to `LINK_TYPES_DOC` at V-span `1.0.2.X`:

```c
// sporgl.c:44-57
if (!findorgl (taskptr, granf, docisa, &orgl, type))
    return (NULL);   // ← if types doc doesn't exist, fails here
for (; vspanset; vspanset = vspanset->next) {
    vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);
    // creates sporgl: {sporgladdress=docisa, sporglorigin=ispanset->stream, ...}
}
```

Then `insertendsetsinspanf` has an explicit NULL guard on the type set [`do2.c:122-126`]:
```c
if (threesporglset) {
    if(!insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN))
        return (FALSE);
}
```

If `threesporglset` is NULL (because the types document doesn't exist or has no content at the target V-address), the `LINKTHREESPAN` entry is simply **never written to the spanfilade**. The link is stored without type information, silently.

---

### What Is `LINK_TYPES_DOC` and `1.0.2.X`?

From `client.py:597-612`:

```python
# Link type addresses - types are in document 1's link subspace (0.2)
# Full address format: 1.1.0.1.0.1.0.2.X where X is the type number
LINK_TYPES_DOC = Address(1, 1, 0, 1, 0, 1)  # Document 1 (bootstrap doc)

# Type numbers from the registry (link-types-relationship.md):
#   2.2 = jump, 2.3 = quote, 2.6 = footnote, 2.6.2 = footnote.margin
# Local address within doc: version.0.link_subspace.type = 1.0.2.X
JUMP_TYPE     = VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 2), Offset(0, 1))])
QUOTE_TYPE    = VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 3), Offset(0, 1))])
FOOTNOTE_TYPE = VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 6), Offset(0, 1))])
MARGIN_TYPE   = VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 6, 2), Offset(0, 1))])
```

`1.0.2.X` is a **V-space address** within document `1.1.0.1.0.1`, structured as `version.0.link_subspace.type_number`. It is *not* a global I-address in the granfilade. The document's internal V-space is organized with link atoms in the `0.x` range and text in the `1.x` range [`finding 0009`], so `0.2.X` targets specific link positions within the link subspace.

The type assignments come from a non-existent `resources/link-registry/link-types-relationship.md` file referenced in the comment. The numbering (jump=2, quote=3, footnote=6, footnote.margin=6.2) is inherited from the original Xanadu specification/Literary Machines taxonomy. The non-contiguous gaps (1 unused, 4 and 5 skipped before footnote at 6) suggest the original registry had more types or reserved slots.

---

### Does the Granfilade Store Actual Content at Those Addresses?

**No, and there is no bootstrapping code to create it.**

`init.c` contains only function-dispatch initialization [`init.c:25-78`]. No document is created, no content is inserted. `be.c:37` establishes only the default account tumbler:
```c
tumbler defaultaccount = {0,0,0,0, 1,1,0,1,0,0,0,0}; /* 1.1.0.1 */
```

For the type sporgl to resolve to anything, `LINK_TYPES_DOC = 1.1.0.1.0.1` would need to exist in the granfilade with content at V-positions `1.0.2.2`, `1.0.2.3`, etc. From the granfilade's address allocation logic [`granf2.c:158-181`], link atoms within document `D` are allocated at I-addresses `D.0.2.1`, `D.0.2.2`, ..., but only when explicitly created by client operations. None of this is pre-loaded.

As a result, in every session tested by this harness:
- `findorgl(granf, LINK_TYPES_DOC, ...)` returns NULL (document was never opened)
- `specset2sporglset` returns NULL for the type specset
- `threesporglset` is NULL
- The `if (threesporglset)` guard at `do2.c:122` is never taken
- All links are effectively **untyped from the backend's perspective**

This was first discovered as Bug 0005 (malformed type addresses), and the current client.py represents the *corrected* convention — but the backend is still never given a bootstrapped types document, so the corrected addresses still resolve to nothing.

---

### Intended Design vs. Actual Implementation

| Question | Answer | Source |
|----------|--------|--------|
| Are `1.0.2.x` hardcoded in C? | No — no constants, no special handling | `init.c`, `be.c`, `granf2.c` |
| What are `1.0.2.x`? | V-space addresses within a designated "types document" | `client.py:604` |
| What types were envisioned? | jump (2), quote (3), footnote (6), footnote.margin (6.2) | `client.py:605-608` |
| Does granfilade store type content? | No — never bootstrapped | `init.c:25-78` |
| What happens when type doc is missing? | Sporgl resolves to NULL; LINKTHREESPAN silently omitted | `sporgl.c:44`, `do2.c:122` |
| Where type content *would* live | As link atoms at `1.1.0.1.0.1.0.2.1`, `.0.2.2`, ... in granfilade | `granf2.c:170-175` |

In the intended design, the types document would be a bootstrapped "type registry" — a real document whose link atoms at specific V-positions define each type. The type endset would then be a sporgl that captures the I-address of a specific type-atom, enabling type-based link queries through `findlinksfromtothreesp` [`spanf1.c:92-98`] via the spanfilade. Instead, the convention exists only as client-side constants pointing to a document that was never created.
