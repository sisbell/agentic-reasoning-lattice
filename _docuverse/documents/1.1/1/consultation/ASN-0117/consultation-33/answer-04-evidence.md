## Question 4 [evidence]

> When DELETEVSPAN receives a span that begins before the document's first arranged V-position (or otherwise falls outside the arranged extent), does udanax-green reject the request, clip the span to the arranged run, or fail — and where in the call path is that check enforced?

## KB Synthesis

## DELETEVSPAN Outside the Arranged Extent

The KB does not describe an explicit out-of-bounds rejection path. Piecing together what is documented:

---

### Entry-Point Check: Width Only

[PRE-DELETE] (Finding 0040) is unambiguous:

> The only precondition enforced by `deletevspanpm()` is that the width is non-zero — `iszerotumbler(&vspanptr->width)` returns FALSE. There is no check preventing deletion of [any subspace].

No bounds check against the document's current V-extent exists. An out-of-range span with non-zero width passes the gate.

---

### Phase 1 (Cutting): No Crums, No Action

[ST-DELETE] (Finding 0075) establishes that `slicecbcpm` fires only when `whereoncrum() == THRUME` — strictly interior to a crum:

> When a DELETE boundary aligns with the crum's grasp → `ONMYLEFTBORDER`; with the reach → `ONMYRIGHTBORDER`. Both skip `slicecbcpm`.

A span that begins before all content crums would yield `TOMYLEFT` for both blades against every crum. No cutting is triggered. [SS-WHEREONCRUM] documents the five-way return: `TOMYLEFT (-2)` when `address < grasp`.

---

### Phase 2 (Classify/Shift): Exponent Guard Prevents Inadvertent Shifts

[ST-DELETE] (Finding 0055) and [FC-SUBSPACE] (Finding 0055/0067) document the `strongsub` exponent guard:

> When the subtrahend's exponent is strictly less than the minuend's exponent, `strongsub` returns the minuend unchanged without performing any subtraction.

V-address positions in the text subspace (`1.x`) have `exp = 0`. A deletion span beginning before the text subspace (e.g., at `0.5`) has a width with `exp = -1`. The guard `b.exp < a.exp` holds, so all text crums that would otherwise be classified as Case 2 (shift-left) are returned unchanged. This is explicitly described as **accidental** protection — it is arithmetic happenstance, not a designed bounds guard [INT-DELETE-SUBSPACE-ASYMMETRY].

---

### Net Behavior: Silent No-Op

For a span entirely before the document's first V-position (same-subspace or cross-subspace):

| Phase | What happens |
|---|---|
| Entry check | Passes (non-zero width only checked) |
| Phase 1 cutting | No crums in range → no `slicecbcpm` calls |
| Phase 2 removal | No crums in range → nothing disowned/freed [ST-DELETE, Finding 0064] |
| Phase 2 shift | Crums after range: exponent guard prevents shift [FC-SUBSPACE, Finding 0055] |
| Result | Silent success, document state unchanged |

The operation returns without error, modifies no enfilade state, and produces no observable effect. [EC-ERROR-ABORT] confirms the system only aborts on internal contract violations (null pointers, unexpected types), not on semantically no-op operations.

---

### Caveat: Same-Exponent Span Just Before Content

The exponent guard only fires when deletion-width exponent < content-displacement exponent. If a span begins just below the first crum at the **same** exponent (e.g., delete `[1.05, 1.1)` when content starts at `1.1`), Phase 2 would classify those crums as Case 2 and attempt subtraction. Whether that subtraction produces a negative V-position depends on the magnitude relationship — [INV-POOM-BIJECTIVITY] and [PRE-DELETE] (Finding 0053) note that negative V-positions can be produced and silently stored, making those crums invisible but not removed.

The KB has no golden-test evidence for this precise edge case.

---

## Code Exploration

I now have everything needed for a complete answer. Here it is:

---

## DELETEVSPAN Out-of-Range Span Handling

**Short answer:** udanax-green does **not** reject or clip an out-of-range span. It silently corrupts the document by misapplying position offsets to whatever crums fall "after" the bogus cut positions. The only guard in the path is a zero-width check, and it fires before any position arithmetic is evaluated.

---

### Call Path

```
fns.c:deletevspan()
  → orglinks.c:deletevspanpm()        ← only guard lives here
    → edit.c:deletend()
      → ndinters.c:newfindintersectionnd()   ← stub: always returns root
      → ndcuts.c:makecutsnd()
      → edit.c:deletecutsectionnd()    ← classifies each crum, no range guard
        → retrie.c:whereoncrum()
```

---

### 1. `fns.c:333` — FEBE Handler (protocol anomaly)

```c
void deletevspan(typetask *taskptr)
{
    (void) getdeletevspan (taskptr, &docisa, &vspan);
    putdeletevspan (taskptr);                          // ← success sent FIRST
    if (!dodeletevspan (taskptr, &docisa, &vspan))
        fprintf(stderr,"deletevspan failed \n");
}
```

`putdeletevspan` at line 340 sends the success response to the client **before** `dodeletevspan` is called at line 341. A commented-out original at lines 319–331 shows the intended design:

```c
/* if (
   getdeletevspan (taskptr, &docisa, &vspan)
&& dodeletevspan (taskptr, &docisa, &vspan))
        putdeletevspan (taskptr);
  else
        putrequestfailed (taskptr); */
```

The production handler unconditionally acknowledges every DELETEVSPAN before doing any work. A client cannot distinguish a successful delete from a silent corruption.

---

### 2. `orglinks.c:145` — The Only Bounds Check

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))      // line 147
        return (FALSE);                        // line 148
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);  // line 149
    logbertmodified(docisaptr, user);          // line 150
    return (TRUE);
}
```

`iszerotumbler` at line 147 is the **only validation** in the entire DELETEVSPAN path. It rejects spans with zero width and returns FALSE (which, per `fns.c:341`, only prints a stderr message). There is no check that `vspan->stream` falls within the document's arranged V-extent. Non-zero-width spans, regardless of position, are passed directly to `deletend`.

`acceptablevsa` (`do2.c:110–113`) exists but is only called from `docopy`/`docopyinternal` (`do1.c:56`, `76`), not from `dodeletevspan`. Even there, it returns `TRUE` unconditionally:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

---

### 3. `ndinters.c:38` — The Intersection Stub

```c
int newfindintersectionnd(typecuc *fullcrumptr, typeknives *knives, typecuc **ptrptr, typewid *offset)
{
    *ptrptr = fullcrumptr;
    clear (offset,sizeof(*offset));
}
```

This function — which should descend the enfilade to find the subtree spanning both knife positions — is a stub. It unconditionally sets `father = root` and `offset = 0`. The commented-out original `findintersectionnd` (lines 18–37) would have walked down the tree. Because the stub skips that descent, `deletend` always iterates the full set of root's direct children regardless of where the deletion span lies.

---

### 4. `edit.c:31` — `deletend` Propagates the Out-of-Range Cut

```c
int deletend(typecuc *fullcrumptr, tumbler *origin, tumbler *width, INT index)
{
    ...
    movetumbler (origin, &knives.blades[0]);           // line 40: blade[0] = span start
    tumbleradd (origin, width, &knives.blades[1]);     // line 41: blade[1] = span end
    knives.nblades = 2;
    knives.dimension = index;
    makecutsnd (fullcrumptr, &knives);                 // line 44: split crums at both blades
    newfindintersectionnd (fullcrumptr, &knives, &father, &foffset);  // line 45: stub → root
    ...
    for (ptr = (typecuc *) findleftson (father); ptr; ptr = next) {
        switch (deletecutsectionnd ((typecorecrum*)ptr, &fgrasp, &knives)) {
          case 0: break;                               // line 56-57: leave alone
          case 1: disown(ptr); subtreefree(ptr); break;// line 58-61: delete crum
          case 2:                                      // line 62-65: adjust position
            tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
            break;
        }
    }
```

`logbertmodifiedforcrum` is called inside `makecutsnd` (`ndcuts.c:19`) immediately — the document is marked dirty before any range check could fire.

---

### 5. `edit.c:235` + `retrie.c:345` — What Out-of-Range Looks Like to `deletecutsectionnd`

Constants (`common.h:86–90`):

| Symbol | Value |
|---|---|
| `TOMYLEFT` | −2 |
| `ONMYLEFTBORDER` | −1 |
| `THRUME` | 0 |
| `ONMYRIGHTBORDER` | 1 |
| `TOMYRIGHT` | 2 |

`whereoncrum` for SPAN/POOM (`retrie.c:354–372`):

```c
tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);   // absolute start
tumbleradd(&left, &ptr->cwid.dsas[index], &right);                  // absolute end
// address < left  → TOMYLEFT
// address == left → ONMYLEFTBORDER
// left < address < right → THRUME
```

`deletecutsectionnd` (`edit.c:235–248`) iterates knives from highest (blade[1]) to lowest (blade[0]):

```c
for (i = knives->nblades-1; i >= 0; --i) {
    cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
    if (cmp == THRUME)                  return (-1);  // crum not yet split — error
    else if (cmp <= ONMYLEFTBORDER)     return (i+1); // caught by this blade
}
return (0);
```

`cmp <= ONMYLEFTBORDER` means cmp ≤ −1, catching both `TOMYLEFT` (−2) and `ONMYLEFTBORDER` (−1).

**Concrete scenario — span entirely before the document:**

- Deletion span: V = 1.0 to 3.0 (width = 2); document first crum at V = 5.0, ending at 8.0.
- `makecutsnd`: both blades (1.0 and 3.0) are `TOMYLEFT` relative to every crum → no splits made.
- `deletecutsectionnd(crum[5,8], 0, {blade[0]=1, blade[1]=3})`:
  - i=1: `whereoncrum(crum[5,8], 0, 3, V)` → address 3 < left 5 → `TOMYLEFT` = −2 ≤ −1 → **return 2**
- Case 2 fires: `tumblersub(&ptr->cdsp.dsas[V], width, &ptr->cdsp.dsas[V])`
  - Crum's V-displacement: 5 − 2 = **3**. Document is now corrupted.

**Concrete scenario — span straddles document start:**

- Deletion span: V = 1.0 to 7.0 (width = 6); document crum at [5, 8].
- `makecutsnd`: blade[1]=7 falls inside crum [5,8] → splits into [5,7] and [7,8].
- For crum [5,7]:
  - i=1: `whereoncrum(crum[5,7], 0, 7)` → 7 == right → `ONMYRIGHTBORDER` → not caught → continue
  - i=0: `whereoncrum(crum[5,7], 0, 1)` → 1 < 5 → `TOMYLEFT` ≤ −1 → **return 1** → crum deleted
- For crum [7,8]:
  - i=1: `whereoncrum(crum[7,8], 0, 7)` → 7 == left → `ONMYLEFTBORDER` = −1 ≤ −1 → **return 2**
  - Crum displacement: 7 − 6 = **1**. Content that was at V=7–8 is now at V=1–2. Corrupted.

---

### Summary

| Stage | File & Line | What Happens |
|---|---|---|
| FEBE handler | `fns.c:340` | Success response sent **before** delete executes |
| Only guard | `orglinks.c:147–148` | Rejects zero-width span only; no position bounds check |
| Intersection finding | `ndinters.c:38–42` | Stub — always returns root with zero offset; no range verification |
| Cut placement | `ndcuts.c:15–31` | Attempts to split crums at blade positions; blades outside all crums produce no splits |
| Crum classification | `edit.c:235–248` | `TOMYLEFT` on the high blade triggers case 2 (offset adjust) on crums that should be untouched |
| Offset corruption | `edit.c:63` | `tumblersub` shifts in-document crums by the out-of-range deletion width |

There is no rejection and no clipping. A span that begins before the document's first arranged V-position is processed as if it were valid: the backend marks the document modified, sends the client a success response, then adjusts crum displacements by the full span width — including any out-of-range prefix — producing a silently corrupted enfilade.
