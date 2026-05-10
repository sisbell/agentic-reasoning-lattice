# Cone Review — ASN-0034/TA-assoc (cycle 8)

*2026-04-17 23:54*

### TA-assoc *Action point of `s`* sub-case `k_b = k_c` elides the ≥/> composition mechanism that TumblerAdd details explicitly

**Foundation**: NAT-order (NatStrictTotalOrder) — supplies the defining clause `m ≤ n ⟺ m < n ∨ m = n` and transitivity of `<` that together discharge the composition of a non-strict `≥` with a strict `>` into a strict `>`; TumblerAdd (sister property, this ASN) — precedent that itemises this composition explicitly at its structurally identical `aₖ + wₖ > aₖ` site.

**ASN**: TA-assoc (AdditionAssociative), *Action point of `s`*, sub-case `k_b = k_c`:
> "NAT-addcompat's left order-compatibility ... lifts to the non-strict `b_{k_b} + c_{k_b} ≥ b_{k_b} + 1`; NAT-addcompat's strict successor inequality (`n < n + 1`, instantiated at `n = b_{k_b}`) supplies the strict `b_{k_b} + 1 > b_{k_b}`; **NAT-order's transitivity composes the non-strict `b_{k_b} + c_{k_b} ≥ b_{k_b} + 1` with the strict `b_{k_b} + 1 > b_{k_b}` into the strict `b_{k_b} + c_{k_b} > b_{k_b}`**."

**Issue**: The step "NAT-order's transitivity composes `≥` with `>` into `>`" is not pure transitivity of `<`. At TumblerAdd's structurally identical site (`aₖ + wₖ ≥ aₖ + 1` composed with `aₖ + 1 > aₖ` into `aₖ + wₖ > aₖ`), the proof spells out the mechanism: NAT-order's defining clause `m ≤ n ⟺ m < n ∨ m = n` unfolds `≥` into `> ∨ =`, the first disjunct chains through NAT-order's transitivity of `<`, and the second disjunct substitutes the equality. TA-assoc's NAT-order Depends entry itemises (i) the identical step inside TumblerAdd's strict-advancement chain, (ii) trichotomy for sub-case splits, (iii) `<`-to-`≤` unfolding and `≤`-transitivity, and (iv) the `≥ 1 → > 0` lift and transitivity of `<` composing `b_{k_b} > 0` with `b_{k_b} + c_{k_b} > b_{k_b}` — but the intermediate `≥`/`>`-to-`>` composition that *produces* `b_{k_b} + c_{k_b} > b_{k_b}` is not itself itemised as a defining-clause + disjunct step. The body elides it to one clause ("NAT-order's transitivity composes"), and the Depends does not re-spell it as category (i) does for TumblerAdd's analogue. Under the per-step citation discipline TumblerAdd enforces ("NAT-addcompat's order-compatibility clauses deliver *only* non-strict conclusions, so this `≥`/`>` composition to strict is discharged from NAT-order"), the mechanism for this composition should be explicit at every occurrence, not abbreviated at one site and expanded at another.

**What needs resolving**: Either spell out the `b_{k_b} + c_{k_b} ≥ b_{k_b} + 1` / `b_{k_b} + 1 > b_{k_b}` / `b_{k_b} + c_{k_b} > b_{k_b}` composition via NAT-order's defining clause at `m = b_{k_b} + 1, n = b_{k_b} + c_{k_b}` with explicit disjunct handling (matching TumblerAdd's strict-advancement chain), or add a category to TA-assoc's NAT-order Depends that owns the `≥`/`>`-to-`>` composition specifically, so readers see one canonical treatment for a step the ASN otherwise treats uniformly across structurally identical sites.

## Result

Cone not converged after 8 cycles.

*Elapsed: 4927s*
