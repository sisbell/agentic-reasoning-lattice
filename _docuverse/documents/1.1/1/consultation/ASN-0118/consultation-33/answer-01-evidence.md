## Question 1 [evidence]

> In udanax-green's spec-set processing, at which stage does the integer-offset clipping arithmetic that discards sub-depth structure occur — admissibility validation (`acceptablevsa`/`specset2ispanset`), the tumbler-order span classification, or content retrieval after classification — so that we can state which stages match the relaxed admissibility and which diverge?

## KB Synthesis

The clipping arithmetic that discards sub-depth structure occurs exclusively at the **arithmetic stage** — in `strongsub`/`tumblersub` during span displacement operations. The earlier stages (admissibility validation and tumbler-order classification) both match the relaxed admissibility posture and perform no clipping.

---

## Stage 1: Admissibility validation — matches relaxed admissibility

`acceptablevsa()` is a stub that unconditionally returns `TRUE` [PRE-SPECSET], [PRE-INSERT] (Finding 0010, 0011). It performs zero sub-depth structural checking. `specset2ispanset()` validates only document existence, not element-level tumbler fields [PRE-SPECSET] (Finding 0001). The result is that any tumbler — whether a properly-formed element address like `1.1.0.1.0.1.0.2.1` or a bare document address like `1.1.0.1.0.2` — passes without clipping or rejection.

This is the "relaxed admissibility" the question names. The stage simply does not enforce sub-depth conventions.

---

## Stage 2: Tumbler-order span classification — also matches relaxed admissibility

`intervalcmp` and `whereoncrum` operate on the full tumbler total order [SS-INTERVAL-CMP], [SS-WHEREONCRUM]. `tumblercmp` compares sign, then exponent, then mantissa digits left-to-right [INV-TUMBLER-TOTAL-ORDER]. No precision is discarded; the full 16-digit mantissa representation is used for the five-way spatial classification (`TOMYLEFT`/`ONMYLEFTBORDER`/`THRUME`/`ONMYRIGHTBORDER`/`TOMYRIGHT`). Every tumbler — including those with sub-depth digit structure — is correctly classifiable. Classification faithfully preserves whatever structure the address carries.

---

## Stage 3: Arithmetic / content retrieval — diverges; clipping occurs here

Two distinct mechanisms discard sub-depth structure at this stage:

### 3a. `strongsub` exponent guard — the primary clipping mechanism

[SS-TUMBLER] (Finding 0055) establishes the rule: when the subtrahend's exponent is strictly less than the minuend's exponent, `strongsub` returns the minuend unchanged. Code at `tumble.c:534-547`:

```
if (bptr->exp < aptr->exp) { movetumbler(aptr, cptr); return(0); }
```

For DELETE, this means: an entry at V-displacement `2.1` (exp=0) is immune to a deletion width of `0.3` (exp=-1), because the width has a smaller exponent. The displacement is returned unchanged — the sub-exponent offset arithmetic is entirely discarded [INT-DELETE-SUBSPACE-ASYMMETRY], [FC-SUBSPACE] (Finding 0055). This is the mechanism by which link-subspace crums survive text-subspace deletions unshifted.

Critically, the classification stage (stage 2) may have *decided* that the entry should be shifted (Case 2 / case 1 of `deletecutsectionnd`), but the arithmetic stage overrides that with a no-op. Stage 2 and stage 3 diverge at this point.

### 3b. `tumblerintdiff` integer extraction in `insertpm` — V-width precision clipping

[SS-INSERT-VWIDTH-ENCODING] (Finding 0076) documents a second clipping path. During INSERT, `insertpm` computes the V-width of a new POOM crum by extracting the integer value from the I-width via `tumblerintdiff`, then re-encoding it at V-address precision via `tumblerincrement`. Any sub-integer fractional component in the I-width tumbler is discarded — only the integer part survives into the V-width representation. The resulting V-width tumbler is structurally different from the I-width tumbler (different exponent, shorter) even though `tumblerintdiff` on both yields the same integer [INV-WIDTH-VALUE-EQUIVALENCE].

---

## Summary table

| Stage | Operation | Sub-depth handling | Matches relaxed admissibility? |
|-------|-----------|-------------------|-------------------------------|
| 1. Admissibility | `acceptablevsa` (stub), `specset2ispanset` (doc-only check) | None — all inputs admitted | **Yes** |
| 2. Classification | `intervalcmp`, `whereoncrum` (full tumbler order) | None — full precision used | **Yes** |
| 3a. Arithmetic | `strongsub` exponent guard | **Clips**: returns minuend when `b.exp < a.exp` | **No — diverges** |
| 3b. Arithmetic | `tumblerintdiff` + `tumblerincrement` in `insertpm` | **Clips**: strips sub-integer precision from I-width → V-width | **No — diverges** |

The architectural consequence is that the system makes a structural bet in the design of `strongsub`: for cross-subspace safety to hold, the widths used in DELETE arithmetic must always have a smaller exponent than the displacements of cross-subspace crums. This is not validated anywhere in stages 1 or 2 — it is an emergent arithmetic consequence that happens to hold for the specific exponent relationships between text-subspace widths (exp=-1) and link-subspace displacements (exp=0) [INT-DELETE-SUBSPACE-ASYMMETRY], [FC-SUBSPACE] (Finding 0067).

---

## Code Exploration

Now I have verified all the critical line numbers. Let me compose the full answer.

---

## Integer-Offset Clipping in Spec-Set Processing: Stage-by-Stage Analysis

### Stage 1 — Admissibility Validation (`acceptablevsa`)

The answer here is unambiguous and decisive. `acceptablevsa` is a stub:

```c
// do2.c:110-113
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

**`acceptablevsa` does no arithmetic at all.** It unconditionally returns TRUE. No clipping occurs here. No depth check, no sub-depth inspection, nothing. Whatever "admissibility" was originally intended, this stage is entirely absent from the implementation. Every spec-set passes.

`specset2ispanset` [do2.c:14-46] is equally passive at this level — it iterates over the spec list and dispatches VSPECID specs to `vspanset2ispanset`. It does no clipping or depth-arithmetic itself; it is purely a dispatch loop.

**Verdict: Stage 1 does not clip. It fully matches any relaxed admissibility definition — trivially, because it accepts everything.**

---

### Stage 2 — Span Classification via V↔I Permutation (`vspanset2ispanset` / `permute` / `span2spanset`)

This stage is where the V-dimension to I-dimension conversion occurs, and it is where the integer-offset clipping arithmetic is most concentrated and most semantically significant.

The call chain is:

```
specset2ispanset [do2.c:36]
  → vspanset2ispanset [orglinks.c:397-401]
      → permute(..., V, ..., I) [orglinks.c:404-422]
          → span2spanset [orglinks.c:425-453]
              → retrieverestricted [orglinks.c:435]
              → context2span [orglinks.c:443]
```

#### The clipping function: `tumblerintdiff` [tumble.c:591-597]

```c
INT tumblerintdiff(tumbler *aptr, tumbler *bptr)
{
  tumbler c;
    tumblersub (aptr, bptr, &c);
    return (c.mantissa[0]);   // ← ONLY the first mantissa component
}
```

`tumblersub` computes the full multi-component tumbler difference, but the return discards everything except `mantissa[0]`. Any difference that lives in `mantissa[1]` or deeper — i.e., any sub-depth fractional offset — is silently dropped.

#### Where this clipped integer is applied: `context2span` [context.c:176-212]

```c
// context.c:191-200
if (tumblercmp (&grasp.dsas[idx1], &lowerbound) == LESS) {
    tumblerincrement (&grasp.dsas[idx2], 0,
        (INT) tumblerintdiff(&lowerbound, &grasp.dsas[idx1]),
        &grasp.dsas[idx2]);
}
if (tumblercmp (&reach.dsas[idx1], &upperbound) == GREATER) {
    tumblerincrement (&reach.dsas[idx2], 0,
        - tumblerintdiff (&reach.dsas[idx1], &upperbound),
        &reach.dsas[idx2]);
}
```

At context.c:194 and context.c:200, the clipped integers are fed into `tumblerincrement` with `rightshift=0`, meaning they are placed at `mantissa[idx]` of the target-dimension span boundary. The `tumblerincrement` call [tumble.c:621] adds the clipped value to `cptr->mantissa[idx + rightshift]` — a single-component integer offset, not a full tumbler displacement. Everything finer-grained than a depth-0 unit on the restriction dimension is discarded before the target dimension's span boundary is adjusted.

#### Explicit sub-depth zeroing in `retrievevspansetpm` [orglinks.c:173-221]

```c
// orglinks.c:197-203
movetumbler (&ccptr->cwid.dsas[V], &linkvspan.stream);
linkvspan.stream.mantissa[1] = 0;     // ← explicit zero of sub-depth
tumblerjustify(&linkvspan.stream);

movetumbler (&ccptr->cwid.dsas[V], &linkvspan.width);
linkvspan.width.mantissa[1] = 0;      // ← explicit zero of sub-depth
tumblerjustify(&linkvspan.width);
```

For multi-story (sub-depth) crums, `mantissa[1]` — the depth-1 sub-component — is zeroed explicitly before the V-span is returned. The comment at orglinks.c:194 says: *"in both cases we have to remove the first digit of the tumbler, the 1 and hack it around a bit."* This is not an accident or an overflow guard; it is intentional structural reduction.

The code that classifies crums as text vs. link also shows the same taxonomy:

```c
// orglinks.c:246-261
bool istextcrum(typecorecrum *crumptr) {
    if(crumptr->cdsp.dsas[V].mantissa[1] == 0          // no sub-depth
       && is1story(&crumptr->cwid.dsas[V])) {           // single-component width
        return TRUE;
    }
    return FALSE;
}

bool islinkcrum(typecorecrum *crumptr) {
    if(crumptr->cdsp.dsas[V].mantissa[0] == 1
       && crumptr->cdsp.dsas[V].mantissa[1] != 0) {    // displaced with sub-depth
        return TRUE;
    }
    return FALSE;
}
```

A crum is a *text crum* if and only if `mantissa[1] == 0` and `is1story()` [tumble.c:237-247] is true (all of mantissa[1..NPLACES-1] are zero). A *link crum* is one with `mantissa[0] == 1` and `mantissa[1] != 0`. Crums with sub-depth structure that do not fit either pattern — i.e., ones with non-canonical depth layout — are neither, and fall through silently.

**Verdict: Stage 2 is where essentially all of the integer-offset clipping arithmetic occurs.** The V→I permutation path through `context2span` / `tumblerintdiff` clips every span boundary to `mantissa[0]` precision. The V-span retrieval in `retrievevspansetpm` explicitly zeroes sub-depth components. This stage diverges from any relaxed admissibility definition that would honour sub-depth addresses as distinct locations.

---

### Stage 3 — Content Retrieval (`context2vtext`, `retrievecrums`)

Clipping occurs here too, but it is downstream of Stage 2 and of the same character.

```c
// context.c:294-305
if (tumblercmp (&crumistart, &ispanstart) == LESS) {
    i = tumblerintdiff (&ispanstart, &crumistart);  // ← clips to mantissa[0]
    vtlength -= i;
}
if (tumblercmp (&crumiend, &ispanend) == GREATER) {
    vtlength -= tumblerintdiff (&crumiend, &ispanend);  // ← clips to mantissa[0]
}
movmem (&...textstring[i], vstuffset->string, vtlength);  // context.c:308
```

The string offset `i` and the length reduction both derive from `tumblerintdiff`, which truncates to `c.mantissa[0]`. If `ispanstart` and `crumistart` differ only in sub-depth components (same `mantissa[0]`, differing `mantissa[1]`), `tumblerintdiff` returns zero and `i` stays at 0, so the start of the text slice is unaffected by the sub-depth displacement. The text byte extracted is the wrong one, but no error is reported.

`tumblertruncate` [tumble.c:625-639] — the depth-parameterised truncation function — zeros mantissa[bint..NPLACES-1]:

```c
for (; bint < NPLACES; ++bint)
    answer.mantissa[bint] = 0;   // tumble.c:636
```

This is called from `granf2.c:239` (`findisatoinsertnonmolecule`) during ISA allocation and from `do2.c:58` (`tumbler2spanset`) for width construction:

```c
// do2.c:58
tumblerincrement (&spanptr->width, tumblerlength(tumblerptr)-1 /*zzzzz*/, 1, &spanptr->width);
```

The `/*zzzzz*/` comment signals acknowledged uncertainty; the width is placed at `mantissa[tumblerlength-1]`, with all higher positions at zero from `tumblerclear`.

**Verdict: Stage 3 inherits clipped spans from Stage 2 and applies the same `tumblerintdiff` arithmetic to compute byte offsets. Sub-depth structure in the I-space coordinates, if it survived to this point, would be silently zeroed. In practice no sub-depth survives Stage 2, so Stage 3's clipping is redundant — it clips an already-clipped span.**

---

### Summary: Which Stages Clip and Which Match Relaxed Admissibility

| Stage | Function(s) | Clips sub-depth? | Matches relaxed admissibility? |
|---|---|---|---|
| Admissibility validation | `acceptablevsa` [do2.c:110-113] | No — stub, returns TRUE always | Yes — unconditionally |
| `specset2ispanset` dispatch | do2.c:14-46 | No — pure dispatch | Yes |
| V→I classification | `permute` → `context2span` [orglinks.c:404; context.c:176] | **Yes** — `tumblerintdiff` [tumble.c:596] returns only `mantissa[0]` | **No — diverges** |
| V-span sub-depth zeroing | `retrievevspansetpm` [orglinks.c:198, 202] | **Yes** — `mantissa[1] = 0` explicit | **No — diverges** |
| Content retrieval | `context2vtext` [context.c:298, 305] | **Yes** — same `tumblerintdiff` mechanism | **No — diverges** |

The integer-offset clipping is not a single point — it is a systematic property of the dimension-permutation path. The primitive that performs it is `tumblerintdiff` [tumble.c:591-597], specifically the `return (c.mantissa[0])` at line 596. Every call site that computes a span offset or a byte index by comparing two tumblers routes through this function and discards everything below depth 0. The stage at which this first matters semantically is `context2span` [context.c:194, 200] during the V→I permutation in Stage 2, because that is where sub-depth V-addresses are mapped to I-spans, and the mapping rounds to integer granularity before the I-span is ever used for retrieval.
