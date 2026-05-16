# Review of ASN-0051

I worked through the proofs of SV2–SV13 and the worked examples in detail. The ASN is dense but the proofs are mostly thorough; the SV6 proof in particular is carefully laid out, with the sub-lemma argument routed through T1 and TumblerAdd correctly. Below are the issues I found that warrant revision.

## REVISE

### Issue 1: Implicit s_C = 1 in SV10 witness
**ASN-0051, Discovery-Resolution Distinction (SV10)**: The witness construction uses I-addresses `i_k = O.0.1.k` with explicit element fields `E(i_k) = [1, k]` (so `E(i_k)₁ = 1`), but defines V-positions parametrically as `v₁ = [s_C, 1]` with `s_C` as a symbol.
**Problem**: For the K.α amendment (`fields(a).E₁ = s_C`, ASN-0047) to be satisfied by `i_k`, we need `s_C = 1`. The example silently assumes this. A reader following the SV10 construction step-by-step has no way to know the parametric `s_C` must coincide with the concrete `1` chosen for `E(i_k)₁`.
**Required**: State explicitly at the start of the witness construction that `s_C = 1` is fixed (or, equivalently, that we adopt the convention `s_C = 1` for the text subspace identifier). Then `v₁ = [1, 1]` and the K.α amendment is visibly satisfied.

### Issue 2: "Contrapositive" misused in wp section
**ASN-0051, Weakest Precondition Analysis**: "The contrapositive — the *vitality-loss* condition — is `(A v : v ∈ dom(Σ.M(d)) \ V_rm :: Σ.M(d)(v) ∉ coverage(e))` together with `(E v : v ∈ V_rm : Σ.M(d)(v) ∈ coverage(e))`..."
**Problem**: This is the *negation* of the wp conjoined with a pre-vitality requirement, not the contrapositive. Contrapositive (`P ⟹ Q` ↔ `¬Q ⟹ ¬P`) is a different logical operation from negation. The content is correct but the label misnames the inference.
**Required**: Rename "contrapositive" to "negation" (or describe more precisely: "the condition under which vitality is lost — the negation of the wp conjoined with the pre-state vitality requirement").

### Issue 3: Cross-document discovery-resolution claim is informal
**ASN-0051, SV10 discussion**: After the single-document SV10 statement, the prose adds: "The cross-document case is starker: a link discovered through document d₁ ... may have empty resolution in a different document d₂ whose arrangement contains none of the endset's I-addresses."
**Problem**: The cross-document asymmetry is the conceptually sharper case (discovery non-empty in d₁, resolution empty in d₂), but it is left informal. SV4 + SV10 give it as a corollary, but no formal predicate is exhibited.
**Required**: State the cross-document case as a numbered corollary or extend SV10 to cover it: `(E Σ, a, d₁, d₂, s, A :: d₁ ≠ d₂ ∧ a ∈ discover_s(A) ∧ A ⊆ ran(M(d₁)) ∧ π(L(a).s, d₂) = ∅)`. The witness is trivial — take any state where d₂ has no overlap with the endset.

### Issue 4: NoStaleResolutionState section presentation
**ASN-0051, Endset Projection (NoStaleResolutionState remark)**: The section starts with a definitional observation about locate, then says "The observation is definitional", then "The substantive claim worth stating is about *what the algebra forbids*", then gives the three-clause schema closure argument, then notes the functional fact is "the immediate definitional reading."
**Problem**: The remark conflates three distinct things — (i) the definitional triviality that locate depends on its arguments; (ii) the architectural claim that no auxiliary stale-V-position state exists; (iii) the functional invariance `M(d) equal ⟹ locate equal`. A reader unfamiliar with the foundation may struggle to extract what claim is being asserted versus what is merely observed. The schema closure argument is the substantive content and should be presented as such, with the definitional observation demoted.
**Required**: Restructure so the architectural remark leads with the schema closure argument (the substantive content) and treats the definitional observation as supporting context, not the main claim. Alternatively, split into two paragraphs: one for the definitional triviality, one for the architectural remark.

## OUT_OF_SCOPE

### Topic 1: Same-origin coverage growth formal characterization
**Why out of scope**: The ASN explicitly defers this to ASN-0034's allocator-discipline treatment. The descriptive analysis here (sequential overshoot, child-depth entry) is appropriately scoped as motivation for SV6's cross-origin restriction.

### Topic 2: Higher-arity links (|Σ.L(a)| > 3)
**Why out of scope**: The "Scoping note" explicitly restricts the entire analysis to standard-triple links and defers the higher-arity generalization. This is appropriate — the slot-wise extension is mechanical.

### Topic 3: Broader-level spans (k ≤ p₃)
**Why out of scope**: The "Note on scope" in SV6 explicitly defers broader-level span treatment to ASN-0034. The architectural rationale (deliberate coverage growth via baptism) is given.

### Topic 4: Link subspace projection structure
**Why out of scope**: SV11 explicitly restricts to π_text and defers link-subspace contributions (and reflexive-addressing cases under L13) to the Link Subspace ASN.

### Topic 5: Discovery latency / real-time guarantees
**Why out of scope**: Listed in Open Questions. Real-time properties are not state-transition properties and don't fit the SV framework.

### Topic 6: Fork-time bilateral vitality preservation
**Why out of scope**: Listed in Open Questions. Forking discipline is partially addressed in the SV7 transclusion corollary; the bilateral vitality refinement is appropriately deferred.

VERDICT: REVISE
