## Question 11 [gregory]

> The `strongsub` exponent guard (line 544 of `tumble.c`) returns `a` unchanged when `b.exp < a.exp` — was this an intentional algebraic design choice to make subtraction a no-op across exponent classes, or a defensive guard against a specific bug?

## KB Synthesis

The KB evidence points toward an algebraic property of the implementation rather than a deliberate defensive guard — but cannot fully resolve the intent question.

**What the KB establishes:**

[SS-TUMBLER] Finding 0055 characterizes it explicitly: *"This is not a deliberate subspace guard — it is a property of how `strongsub` handles cross-exponent arithmetic."* The guard at `tumble.c:544` reads: `if (bptr->exp < aptr->exp) { movetumbler(aptr, cptr); return(0); }` — when the subtrahend has a smaller exponent than the minuend, return the minuend unchanged.

**The algebraic reading:**

Tumblers use a sign-magnitude representation where the exponent encodes hierarchical scale. `2.1` (exp=0) and `0.3` (exp=-1) operate at fundamentally different scales — one is an address like a street address, the other is an offset like a room number. Under this interpretation, `strongsub` is saying: *I don't know how to subtract a sub-scale quantity from a whole-scale quantity, so I return the whole unchanged*. That's a coherent algebraic position, not obviously wrong.

**The fragility evidence:**

[INT-DELETE-SUBSPACE-ASYMMETRY] is unambiguous: INSERT's subspace isolation was *deliberately designed* — `findaddressofsecondcutforinsert()` has explanatory source comments about its purpose. DELETE's subspace isolation through `strongsub` has no such comments. This asymmetry is described as a "fragility risk" — if someone "corrected" `strongsub` to handle cross-exponent subtraction, DELETE would break subspace isolation while INSERT would remain unaffected [FC-SUBSPACE, Finding 0055].

**My read:**

The `strongsub` behavior looks like a pragmatic algebraic decision — cross-exponent subtraction was either undefined or unneeded for the use cases at hand, so the implementation returns the minuend unchanged rather than attempting mixed-scale arithmetic. Whether that was a conscious design choice or the path of least resistance is unknowable from the code alone.

What I'm confident about: it was *not* inserted as a subspace protection mechanism. That's a consequence the original authors appear not to have noticed or documented. The KB has no citation showing anyone wrote "this guard protects subspace isolation in DELETE" — that connection was only reconstructed by analysis [Finding 0055].

---

## Code Exploration

Now I have everything I need. Let me write the full analysis.

---

## The `strongsub` Exponent Guard at `tumble.c:544`

### What the guard does

```c
// tumble.c:534-565
int strongsub(tumbler *aptr, tumbler *bptr, tumbler *cptr)
{
  tumbler answer;
  register INT i, j;

    tumblerclear(&answer);
    if (tumblereq (aptr, bptr)) {           // line 540 — equal case: return zero
        movetumbler (&answer, cptr);
        return(0);
    }
    if (bptr->exp < aptr->exp) {            // line 544 — THE GUARD
        movetumbler(aptr,cptr);
        return(0);
    }
    answer.exp = aptr->exp;
    for (i = 0; aptr->mantissa[i] == bptr->mantissa[i]; ++i) {   // line 549
        --answer.exp;
        ...
    }
    answer.mantissa[0] = aptr->mantissa[i] - bptr->mantissa[i];  // line 556
```

When `bptr->exp < aptr->exp`, the guard fires and returns `aptr` unchanged into `cptr`.

---

### What `exp` means

From `common.h:59-65`, the tumbler struct:

```c
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign;
    short exp;               // exponent of most-significant digit; always <= 0
    tdigit mantissa[NPLACES]; // NPLACES = 16
} tumbler;
```

`tumblercheckptr` (`tumble.c:174`) treats `exp > 0` as a hard error (`"bad exp"`). So `exp` is always `<= 0`. The mantissa digit at `mantissa[i]` is at hierarchical scale `i` levels below `exp`. Larger `exp` (less negative) means larger magnitude — confirmed by `abscmp` at `tumble.c:92-97`:

```c
if (aptr->exp != bptr->exp) {
    if (aptr->exp < bptr->exp) {
        return(LESS);
    } else {
        return(GREATER);
    }
}
```

A tumbler with `exp=0, mantissa=[3]` is address `3`. With `exp=-1, mantissa=[3,2]` it is address `3.2` — a sub-address one level deeper. Comment in `common.h:53`: NPLACES was *"increased from 11 to support deeper version chains"* — confirming that `exp` depth is the version/sub-version hierarchy.

---

### When `strongsub` is called

`functiontumbleradd` at `tumble.c:384-395`:

```c
} else if (abscmp (aptr, bptr) == GREATER) {
    strongsub (aptr, bptr, cptr);          // |a| > |b|
    cptr->sign = aptr->sign;
    ...
} else {
    weaksub (bptr, aptr, cptr);            // |b| >= |a|
    cptr->sign = bptr->sign;
    ...
}
```

`strongsub` is called exactly when `|a| > |b|`. Since `abscmp` ranks purely by `exp` when exponents differ (`tumble.c:92-97`), `|a| > |b|` is satisfied in two cases:

1. **Same exponent** (`a.exp == b.exp`) but `a.mantissa > b.mantissa`
2. **Different exponents** (`a.exp > b.exp`) — regardless of mantissa

The guard at line 544 fires exclusively in case 2.

---

### Why the algorithm below the guard would fail without it

The core loop at `tumble.c:549-556`:

```c
answer.exp = aptr->exp;
for (i = 0; aptr->mantissa[i] == bptr->mantissa[i]; ++i) {
    --answer.exp;
    ...
}
answer.mantissa[0] = aptr->mantissa[i] - bptr->mantissa[i];
```

This compares `a.mantissa[i]` to `b.mantissa[i]` positionally, assuming both start at the same scale. It works correctly when `a.exp == b.exp`.

When `a.exp > b.exp` — say `a.exp = 0` and `b.exp = -1` — `a.mantissa[0]` is at level 0, but `b.mantissa[0]` is at level −1 (one hierarchy deeper). Comparing them positionally is category confusion: the algorithm would compute `a[0] − b[0]` as if they're at the same scale, producing a value that has no correct interpretation in either address space. There is no conditional, shift, or alignment step in `strongsub` for this cross-exponent case.

**Contrast with `weaksub`** (`tumble.c:567-589`), which IS called with cross-exponent tumblers (when `|b| >= |a|`, `b.exp >= a.exp`). It handles the mismatch correctly:

```c
answer.exp = aptr->exp;          // aptr here is the LARGER arg (b in the outer call)
expdiff = aptr->exp - bptr->exp; // >= 0
for (i = 0; i < expdiff; ++i) {
    answer.mantissa[i] = aptr->mantissa[i]; // copy high-order digits of a not reached by b
}
answer.mantissa[i] = aptr->mantissa[i] - bptr->mantissa[0]; // subtract at the overlap point
```

`weaksub` explicitly computes `expdiff` and copies the non-overlapping high-order digits of the larger argument first. `strongsub` has no such mechanism. The asymmetry is the key tell: whoever wrote `weaksub` knew how to handle cross-exponent subtraction, yet `strongsub` lacks it.

---

### Is returning `a` mathematically correct?

Only in a truncation sense. If `a = 5` (exp=0) and `b = 0.32` (exp=−1), then `a − b = 4.68`, not `5`. The guard returns `5`, which is wrong in exact arithmetic.

However, there is a plausible precision rationale: when `b.exp < a.exp`, `b`'s most-significant digit is at a finer hierarchical level than `a`'s least-significant digit. If `b` falls entirely below `a`'s resolution, the truncated result would be `a`. The guard fires on *any* exponent mismatch, not just the truly-negligible case — so it over-applies this truncation. It does not check whether `|b|` is actually below the least-significant digit of `a`.

---

### Was there a specific bug this prevented?

There is no comment on the guard, no named bug reference, and no disabled test pointing to a crash here. What the code record does show is:

- The guard was written inline, without any diagnostic `fprintf` or `gerror` branch (unlike the many other guards in `tumblercheckptr` and elsewhere that do emit diagnostics for truly invalid states). This implies it was not written as a hard-error catch.
- The body `movetumbler(aptr,cptr); return(0)` is identical in structure to the `tumblereq` equality guard two lines above — both are silent no-ops. The pair reads as two "bail out early if this case won't work" guards, not as one assertion and one design choice.
- `weaksub` correctly handles the analogous cross-exponent case via `expdiff`, but `strongsub` never got that treatment. The most parsimonious explanation is that `strongsub`'s algorithm was written only for the same-exponent case, and the guard was added to prevent the broken path from executing when real data occasionally triggered the cross-exponent branch.

---

### Verdict

The guard at `tumble.c:544` is **a defensive measure against a broken algorithm path, not an intentional algebraic design choice.**

The algorithm below it (`tumble.c:549-556`) is only correct when `a.exp == b.exp`. It has no mechanism to align digits from different exponent levels. Without the guard, it would silently produce garbage when `a.exp > b.exp`. The guard was added to make `strongsub` safe for that input rather than to define a principled "subtraction across exponent classes is a no-op" semantics.

The result of returning `a` unchanged is a coincidental approximation — defensible only when `b` happens to be negligibly small relative to `a`'s precision, which the guard does not verify. The absence of any explanatory comment, the absence of an error branch, and the contrast with `weaksub`'s explicit `expdiff` handling all point to a quick protective fix rather than a deliberate algebraic invariant.
