## Question 14 [gregory]

> Under what specific conditions does `tumblersub` during DELETE shifting produce a negative V-position tumbler — is it only when the deletion width's mantissa exceeds the surviving entry's V-displacement mantissa at the same exponent, and does the system continue to function correctly with negative V-positions in the POOM?

## KB Synthesis

## Conditions for Negative V-Position Tumblers from DELETE

Two conditions must both hold simultaneously for `tumblersub` to produce a negative V-position during DELETE's Case 2 shifting:

**Condition 1 — Exponent match.** The deletion width's exponent must equal the surviving entry's V-displacement exponent. `deletend` calls `tumblersub` which delegates to `strongsub`. The `strongsub` exponent guard at `tumble.c:534-547` returns the minuend unchanged when `width.exp < entry.vpos.exp` — no subtraction occurs. This is why cross-subspace deletions cannot produce negative link-subspace entries: text deletion widths have exponent -1, while link crums at `2.x` have exponent 0. `strongsub(2.1, 0.3)` simply returns `2.1` [ST-DELETE, FC-SUBSPACE, INT-DELETE-SUBSPACE-ASYMMETRY].

**Condition 2 — Width exceeds displacement.** At the same exponent, the deletion width's mantissa must exceed the surviving entry's V-displacement mantissa. When both operands share the same exponent and `b > a` in absolute value, `tumblersub` produces `sign=1` (negative) with the magnitude of `b - a`. Since `tumblercmp` treats negative tumblers as strictly less than all positive tumblers and zero, the resulting entry sorts before all valid V-addresses [SS-TUMBLER Finding 0053].

Concretely: a text crum at V-displacement `0.4` (exp=-1) struck by a deletion of width `0.6` (exp=-1) would yield `sign=1, magnitude=0.2` — a negative tumbler stored back into `cdsp.dsas[V]` at `edit.c:63`.

### Scope Narrowed by Finding 0055

Finding 0055 corrects Finding 0053's broader claim. The negative V-position hazard applies only to **same-subspace, same-exponent** entries where the deletion width exceeds the entry's displacement. The often-observed empty endsets after deletion are more commonly caused by a different mechanism: I-address mappings being removed from the POOM via `disown` + `subtreefree` (Case 1 in `deletend`, for entries whose grasp falls within the deletion range) rather than their V-position going negative [EC-DEEPLY-ORPHANED-LINK].

### Behavior with Negative V-Positions in the POOM

The system does not detect, reject, or clean up negative V-position entries:

- **No integrity check.** `deletevspanpm` only verifies non-zero width before calling `deletend`. No guard exists on the resulting post-shift position [PRE-DELETE].
- **Entry persists as dead state.** The POOM tree retains the entry at its negative displacement. `tumblercmp` places it before all positive V-addresses, so it is unreachable by any V-space query that uses positive start positions [INV-POOM-BIJECTIVITY].
- **FOLLOWLINK returns empty.** The I-to-V conversion path at `orglinks.c:446-448` calls `retrieverestricted` against the document's POOM. A negative V-position has no match for positive-address queries, so the address is silently dropped — FOLLOWLINK succeeds but returns empty endsets [EC-DEEPLY-ORPHANED-LINK, INV-ITOV-FILTERING].
- **FINDLINKS cannot locate the link.** Since the entry's V-position is negative and V-space queries operate over non-negative addresses, the link cannot be rediscovered through content-identity search either [EC-DEEPLY-ORPHANED-LINK].
- **Cannot be deleted.** A subsequent DELETEVSPAN targeting the link's original position (e.g., `2.1`) will not reach the entry, because the entry now resides at a negative V-position. The leaked entry is irrecoverable through normal operations.
- **INV-POOM-BIJECTIVITY is violated.** The POOM's intended bijection from V-addresses to I-addresses holds only for non-negative V-addresses. The spec must weaken the bijectivity invariant to: `poom_d restricted to non-negative V-addresses is a bijection` [INV-POOM-BIJECTIVITY].

The system continues to function — it does not crash — but the affected link enters a permanently unreachable state distinct from both normal orphaning (content deleted, POOM entry cleanly removed or at valid position) and reverse orphaning (POOM entry cleanly removed via DELETEVSPAN) [EC-REVERSE-ORPHAN].

---

## Code Exploration

I now have the complete picture. Here is the full answer.

---

## `tumblersub` During DELETE: Negative V-Position Conditions and Structural Safety

### The Exact Site

The `tumblersub` call in question is at `edit.c:63`, inside `deletend` (`edit.c:31`):

```c
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    /* This will get set to modified in setwisp */
    break;
```

This is reached for every crum classified "case 2" by `deletecutsectionnd` — crums that survive the deletion and must shift leftward.

---

### How Delete Gets Here

Call chain: `dodeletevspan` (`do1.c:158`) → `deletevspanpm` (`orglinks.c:145`) → `deletend` (`edit.c:31`).

`deletevspanpm` (`orglinks.c:149`) calls:
```c
deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
```

Inside `deletend`, two knife positions are set (`edit.c:40-41`):
```c
movetumbler (origin, &knives.blades[0]);
tumbleradd (origin, width, &knives.blades[1]);
```

After `makecutsnd` splits the tree at both knife positions, `newfindintersectionnd` finds the deepest common-ancestor node (`father`) and its accumulated absolute V-offset (`foffset`). Then (`edit.c:46`):
```c
prologuend ((typecorecrum*)father, &foffset, &fgrasp, (typedsp*)NULL);
```
which computes `fgrasp.dsas[V] = foffset.dsas[V] + father->cdsp.dsas[V]` — the absolute V-start of the father's subtree.

---

### What `deletecutsectionnd` "case 2" Means

`deletecutsectionnd` (`edit.c:235`) iterates knives from i=1 (deletion end) down to i=0 (deletion start). For POOM/SPAN nodes, `whereoncrum` (`retrie.c:355-372`) computes:
```c
tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);   // absolute start
tumbleradd(&left, &ptr->cwid.dsas[index], &right);                 // absolute end
```
and returns TOMYLEFT / ONMYLEFTBORDER / THRUME / ONMYRIGHTBORDER / TOMYRIGHT.

Case 2 means: checking knife 1 (deletion end = `origin + width`) returns ≤ ONMYLEFTBORDER, i.e., the crum's absolute left border is at or before the deletion end address. Combined with not matching case 1, this means **the crum lies entirely to the right of or at the deletion end** — it survives and must be shifted left by `width`.

---

### The Precise Negative-V Condition

The shift is:
```c
tumblersub(&ptr->cdsp.dsas[V], width, &ptr->cdsp.dsas[V])   // edit.c:63
```

`tumblersub` (`tumble.c:406`):
```c
int tumblersub(tumbler *aptr, tumbler *bptr, tumbler *cptr) {
    ...
    movetumbler (bptr, &temp);
    temp.sign = !temp.sign;
    tumbleradd (aptr, &temp, cptr);
    tumblerjustify (cptr);
}
```

In `functiontumbleradd` (`tumble.c:365`), when `|a| < |b|`:
```c
} else {
    weaksub (bptr, aptr, cptr);
    cptr->sign = bptr->sign;  // bptr = temp (sign=1), so cptr->sign = 1
```

**The result is negative (sign=1) if and only if `|ptr->cdsp.dsas[V]| < |width|`.**

To be precise about the mantissa comparison: `abscmp` (`tumble.c:87`) first compares exponents; if equal, it compares mantissa arrays element-by-element. So the question is mantissa-centric **when the exponents are equal**: `ptr->cdsp.dsas[V].mantissa[0] < width.mantissa[0]`. When exponents differ, the lower exponent is automatically smaller in `abscmp`.

**This situation arises structurally** when the `father` node found by `newfindintersectionnd` has already accumulated an absolute V-offset (`fgrasp.dsas[V]`) strictly greater than the deletion start `origin`. In that case:
- A crum `ptr` can have a small relative displacement `ptr->cdsp.dsas[V]` — small relative to `father` — while still having an absolute position `fgrasp.dsas[V] + ptr->cdsp.dsas[V]` that lies beyond the deletion end.
- The shift subtracts the full `width` from the small relative displacement, producing a negative result.

Concretely: if `fgrasp.dsas[V] = 5`, `ptr->cdsp.dsas[V] = 2`, `origin = 1`, `width = 4` (deletion end = 5), then absolute position = 7 ≥ 5 (case 2 fires), but `new_cdsp = 2 − 4 = −2`.

The commented-out debug code at `tumble.c:407-416` confirms this was observed and accepted:
```c
/*
    if(aptr->sign || bptr->sign) {
        fprintf(stderr,"TUMBLERSUB NEG IN \n");
        ...
    }
*/
```
And at `tumble.c:432-438`:
```c
/*
    if (cptr->sign) {
        fprintf(stderr,"TUMBLERSUB NEGATIVE OUTPUT\n");
        ...
    }
*/
```
These were removed as debug noise, not as error handlers — the negative output was deliberate.

---

### Does `tumblercheck` Catch Negative Displacements?

No. `tumblercheckptr` (`tumble.c:169`) checks for:
- `exp > 0` → error
- `sign=1 && mantissa[0]==0` → "negative zero" error
- Negative mantissa **digit** values (each `mantissa[i] < 0`) → error

It does **not** check for `sign == 1` with a nonzero mantissa. A proper negative tumbler (sign=1, mantissa=[2,0,...]) is **not flagged as invalid**. Similarly, `assertwidsarepositive` (`test.c:336`) calls `tumblercheckptr` on displacements but would not catch negative-signed tumblers. The name "assertwidsarepositive" is aspirational rather than enforced.

---

### Does the System Function Correctly? Yes — via `setwispnd` Normalization

Immediately after the shift loop in `deletend` (`edit.c:74-75`):
```c
setwispupwards (father, 1);
recombine (father);
```

`setwispupwards` calls `setwispnd` (`wisp.c:171`) for `father`, which is precisely the node whose children may now have negative displacements.

`setwispnd` computes the **element-wise minimum displacement** across all sons (`wisp.c:193-196`):
```c
movewisp (&ptr->cdsp, &mindsp);
for (ptr = getrightbro(ptr); ptr; ptr = getrightbro(ptr))
    lockmin ((tumbler*)&mindsp, (tumbler*)&ptr->cdsp, (tumbler*)&mindsp, dspsize(...));
```

`lockmin` uses `macrotumblermin` (`common.h:144`):
```c
#define macrotumblermin(a,b,c) ((*(tumbler*)(c)) = (tumblercmp((a),(b)) == LESS) ? ... : ...)
```
which uses `tumblercmp` (`tumble.c:72`) — correctly ordering negative tumblers by sign first, then absolute magnitude.

Then (`wisp.c:197-211`):
```c
lockiszerop = iszerolock((tumbler*)&mindsp, dspsize(father->cenftype));
if (!lockiszerop) {
    dspadd (&father->cdsp, &mindsp, &newdsp, ...);  // father shifts backward by |mindsp|
    ...
    for (ptr = findleftson(father); ...) {
        dspsub(&ptr->cdsp, &mindsp, &ptr->cdsp, ...); // each child: cdsp -= mindsp
```

`iszerolock` (`wisp.c:253`) returns FALSE for any negative tumbler because `iszerotumbler` checks `mantissa[0] == 0`, and a negative tumbler has nonzero mantissa. So the normalization branch always fires when any child has a negative displacement.

`dspsub(&ptr->cdsp, &mindsp, &ptr->cdsp)` = `ptr->cdsp − mindsp`. When `mindsp` is negative (say −2): `ptr->cdsp − (−2) = ptr->cdsp + 2`. The originally-negative child gets `−2 + 2 = 0`. Other children get shifted up by the same amount. `father->cdsp` gets `+mindsp = +(−2)`, i.e., decremented, preserving all absolute positions.

The normalization is conservative on sign but not on absolute displacements: it guarantees all children end with non-negative displacements, and the father absorbs the shift. Absolute V-positions are preserved throughout because `tumbleradd` operates correctly on signed tumblers.

---

### Summary

**Condition for negative V-position:** `tumblersub` at `edit.c:63` produces a negative `ptr->cdsp.dsas[V]` when the deletion width `width` exceeds the surviving crum's relative V-displacement `ptr->cdsp.dsas[V]` in absolute magnitude — i.e., `|ptr->cdsp.dsas[V]| < |width|`. At equal exponent, this reduces to the mantissa comparison the question poses: `width.mantissa[0] > ptr->cdsp.dsas[V].mantissa[0]` after exponent alignment in `abscmp`. At different exponents, the lower-exponent operand is automatically smaller. The structural precondition is that `father` (the intersection node) already has an accumulated absolute V-offset exceeding the deletion start, leaving children with small relative displacements that underflow when the full width is subtracted.

**Does the system continue to function?** Yes, completely. The negative displacement is transient by design. `setwispnd` (`wisp.c:171`), invoked immediately via `setwispupwards(father, 1)` at `edit.c:74`, detects the minimum (negative) child displacement via `lockmin`/`tumblercmp`, then normalizes the subtree in-place: each child's displacement is increased by `|mindsp|` and the father's displacement is correspondingly decreased. This preserves all absolute V-positions while eliminating all negative relative displacements before any retrieval or comparison operation sees the POOM state.
