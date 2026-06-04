# Review of ASN-0091

## REVISE

### Issue 1: Circular discharge of K.μ~ admissibility clause (iv) against RA-adm

**ASN-0091, "Clause Correspondences and Per-Invariant Discharges"**: The discharge table lists clause (iv) (subspace-preserving) as discharged by "RE-subpres (abstract), strengthened by R-PPERM/R-SPERM confining each branch of π to one subspace."

**Problem**: The dependency chain is circular. RA-adm is discharged in three layers; Layer 3 ("Remaining per-state invariants, from ExtendedReachableStateInvariants") is what establishes post-state S3★ and S3★-aux, and it requires K.μ~ to be a valid composite — i.e., clauses (i)–(v) already closed. But clause (iv)'s discharge cites RE-subpres, whose own derivation (stated explicitly) consumes "RA-adm (for both post-state S3★ and post-state S3★-aux)." So:

clause (iv) ← RE-subpres ← post-state S3★/S3★-aux ← ExtendedReachableStateInvariants ← K.μ~ valid ← clause (iv).

The constructive R-PPERM/R-SPERM confinement *can* break this cycle (subspace(π(v)) = subspace(v) follows from the cut-sequence branch structure and OrdShiftHom alone, with no appeal to post-state S3★), but the table lists RE-subpres as the primary discharge and demotes the constructive argument to a "strengthening" — exactly backwards for breaking the cycle.

**Required**: Reorder the discharge so clause (iv) for REARRANGE_K rests solely on the constructive R-PPERM/R-SPERM confinement (independent of RA-adm), and drop RE-subpres from clause (iv)'s discharge. State that RE-subpres is a downstream consequence of RA-adm, not a premise of it.

### Issue 2: The abstract RA-* class restates a foundation definition rather than building on it

**ASN-0091, "REARRANGE as Vstream-Only Operation"**: RA-reg, RA-dom, RA-π, and the C-frame portion of RA-frame.

**Problem**: ASN-0084 (foundation) already defines ArrangementRearrangement: `dom(M'(d)) = dom(M(d))`, `C' = C`, `M'(d') = M(d')` for `d' ≠ d`, and the bijection equation `M'(d)(π(v)) = M(d)(v)`. RA-dom, RA-π, and RA-frame's `Σ'.C = Σ.C` / other-document clause reproduce this verbatim under new labels, without citing it. Per review standard 7, an ASN must use a foundation definition, not reinvent it.

**Required**: Define the Vstream-only class as ASN-0084's ArrangementRearrangement *extended* with the L/E/R frame conditions and the admissibility clause RA-adm. Retain only the genuinely new clauses (L/E/R frame, RA-adm); cite the foundation for the rest.

### Issue 3: Forward-reference meta-prose in the definition section

**ASN-0091, "REARRANGE as Vstream-Only Operation"**: "Every RE-* claim derived from RA-π below is parameterised by the specific π witnessing the transition; RE-proj in particular states `project(e, d, Σ') = π(project(e, d, Σ))` for whichever π witnesses Σ → Σ', not for an arbitrary bijection." Also, mid-S2-derivation: "An abstract-tagged claim, here and throughout, is one derived from the RA-* clauses alone, so it holds for every concrete realisation of the class."

**Problem** (anti-bloat classifier): The first sentence is a use-site inventory that names and partially states a downstream claim (RE-proj) before it is introduced — it advances no reasoning at the definition site. The second is a terminology essay inserted into the middle of a proof. Additionally, RA-adm's "lies outside its scope" qualification is restated in the definition, the Claims-Introduced table, and the worked-example "Composite-boundary properties" bullet; and the clause-correspondence table defers RA-adm to "the per-invariant layers below" three times in close succession.

**Required**: Remove the forward inventory of RE-proj from the definition. Move the "abstract-tagged claim" terminology to a single defining location (e.g., adjacent to the Provenance-column legend) rather than inline in a derivation. State the RA-adm scope qualification once.

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics, run-cardinality upper bounds, observational equivalence
**Why out of scope**: These are correctly confined to the Open Questions list. CS3 fixes the cut subspace to s_C, so content-only rearrangement is the deliberate scope; link-subspace reordering, a bound on per-invocation run-cardinality increase, and discoverability-level equivalence are genuinely future territory, not gaps in this ASN.

VERDICT: REVISE
