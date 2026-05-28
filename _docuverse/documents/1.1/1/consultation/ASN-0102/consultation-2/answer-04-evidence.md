## Question 4 [evidence]

> When two consecutive content references in a single COPY resolve to content sharing one origin (equal `homedoc`) and abutting in I-space across the boundary, does `docopy`/`insertspanf` (via `isanextensionnd`) coalesce them into one crum, or still emit a separate crum per reference?

## KB Synthesis

**Yes, they coalesce into one POOM crum.**

`isanextensionnd` checks exactly two conditions [ST-VCOPY / Finding 0046]:
1. Same `homedoc` — satisfied by premise
2. `new.I-origin == existing.crum.I-reach` — satisfied because the references are I-abutting

When both hold, `insertnd.c:243` extends the existing crum's width in place rather than allocating a new one. Since the two references are inserted at consecutive V-positions (contiguous in V as well), the second `insertpm` call finds the first crum's reach at exactly the right position and coalesces.

**However, the spanf side does not coalesce.** `insertspanf` loops over the ispanset and makes one `insertnd` call per `typeispan` struct [SS-DOCISPAN / Finding 0047]. If the two references arrive as separate I-span entries in the ispanset, they produce two DOCISPAN spanf entries — there is no `isanextensionnd`-style extension mechanism described for the spanfilade.

**Summary:** POOM gets one coalesced crum (via `isanextensionnd`); spanf gets two entries (per-span granularity). The observability of this split is: `compare_versions` sees a single contiguous span [ST-VCOPY / Finding 0033], but DOCISPAN storage cost reflects the number of distinct I-spans in the input.

---

## Code Exploration

I have everything I need. Here is the complete answer.

---

## Answer: Yes — Consecutive Abutting Same-Origin Spans Are Coalesced

The coalescing happens in `insertcbcnd` via `isanextensionnd`. Here is the full traced path.

---

### 1. `docopy` — Entry Point (`backend/do1.c:45–65`)

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    ...
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)     // do1.c:60
    && insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)  // do1.c:62
    ...
}
```

`docopy` converts the specset to an I-span set and calls `insertspanf` with the full list.

---

### 2. `insertspanf` — Loops Per-Reference (`backend/spanf1.c:15–54`)

```c
for (; sporglset; sporglset = ...) {          // spanf1.c:25
    ...extract lstream, lwidth, linfo.homedoc...
    insertnd(taskptr,(typecuc*)spanfptr,       // spanf1.c:51
             &crumorigin,&crumwidth,&linfo,SPANRANGE);
}
```

**Critical point:** `insertspanf` calls `insertnd` once **per item** in the loop. There is no coalescing logic here. The coalescing decision is deferred to `insertnd` → `insertcbcnd`.

---

### 3. `insertnd` / `doinsertnd` / `insertmorend` — Dispatching

`insertnd` (`backend/insertnd.c:15`) dispatches SPAN to `doinsertnd` at line 63:

```c
case SPAN:
    bothertorecombine=doinsertnd(fullcrumptr,origin,width,infoptr,index); // insertnd.c:63
```

`doinsertnd` (`insertnd.c:185`) calls `insertmorend` for a non-empty enfilade:

```c
return(insertmorend (father, &offset, origin, width, infoptr, index)); // insertnd.c:196
```

`insertmorend` (`insertnd.c:219`) recurses until height == 1, then calls:

```c
if (father->height == 1) {
    return(insertcbcnd (father, &grasp, origin, width, infoptr)); // insertnd.c:231
}
```

---

### 4. `insertcbcnd` — The Coalescing Decision (`backend/insertnd.c:242–275`)

```c
INT insertcbcnd(typecuc *father, typedsp *grasp, typewid *origin, typewid *width, type2dbottomcruminfo *infoptr)
{
    for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {  // insertnd.c:249
        if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) { // insertnd.c:250
            dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype); // insertnd.c:251
            ivemodified (ptr);
            setwispupwards (father,1);
            ...
            return(FALSE); // insertnd.c:257
        }
    }
    // No match — create a new crum:
    new = createcrum (0, (INT)father->cenftype);    // insertnd.c:260
    ...
}
```

When processing the **second** I-span reference, `insertcbcnd` iterates over existing bottom crums. If `isanextensionnd` returns `TRUE` for the crum laid down by the **first** reference, it **widens that crum's `cwid`** (line 251) and returns immediately — no new crum is created.

---

### 5. `isanextensionnd` — The Two-Part Test (`backend/insertnd.c:301–309`)

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    typedsp grasp, reach;
    bool lockeq();
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc)) // insertnd.c:305
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);               // insertnd.c:307
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype))); // insertnd.c:308
}
```

Two conditions, both required:

**Condition 1 (`insertnd.c:305`):** The incoming `infoptr->homedoc` must equal the existing crum's `c2dinfo.homedoc` — same origin document.

**Condition 2 (`insertnd.c:308`):** The incoming span's I-space `originptr` must equal the `reach` of the existing crum — i.e., the new span starts exactly where the old crum ends (abutting in I-space). `prologuend` computes `reach = grasp + crum_offset + crum_width`, so this is a precise adjacency check with no gap tolerance.

---

### Synthesis

When `docopy` processes a COPY containing two consecutive content references where:

- Both resolve to the same `homedoc` (equal origin document tumbler), **and**
- The second reference's I-space origin equals `first_origin + first_width` (abutting, no gap),

then on the second call to `insertnd` (from the `insertspanf` loop at `spanf1.c:51`), `insertcbcnd` finds the first crum via `isanextensionnd`, and **widens it in place** (`insertnd.c:251`). No second crum is created.

If either condition fails — different `homedoc`, or a gap/overlap in I-space — `isanextensionnd` returns `FALSE`, the loop exhausts without a match, and `insertcbcnd` allocates a fresh crum at lines 260–274.

**The coalescing is exact and unconditional for the two-condition case.** There is no heuristic; the logic is purely structural: equal `homedoc` + I-space reach == next origin → one crum, widened.
