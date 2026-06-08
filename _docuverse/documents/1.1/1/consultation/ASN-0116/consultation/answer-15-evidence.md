## Question 15 [evidence]

> When typing characters sequentially at adjacent positions, does only the first character cost +2 crums while subsequent ones coalesce via `isanextensionnd`'s ONMYRIGHTBORDER case at +0 cost?

## KB Synthesis

Yes, exactly. The mechanics are confirmed across several KB entries:

**First character at a new interior position (cost +2):**

`whereoncrum` returns THRUME (strictly interior), so `makegappm` fires and constructs the two-blade knife. The existing crum splits into two pieces, and a new crum is created for the inserted character — net +2 crums. [SS-WHEREONCRUM], [ST-INSERT] Finding 0062

**Each subsequent character at the adjacent position (cost +0):**

The previous character's crum has `reach = v+1`. When inserting at `v+1`, `makegappm`'s early-exit guard fires:

```c
if (... tumblercmp(&origin->dsas[V], &reach.dsas[V]) != LESS) return(0);
```

`origin == reach` → not LESS → early exit, no knife cut. Then `isanextensionnd` checks two conditions: (1) same `homedoc`, (2) `crum.reach == new_origin`. Both hold, so the crum is extended in place. +0 crums. [ST-INSERT] Finding 0062

**The formal bound:**

```
c ≤ 1 + 2C + 3R + 3P
```

where C counts distinct cursor repositionings. Continuous typing at the same cursor is one C=1 event paying +2 once, then +0 for all N subsequent characters. [INV-CRUM-BOUND] Finding 0062

Note that CREATELINK between two INSERT sequences breaks this coalescing — it allocates an orgl in the same I-address space, so the next INSERT's `isanextensionnd` check fails (I-address gap), forcing a new crum at +2 cost again. [EC-DEEPLY-ORPHANED-LINK / INT-LINK-INSERT] Finding 0063

---

## Code Exploration

Now I have all the source I need for a complete, cited answer.

---

## Analysis: Sequential Character Insertion and Crum Cost

The claim is **substantially correct in its effects** but contains two mechanical inaccuracies worth stating precisely.

---

### The First-Character Path: +2 Crums

Each `insert` call goes through `fns.c:84` → `doinsert` (`do1.c:87`) → two parallel enfilade modifications:

**1. Granfilade (permascroll text storage): `insertseq` at `insert.c:17`**

`inserttextgr` (`granf2.c:83`) allocates a permascroll address via `findisatoinsertgr`, then calls `insertseq`. For the first character into an existing document, `retrievecrums` finds the current terminal crum. The extension check at `insert.c:34-42`:

```c
if (info->infotype == GRANTEXT
&& ptr->cinfo.infotype == GRANTEXT
&& ptr->cinfo.granstuff.textstuff.textlength < GRANTEXTLENGTH) {
    if (!fillupcbcseq (ptr, &nextaddress, info)) {
        return(0);  // packed in-place
    }
}
```

If this fails (non-GRANTEXT terminal, or full crum), execution falls through to `insert.c:43-46`:

```c
reserve ((typecorecrum*)ptr);
new = createcrum (0,(INT)ptr->cenftype);  // +1 GRAN crum
reserve (new);
adopt (new, RIGHTBRO, (typecorecrum*)ptr);
```

**+1 GRAN crum** created via `createcrum`.

**2. POOM enfilade (virtual space mapping): `insertcbcnd` at `insertnd.c:242`**

`doinsert` → `docopy` → `insertpm` → `insertnd` (`insertnd.c:15`) → `insertmorend` → `insertcbcnd`.

In `insertcbcnd`, `isanextensionnd` is tested first. On the first character, no existing crum spans the insertion point, so `isanextensionnd` returns FALSE. Execution proceeds to `insertnd.c:260-262`:

```c
new = createcrum (0, (INT)father->cenftype);  // +1 POOM crum
reserve (new);
adopt (new, SON, (typecorecrum*)father);
```

**+1 POOM crum** created via `createcrum`.

**Total first character: +1 GRAN crum + +1 POOM crum = +2 crums.** ✓

---

### Subsequent Adjacent Characters: +0 via Two Distinct Mechanisms

**POOM side — `isanextensionnd` (`insertnd.c:301-309`):**

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
  typedsp grasp, reach;
  bool lockeq();
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

`prologuend` (`retrie.c:334`) computes:
- `grasp = offset + ptr->cdsp` — absolute start of the crum
- `reach = grasp + ptr->cwid` — absolute right boundary

`lockeq(reach.dsas, originptr->dsas, ...)` returns TRUE if `reach == origin`, i.e., the new insertion starts exactly where the existing crum ends. When TRUE, `insertcbcnd` (`insertnd.c:249-258`) executes:

```c
if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
    dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
    ivemodified (ptr);
    setwispupwards (father,1);
    ...
    return(FALSE);
}
```

No `createcrum`. Just `dspadd` extending the existing POOM crum's width. **+0 POOM crums.** ✓

**GRAN side — `fillupcbcseq` (`insert.c:75-103`):**

For the second character, `retrievecrums` at `lsa_second = lsa_first + 1` lands on the current GRANTEXT crum (the previous character's crum is now the terminal region). The extension check at `insert.c:34-42` succeeds as long as `textlength < GRANTEXTLENGTH`, and `fillupcbcseq` packs the character in-place:

```c
movmem(&info->granstuff.textstuff.textstring,
       (char*)(&(ptr->cinfo.granstuff.textstuff))+crumlength,
       textlength);
ptr->cinfo.granstuff.textstuff.textlength = crumlength + textlength;
```

No `createcrum`. **+0 GRAN crums** (until the crum fills to `GRANTEXTLENGTH`). ✓

---

### Mechanical Corrections to the Question's Framing

**Correction 1: `isanextensionnd` does NOT use `ONMYRIGHTBORDER`.**

`ONMYRIGHTBORDER = 1` is defined at `common.h:89` and returned by `whereoncrum` (`retrie.c:368-369`) when `address == reach`. But `isanextensionnd` at `insertnd.c:301` never calls `whereoncrum`. It directly calls `prologuend` + `lockeq(reach, origin)` — a raw equality test across all dimensions of the displacement vector. The effect is identical to "origin is on my right border," but the code does not go through `whereoncrum`.

**Correction 2: The +0 GRAN cost is handled by `fillupcbcseq`, not `isanextensionnd`.**

`isanextensionnd` is POOM-only. The granfilade coalescing is a separate mechanism in `insertseq` (`insert.c:34-42`). These are two independent optimizations running in parallel across two different enfilades.

---

### One Caveat: `makegappm` for Appending

`insertnd` (`insertnd.c:53-55`) always calls `makegappm` before `doinsertnd` for POOM insertions. For appending at the right end of existing text, `makegappm` (`insertnd.c:140-143`) short-circuits early:

```c
if (iszerotumbler (&fullcrumptr->cwid.dsas[V])
|| tumblercmp (&origin->dsas[V], &grasp.dsas[V]) == LESS
|| tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);    /* this if for extensions to bc without calling cut*/
```

When `origin >= reach` (appending past the current right boundary), `makegappm` returns 0 immediately with no cuts, no splits, no additional crums. The "extension to bc without calling cut" comment confirms this is the intended append path.

---

### Summary

| Event | GRAN crum delta | POOM crum delta | Mechanism |
|---|---|---|---|
| First character | +1 (`insertseq`:`createcrum`, `insert.c:44`) | +1 (`insertcbcnd`:`createcrum`, `insertnd.c:260`) | +2 total |
| Subsequent adjacent | +0 (`fillupcbcseq`, `insert.c:88`) | +0 (`dspadd` after `isanextensionnd`, `insertnd.c:251`) | +0 total |
| GRAN crum full | +1 (new crum in `insertseq`) | +0 (POOM still extends) | +1 total |

The "+2 / +0" pattern is real. The attribution to "`isanextensionnd`'s ONMYRIGHTBORDER case" is conceptually right — `isanextensionnd` checks right-border adjacency — but it implements this via `lockeq(reach, origin)` at `insertnd.c:308`, not via `whereoncrum` + `ONMYRIGHTBORDER`. And the GRAN side's +0 is entirely separate, handled by `fillupcbcseq` in `insert.c`.
