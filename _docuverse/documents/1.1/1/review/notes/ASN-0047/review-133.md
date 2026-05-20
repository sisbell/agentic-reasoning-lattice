# Review of ASN-0047

After thorough review covering the state model, elementary transition definitions, the K.δ case-by-case freshness discharge chain (including FrontierEquivalence and the cross-document disjointness lemma), the K.μ⁻ admissible contraction shape derivation (both directions), the K.μ~ link-subspace fixity dependency chain (Steps A–E), all coupling constraints (J0, J1★, J1'★), the cross-layer invariants P6/P7/P7a/NodeLineage/GlobalLineage, the per-state vs composite-boundary partition of ExtendedReachableStateInvariants, the verification matrix (every cell I sampled checked out against the body prose), and all five worked examples (entity hierarchy, fork composite, content insertion/deletion/reordering, interior content replacement, link allocation with link-subspace fixity), I find no logical gaps, hand-waves disguised as proofs, or missing edge cases.

Several items I scrutinized that initially looked weak but verified on closer reading:

- **K.μ~ link-subspace fixity dependency chain.** Steps (A)–(E) cleanly disentangle the apparent CL-UNIQ ↔ link-fixity circularity: Steps 1–3 establish the *functional* identity `M'(d)|_{dom_L} = M(d)|_{dom_L}` without consuming CL-UNIQ; Step 4 uses pre-state CL-UNIQ (inductive hypothesis) to derive *pointwise* fixity. Post-state CL-UNIQ preservation rides on the functional identity from Steps 1–3, not on Step 4's pointwise result. The "dual consequence" paragraph makes this explicit.
- **K.μ~ existence condition `|dom_C(M(d))| ≥ 2`.** All four cardinality cases (empty, singleton-content/empty-link, mixed empty-content/non-empty-link, singleton-content/multi-link) are explicitly excluded with the correct reasoning. The empty case is "doubly excluded" — once by the identity-only bijection, once by K.μ⁻'s effect clause being unsatisfiable on `∅`.
- **K.μ⁻ admissible contraction shape equivalence.** Both directions (constructive ⟹ post-state invariants; post-state invariants ⟹ constructive) are proved, with the reverse direction correctly noting that D-CTG★/D-MIN★ at Σ' are *hypothesis*, while S8-depth/S8-fin/S8a are *preserved by restriction*.
- **K.δ case (ii) k = 2 sub-case A2 induction.** The recursive structure (subsequent account chains back to first-account via K.δ k = 0 events) terminates at sub-case A1, with the finite-history justification explicit and the alternative direct T10a.6 discharge offered as a sanity check.
- **Cross-document disjointness chain lemma.** The Case A length argument (`#e₁ < #e₂` from `e₁ ≼ e₂ ∧ e₁ ≠ e₂` via T3) and the same-level zero-count accounting (e₂'s extension positions contain no zeros because both entities have the same total zero count) are tight.
- **P4a transient failure paragraph.** Explicitly admits that the K.α → K.ρ → K.μ⁺ ordering produces an intermediate state where P4a fails (provenance entry without matching containment), and correctly identifies that restoration is *structural* (Σ' carries the witness via J1'★) rather than *temporal* (no earlier state need carry it).
- **L1c structural inc-chain at first link.** The chain `d → b_C(d) → b_L(d) → [d.0.s_L.1]` rests on `s_L = s_C + 1`, which is explicitly cited from SubspaceConventionAxiom rather than assumed implicitly.

## REVISE

(none)

## OUT_OF_SCOPE

(none beyond the twelve Open Questions the ASN already catalogues — link withdrawal mechanism, registry protocol, concurrency, account-level depth-1 extension, link arity admissibility, etc. are all appropriately deferred)

VERDICT: CONVERGED
