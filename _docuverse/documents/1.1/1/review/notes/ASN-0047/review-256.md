# Review of ASN-0047

This is a thorough and largely sound specification. The state model (Σ = C, L, E, M, R), the seven elementary transitions, the per-subspace strengthenings (D-CTG★/D-MIN★/D-SEQ★), and the K.μ~ decomposition are carefully argued, and the worked examples genuinely exercise the postconditions. The K.μ~-FIX / link-subspace-fixity ordering is non-circular, clause (iv)'s independence is correctly defended, and the J1★/J1'★ wp derivations are real analysis. The issues below are prose-integrity and notational, not structural-correctness, gaps.

## REVISE

### Issue 1: "Inherited from foundation" preamble contradicts the body's own preservation work
**ASN-0047, *Properties Introduced → Inherited from foundation***: "They are restated in the body of this ASN purely for narrative continuity — every statement and **every preservation argument is supplied by the cited foundation, not by local derivation.**"

**Problem**: This is false for the link invariants in that very table. L0, L1, L1a, L1c, L3 must be preserved under transitions that *did not exist* in the cited foundation — K.μ⁺_L (genuinely new here) and the amended K.λ/K.μ⁺/K.μ⁻/K.μ~. The foundation (ASN-0093) cannot have argued preservation under transitions ASN-0047 introduces, and indeed the Class (a) verification *does* derive them locally (e.g., "L0 (SubspacePartition). L-clause from K.λ's precondition subspace_I(ℓ)=s_L; preserved by L12. C-clause from K.α's E(a)₁=s_C precondition…", and L1c's full first-link/subsequent-link chain construction). The preamble's "not by local derivation" is directly contradicted by the body it introduces.

**Required**: Rewrite the preamble to say that the foundation supplies the *statement* (and preservation under foundation transitions), while preservation under this ASN's new/amended transitions is established locally in the Class (a) verification. Otherwise either the preamble or the body's link-preservation prose is wrong.

### Issue 2: "tracked" sub-allocator terminology is load-bearing but undefined, reinventing ASN-0034's "activated allocator"
**ASN-0047, *FrontierEquivalence*, *TrackedEmission*, *ParentAllocatorDispatch***: "the unique allocator `A` whose **tracked domain** contains `t`"; "every non-node entity is an emission of a **tracked entity-level sub-allocator**"; "for any entity `t` produced by a **tracked allocator**."

**Problem**: The freshness/frontier arguments turn on an allocator being "tracked" and on "tracked-domain monotonicity," yet "tracked" is never defined. ASN-0034's AllocatedSet already supplies the corresponding notions — *activated* allocators, the realized domain `domₛ(A)`, and its monotonicity. If "tracked" is meant to be "activated," the ASN should use the foundation term or explicitly define the synonym; if it means something else, that something must be stated, since T10a.6/T10a.7 uniqueness (on which FrontierEquivalence rests) are stated over allocator domains, not over an undefined "tracked" status.

**Required**: Either replace "tracked" with ASN-0034's "activated"/`domₛ(A)` vocabulary, or add a one-line definition tying "tracked sub-allocator" / "tracked domain" to the foundation notion it abbreviates.

### Issue 3: Orphan-links section duplicates the Class (a) link-invariant preservation prose
**ASN-0047, *Orphan links and coupling flexibility***: "K.λ's preconditions guarantee L0 (…), L1 (zeros(ℓ) = 3), L1a (origin(ℓ) ∈ E_doc), L3 (…), L12 (…), and L14 (disjointness…)."

**Problem**: This restates, transition-by-transition, the exact preservation facts the Class (a) verification already establishes for K.λ (the L0/L1/L1a/L3/L12/L14 rows and their prose). The section's *unique and worthwhile* content is the coupling-vacuity argument — that K.λ-alone satisfies ValidComposite★ (J0, J1★, J1'★ all vacuous) so the orphan state is a valid composite endpoint. The invariant re-enumeration is the "two paragraphs saying the same thing" pattern the anti-bloat directive flags.

**Required**: Reduce the invariant list to a single pointer ("the per-state invariants are preserved by K.λ's frame and preconditions per the Class (a) verification") and keep only the coupling-vacuity argument, which is the section's actual contribution.

## OUT_OF_SCOPE

### Topic 1: Link-withdrawal / tombstoning mechanism under D-CTG★
**Why out of scope**: The interaction between Nelson's tombstoning (LM 4/9) and the dropped link-subspace exemption (interior link withdrawal now forces suffix withdrawal) is correctly identified by the ASN as requiring a separate mechanism; it is already listed in Open Questions, not falsely claimed here.

VERDICT: REVISE
