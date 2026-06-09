## Question 2 [evidence]

> When udanax-green processes a COPY (transclusion) spec, does it require or normalize the source span's action point to sit at the deepest component (ordinal-level), or does it accept spans whose action point is above the last component and resolve them anyway?

## KB Synthesis

The KB does not contain a finding that directly tests whether COPY normalizes span action points to ordinal depth. What it does say:

**No normalization or depth enforcement occurs in the backend.**

`docopy()` → `specset2ispanset()` → `permute()` → `span2spanset()` → `retrieverestricted()` is entirely type-agnostic and hierarchy-blind. The POOM lookup resolves whatever V-address is supplied against the stored V→I mappings without enforcing any tumbler depth structure. [PRE-SPECSET, FC-SUBSPACE, SS-DUAL-ENFILADE]

**Backend validation is document-existence only.**

`specset2sporglset()` checks that the referenced document exists but explicitly does not enforce element-level tumbler structure. A specset with an action point above the last component is accepted without error; element-level correctness is the client's obligation. [PRE-SPECSET, INT-CLIENT-VALIDATION]

**Consequence for COPY:** A span whose action point is above ordinal depth will resolve against whatever I-addresses happen to be mapped in the POOM at that V-address range — no normalization, no rejection. If nothing is mapped there, `retrieverestricted()` returns NULL and the address is silently dropped from the result. [INV-ITOV-FILTERING, SS-FOLLOWLINK]

The KB has no finding that tests this edge case directly, so I cannot confirm the exact behavior when a non-ordinal action point spans content that *does* exist. The above is the limit of what can be derived from recorded findings.

---

## Code Exploration

I now have everything I need. Here is the complete answer.

---

## Answer: COPY Action Point Depth Handling in udanax-green

### The Short Answer

udanax-green **does not require and does not normalize** the action point (vsaptr) to the ordinal (deepest) level. It accepts a vsaptr at any tumbler depth and uses the depth parametrically to compute the V-dimension width of the inserted crum. There is no guard, clamp, or normalization anywhere in the call chain.

---

### Execution Path

#### 1. Entry: `fns.c:35-47`

```c
void copy(typetask *taskptr)
{
  typeisa docisa, vsa;
  typespecset localspecset;
  ...
    if (
       getcopy (taskptr, &docisa, &vsa, &localspecset)
    && docopy (taskptr, &docisa, &vsa, localspecset))
        putcopy (taskptr);
      else
        putrequestfailed (taskptr);
}
```

`getcopy` deserializes the FEBE packet and populates `vsa` — the V-Space Address (action point). Its depth is whatever the client sent. No checking happens here.

---

#### 2. Validation Gate: `do1.c:45-65` → `do2.c:110-113`

`docopy` calls:

```c
   specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
&& findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& acceptablevsa (vsaptr, docorgl)          /* do1.c:56 */
&& asserttreeisok(docorgl)
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
```

The sole validation of the action point is `acceptablevsa`. Its full body in `do2.c:110-113`:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

This is a **stub that unconditionally passes**. There is no check on tumbler depth, story count, or ordinal position.

---

#### 3. Actual Insertion: `orglinks.c:75-134`

`insertpm` is where the action point is consumed. Two checks exist, neither concerning depth:

- **`orglinks.c:86-91`**: rejects a zero vsaptr (returns FALSE)
- **`orglinks.c:93-98`**: rejects a negative vsaptr (calls `gerror`)

Then the depth-parameterized logic:

```c
movetumbler (vsaptr, &crumorigin.dsas[V]);          /* line 113 — vsaptr becomes V-origin */
/*I'm suspissious of this shift <reg> 3/1/85 zzzz*/
shift = tumblerlength (vsaptr) - 1;                 /* line 115 */
inc = tumblerintdiff (&lwidth, &zero);              /* line 116 */
tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);  /* line 117 */
```

The vsaptr's depth is used **directly as the shift parameter** for computing the V-dimension width of the new crum.

---

#### 4. What `shift` means: `tumble.c:259-262` and `:599-623`

```c
INT tumblerlength(tumbler *tumblerptr)
{
    return (nstories (tumblerptr) - tumblerptr->exp);   /* tumble.c:261 */
}
```

`nstories` counts significant mantissa digits. `tumblerlength` = stories − exp, which gives the effective "depth" of the address (how many components deep it is).

`tumblerincrement(&zero, shift, inc, &result)` at `tumble.c:599-623`:
```c
if (iszerotumbler (aptr)) {
    cptr->exp = -rightshift;       /* shift becomes negative exponent */
    cptr->mantissa[0] = bint;
    return(0);
}
```

So with `shift=0`, the V-width is an integer-level quantity (e.g., N). With `shift=1`, it is a sub-level quantity (0.N). With `shift=2`, sub-sub-level (0.0.N). The depth of the action point determines the *granularity* of the new V-span.

---

### The Suspicious Comment

The comment at `orglinks.c:114` is from Gregory himself, dated 3/1/85:

```c
/*I'm suspissious of this shift <reg> 3/1/85 zzzz*/
```

The same pattern (`tumblerlength(tumblerptr)-1`) appears in `do2.c:58` inside `tumbler2spanset`, also annotated with `/*zzzzz*/`. These are author-placed uncertainty markers on the depth-parameterized design — the shift arithmetic was recognized as potentially fragile even when written.

---

### Summary Table

| Location | What happens to vsaptr depth | Normalization? |
|---|---|---|
| `fns.c:42` — `getcopy` | Populated from wire format | None |
| `do2.c:110-113` — `acceptablevsa` | Unconditionally accepted | None |
| `orglinks.c:86-98` — zero/negative guard | Zero and negative rejected | None |
| `orglinks.c:115` — `tumblerlength(vsaptr)-1` | Depth read and used as shift | None — depth is preserved and propagated |
| `tumble.c:599-623` — `tumblerincrement` | Shift sets V-width resolution | None — depth determines output granularity |

**Conclusion:** The system accepts action points at any tumbler depth and resolves them as-is. The action point's depth parametrically controls the resolution of the inserted V-span: a shallow (e.g., 1-story) action point produces an integer-level V-width; a deep (ordinal-level) action point produces a finer V-width. The design is parametric, not normalizing. No code enforces or promotes the action point to the ordinal level.
