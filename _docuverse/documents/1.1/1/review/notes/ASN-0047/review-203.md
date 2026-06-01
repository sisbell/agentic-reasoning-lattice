# Review of ASN-0047

## REVISE

### Issue 1: K.μ~ S3★ discharge is circular for arbitrary admissible π
**ASN-0047, *Decomposition of K.μ~*, Steps (A)–(B)**: Step (A): "Admissibility clause (i) hands us both S3★(Σ') and S3★-aux(Σ') as hypotheses on the candidate π. Consuming them, we derive subspace preservation." Step (B.3): "what remains is to show the K.μ⁻ + K.μ⁺ decomposition actually realises an admissible π and produces a post-state Σ' that genuinely satisfies that S3★(Σ')."

**Problem**: Step (A) derives subspace preservation by *consuming* S3★(Σ') (the s_C→s_L and s_L→s_C cases are closed using S3★(Σ')'s link/content clauses at π(v)). Step (B.2)/(B.3) then uses Step (A)'s subspace preservation to "genuinely establish" S3★ at the realized post-state. The conclusion (S3★ holds at the post-state) feeds the premise (S3★(Σ') consumed in Step A). So Steps (A)/(B) cannot serve as an independent discharge of S3★ under K.μ~. The only non-circular verification is the sufficiency construction (π_swap), where subspace preservation is read directly off the transposition's structure (a swap within dom_C) without assuming S3★(Σ'). The text's claim that B.3 is a discharge — and the verification-matrix note "this same filter stipulation, discharged at Step (B.3)" — overstates what B.3 does.

**Required**: Either (a) present S3★ under K.μ~ honestly as *guaranteed by the admissibility filter*, with non-vacuity carried entirely by the sufficiency construction's direct verification of clause (i) (including S3★) for π_swap; or (b) derive subspace preservation for the realized decomposition without presupposing S3★(Σ'). Point the matrix's S3★/K.μ~ cell at the sufficiency construction, not at the circular Step (B.3).

### Issue 2: "frame" justification for K.μ⁺ under CL-UNIQ is incorrect
**ASN-0047, Class (a) matrix (CL-UNIQ row, K.μ⁺ cell = "frame") and CL-UNIQ prose**: "K.μ⁻ restriction ... K.μ~ preservation ... All other transitions hold M in frame."

**Problem**: "All other transitions" includes K.μ⁺, but K.μ⁺ does *not* hold M in frame — it extends M(d) (`dom(M'(d)) ⊃ dom(M(d))`). The CL-UNIQ matrix cell for K.μ⁺ likewise reads "frame." The correct discharge is that the K.μ⁺ amendment confines additions to subspace s_C, leaving `M(d)|_{dom_L}` unchanged, so link-subspace injectivity is preserved. Note the CL-OWN/K.μ⁺ cell *does* qualify this correctly ("frame (no link-subspace V-positions added)"); CL-UNIQ is inconsistent with it.

**Required**: Replace the bare "frame" for CL-UNIQ/K.μ⁺ (cell and prose) with the content-subspace-confinement justification, matching the CL-OWN treatment.

### Issue 3: Epistemic meta-prose in K.δ case (ii) discharge does not advance the argument
**ASN-0047, *K.δ case (ii) discharge and parent-allocator activation*, opening**: "Each non-node K.δ event observes the freshness conjunct `e ∉ E` before firing: it is a caller-checked guard, a precondition observed before the event fires, not a conclusion derived afterward. Once the guard has been applied, GlobalUniqueness preserves the distinctness invariant that always applying it maintains — GlobalUniqueness preserves distinctness, it does not supply the guard."

**Problem**: This restates one fact ("the guard is a precondition, not a derived conclusion") twice in two clauses, then restates GlobalUniqueness's role twice ("preserves the distinctness invariant... preserves distinctness, it does not supply the guard"). It explains the *epistemic status* of the guard rather than discharging any obligation — the precise reader must skip it to reach the per-k case analysis that follows. This is the "explains why rather than what" / "two clauses say the same thing" pattern flagged by the anti-bloat classifier.

**Required**: Collapse to a single sentence: the freshness guard `e ∉ E` is a caller-checked precondition; GlobalUniqueness (ASN-0034) preserves resulting distinctness. Then proceed to the per-k analysis.

### Issue 4: K.δ-ID table note enumerates naming rationale instead of advancing content
**ASN-0047, *Derived structural identities* table preamble**: "The K.δ-ID identities below are *derived consequences* of TA5... and T4b... *not* primitive specifications introduced by this ASN. They are listed under separate naming so they can be cited by name ... without unpacking the TA5 / T4b derivation chain at each invocation."

**Problem**: This is meta-prose justifying *why the identities are named and tabulated* rather than stating or advancing them. The "derived not primitive" claim and the citation-convenience rationale carry no object-level content; the derivations themselves already live at the inline K.δ catalogue.

**Required**: Drop the rationale sentences; a one-line pointer ("Derivations at *Elementary transitions*, K.δ case (ii)") suffices, which the table's "Derivation" column already supplies.

## OUT_OF_SCOPE

### Topic 1: K.μ⁺ as content-subspace append-only operation
The implicit consequence that K.μ⁺ alone can only append at the content-subspace maximum (interior insertion requires the K.μ⁻+K.μ⁺ replacement composite) is correct and demonstrated in the interior-replacement example, but is never stated as a derived consequence. Making it explicit is a clarity improvement, not a correctness defect in this ASN.

**Why out of scope**: The behavior is fully determined by the D-CTG★/D-MIN★ preconditions already stated; an explicit "append-only" lemma is an additive convenience, not a fix to anything wrong here.

VERDICT: REVISE
