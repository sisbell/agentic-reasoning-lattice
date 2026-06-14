# Channel Assignment — ASN-0134 review-2

**Date:** 2026-06-13 18:14

## Issue 1: K.σ (document registration) is in the step vocabulary but absent from the conflict analysis, the confluence result, and the contract
Reason: Derivable internally. K.σ's semantics come from the note's own chosen stack (ASN-0093: caller-supplied `d`, precondition `d ∉ dom(M)`, document-allocation deferred to the deliberately-excluded ASN-0047 entity layer), and its conflict structure is a direct instance of the H1/H2 template already in the note — same-`d` registrations collide like H2, distinct-`d` commute like H1, and the register-before-allocate dependency is just the existing "homes registered at Σ" precondition. The choice between bringing K.σ in (option a) or scoping its freshness out as the excluded layer's assumed precondition (option b) follows from the note's own ASN-0047-exclusion framing; no new design intent or implementation evidence is required.

## Issue 2: G1(ii)'s confluence is proven for a fixed step-schedule, but §4 applies it to runtime *operation* interleavings — where idem=⊤ dedup makes the committed survivor order-dependent
Reason: Internal precision fix. The carve-out follows from facts already present — idempotent hit = zero steps (A1), the global type-`K` audit slice `A_K` (so dedup is global, not per-home), and ASN-0128 I4 first-to-commit (the same I-series the note already cites in M1(b)) — so the author can restrict G1(ii) to the raw step level and append the operation-level non-confluence carve-out using only the note's existing definitions and cited results.

## Issue 3: A6 asserts the inductive step without a base case — Σ₀ is never anchored to a reachable/initial state
Reason: Purely internal formal patch. `Σ_init`'s canonicity is a foundation theorem of the note's own stack (constructed by R-VAL, which W6 already references), and G-PO already uses "reachable start state," so anchoring `Σ₀ = Σ_init` (or `→_sh*`-reachable) at 𝔼's introduction supplies the missing base case with no external input.
