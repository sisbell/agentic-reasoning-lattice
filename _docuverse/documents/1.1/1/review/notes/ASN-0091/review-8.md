# Review of ASN-0091

## REVISE

### Issue 1: Abstract definition implicitly requires d ∈ dom(Σ.M) without stating it

**ASN-0091, "REARRANGE as Vstream-Only Operation"**: "A transition `Σ → Σ'` is *Vstream-only on `d`* when dom(Σ'.M(d)) = dom(Σ.M(d))..."

**Problem**: The abstract definition uses `Σ.M(d)`, `dom(Σ.M(d))`, and the bijection `π : dom(Σ.M(d)) → dom(Σ.M(d))` throughout. These are well-typed only when `d ∈ dom(Σ.M)`. RA-frame's `dom(Σ'.M) = dom(Σ.M)` clause preserves registration but does not establish d ∈ dom(Σ.M) at the pre-state. Without an explicit precondition, the conditions are not well-formed when d ∉ dom(M), and the definition would vacuously admit any transition with d unregistered. The ASN's empty-case discussion (`dom(Σ.M(d)) = ∅`) handles the empty-but-registered case but not the unregistered case.

**Required**: Add explicit precondition `d ∈ dom(Σ.M)` to the abstract Vstream-only definition. This brings the abstract definition into alignment with K.μ~'s actual precondition `d ∈ E_doc` (ASN-0047) and makes type-correctness of `dom(Σ.M(d))` immediate.

### Issue 2: Reverse witness coalescence requires justifying why cross-chain disjointness implies c ∉ {a-1, a+2}

**ASN-0091, "Run Decomposition Is Not Invariant"**: "let `c` be an I-address allocated from a different sub-allocator chain disjoint from the chain segment containing `a` and `a + 1` (so in particular `c ∉ {a − 1, a + 2}` — the two values that would make `c` adjacent to `a + 1` on the right or to `a` on the left within a single chain)"

**Problem**: The "so in particular" claims that being in a different sub-allocator chain implies `c ∉ {a-1, a+2}` as tumblers. The structural argument — every chain element of Y has form `[d_Y, 0, s_Y, k_Y]` while a-1, a+2 (as chain elements of X if they exist) have form `[d_X, 0, s_X, k_X ± 1]`, and these structural forms differ — is correct but elided. A reader unfamiliar with the chain-element form derivation cannot verify the "in particular" step.

**Required**: Either (a) state c ∉ {a-1, a+2} as an additional explicit precondition rather than deriving it from chain disjointness, or (b) make the structural-form argument explicit (one sentence noting that distinct sub-allocator chains have structurally distinct element forms by SC-NEQ or cross-document position-5 disagreement).

### Issue 3: Worked example admissibility section omits S2 verification

**ASN-0091, "Worked Example"**: The "Admissibility (RA-adm)" subsection verifies S8a, S8-depth, S3★, D-CTG★, D-MIN★, D-SEQ★ but omits S2 (ArrangementFunctionality).

**Problem**: S2 requires `Σ'.M(d)` to be a partial function. This is not trivially obvious from the construction — it requires that the displayed post-state arrangement assigns at most one I-address per V-position. While derivable from π's injectivity, the omission breaks the worked example's stated pattern of concretely verifying each invariant.

**Required**: Add one line confirming S2 — that the post-state arrangement assigns each listed V-position exactly one I-address (immediate by inspection of the displayed map).

### Issue 4: Identity case derivation compresses RA-frame's role

**ASN-0091, "REARRANGE as Vstream-Only Operation"**: "The *identity case* π = id is admitted: RA-π collapses to `Σ'.M(d)(v) = Σ.M(d)(v)` and RA-frame forces Σ' = Σ."

**Problem**: The claim "RA-frame forces Σ' = Σ" elides the two-step derivation: (i) RA-π + RA-dom give `Σ'.M(d) = Σ.M(d)` as functions; (ii) RA-frame's conjunction (`Σ'.C = Σ.C`, `Σ'.L = Σ.L`, `Σ'.E = Σ.E`, `Σ'.R = Σ.R`, `dom(Σ'.M) = dom(Σ.M)`, and `Σ'.M(d') = Σ.M(d')` for `d' ≠ d`) combined with (i) gives `Σ' = Σ`. Without step (i), RA-frame alone does not pin Σ'.M(d).

**Required**: State the derivation as a two-step composition: "RA-π under π = id together with RA-dom gives `Σ'.M(d) = Σ.M(d)`; combined with RA-frame's preservation of all other state components, `Σ' = Σ`."

## OUT_OF_SCOPE

### Topic 1: Cross-document transclusion split joint-reference semantics
**Why out of scope**: When REARRANGE splits a contiguous V-interval transcluding a contiguous I-span into two non-contiguous V-intervals, the joint-reference semantic (two consecutive V-positions transcluding consecutive I-addresses from the same source as a single semantic unit) is beyond the individual `(a, d)` preservation that RE-trans establishes. The ASN correctly flags this as an open question for a future ASN.

### Topic 2: Link subspace rearrangement
**Why out of scope**: REARRANGE_K's cut subspace is fixed at S = s_C (ASN-0084's CS3). Extension to link subspace rearrangement requires preservation of CL-OWN and CL-UNIQ (ASN-0047), constituting a new operation kind.

### Topic 3: Bijection realizability via cut sequences
**Why out of scope**: Whether every admissible bijection of `dom(M(d))` decomposes into a finite sequence of cut-sequence rearrangements is a structural completeness question about REARRANGE_K's expressive power.

### Topic 4: Cardinality increase upper bounds
**Why out of scope**: The maximum fragmentation increase from one REARRANGE invocation depends on cut count and pre-state run structure; this is an algorithmic-analysis question, not a state-invariant question.

### Topic 5: Discoverability-level observational equivalence
**Why out of scope**: Refined equivalence classes at the discoverability level (coarser than arrangement equality) constitute future development on rearrangement equivalence theory.

VERDICT: REVISE
