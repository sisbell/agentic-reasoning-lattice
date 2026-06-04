# Review of ASN-0077

I focused on proof rigor for the operation claims (O11/O11'/O11★★/O13/O14, the singleton edge case, and the two wp derivations) and applied the `review-mode.anti-bloat` checks. The mathematics is sound: the singleton-span squeeze argument, the K.μ~/K.μ⁻ negative witnesses, and the multi-step closures (O5★, O6★, O11★★) all discharge their foundation preconditions correctly, and the prior-cycle re-review items (O0 vs ASN-0040; O3/O10 vs ASN-0098) hold up — O5★/O6★ now invoke ASN-0098's Closure schema and Store Monotonicity★ appropriately. One repetition pattern remains.

## REVISE

### Issue 1: The depth-coincidence argument is restated three-plus times rather than extracted

**ASN-0077, O11 sub-case (a) / O11.1 conjunct (v) / O11' sub-case (b)**: The same sub-argument — "`#v` (and `subspace(v)`) is a state-independent structural projection, so pre-state positions carry forward with depth preserved, and S8-depth at Σ' forces a single common depth across the (superset) V_S(d)|_Σ', whence m' = m" — appears in:
- O11 sub-case (a) (`s_C`, K.μ⁺), spelled out in three steps;
- O11.1 conjunct (v), which *both* cites "the cross-state depth identification of O11's sub-case (a)" *and* re-states it inline, then does so a second time "with s_L in place of s_C" for the K.μ⁺_L case;
- O11' sub-case (b) steps (1)–(3), a `#v_ℓ = m` variant of the same projection-plus-S8-depth reasoning.

**Problem**: This is the "two paragraphs say the same thing in different words" / "content relocated rather than removed" pattern the anti-bloat classifier names. O11.1's double-citation (reference *and* full restatement of an argument that, in O11, only exists for `s_C` — there is no s_L depth sub-case in O11 to "apply with s_L in place of s_C") forces the precise reader to reconcile a cited sub-case against an inline re-derivation. The repetition compounds across the O11-series.

**Required**: Extract the depth-coincidence step as a single named lemma — roughly "for an arrangement-extension step on `d`, the common depth of any non-empty subspace S is preserved, because `subspace(·)` and `#·` are state-independent and S8-depth forces a single value over the superset" — and have O11, O11', O11.1, and the worked example cite it once. Remove the inline re-statements (and the mismatched "O11 sub-case (a) ... with s_L in place of s_C" pointer).

## OUT_OF_SCOPE

### Topic 1: Unified content+link origin operation, intermediate-chain surfacing, native-vs-transcluded distinction, historical-containment operation

**Why out of scope**: These are the four Open Questions the note itself raises; each defines a *new* operation or coupling (to `Σ.R`, or across subspaces) and belongs in a future ASN, not a revision of SHOWORIGIN's pointwise/lift specification.

VERDICT: REVISE
