## Question 15 [gregory]

> If CREATELINK advances the I-address allocation counter past the text range, creating a gap, is that gap permanently reserved — meaning no future text INSERT can ever fill those gap I-addresses — or could a different document or session allocate into that gap region?

## KB Synthesis

## Gap I-Addresses After CREATELINK Are Permanently Inaccessible

**For the same document (any session):** The gap is permanently unavailable — no future text INSERT into that document can ever allocate those addresses.

The mechanism is layered:

1. **Monotonic allocation** [INV-MONOTONIC, Finding 0061]: `findpreviousisagr` returns the highest existing I-address below the upper bound, then increments by 1. There is no free-list and no gap-filling — allocation always continues upward from the current maximum.

2. **No reuse** [INV-NO-IADDR-REUSE]: "Once allocated in the granfilade, I-addresses are permanent... the I-address space grows strictly monotonically and permanently."

3. **Shared per-document allocator** [Finding 0063]: Both link orgl and text content use `findisatoinsertmolecule` for the same document's allocation space. After CREATELINK advances the maximum into the link orgl's address range, subsequent text INSERTs find the link orgl as the maximum and allocate above it — the gap addresses are simply skipped forever. The empirical proof: INSERT "ABC" → CREATELINK → INSERT "DEF" produces 2 shared span pairs (gap visible), while INSERT "ABC" → VERSION → INSERT "DEF" produces 1 pair (no gap, VERSION does not touch content allocation) [Finding 0077].

4. **Sessions share state** [Finding 0042, INV-ATOMICITY]: The backend is single-threaded with run-to-completion dispatch. All sessions query the same granfilade tree. A different session inserting into the same document would see the same maximum and allocate above the same gap.

**For different documents:** Unaffected. Allocation is partitioned by document — the upper-bound search in `findisatoinsertmolecule` is scoped to the specific document's subtree [Finding 0065: "element_number is scoped to the document, not global"; Finding 0077: "both query the same granfilade tree but search different subtrees"]. A gap in document A's I-address space has no bearing on document B's text allocation counter.

**Summary:** The gap is a permanent artifact of the monotonic, no-reuse design. The gap I-addresses are structurally inaccessible in perpetuity for any operation on that document, in any session. Different documents have independent allocation spaces and are entirely unaffected.

---

## Code Exploration

The user hasn't granted write access. Here is the complete answer based on code analysis:

---

## Answer: CREATELINK Does Not Create a Gap in the Text I-Address Range

The premise of the question requires correction. **CREATELINK does not advance the text I-address counter at all.** The "gap" it creates is in **V-space** (virtual document position), not in I-space.

---

### I-Address Subspace Separation — The Core Mechanism

`findisatoinsertmolecule` (`granf2.c:158-181`) is the allocation function for both text and link atoms. It uses `atomtype` to create strict, non-overlapping search bounds:

```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
```

With `TEXTATOM = 1` and `LINKATOM = 2` (`xanadu.h:145-146`):

| Atom type | `atomtype` | `upperbound` | Allocated I-range |
|-----------|-----------|--------------|------------------|
| TEXTATOM  | 1         | `docisa.0.2` | `docisa.0.1.*`   |
| LINKATOM  | 2         | `docisa.0.3` | `docisa.0.2.*`   |

For text allocation, `findpreviousisagr` searches for the highest ISA **strictly less than** `docisa.0.2`. Link ISAs live at `docisa.0.2.*`, which is **greater than** `docisa.0.2`. They are invisible to the text search. The text I-counter never sees a link ISA.

This is confirmed by Finding 0065's golden data: link ISA `1.1.0.1.0.1.0.2.1` is in element field `0.2`, while text ISAs are in field `0.1`. Document A's second link (`1.1.0.1.0.1.0.2.2`) is consecutive with its first (`1.1.0.1.0.1.0.2.1`) even after intervening operations in another document. There is no shared counter.

---

### What CREATELINK Actually Does to Allocation State

`docreatelink` (`do1.c:195-221`) calls:

1. **`createorglingranf`** — allocates a `GRANORGL` node at `docisa.0.2.1` (link subspace) via `findisatoinsertmolecule` with `LINKATOM`. This modifies the granfilade, but only in the `docisa.0.2.*` range.

2. **`findnextlinkvsa`** (`do2.c:151-167`) — computes the link's **V-address** (position in the document's virtual space) as `max(text_vspan_end, 2.1)`:

```c
tumblerclear (&firstlink);
tumblerincrement (&firstlink, 0, 2, &firstlink);  // firstlink = 2
tumblerincrement (&firstlink, 1, 1, &firstlink);  // firstlink = 2.1
(void) doretrievedocvspan (taskptr, docisaptr, &vspan);
tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
if (tumblercmp (&vspanreach, &firstlink) == LESS)
    movetumbler (&firstlink, vsaptr);   // link goes at 2.1
else
    movetumbler (&vspanreach, vsaptr);
```

3. **`docopy`** — inserts the link's I-address reference into the document's POOM (V→I enfilade) at the V-position computed above.

---

### The Gap Is in V-Space

If a document's text occupies V-positions 1.1 through (say) 1.4, `findnextlinkvsa` places the link at V-position 2.1, leaving a gap at V-positions ~1.4 to 2.0 with no content. This explains the 2 span pairs in Finding 0063's `compare_versions` result: ABC text is at V-positions 1.1–1.3, and DEF text (inserted "at end" after the link) lands in the 2.x V-range. The two documents being compared have different V-space mappings for the same I-addresses — hence 2 pairs, not 1. Finding 0063's explanation ("link orgl advances the text I-counter") is incorrect. Its golden file comment is correct: `"CREATELINK modifies POOM enfilade only, not granfilade"`.

---

### Is the V-Space Gap Permanently Reserved?

No. `acceptablevsa` (`do2.c:110-113`) is an unconditional stub:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

Any V-address is accepted. A client can INSERT text at gap V-positions (between text-end and 2.1) and the backend will accept it. There is no enforcement preventing this. In practice, clients inserting "at end" will push further into the 2.x range, widening the gap rather than filling it, but this is a client convention, not a backend constraint.

---

### Cross-Document Isolation

I-addresses are scoped by document ISA prefix. The `upperbound` in `findisatoinsertmolecule` is constructed from `hintptr->hintisa`, which is the owning document's ISA (`do2.c:78-84`). `findpreviousisagr` searches only within that document's address range. A different document's CREATELINK — or any operation — cannot touch this document's text or link I-address subspaces. Allocation for document A does not advance any counter visible to document B.

---

### Cross-Session Persistence

There is no session-local allocation counter. On every INSERT, `findisatoinsertmolecule` calls `findpreviousisagr` (`granf2.c:255-278`) to query the current granfilade tree for the highest existing ISA below the bound. This is stateless — the granfilade is the authoritative persistent store. Once an ISA is allocated, it remains in the tree permanently (no free list, no garbage collection). A future session will find the same highest ISA and continue monotonically from there. No reuse of addresses is possible.

---

### Summary

| Property | Answer | Code location |
|----------|--------|---------------|
| Does CREATELINK advance the text I-counter? | **No** | `granf2.c:162` — separate `upperbound` per `atomtype` |
| Is there a text I-space gap from CREATELINK? | **No** | Text ISAs `docisa.0.1.*` never overlap link ISAs `docisa.0.2.*` |
| Is there a V-space gap? | **Yes** | `do2.c:157-163` — link placed at `max(end, 2.1)` |
| Is the V-gap reserved/enforced? | **No** | `do2.c:110-113` — `acceptablevsa` always returns `TRUE` |
| Can a different document fill the I-gap? | **N/A** (no I-gap exists) | `granf2.c:162` — bound is per-`docisa` |
| Can a different session fill the I-gap? | **N/A** (no I-gap exists) | `granf2.c:255` — stateless query of persistent tree |
