# Review of ASN-0047

## REVISE

(none)

## OUT_OF_SCOPE

(none — the ASN respects the scope boundary established in the prompt; named operations, authority model, and concurrency are properly deferred to future ASNs, with the Open Questions section curating those topics)

**Notes on strengths verified during review:**

The ASN is mathematically rigorous and self-contained. Specific verifications I performed:

- **FrontierEquivalence lemma**: the three-premise chain (TA5(c) functional determinism + P1 + operational precondition; derived T10a chain-advancement uniqueness at `(t, 0)` since T10a's direct per-`(t, k')` uniqueness is stated only for k ∈ {1, 2}) closes both directions of the biconditional. The reverse direction's invocation of T10a.6 (cross-allocator domain-disjointness) is sound: inc(t, 0) cannot be the base of a new child allocator (T10a's spawning rule requires k' ∈ {1, 2}, not 0), so inc(t, 0) can only be produced by t's own sub-allocator chain.

- **K.μ⁻ admissible contraction shape** (forward and reverse direction): the equivalence between the constructive precondition (per-subspace retention count `n'_S`) and the post-state characterisation (D-CTG★ + D-MIN★ + D-SEQ★) is proved both ways. The reverse direction's use of D-SEQ★ at the candidate post-state Σ' (hypothesised, not derived from arbitrary restriction) correctly handles that D-CTG★/D-MIN★ are not automatically preserved by restriction — they're supplied by the candidate-state hypothesis.

- **K.μ~ dependency chain (Steps A–E)**: Step (A) derives subspace preservation in a single step from admissibility (i)'s stipulated S3★(Σ') + S3★(Σ) + L14 + bijection equation. Step (B)'s mechanical realisation by the full-clearance form consumes Step (A) but not link-fixity. Steps (C)–(D) establish link-fixity (functional identity from Steps 1–3 supplies post-state CL-UNIQ; pointwise fixity via Step 4 requires CL-UNIQ at the pre-state — properly noted as the inductive hypothesis on reachable Σ). Step (E)'s `|dom_C(M(d))| ≥ 2` is shown necessary and sufficient with a constructive transposition witness for sufficiency.

- **Worked examples verify load-bearing postconditions concretely**: the entity-hierarchy example traces all four K.δ patterns including the K.δ k = 0 sibling document dispatch through FrontierEquivalence; the interior-content-replacement four-step composite explicitly computes `ran(M'(d)|_{s_C}) \ ran(M(d)|_{s_C}) = {a₂'}` to verify J1★/J1'★ with re-added addresses vacuously discharged; the two-step/three-step replacement variants partition cleanly by pre-state membership of `(a, d)` in R.

- **Boundary cases**: empty arrangements (vacuous quantifiers), single-element arrangements (K.μ~ existence condition excludes), first emissions (SubAllocatorAxiom.FirstEmission), subsequent emissions (T10a's GlobalUniqueness on inc chains), fresh documents (totality convention `M(d) = ∅` for `d ∉ E_doc`), and the empty-arrangement boundary for K.μ⁻ (`dom(M(d)) ≠ ∅` precondition).

- **Cross-ASN references**: every numbered ASN reference is to a foundation ASN (0034, 0036, 0040, 0043, 0045, 0093). No prohibited cross-references.

VERDICT: CONVERGED
