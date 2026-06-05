# Review of ASN-0100

This is a rigorous, carefully constructed ASN. The proofs are thorough: the three-region decomposition, the S2 pairwise-disjointness argument, the D-CTG★ closed-interval reduction, the INS.proj step-by-step projection trace, and the per-state/boundary atomicity split all hold up under inspection. Edge cases (append, empty document, re-insertion after full clearance, j=0) are handled. Cross-ASN references are all to foundation ASNs. The findings below are confined to the prose accretion the `review-mode.anti-bloat` classifier targets.

## REVISE

### Issue 1: Two-tier atomicity guarantee stated in full twice
**ASN-0100, "The Question" §2 and "Atomicity and Canonical Order"**: The Question contains "We are careful with the word 'atomically.' As the Atomicity section establishes, the guarantee is genuinely two-tiered. The *per-state* invariants (Class (a)) hold at every intermediate state... the *coupling/boundary* properties — P4★..., P4a, and P7a — are transiently unestablished mid-composite... and are restored only at the composite boundary." The Atomicity section opens with the identical content: "its atomicity is the *composite-boundary* form: per-state invariants (Class (a)...) hold at *every* state... composite-boundary properties (Class (b)...) and the coupling constraints... hold at the boundary."
**Problem**: The same two-tier claim is spelled out in full in two sections (plus the INS.atomicity claim row), with the earlier instance forward-deferring to the later one ("As the Atomicity section establishes"). This is the "defer to a downstream location while also stating its content" pattern — the reader processes the full argument twice.
**Required**: In "The Question," pose the atomicity sub-question and defer the answer to the Atomicity section without restating the Class (a)/Class (b) split; let the Atomicity section be the single site that states and discharges it.

### Issue 2: Process-narration that does not advance reasoning
**ASN-0100, "Discovering the Three Effects"**: "We reason from the intent backward to the formal specification."
**Problem**: This narrates the author's method rather than stating content. The three Effect subsections stand on their own; the sentence is meta-prose the precise reader skips. (The "We are careful with the word 'atomically'" framing in Issue 1 is the same category.)
**Required**: Delete the methodological framing sentence; open directly with Effect One.

### Issue 3: INS.identity.tightsurv relabels INS.proj's tight case
**ASN-0100, "INSERT vs. COPY," corollary INS.identity.tightsurv**: "If a tight endset `e` was incorporated at state `Σ_e`... then `a_new ∉ coverage(e)`. This is INS.proj's tight-endset case (`N_{ℓ,i} = ∅`): the endset's coverage is a set of I-addresses, not of values..."
**Problem**: The corollary's body explicitly identifies itself as already-established content ("This is INS.proj's tight-endset case"). It introduces a new claim label for a consequence already proven and stated under INS.proj, adding only the value-vs-address gloss. This is the "two paragraphs say the same thing in different words" pattern dressed as a derived corollary. (By contrast, INS.identity.crossdoc *is* a genuine derivation via SubAllocatorBundle and should stay.)
**Required**: Either fold the value-vs-address observation into INS.proj's tight-endset discussion and drop the separate label, or, if the COPY-distinction framing is wanted, cite INS.proj in one sentence rather than re-deriving and re-labeling.

## OUT_OF_SCOPE

### Topic 1: Link-subspace insertion (K.μ⁺_L) semantics
**Why out of scope**: The ASN correctly bounds itself to the content subspace and names link-subspace insertion as a structurally distinct future operation. The first Open Question already records this.

### Topic 2: Recovery of canonical order after partial composite failure
**Why out of scope**: Implementation-level fault recovery; the abstract spec's atomicity is the composite-boundary guarantee, and the first Open Question flags the implementation obligation appropriately.

VERDICT: REVISE
