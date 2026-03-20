## Question 10 [gregory]

> In a POOM bottom crum, must V-width and I-width always represent the same logical span length, or can they diverge — and if they must match, what mechanism enforces this coupling when `tumblerlength` computes V-width from V-address exponent while I-width is copied directly from I-space?

## KB Synthesis

## V-width and I-width in POOM Bottom Crums

**They must always encode the same logical span length (byte count), and the coupling is enforced structurally at crum creation — not by a runtime check.**

---

### The invariant

[INV-WIDTH-VALUE-EQUIVALENCE] states it formally:

```
forall crum c :: tumblerintdiff(c.width.dsas[V], zero) == tumblerintdiff(c.width.dsas[I], zero)
```

The two tumbler representations differ in exponent and digit count, but `tumblerintdiff` applied to either returns the same integer. [SS-POOM-BOTTOM-CRUM] makes the asymmetry concrete: for an 11-character insert, I-width is `0.0.0.0.0.0.0.0.11` (9 digits) while V-width is `0.11` (2 digits) — structurally unequal as tumblers, numerically identical as span lengths.

---

### The enforcement mechanism

The coupling is enforced by the construction path in `insertpm`, documented in [SS-INSERT-VWIDTH-ENCODING]:

1. **Extract the byte count from I-width**: `inc = tumblerintdiff(&lwidth, &zero)` — this converts the I-space tumbler to an integer, discarding its representation details.
2. **Re-encode at V-space precision**: `tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V])` where `shift = tumblerlength(vsaptr) - 1` — this builds a fresh V-width tumbler encoding `inc` at the exponent implied by the V-address's digit length.
3. **Copy I-width directly**: `movetumbler(&lwidth, &crumwidth.dsas[I])` — no transformation.

The integer `inc` is the bridge. Both representations are derived from it, so they cannot diverge at creation time.

---

### Why it holds structurally thereafter

Crums are not mutated after creation. [SS-POOM-MUTABILITY] establishes that INSERT adds new leaf nodes, DELETE removes and frees them, and REARRANGE shifts only the displacement (`cdsp`) fields — not the width fields. Since no operation writes to an existing crum's width fields after initial construction, the invariant cannot be broken by post-creation modification.

---

### The fragility: the V-address exponent coupling

The V-width exponent is `−shift = −(tumblerlength(vsaptr) − 1)`, which means the V-width encoding precision is determined by the V-address at insertion time, not by the content itself. This creates an implicit dependency: the "same" byte count 11 encodes as `0.11` when inserted at a 2-digit V-address like `1.1`, but would encode differently at a V-address with a different digit length.

[EC-VWIDTH-ZERO-ADDRESS] flags the boundary case: if `vsaptr` is the zero tumbler, `tumblerlength = 0` gives `shift = -1`, producing `exp = +1` — a positive exponent, putting the V-width in a qualitatively different magnitude range from all normal V-widths (which have negative exponents). The 1985 comment `/*I'm suspissious of this shift*/` in `orglinks.c:106` suggests the developer was aware of this. The formal precondition should require `vsaptr` is non-zero with `tumblerlength(vsaptr) >= 1`.

---

### Summary

| Property | Status |
|---|---|
| V-width and I-width encode same span length | Required invariant [INV-WIDTH-VALUE-EQUIVALENCE] |
| Enforcement mechanism | Construction-time derivation from shared integer `inc` [SS-INSERT-VWIDTH-ENCODING] |
| Runtime check after creation | None — invariant holds by immutability of width fields |
| Comparison via `tumblercmp` | Will not detect equality; must use `tumblerintdiff` to extract values |
| Zero-address edge case | May break the encoding; developer-flagged as suspicious [EC-VWIDTH-ZERO-ADDRESS] |

---

## Code Exploration

I now have everything needed. Here is the full analysis.

---

## V-width vs I-width in POOM Bottom Crums

### Short Answer

**V-width and I-width are structurally independent tumblers that encode the same logical span count but at different address-space depths.** They are not equal as tumbler values and can diverge — no invariant enforcement exists. The only coupling is a one-time derivation at insertion time in `insertpm`, where V-width is computed from I-width using a depth-based shift. After that, both dimensions are propagated upward independently, and the code has multiple comments suggesting the mechanism was known to be fragile.

---

### 1. What the Bottom Crum Holds

A POOM bottom crum stores a `typewid cwid` — a 2-element array of tumblers (from `wisp.h`):

```c
#define I  0
#define V  1
```

So `cwid.dsas[I]` is the I-space width and `cwid.dsas[V]` is the V-space width. These are **separate tumblers** representing spans in two distinct coordinate systems. The same `typedsp cdsp` structure holds the I- and V-displacements (start addresses).

---

### 2. How V-width is Derived from I-width at Insertion

The critical code is in `insertpm` (orglinks.c:75–134). For each sprogl in the sprogl set, the function:

```c
// orglinks.c:109
movetumbler (&lwidth, &crumwidth.dsas[I]);    // I-width = direct copy of sprogl width

// orglinks.c:114–117
/*I'm suspissious of this shift <reg> 3/1/85 zzzz*/
shift = tumblerlength (vsaptr) - 1;
inc   = tumblerintdiff (&lwidth, &zero);
tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);
```

Step by step:

- **I-width** is copied verbatim from `lwidth` — the raw I-space width of the content being linked.
- `tumblerlength(vsaptr)` [tumble.c:259–262] returns `nstories(vsaptr) - vsaptr->exp`, which measures how many digit positions deep the V-space address is.
- `tumblerintdiff(&lwidth, &zero)` [tumble.c:591–597] extracts `lwidth.mantissa[0]` — the integer count of I-space atoms.
- `tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V])` [tumble.c:599–622] constructs V-width as:
  ```c
  cptr->exp = -shift;       // depth matches V-address depth
  cptr->mantissa[0] = inc;  // same integer count
  ```

**Result:** V-width and I-width encode the **same integer count** (`inc` atoms) but at **different exponent positions** in the tumbler — I-width is at whatever depth the I-space address naturally falls, while V-width is placed at depth `shift = tumblerlength(vsaptr) - 1`, matching the depth of the V-address.

As tumbler values they are structurally different. The only "coupling" is that `inc` is shared. Roger Gregory himself flagged this with a 1985 comment marking his own suspicion about the shift.

---

### 3. `tumblerlength` Computes Depth, Not a Width in Common Units

```c
// tumble.c:249–257
INT nstories(tumbler *tumblerptr) {
    for (i = NPLACES; i > 0 && tumblerptr->mantissa[--i] == 0;);
    return (i + 1);
}

// tumble.c:259–262
INT tumblerlength(tumbler *tumblerptr) {
    return (nstories (tumblerptr) - tumblerptr->exp);
}
```

`tumblerlength` measures the **span of significant digit places** — essentially, how deep the address sits in the hierarchical address tree. This is the structural depth in V-space. When V-width is set using `shift = tumblerlength(vsaptr) - 1`, it is being placed at that depth so that the V-space span aligns with the grain of the V-address.

**I-width has no such shift applied** — it is copied as-is, maintaining the I-space grain. The two widths therefore sit at different levels of their respective address hierarchies.

---

### 4. `widdiffs` Detects Divergence but Does Not Prevent It

```c
// insertnd.c:114–122
static INT widdiffs(typecuc *crumptr) {
    INT i,v;
    if(crumptr->cenftype != POOM)
        return(0);
    i = lastdigitintumbler(&crumptr->cwid.dsas[I]);
    v = lastdigitintumbler(&crumptr->cwid.dsas[V]);
    return(i-v);
}
```

`lastdigitintumbler` returns `mantissa[nstories - 1]` — the highest-order non-zero digit. `widdiffs` computes whether the leading count digit is the same in both dimensions. It is called at the start and end of `insertnd` [insertnd.c:46, 78]:

```c
// insertnd.c:46, 78–85
olddiff = widdiffs(fullcrumptr);
// ... do the insertion ...
newdiff = widdiffs(fullcrumptr);
#ifndef DISTRIBUTION
if(FALSE&&(fullcrumptr->cenftype==POOM)&&olddiff != newdiff){
    fprintf(stderr,"insertnd  possible error dumping widdiffs%d %d\n\r",olddiff,newdiff);
    ...
}
```

Two things are notable here:

1. The check is guarded by `FALSE&&` — it **never executes** even in debug builds. The developer disabled it rather than letting it assert.
2. The fact that `widdiffs` exists at all confirms that V-width and I-width were expected to have matching leading digits — but also that they could diverge in practice, requiring detection.

No assertion runs on this invariant at any stage.

---

### 5. `setwispnd` Propagates Both Dimensions Independently

When widths are propagated upward after insertion, `setwispnd` (wisp.c:171–228) operates on the full lock (both tumblers simultaneously via `lockadd` and `lockmax`):

```c
// wisp.c:213–214
lockadd((tumbler*)&ptr->cdsp, (tumbler*)&ptr->cwid,
        (tumbler*)&tempwid, (unsigned)widsize(ptr->cenftype));
lockmax((tumbler*)&newwid, (tumbler*)&tempwid,
        (tumbler*)&newwid, (unsigned)widsize(ptr->cenftype));
```

This computes the bounding box in both dimensions together — the max of `cdsp[I]+cwid[I]` and max of `cdsp[V]+cwid[V]` — separately, with no cross-check between them. There is nothing here that would force `cwid.dsas[I] == cwid.dsas[V]` at any parent node.

The related `setwidnd` (wisp.c:235–247), called from `makegappm` [insertnd.c:170], has an additional bug: it resets `newwid` **inside** the loop, so it only retains the last child's width rather than the max — yet another place where widths can silently become wrong.

---

### 6. The `fixincoresubtreewids` Kluge Confirms Widths Can Drift

Multiple dead-code blocks in `insertnd.c` (lines 32, 59, 65, 98) contain this:

```c
/*fixincoresubtreewids(fullcrumptr);/*1999 // a temp kluge zzz till we find
  where setwisp isnt called// this is a brute force kluge, if this fixes
  anything it means that the wids aren't being set properly somplace else
  probably near here */
```

This 1999 kluge — a brute-force tree-wide width recomputation — was introduced specifically because `setwispupwards` was **not being called reliably**, causing the stored widths to drift from what they should be. It was subsequently commented out, leaving the underlying problem unresolved.

---

### Summary

| Question | Answer |
|----------|--------|
| Must V-width == I-width as tumbler values? | **No.** They live in different address spaces at different depths. |
| Do they represent the same logical span length? | **Intended yes** (same integer count `inc`), but not guaranteed after subsequent operations. |
| What couples them? | Only the initial derivation in `insertpm` [orglinks.c:109–117]: `inc` is taken from I-width and placed into V-width at the V-address depth via `tumblerincrement`. |
| Is this coupling enforced? | **No.** `widdiffs` can detect divergence in leading digits [insertnd.c:114–122], but the check is disabled (`FALSE&&`) and never fires [insertnd.c:80]. `setwispnd` propagates both dimensions independently [wisp.c:213–214]. `setwidnd` has a loop bug that loses all but the last child width [wisp.c:239–241]. |
| Historical evidence of drift? | Yes — the `fixincoresubtreewids` kluge [insertnd.c:32, 59, 65, 98] was a 1999 admission that widths were routinely drifting out of correct state. |

The coupling is a creation-time convention, not a maintained invariant. Once a POOM crum is in the tree, its V-width and I-width are maintained by independent propagation paths that have no coupling mechanism between them.
