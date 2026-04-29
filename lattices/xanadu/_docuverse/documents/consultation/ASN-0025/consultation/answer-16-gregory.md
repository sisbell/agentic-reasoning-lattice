## Question 16 [gregory]

> When `strongsub`'s exponent guard fires during DELETE and returns a link V-position unchanged, is this a guaranteed no-op on the POOM entry (the crum is literally not touched), or does the code write back the same value, risking any subtle modification through the write path?

## KB Synthesis

The KB gives us enough to answer this precisely, though with one residual uncertainty.

## What `strongsub` actually does on the exponent guard

From [SS-TUMBLER] / [FC-SUBSPACE] (Finding 0055), the guard at `tumble.c:544` is:

```c
if (bptr->exp < aptr->exp) { movetumbler(aptr, cptr); return(0); }
```

The call site from [ST-DELETE] (Finding 0055) is:

```c
// edit.c:63
tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index])
```

Notice that the first argument (input `a`) and the third argument (output `c`) are **the same pointer**: `&ptr->cdsp.dsas[index]`. So when `strongsub` fires the exponent guard and executes `movetumbler(aptr, cptr)`, it is copying the tumbler from a memory address **to itself**.

**This is not a true no-op at the memory level.** The write path is exercised — `movetumbler` performs a memory copy, it just happens to copy `x` into `x`. The crum's V-displacement field is written, but with its own current value.

## The residual uncertainty: dirty marking

The KB documents that on INSERT, `ivemodified()` is called to mark the crum and its ancestors as `modified = TRUE` ([SS-CACHE-MECHANISM], Finding 0059). For DELETE, the KB does not specify exactly where in `deletend()`'s Case 2 path `ivemodified()` is called relative to the `tumblersub` invocation.

- If `ivemodified()` is called **unconditionally** for every Case 2 crum that `deletend` visits, then link crums at `2.x` would be unnecessarily marked dirty and queued for a disk write by the grim reaper — a performance cost but no correctness issue.
- If `ivemodified()` is called **only when `tumblersub` actually changes the value**, then the link crum's dirty bit is never set and the write is completely skipped.

The KB's code references don't resolve this distinction; it would require reading `edit.c:31-76` directly.

## Spec implication

For the formal model, the consequence is clear either way: **the V-displacement value of the link crum is unchanged** — `entry.vpos' = entry.vpos` holds as a value invariant [FC-SUBSPACE]. Whether the implementation writes an identical value back is an implementation detail beneath the abstraction boundary. The frame condition `∀ entry with entry.vpos.exp > width.exp : entry.vpos' = entry.vpos` is satisfied in both cases. The dirty-marking question is relevant only to the durability/performance model ([SS-DURABILITY-BOUNDARY]), not to the behavioral specification.

---

## Code Exploration

I have everything I need. Here is the complete analysis.

---

## Answer

**The exponent guard is a guaranteed no-op. The POOM crum field is not modified — not even a same-value write-back in any meaningful sense, because the output pointer aliases the input pointer, making the write a C struct self-assignment.**

---

### 1. The `movetumbler` macro

`common.h:73`:
```c
#define movetumbler(A,B) (*((tumbler *)(B)) = *((tumbler *)(A)))
```

It is a plain struct-copy via `=`. When `A == B`, this becomes `*A = *A` — a C self-assignment. The C standard gives no undefined behaviour for this; the stored bytes are unchanged.

---

### 2. The exponent guard in `strongsub`

`tumble.c:534–547`:
```c
int strongsub(tumbler *aptr, tumbler *bptr, tumbler *cptr)
{
  tumbler answer;          // local, stack-only
  register INT i, j;

    tumblerclear(&answer); // clears local 'answer' — does NOT touch cptr
    if (tumblereq (aptr, bptr)) {
        movetumbler (&answer, cptr);  // would write zero — but only if equal
        return(0);
    }
    if (bptr->exp < aptr->exp) {   // ← THE GUARD
        movetumbler(aptr,cptr);    // ← the write in question
        return(0);
    }
    ...
```

Before the guard fires, only two things happen:

- `tumblerclear(&answer)` — writes to the **local** `answer` variable; the crum is not referenced.
- `tumblereq(aptr, bptr)` — a pure comparison; no write.

So if the guard fires, the crum has not been touched at all yet.

---

### 3. Pointer aliasing through the DELETE call chain

The delete path is `edit.c:63`:
```c
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
```

`ptr->cdsp.dsas[index]` is the POOM crum's displacement tumbler in the V-space dimension (`enf.h:47–48`, `wisp.h:50–51`). Crucially, **the same address is passed as both `aptr` (arg 1) and `cptr` (arg 3).**

This aliasing propagates through every layer:

| Frame | `aptr` | `cptr` | Same address? |
|---|---|---|---|
| `tumblersub` (`tumble.c:406`) | `&cdsp.dsas[index]` | `&cdsp.dsas[index]` | yes |
| → `tumbleradd` / `functiontumbleradd` (`tumble.c:428`, `385`) | `&cdsp.dsas[index]` | `&cdsp.dsas[index]` | yes |
| → → `strongsub` (`tumble.c:385`) | `&cdsp.dsas[index]` | `&cdsp.dsas[index]` | yes |

Inside `tumblersub`, the else-branch (`tumble.c:426–429`) copies `bptr` (`width`) into a local `temp` on the stack, negates its sign, and calls `tumbleradd(aptr, &temp, cptr)`. The local `temp` is the `bptr` that reaches `strongsub`. The `aptr`/`cptr` aliasing is preserved throughout.

---

### 4. What the guard actually executes

When the guard fires inside `strongsub`, with `aptr == cptr == &ptr->cdsp.dsas[index]`:

```c
movetumbler(aptr, cptr);
// expands to:
*((tumbler *)(cptr)) = *((tumbler *)(aptr));
// with aptr == cptr, this is:
*((tumbler *)(&cdsp.dsas[index])) = *((tumbler *)(&cdsp.dsas[index]));
// i.e., the struct copies itself to itself — no bytes change.
```

---

### 5. Nothing after `strongsub` touches the crum either

Back in `functiontumbleradd` (`tumble.c:385–389`):
```c
strongsub (aptr, bptr, cptr);   // returned with guard — cptr unchanged
cptr->sign = aptr->sign;         // aptr == cptr: self-assignment of sign field, no-op
if(cptr->mantissa[0] == 0){      // false for a normalized V-position tumbler
    partialtumblerjustify (cptr);
}
```

Back in `tumblersub` (`tumble.c:430`):
```c
tumblerjustify (cptr);
```
`tumble.c:296–298`:
```c
if (mantissaptr[0] != 0) {
    return(0);   // exits immediately for a normalized tumbler
}
```

A valid link V-position tumbler is always normalized (`mantissa[0] != 0`), so `tumblerjustify` exits without touching anything.

---

### 6. Conclusion

The exponent guard in `strongsub` is a **guaranteed no-op** on the POOM crum. The code does issue a write via `movetumbler(aptr, cptr)` (`tumble.c:545`), but because `aptr` and `cptr` are the same pointer (both resolved from `&ptr->cdsp.dsas[index]` at `edit.c:63`), the write is a C struct self-assignment: `*cptr = *cptr`. No byte of the crum's `cdsp.dsas[index]` field changes value. The crum is **literally not touched in any observable way**.

There is no write path that could introduce subtle modification: the only write is the self-assignment, and every subsequent operation (`cptr->sign = aptr->sign`, the `tumblerjustify` early-exit) is also a no-op for a well-formed V-position tumbler.
