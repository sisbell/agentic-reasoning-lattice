## Question 18 [gregory]

> When COPY detects I-address contiguity via `isanextensionnd` and extends an existing POOM crum rather than creating a new one, does the extended crum's I-displacement remain identical to the original, with only the width growing — or does the extension recompute the displacement?

## KB Synthesis

The I-displacement remains identical — only the width grows.

The condition `isanextensionnd` checks is that the new content's I-address origin equals the existing crum's **reach** (i.e., `crum.origin + crum.width`) [ST-INSERT, Finding 0062]:

> `isanextensionnd()` checks two conditions: (1) the new mapping has the same `homedoc` as an existing crum, and (2) the new mapping starts exactly where the existing crum ends (contiguous in both V and I dimensions). If both hold, the existing crum's **width is extended in place** — no new crum is allocated.
> — `insertnd.c:293-301` (check), `insertnd.c:243` (extension)

[PRE-COPY, Finding 0046] confirms the same path for COPY specifically:

> The new mapping starts exactly where the existing crum ends (contiguous in both V and I dimensions). If both hold, the existing crum's width is extended in place.

The logic is self-consistent: the extension precondition is `new_origin == crum.origin + crum.width`. If the displacement were recomputed to point at the new content, the original I-addresses covered by the crum would be orphaned. Instead, the crum's I-origin stays fixed at its original value, the I-width grows to `old_width + new_width`, and the crum now spans `[origin, origin + old_width + new_width)` — absorbing the appended content contiguously to the right.

The same holds for the V-dimension: [SS-INSERT-VWIDTH-ENCODING, Finding 0076] confirms V-width and I-width are independently encoded but represent the same numeric value, both growing by the same amount during extension.

---

## Code Exploration

I now have everything needed for a complete answer. Here it is:

---

## Answer: The I-displacement is never touched. Only the width grows.

### Execution path

`docopy` [`do1.c:45`] → `insertpm` → `insertnd` [`insertnd.c:15`] → `doinsertnd` [`insertnd.c:185`] → `insertmorend` [`insertnd.c:219`] → `insertcbcnd` [`insertnd.c:242`] (once `father->height == 1`).

---

### `insertcbcnd`: the extension branch

```c
// insertnd.c:249-258
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
        dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);  // line 251
        ivemodified (ptr);
        setwispupwards (father,1);
        ...
        return(FALSE);
    }
}
```

Line 251 is the **only mutation** that occurs on the extension path. It does:

```
ptr->cwid = ptr->cwid + width
```

`ptr->cdsp` — the crum's displacement (containing both its I- and V-address offsets) — **is not assigned, not read-for-write, not touched at all.**

---

### What `isanextensionnd` actually checks

```c
// insertnd.c:301-309
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
  typedsp grasp, reach;
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

`prologuend` [`retrie.c:334-339`] computes:

```c
grasp = offset + ptr->cdsp    // absolute start of the crum
reach = grasp  + ptr->cwid    // absolute end   of the crum
```

Then `lockeq` compares `reach` to `origin` across `dspsize(POOM) = 2` tumblers [`wisp.h:26-27`]:

```c
#define DSPSIZEPM 2   // wisp.h:26 — covers both I (index 0) and V (index 1)
```

So contiguity is verified in **both** I and V simultaneously. The extension fires only when `reach.dsas[I] == origin.dsas[I]` AND `reach.dsas[V] == origin.dsas[V]`.

---

### What `dspadd` does to the width

```c
// wisp.c:15-18
int dspadd(typedsp *a, typewisp *b, typedsp *c, INT enftype)
{
    lockadd (a->dsas, b->dsas, c->dsas, (unsigned)dspsize(enftype));
}
```

`lockadd` loops over `dspsize(POOM) = 2` tumblers and calls `tumbleradd` on each [`wisp.c:269-273`]. The call at `insertcbcnd:251` is:

```c
dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
//       src=cwid    src2=new_width  dst=cwid   type=POOM
```

Result: `ptr->cwid.dsas[I] += width->dsas[I]`, `ptr->cwid.dsas[V] += width->dsas[V]`.

---

### Summary

| Field | Extension path |
|-------|---------------|
| `ptr->cdsp.dsas[I]` (I-displacement) | **Unchanged** — not touched |
| `ptr->cdsp.dsas[V]` (V-displacement) | **Unchanged** — not touched |
| `ptr->cwid.dsas[I]` (I-width) | **Grows** — `+= width->dsas[I]` |
| `ptr->cwid.dsas[V]` (V-width) | **Grows** — `+= width->dsas[V]` |

The I-displacement of the extended crum is left **identical to the original**. The extension is purely additive to the width field; no displacement recomputation occurs. This is consistent with the contiguity precondition: because `isanextensionnd` already confirmed that `reach == origin` (the existing crum's right edge exactly abuts the new content's left edge), the crum's origin (`cdsp`) needs no adjustment — the crum already starts in the right place; it simply needs to be made wider.
