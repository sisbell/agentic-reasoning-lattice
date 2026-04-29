## Question 14 [gregory]

> What was the design rationale for sign-magnitude representation instead of two's complement — was it to make the total order (negative < zero < positive) straightforward in `tumblercmp`, or was there a deeper reason related to hierarchical addressing?

## KB Synthesis

The KB does not contain the design rationale — no finding records why sign-magnitude was chosen over two's complement. I can offer what the KB makes inferable, but cannot claim this reflects actual design intent.

**What the KB says about the representation:**

From [SS-TUMBLER] Finding 0031: tumblers store a sign bit, exponent, and 16-digit mantissa, with zero digits acting as hierarchical separators (e.g., `1.1.0.2.0.5` encodes a three-level hierarchy). From [SS-TUMBLER] Finding 0053: `tumblercmp` simply orders all negatives before zero before all positives, with absolute magnitude comparison within sign classes.

**What can be inferred:**

The hierarchical separator convention — zeros *within* the mantissa as field delimiters — is likely the deeper reason. In two's complement, the bit pattern for negative numbers would be opaque as a digit sequence; the `1.1.0.2.0.5` style addressing would lose its legibility. Sign-magnitude preserves the digit sequence intact with only a separate sign flag, so the hierarchical structure remains inspectable and the same comparison logic (`abscmp`: exponent first, then lexicographic mantissa) works uniformly across the magnitude.

The `tumblercmp` ordering being "straightforward" is a consequence of sign-magnitude, not a primary motivation — any representation can implement a total order. But sign-magnitude makes the order *obvious*: negative sign flips an otherwise identical comparison, with no wraparound arithmetic to reason about.

Supporting evidence: [SS-TUMBLER] Finding 0055 notes that `strongsub` uses an explicit exponent guard (`b.exp < a.exp → return a unchanged`), which operates directly on the tumbler's structural fields. This kind of direct exponent reasoning would be harder with two's complement encoding.

**Bottom line:** The KB supports inferring that hierarchical digit-sequence legibility drove the representation choice, with the clean total order as a secondary benefit. But this is inference — no KB entry states the rationale explicitly.

---

## Code Exploration

Now I have everything I need. Let me compile the full analysis.

---

## Sign-Magnitude in Tumbler Arithmetic: A Code-Grounded Analysis

The answer is that sign-magnitude was chosen primarily because of **hierarchical addressing semantics** — the digit values must be intrinsically non-negative — and secondarily because the subtraction identity it provides is cleaner. The simple total order in `tumblercmp` is a consequence, not the cause.

---

### 1. The Fundamental Constraint: `tdigit` Is Unsigned

`common.h:57`:
```c
typedef UINT tdigit;
```

And the full struct, `common.h:59-65`:
```c
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign  BIT ;  /* 1 if negative, otherwise 0 */
    short exp;
    tdigit mantissa[NPLACES];
} tumbler;
```

The mantissa digits are typed as unsigned integers. Sign is a completely *separate* field — a single bit isolated from the digits. This is the defining structural choice.

The validator enforces it explicitly. `tumble.c:202-209`:
```c
for (i = 0; i < NPLACES; ++i){
    if ((INT)(ptr->mantissa[i]) < 0){
        fprintf(stderr,"negative digit");
        wrong = TRUE;
    }
}
```

And negative zero is independently invalid — `tumble.c:180-184`:
```c
if (ptr->sign && ptr->mantissa[0] == 0){
    fprintf(stderr," negative zero ");
    wrong = TRUE;
}
```
Two's complement doesn't have negative zero; that check only makes sense for sign-magnitude.

---

### 2. The Deep Reason: Hierarchical Addresses Have No Negative Digits

A tumbler like `3.7.2` is not an integer — it's a *hierarchical path*. The digits name positions in a containment hierarchy (document → section → subsection). It is semantically meaningless for a digit to be negative. You cannot be at the "−3rd" subsection of something.

The `exp` field encodes depth in the hierarchy (it is validated to be non-positive, `tumble.c:174-178`):
```c
if (ptr->exp > 0){
    fprintf(stderr,"bad exp ");
    wrong = TRUE;
}
```

The `exp` says how many levels deep the implicit decimal point sits. All digits above that point are non-negative path components.

If two's complement were used, negative numbers would corrupt bit `31` of mantissa digits. The hierarchical semantic of "count at level i" would break. `absadd` (`tumble.c:444-485`) operates directly on unsigned digit arrays with no sign involvement — that would be impossible with two's complement encoding in the digits.

---

### 3. The Sign Bit Is Solely for Signed Displacement Arithmetic

Negative tumblers appear only as transient computational intermediates. They **cannot be serialized**. `tumbleari.c:77-78`:
```c
if(ptr->sign)
    gerror("negative tumbler in tumblerfixedtoptr\n");
```

The constant `TUMBLERMINUS = 129` (`common.h:56`) is defined as if for a wire encoding, but `tumblerfixedtoptr` refuses to produce it. Negative tumblers only live in memory, during arithmetic.

The canonical use of sign is in subtraction. `tumble.c:425-428`:
```c
movetumbler (bptr, &temp);
temp.sign = !temp.sign;
tumbleradd (aptr, &temp, cptr);
```

`tumblersub(a, b, c)` negates `b` by flipping its sign bit, then calls `tumbleradd`. This is the sign-magnitude identity `a − b = a + (−b)`. With two's complement you'd need one's complement inversion + increment, which corrupts the digit values and breaks the unsigned-digit invariant.

---

### 4. The Wire Format Depends on Non-Negative Digits

The `humber` encoding scheme (`tumbleari.c`) is a self-delimiting unsigned variable-length integer encoding. Each mantissa digit of a tumbler is encoded separately as a humber (`tumbleari.c:53-62`):
```c
for (i = 0; i < NPLACES && mantissadigitptr < humberEnd; i++) {
    if(mantissadigitptr[0] <=127){
        tptr->mantissa[i] = mantissadigitptr[0];
    }else{
        tptr->mantissa[i] = functionintof(mantissadigitptr);
    }
}
```

Humbers are unsigned: `humberput` (`tumbleari.c:137`) rejects negative values:
```c
if((int)i <0){
    gerror("humberput of negative number\n");
}
```

Two's complement would require a completely different serialization per digit. Sign-magnitude lets each digit be independently encoded as a non-negative humber.

---

### 5. `strongsub` and `weaksub` Are Hierarchical Operations, Not Integer Arithmetic

There are two subtraction operations distinct from `tumblersub` that only make sense with unsigned digits.

`strongsub` (`tumble.c:534-565`) strips a common hierarchical prefix, returning the suffix offset:
```c
for (i = 0; aptr->mantissa[i] == bptr->mantissa[i]; ++i) {
    --answer.exp;
    ...
}
answer.mantissa[0] = aptr->mantissa[i] - bptr->mantissa[i];
```

This finds where two addresses diverge in their hierarchy and returns "how far apart" they are at that level. It is not integer subtraction — it is prefix-stripping. Two's complement digits would break the digit-by-digit prefix comparison.

`weaksub` (`tumble.c:567-589`) subtracts the first digit of `b` from the corresponding position in `a` — a "partial suffix" operation:
```c
answer.mantissa[i] = aptr->mantissa[i] - bptr->mantissa[0];
```

Again, this makes sense only when digits are non-negative path components.

---

### 6. The `tumblercmp` Simplicity Is Real but Derivative

`tumblercmp` (`tumble.c:72-85`):
```c
INT tumblercmp(tumbler *aptr, tumbler *bptr)
{
    if (iszerotumbler(aptr)){
        if (iszerotumbler(bptr))
            return (EQUAL);
        else
            return (bptr->sign ? GREATER : LESS);
    }
    if (iszerotumbler(bptr))
        return (aptr->sign ? LESS : GREATER);
    if (aptr->sign == bptr->sign)
        return (aptr->sign ? abscmp(bptr,aptr) : abscmp(aptr,bptr));
    return (aptr->sign ? LESS : GREATER);
}
```

The logic is: same sign → compare absolute values (negatives in reversed order because larger magnitude = more negative); different signs → negative is always less. This is the total order negative < zero < positive, clean and readable.

But this simplicity is a *consequence* of the design, not the reason for it. The deeper reason is that `abscmp` (`tumble.c:87-111`) does unsigned lexicographic comparison of digit arrays:
```c
a = (INT *) aptr->mantissa;
b = (INT *) bptr->mantissa;
for (i = NPLACES; i--;) {
    if(!(cmp = *a++ - *b++)){
    } else if (cmp < 0) {
        return (LESS);
    } else {
        return (GREATER);
    }
}
```

This direct pointer arithmetic over the digit arrays works because digits are unsigned and the address ordering is lexicographic. With two's complement digits the subtraction `*a++ - *b++` would produce wrong results for large values (signed overflow). The comparison function works correctly *because* the digits are unsigned non-negative hierarchical components.

---

### Summary

The sign-magnitude choice is layered in three tiers, from deepest to shallowest:

1. **Deepest — hierarchical semantics**: Tumbler digits are non-negative path components naming levels in a containment hierarchy. They are typed `UINT` (`common.h:57`). This is a semantic constraint, not a numerical one. Two's complement would corrupt the digit semantics.

2. **Middle — wire format and `abscmp`**: The `humber` variable-length encoding is purely unsigned (`tumbleari.c:137`). `abscmp` does unsigned digit-array comparison (`tumble.c:99-108`). Both require that digit values be non-negative. Negative tumblers are therefore never serialized (`tumbleari.c:77-78`).

3. **Shallowest — the subtraction identity**: Sign-magnitude allows `tumblersub` to be implemented as `tumbleradd(a, flip_sign(b))` (`tumble.c:425-428`), a clean algebraic identity. Two's complement would require inversion + increment, touching the digit values themselves.

The total order in `tumblercmp` (negative < zero < positive) falls out naturally from all of this, but it would have been achievable with two's complement too. The real reason is that tumblers are hierarchical addresses, and hierarchical addresses are made of non-negative path components — so the sign of the *address* must live in a dedicated bit separate from those components.
