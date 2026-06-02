# Review of ASN-0047

## REVISE

### Issue 1: J2's P4★ justification asserts the bound at intermediate states where it is declared able to fail
**ASN-0047, *Coupling and isolation*, J2 (Contraction isolation)**: "For the operative provenance bound P4★: contraction can only remove pairs from Contains_C, so `Contains_C(Σ') ⊆ Contains_C(Σ) ⊆ R = R'`."

**Problem**: The middle inclusion `Contains_C(Σ) ⊆ R` is precisely P4★ evaluated at the *pre-state* Σ of the elementary K.μ⁻. But P4★ is declared a *composite-boundary property* that "may transiently fail at intermediate states within a composite" (section preamble; Composite-boundary verification matrix records its failure point as "After K.μ⁺ before K.ρ"). A valid composite may fire K.μ⁻ at exactly such an intermediate state — e.g. the sequence K.μ⁺ (places `a`, breaking P4★) → K.μ⁻ → K.ρ, where each step satisfies its elementary precondition (K.μ⁻ requires no P4★). At that Σ, `Contains_C(Σ) ⊆ R` is false, so the stated inclusion chain does not hold. What J2 actually needs — that K.μ⁻ removes from Contains_C and frames R, hence *cannot newly violate* P4★ — is true and independent of P4★ holding at Σ, but the inclusion chain as written overstates it.

**Required**: Replace the chain with the monotonicity statement K.μ⁻ genuinely supports: `Contains_C(Σ') ⊆ Contains_C(Σ)` with `R' = R`, so K.μ⁻ introduces no new P4★ violation relative to Σ (whatever P4★'s status at Σ). Do not assert `Contains_C(Σ) ⊆ R` as a pre-state fact.

### Issue 2: K.μ⁻ contraction-shape semantics are restated in four separate locations
**ASN-0047, K.μ⁻ definition / K.μ⁻ amendment / *K.μ⁻ admissible contraction shape* / Class (a) matrix prose**: The per-subspace suffix-prefix retention shape (`V_S(d') = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}`, derived from D-CTG★+D-MIN★+D-SEQ★, strict on at least one subspace) is stated in the K.μ⁻ box, restated in the K.μ⁻ amendment ("PerSubspaceScope") box, re-derived in full in the "K.μ⁻ admissible contraction shape" equivalence proof, and described again in the *D-CTG★ / D-MIN★* matrix prose ("constructive precondition (canonical shape); see ... prose below").

**Problem**: This is the anti-bloat pattern "two paragraphs in different sections say the same thing" compounded with deferral chains (the K.μ⁻ box defers the equivalence "below," the matrix cell defers to the prose "below," the prose restates the box). A reader tracing what K.μ⁻ does to V-positions must reconcile four descriptions of one mechanism. The note carries `review-mode.anti-bloat`; this is exactly the accretion it targets.

**Required**: State the contraction shape once (in the K.μ⁻ box), keep the equivalence proof as the *only* expansion, and replace the K.μ⁻ amendment box and matrix prose with one-line pointers rather than re-descriptions.

### Issue 3: NodeBaptism axiom is surrounded by rationale and restated, mixing "why" with "what"
**ASN-0047, *Elementary transitions* (NodeBaptism, NodeRootedForest, SSGU) and Properties Introduced**: NodeBaptism's content (freshness `e ∉ Σ.E`, lineage `n₀ ≼ e`) is followed immediately by NodeRootedForest "Derived structure" and the SSGU paragraph, both heavy with non-circularity/why prose ("prefix-nesting (NodeLineage) being not `inc`-descent — remains an independent `inc`-root"; "Cross-node distinctness ... is not a within-subtree GlobalUniqueness consequence; it is discharged by SSGU below"), and the axiom is then restated again in the Properties-Introduced table.

**Problem**: This matches two flagged patterns: "new prose around an axiom explains why it's needed rather than what it says," and the same axiom content appearing in multiple places. The load-bearing facts SSGU actually uses (T10, CrossNodeAccountBase) are derived elsewhere; the inline prose largely re-argues why the forest structure is sound rather than advancing a claim.

**Required**: Reduce NodeRootedForest/SSGU to the minimal derived statement each downstream proof consumes (cross-node distinctness via CrossNodeAccountBase/T10), and drop the self-justifying non-circularity asides. Do not also restate NodeBaptism's conjuncts in the Properties-Introduced table beyond a one-line pointer.

### Issue 4: "V-position depth (operational)" and "Clause (i)'s scope" carry defensive essay prose in structural slots
**ASN-0047, *Elementary transitions* (V-position depth) and *Decomposition of K.μ~* (clause (i) scope)**: The "V-position depth (operational)" paragraph mixes the definition of `m_S(d)` with rationale ("This live-depth rule governs both subspaces uniformly ... re-pins `m_S(d)` from scratch — at any value ≥ 2 by S8a, not necessarily the prior depth"). The K.μ~ admissibility passage inserts "**Clause (i)'s scope** is the arrangement-*shape* package only — a constraint on which V-position *domains* exist, not on which I-address each position carries" followed by a defensive enumeration of the two obligations "outside it."

**Problem**: These are defensive justifications occupying definitional/structural slots — the reader must skip past scope-disambiguation prose to reach the operative content. The re-pin semantics is genuinely informative and should stay; the surrounding "governs uniformly"/"not necessarily the prior depth" framing and the clause-(i)-scope defense are meta-prose.

**Required**: Keep the definition of `m_S(d)` and the single substantive fact (re-pin can change depth); cut the uniformity/defensive framing. Fold the clause-(i) scope note into the clause statement itself rather than as a separate defensive paragraph.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link-arrangement contraction
**Why out of scope**: The gap between suffix-only K.μ⁻ and the implementation's compacting interior `DELETEVSPAN` is already an Open Question and concerns a named-operation mechanic (DELETEVSPAN), which the Scope section excludes. It belongs in a future operation-level ASN, not as a revision here.

VERDICT: REVISE
