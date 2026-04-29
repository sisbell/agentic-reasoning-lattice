## Question 13 [gregory]

> When `slicecbcpm` splits a bottom crum at a DELETE boundary classified as THRUME, does the surviving fragment's I-width get recomputed from the new V-width, or is it sliced independently — and can the two ever diverge in tumbler exponent?

## KB Synthesis

The KB documents the pre/post conditions of `slicecbcpm` but not its internal mechanics directly. Here is what can be synthesized with confidence, and where the KB is silent.

---

## What the KB establishes

**The cut is identified in V-space.** `makecutsbackuptohere` calls `whereoncrum()` on V-addresses, and the THRUME guard fires only when `grasp_V < cut < reach_V` (strict inequalities). The local offset is then `localcut = tumblersub(cut, &grasp)` — a V-dimension subtraction [PRE-DELETE, `ndcuts.c:396`].

**Both pieces must have positive width in both dimensions.** [INV-NO-ZERO-WIDTH-CRUM] proves this from the strict interiority of the cut: `0 < localcut < cwid`. `locksubtract` at `ndcuts.c:444` computes the remainder, also guaranteed positive. These invariants hold for each piece independently, but the KB proves them only via V-space reasoning — it does not separately prove the I-dimension widths are positive.

**V-width and I-width encode the same integer at different precisions.** [SS-POOM-BOTTOM-CRUM] and [SS-INSERT-VWIDTH-ENCODING] establish that at INSERT time, V-width is produced by extracting `inc = tumblerintdiff(I_width, zero)` and re-encoding as `tumblerincrement(zero, shift, inc)` where `shift = tumblerlength(V_address) - 1`. The two representations have structurally different exponents by design — I-width uses ~9 tumbler digits, V-width uses ~2 — but `tumblerintdiff` on either always returns the same integer. [INV-WIDTH-VALUE-EQUIVALENCE] requires this to hold after every operation that creates or modifies bottom crums.

---

## The question the KB cannot answer

The KB does not contain `slicecbcpm` source code or a finding that directly documents its internal cut-point computation. Two plausible implementations both satisfy [INV-WIDTH-VALUE-EQUIVALENCE]:

1. **V-first, then I derived.** Compute `localcut_V` in V-space arithmetic. Extract its integer value via `tumblerintdiff`. Re-encode at I-precision for the I-width. This mirrors the [SS-INSERT-VWIDTH-ENCODING] pattern exactly.

2. **Independent slicing.** Compute `localcut_V` for the V-dimension and `localcut_I` for the I-dimension separately using each space's arithmetic. Since the crum represents a 1-to-1 V-to-I mapping across a contiguous range, the same integer count falls out of both calculations naturally.

Either path produces pieces where `tumblerintdiff(new_V_width) == tumblerintdiff(new_I_width)`.

---

## Can the exponents diverge?

They were already asymmetric before the split — this is structural, not pathological [SS-POOM-BOTTOM-CRUM]. After a THRUME split:

- The new V-width exponent is determined by the V-address precision of the cut (`shift = tumblerlength(cut_V) - 1`), consistent with [SS-INSERT-VWIDTH-ENCODING].
- The new I-width exponent is determined by I-address arithmetic, which operates at a much finer precision.

A *pathological* divergence — where the two representations encode *different integers* — cannot occur as long as [INV-WIDTH-VALUE-EQUIVALENCE] holds as a maintained invariant. The KB gives no evidence that `slicecbcpm` violates this invariant; [INV-NO-ZERO-WIDTH-CRUM] is proved specifically assuming the cut is THRUME, which is the same precondition under which `slicecbcpm` is invoked [PRE-DELETE, `ndcuts.c:77-90`].

The edge case in [EC-VWIDTH-ZERO-ADDRESS] — `shift = tumblerlength(vsaptr) - 1` producing anomalous exponents when `vsaptr` is zero — does not apply here because `slicecbcpm` is only reached from non-zero cut positions strictly interior to a non-zero-width crum.

---

## Summary

The KB establishes that `slicecbcpm` is called only for THRUME cuts, produces two pieces of strictly positive width, and must preserve [INV-WIDTH-VALUE-EQUIVALENCE]. Whether V and I dimensions are sliced independently or one is derived from the other is not documented — the KB is silent on `slicecbcpm` internals. What is documented is the invariant that must be maintained: integer value equality across representations, with a pre-existing and permanent exponent asymmetry that is a structural property of POOM bottom crums, not something the split can introduce or repair.

---

## Code Exploration

I now have all the code I need. Here is the complete answer:

---

## `slicecbcpm` at a THRUME DELETE boundary: I-width vs V-width

### The function and its invariants

`slicecbcpm` lives at `backend/ndcuts.c:373`. Its signature:

```c
int slicecbcpm(typecorecrum *ptr, typewid *offset, typecorecrum *new,
               tumbler *cut, INT index)
```

`ptr` is the crum being split; `new` will become the right fragment; `cut` is the cut address; `index` is the single dimension on which the THRUME test was applied.

**THRUME** is defined at `backend/common.h:88`:

```c
#define THRUME 0
```

It means `cut` lies strictly inside `[grasp, grasp + cwid)` in the `index` dimension. The guard at `ndcuts.c:383` fires a `gerror` if the cut is not THRUME before proceeding.

**Precondition on widths**: `ndcuts.c:389` runs:

```c
if (!lockis1story (ptr->cwid.dsas, (unsigned)widsize(enftype)))
    gerror ("Not one story in POOM wid\n");
```

`lockis1story` (`wisp.c:298-304`) checks every dimension in `cwid` for `is1story`, which (`tumble.c:237-247`) verifies `mantissa[1..NPLACES-1]` are all zero. So before any split, **every dimension of the crum width must be a single-digit tumbler** — i.e., of the form `{exp: E, mantissa[0]: M, rest 0}`.

For POOM crums, `widsize(POOM) = WIDSIZEPM = 2` (`wisp.h:27`, `wisp.h:60`), so `cwid.dsas` has two tumblers: `[0]` = V-space width, `[1]` = I-space width.

---

### Computing `localcut`

```c
tumblersub (cut, &grasp.dsas[index], &localcut);   // ndcuts.c:396
```

`grasp.dsas[index]` is the left boundary of the crum in the `index` dimension (computed by `prologuend` at `retrie.c:334-339` as `offset + ptr->cdsp`). So `localcut` is the cut's offset within the crum — but **only in the `index` dimension** (typically V, the dimension where THRUME was established for a delete).

Two further guards on `localcut`:

- `ndcuts.c:398`: `localcut.exp == ptr->cwid.dsas[index].exp` — same tumbler exponent as the V-width
- `ndcuts.c:410`: `is1story(&localcut)` — `localcut` is itself a single-digit tumbler

So `localcut = {exp: E_v, mantissa[0]: L, rest 0}` where `0 < L < M_v` (strictly inside by THRUME).

---

### The split loop — the key section

```c
movewisp (&ptr->cwid, &newwid);                          // ndcuts.c:438
for (i = 0; i < widsize(enftype); i++) {   /* I really don't understand this loop */
    newwid.dsas[i].mantissa[0] = localcut.mantissa[0];   // ndcuts.c:440
    tumblerjustify (&newwid.dsas[i]);                     // ndcuts.c:441
}
locksubtract ((tumbler*)&ptr->cwid, (tumbler*)&newwid,
              (tumbler*)&new->cwid, (unsigned)widsize(enftype)); // ndcuts.c:444
movewisp (&newwid, &ptr->cwid);                          // ndcuts.c:445
dspadd (&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype);   // ndcuts.c:446
```

The comment at line 439 — **`/* I really don't understand this loop */`** — is in the original source.

Step by step:

1. `movewisp` copies all of `ptr->cwid` into `newwid`, both dimensions.
2. The loop runs for `i = 0` (V-dim) and `i = 1` (I-dim).
   - **For both**, it overwrites `newwid.dsas[i].mantissa[0]` with `localcut.mantissa[0]` (= `L`).
   - The exponent is **not touched** — each `newwid.dsas[i].exp` remains whatever the original crum width's exponent was for that dimension.
   - `tumblerjustify` normalizes leading zeros (shifts mantissa and decrements exp if `mantissa[0] == 0`).
3. `locksubtract` (`wisp.c:275-279`) calls `tumblersub` independently on each dimension:
   - right V-width: `tumblersub(&ptr->cwid.dsas[0], &newwid.dsas[0], &new->cwid.dsas[0])`
   - right I-width: `tumblersub(&ptr->cwid.dsas[1], &newwid.dsas[1], &new->cwid.dsas[1])`
4. `movewisp` installs `newwid` as `ptr->cwid` (the left fragment).

**The I-width is sliced independently.** It is not recomputed from the V-width. The same `localcut.mantissa[0]` value is injected into both `newwid.dsas[0]` and `newwid.dsas[1]`, but the subtraction that produces each fragment's width runs separately per dimension, with no cross-dimension awareness.

---

### What each fragment gets

Let the original crum have:
- V-width: `{exp: E_v, mantissa[0]: M_v, rest 0}`
- I-width: `{exp: E_i, mantissa[0]: M_i, rest 0}`
- Cut localcut: `{exp: E_v, mantissa[0]: L}`, with `0 < L < M_v`

After the loop, `newwid`:
- dim 0: `{exp: E_v, mantissa[0]: L}`
- dim 1: `{exp: E_i, mantissa[0]: L}`  ← **same L, but original I-exponent**

**Left fragment** (`ptr->cwid = newwid`):
- V-width: `{exp: E_v, mantissa[0]: L}`
- I-width: `{exp: E_i, mantissa[0]: L}`

**Right fragment** (`new->cwid = ptr->cwid - newwid` via `strongsub`):

`strongsub` (`tumble.c:534-565`) with two 1-story tumblers of the same exponent and `M ≠ L`:

```c
answer.exp = aptr->exp;              // tumble.c:548
for (i = 0; aptr->mantissa[i] == bptr->mantissa[i]; ++i) {
    --answer.exp;                    // tumble.c:550
    ...
}
answer.mantissa[0] = aptr->mantissa[i] - bptr->mantissa[i];  // tumble.c:556
```

Because `M_v ≠ L` (THRUME ensures strict interior), the first digit comparison at line 549 fails immediately — zero iterations — so:
- right V-width: `{exp: E_v, mantissa[0]: M_v - L}`
- right I-width: `{exp: E_i, mantissa[0]: M_i - L}`

---

### Can V and I exponents diverge?

**The split cannot create new exponent divergence where none existed.**

If the original crum had `E_v == E_i`, both fragments will also have equal exponents in V and I after the split. The `strongsub` exponent logic (`tumble.c:548-554`) only decrements exp when *matching leading digits* are found — and with `M ≠ L`, the very first comparison fails, so `answer.exp = aptr->exp` (the original dimension's exponent, unchanged).

**Pre-existing divergence is preserved.** If `E_v ≠ E_i` in the original crum, both output fragments will have `E_v` in their V-widths and `E_i` in their I-widths. The split makes no attempt to equalize them.

**One edge case that can produce I-width zero**: THRUME is tested only in the `index` dimension (V). There is no guard that `L < M_i`. If `M_i == L`, then `M_i - L = 0` and after `tumblerjustify` inside `tumblersub` (`tumble.c:289-313`), the right fragment's I-width becomes the zero tumbler (`{exp: 0, sign: 0, mantissa: all 0}`). If the V-width is non-zero with exponent `E_v`, this produces `E_v ≠ 0 = E_i` — exponent divergence introduced by the split itself. There is no code guard against this scenario; only the application-layer invariant that POOM crums maintain equal V-span and I-span (a 1:1 content mapping) prevents it in practice.

---

### Summary

| Question | Answer |
|---|---|
| Is I-width recomputed from new V-width? | **No.** The same `localcut.mantissa[0]` is injected into both dimensions' `newwid.dsas[i]` in the loop at `ndcuts.c:439-442`, then each is subtracted independently via `locksubtract`. |
| Are they sliced independently? | **Yes.** `locksubtract` calls `tumblersub` once per dimension with no inter-dimension coordination (`wisp.c:275-279`). |
| Can exponents diverge from the split? | **Not from the arithmetic itself** — `strongsub` preserves each dimension's original exponent when the 1-story precondition holds. Pre-existing divergence (`E_v ≠ E_i`) is passed through unchanged. The one true divergence risk is if `L == M_i` (I-width right-fragment goes to zero), but THRUME only guards `L < M_v`, not `L < M_i`. |
| Programmer's confidence in the loop? | Low — it is annotated `/* I really don't understand this loop */` at `ndcuts.c:439`. |
