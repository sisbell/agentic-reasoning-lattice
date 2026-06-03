## Question 1 [evidence]

> In udanax-green, is there any operation other than the standard link-creation path (`findnextlinkvsa`) that seeds a document's first link-subspace V-position, and if so can it place that first link at a depth other than 2?

## KB Synthesis

Looking at this carefully across several KB entries.

**The standard seeding path**

`docreatelink` is the only operation that properly seeds the link subspace with link orgl ISAs. It calls `findnextlinkvsa`, which hardcodes the first link V-position as `2.1` by incrementing the tumbler through `2.0` → `2.1`. All subsequent links append at `vspanreach`. This is covered in [SS-LINK-SUBSPACE] and [ST-CREATE-LINK].

`setlinkvsas` (called within the same `docreatelink` path) also seeds the type-endpoint subspace at `3.x` for the link's THREE endpoint — a second subspace seeded by the same standard operation, but at digit `3`, not `2` [SS-SUBSPACE-CONVENTION / Finding 0038].

**Non-standard paths that can place content at 2.x**

Three operations bypass `findnextlinkvsa` entirely and can write to the link-subspace V-positions:

- **INSERT** — `acceptablevsa` always returns `TRUE`, so INSERT at V-position `2.1` with text content succeeds silently ([PRE-INSERT / Finding 0049], [PRE-ENF0-PLACEMENT-GAP]).
- **COPY/VCOPY** — `docopy` calls the same `acceptablevsa` stub and `insertpm`, placing whatever I-addresses the caller supplies at any V-position, including `2.x` ([PRE-VCOPY / Finding 0010]).
- **REARRANGE** — pivot cuts spanning the subspace boundary use `tumbleradd` with no digit-0 guard, moving previously text-subspace content into `2.x` ([PRE-REARRANGE / Finding 0051]).

None of these go through `findnextlinkvsa`. All produce semantically invalid states (text bytes or arbitrary I-addresses at link-subspace positions) because the subspace invariant is purely caller-enforced [INV-SUBSPACE-CONVENTION].

**Can the first digit be other than 2?**

Via non-standard paths, yes — content can be placed at any V-position. The standard `docreatelink` path is hardcoded to digit `2` (from endpoint) and digit `3` (type endpoint), with no runtime check preventing other placements. Through REARRANGE with cross-subspace cuts, a link orgl ISA already sitting at `2.x` could in principle be displaced to `1.x` or `3.x` ([EC-REARRANGE-CROSS-SUBSPACE]), though the result would violate [INV-SUBSPACE-CONVENTION] and corrupt retrieval semantics.

**Summary**

The only operation that properly seeds link-subspace positions is `docreatelink` via `findnextlinkvsa` (digit `2`) and `setlinkvsas` (digit `3` for type endpoints). INSERT, COPY, and REARRANGE can all write to `2.x` without `findnextlinkvsa`, but they do not create valid link orgl references — the storage layer has no type enforcement ([SS-SUBSPACE-CONVENTION / Finding 0010]).

---

## Code Exploration

I now have everything needed. Here is my full answer.

---

## Answer

### 1. The standard path: `findnextlinkvsa`

The function `findnextlinkvsa` [`do2.c:151-167`] is the dedicated entry point for computing the host-document link-subspace V-address during link creation. It has exactly two callers, both inside the link-creation layer:

- `domakelink` (2-endpoint) [`do1.c:184`]
- `docreatelink` (3-endpoint) [`do1.c:211`]

The first-link address it builds is always **depth 2**:

```c
// do2.c:156-158
tumblerclear (&firstlink);
tumblerincrement (&firstlink, 0, 2, &firstlink);   // mantissa[0] = 2
tumblerincrement (&firstlink, 1, 1, &firstlink);   // → 0.2.1
```

If the document has no prior content past 0.2.1, the new link lands at 0.2.1. If the document already has content reaching to or beyond 0.2.1, the new link is placed immediately after:

```c
// do2.c:160-165
(void) doretrievedocvspan (taskptr, docisaptr, &vspan);
tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
if (tumblercmp (&vspanreach, &firstlink) == LESS)
    movetumbler (&firstlink, vsaptr);
else
    movetumbler (&vspanreach, vsaptr);
```

The depth of the initial anchor (mantissa[0] = 2) is **hardcoded**; there is no parameter that changes it.

---

### 2. A second seeding path: the FEBE `copy` command

The FEBE `copy` operation [`fns.c:35-47`] calls `docopy` with a **client-supplied** V-address:

```c
// fns.c:41-44
if (
   getcopy (taskptr, &docisa, &vsa, &localspecset)
&& docopy (taskptr, &docisa, &vsa, localspecset))
    putcopy (taskptr);
```

Inside `docopy` [`do1.c:45-65`], the V-address is passed to `acceptablevsa` before the insert:

```c
// do1.c:53-60
return (
   specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
&& findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& acceptablevsa (vsaptr, docorgl)
...
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
```

`acceptablevsa` is:

```c
// do2.c:110-113
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

It is **a stub — unconditionally TRUE**. No depth, boundary, or range check is performed. The V-address is accepted regardless of its tumbler depth.

**Consequence:** a client can call the raw `copy` FEBE command with a V-address whose mantissa[0] is any value — 2, 3, 5, 100 — and `docopy` will place the supplied I-span content there without complaint. This independently seeds the link subspace (or any subspace) at any depth chosen by the client.

The `copy` path (`fns.c` → `docopy`) and the link-creation path (`domakelink`/`docreatelink` → `findnextlinkvsa` → `docopy`) both ultimately call `insertpm` [`orglinks.c:75`] with the V-address. The difference is that only link creation goes through `findnextlinkvsa` to compute the address; `copy` uses whatever address the client supplies.

---

### 3. `setlinkvsas` — link-document internal seeding at depths 1, 2, and 3

`setlinkvsas` [`do2.c:169-183`], called from both `domakelink` [`do1.c:189`] and `docreatelink` [`do1.c:217`], seeds fixed V-addresses *within the link document's own POOM* — not in the host document:

```c
// do2.c:171-181
tumblerclear (fromvsaptr);
tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);   // 0.1.1  (depth 1 — text subspace)
tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);

tumblerclear (tovsaptr);
tumblerincrement (tovsaptr, 0, 2, tovsaptr);       // 0.2.1  (depth 2 — link subspace)
tumblerincrement (tovsaptr, 1, 1, tovsaptr);

if (threevsaptr) {
    tumblerclear (threevsaptr);
    tumblerincrement (threevsaptr, 0, 3, threevsaptr); // 0.3.1 (depth 3 — link subspace)
    tumblerincrement (threevsaptr, 1, 1, threevsaptr);
}
```

These addresses are used in `insertendsetsinorgl` [`do2.c:130-147`] → `insertpm` to store the endpoint sporgl-sets inside the link's own ORGL. The link document's from-endpoint lives at depth 1 (text subspace), to-endpoint at depth 2 (link subspace), and three-endpoint — when present — at depth **3**.

This is seeding the link document's own V-structure, not the host document's link subspace. But it is worth noting that within the link document, `setlinkvsas` places the three-endpoint at a depth-3 position — a different depth than the depth-2 used by `findnextlinkvsa` for the host document.

---

### Summary

| Path | Document targeted | Depth of first link position |
|------|------------------|------------------------------|
| `findnextlinkvsa` [`do2.c:157`] | host document | always 2 (hardcoded) |
| FEBE `copy` via `acceptablevsa` stub [`do2.c:110-113`] | any document | **any depth** (no validation) |
| `setlinkvsas` (to-endpoint) [`do2.c:174-176`] | link document internal | always 2 |
| `setlinkvsas` (three-endpoint) [`do2.c:178-180`] | link document internal | always 3 |

**Answers to the original questions:**

1. **Yes**, there is another path besides `findnextlinkvsa` that can seed a link-subspace V-position: the FEBE `copy` command, because `acceptablevsa` is an unconditional stub and places no constraint on the supplied V-address.

2. **Yes**, that second path (`copy`) can place content at a depth other than 2 — the depth is chosen entirely by the caller. `findnextlinkvsa` itself is incapable of producing a first-link depth other than 2; its anchor is hardcoded to mantissa[0] = 2 at `do2.c:157`.

Additionally, within the link document's own structure, `setlinkvsas` seeds the three-endpoint at depth 3 (`do2.c:179`), which is part of the standard link-creation path but targets a different document.
