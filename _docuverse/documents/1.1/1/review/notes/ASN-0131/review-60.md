# Review of ASN-0131

This note defines a pure query `RE(W, d, Σ)` that surfaces touching endsets over a content region without naming links. I checked the substantive proofs — RE-DEF/RE-SND/RE-CMP (definitional reads), RE-UDIST and its one-sided intersection law plus the non-injective counterexample, the worked instance, RE-ADDR's antichain argument, RE-CWP's weakest precondition, and RE-RET's "sole addressable bearer" derivation — and they are sound. The decidability argument correctly tests the finite image against (possibly infinite) coverage rather than enumerating coverage; the field-agreement argument for type/retraction content-disjointness is rigorous and correctly scoped to unit-depth spans; the boundary cases (empty image, no addressable links, empty slot, R = ∅) are handled. No correctness defect found. The findings below are placement/precision, in line with this note's anti-bloat mandate.

The note correctly cites ASN-0127's image and existence/discovery machinery rather than rebuilding it, and defines no claims for the out-of-scope operations (counting, pagination, READLINK, etc.) — so there are no OUT_OF_SCOPE items.

## REVISE

### Issue 1: Import-licensing infrastructure front-loaded before the central definition

**ASN-0131, "The unit of the answer: anchoring without names"**: the two paragraphs preceding RE-DEF (the `Σ.L`-evolution bridge and "One consequence of that shared K.λ semantics recurs…" deriving RE-ADDR), plus: "We import only a handful — R0a/FlatLinkDomain, R-Scope (SingleTupleScope), R6a (RetractionStability), and the computability of `nullified` (all ASN-0086) — and the bridge licenses each here."

**Problem**: ~450 words of cross-ASN reachability plumbing precede RE-DEF, the note's central object. Of the imports, only `nullified`'s well-definedness is consumed at definition time (RE-DEF's `addressable`, and the immediately-following decidability paragraph). RE-ADDR's first use is the intersection counterexample in "Composing regions"; R-Scope and R6a are first used in "Under retraction" (Stability). So RE-ADDR and the R0a/R-Scope/R6a citations are infrastructure pulled forward of their use sites. The "We import only a handful — [list] — and the bridge licenses each here" sentence is precisely the flagged use-site-inventory pattern.

**Required**: Keep the bridge's licensing near RE-DEF (it grounds `nullified`), but relocate the RE-ADDR derivation and the R0a/R-Scope/R6a citations to their consuming sections (Composing regions / Stability), citing each lemma where it is used rather than pre-inventorying them.

### Issue 2: An excluded case explored inline, duplicating Open Question 7

**ASN-0131, "Under retraction"**: "(This content-disjointness is exactly what the standing `W ⊆ s_C` obligation buys. Were the region drawn from the link subspace instead — `W ⊆ s_L`, resolving by S3★ (ASN-0047) to an image `I ⊆ dom(Σ.L)` — the to-set `{(ℓ, δ(1, #ℓ))}` … could meet that image, and retraction stability would acquire an extra surfacing term for the emitter `b`; that case lies outside the content-region scope of this note and is reopened as Open Question 7.)"

**Problem**: The caller obligation fixes `W ⊆ s_C`, so the explored `W ⊆ s_L` scenario is excluded by the operation's own precondition — and it is already reopened verbatim as OQ7. The detailed walk-through (image meeting the to-set, "extra surfacing term") is an excluded-case exploration that duplicates the open question.

**Required**: Keep the load-bearing point — the retraction to-set is content-disjoint, which is what `W ⊆ s_C` secures — and drop the `W ⊆ s_L` exploration, letting OQ7 carry the link-subspace question.

### Issue 3: Permanence claim cites the single-step lemma, not the multi-step one

**ASN-0131, "Anchoring reached through borrowed content" (RE-IDENT, body and table)**: "no transition alters an endset's coverage (LP3, ASN-0098), so once an endset is surfaced the I-addresses it anchors are a fixed fact about a permanent link."

**Problem**: The conclusion ("a fixed fact," invariant across all states in which the link exists) is an across-reachable-sequence claim, but LP3 (CoverageInvariance) is single-transition. The foundation supplies LP3★ (MultiStepCoverageInvariance) for exactly this permanence statement.

**Required**: Cite LP3★ for the permanence claim (in both the prose and the RE-IDENT table row), or make the per-step LP3 + induction step explicit.

## OUT_OF_SCOPE

(none — the note cites ASN-0127's region/taxonomy machinery rather than rebuilding it, and defines no claims for the listed out-of-scope operations.)

VERDICT: REVISE
