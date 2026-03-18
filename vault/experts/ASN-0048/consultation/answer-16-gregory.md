## Question 16 [gregory]

> When INSERT adds text immediately adjacent to existing content (e.g., appending at the end of current text), does the granfilade always allocate the next contiguous I-address such that the POOM can coalesce into a single bottom crum, or are there conditions where the I-address is non-contiguous despite the V-position being adjacent?

## KB Synthesis

## I-Address Contiguity for Adjacent Inserts

The short answer: adjacent V-position inserts produce contiguous I-addresses **only when no content-allocating operation intervenes**. Several KB entries are relevant.

### The Allocation Mechanism

From [SS-ADDRESS-ALLOC] / [INV-MONOTONIC]: I-address allocation is stateless — `findisatoinsertmolecule` queries the granfilade for the current maximum I-address and increments by 1. There is no per-session counter or locality hint. The allocation is purely `next_iaddr(granf) = max_iaddr(granf) + 1`, regardless of where the insertion falls in V-space.

### What Enables Coalescing

From [ST-INSERT] (Finding 0062): `isanextensionnd()` coalesces a new insertion into an existing POOM crum when **both** hold:
1. Same `homedoc` (I-address origin document)
2. New content's I-address origin == existing crum's reach (I-space contiguity)

V-adjacency is necessary but insufficient — I-address contiguity is the operative condition.

### What Breaks I-Address Contiguity

From [INT-LINK-INSERT] (Finding 0063): **CREATELINK** is the primary disruptor. It calls `createorglingranf`, which allocates a link orgl in the granfilade. This advances `max_iaddr(granf)`. When the next INSERT calls `findpreviousisagr`, it finds the link orgl's I-address as the maximum and allocates text I-addresses above it — non-contiguous with any preceding text I-addresses. This is directly observable: `INSERT "ABC" → CREATELINK → INSERT "DEF"` yields **two** shared span pairs in `compare_versions`.

Any other **INSERT** (at any V-position in any document) also advances the global maximum, breaking contiguity for subsequently adjacent inserts.

### What Does NOT Break Contiguity

From [INV-MONOTONIC] (Finding 0077) and [FC-GRANF-ON-DELETE] (Finding 0061):

- **DELETE** and **REARRANGE**: granfilade unchanged; `findpreviousisagr` returns the same maximum. I-address contiguity is preserved.
- **CREATENEWVERSION**: allocates only a document address in a separate tumbler range, not a content I-address. `INSERT "ABC" → VERSION → INSERT "DEF"` yields **one** shared span pair — contiguous.

The contiguity-breaking predicate from [INV-MONOTONIC] (Finding 0077): `text_contiguous(insert_a, insert_b) ⟺ ¬∃ alloc_c : time(a) < time(c) < time(b) ∧ alloc_c ∈ content_allocations`, where `content_allocations = {INSERT, CREATELINK}`.

### Summary Table

| Intervening Operation | Granfilade Modified? | I-Addresses Contiguous? | POOM Coalesces? |
|---|---|---|---|
| None | No | Yes | Yes |
| DELETE / REARRANGE | No | Yes | Yes |
| CREATENEWVERSION | Doc address only | Yes | Yes |
| CREATELINK | Yes (link orgl) | **No** | No |
| Another INSERT | Yes (text) | **No** | No |

### The Homedoc Caveat

Even with contiguous I-addresses, if adjacent V-positions hold content from **different source documents** (e.g., text inserted natively vs. transcluded via COPY), `isanextensionnd` fails the `homedoc` check [ST-INSERT, Finding 0046]. The I-addresses may be contiguous in the permascroll, but the POOM crums will not coalesce because the content origin differs.

---

## Code Exploration

Now I have the complete picture. Let me compose the full answer.

---

## Answer: I-Address Contiguity and POOM Coalescence on Adjacent INSERT

### The Full Call Chain for INSERT

`fns.c:insert` [fns.c:84] → `doinsert` [do1.c:87] → (1) `inserttextingranf` to allocate I-address, (2) `docopy` → `insertpm` → `insertnd` → `insertcbcnd` to register V↔I mapping in the POOM.

---

### Step 1: I-Address Allocation in the Granfilade

`inserttextgr` [granf2.c:83-109] calls `findisatoinsertgr` [granf2.c:130] to determine the starting I-address for new text. For text atoms (`ATOM` subtype with `TEXTATOM=1`), this routes to `findisatoinsertmolecule` [granf2.c:158-181].

That function first establishes a search boundary:

```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);  // granf2.c:162
clear (&lowerbound, sizeof(lowerbound));
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);  // granf2.c:164
```

`upperbound` = `docISA.0.(TEXTATOM+1)` = `docISA.0.2` — this strictly excludes link atoms (`LINKATOM=2` lives at addresses ≥ `docISA.0.2.0.1`, which are all greater than `docISA.0.2`). The search is bounded to this document's text atom range only.

`findpreviousisagr` [granf2.c:256-278] walks the granfilade tree right-to-left, accumulating relative offsets. At the leaf node (height=0), it calls `findlastisaincbcgr` [granf2.c:280-284]:

```c
int findlastisaincbcgr(typecbc *ptr, typeisa *offset)   /* offset is last isa if non-text or one char */
{
    if (ptr->cinfo.infotype == GRANTEXT)
        tumblerincrement (offset, 0, (INT) ptr->cinfo.granstuff.textstuff.textlength - 1, offset);
}
```

This sets `lowerbound` to the address of the **last character** of the last text crum.

Now in `findisatoinsertmolecule`, there are two cases:

**Case A** — `tumblerlength(hintisa) == tumblerlength(lowerbound)`: no text atoms exist yet (the search found the document's own GRANORGL, at the same address depth as `hintisa`):
```c
tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);  // granf2.c:166
tumblerincrement (isaptr, 1, 1, isaptr);                       // granf2.c:167
```
Allocates the first text atom at `docISA.0.1.0.1` (two levels below document ISA). This is a cold start — no predecessor to coalesce with anyway.

**Case B** — text atoms already exist, `atomtype == TEXTATOM`:
```c
tumblerincrement (&lowerbound, 0, 1, isaptr);  // granf2.c:169
```
`lowerbound` is the last character's address. Adding 1 at level 0 (same digit depth) gives `new_start = last_char_addr + 1`.

**This IS the address immediately after the last allocated character. I-addresses are strictly contiguous here.**

If the previous crum had I-start = S and length = L, it occupied [S, S+L-1]. `findlastisaincbcgr` returns S+L-1. Case B gives new start = S+L = the previous crum's I-reach. That is the definition of contiguity.

---

### Step 2: POOM Coalescence Test

After `inserttextingranf` returns `ispanset = {stream: lsa, width: total_chars}`, `docopy` → `insertpm` [orglinks.c:75-134] passes the V and I spans to `insertnd` [insertnd.c:15] → `insertcbcnd` [insertnd.c:242].

Before creating a new bottom crum, `insertcbcnd` [insertnd.c:249-258] scans existing bottom crums:

```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
        dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);  // extend in-place
        ...
        return(FALSE);  // coalesced — no new crum
    }
}
```

The coalescence predicate `isanextensionnd` [insertnd.c:301-309]:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

Two conditions must hold:
1. Same home document (`homedoc` match)
2. **Both V-reach and I-reach of the existing crum equal the V-origin and I-origin of the new insertion** — `lockeq` is a full 2D comparison of the `dsas[V]` and `dsas[I]` fields simultaneously

For appending at the V-end of a document, `appendpm` calls `findvsatoappend` [orglinks.c:29-49] to get exactly `reach.dsas[V]` of the last text crum:

```c
} else if (tumblercmp (&reach.dsas[V], &linkspacevstart) == LESS) {
    movetumbler (&reach.dsas[V], vsaptr); /* no links in doc */
```

So V-adjacency holds. And since Case B gives `I_new_start = I_reach_of_last_crum`, I-adjacency also holds. **Coalescence occurs for a pure append.**

For `makegappm` [insertnd.c:124]: when appending, `origin.dsas[V] >= reach.dsas[V]` of the full POOM, so the early-return guard fires:
```c
if (...|| tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);    /* this if for extensions to bc without calling cut */  // insertnd.c:143
```
No splitting needed for a pure append. ✓

---

### The Granfilade Also Has Its Own Compaction

Independently of POOM coalescence, `insertseq` [insert.c:17-70] does compaction at the granfilade level:

```c
if (           /* crum can be extended */
   info->infotype == GRANTEXT
&& ptr->cinfo.infotype == GRANTEXT
&& ptr->cinfo.granstuff.textstuff.textlength < GRANTEXTLENGTH) {
    if (!fillupcbcseq (ptr, &nextaddress, info)) {   // insert.c:38
        ivemodified ((typecorecrum*)ptr);
        return(0);  // text absorbed into existing granfilade crum
    }
}
```

`fillupcbcseq` [insert.c:75] appends new characters directly into the existing granfilade leaf if there is capacity. This is separate from POOM coalescence — it compacts the permascroll storage itself.

---

### The Conditions Where I-Address Is Non-Contiguous Despite V-Adjacency

**Case: document versioning or content copy**

`docreatenewversion` [do1.c:260] creates a new document under a different ISA, then calls `docopyinternal` → `insertpm` to populate the new document's POOM with crums whose I-addresses point into the **original** document's ISA subtree (e.g., `origDocISA.0.1.0.*`).

When a subsequent INSERT appends to the new version:

- `doinsert` calls `inserttextingranf` with `hint.hintisa = newDocISA`
- `findisatoinsertmolecule` searches `findpreviousisagr` up to `newDocISA.0.2`
- No text atoms exist under `newDocISA.0.1.*` (only the GRANORGL at `newDocISA` itself)
- `tumblerlength(hintisa) == tumblerlength(lowerbound)` → **Case A fires**
- Fresh I-address allocated: `newDocISA.0.1.0.1.0.1`

The POOM's last crum has I-reach = some address in `origDocISA.0.1.*`. The new I-origin = `newDocISA.0.1.0.1.0.1`. These are in **entirely different branches of the address hierarchy**.

`isanextensionnd` tests `lockeq(reach.dsas, originptr->dsas, ...)`:
- `reach.dsas[I]` ≠ `originptr->dsas[I]`
- **Coalescence fails.**

The POOM acquires a new bottom crum even though the V-position is adjacent. The new text's I-address is non-contiguous with the copied content's I-addresses — they live in separate document ISA subtrees.

**The same pattern applies to `docopy`** [do1.c:45] when inserting content transcluded from another document. The POOM crum's I-span points to the source document's permascroll range; new original text in the target document gets fresh I-addresses from the target's ISA subtree.

---

### Summary

| Condition | I-contiguous? | V-adjacent? | POOM coalesces? |
|-----------|--------------|-------------|-----------------|
| Append to original document | Yes — `findisatoinsertmolecule` Case B: `lowerbound + 1` | Yes — `findvsatoappend` returns exact V-reach | Yes — both arms of `isanextensionnd` succeed |
| Mid-document insert (original) | Yes — still Case B, allocates next sequential I-addr | No — V-origin ≠ V-reach of any crum | No — V-arm of `isanextensionnd` fails |
| First insert into fresh document | N/A — Case A, cold start | N/A | N/A — nothing to coalesce with |
| Append to versioned/copied document | No — Case A, new ISA subtree | Yes | No — I-arm of `isanextensionnd` fails |

**The definitive non-contiguous case**: After `docreatenewversion` or `docopy`, the target document's POOM holds I-spans from a foreign ISA subtree. Any original text insertion allocates from the target document's own ISA subtree via Case A of `findisatoinsertmolecule`. Even though V-positions are adjacent at the append point, the I-addresses are non-contiguous across ISA subtree boundaries — `isanextensionnd` [insertnd.c:308] fails the `lockeq` test, and the POOM acquires a new bottom crum rather than extending the existing one.
