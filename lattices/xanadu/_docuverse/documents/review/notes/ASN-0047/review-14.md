# Review of ASN-0047

## REVISE

### Issue 1: J4 fork definition omits d_src ∈ E_doc precondition
**ASN-0047, Coupling and isolation / J4**: "A *fork* of d_src to d_new is a composite transition Σ → Σ' consisting of: ... (ii) K.μ⁺ populating M'(d_new) with ran(M'(d_new)) ⊆ ran(M(d_src))"
**Problem**: The constraint references M(d_src), which is only defined when d_src ∈ E_doc. Every other transition definition states its entity preconditions explicitly — K.α requires origin(a) ∈ E_doc, K.δ requires parent(e) ∈ E, K.μ⁺ requires d ∈ E_doc. J4 leaves d_src's membership implicit. Without it the definition is ill-formed: M(d_src) is undefined when d_src is a node or account, or when d_src has not been created.
**Required**: State `d_src ∈ E_doc` as a precondition of the fork definition, parallel to the precondition style used for every elementary transition.

### Issue 2: P6 mislabeled as cross-layer invariant
**ASN-0047, Temporal decomposition**: "Two cross-layer invariants bridge the existential and historical layers, making the temporal contracts precise."
**Problem**: P6 (origin(a) ∈ E_doc for all a ∈ dom(C)) links C and E — both components of the existential layer as defined three paragraphs earlier ("The existential layer (C, E) answers *what is*"). P6 is an intra-existential coherence constraint, not a cross-layer bridge. Only P7 (a ∈ dom(C) for all (a, d) ∈ R) actually bridges the existential (C) and historical (R) layers. The sentence claims two cross-layer invariants where only one qualifies. The missing cross-layer bridge is arguably P4 / Contains(Σ) ⊆ R, which bridges the presentational layer (M, via Contains) and the historical layer (R) — but P4 isn't mentioned in this section despite being the load-bearing invariant that makes J1 necessary.
**Required**: Correct the characterization. P6 is intra-existential; P7 is existential-to-historical. If the section intends to catalogue cross-layer invariants, Contains ⊆ R (presentational-to-historical) belongs here as the third relationship, or at minimum acknowledge P4's cross-layer role.

### Issue 3: Worked example does not trace K.μ~ (reordering)
**ASN-0047, Worked example**: "The three steps exercise J0, J1, J2, J4, P4, P5, P6, P7, and P8"
**Problem**: The worked example traces fork (K.δ + K.μ⁺ + K.ρ), insertion (K.α + K.μ⁺ + K.ρ), and deletion (K.μ⁻). K.μ~ receives extensive treatment — its own definition, an isolation property (J3), a decomposition argument, and a role in the temporal decomposition table — but no concrete verification. The claim that ran(M(d)) is preserved, that Contains(Σ') = Contains(Σ), and that no provenance recording is needed are all asserted abstractly. A single step — e.g., swapping V-positions [1,2] and [1,3] in d₂ after the deletion, verifying J3 and P4 against specific values — would ground these claims and complete the coverage of all six transition kinds.
**Required**: Add a K.μ~ step to the worked example, verifying J3 (isolation), ran preservation, and P4 against concrete state.

## OUT_OF_SCOPE

### Topic 1: Link endset semantics and structural distinction from documents
**Why out of scope**: The ASN correctly places links in E_doc ("We include links in E_doc ... The structural distinction between documents and links — endset semantics, subspace layout — belongs to a separate analysis"). The elementary transitions defined here apply uniformly to documents and links; endset-specific invariants (span references, directionality, type endsets) are new territory requiring their own formal treatment.

### Topic 2: Operational composition from elementary transitions
**Why out of scope**: The ASN defines what changes are possible (elementary transitions) and what constraints bind them (coupling). How these compose into user-facing operations (INSERT, COPY, REARRANGE, MAKELINK) with their own preconditions, postconditions, and sequencing constraints is explicitly deferred in the scope section and is a distinct specification problem.

VERDICT: REVISE
