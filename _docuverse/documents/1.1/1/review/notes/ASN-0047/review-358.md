# Review of ASN-0047

This ASN carries the `review-mode.anti-bloat` classifier, so my findings concentrate on forward-reference accretion and redundant meta-prose. I checked the correctness spine (the K.δ allocation dispatch, the K.μ⁻ constructive/post-state equivalence, the K.μ~ full-clearance decomposition with LRP/link-fixity, the per-state vs composite-boundary invariant split, and the worked examples' arithmetic) and found it sound — the issues below are presentation-level, but they are the specific noise this review pass is meant to remove.

## REVISE

### Issue 1: Elementary K.μ⁻ box carries dual forward-deferral and references D-SEQ★ before it exists
**ASN-0047, *Elementary transitions*, K.μ⁻**: the precondition prose contains two parenthetical pointers forward:
- "(The per-subspace generalization to the extended state … is given in *K.μ⁻ amendment (PerSubspaceScope)* below.)"
- "the per-subspace generalization and its full equivalence proof are given in *K.μ⁻ admissible contraction shape* below."

**Problem**: A single elementary definition defers forward to two distinct downstream sections, and the first parenthetical names **D-SEQ★** — an invariant not introduced until the *Amendments to existing transitions* section that follows. The reader meeting K.μ⁻ for the first time must hold two unresolved forward pointers and one undefined symbol to read a definition that is otherwise self-contained at the elementary (content-only) level. This is the forward-reference accretion pattern: prose that justifies where the *rest* of the account lives rather than advancing the elementary definition itself.

**Required**: Drop the two parenthetical deferrals from the elementary box (the *PerSubspaceScope* and *admissible contraction shape* sections stand on their own and are reached in document order). State the elementary precondition purely in ASN-0036's D-SEQ/D-CTG/D-MIN terms, without naming the starred forms.

### Issue 2: Full-clearance realization stated twice
**ASN-0047, *Decomposition of K.μ~***: the "Full-clearance form (canonical statement)" paragraph says K.μ⁻ "clears the entire content subspace … while retaining every link-subspace position pointwise, and K.μ⁺ rebuilds the content subspace at fresh positions, framing the retained link positions." The later "Decomposition" paragraph restates the same: "the full-clearance form (`n'_{s_C} = 0`) covers every admissible π; for a given π its concrete realisation is the write set `{π(v) ↦ M(d)(v) : v ∈ V_{s_C}(d)}`. The retention of link-subspace mappings under the clearance is the clause-(v) discharge."

**Problem**: Two paragraphs in the same section describe the K.μ⁻+K.μ⁺ full-clearance realization in different words. The second adds only the write-set spelling already implied by the bijection equation. This is the "two paragraphs say the same thing" pattern.

**Required**: Fold the write-set spelling into the canonical-statement paragraph and delete the redundant "Decomposition" restatement, keeping only its genuinely new content (the *Intermediate-state admissibility* discharge).

### Issue 3: S8★ content/link split narrated before it is performed
**ASN-0047, *S8★ (per-subspace span decomposition)***: the introductory paragraph already walks the content-vs-link condition-(c) split in full ("For the content subspace, the partition together with conditions (a) and (b) *and* condition (c) is exactly ASN-0036's S8 … Only the link-subspace projection omits (c) …"), and then the two bullets ("*Content subspace.*" / "*Link subspace.*") perform that same split again with the actual discharge.

**Problem**: The prose introduction restates the per-subspace routing that the bullets then carry out, so the reader reads the content/link distinction twice before reaching the one copy that does the work.

**Required**: Compress the introduction to the bare claim (per-subspace decomposition exists, content via ASN-0036 S8, link via length-1 decomposition with (c) dropped) and let the bullets supply the discharge once.

## OUT_OF_SCOPE

The topics a reader might flag as "missing" — interior (renumbering) link withdrawal, link-specific sequential invariants beyond D-SEQ★, link-endset provenance permanence, address-space exhaustion, and concurrent same-document allocation — are already carried as Open Questions and correctly belong to future ASNs, not to this one. No additional out-of-scope topics to record.

VERDICT: REVISE
