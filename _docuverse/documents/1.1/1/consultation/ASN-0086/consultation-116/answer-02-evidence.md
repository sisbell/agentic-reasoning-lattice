## Question 2 [evidence]

> At system initialization (before any link allocation), does udanax-green's link store begin empty, or can it boot with a pre-populated set of link addresses — and if pre-populated, are those addresses a contiguous sibling-chain prefix per home?

## KB Synthesis

## Initial Link Store State

The KB gives a clear answer for the **code-level initialization** but leaves the **bootstrap document** partially open.

---

### Fresh file: link store starts empty

At code initialization, both enfilades are created empty [SS-DUAL-ENFILADE, Finding 0012]:

```
granf = createenf(GRAN)   — empty content enfilade
spanf = createenf(SPAN)   — empty link index
```

The spanf has no link index entries and the granf has no link orgls. The first `MAKELINK` call on any document `D` would allocate at `D.0.2.1` per the "no prior links" branch in `findisatoinsertmolecule` [SS-ADDRESS-ALLOC, Finding 0065].

---

### Restart: whatever `enf.enf` holds

All state persists in `enf.enf` [SS-UNIFIED-STORAGE, Finding 0059]. On restart, `initenffile()` loads the file with no consistency check and no traversal [EC-NO-STARTUP-VALIDATION]. The link store is whatever it was at last clean shutdown — not reset.

---

### Bootstrap document: partially documented

[SS-LINK-ENDPOINT, Finding 0024] establishes that the type registry lives in **bootstrap document (doc 1)** at addresses `1.0.2.2` (JUMP), `1.0.2.3` (QUOTE), `1.0.2.6` (FOOTNOTE), `1.0.2.6.2` (MARGIN). This implies some pre-seeded structure exists in the initial `enf.enf`. However, the KB does not document whether this is injected at factory-build time, created on first run, or assumed to already be in the persistent file. **This question is not answerable from the KB.**

---

### If pre-populated: yes, contiguous sibling-chain prefix

The allocation invariant [INV-MONOTONIC, Finding 0065; SS-ADDRESS-ALLOC, Finding 0065] guarantees that link addresses within a home document's subspace form a strict monotone sequence: `D.0.2.1, D.0.2.2, D.0.2.3, ...`. The query-and-increment mechanism (`findpreviousisagr` → `tumblerincrement`) never skips or reuses [INV-NO-IADDR-REUSE]. So any pre-populated block would necessarily be a contiguous sibling-chain prefix from `.0.2.1` upward within each home document — gaps cannot arise unless a non-text allocation intervened [INT-LINK-INSERT, Finding 0063], which would only shift text I-addresses, not the link subspace numbering.

---

**Summary:** The link store boots empty for a fresh `enf.enf`. Whether the type-registry entries in the bootstrap document are pre-seeded in that initial file cannot be determined from the KB.

---

## Code Exploration

I have read all the relevant source. Here is the complete answer.

---

## Link Store Initialization in udanax-green

### Startup Sequence

`main()` in `backend/bed.c:92-95` runs this sequence before the event loop:

```c
init(1);             // bed.c:92 — registers FEBE request handlers
inittask(&task);     // bed.c:93 — clears per-request task struct
errno = 0;           // bed.c:94
initmagicktricks();  // bed.c:95 — THE link-store initializer
```

`initmagicktricks()` in `backend/entexit.c:19-47` is the critical function:

```c
if (initenffile()) {
    initkluge ((typecuc**)&granf, (typecuc**)&spanf);   // entexit.c:42
} else {
    granf = (typegranf) createenf (GRAN);               // entexit.c:44
    spanf = (typespanf) createenf (SPAN);               // entexit.c:45
}
```

There are exactly **two paths**, selected by whether the `enf.enf` disk file exists.

---

### Path 1 — Fresh System (no `enf.enf`)

`granf` and `spanf` are created as empty enfilades via `createenf()`. No link addresses exist. The link store is completely empty.

---

### Path 2 — Reboot (existing `enf.enf`)

`initkluge()` in `backend/corediskin.c:18-41` deserializes both structures from the file:

```c
tempcbc->cinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = GRANFDISKLOCATION;
// corediskin.c:25
inorgl(tempcbc);                              // corediskin.c:27 — reads granf apex from disk
*granfptr = tempcbc->cinfo.granstuff.orglstuff.orglptr;
(*granfptr)->numberofsons = 0;                // corediskin.c:30 — hack for correct son count

tempcbc->cinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = SPANFDISKLOCATION;
// corediskin.c:33
inorgl(tempcbc);                              // corediskin.c:35 — reads spanf apex from disk
*spanfptr = tempcbc->cinfo.granstuff.orglstuff.orglptr;
(*spanfptr)->numberofsons = 0;                // corediskin.c:38
```

The deserialized granfilade and spanfilade contain exactly what was flushed during the prior session — **no special pre-population occurs during reboot**. Whatever links existed before `diskflush()` (called at `bed.c:105`) are restored verbatim.

---

### Are Pre-populated Addresses a Contiguous Sibling-Chain Prefix Per Home?

**Yes — by construction.** Here is why.

All link allocation goes through `docreatelink()` at `backend/do1.c:195-221`, which calls `createorglingranf()` (line 209), which calls `findisatoinsertgr()`, which calls `findisatoinsertmolecule()` at `backend/granf2.c:158-181` for `LINKATOM` atoms:

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound); // granf2.c:162
    clear(&lowerbound, sizeof(lowerbound));
    findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);    // granf2.c:164
    if (tumblerlength(&hintptr->hintisa) == tumblerlength(&lowerbound)) {
        tumblerincrement(&lowerbound, 2, hintptr->atomtype, isaptr);             // granf2.c:166
        tumblerincrement(isaptr, 1, 1, isaptr);                                  // granf2.c:167
    } else if (hintptr->atomtype == LINKATOM) {
        tumblerincrement(&hintptr->hintisa, 2, 2, isaptr);                      // granf2.c:171
        if (tumblercmp(&lowerbound, isaptr) == LESS)
            tumblerincrement(isaptr, 1, 1, isaptr);                              // granf2.c:173
        else
            tumblerincrement(&lowerbound, 0, 1, isaptr);                         // granf2.c:175
    }
}
```

For a document with ISA `D`:
- The **first link** gets ISA `D.2.2.1` (the `tumblerincrement(..., 2, 2, isaptr)` at line 171 gives `D.2.2`, then `+1` at line 173 gives `D.2.2.1`)
- Every subsequent link gets `lowerbound + 0.1` (line 175): `D.2.2.2`, `D.2.2.3`, …

`findpreviousisagr()` at `granf2.c:255-278` always finds the **highest** existing ISA below `upperbound = D.2.3`. This means each new link is appended immediately after the last, with no gaps. The result is a **strictly contiguous, strictly ascending, strictly prefix sequence**:

```
D.2.2.1   ← first link
D.2.2.2   ← second link
D.2.2.3   ← third link
…
D.2.2.K   ← K-th link
```

When this is flushed to `enf.enf` and later reloaded via `initkluge`, these K entries are restored exactly. Because they were inserted sequentially into the granfilade and the enfilade's bottom crums (CBC nodes) hold them in sorted ISA order, they will appear as a **contiguous run in the CBC sibling chain** at the bottom level of the granfilade tree — as many as fit per crum, overflowing into sibling CBCs only when a split occurs (`backend/split.c`).

---

### Summary

| Condition | Link store state at boot |
|-----------|--------------------------|
| No `enf.enf` | Completely empty (`entexit.c:44-45`) |
| `enf.enf` exists | Deserialized from disk exactly as flushed (`corediskin.c:18-41`) |
| Addresses pre-populated? | Only if prior session created links — no synthetic injection at boot |
| Address structure per home `D` | Contiguous prefix `D.2.2.1 … D.2.2.K`, allocated strictly sequentially by `findisatoinsertmolecule` (`granf2.c:170-175`) |
| Sibling-chain prefix? | Yes — sequential insertion into a sorted enfilade guarantees the K link ISAs for home `D` occupy a contiguous range in the CBC-level sibling chain, subject only to node splits that subdivide (but do not scatter) that range |
