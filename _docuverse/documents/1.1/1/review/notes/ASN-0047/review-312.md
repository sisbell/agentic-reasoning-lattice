# Review of ASN-0047

I checked the transition model end-to-end: the five-component state, the seven elementary transitions plus the K.μ~/J4 composites, the Class (a)/(b) invariant induction, the wp-derived couplings, and all five worked examples. The correctness machinery is sound — the boundary cases I probed (empty-document contraction, full-clearance reordering, interior replacement, transclusion multiplicity, node-nesting disjointness, front-insertion reachability) are all either handled or correctly excluded by precondition. D-CTG★/D-MIN★ tiling is enforced by precondition and demonstrated satisfiable in the examples; referential integrity survives transclusion; the FrontierEquivalence and CrossDocEntityDisjoint proofs are complete. Standard 6 (depth) is met: real wp analysis, five concrete examples, derived consequences (P3, temporal decomposition).

The findings below are the meta-prose / forward-reference accretion patterns the active `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: Prose justifying document placement
**ASN-0047, "Link-subspace ownership" → Link V-position permanence**: "(This concerns a K.μ⁻ + K.μ⁺_L composite, not the K.μ~ named composite of *Decomposition of K.μ~*; it is recorded here, alongside CL-OWN/CL-UNIQ and K.μ⁺_L, because the guarantees it tests are link-subspace ones.)"
**Problem**: This is the flagged "prose justifies document ordering" pattern. The parenthetical explains *why the paragraph sits where it sits* rather than advancing the claim. A reader following the link-permanence guarantee must skip past it.
**Required**: Delete the placement rationale. If the K.μ⁻ + K.μ⁺_L (vs. K.μ~) distinction is load-bearing, state it as a one-clause fact ("Re-seating uses K.μ⁻ + K.μ⁺_L, not K.μ~"); drop the "it is recorded here ... because" framing.

### Issue 2: Structural-process prose in lemma/definition slots
**ASN-0047, "Decomposition of K.μ~" → LRP**: "A direct consequence of the full-clearance form, isolated here as a single named fact so it is proved once and cited rather than re-derived"
**ASN-0047, ValidComposite★ definition**: "This is the full statement of ValidComposite★, now that J1★, J1'★, and the K.μ~ decomposition convention are in hand."
**Problem**: Both clauses describe the document's own bookkeeping ("isolated here ... so it is proved once and cited", "now that ... in hand") rather than stating what LRP/ValidComposite★ *say*. This is the "new prose explains why it is needed rather than what it says" pattern. LRP's actual content ("full-clearance leaves every link-subspace V-position in place with its value") is what the reader needs; the reuse-justification is noise.
**Required**: For LRP, lead with the statement and drop "isolated here as a single named fact so it is proved once and cited rather than re-derived." For ValidComposite★, drop "now that J1★, J1'★, and the K.μ~ decomposition convention are in hand" — the dependencies are visible from the references inside the statement.

## OUT_OF_SCOPE

### Topic 1: Interior link-arrangement contraction with renumbering
**Why out of scope**: K.μ⁻ models suffix-removal only; interior withdrawal-with-compaction (the implementation's `DELETEVSPAN`) is a distinct contraction operation. The ASN correctly defers this to a future ASN — it is already an explicit Open Question, not a gap in the present transition vocabulary.

### Topic 2: Type-only / one-sided link admissibility
**Why out of scope**: Whether K.λ should require `e₁ ∪ e₂ ≠ ∅` and the semantics of empty from/to endsets is new territory flagged in the Open Questions; the current K.λ (requiring only `e₃ ≠ ∅`) is internally consistent.

VERDICT: REVISE
