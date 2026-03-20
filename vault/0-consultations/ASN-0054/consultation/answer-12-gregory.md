## Question 12 [gregory]

> When `isanextensionnd` coalesces a new entry with an existing bottom crum, does it always extend the V-width and I-width symmetrically — that is, does a single bottom crum always represent a 1:1 mapping where V-width equals I-width in magnitude?

## KB Synthesis

Yes, a single bottom crum always represents a 1:1 mapping where V-width and I-width encode the same numeric magnitude, though the tumbler representations differ.

## The invariant holds universally

[INV-WIDTH-VALUE-EQUIVALENCE] states this directly:

> `forall crum c :: tumblerintdiff(c.width.dsas[V], zero) == tumblerintdiff(c.width.dsas[I], zero)`

The V-width and I-width are **not equal as tumblers** (they have different exponents and digit counts — see [SS-POOM-BOTTOM-CRUM] and [SS-INSERT-VWIDTH-ENCODING]), but extracting the integer value from either yields the same count.

## Why this is structurally necessary

Three facts force symmetry:

1. **[INV-SINGLE-CHAR-GRANULARITY]**: Each byte occupies exactly one I-address. V-space width equals byte count; I-space width equals I-address count. Both count the same thing.

2. **[SS-INSERT-VWIDTH-ENCODING]**: V-width is explicitly *derived from* the I-width integer value at crum creation. The construction `inc = tumblerintdiff(lwidth, zero)` extracts the I-width's count, then `tumblerincrement(zero, shift, inc, &crumwidth.dsas[V])` re-encodes that same count at V-space exponent precision. They start equal by construction.

3. **[ST-INSERT, Finding 0062]**: `isanextensionnd` checks that `new_content.origin == existing_crum.reach` in both V and I dimensions (the condition is contiguity in both spaces simultaneously). A single character added via extension contributes exactly +1 to both widths' numeric value, preserving the invariant.

## What the asymmetry actually is

The asymmetry is purely representational: I-widths use 6–9 tumbler digits (full I-space precision), while V-widths use 2 digits (V-address precision, with exponent = `tumblerlength(vsaptr) - 1`). A crum covering 11 bytes has:

```
V-width: exp=-1, mantissa[0]=11  →  tumbler 0.11
I-width: 0.0.0.0.0.0.0.0.11      →  same value, 9-digit tumbler
```

Comparing with `tumblercmp` would show them unequal; comparing with `tumblerintdiff` shows them equal. Any code performing width comparisons across the two dimensions must use the integer extraction path, not raw tumbler comparison.

The KB does not document what happens if `vsaptr` is the zero tumbler during V-width encoding — [EC-VWIDTH-ZERO-ADDRESS] flags this as a suspected edge case — but for all normal INSERT paths where V-addresses are positive and non-zero, the 1:1 magnitude relationship holds unconditionally.

---

## Code Exploration

Now I have everything I need for a complete answer.

---

## Answer

**No. A single bottom crum does not always have V-width equal to I-width in magnitude.** The extension check in `isanextensionnd` enforces 2D adjacency — not 2D symmetry — and the widths added during coalescing are constructed with deliberately different formulas for each dimension.

---

### 1. `isanextensionnd` checks adjacency in both dimensions simultaneously

`isanextensionnd` [insertnd.c:301-309]:

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

`prologuend` [retrie.c:334-339] computes:
- `grasp = offset + crum->cdsp` (in both I and V dimensions)
- `reach = grasp + crum->cwid` (in both I and V dimensions)

via `dspadd` → `lockadd` over `dspsize(POOM) = DSPSIZEPM = 2` tumblers [wisp.h:26, wisp.c:17].

Then `lockeq` [wisp.c:261-266] checks `reach.dsas[0] == origin.dsas[0]` AND `reach.dsas[1] == origin.dsas[1]` — that is, I-reach == new I-origin **and** V-reach == new V-origin simultaneously. This is a 2D contiguity gate, not a symmetry assertion.

---

### 2. When coalescing fires, both widths are added independently

`insertcbcnd` [insertnd.c:250-251]:

```c
if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
    dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
```

`dspadd` [wisp.c:15-18] calls `lockadd` over `dspsize(POOM) = 2` tumblers:
- `ptr->cwid.dsas[I] += width->dsas[I]`
- `ptr->cwid.dsas[V] += width->dsas[V]`

No assertion is made that these increments are equal. Whatever relationship (or mismatch) exists between the I and V components of `width` is simply preserved.

---

### 3. The V-width is constructed differently from the I-width

The only caller of `insertnd` for POOM is `insertpm` [orglinks.c:75-134]. The critical width-construction block [orglinks.c:105-117]:

```c
movetumbler (&lstream, &crumorigin.dsas[I]);    // I-origin = I-span start
movetumbler (&lwidth, &crumwidth.dsas[I]);      // I-width = raw I-span width
movetumbler (vsaptr, &crumorigin.dsas[V]);      // V-origin = current vsa
/*I'm suspissious of this shift <reg> 3/1/85 zzzz*/
shift = tumblerlength (vsaptr) - 1;
inc = tumblerintdiff (&lwidth, &zero);
tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);
```

`lwidth` is the raw I-span width from `unpacksporgl` [sporgl.c:178-203] — a full tumbler with its own `exp` and mantissa.

`tumblerincrement(&zero, shift, inc, result)` [tumble.c:599-607] with a zero `aptr` produces:

```c
cptr->exp = -rightshift;   // = -(shift)
cptr->mantissa[0] = bint;  // = inc = lwidth.mantissa[0] only
```

So the V-width tumbler is `inc × base^(-shift)` where:
- `inc = tumblerintdiff(&lwidth, &zero)` extracts only `lwidth.mantissa[0]` (the leading digit — sub-integer digits in `lwidth` are discarded)
- `shift = tumblerlength(vsaptr) - 1 = nstories(vsaptr) - vsaptr->exp - 1` depends on the depth of the V-address

The I-width is the full `lwidth` (all digits, its own `exp`). The V-width discards sub-integer I-space precision and rescales by V-address depth.

**Example**: If `lwidth` is a simple integer tumbler `{exp=0, mantissa=[5,0,0...]}` (N=5 characters) and `vsaptr` has `tumblerlength=3` (a three-story address like `1.0.3`):

- I-width: `{exp=0, mantissa=[5,0,0...]}` — represents 5 at the top level
- V-width: `tumblerincrement(&zero, 2, 5, ...)` → `{exp=-2, mantissa=[5,0,0...]}` — represents 5 at depth 2

These are not equal tumblers. The V-width is two decimal places "deeper" in the tumbler hierarchy.

If `vsaptr` has `tumblerlength=1` (top-level address, `shift=0`), the V-width would equal the I-width for simple integer tumblers — the 1:1 case holds **only for top-level V-addresses with no sub-integer I-width precision**.

---

### 4. The developers tracked this divergence explicitly

`widdiffs` [insertnd.c:114-122]:

```c
static INT widdiffs(typecuc *crumptr)
{
    INT i,v;
    if(crumptr->cenftype != POOM)
        return(0);
    i = lastdigitintumbler(&crumptr->cwid.dsas[I]);    
    v = lastdigitintumbler(&crumptr->cwid.dsas[V]);    
    return(i-v);
}
```

This function exists precisely to measure the difference between the last digit of I-width and V-width. It is called before and after every POOM insertion [insertnd.c:46, 78], and a disabled diagnostic [insertnd.c:80-85] prints "possible error" when the diff changes:

```c
if(FALSE&&(fullcrumptr->cenftype==POOM)&&olddiff != newdiff){      
    fprintf(stderr,"insertnd  possible error dumping widdiffs%d %d\n\r",olddiff,newdiff);
```

The `FALSE&&` disablement tells us: the developers knew this could diverge, investigated it, and ultimately decided not to treat it as fatal. The comment `/*I'm suspissious of this shift <reg> 3/1/85 zzzz*/` at orglinks.c:114 further shows that the V-width shift calculation was a known concern from 1985.

---

### Conclusion

**`isanextensionnd` coalescing does not guarantee V-width == I-width.** The function enforces that the new insertion is contiguous with the existing crum in *both* I-space and V-space simultaneously — but this is a condition on positions, not widths. The widths are constructed independently in `insertpm`: I-width from the raw I-span, V-width from the leading digit of that span scaled to the V-address depth. For V-addresses deeper than story 1, the resulting tumblers are structurally different in their `exp` fields, even when they represent the same integer count of characters. The `widdiffs` function and its accompanying disabled diagnostic confirm the developers were aware that POOM bottom crums can carry asymmetric I/V widths and chose not to enforce strict equality at the tumbler level.
