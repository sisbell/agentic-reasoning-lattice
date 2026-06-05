# Review of ASN-0113

The core query — its precondition (W-pre), return type (W0), the per-subspace extent span (W2/W3), exact coverage (W4), confinement/disjointness (W10/W11), and the partition/independence invariants (W15/W16) — is rigorously argued, with non-vacuous worked instances at `m_S = 2` and `m_S = 3` that genuinely exercise the T5 prefix-confinement step. The unallocated-vs-allocated-empty distinction is handled carefully. Two accuracy issues remain.

## REVISE

### Issue 1: W12's "symmetric witness" claim contradicts the ASN's own content/link coupling asymmetry
**ASN-0113, "What the pair reveals…" (W12 proof)**: "The symmetric witness (fix the link extent, vary the text extent) is identical with the roles exchanged."

**Problem**: The construction is explicitly *not* symmetric, and the ASN says so two sentences earlier. A text position is added by a *coupled* `K.α + K.μ⁺ + K.ρ` composite that must discharge J0 ∧ J1★ ∧ J1'★; a link position is added by an *uncoupled* `K.λ + K.μ⁺_L` composite where the provenance couplings are vacuous. To fix the link extent and vary the text extent, one uses the *same two recipes* — coupled content composites for text, uncoupled link composites for links — merely changing which count varies. There is no "role exchange": content cannot be inserted by the link mechanism, and the asymmetry (content bound to provenance, links not) is precisely what the surrounding paragraph establishes. Calling the second witness "identical with the roles exchanged" papers over the asymmetry the proof itself relies on.

**Required**: Rephrase to state the symmetric *proposition* is witnessed by the same construction with the varying axis changed (coupled content composites driving `n_{s_C}` to `c₁`/`c₂`, uncoupled link composites holding `n_{s_L} = k`), not by exchanging the content and link mechanisms.

### Issue 2: W5 biconditional statement is quantifier-ambiguous relative to its proof
**ASN-0113, W5 (table) and "Exactness is contingent on contiguity"**: "a single level-uniform span `σ` of subspace `S` at depth `m` satisfies `⟦σ⟧ ∩ VSlice(S, m) = V_S(d)` *if and only if* `V_S(d)` is contiguous."

**Problem**: As written with `σ` introduced as a fresh span, the biconditional is ill-formed: the forward direction needs an *existential* (`contiguous ⟹ ∃ exact σ`, since a badly chosen `σ` is inexact even when `V_S(d)` is contiguous), while the converse needs a *universal* (`¬contiguous ⟹ ∀σ inexact`). The proof body in fact proves the clean statement "(∃ a single exact span) ⟺ contiguous," but the headline claim does not say "exists."

**Required**: State W5 as "there exists a single level-uniform span exactly covering `V_S(d)` iff `V_S(d)` is contiguous," matching the forward/converse structure of the proof.

## OUT_OF_SCOPE

The six Open Questions (non-contiguous fragmentation reporting, consumer interpretation of an omitted member, version-fork permanence, transclusion stability, consistency with the single overall extent, and extending the subspace convention) are correctly left undefined — each is future territory, not a defect here. None is flagged: the ASN states them as questions rather than asserting claims about them.

VERDICT: REVISE
