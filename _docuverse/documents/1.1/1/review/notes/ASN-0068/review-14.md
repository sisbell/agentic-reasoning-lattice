# Review of ASN-0068

I checked the operation definition, the correspondence relation, the run/maximality conditions, CV-MAX (existence + uniqueness + offset uniqueness), the boundary claims (CV-EMPTY, CV-FIN), the span projection, and all four worked examples. I verified the proof chains step by step.

## What I verified holds

- **CV-MAX existence.** The left/right walk construction, the left-region/right-region split via M-aux and the CV-PRED inverse properties, and the maximality discharge are all correct. Left-walk termination is grounded in D-SEQ★ + S8a (last-component bound), right-walk in S8-fin — both concrete, not hand-waved.
- **CV-MAX uniqueness.** The lockstep-offset reduction (`δ = j²_a − j¹_a = j²_b − j¹_b` via OrdinalShift last-component + T3), the δ = 0 and δ > 0 cases, and the separate offset-uniqueness conjunct are each sound. The inequality chain in Case δ > 0 (`0 ≤ δ−1 < n¹`) is valid.
- **Subspace confinement under admissibility.** The exact `actionPoint(width(σ)) = m_σ` constraint forces `width(σ)_1 = 0`, so start and reach share prefix `[S,1,…,1]`; T5 then confines all of `⟦σ⟧` to subspace S at depth `m_σ`. This underwrites the well-formedness of the run-start positions used in CV-SPAN-VIEW (a), so that postcondition's "v_a is a depth-`m_a` V-position in subspace S" premise is established (in CV-IN), not assumed.
- **Boundary cases.** Empty restriction / empty subspace (CV-EMPTY), width-1 and aggregation (CV-ATOM), self-comparison content (CV-SELF) and link (CV-LINK-SELF), cross-document link degeneracy (CV-LINK-DEGEN), and differing depths (Example 4 + CV-SPAN-VIEW input parameterization) are all covered with derivations, not deferrals.
- **Examples.** Examples 1–4 recompute correctly; the cardinality remarks in CV-FIN (interior bound not an upper bound; product bound smallest cardinality-expressible) check out against Examples 1 and 3.
- **Read-only / determinism / symmetry.** CV-RO, CV-DETERM, CV-SYM each trace single-valued determination chains or syntactic-symmetry arguments correctly.
- **References.** Only foundation ASNs (0034, 0036, 0047, 0053, 0058) are cited. No reinvented notation. No simulated tool use. The operation specifies a system observation abstractly — no implementation drift.

The Open Questions correctly defer concurrent modification, replication, sub-allocator-boundary runs, and depth-representation presentation to future ASNs, matching the declared scope. A correspondence run does not assume I-address contiguity across offsets, so the sub-allocator-boundary question is genuinely open rather than a latent gap in CV-MAX.

I found no skipped case, no proof-by-similarly, and no checkmark standing in for an argument.

VERDICT: CONVERGED
