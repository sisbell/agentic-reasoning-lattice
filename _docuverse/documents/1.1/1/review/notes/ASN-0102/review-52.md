# Review of ASN-0102

## REVISE

### Issue 1: "Canonical count of the copied region" conflates a global property with a local one
**ASN-0102, X8 (RunFragmentation)**: "The *canonical* (maximally-merged, M12) count of the copied region need not equal `k` … Hence the canonical block count is `≤ k`, with equality exactly when no inter-reference boundary is I-adjacent."
**Problem**: M12 (CanonicalUniqueness, ASN-0058) defines the maximally-merged decomposition of the *whole* arrangement `M(d)`, uniquely — there is no "canonical decomposition of a region." X12 establishes that copied blocks can also merge with the *unmoved predecessor* (leading boundary) and the *first displaced block* (trailing boundary). So in the global canonical form the copied blocks do not have a well-defined separate count. The final worked example demonstrates this directly: with no further qualification the whole arrangement collapses to the single block `([1,1], a_1−2, 6)`, in which the "copied region" of `k=2` blocks has no independent canonical count. As written, X8's "equality iff no inter-reference boundary is I-adjacent" is only true if the copied blocks are canonicalized *in isolation*, which contradicts the global M12 the claim cites and the boundary absorption X12 asserts.
**Required**: State explicitly that X8's "canonical count" is the in-isolation merge of the copied blocks among themselves, and that the whole-arrangement canonical count is further reduced by X12 boundary absorption. The two notions must be named distinctly, since X8 and X12 currently describe reductions of the same object without reconciling them.

### Issue 2: X14 is saturated with proof-bookkeeping meta-prose
**ASN-0102, X14**: "**Boundary lift (invoked uniformly below).** … We cite "(i)/(ii) at `B`" below without re-deriving the standalone/embedded split per clause." and the repeated restatement of the standalone-vs-embedded reading inside J1★, J1'★, P4★, and P4a.
**Problem**: The standalone/embedded distinction may be substantively necessary (COPY appears both as a length-1 composite and embedded), but the discharge is wrapped in essay-level commentary about *how the proof is organized* rather than what each invariant requires: a "boundary lift … invoked uniformly below" preamble, citation-discipline asides ("we cite … without re-deriving"), and "We do **not** lift the `New`/`Old` split (taken at `Σ_i`) to the embedded boundary `Σ_0`." The reader must work past this scaffolding to reach the object-level argument. The same standalone/embedded content is re-stated in multiple clauses in different words.
**Required**: Hoist the boundary lift to a single named premise (`B = Σ` standalone, `B = Σ_0` embedded; facts (i)/(ii)), then discharge each coupling once against it. Delete the citation-discipline asides and the per-clause re-explanations; the device should be stated once and applied silently.

### Issue 3: The Amendment explains COPY's coupling status by analogy/contrast rather than stating it
**ASN-0102, Amendment to ValidComposite★**: "This is the discipline ASN-0047's composite `J4` (Fork) follows — bundling arrangement extension with its own `K.ρ` provenance recording. It is *weaker* than the full state-isolation ASN-0047 attributes to `K.μ⁻` (J2) and `K.μ~` (J3), which assert `C' = C ∧ L' = L ∧ E' = E ∧ R' = R` and so record no provenance; COPY changes both `M` and `R`."
**Problem**: The object-level fact — COPY records its own provenance and discharges the step-local couplings for its own effect — is already stated in the preceding sentence. The J4/J2/J3 comparison is rationale explaining *why* COPY's coupling status sits where it does relative to other operations, not *what* COPY guarantees. This is the "explains why the [status] is needed rather than what it is" pattern.
**Required**: Drop the comparative paragraph. State COPY's coupling obligations (it changes `M` and `R`; it records provenance for every copied address) and discharge them; the contrast with J2/J3/J4 carries no obligation for COPY and belongs, if anywhere, in a design note.

## OUT_OF_SCOPE

### Topic 1: Re-displacement of copied content by later operations (Open Question 1)
**Why out of scope**: The invariant tying origin to continued discoverability under subsequent displacement is INSERT/DELETE/REARRANGE mechanics and link-projection territory (ASN-0098), not COPY's contract. Correctly deferred as an Open Question.

### Topic 2: Time-varying resolution of two references to the same content (Open Question 3)
**Why out of scope**: Cross-time view divergence is a versioning/replication concern, explicitly outside this ASN's scope.

VERDICT: REVISE
