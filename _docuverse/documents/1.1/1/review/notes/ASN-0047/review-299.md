# Review of ASN-0047

I read the ASN on its own terms and checked the proofs, boundary cases, and — per the `review-mode.anti-bloat` classifier on this note — the forward-reference / meta-prose patterns it asks me to surface. The core argument (the three-layer mutability hierarchy, the per-elementary preservation matrix, the K.μ~ decomposition and its admissibility clauses, the coupling-constraint wp derivations, and the worked traces) is rigorous and I found no substantive correctness gap. The findings below are the anti-bloat patterns this note is explicitly tasked to flag.

## REVISE

### Issue 1: Redundant deferral — the K.μ~ shape-package discharge is pointed to from both the matrix and the prose
**ASN-0047, Class (a) verification matrix and the per-invariant prose that follows it**: The K.μ~ column carries `"per *K.μ~ discharge for the arrangement-shape package* below"` in four cells (S8a/S8-depth/S8-fin, S8★, D-CTG★/D-MIN★, D-SEQ★). The matching prose paragraphs each then *repeat the same pointer* — e.g. S8★ prose `"(K.μ~ is discharged at *K.μ~ discharge for the arrangement-shape package* below.)"`, D-CTG★/D-MIN★ prose `"(K.μ~ is discharged at ... below.)"`, D-SEQ★ prose `"(The K.μ~ instance at Σ' is discharged at ... below.)"`, S8a prose `"(K.μ~ ... is discharged at ... below.)"`.

**Problem**: This is exactly the flagged pattern "multiple paragraphs in different sections defer to the same downstream location." Eight pointers resolve to one consolidation section, and the four prose parentheticals add nothing the four matrix cells did not already say — the reader hits the same "see below" twice per invariant.

**Required**: Keep the deferral in one place. The matrix cell is the natural home (the matrix is declared the navigational index); drop the duplicate parenthetical from each prose paragraph, or vice versa, but not both.

### Issue 2: Use-site inventory in a lemma's introduction
**ASN-0047, *Allocator hierarchy under documents*, CrossDocEntityDisjoint introduction**: "We abbreviate this lemma **CrossDocEntityDisjoint** ... The Class (a) S4 and S7d verification annotations below cite this lemma rather than re-deriving it."

**Problem**: This is a downstream-consumer inventory in a structural slot — the introduction enumerates where the lemma is later cited rather than advancing the lemma's content. The S4 and S7d cells/prose already cite CrossDocEntityDisjoint, so the inventory is the wrong-direction pointer.

**Required**: Delete the sentence. The cite sites already name the lemma; the lemma need not announce its consumers.

## OUT_OF_SCOPE

None. The Open Questions already correctly defer renumbering-aware contraction, transclusion-chain provenance, concurrency, and node-baptism protocol mechanics to future ASNs.

VERDICT: REVISE
