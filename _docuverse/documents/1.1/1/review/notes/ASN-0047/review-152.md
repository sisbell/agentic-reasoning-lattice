# Review of ASN-0047

## REVISE

### Issue 1: Verification matrix hardcodes `m_L = 2`, contradicting the per-document depth axiom
**ASN-0047, Class (a) verification matrix, row "S8a, S8-depth, S8-fin", column K.μ⁺_L**: "precondition: positivity, m_L=2, finite"
**Problem**: LinkVPositionDepthAxiom fixes a per-document depth `m_L(d) ≥ 2` "without pinning `m_L(d)` to any particular value," and K.μ⁺_L's own definition uses `m_L(d)` throughout. The matrix cell pins it to `2`, which is only the value chosen in the worked example. A reader relying on the matrix as a navigational index will read the wrong constraint.
**Required**: Replace `m_L=2` with `depth m_L(d)` (or `m_L(d) ≥ 2`) to match the axiom and the K.μ⁺_L precondition.

### Issue 2: Essay content in an axiom slot — LinkVPositionDepthAxiom (anti-bloat)
**ASN-0047, Link-subspace extension, "Why link depth is permanent across an empty subspace while content depth is not"**: a ~250-word paragraph arguing from Nelson's "permanent order of arrival" and T0(b) why the axiom should hold.
**Problem**: This is the `review-mode.anti-bloat` pattern "new prose around an axiom explains *why* the axiom is needed rather than *what* it says." The axiom's content is the single sentence preceding it; the essay is design rationale, not a statement of the invariant, and the reader must skip it to reach the next load-bearing claim.
**Required**: Reduce to one sentence stating the design intent (link depth permanent, content depth per-insertion), or move the rationale to a non-structural note.

### Issue 3: Defensive justification essay for D-CTG★/D-MIN★ (anti-bloat)
**ASN-0047, Amendments to existing transitions, "Justification (uniform contiguity, no link-subspace exemption)"**: a ~450-word paragraph defending the strengthening against a perceived deviation from Nelson's tombstoning design (LM 4/9), with sub-arguments (i)/(ii) and implementation-evidence recitation.
**Problem**: Anti-bloat pattern "defensive justifications ... in structural slots." The two architectural commitments are already discharged by L12 and the named orphan-link state elsewhere; this paragraph restates them defensively rather than advancing the contiguity claim. The substantive content (interior withdrawal is out of K.μ⁻'s contract) is also stated in Open Questions and in *Orphan links and coupling flexibility*.
**Required**: Collapse to the load-bearing sentence (uniform contiguity constrains arrangement, not link existence; interior withdrawal needs a separate mechanism — see Open Questions) and delete the duplicated tombstoning recitation.

### Issue 4: Repeated boilerplate across transition frames (anti-bloat)
**ASN-0047, Amendments to existing transitions (K.α, K.μ⁺, K.μ⁻, K.ρ) and J2, J3**: the near-identical sentence "The `L' = L` conjunct extends the original ... frame (which predated the link store) into the extended state, discharging P3's L-monotonicity clause `dom(L) ⊆ dom(L')`" recurs ~6 times.
**Problem**: Anti-bloat pattern "two paragraphs say the same thing in different words." The matrix preamble already states the uniform justification ("link-store invariant rows ... rest on the amended forms ... which add the explicit `L' = L` conjunct"). Repeating it per-transition is noise.
**Required**: State the `L' = L` rationale once (the matrix preamble already does) and drop the per-frame restatements.

### Issue 5: Multiple deferrals to "Decomposition of K.μ~" for one claim (anti-bloat)
**ASN-0047**: S3★ preservation under K.μ~ is asserted-and-deferred in at least three places — "K.μ~'s preservation of S3★ ... is established in *Decomposition of K.μ~* below" (S3★ section), the matrix S3★/K.μ~ cell "holds by the admissibility filter; see *Decomposition of K.μ~*", and the *Generalized referential integrity* prose — before the actual Steps (A)/(B) proof.
**Problem**: Anti-bloat pattern "multiple paragraphs in different sections defer to the same downstream location." The reader is pointed forward three times to a single proof.
**Required**: Keep one forward pointer (the matrix cell) and let the Decomposition section carry the proof; drop the redundant deferrals.

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
**Why out of scope**: J4 explicitly leaves "a mechanism for link inheritance under forking" to a future ASN, and the version-lineage/arrangement relationship is an Open Question. Not an error here.

### Topic 2: Type-only link admissibility (`e₁ ∪ e₂ ≠ ∅`)
**Why out of scope**: The ASN records the K.λ narrowing decision as design-uncertain and defers it to a future operations ASN. Correctly deferred.

VERDICT: REVISE
