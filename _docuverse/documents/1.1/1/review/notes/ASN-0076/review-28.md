# Review of ASN-0076

I read the ASN as a composite-operation specification: EDITLINK is defined as two K.λ steps, and E0–E10 establish what the composite does and (crucially) does not do. I checked each proof against the foundation claims, traced the worked example by hand, and probed boundary cases.

## REVISE

(none)

The proofs are complete and the hard depth standards are met:

- **Every claim has a worked proof, not a checkmark.** E0's K.λ precondition discharge is done per-step and per-clause; the `#E(ℓ_new) ≥ 2` depth bound is proved by an explicit induction (base: SubAllocatorBundle first emission; step: TA5(c) length preservation + TA5(b) modification-confinement + TA5-SigValid terminal-position + T0 successor closure ⟹ zeros and field boundaries preserved). No "by similar reasoning" shortcuts.
- **Boundary cases are covered.** First-emission vs. subsequent-emission of `A_L(d_new)` are split and each discharged (freshness at the *firing* state Σ / Σ₁, not at the earlier entity-allocation event). Empty from/to endsets are admitted (only `e'_3 ≠ ∅` required by L3). `τ_sup` well-formedness reduces to `#τ_sup ≥ 1` saturating T12(b) at equality via OrdinalDisplacement.
- **Derived consequences are explicit.** E5–E10 are derived from E1–E4 with named premises and full chains; E5's induction handles the base case and the reachability concatenation correctly; the `covers`/`discoverable_from` reconciliation in E7 (orphaning via LP17, resurrection via LP18) correctly distinguishes the structural witness from arrangement-conditional discoverability rather than overclaiming.
- **The worked example is concrete and correct.** Traced `ℓ_old = [3,0,5,0,7,0,2,1]`, `ℓ_new = [4,0,2,0,3,0,2,1]`, `ℓ_sup = inc(ℓ_new,0) = [4,0,2,0,3,0,2,2]`; zeros, subspace, origin, `#E`, and the δ(1,8) displacements all check out, and E0–E10 are each re-verified against this state.
- **Citations are clean.** Every external reference is to a foundation ASN (0034/0036/0043/0047/0098); ASN-0093 appears only inside quoted foundation claim text, never as a direct ASN-0076 citation. The `covers` predicate is genuinely new (an inverse store-lookup), not a reinvention of ASN-0098's `project`, and the ASN says so.

I also confirmed the previously-declined E1/E8-vs-LP2 territory is settled: E1 now rests on LP13 (multi-step persistence) and E8 reduces to E1; I did not re-raise it.

## OUT_OF_SCOPE

### Topic 1: Supersession-type convention (pinning `τ_sup`)
**Why out of scope**: The link model cannot *identify* `ℓ_sup` as a supersession without an external designation of the type address; the ASN correctly treats `τ_sup` as caller-supplied (grounded in L4/L9) and defers the convention to a future type-endset ASN. The structural-witness framing of E4/E7 is exactly the right boundary.

### Topic 2: Acyclicity / termination of supersession chains
**Why out of scope**: Whether the supersession relation may contain cycles, and how a reader computes "current" successors, is a property of a future link-search/lineage ASN, not a guarantee EDITLINK must establish. The illustrative reader-procedure appendix is explicitly marked non-normative.

META: not applicable — the ASN defines an operation on link state as a composite of existing primitives and proves the resulting invariants, squarely within specification territory.

VERDICT: CONVERGED
