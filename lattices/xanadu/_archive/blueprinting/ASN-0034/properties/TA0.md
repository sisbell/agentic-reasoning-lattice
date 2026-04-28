## Tumbler arithmetic

We now turn to the arithmetic operations. The system requires operations that advance a position by a displacement (for computing span endpoints and shifting positions) and that recover the displacement between two positions (for computing span widths). These operations — tumbler addition and subtraction — are not arithmetic on numbers but position-advance operations in a hierarchical address space.

A displacement `w` is a tumbler whose leading zeros say "stay at these hierarchical levels" and whose first nonzero component says "advance here." Components after the advance point describe the structure of the landing position within the target region.

### Addition for position advancement

Let `⊕` denote tumbler addition: given a start position `a` and a displacement `w`, compute the advanced position.

We require a notion of where a displacement "acts." For a positive displacement `w = [w₁, w₂, ..., wₙ]`, define the *action point* as `k = min({i : 1 ≤ i ≤ n ∧ wᵢ ≠ 0})` — the position of the first nonzero component. The leading zeros say "stay at these hierarchical levels"; the first nonzero component says "advance here."

**TA0 (WellDefinedAddition).** For tumblers `a, w ∈ T` where `w > 0` and the action point `k` of `w` satisfies `k ≤ #a`, the result `a ⊕ w` is a well-defined tumbler in `T`.

The precondition `k ≤ #a` is essential: the constructive definition copies components `a₁, ..., aₖ₋₁` from the start position and adds `wₖ` to `aₖ`, so position `k` must exist within `a`. A displacement whose action point exceeds `#a` — one with more leading zeros than `a` has components — would attempt to "stay at" hierarchical levels that the start position does not have, and the operation is undefined.

*Proof.* We show that under the stated preconditions, the constructive rule for `⊕` produces a member of `T` with length `#w`.

Let `a = [a₁, ..., aₘ]` and `w = [w₁, ..., wₙ]`. The action point `k = min({i : 1 ≤ i ≤ n ∧ wᵢ ≠ 0})` — the position of the first nonzero component of `w` — exists because `w > 0`. The precondition requires `k ≤ m`.

The constructive definition (TumblerAdd) builds `r = a ⊕ w = [r₁, ..., rₙ]` by three rules: `rᵢ = aᵢ` for `1 ≤ i < k` (copy from start), `rₖ = aₖ + wₖ` (single-component advance), and `rᵢ = wᵢ` for `k < i ≤ n` (copy from displacement). We must establish two things: that `r ∈ T`, and that `#r = n = #w`.

**Length.** The result has `(k − 1)` prefix components, one action-point component, and `(n − k)` tail components, for a total of `(k − 1) + 1 + (n − k) = n`. Since `w ∈ T` requires `n ≥ 1`, the result has at least one component. So `#r = n = #w`.

**Components.** We verify `rᵢ ∈ ℕ` for each of the three regions.

*(i) Prefix, `1 ≤ i < k`.* Each `rᵢ = aᵢ`. The precondition `k ≤ m` ensures position `i < k ≤ m` exists within `a`, and since `a ∈ T`, each `aᵢ ∈ ℕ`. So `rᵢ ∈ ℕ`.

*(ii) Action point, `i = k`.* `rₖ = aₖ + wₖ`. We have `aₖ ∈ ℕ` (since `k ≤ m` and `a ∈ T`) and `wₖ ∈ ℕ` (since `k ≤ n` and `w ∈ T`). The natural numbers are closed under addition, so `aₖ + wₖ ∈ ℕ`.

*(iii) Tail, `k < i ≤ n`.* Each `rᵢ = wᵢ`. Since `w ∈ T`, each `wᵢ ∈ ℕ`. So `rᵢ ∈ ℕ`.

The result `r` is a finite sequence of natural numbers with length `n ≥ 1` — a member of `T`, with `#r = #w`. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, w ∈ T, w > 0, actionPoint(w) ≤ #a
- *Postconditions:* a ⊕ w ∈ T, #(a ⊕ w) = #w
