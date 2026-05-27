# Review of ASN-0091

## REVISE

### Issue 1: Unified-state identification E_doc = dom(M) derivation is interpretive

**ASN-0091, "REARRANGE_K (the cut-sequence operation of ASN-0084) realizes this class" paragraph**: "K.σ adds d to dom(M) with M'(d) = ∅; K.δ-IsDocument adds e to E_doc with effect clause M'(e) = ∅, which extends dom(M) to include e."

**Problem**: ASN-0093's K.σ effect clause only states `dom(M') = dom(M) ∪ {d}` and doesn't mention E_doc; ASN-0047's K.δ-IsDocument adds to E_doc but doesn't explicitly extend dom(M). The claim that each operation extends both sets jointly is an interpretation bridging the two source ASNs but isn't formally anchored in either's effect clause. Since this identification is load-bearing for discharging RA-reg via K.μ~'s `d ∈ E_doc` precondition, the gap matters.

**Required**: Either cite where the unified-state operation semantics formally specifies the joint extension, or supply explicit verification of how K.σ updates E_doc and how K.δ-IsDocument updates dom(M) under unification. The induction step on transition count needs an actual derivation, not an interpretive bridge.

### Issue 2: M0 and M1 from ASN-0093 omitted from per-invariant discharge enumeration

**ASN-0091, "REARRANGE_K (the cut-sequence operation of ASN-0084) realizes this class" paragraph**: "In particular, P0, P1, P2, P3, P6, P7, P7a, P8, NodeLineage, L0–L14, L12, L-fin, C0–C2, and C-fin hold at Σ' iff they hold at Σ."

**Problem**: ASN-0093's M0 (DocumentTumblerWellFormed) and M1 (ArrangementMonotonicity) aren't named. M0 depends on dom(M) (preserved by RA-frame) plus structural ValidAddress and zeros = 2 (state-independent); M1 asserts dom(Σ.M) ⊆ dom(Σ'.M), satisfied by RA-frame's equality. Both are preserved trivially but should appear in the explicit enumeration to make exhaustiveness clear.

**Required**: Add M0 and M1 to the enumeration with discharge justifications matching their structural form.

### Issue 3: Abstract subspace-preservation of π lacks its own labeled claim

**ASN-0091, "Subspace Frame (REARRANGE_K-specific)"**: "RA-adm together with foundation S3★ + L14 already forces subspace preservation — no V-position may cross from one subspace to another under π — but admissibility leaves room for non-identity permutations within each subspace."

**Problem**: The abstract subspace-preservation property of π (`subspace(π(v)) = subspace(v)` for every v) is repeatedly invoked — it's load-bearing for RE-proj transport, for the abstract S3★ discharge at Σ', and as the weaker counterpart to REARRANGE_K-specific RE-sub — but never gets a labeled claim with formal derivation. The proof-by-contradiction structure (using RA-adm + pre-state S3★ + L14) appears twice in prose without becoming an extractable lemma.

**Required**: Introduce a labeled claim — e.g., "RE-subpres" — stating "π preserves subspace identity: subspace(π(v)) = subspace(v) for every v ∈ dom(Σ.M(d))" — with explicit derivation from RA-adm + S3★ + L14, provenance "abstract". Add it to the claims table. RE-sub then becomes the REARRANGE_K-specific pointwise strengthening of this abstract claim.

### Issue 4: RE-frag★/RE-coal★/RE-eq★ existential claim is too informal

**ASN-0091, Claims Introduced table, RE-frag★/RE-coal★/RE-eq★ row**: "Existential composite cardinality variations: any combination of strict increase, strict decrease, or equality is realisable across multi-step sequences."

**Problem**: "Any combination is realisable" requires specifying: for any finite sequence (s₁, ..., s_n) ∈ {+, −, =}^n, there exists a multi-step REARRANGE sequence Σ₀ →_R ... →_R Σ_n where step i exhibits direction s_i. The composition isn't immediate — the post-state shape of one witness must serve as a valid pre-state for the next witness, and this concatenation requires verification (each witness's pre-state assumption must be compatible with the prior witness's post-state).

**Required**: State the existential precisely (per-step direction sequence is arbitrary), and either supply or cite a concatenation construction that produces the required mixed sequence.

### Issue 5: Bijection signature in RA-π overconstrains and creates dependency on RA-dom

**ASN-0091, "REARRANGE as Vstream-Only Operation"**: "there exists a bijection π : dom(Σ.M(d)) → dom(Σ.M(d)) satisfying (A v : v ∈ dom(Σ.M(d)) : Σ'.M(d)(π(v)) = Σ.M(d)(v))"

**Problem**: The signature `π : dom(Σ.M(d)) → dom(Σ.M(d))` pins π's codomain to the *pre-state* domain. The equation requires π(v) ∈ dom(Σ'.M(d)) for the LHS to be defined, so the signature implicitly assumes `dom(Σ.M(d)) ⊆ dom(Σ'.M(d))` — i.e., the forward inclusion half of RA-dom. The ASN's remark acknowledges that "RA-dom and RA-π are not fully independent" but retains the redundancy "for ease of reference" without resolving the type-checking issue.

**Required**: Either weaken π's signature to `dom(Σ.M(d)) → dom(Σ'.M(d))` (with RA-dom partially derivable) — the cleaner choice — or explicitly state that the signature presupposes RA-dom's forward inclusion and use the equation's well-formedness as the implicit justification.

### Issue 6: Density of per-invariant discharge paragraph impedes verification

**ASN-0091, paragraph beginning "REARRANGE_K (the cut-sequence operation of ASN-0084) realizes this class"**: A single ~3000-word paragraph mixes class realization, K.μ~ admissibility derivation, unified-state E_doc = dom(M) discharge, per-invariant discharges for ~15 foundation invariants, extended invariants (S3★, S3★-aux, CL-OWN, CL-UNIQ, P4★, S8★), state-component-only invariants, and P4a handling.

**Problem**: While individually rigorous, the dense interleaving forces the reader to track many concurrent threads. Per-invariant discharges that should stand as independently verifiable sub-claims are buried in prose flow. Specific discharges (e.g., S2 from RA-π + RA-dom, S8★'s content/link split, P4a via append-only trace) deserve their own paragraphs.

**Required**: Break into subsections — "Realization", "K.μ~ Admissibility Clauses", "Unified-state E_doc = dom(M) Discharge", "Per-Invariant Discharges (ASN-0036 set)", "Per-Invariant Discharges (ASN-0047 extended set)", "P4a Handling". Within each subsection, give each invariant its own paragraph or numbered list entry. This eases verification and exposes the discharge structure.

## OUT_OF_SCOPE

### Topic 1: Link-subspace REARRANGE semantics
**Why out of scope**: The ASN flags this in Open Questions. REARRANGE_K's CS3 fixes the cut subspace at s_C, so the link subspace isn't rearrangeable through the current operation. A separate operation for link-subspace rearrangement is genuinely new territory.

### Topic 2: REARRANGE composition with non-REARRANGE operations in mixed sequences
**Why out of scope**: The "Composition Across Multi-Step REARRANGE Sequences" section explicitly restricts the ★ forms to pure REARRANGE-only sequences. Mixed sequences with K.α, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.δ, K.σ, K.ρ are noted to require care (intervening operations shift coverage), but full treatment belongs to per-operation lemmas in the foundation ASNs.

### Topic 3: Whether every well-formed bijection on dom(M(d)) is realisable by a finite composition of REARRANGE_K cut sequences
**Why out of scope**: The Open Questions section flags this. Establishing it requires an inverse construction (given an arbitrary bijection, produce a cut sequence realising it) structurally distinct from this ASN's forward derivation.

### Topic 4: Reachability verification for constructed witness pre-states
**Why out of scope**: The fragmentation/coalescence/equality witnesses construct hypothetical pre-states satisfying foundation invariants. Verifying each pre-state is reachable from Σ₀ via a specific operation trace requires explicit trace construction beyond this ASN's scope.

VERDICT: REVISE
