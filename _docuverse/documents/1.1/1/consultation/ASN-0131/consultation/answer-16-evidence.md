## Question 16 [evidence]

> Does this operation answer the existence side or the discoverability side of ASN-0127's distinction — i.e., does it report endsets that are currently anchored through some document's live V-stream, or all endsets whose I-spans were ever indexed in the spanfilade even if no POOM now references them?

## KB Synthesis

## RETRIEVEENDSETS Answers the Discoverability Side

RETRIEVEENDSETS (opcode 28) answers the **discoverability side** — but this holds for both its input and its output, with the spanfilade sitting in between as an existence-side index whose stale entries are filtered out before any result reaches the caller.

### The Input Side (What Triggers Discovery)

The call chain begins with `retrieveendsetsfromspanf()` converting the caller's input V-spec into I-addresses by walking the **querying document's current POOM** [SS-RETRIEVE-ENDSETS]. Only I-addresses that currently map to live V-positions in that document participate in the spanfilade search. If the caller specifies a region whose content has been deleted, those I-addresses are gone from the POOM and produce nothing to search for. The input is anchored to the live V-stream.

### The Spanfilade Search (Existence-Side Internals)

The SPANRANGE/ORGLRANGE search against the spanfilade is existence-side: the spanfilade is write-only and monotonically growing [INV-SPANF-WRITE-ONLY], so it retains all endpoint I-spans ever indexed, including those whose content has since been deleted from all documents [EC-STALE-SPANF-REFERENCE]. The search will find any link whose endpoint I-addresses overlap the input, even if that link's endpoint content is now orphaned.

### The Output Side (Endset V-Address Resolution)

This is where discoverability is enforced as a filter. The found link endpoint sporglsets are converted back to V-addresses via `linksporglset2specset()` using the **querying document's docid** [SS-RETRIEVE-ENDSETS, Finding 0035]. Per [INV-ITOV-FILTERING], this conversion path — `sporglset2vspanset()` → `ispan2vspanset()` → `span2spanset()` → `retrieverestricted()` — silently drops any I-address for which `retrieverestricted()` returns NULL (i.e., no current POOM mapping). This is the universal I-to-V filter shared with FOLLOWLINK [EC-GHOST-LINK].

The consequence: endset I-addresses that are not currently anchored in the querying document's live V-stream produce no V-span output.

### Contrast with FOLLOWLINK

| Aspect | FOLLOWLINK | RETRIEVEENDSETS |
|--------|-----------|-----------------|
| Input | Link ISA (existence-side — direct orgl read) | V-spec (discoverability-side — POOM lookup first) |
| Lookup | Link orgl directly | Spanfilade search |
| Output filter | Querying doc POOM (discoverability-side) | Querying doc POOM (discoverability-side) |

Both operations share the same I-to-V filtering mechanism for output [INV-ITOV-FILTERING], but FOLLOWLINK's input is existence-side (you already know the link ID), while RETRIEVEENDSETS' input is discoverability-side (you must have live content to search from).

### Summary

RETRIEVEENDSETS is discoverability-side end-to-end at the API boundary:

1. **Input**: The caller's V-spec is resolved through the current live POOM — deleted content produces no search keys.
2. **Internal**: The spanfilade search may touch stale existence-side entries, but those survive only if the input content (which must be live) shares I-addresses with them.
3. **Output**: Endset I-spans are converted to V-positions through the querying document's current POOM, silently discarding any I-addresses with no live mapping.

The result is that RETRIEVEENDSETS reports only endsets whose I-addresses are **currently anchored in the querying document's live V-stream** — not all endsets ever indexed in the spanfilade.

---

## Code Exploration

I now have everything I need to give the definitive answer.

---

## The Existence/Discoverability Split in the Spanfilade Operations

ASN-0127 is not present in this repository, but the distinction it describes is directly traceable in the code. The question maps exactly onto the structural separation between two layers in `retrieveendsetsfromspanf` and `findlinksfromtothreesp`. Here is the full analysis.

---

### The Two Operations That Report Endsets

`fns.c:retrieveendsets()` → `do1.c:doretrieveendsets()` [line 369–374] → `spanf1.c:retrieveendsetsfromspanf()` [line 190–235]

`fns.c:findlinksfromtothree()` → `do1.c:dofindlinksfromtothree()` [line 348–353] → `spanf1.c:findlinksfromtothreesp()` [line 56–103]

---

### Three Semantic Layers Inside `retrieveendsetsfromspanf`

#### Layer 1 — Input V→I conversion (POOM-gated, existence side)

```c
// spanf1.c:222
specset2sporglset(taskptr, specset, &sporglset, NOBERTREQUIRED)
```

`specset2sporglset` is defined at `sporgl.c:14–33`. For V-specs it calls `vspanset2sporglset` (sporgl.c:35–65), which calls `findorgl(taskptr, granf, docisa, &orgl, type)` to get the querying document's POOM, then `vspanset2ispanset` to translate V-positions to I-addresses. **Only I-addresses that currently exist in that document's POOM are returned.** This is a hard existence gate — content not currently in the POOM produces no I-addresses and generates no spanfilade query.

#### Layer 2 — Spanfilade query (append-only, discoverability side)

```c
// spanf1.c:244–245
context = retrieverestricted((typecuc*)spanf, (typespan*)sporglptr, SPANRANGE,
                              whichspace, ORGLRANGE, (typeisa*)NULL);
```

The spanfilade is **write-only at the removal level**. The evidence is direct:

- `do1.c:162–171` (`dodeletevspan`): calls only `deletevspanpm` → `deletend` on the document's orgl. There is no call to anything in `spanf1.c`.
- `do2.c:116–128` (`insertendsetsinspanf`): calls `insertspanf` for FROM, TO, and THREE endsets. No corresponding removal function exists anywhere.
- `spanf1.c` contains `insertspanf` (line 15), `findlinksfromtothreesp` (line 56), `retrieveendsetsfromspanf` (line 190), `retrievesporglsetinrange` (line 237) — **no delete, remove, or cleanup function**.

`retrieverestricted` on the spanfilade therefore returns **all entries ever written for those I-address ranges**, including endsets from links whose endpoint content was subsequently deleted from every POOM, and endsets from links that were themselves deleted (Finding 0024). This layer answers the **discoverability side** — it reports what was ever indexed.

#### Layer 3 — Output I→V conversion (POOM-gated, partial existence side)

```c
// spanf1.c:224–226
linksporglset2specset(taskptr, &((typevspec *)specset)->docisa, fromsporglset, fromsetptr, NOBERTREQUIRED)
```

`homedoc` here is `((typevspec *)specset)->docisa` — the **querying document's ISA**, not the endset's own home document. Tracing into `sporgl.c:97–123` → `linksporglset2vspec` (sporgl.c:127–137) → `sporglset2vspanset` (sporgl.c:141–176) → `ispan2vspanset` (`orglinks.c:389–394`) → `permute` → `span2spanset` (`orglinks.c:425–454`):

```c
// orglinks.c:435
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);
// orglinks.c:446–448
if(!context){
    return(targspansetptr);  // ← SILENT DROP: no V-span added
}
```

If the endset I-address is not present in the **querying document's** POOM, `retrieverestricted` returns NULL and the I-address is silently dropped — `targspansetptr` is returned unchanged. Nothing in the returned specset reflects that the address existed.

---

### The Decisive Answer

**`retrieveendsetsfromspanf` answers neither the full existence side nor the full discoverability side. It answers a narrower, document-local variant of the existence side.**

- Layer 2 (spanfilade raw query) is on the **discoverability side**: it returns all endset I-spans ever indexed, regardless of current POOM state anywhere.
- Layers 1 and 3 (POOM conversions) impose **existence-side filters** — but only against the **querying document's single POOM**, not globally across all documents.

Concrete consequence: if endset I-address `a` is currently in document B's POOM (it is live, it is anchored through a real V-stream), but not in the querying document A's POOM, then `retrieveendsetsfromspanf` called from document A will **drop `a` silently**. The operation answers "is this endset currently in *this* document's V-stream" — not "is this endset currently anchored through *some* document's V-stream."

This means the existence/discoverability distinction in ASN-0127's terms is not cleanly implemented at either end: the underlying spanfilade carries discoverability data, but the POOM conversion collapses it into single-document existence, not global existence.

---

### `findlinksfromtothreesp` for Comparison

`dofindlinksfromtothree` → `findlinksfromtothreesp` (spanf1.c:56–103):
- Layer 1: same POOM-gated V→I conversion (`specset2sporglset`, line 71–75)
- Layer 2: `sporglset2linksetinrange` (sporgl.c:239–269) queries the spanfilade and extracts link ISAs via `beheadtumbler`
- Layer 3: **no POOM conversion on output** — just raw link ISAs (`onlinklist`)

`findlinksfromtothreesp` therefore answers **closer to the discoverability side for output**: it returns all link ISAs ever indexed for I-addresses currently in the querying document's POOM, including deleted links (stale spanfilade entries, Finding 0024). There is no output-side existence filter. The caller gets link ISAs it can follow even if those links no longer have live endpoint content.

---

### Root Cause

The spanfilade is architecturally a **historical append log**, not a live index. `insertspanf` (`spanf1.c:15`) adds entries; no function removes them. Every read from the spanfilade via `retrieverestricted` is inherently a discoverability-side operation. The illusion of existence-side behavior comes entirely from the POOM conversions that wrap the spanfilade call — and those conversions are document-local, not global.

| Layer | Location | Side |
|---|---|---|
| V→I input conversion | `sporgl.c:35–65` (POOM lookup) | Existence (querying doc only) |
| Spanfilade raw query | `spanf1.c:244` / `sporgl.c:259` | Discoverability (all ever indexed) |
| I→V output conversion | `orglinks.c:435–448` (POOM lookup, silent drop) | Existence (querying doc only) |

The operation **reports discoverability data from the spanfilade**, then **filters it to document-local existence** at the output boundary. It does not report globally anchored endsets — an endset I-address live in any other document is indistinguishable from an unreferenced I-address from this operation's perspective.
