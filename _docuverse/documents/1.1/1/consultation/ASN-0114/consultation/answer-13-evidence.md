## Question 13 [evidence]

> Must the returned spec-set be a value-exact copy of the I-address spans the link orgl records at that endset position, or can it differ in tumbler exponent representation between the stored I-width and the returned width?

## KB Synthesis

The returned spec-set **can differ in tumbler exponent representation** from the I-address spans stored in the link orgl.

## Why the representations diverge

FOLLOWLINK does not return I-addresses directly. The call chain is [SS-FOLLOWLINK]:

1. `link2sporglset()` extracts I-addresses from the link orgl via `retrieverestricted()`
2. `linksporglset2specset()` converts those I-addresses to V-addresses by looking them up in the homedoc's POOM

The POOM bottom crums store **dual-space coordinates with asymmetric precision** [SS-POOM-BOTTOM-CRUM]: I-widths use 6–9 tumbler digits (e.g., `0.0.0.0.0.0.0.0.11`), while V-widths use 2 digits (e.g., `0.11`). These are different tumbler representations of the same integer.

The encoding rule is explicit [SS-INSERT-VWIDTH-ENCODING]: during `insertpm`, V-width is computed as `tumblerincrement(zero, shift, inc, &V-width)` where `shift = tumblerlength(vsaptr) - 1`. This re-encodes the I-width's integer value at V-space precision, producing a structurally different tumbler.

## The invariant that holds

[INV-WIDTH-VALUE-EQUIVALENCE] guarantees:
> `value(crum.width.dsas[V]) == value(crum.width.dsas[I])` but `crum.width.dsas[V] != crum.width.dsas[I]` as tumbler representations.

So the numeric width (character count) is preserved through the I→V round-trip, but the tumbler exponent differs. The returned specset width `0.11` and the stored I-width `0.0.0.0.0.0.0.0.11` are the same value, not the same tumbler.

## Implication

Any spec for FOLLOWLINK must state that the returned spec-set is value-equivalent to the stored endset I-spans (same numeric origin offset and width), not representation-identical. The postcondition from [ST-FOLLOW-LINK] — `follow_link(L, SOURCE) == L.source_specset` — holds at the **logical value** level, not at the tumbler byte level.

---

## Code Exploration

Now I have all the pieces needed to trace the complete execution chain. Let me compile the answer.

---

## Answer

**Short answer:** For I-span endsets, the returned spec-set is a representation-exact copy of the stored I-address spans — the `exp` field is preserved exactly. For V-spec endsets, the returned V-width comes from `tumblersub` over V-coordinates and is in a different address space entirely.

---

### Execution chain for `followlink` / `dofollowlink`

`fns.c:114` → `do1.c:223`:

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
    return (
       link2sporglset(taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset(taskptr, &((typesporgl*)sporglset)->sporgladdress,
                             sporglset, specsetptr, NOBERTREQUIRED));
}
```

---

### Step 1: `link2sporglset` — sporgl.c:67

```c
tumblerincrement(&zero, 0, whichend, &vspan.stream);
tumblerincrement(&zero, 0, 1, &vspan.width);
if (context = retrieverestricted((typecuc*)orgl, &vspan, V, NULL, I, NULL)) {
    for (c = context; c; c = c->nextcontext) {
        contextintosporgl((type2dcontext*)c, NULL, sporglptr, I);
        ...
    }
}
```

It queries the link's POOM enfilade restricted to the endset's V-address (e.g., V=1 for FROM). For each matching crum, it calls `contextintosporgl` with `index=I`.

---

### Step 2: `contextintosporgl` — sporgl.c:205-220

```c
int contextintosporgl(type2dcontext *context, tumbler *linkid, typesporgl *sporglptr, INT index)
{
    sporglptr->itemid = SPORGLID;
    movetumbler(&context->context2dinfo.homedoc, &sporglptr->sporgladdress);
    movetumbler(&context->totaloffset.dsas[index], &sporglptr->sporglorigin);
    movetumbler(&context->contextwid.dsas[index], &sporglptr->sporglwidth);  // <-- key
}
```

`sporglptr->sporglwidth` = `context->contextwid.dsas[I]`.

---

### Step 3: `makecontextfromcbc` — context.c:151-173

```c
movewisp(&crumptr->cwid, &context->contextwid);
...
if (crumptr->cenftype != GRAN)
    dspadd(&context->totaloffset, &crumptr->cdsp, &context->totaloffset, (INT)crumptr->cenftype);
```

`movewisp` is a raw `movmem` (bit-copy). So `context->contextwid.dsas[I]` = `crumptr->cwid.dsas[I]` exactly. **The `dspadd` only touches `totaloffset` (the origin/stream), never `contextwid` (the width).** The I-width passes through as a bit-copy.

---

### Step 4: I-width at insert time — `insertpm` orglinks.c:75-131

```c
unpacksporgl(sporglset, &lstream, &lwidth, &linfo);
movetumbler(&lwidth, &crumwidth.dsas[I]);   // stored I-width = exact copy
...
insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
```

For I-span inputs (where `linfo.homedoc = 0`), `unpacksporgl` (sporgl.c:181-183):
```c
movetumbler(&((typeispan*)sporglptr)->stream, streamptr);
movetumbler(&((typeispan*)sporglptr)->width, widthptr);
tumblerclear(&infoptr->homedoc);   // homedoc = 0
```

The stored `crumwidth.dsas[I]` is a direct `movetumbler` copy of the original I-span width. No arithmetic.

---

### Step 5: `linksporglset2specset` — sporgl.c:97-122

```c
if (iszerotumbler(&((typesporgl*)sporglset)->sporgladdress)) {
    // I-span path: homedoc was 0 at insert, so sporgladdress is 0 here
    ((typeitemheader*)specset)->itemid = ISPANID;
    movetumbler(&sporglptr->sporglorigin, &((typeispan*)specset)->stream);
    movetumbler(&sporglptr->sporglwidth,  &((typeispan*)specset)->width);  // <-- pure copy
} else {
    linksporglset2vspec(...);   // V-spec path: I→V conversion
}
```

For I-span endsets, the width flows: original I-span → `crumptr->cwid.dsas[I]` → `context->contextwid.dsas[I]` → `sporglptr->sporglwidth` → returned `width`. **Every step is `movetumbler` / `movewisp` — raw bit copies. No arithmetic, no `tumblerjustify`, no `strongsub`.**

---

### Step 5b: V-spec path — `context2span` context.c:176-212

For V-spec endsets, `sporglset2vspanset` → `ispan2vspanset` → `permute` → `context2span`:

```c
movetumbler(&grasp.dsas[idx2], &foundspanptr->stream);
tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width);
```

The V-width is `tumblersub(reach[V], grasp[V])`. This calls `strongsub` (tumble.c:534):

```c
answer.exp = aptr->exp;
for (i = 0; aptr->mantissa[i] == bptr->mantissa[i]; ++i) {
    --answer.exp;    // <-- exp changes based on shared leading digits
    ...
}
answer.mantissa[0] = aptr->mantissa[i] - bptr->mantissa[i];
```

For canonical inputs, `strongsub` produces a canonical result, and `tumblersub` always calls `tumblerjustify(cptr)` at exit (tumble.c:430). The resulting V-width `exp` is determined entirely by the V-coordinates of the POOM crum — it is not derived from the stored I-width at all.

---

### The `tumblercheckptr` invariant — tumble.c:169-227

The check enforces: for any non-zero tumbler, `mantissa[0] != 0`. This means all stored widths are already in canonical (justified) form. `tumblerjustify` is a no-op for canonical tumblers (it exits immediately at `mantissaptr[0] != 0`, tumble.c:296-298). So there is no "silent renormalization" possible.

---

## Conclusion

**For I-span endsets** (where the link was created with an I-span spec, so `homedoc = 0`):

The returned spec-set's I-width is a **value-exact, representation-exact copy** of the I-address spans stored in the link orgl. The `exp` field is preserved without any possible change. The chain is:

> `crumptr->cwid.dsas[I]` →(movewisp)→ `context->contextwid.dsas[I]` →(movetumbler)→ `sporglptr->sporglwidth` →(movetumbler)→ returned `((typeispan*)specset)->width`

No arithmetic operation is applied to the width at any point in this chain.

**For V-spec endsets** (where the link was created with a V-spec, so `homedoc` is the doc ISA):

The returned width is a V-span width computed by `context2span`'s `tumblersub(reach[V], grasp[V])` [context.c:207]. Its `exp` is determined by `strongsub`'s shared-leading-digit stripping algorithm applied to V-coordinates. For canonical inputs (which the system enforces), this result is also canonical — but it is a fundamentally different value in a different coordinate space, not a copy of the stored I-width. A comparison between stored I-width and returned V-width is not meaningful.

**The returned spec-set cannot differ in tumbler exponent representation from the stored I-address spans** — but only because the I-span path is a pure copy chain, not because there's any normalization applied. The `exp` of the stored I-width is whatever was passed in at link-creation time, and it comes out unchanged.
