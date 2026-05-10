## Question 13 [gregory]

> If document A transcludes content from document B, and document C then transcludes that same content from document A, do all three documents' POOMs point to the original I-addresses from B's initial creation — i.e., is transclusion identity preserved transitively through arbitrary copy chains?

## KB Synthesis

Yes — transclusion identity is preserved transitively through arbitrary copy chains, and all three POOMs point to B's original I-addresses. Here is how the KB entries support this:

## The Mechanism: VCOPY shares, never allocates

When B inserts content, `inserttextingranf` allocates fresh I-addresses α in the granfilade [SS-ADDRESS-SPACE, Finding 0033]. Those I-addresses are permanent [INV-IADDR-IMMUTABILITY].

When A transcludes from B via VCOPY, the call chain is:

```
docopy → specset2ispanset → insertpm
```

`specset2ispanset` reads B's POOM to extract the I-addresses (α) currently mapped there. `insertpm` places those same α into A's POOM without calling `inserttextingranf` [ST-VCOPY, Finding 0046]. No new I-addresses are allocated.

When C transcludes from A, the identical mechanism runs: `specset2ispanset` reads A's POOM, finds α there (because VCOPY placed them there), and `insertpm` writes α into C's POOM.

The sporgl is the carrier that preserves identity through each hop — it packages `(origin: IAddress, width, source_doc)` and passes the origin I-address through unchanged [INT-SPORGL-TRANSCLUSION, SS-SPORGL].

## The Invariant

This is stated directly in [INV-TRANSITIVE-IDENTITY, Finding 0018]:

> Content identity flows transitively through transclusion chains. If A transcludes from B, and B transcludes from C, then A and C share content identity for the transcluded portion — even though A never directly referenced C.

The concrete example:
```
C: "ABCDEFGHIJ"
B: vcopies all of C              → B's POOM maps to C's I-addresses
A: vcopies "DEFGH" from B       → A's POOM maps to C's original I-addresses

compare_versions(A, C) → "DEFGH" shared
find_documents("DEF" from C) → [A, B, C]
```

## Why it cannot fail

Two structural facts preclude identity loss at any hop:

1. **VCOPY never creates new I-addresses.** The only operation that allocates fresh I-addresses is `inserttextingranf`, called only by INSERT [ST-INSERT, Finding 0036]. VCOPY goes through `docopy` → `insertpm`, which writes existing I-addresses into the destination POOM [PRE-COPY, Finding 0046].

2. **I-addresses in the granfilade are immutable and permanent.** DELETE removes POOM mappings but leaves the granfilade untouched [FC-GRANF-ON-DELETE]. No operation can change what content an I-address refers to [INV-IADDR-IMMUTABILITY].

## Depth limit?

The KB records no depth limit on this transitivity for transclusion chains. (There is a separate Bug 0012 crash for deep *version* chains in `compare_versions`, but that is a different operation [EC-COMPARE-VERSIONS-LINK-CRASH, Finding 0018].) For pure transclusion, INV-TRANSITIVE-IDENTITY is stated unconditionally, and the mechanism is purely structural — each hop is identical.

**Summary:** After B→A→C, all three documents' POOMs contain mappings to B's original I-addresses. `compare_versions(B, C)` reports shared content; `find_documents` returns all three from a search against any of those I-addresses. The chain can extend to arbitrary depth without loss.

---

## Code Exploration

Now I have everything I need to trace the complete execution path. Here is my full answer.

---

## Transclusion Identity Through Copy Chains: Is It Preserved Transitively?

**Answer: Yes.** All three documents' POOMs point to the same original I-addresses from B's initial creation, and this holds through arbitrarily deep copy chains. Here is the full proof from source.

---

### Step 1: Original content creation in B

When text is first inserted into B (`doinsert`, `do1.c:87-123`):

```c
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy (taskptr, docisaptr, vsaptr, ispanset)
```

`inserttextingranf` calls `inserttextgr` (`granf2.c:83-109`), which:
1. Allocates a new permanent I-address via `findisatoinsertgr` → `findisatoinsertmolecule` (`granf2.c:158-181`)
2. Stores text bytes at that I-address in the granfilade
3. Returns `ispanset` — a `typeispan` with `stream = lsa` (the freshly-allocated permanent I-address) and `width = textlength`

Then `docopy(taskptr, docisaptr, vsaptr, ispanset)` is called with those I-spans.

Inside `docopy` (`do1.c:53-64`):
```c
specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
...
insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
```

`specset2ispanset` (`do2.c:24-26`) detects `itemid == ISPANID` and passes the I-spans through unchanged:
```c
if (((typeitemheader *)specset)->itemid == ISPANID) {
    *ispansetptr = (typeispanset)specset;
```

`insertpm` (`orglinks.c:100-131`) then installs the crum in B's POOM:
```c
unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
movetumbler (&lstream, &crumorigin.dsas[I]);   // I = original granfilade address
movetumbler (vsaptr, &crumorigin.dsas[V]);      // V = position in B
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
```

**Result**: B's POOM contains a crum mapping `V-address in B → original I-address in granfilade`.

---

### Step 2: A copies from B (FEBE `copy` command)

The client sends `copy(docisa=A, vsa=Y, specset=[B at V=X..X+n])`.

`copy` in `fns.c:41-46` routes to `docopy(taskptr, &docisa_A, &vsa_Y, specset)` where `specset` is a `VSPECID` pointing into B's V-space.

In `docopy`, `specset2ispanset` hits the `VSPECID` branch (`do2.c:27-38`):
```c
findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
&& (ispansetptr = vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr))
```

`docorgl` is **B's POOM**. `vspanset2ispanset` (`orglinks.c:397-402`) calls:
```c
return permute(taskptr, orgl, ispanptr, V, ispansetptr, I);
```

`permute` (`orglinks.c:404-422`) → `span2spanset` → `retrieverestricted(orgl, span, V, NULL, I, NULL)` (`retrie.c:56-85`). This walks B's POOM looking for crums whose V-dimension intersects the requested V-span, then for each matching crum calls `context2span(c, restriction, V, &foundspan, I)` (`context.c:176-212`):

```c
/* idx1=V (restriction), idx2=I (target) */
movetumbler (&grasp.dsas[idx2], &foundspanptr->stream);
tumblersub(&reach.dsas[idx2],&grasp.dsas[idx2],&foundspanptr->width);
foundspanptr->itemid = index2itemid (idx2, context);   // → ISPANID
```

`grasp.dsas[I]` and `reach.dsas[I]` come from the POOM crum's stored I-coordinates — the **exact same I-addresses from B's original creation**. These form the returned `ispanset`.

`insertpm` then stores these I-addresses into **A's POOM** at new V-addresses from `vsa_Y` (`orglinks.c:105,113`):
```c
movetumbler (&lstream, &crumorigin.dsas[I]);  // = original I-address from B
movetumbler (vsaptr, &crumorigin.dsas[V]);    // = new V-position in A
```

**Result**: A's POOM crum has `cdsp.dsas[I]` = the original I-address from B's creation.

---

### Step 3: C copies from A (second hop)

Identical machinery. The client sends `copy(docisa=C, vsa=Z, specset=[A at V=Y..Y+n])`.

`specset2ispanset` finds `docorgl` = **A's POOM** and calls `vspanset2ispanset` with A's POOM. The permutation walks A's POOM, whose crums already have `cdsp.dsas[I]` = original I-addresses from B. `context2span` extracts those same I-coordinates and returns them as I-spans.

`insertpm` stores them in **C's POOM** at yet another V-position — but the same original I-addresses.

**Result**: C's POOM crum has `cdsp.dsas[I]` = the original I-address from B's creation.

---

### Why This Is Structurally Inevitable

The POOM is a 2D enfilade that maps V↔I. The V→I permutation (`vspanset2ispanset` → `permute` → `context2span`) **reads I-coordinates out of existing POOM crums**. It never consults the granfilade during a copy — it only consults the source document's POOM. Since copying writes those same extracted I-addresses into the destination POOM, each subsequent transclusion hop reads out the same I-addresses again.

The content allocation only happens once — in `inserttextgr` (`granf2.c:92-108`) — at the moment of original insertion. From that point forward, every `copy` operation is purely a coordinate-space remapping: V-address in source → I-address via source POOM → stored at new V-address in destination POOM.

This means the I-address is **invariant under any number of copy hops**. Documents B, A, C, and arbitrarily many more all have POOM crums whose I-dimension points into the same granfilade storage location.

---

### One Structural Caveat: `rearrangepm`

If document A is rearranged after being copied from B (`dorearrange` → `rearrangepm`, `orglinks.c:137-142`), its V-order changes via `rearrangend`. But rearrangement only moves V-coordinates within the POOM — it does not alter the I-coordinates of existing crums. So when C subsequently copies from A, the permutation still extracts the original I-addresses from the crums, regardless of their new V-positions. Transclusion identity is preserved even across rearrangements.

---

### Summary of the Call Chain

```
B creation:    inserttextgr → alloc I-address → insertpm → B's POOM[V_B → I_orig]
A copies B:    specset2ispanset → vspanset2ispanset(B's POOM) → context2span → I_orig
               → insertpm → A's POOM[V_A → I_orig]
C copies A:    specset2ispanset → vspanset2ispanset(A's POOM) → context2span → I_orig
               → insertpm → C's POOM[V_C → I_orig]
```

The key lines:
- **Allocation (once)**: `granf2.c:94` — `findisatoinsertgr` assigns the permanent I-address
- **V→I lookup**: `do2.c:34-38` — uses the source document's POOM, not the granfilade
- **I extracted**: `context.c:206-207` — `grasp.dsas[I]` from the POOM crum's stored I-coordinate
- **I installed**: `orglinks.c:105` — `movetumbler(&lstream, &crumorigin.dsas[I])` — same value stored in destination POOM

Transclusion identity is preserved completely and transitively through arbitrary copy chains.
