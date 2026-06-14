# Review of ASN-0125

I reviewed this note as a derived-composite specification: an impossibility result (EL0–EL1), a necessity argument selecting the carrier (EL2–EL3), two operations with contracts (EL6–EL7), and a battery of derived consequences (EL8–EL16) closing each question posed in *The problem*. I checked the proofs, the boundary cases, the cross-layer transfers, and the worked example.

## REVISE

None. The substantive checks all hold:

- **EL0 wp = false** is sound: `J ≡ a ∈ dom(L) ∧ L(a) = ℓ₀` persists by LP13, `J ⟹ ¬R_mut` since `Σ.L` is a partial function and `w ≠ ℓ₀`, every finite program lands in a reachable state, so `R_mut` is establishable from nowhere.
- **EL2(c)/EL3 necessity** is exhaustive: the four in-place carriers are each closed (L12 twice; the `#E = 2` flat-chain fact plus the R0a antichain for address nesting; the C/L/E/R/M inventory for index markers), and the surviving entity carrier is forced to a typed link-to-link tuple. The "menu collapse" (separate-link ≡ typed-relation under L8/ASN-0086) is correct.
- **EL4 SingleTarget** correctly carries the antichain collapse `{t : x ≼ t} ∩ dom(Σ.L) = {x}` and is stated per-claim, not under a whole-state hypothesis — the right move, since it makes `old/new` total on `Ŝ^Σ` even at non-disciplined states.
- **EL6(iii)/(iv)** correctly conditions "active at birth" and full `nullified` preservation on edit-discipline (ASN-0086 wp Case 2 disciplined simplification), while keeping the weaker `nullified(Σ') ∩ dom(Σ.L) = nullified(Σ)` unconditional via the `coverage(K_sup) ≠ coverage(R)` slice argument.
- **EL7(vi)** discharges discipline preservation across both `K.λ` steps, including the non-obvious case split on whether `a'` lands in `S^{Σ₁}` (the `|ℓ'| = 3 ∧ coverage(ℓ'.e₃) = coverage(K_sup)` guard exactly matching ASN-0086's arity-3 slice restriction), with `DC`'s witnesses correctly pinned at the pre-state since `dom(L)` only grows.
- **EL9(2)** correctly identifies that `K.μ⁻` retains a *prefix* and so de-listing a middle link forces a drop-suffix-then-reseat construction; the `j = 1` and "last/only" edges are handled.
- **EL11(a)** is fully proved (no content address extends a link address — the subspace-component contradiction via L0/C1/SC-NEQ — plus R0a for the link side), and the "symmetrically for the from-side" is genuinely symmetric, not a hand-wave.
- **EL13** commutation is sound; "distinct fresh keys" is licensed by the preceding step (each emission is homed at its own `d`, and `d₁ ≠ d₂`).
- **EL14(c)/(e)** are the strongest results: the `current = ∅` standoff and the activity-agnostic membership (`z ∈ current(y)` without `active(z)`, since `succ_o` filters only on the *claim* address) are both constructed inside the disciplined layer and check out.
- **Reachability linchpin** ("K.λ-only composites are valid") correctly verifies J0/J1★/J1'★ vacuous, so EL6/EL7 outputs satisfy the ExtendedReachableStateInvariants.
- The **worked example** address arithmetic (`inc(·,0)` on the flat `H.0.s_L.k` / `P.0.s_L.k` chains, the demotion/revert/standoff/registry-churn trace) is internally consistent.

Self-containment holds — only foundation ASNs (0034, 0036, 0042, 0043, 0047, 0086, 0093, 0098) are cited, with no reinvention of foundation notation. The anti-bloat pass turned up no skippable meta-prose: the dense passages (EL14(d)/(e)) are statements of what `current` does and does not do, which are exempt; the implementation notes are grounding evidence the depth standard explicitly requires, not spec drift.

## OUT_OF_SCOPE

None. The note specifies only the editing composite and its supersession relation; its use of bare `K.λ` (foundation primitive) for original-link creation, and of `project`/`Observe_K` for characterizing claim discoverability, does not stray into MAKELINK, FINDLINKSFROMTOTHREE, FOLLOWLINK, or the other excluded operations.

VERDICT: CONVERGED
