# Review of ASN-0091

This note's reasoning is largely sound — the abstract/concrete split is clean, the per-invariant discharge is non-circular (shape package from RA-dom → clauses (i)–(v) → ExtendedReachableStateInvariants), and the worked examples genuinely exercise distinct mechanisms (R-PPERM, R-SPERM, R-EXT, bijection non-uniqueness). All cross-ASN references are to foundation ASNs, so the self-containment rule is satisfied. The findings below are accumulated meta-prose around forward references and case-splits, consistent with the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Repeated downstream pointers to the same worked examples
**ASN-0091, multiple sections**: The abstract section says bijection non-uniqueness is "concretely realised in the 'Worked Example — Bijection Non-Uniqueness Under Shared I-Addresses' below"; "Where Position Lives After Rearrangement" repeats "exhibited concretely in the 'Worked Example — Bijection Non-Uniqueness...' trace below"; the RE-ext section says it "is exercised concretely in the third Worked Example ('Interior Cuts (R-EXT Exercised)') below"; RE-sub carries an analogous pointer.
**Problem**: Multiple paragraphs in different sections defer to the same downstream worked examples — the use-site-inventory / downstream-pointer pattern. The worked examples already announce which RE-* claim they exercise; the upstream sections do not need to forward-reference them.
**Required**: Delete the forward pointers from the claim-introduction prose. The worked example headings already carry the cross-reference in the right direction.

### Issue 2: Defensive clarification and redundant derivation in the collapse-case split
**ASN-0091, "REARRANGE as Vstream-Only Operation"**: "Neither case should be conflated with the domain-cardinality bound `|dom_C(M(d))| ≥ 2`, which R-PRE(iv) ∧ CS2 force ... That bound counts *positions*, not distinct I-addresses..."
**Problem**: This paragraph defends against a confusion the preceding text does not invite — a defensive justification rather than an advancing step. Separately, the collapse-case derivation "RA-π under this π together with RA-dom gives Σ'.M(d) = Σ.M(d) as partial functions" is redundant: the collapse case is *defined* by `M'(d) = M(d)`, which is already `Σ'.M(d) = Σ.M(d)`; RA-frame then gives `Σ' = Σ` directly.
**Required**: Drop the "Neither case should be conflated" paragraph. In the collapse case, conclude `Σ' = Σ` from the case definition plus RA-frame without re-deriving the arrangement equality through RA-π.

### Issue 3: Roadmap prose and bidirectional-discharge duplication
**ASN-0091, "REARRANGE_K Realises the Abstract Class"**: "The realisation involves two layers of obligation: first, each definitional clause ... must be discharged ...; second, every foundation invariant must be preserved." Followed by the "K.μ~ Admissibility Clauses" bullet list (RA-reg ← ..., RA-π ← ..., etc.) and then the "Forward Direction" subsection closing clauses (i)–(v).
**Problem**: The opening sentence is scaffolding that restates the section structure. The RA-* ← K.μ~ bullet list and the Forward Direction subsection both narrate the two-directional correspondence; the bidirectional framing is explained more than it is used.
**Required**: Cut the "two layers of obligation" sentence. Keep one discharge direction as a list and the reverse as a list; remove the connective prose explaining that there are two directions.

### Issue 4: Duplicate closing paragraphs in RE-sub and RE-ext
**ASN-0091, "Subspace Frame" and "In-Subspace Exterior Frame"**: RE-sub closes with "RE-sub is REARRANGE_K-specific: a different concrete realization of the abstract class could non-trivially permute the link subspace while satisfying RE-subpres ... and still meet RA-adm." RE-ext closes with "Like RE-sub, RE-ext is REARRANGE_K-specific: a different concrete realisation of the abstract class could non-trivially permute the in-subspace exterior while preserving the affected range's image and the cut-subspace identity, and would still satisfy RA-adm."
**Problem**: Two paragraphs in different sections say the same thing in different words (one about the non-cut subspace, one about the in-subspace exterior). The "REARRANGE_K-specific vs abstract" point is identical.
**Required**: State the "pointwise fixity is REARRANGE_K-specific, not abstract" observation once, covering both the non-S subspace (RE-sub) and the in-S exterior (RE-ext) together.

### Issue 5: Document-organization framing in the unified-state subsection
**ASN-0091, "Unified-State Identification E_doc = dom(M)"**: "The unified state model adopts this identification as a *definitional convention* — neither ASN's isolated formulation carries both names — and the two registering operations must each maintain it."
**Problem**: This sentence justifies why the convention is adopted and notes how the source ASNs differ — organizational meta-prose. The substantive content (verifying K.σ and K.δ both extend `dom(M)` and `E_doc` by the same singleton) follows and is fine.
**Required**: Open the subsection with the identification itself and the joint-extension verification; drop the sentence explaining that neither source ASN carries both names.

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics
The note hardcodes the cut subspace to `S = s_C` (CS3) and leaves link-subspace reordering to a future ASN. This is correctly listed as an open question, not a gap in this note.

### Topic 2: Upper bound on run-decomposition cardinality increase
RE-frag establishes increase is possible but not bounded. The note explicitly declines to bound it (open question). Appropriate to defer.

VERDICT: REVISE
