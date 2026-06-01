# Review of ASN-0047

## REVISE

### Issue 1: "Why-needed" rationale prose around K.δ conjuncts does not advance the spec

**ASN-0047, *Elementary transitions*, K.δ "Rationale (k = 0 conjuncts)"**: "The `¬IsNode(t)` conjunct is required for `parent(t)` to be defined — T4b's parent projection is partial on T and undefined when `IsNode(t)`. The freshness conjunct `inc(t, 0) ∉ E` is the case-level `e ∉ E` specialised to `e = inc(t, 0)` — stated locally to record that the caller's operand selection must observe it."

**Problem**: This is a `review-mode.anti-bloat` pattern — prose that explains *why a conjunct is present / stated here* rather than what the operation does. The precondition already lists `¬IsNode(t)` and `inc(t,0) ∉ E`; the K.δ-ID identities and FrontierEquivalence already carry the load. The rationale paragraph is skippable: a reader following the precondition gains nothing from being told the conjunct "is stated locally to record" a caller obligation. The same pattern recurs in the L1c discharge ("Allocator-activation discharge for the anchor traversal and first emission goes through SubAllocatorAxiom; T10a's full discipline applies only to subsequent emissions...") — justifying which mechanism applies where rather than stating the chain.

**Required**: Delete the "Rationale" paragraph (the conjuncts stand on their own; FrontierEquivalence already supplies the operative equivalence). In L1c, state the inc-chain conformance directly and drop the meta-commentary on which discharge route applies to which segment.

### Issue 2: Two cross-layer properties stated in one section, proved in another, with explicit deferral prose

**ASN-0047, *Cross-layer invariants* (P7a) and the P4a definition near the J-couplings**: P7a — "P7a is a composite-boundary property (Class (b)), not preserved by each elementary transition; its proof is given once under Class (b) in the *Extended reachable-state invariants* section." P4a — "P4a is a composite-boundary property (Class (b)); its derivation by induction with J1'★ as the coupling is given once under Class (b)."

**Problem**: This is the "multiple paragraphs in different sections defer to the same downstream location" accretion pattern. Both P4a and P7a are *stated* in body sections but their proofs are deferred to the Class (b) block, each with a navigational sentence. The reader must hold the statement, skip to Class (b), and return. S8★ and S3★-aux carry similar "discharged as per the dedicated paragraph" deferrals. The deferrals compound: the document now has the statement, the deferral pointer, and the proof in three locations for these properties.

**Required**: State P4a and P7a once, at the point of proof (Class (b)), with a one-line forward reference from the Cross-layer section if needed for narrative — not a statement-plus-deferral-paragraph in both places. Collapse the duplicated framing ("is a composite-boundary property (Class (b))") that appears at both the statement site and the proof site.

### Issue 3: Worked-example enumeration of excluded attempts is reviser-drift

**ASN-0047, *Worked example: entity hierarchy by K.δ*, closing paragraph**: "A second K.δ case (i) attempting to re-baptise `1.2` is excluded by `e ∉ E`; a K.δ case (i) attempting to baptise a disconnected node `2.1` is excluded by `n₀ ≼ e`. A second Step 4 attempting `inc(1.2.0.1.0.1, 0)` again is excluded by `inc(t, 0) ∉ E₄`..."

**Problem**: This paragraph imagines three transitions the preconditions already exclude and walks through each exclusion. It adds no reasoning the precondition list does not already carry — it is the "paragraph imagines a case the claim's precondition already excludes" drift pattern. A reader who understands the guards does not need them re-applied to invented non-firing attempts.

**Required**: Remove the enumeration. If a single illustration of guard-biting is wanted, keep one line, not three.

## OUT_OF_SCOPE

### Topic 1: Version-DAG branching semantics (forking a non-frontier version)

**Why out of scope**: The fork definition admits versions on a single `A_v(d_src)` chain plus nested `A_v(version)` forks, which suffices to *support* a version DAG, but the invariants governing the DAG's branching structure (e.g., what relationship a fork-of-a-fork must bear to the common ancestor's arrangement) are correctly deferred — the ASN's Open Questions already name "relationship between a document's version lineage and its sequence of arrangement transitions." New territory, not an error here.

### Topic 2: Interior link withdrawal / tombstoning mechanism

**Why out of scope**: D-CTG★/D-MIN★ confine K.μ⁻ to link-subspace suffix truncation, so withdrawing an interior link requires a mechanism outside K.μ⁻'s contract. The ASN flags this in Open Questions rather than specifying it. Correctly deferred to a future operations ASN.

VERDICT: REVISE
