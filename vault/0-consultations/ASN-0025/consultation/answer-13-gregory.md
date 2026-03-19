## Question 13 [gregory]

> After INSERT shifts V-positions rightward via `makegappm`, do the shifted POOM entries retain their exact original I-address values byte-for-byte, or could the tumbler arithmetic in `tumbleradd` introduce any rounding, normalization, or exponent change that alters the I-address representation?

## KB Synthesis

The I-address values in shifted POOM entries are completely unaffected — byte-for-byte identical before and after the shift.

**The mechanism is dimensional isolation.** The `makegappm` shift call (from [ST-INSERT] / Finding 0054) is:

```c
tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V])
```

This explicitly targets only `dsas[V]` — the V-dimension of the POOM crum's displacement. The I-dimension `dsas[I]` is a separate field and is never passed to `tumbleradd`. No arithmetic of any kind touches it during the shift phase.

**This is not accidental.** [ST-REARRANGE] / Finding 0056 confirms the same design for REARRANGE's displacement arithmetic: *"The code modifies only `ptr->cdsp.dsas[index]` (the V-address component of the displacement). The I-address, stored separately, is never touched."* `makegappm`'s shift follows the same convention.

**The `setwispupwards` concern.** After insertion, `setwispnd` recalculates the tree's root displacement across all dimensions (Finding 0066). For a 2D enfilade, this absorbs the minimum child displacement — including the I-dimension — into the parent and adjusts children to relative encoding. However, this is purely a representational change: the *absolute* logical I-address (sum of ancestor I-displacements + node's I-displacement) is invariant under this re-encoding. No content identity is altered; only how displacements are split between parent and child nodes in the tree structure.

**The invariants confirm it globally:**
- [INV-IADDR-IMMUTABILITY]: *"INSERT shifts V-addresses but preserves every existing I-address assignment. Content 'C' that had I-address I.3 before insertion still has I-address I.3 after insertion."*
- [FC-INSERT-IADDR]: *"INSERT does not modify the I-address of any pre-existing content... No I-address is lost; they may appear at different V-positions but the I-address itself is invariant."*

**Bottom line:** No rounding, normalization, or exponent change to I-addresses is possible because `tumbleradd` is never applied to `dsas[I]` during the shift. The only tumbler arithmetic during `makegappm` is on the V-dimension, and the two dimensions of a POOM crum are stored and modified independently.

---

## Code Exploration

I now have everything needed. Here is the complete answer.

---

## Answer: I-addresses are preserved byte-for-byte after `makegappm`

### The single `tumbleradd` call in `makegappm` touches only `dsas[V]`

The entire gap-making logic in `makegappm` iterates over POOM children of the insertion point and classifies each one with `insertcutsectionnd`. For nodes that fall to the right of the cut (case `1`), it shifts their V-displacement:

**`insertnd.c:161–164`:**
```c
case 1:/*9-17-87 fix */
    tumbleradd(&ptr->cdsp.dsas[V],&width->dsas[V],&ptr->cdsp.dsas[V]);
    ivemodified (ptr);
    break;
```

`dsas[V]` is index `1` — the V-dimension. `dsas[I]` is index `0` — the I-dimension. This is defined unambiguously in `wisp.h:19–20`:

```c
#define I  0
#define V  1
```

The I-address field `ptr->cdsp.dsas[I]` is **never written** in `makegappm`. The loop body only ever modifies `dsas[V]`, or does nothing (cases `0` and `2`). `insertcutsectionnd` (`edit.c:207–233`) is purely a classifier — it calls `whereoncrum` to determine position and returns an integer; it does not modify any tumbler fields.

---

### What `absadd` does to the V-dimension (and what it cannot do to I)

`tumbleradd` is a macro that expands to `functiontumbleradd` (`common.h:197`). In the same-sign case (the only one that applies to a positive V-shift), `functiontumbleradd` calls `absadd` (`tumble.c:374–376`):

```c
} else if (aptr->sign == bptr->sign) {
    absadd (aptr, bptr, cptr);
    cptr->sign = aptr->sign;
```

**`absadd` (`tumble.c:460–484`)** performs digit-by-digit alignment and addition without carry propagation. When `aptr->exp == bptr->exp`, it does:

```c
ansmant[0] = amant[0] + bmant[0];
```

There is no carry into `ansmant[1]`. If the sum overflows `tdigit` (defined as `UINT`, `common.h:57`), the result wraps silently. This is a latent overflow risk in V-arithmetic, but it is structurally impossible for it to affect I-addresses because `absadd` is only ever called on the V-component.

**No post-add normalization occurs.** The `functiontumbleradd` code has this comment at `tumble.c:377–383`:

```c
/*absadd returns justified result so no need to justify*/
/*
if(cptr->mantissa[0] == 0){
    partialtumblerjustify (cptr);
}
*/
```

The call to `partialtumblerjustify` is commented out for same-sign additions. `absadd` itself also does not call `tumblerjustify`. Since `tumbleradd` only operates on V-displacements, none of this normalization logic touches I-addresses regardless.

---

### `movetumbler` is a raw struct copy — no transformation

`movetumbler` is defined as:

**`common.h:73`:**
```c
#define movetumbler(A,B) (*((tumbler *)(B)) = *((tumbler *)(A)))
```

A plain struct assignment. No arithmetic, no normalization, no field reinterpretation. Whenever a node is moved in the tree during cuts (`makecutsnd`) and insertion, its I-address is carried unchanged.

---

### Summary

| Component | Touched by `makegappm`? | Arithmetic applied? | Normalization risk? |
|---|---|---|---|
| `ptr->cdsp.dsas[I]` | **No** | **None** | **None** |
| `ptr->cdsp.dsas[V]` | Yes | `absadd` (no carry, no justify) | Overflow possible on carry |

The shifted POOM entries retain their exact original I-address values (`cdsp.dsas[I]`) byte-for-byte. The `tumbleradd` call in `makegappm` is surgically scoped to `dsas[V]`. The `absadd` implementation does not normalize, justify, or canonicalize its result for same-sign addition — and even if it did, I-addresses are not operands or outputs of any `tumbleradd` call in this path.
