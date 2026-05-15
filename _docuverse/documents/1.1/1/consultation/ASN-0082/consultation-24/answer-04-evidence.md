## Question 4 [evidence]

> Does the udanax-green implementation handle contraction at V-position depths greater than 2 (e.g., for nested subspace structures), or is it restricted to depth-2 ordinal-level spans?

## KB Synthesis

## V-Address Depth in udanax-green

The KB does not provide evidence that the implementation handles "nested subspace" structures at V-position depths greater than 2. Here is what can be derived:

---

### The Three-Subspace Model Is Flat

[SS-SUBSPACE-CONVENTION] / Findings 0009, 0038 establish that V-address subspace identity is determined exclusively by `mantissa[0]`:

- `1` = text (1.x)
- `2` = links (2.x)
- `3` = link type endpoints (3.x)

This partition is at depth 1 (the first digit only). There is no documented sub-subspace structure like `1.1.x` vs `1.2.x` with independent isolation.

---

### The Two-Blade Knife Enforces a Depth-2 Assumption

[SS-TWO-BLADE-KNIFE] / Finding 0054 is the critical constraint. `findaddressofsecondcutforinsert()` always computes the second blade as `(N+1).1` — a depth-2 address — regardless of the fractional complexity of the insertion point:

- INSERT at `1.x` → blades `[1.x, 2.1)` — shift domain bounded by first digit only
- INSERT at `2.x` → blades `[2.x, 3.1)` — same structure

The hardcoded `1` at the second digit position means the knife cuts between subspaces, not between sub-subspaces. Any hypothetical V-address `1.2.3` would be shifted by INSERT at `1.1` (since `1.2.3 < 2.1`), with no mechanism to isolate it differently from `1.2`.

---

### DELETE Subspace Isolation Is Also Depth-1

[INT-DELETE-SUBSPACE-ASYMMETRY] / Finding 0055 shows that DELETE's subspace protection relies on `strongsub`'s exponent guard — specifically that text-subspace deletion widths (exp = −1) differ from link-subspace positions (exp = 0). This is a coarse depth-1 property, not a depth-3+ mechanism. There is no analogous protection for hypothetical sub-subspace nesting within `1.x`.

---

### The Underlying Tumblers Are Unconstrained

[SS-TUMBLER] / Finding 0031 establishes that tumblers have a 16-digit mantissa with no inherent structural restrictions. V-addresses at depth 3+ (e.g., `1.2.3`) are representable as tumblers and storable in the POOM. The `tumblerlength(vsaptr) - 1` exponent in [SS-INSERT-VWIDTH-ENCODING] / Finding 0076 shows the code does read V-address length, with the developer noting suspicion about the shift computation — suggesting depth variability was at least contemplated.

---

### Conclusion

The implementation is **functionally restricted to depth-2 ordinal-level spans**. The subspace isolation machinery ([FC-SUBSPACE], [SS-TWO-BLADE-KNIFE]) assumes `subspace.position` structure throughout. Deeper V-addresses are representable in the tumbler arithmetic but receive no special isolation treatment — insertions would shift them within the enclosing first-digit subspace. The KB contains no evidence of depth > 2 being used or tested for V-positions.

---

## Code Exploration

I now have all the information needed for a complete answer.

---

## Answer: V-Position Depth and Contraction in udanax-green

The implementation is **restricted to depth-2 V-position ordinal spans**. There is no support for nested subspace structures at depth > 2. Here is the full technical case, by evidence.

---

### 1. Tumbler Capacity vs. Actual Usage

The tumbler structure in `common.h:53-65` supports up to 16 mantissa positions:

```c
#define NPLACES 16   /* places in mantissa of tumbler - increased from 11 to support deeper version chains */
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign;
    short exp;
    tdigit mantissa[NPLACES];
} tumbler;
```

The comment is critical: `NPLACES` was increased from 11 to 16 "to support deeper version chains" — meaning deeper **I-space ISA addresses** (account.document.version hierarchies), **not** deeper V-space subspace nesting. The arithmetic machinery can represent 16-story tumblers, but the V-space semantic layer uses at most 2.

---

### 2. V-Space Is Hardcoded to Two Depths

**Depth 1 — text content** is enforced by `istextcrum()` at `orglinks.c:246-253`:

```c
bool istextcrum(typecorecrum *crumptr)
{
    if(crumptr->cdsp.dsas[V].mantissa[1] == 0  && is1story(&crumptr->cwid.dsas[V])){ 
        return TRUE;
    }
    return FALSE;
}
```

A crum is a text crum exactly when `mantissa[1] == 0` (second story is zero) **and** its V-width is `is1story()` (only `mantissa[0]` non-zero). This predicate cannot recognise depth-3+ text content — it would return FALSE for any multi-story displacement.

**Depth 2 — link endpoints** is enforced by `islinkcrum()` at `orglinks.c:255-261`:

```c
bool islinkcrum(typecorecrum *crumptr)
{
    if(crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0){ 
        return TRUE;
    }
    return FALSE;
}
```

This checks specifically for the `1.x` pattern (first story = 1, second story ≠ 0). A depth-3 address like `1.2.3` would pass this predicate — but only because the check is insufficient: it would be misclassified as a link crum rather than a separate subspace level, because `mantissa[2]` is never tested.

**All link VSA creation** is hardcoded to depth 2 via `setlinkvsas()` at `do2.c:169-183`:

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
    tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);
    tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);   /* fromvsa = 1.1 */
    tumblerincrement (tovsaptr, 0, 2, tovsaptr);
    tumblerincrement (tovsaptr, 1, 1, tovsaptr);       /* tovsa  = 2.1 */
    if (threevsaptr) {
        tumblerincrement (threevsaptr, 0, 3, threevsaptr);
        tumblerincrement (threevsaptr, 1, 1, threevsaptr);  /* threevsa = 3.1 */
    }
    ...
}
```

The two-call pattern (`rightshift=0` then `rightshift=1`) always produces depth-2 tumblers. There is no mechanism for constructing deeper link VSAs and no call path that would pass a depth-3+ address to `setlinkvsas()`.

---

### 3. `retrievevspansetpm()` Is Incorrect for Depth > 2

The function that decomposes a document's V-span into text and link parts, at `orglinks.c:191-221`, manually strips the second story by zeroing `mantissa[1]`:

```c
linkvspan.stream.mantissa[1] = 0;
tumblerjustify(&linkvspan.stream);
linkvspan.width.mantissa[1] = 0;
tumblerjustify(&linkvspan.width);
```

The comment at line 193 makes the assumption explicit: *"in both cases we have to remove the first digit of the tumbler, the 1"*. This code is correct only for 2-story addresses. For a hypothetical depth-3 address `1.2.3`, zeroing `mantissa[1]` produces `1.0.3`, which after `tumblerjustify` becomes `1.3` — an incorrect result. The function has no code path for addresses with non-zero values in `mantissa[2]` or beyond.

---

### 4. `beheadtumbler()` — Contraction by One Story

The function `beheadtumbler()` at `tumble.c:673-683` strips the leading story from a tumbler:

```c
int beheadtumbler(tumbler *aptr, tumbler *bptr)
{
    tumbler temp;
    movetumbler (aptr, &temp);
    ++temp.exp;
    if (aptr->exp == 0)
        temp.mantissa[0] = 0;
    tumblerjustify (&temp);
    movetumbler (&temp, bptr);
}
```

This is the closest the codebase has to a "contraction" operation. It is called in three places:

- **`insertnd.c:180`** — `findaddressofsecondcutforinsert()`, which computes the second cut address for text insertion. The function comment at line 175 reads: *"needs this to give it a place to find intersection of for text is 2.1"* — explicitly targeting a depth-2 split.
- **`spanf1.c:174`** — removes the document-ID prefix from a tumbler to recover the within-document address.
- **`sporgl.c:264`** — strips the ORGLRANGE offset prefix to recover a link ISA from context.

All three call sites operate on depth-2 (or I-space ISA) addresses. There is no call site that iteratively applies `beheadtumbler` to handle depth-3+ contraction, and no loop or recursive mechanism that would reduce a depth-N address to depth-1 through successive beheadings.

---

### 5. Gregory's Own Suspicious Comment in `insertpm()`

The most telling evidence of unverified depth handling is in `insertpm()` at `orglinks.c:114-117`:

```c
/*I'm suspicious of this shift <reg> 3/1/85 zzzz*/
shift = tumblerlength (vsaptr) - 1;
inc = tumblerintdiff (&lwidth, &zero);
tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);
```

`tumblerlength()` is depth-agnostic — it returns `nstories - exp` for any tumbler. So the arithmetic could theoretically handle depth-3+ insertions if the correct VSA were passed in. But Gregory's own comment — the "zzzz" marker he consistently used for unresolved questions — records that the shift calculation was suspected to be wrong even for the depth-2 case. This was never resolved, and depth > 2 was never tested.

---

### 6. Enfilade Operations Are Depth-Agnostic but Never Exercised Beyond Depth 2

The low-level enfilade machinery in `retrie.c` — `findcbcnd()`, `findcbcinarea2d()`, `whereoncrum()` — all pass through to `tumblercmp()` and `tumbleradd()`, which are depth-agnostic. The `crumqualifies2d()` at `retrie.c:270-305` does not check depth at all. In principle, the enfilade tree could store and retrieve content at any depth.

But this generality is never exercised in V-space beyond depth 2, because:
- No code constructs V-addresses at depth 3+
- The classification predicates can't correctly distinguish them
- `retrievevspansetpm()` would corrupt their span boundary data

---

### Summary

| Layer | Depth support |
|---|---|
| Tumbler arithmetic (`tumble.c`) | Depth-agnostic, up to NPLACES=16 |
| Enfilade tree operations (`retrie.c`, `genf.c`) | Depth-agnostic, structural only |
| V-space address creation (`do2.c:setlinkvsas`) | Hardcoded depth 1 and depth 2 |
| Crum classification (`orglinks.c:istextcrum, islinkcrum`) | Hardcoded to mantissa[0] and mantissa[1] |
| Span decomposition (`orglinks.c:retrievevspansetpm`) | Zeroes mantissa[1] — correct only for depth 2 |
| Depth contraction (`tumble.c:beheadtumbler`) | Removes one story; always applied to depth-2 addresses; no iteration for depth > 2 |
| Depth shift in POOM insertion (`orglinks.c:insertpm`) | Uses tumblerlength — general, but never exercised past depth 2; Gregory marked it suspicious |

The implementation assumes V-space has exactly two inhabited subspaces: depth-1 ordinal positions for text content and depth-2 `N.1` positions for link endpoints. V-positions at depth 3 or beyond are not handled — no code creates them, the classification predicates misidentify them, and `retrievevspansetpm()` would produce incorrect span boundaries for them.
