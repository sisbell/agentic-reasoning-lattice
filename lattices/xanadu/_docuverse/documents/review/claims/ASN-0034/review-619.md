# Cone Review — ASN-0034/TS2 (cycle 1)

*2026-04-26 10:06*

Reading the ASN end-to-end. Foundation statements are listed as none — internal-consistency review only.

### OrdinalShift's terminal composition cites only `<`-transitivity
**Class**: OBSERVE
**Foundation**: n/a (internal — NAT-order)
**ASN**: OrdinalShift derivation, final sentence of the component-lower-bound paragraph: "NAT-order composes `vₘ + n ≥ n` with precondition `n ≥ 1` into `vₘ + n ≥ 1` via its defining clause and transitivity of `<`."
**Issue**: Composing `n ≤ vₘ + n` with `1 ≤ n` to get `1 ≤ vₘ + n` is ≤-transitivity. Decomposing each `≤` via the defining clause yields four cases; only the `<`-with-`<` case is discharged by `<`-transitivity alone — the other three need substitution under `=`. The result is sound (NAT-order's Consequence section establishes ≤-transitivity directly), but the cited mechanism understates what is being invoked. The matching Depends entry for NAT-order also names only the defining clause and transitivity of `<`.
**What needs resolving**: n/a (sound as written).

### OrdinalShift glosses NAT-zero → `0 ≤ vₘ` conversion
**Class**: OBSERVE
**Foundation**: n/a (internal — NAT-zero, NAT-order)
**ASN**: OrdinalShift, "T0 places vₘ ∈ ℕ. NAT-zero gives `0 ≤ vₘ`."
**Issue**: NAT-zero supplies `0 < vₘ ∨ 0 = vₘ`. The `≤`-form is reached only after applying NAT-order's defining clause `m ≤ n ⟺ m < n ∨ m = n`. The downstream NAT-addcompat invocation is right-order-compatibility (`p ≤ n ⟹ p + m ≤ n + m`), which requires the ≤-form on input. The step is sound but skips the NAT-order folding.
**What needs resolving**: n/a (sound as written).

VERDICT: OBSERVE

## Result

Cone review converged.

*Elapsed: 969s*
