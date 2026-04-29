# Cone Review — ASN-0034/TA3-strict (cycle 1)

*2026-04-18 16:48*

### min/max primitives reintroduced in TA3-strict Preliminaries contradict T1 and TumblerSub as defined

**Foundation**: N/A — internal consistency. The relevant anchors are T1's Definition and Formal Contract, which fix case (i) as `k ≤ #a ∧ k ≤ #b` (originally stated `k ≤ m ∧ k ≤ n`), and TumblerSub's Definition, which dispatches `L` by NAT-order's trichotomy on `(#a, #w)` with explicit sub-cases (α), (β), (γ).

**ASN**: TA3-strict, *Preliminaries* paragraph:

> "T1 defines `a < b` by: there exists a least `k ≥ 1` with `aᵢ = bᵢ` for all `i < k`, and either (i) `k ≤ min(#a, #b)` with `aₖ < bₖ`, or (ii) `k = #a + 1 ≤ #b` …"
>
> "TumblerSub defines `x ⊖ w` (for `x ≥ w`) by zero-padding both operands to length `max(#x, #w)` and scanning … If no disagreement exists … the result is the zero tumbler of length `max(#x, #w)`. … `#r = max(#x, #w)`."

TA3-strict Case A also repeats: "`a ⊖ w` is the zero tumbler of length `max(#a, #w)`".

**Issue**: T1's Definition explicitly uses the conjunction `k ≤ m ∧ k ≤ n`, and TumblerSub, TA2, and ZPD all take substantial pains to name the longer length `L` via NAT-order's trichotomy dispatch on `(#a, #w)` precisely so that no primitive binary-maximum (or minimum) operator on ℕ is invoked — the convention is stated verbatim in TumblerSub's Depends ("every operator in the Definition must be discharged by a Depends entry") and repeated in ZPD, TA2, and TumblerSub's NAT-order entries. TA3-strict's Preliminaries reintroduce `min(#a, #b)` and `max(#x, #w)` as if they were primitives, contradicting the upstream definitions TA3-strict is paraphrasing. TA3-strict's Depends does not list these operators nor cite NAT-order for a trichotomy dispatch that would license them, so the operators are unsourced here while being explicitly eliminated elsewhere — the same symbols carry two incompatible formulations in one document.

**What needs resolving**: Either (a) rewrite TA3-strict's Preliminaries and Case A recap to match the trichotomy-dispatched forms used in T1, TumblerSub, TA2, and ZPD (and extend TA3-strict's Depends with the corresponding NAT-order trichotomy site(s) on `(#a, #b)` and `(#a, #w)`/`(#b, #w)`), or (b) state once, centrally, that `min` and `max` are admissible abbreviations for the trichotomy dispatch and that the two formulations are interchangeable — so downstream readers don't encounter T1 claiming `k ≤ m ∧ k ≤ n` in one section and TA3-strict claiming `k ≤ min(#a, #b)` in the next.
