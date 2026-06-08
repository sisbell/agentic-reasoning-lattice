# Review of ASN-0111

I read the note as a self-contained specification of a pure read operation on the link store, checked each claim against the foundation invariants it cites, verified the worked example's arithmetic, and stress-tested the boundary cases (undefined address, empty connective slot, ghost type, orphaned link, link→link nesting, arity > 3).

## Verification performed

- **Address arithmetic in the worked example.** `a = [1.0.1.0.1.0.2.1]` has zeros at positions 2,4,6 (`zeros = 3`), `E(a) = [2,1]` so `subspace_I = s_L`, `#E = 2` — consistent with the first emission `[d.0.s_L.1]` of `d₁`'s link sub-allocator. `s ⊕ δ(2,8) = [1.0.1.0.1.0.1.3]`, and by T1 case (ii) the half-open interval correctly contains the subtrees of `…1.1` and `…1.2` (infinite), not the two points — the note states this correctly. `inc(a,0) = [1.0.1.0.1.0.2.2]` is right for T4-valid `a` (`sig = #a`).
- **Orphan dispatch (RL8).** The discoverability check is correctly run over *all three* slots per LP12. I confirmed `coverage(F)` (content subspace, `E₁ = 1`) contains no link addresses (any T4-valid extension keeps `zeros = 3` and `E₁ = 1`), and `coverage(Θ)` meets neither store via S3★ — so `discoverable_from` is false for every `d`. The argument is sound.
- **Single-step vs. multi-step persistence.** RL7 correctly distinguishes L12 (single-step) from the `→*` closure it needs, and discharges the closure via LP13 (ASN-0098) for both definedness and value preservation. The composite wp in RL0 is honestly labelled the substantive one and grounded in the same lift.
- **Cross-ASN discipline.** Every numbered reference (ASN-0034/0043/0047/0093/0098) is to a foundation ASN. No non-foundation ASN is cited in the body; out-of-scope neighbours are named descriptively, not as dependencies. Nelson/udanax-green are primary-source citations, not ASN cross-refs.
- **Anticipated-finding checks.** The wp-triviality concern is met head-on (pure stateless read), the ghost-type asymmetry is *not* overclaimed (RL5 explicitly disclaims the false from/to-vs-type content asymmetry via L4/L9), and the empty-connective-vs-unwitnessed distinction is correctly deferred to an Open Question rather than asserted.

## Assessment

The note defines state-read behaviour (`readlink ≡ Σ.L(a)`), its definedness domain, completeness, role/arity preservation, determinacy under evolution, and the recorded-vs-resolved distinction — all stated abstractly enough that an alternative implementation must satisfy them. It carries a concrete worked example exercising the load-bearing postconditions (RL1, RL2 including an N=4 instance, RL5, RL-ARITY, RL6, RL8), a non-trivial wp (the composite read-after-transition), and genuinely derived consequences (ownership disclosure, type-without-dereference, "unwitnessed" vs "gone"). The standing reachability precondition is correctly invoked to ground the structural guarantees that depend on theorems-about-reachable-states.

I found no missing boundary case, no proof-by-checkmark, no hand-wave, and no unsupported multi-step claim. The slot-role language for N > 3 reaches slightly past what the arity-3 StandardTriple convention establishes, but the note frames roles as interpretation (consistent with L7) and READLINK's actual guarantee — faithful positional return of all N slots — is fully supported; this does not rise to a defect.

## REVISE

(none)

## OUT_OF_SCOPE

The four Open Questions (continued-validity guarantees from a read alone, cross-time completeness invariants, creation-time vs. read-time coverage denotation, empty-vs-unwitnessed distinguishability, link-identity distinguishability of equal-structure links) are correctly posed as future territory rather than gaps in this note.

VERDICT: CONVERGED
