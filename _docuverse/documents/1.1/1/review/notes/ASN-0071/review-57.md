# Review of ASN-0071

## REVISE

### Issue 1: wp-defined introduced, forward-referenced, then re-derived
**ASN-0071, Resolution and The operation**: Resolution states "We name this semantic precondition `wp-defined: (A (d_s, σ) ∈ Q :: d_s ∈ Σ.E_doc)` and evaluate throughout this section at a state `Σ` satisfying it (*The operation* shows it is exactly the domain of the partial function `find`)". The operation then re-delivers the same content: "It is the domain of the partial function `find`: `find(Q)(Σ)` is defined exactly when `wp-defined` holds at the evaluation state `Σ`."
**Problem**: The same fact — wp-defined is the domain of the partial function `find` — is asserted in two sections joined by a forward pointer. This is the forward-reference accretion pattern: a parenthetical promise in one section discharged by a near-verbatim restatement downstream.
**Required**: State wp-defined and its role as `find`'s domain once, at the point of definition. Drop the forward pointer and the duplicate gloss.

### Issue 2: F-DEEP presupposes `m_C` defined; empty content-subspace source uncovered
**ASN-0071, F-DEEP / Resolution**: "`#u > m_C ⟹ iaddrs_one(d_s, σ)(Σ) = ∅` — a vspec whose anchor is deeper than the source's arrangement depth resolves to nothing." Proof: "By S8-depth every `v ∈ dom(M(d_s))` has `#v = m_C < #u`."
**Problem**: `m_C` (S8-depth) is well-defined only when `V_{s_C}(d_s) ≠ ∅`. A source whose content subspace is empty (e.g. a freshly created document, or one carrying only link-subspace positions — both reachable under ASN-0047) has no `m_C`, so the hypothesis `#u > m_C` does not type-check and the proof's invocation of S8-depth is vacuous. The resolution is empty in that case, but the claim as stated does not cover it. This is the "applied to empty structure" boundary the spec must address.
**Required**: Either restrict F-DEEP to `V_{s_C}(d_s) ≠ ∅` and add a one-line companion statement that `V_{s_C}(d_s) = ∅ ⟹ iaddrs_one = ∅` trivially, or restate F-DEEP so its premise is well-formed when no content positions exist.

### Issue 3: defensive notation remark in Resolution
**ASN-0071, Resolution**: "The subset claim `iaddrs(Q)(Σ) ⊆ dom(Σ.C)` is read with `Σ` explicit on both sides — the right-hand side is the input state's content store, not a fixed set."
**Problem**: This explains how to read a claim rather than advancing the argument — meta-prose anticipating a misreading. The `Σ`-parameterisation is already visible in the notation `iaddrs(Q)(Σ) ⊆ dom(Σ.C)`.
**Required**: Delete the sentence; the notation carries it.

### Issue 4: Currency section restates the R-independence point twice
**ASN-0071, Currency: state dependence**: "`find` does not consult ASN-0047's provenance relation `R` ... the current-containment result versus the ever-containing relation `R` is deferred (Open Questions). F-COMP must be read in this light — completeness is over the *currently-containing* set: an implementation that misses a currently-containing document violates F-COMP; one that omits a historically-containing-but-no-longer-current document does not."
**Problem**: The substantive point (completeness is over current, not historical, containment) is made first by "`find` does not consult ... `R`", then again by the F-COMP conformance gloss. The second sentence is implementation-conformance essay content restating the first.
**Required**: Keep one statement of the current-vs-historical distinction. Drop the duplicate F-COMP conformance gloss (or fold its single new word — that this is *completeness* over the current set — into the first sentence).

## OUT_OF_SCOPE

### Topic 1: relationship between current result and historical relation R
**Why out of scope**: The Open Questions correctly defer the current-containment-vs-`R` connection; this is genuinely new territory (a temporal/provenance invariant), not a defect in the present operation.

### Topic 2: rejection vs silent filtering of unresolvable positions
**Why out of scope**: Whether the system must reject deep/unmapped vspec positions rather than silently filter (F-FILT) is a policy question for a future ASN; the present ASN's silent-filter semantics are internally consistent.

VERDICT: REVISE
