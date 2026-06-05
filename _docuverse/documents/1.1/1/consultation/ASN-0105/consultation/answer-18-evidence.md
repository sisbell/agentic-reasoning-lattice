## Question 18 [evidence]

> Does a read of a span containing a negative V-position tumbler [EC-NEGATIVE-VPOSITION] — produced by a prior DELETE shift — return that content, and does `intervalcmp` order it before the positive positions?

## KB Synthesis

## Negative V-Position Tumblers: Reads and Ordering

### Does a read return the content?

No. A negative V-position POOM entry is **unreachable by any positive-range retrieval query**.

`retrieve_contents` accepts a specset with positive V-span arguments. During retrieval, `whereoncrum()` [SS-WHEREONCRUM] classifies each POOM crum relative to the query interval `[grasp, reach)`. Because `tumblercmp` places all negative tumblers strictly before all positive tumblers and zero [SS-TUMBLER, Finding 0053], a crum at V-position `-0.8` relative to any positive query range returns `TOMYLEFT (-2)`. The traversal never descends into it.

[INV-POOM-BIJECTIVITY] states this explicitly: after DELETE shifts a POOM entry to a negative V-position, the entry "remains in the POOM tree but becomes invisible" — "unreachable by any V-space query."

### Does `intervalcmp` order it before positive positions?

Yes, unconditionally. From [SS-TUMBLER] Finding 0053:

> `tumblercmp` treats negative tumblers as strictly less than all positive tumblers and zero, regardless of magnitude.

And the concrete ordering from [INV-TUMBLER-TOTAL-ORDER]:

```
tumblercmp(-0.8, 0.0):  → LESS
tumblercmp(-0.8, 1.1):  → LESS
tumblercmp(-0.8, -0.3): → GREATER (larger absolute value = more negative)
```

`intervalcmp` delegates to `tumblercmp` for comparison [SS-INTERVAL-CMP], so any negative address is classified `TOMYLEFT` (-2) relative to any interval with a positive left boundary.

### Summary

The negative-V-position entry sorts before all valid V-addresses per the total tumbler order, making it unreachable by normal retrieval. It persists as leaked state — a POOM entry that can never be deleted by a subsequent `DELETEVSPAN` (which also requires a positive V-span argument) and never returned by any read.

---

## Code Exploration

I now have a complete picture from the source code. Here is the full answer.

---

## Does a Negative V-Position (from DELETE shift) Return Content? Does `intervalcmp` Order It Before Positive Positions?

### How DELETE Produces Negative V-Positions

`dodeletevspan` → `deletevspanpm` → `deletend` [edit.c:31-76] makes two passes over the POOM crums after cutting the tree. Each child of the "father" node is classified by `deletecutsectionnd` [edit.c:235-248]:

- **Case 1** (crum is entirely inside the deleted range): freed from the tree
- **Case 2** (crum is entirely to the right of the deleted range): V-displacement is shifted left

The case-2 shift is at `edit.c:63`:

```c
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    /* This will get set to modified in setwisp */
    break;
```

`tumblersub` [tumble.c:406-440] implements subtraction as negation-and-add:

```c
else {
    movetumbler (bptr, &temp);
    temp.sign = !temp.sign;        // ← negate bptr  [tumble.c:427]
    tumbleradd (aptr, &temp, cptr);
}
tumblerjustify (cptr);
```

When the deletion `width` exceeds the child crum's relative V-displacement, `tumbleradd` with a dominating negative term propagates the negative sign to the result [tumble.c:391-393]:

```c
} else {
    weaksub (bptr, aptr, cptr);
    cptr->sign = bptr->sign;   // ← bptr is the negated width → result is negative
```

The `sign` field of the tumbler is set to 1 (negative). There is no guard preventing this: `tumblercheckptr` [tumble.c:180-181] only flags *negative zero* (sign=1, mantissa=0) as invalid:

```c
if (ptr->sign && ptr->mantissa[0] == 0){
    fprintf(stderr," negative zero ");
    wrong = TRUE;
}
```

A negative tumbler with non-zero mantissa silently passes. The guard in `insertpm` [orglinks.c:93-96] prevents *inserting* at a negative VSA:

```c
if (tumblercmp (vsaptr, &zero) == LESS)
    gerror ("insertpm called with negative vsa.\n");
```

But this guard applies only to new insertions, not to existing crums shifted leftward by a subsequent delete.

---

### Does a Read of the Negative-V Span Return Content?

**No.** The negative-V crum remains in the POOM tree but is invisible to any positive-address query.

Retrieval enters via `retrieverestricted` [retrie.c:56-85] → `retrieveinarea` → `findcbcinarea2d` → `crumqualifies2d` [retrie.c:270-305], which calls `whereoncrum` [retrie.c:345-398] for every crum:

```c
case SPAN:
case POOM:
    tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
    cmp = tumblercmp(address, &left);
    if (cmp == LESS){
        return(TOMYLEFT);
    } else if (cmp == EQUAL){
        return(ONMYLEFTBORDER);
    }
    tumbleradd (&left, &ptr->cwid.dsas[index], &right);
    cmp = tumblercmp(address, &right);
    if (cmp == LESS){
        return(THRUME);
    } else if (cmp == EQUAL){
        return (ONMYRIGHTBORDER);
    } else {
        return(TOMYRIGHT);
    }
```

Consider a crum whose V-displacement has been shifted to -5 (sign=1), with a width of 3, giving a V-range of [-5, -2). A positive query address of +3:

1. `tumbleradd(offset=0, cdsp=-5, left)` → left = -5
2. `tumblercmp(+3, -5)`: signs differ, aptr (=+3) has sign=0 → `return (aptr->sign ? LESS : GREATER)` = **GREATER** [tumble.c:84]
3. Proceed to right comparison: right = -5 + 3 = -2
4. `tumblercmp(+3, -2)`: signs differ → **GREATER** → return **TOMYRIGHT**

`TOMYRIGHT` means "the query address is to the right of this crum." In `crumqualifies2d` [retrie.c:283-290]:

```c
startcmp = whereoncrum (crumptr, offset, span1start, index1);
if( (startcmp > THRUME)){
    return (FALSE);
```

The span start address (+3 or any positive start) places it `TOMYRIGHT` of the negative crum → `crumqualifies2d` returns FALSE → crum is skipped.

The effect: **all negative-V crums are invisible to queries for positive V-addresses**. They sit in the POOM tree, consuming space, but are unreachable by any properly-formed retrieval.

This has been confirmed empirically: golden tests show that after a delete shifts link endset V-positions negative, `FOLLOWLINK` returns empty endsets (`[]`). The link's I-span in the spanfilade is permanent (Finding 0023/0024), but the V→I mapping path through the document POOM can no longer reach it.

---

### Does `intervalcmp` Order Negative Positions Before Positive Ones?

**Yes, definitively.** The ordering falls out directly from `tumblercmp` [tumble.c:72-85]:

```c
INT tumblercmp(tumbler *aptr, tumbler *bptr)
{
    if (iszerotumbler(aptr)){
        if (iszerotumbler(bptr)) return (EQUAL);
        else return (bptr->sign ? GREATER : LESS);   // 0 > negative
    }
    if (iszerotumbler(bptr))
        return (aptr->sign ? LESS : GREATER);        // negative < 0
    if (aptr->sign == bptr->sign)
        return (aptr->sign ? abscmp(bptr,aptr) : abscmp(aptr,bptr));  // both same sign
    return (aptr->sign ? LESS : GREATER);            // ← different signs: negative=LESS [line 84]
}
```

When signs differ: a negative tumbler (sign=1) always returns `LESS` vs any positive tumbler (sign=0). This is unconditional — no magnitude check is performed when signs differ.

`intervalcmp` [tumble.c:144-160] delegates entirely to `tumblercmp`:

```c
INT intervalcmp(tumbler *left, tumbler *right, tumbler *address)
{
    cmp = tumblercmp (address, left);
    if (cmp == LESS) return (TOMYLEFT);
    ...
}
```

If `address` is negative and `left` is positive: `tumblercmp(negative, positive)` = `LESS` → `TOMYLEFT`. A negative address lies *to the left* of any positive-bounded interval.

Within the negative range itself, `tumblercmp` is also correct for two negatives [tumble.c:82-83]:

```c
return (aptr->sign ? abscmp(bptr,aptr) : ...);  // when both negative, arguments reversed
```

`abscmp(bptr, aptr)` with both negative reverses the comparison to match signed ordering: `tumblercmp(-5, -2)` = `abscmp(|-2|, |-5|)` = `abscmp(2, 5)` = `LESS` ✓ (−5 < −2 numerically).

So `intervalcmp` correctly orders negatives before zero before positives. The problem is not an ordering bug — it is that the system creates and retains negative-V POOM entries via the delete-shift mechanism, and then *positive* queries never reach them.

---

### Summary

| Question | Answer | Key Citation |
|---|---|---|
| Can DELETE produce negative V-positions? | **Yes**, when deletion width > crum's relative V-displacement | `edit.c:63`, `tumble.c:406-440` |
| Does reading a positive V-span find shifted-negative content? | **No** — `whereoncrum` returns TOMYRIGHT for positive queries on negative crums | `retrie.c:345-398` |
| Does `intervalcmp` order negatives before positives? | **Yes** — unconditionally via sign-check in `tumblercmp` | `tumble.c:84` |
| Is a negative-V tumbler invalid? | **No** — only negative-zero (sign=1, mantissa=0) is checked | `tumble.c:180-181` |
| Is there a guard preventing new inserts at negative VSA? | Yes (`insertpm`), but it does not protect against shift-to-negative | `orglinks.c:93-96` |

The negative-V POOM entries are structural debris: they occupy tree space, pass tumbler validation, sort correctly relative to each other and to positive positions, but are permanently unreachable by any valid positive-address retrieval request. They represent a violation of POOM bijectivity (I₁) that the system neither detects nor recovers from. See Finding 0053 for golden test evidence.
