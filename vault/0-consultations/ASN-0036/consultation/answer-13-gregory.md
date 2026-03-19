## Question 13 [gregory]

> Was permanent retention of all I-space content always the design intent, or was garbage collection of I-addresses unreferenced by any V-space mapping ever planned or prototyped?

## KB Synthesis

The KB is clear on what the implementation does, but only partially answers the question of *original intent*.

## What the implementation unambiguously shows

Permanent retention was built in from the start, not retrofitted:

**No GC infrastructure exists at any layer.** The granfilade allocation mechanism is query-and-increment with no free-list — `findpreviousisagr` finds the highest existing I-address and increments past it, never filling gaps [INV-NO-IADDR-REUSE]. There's nowhere to put a freed address even if you wanted to reclaim it.

**The spanfilade has no delete functions.** Inspection of `spanf1.c` and `spanf2.c` shows only insertion and query operations — no `deletespanf`, no removal path [INV-SPANF-WRITE-ONLY]. This isn't a stub or placeholder; the data structures weren't designed with deletion in mind.

**DELETE deliberately touches only the POOM.** `dodeletevspan` calls `deletevspanpm` → `deletend`, with no call to any granfilade or spanfilade removal function [FC-GRANF-ON-DELETE]. The result is permanent divergence: after delete, the spanfilade still indexes I-addresses that no V-space mapping references [INT-DELETE-SPANF-DIVERGENCE]. If GC had been planned, you'd expect at least a stub or commented-out call here.

**The grim reaper is RAM management only.** The cache eviction mechanism writes modified crums to disk and frees memory — it preserves content permanently, it doesn't reclaim it [SS-CACHE-MECHANISM].

## The design principle

[FC-GRANF-ON-DELETE] explicitly frames this as the Xanadu "bytes never die, addresses never change" principle. The combination of permanent I-addresses enabling transclusion identity [INV-IADDR-IMMUTABILITY], permanent spanfilade entries enabling provenance history [INV-IADDRESS-PERMANENT], and the fact that [INV-DELETE-NOT-INVERSE] is a *property* rather than a defect — all point to permanence being load-bearing, not accidental.

## What the KB cannot answer

Whether GC was ever *planned, prototyped, or debated* — the KB is derived from implementation behavior, not design discussions or source history. I built udanax-green; the permanence was intentional in what I shipped. But whether there were whiteboard sessions about GC, or commented-out experiments, isn't derivable from the findings here.

What I can tell you with confidence: nothing in the codebase was left behind as a GC stub. The disabled `levelpull` (tree height reduction, commented out at `genf.c:318-342`) [INV-ENFILADE-MINIMALITY] is the only major "designed but not implemented" feature the KB surfaces — and that's about tree structure optimization, not content reclamation. For I-space GC specifically, there's no trace of scaffolding.

---

## Code Exploration

I now have sufficient evidence to give a definitive answer. Let me compile it.

---

## Permanent Retention of I-Space Content: Design Intent vs. GC Plans

### Short Answer

Permanent retention appears to be the *operational reality*, but the code contains explicit evidence that **disk-level GC was planned and partially scaffolded — and then deliberately disabled or left incomplete**. No mechanism exists at any level to detect or reclaim I-space addresses orphaned by V-span deletion.

---

### Evidence Trail

#### 1. GC Was Explicitly Named as a Design Goal

`backend/coredisk.h:18-19` — the `typediskloafhedr` struct (used for every on-disk enfilade block) carries a `refcount` field whose comment reads:

```c
SINT refcount;      /* for subtree sharing, */
                /* disk garbage collecting */
```

This is not speculative. The field exists; the intent is annotated in the header. GC was part of the original design vocabulary.

---

#### 2. The "Grim Reaper" Is Explicitly NOT Garbage Collection

`backend/NOTES:39`:

```
credel.c  crum create&delete   memory collection (not gc, but data age stuff)
```

The authors drew this line themselves. `credel.c`'s `grimlyreap()` / `reap()` machinery is **age-based LRU eviction** of in-memory crums — it writes old crums to disk to free RAM. It is not referential GC. Crums are never freed because their I-space content is unreferenced; they are freed because they are old.

---

#### 3. Disk-Level GC Infrastructure Exists — and Is Disabled

`backend/corediskout.c` contains two GC functions:

- `deletefullcrumandgarbageddescendents()` [line 358]
- `deletewithgarbageddescendents()` [line 388]

These traverse on-disk crum tree nodes and decrement refcounts via `changerefcount()`. When a refcount would reach zero, a disk block is eligible for freeing.

But the punchline is at `corediskout.c:410`:

```c
/*subtreefree(ptr);*/ /*12/04/86*/
```

The actual reclamation call was **commented out on December 4, 1986**. The traversal runs; nothing gets freed. This is the skeleton of a GC system with the collection step removed.

---

#### 4. The Context in Which Disk GC Is Called: Not Deletion

These GC functions are called only from `orglwrite()` [corediskout.c:328-355], which runs when a **modified orgl is persisted to disk**. The trigger is a copy-on-write update to the crum tree (writing a changed tree to a new disk location and decrementing the refcount on the old location). It is structural GC of the tree encoding — not semantic GC of content.

It is **never called from `dodeletevspan`**.

---

#### 5. `dodeletevspan` Never Touches I-Space

The full call chain for V-span deletion:

```
dodeletevspan()         [do1.c:158]
  → deletevspanpm()     [orglinks.c:145]
    → deletend()        [edit.c:31]  — operates on the SPANFILADE only
        → disown()      [genf.c:349] — removes crum from tree, restructure only
        → subtreefree() [edit.c:60]  — frees the V-space crum node in memory
```

`deletend` [edit.c:31-76] cuts the span out of the spanfilade (V↔I mapping). The **granfilade** (I-space content store) is never touched. The I-addresses that backed the deleted V-span remain in the granfilade, intact, with no pointer back to indicate they are now unreferenced.

---

#### 6. No Reverse Index Exists to Enable I-Space GC

`orglinks.c` converts V-spans → I-spans (`vspanset2ispanset`) and I-spans → V-spans (`ispan2vspanset`). The `ispan2vspanset` direction uses `retrieverestricted()` in `retrie.c`, which scans the spanfilade for any V-span that maps to a given I range. This is a forward query tool — not a maintained reverse index. To GC an I-address range, you would need to confirm that *no* V-span references it, requiring a full spanfilade scan. No such scan is ever initiated anywhere in the delete path.

---

#### 7. `levelpull()` — Tree Compaction Disabled

`backend/genf.c:318-342`:

```c
int levelpull(typecuc *fullcrumptr)
{
/*  typecuc *ptr; */
return(0);
/*
    if (!isfullcrum (fullcrumptr))
        gerror ("Levelpull not called with fullcrum.");
    if (fullcrumptr->numberofsons > 1)
        return;
    if (fullcrumptr->height <= 1)
        return;
    ptr = (typecuc *) findleftson (fullcrumptr);
    dspadd (&fullcrumptr->cdsp, &ptr->cdsp, &fullcrumptr->cdsp, fullcrumptr->cenftype);
    disown (ptr);
    fullcrumptr->height--;
    transferloaf (ptr, fullcrumptr);
    setwispupwards (fullcrumptr,1);
    freecrum (ptr);
*/
}
```

This was meant to collapse single-child enfilade nodes (reduce tree height after deletions make internal nodes redundant). It is a complete stub. Tree height only grows; it never shrinks.

---

### Summary

| Question | Finding | Evidence |
|---|---|---|
| Was GC of I-space ever designed? | Planned, named, not implemented | `coredisk.h:18-19` |
| Is the "grim reaper" GC? | No — explicitly called "data age stuff, not gc" | `NOTES:39` |
| Does disk-level GC infrastructure exist? | Exists, but the free step was commented out (12/04/86) | `corediskout.c:410` |
| Does V-span deletion reclaim I-addresses? | Never. `dodeletevspan` → `deletend` never touches granfilade | `do1.c:158`, `edit.c:31-76` |
| Is there a reverse I→V index to enable GC? | No. `ispan2vspanset` is a query, not a maintained structure | `orglinks.c`, `retrie.c` |
| Is tree compaction after deletion implemented? | No. `levelpull()` is a stub returning 0 | `genf.c:318` |

**Conclusion:** I-space is append-only and permanently retained in udanax-green — not as a philosophical commitment baked into the architecture, but as an artifact of incomplete implementation. The design contemplated GC (the `refcount` field exists; the function names say "garbage"); the structural machinery was partially built; and then the actual reclamation was commented out with a date stamp (1986) and never reinstated. What remains is a system that accumulates I-space content forever because the mechanism to do otherwise was never finished.
