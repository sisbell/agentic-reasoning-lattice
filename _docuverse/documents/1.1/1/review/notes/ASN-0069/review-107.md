# Review of ASN-0069

I read the full derivation and checked the proofs: the identity inductions (V1), the K.δ/K.μ⁺/K.ρ composite verification, the correspondence and provenance claims (V8, V9, V12), and the empty-source and chain cases (V7, V10, V11). The technical content is sound — boundary cases (empty content subspace, sibling forks, fork-of-fork, post-fork source deletion) are handled, `n = |ran(M'(d_new))|` correctly counts distinct I-addresses against S5's within-document sharing, and the ValidComposite★ coupling discharges are complete in both the populated and K.δ-alone branches. I found one precision defect and one accretion item.

## REVISE

### Issue 1: "owning document is implicit in M(d)(v)'s second argument" is incorrect
**ASN-0069, §"The Arrangement Layer"** (paragraph after V4): "they do not encode the owning document — the owning document is implicit in `M(d)(v)`'s second argument — so nothing about a V-position needs to change when it appears in `d_new`'s arrangement."

**Problem**: The owning document is the parameter `d` selecting the arrangement `M(d)`. In the application `M(d)(v)` the two tumblers are the V-position `v` and the I-address `a = M(d)(v)`; neither is `d`. There is no "second argument" that encodes the owning document. A precise reader stumbles here: the phrase points at the wrong object to carry the claim. This matters because the sentence is the load-bearing justification for *why* V-positions can be inherited literally (V4's identity-`φ` commitment).

**Required**: State it directly — the owning document is the parameter `d` of `M(d)`, not encoded in the tumbler `v`; therefore the same V-position tumbler may serve as a key in `M(d_op)` and `M(d_new)` independently.

### Issue 2: V9a's V9b carve-out is folded-in defensive prose
**ASN-0069, §"Provenance Recording"**, V9a: "Direct allocation is excluded from this enumeration: V9b establishes `origin(a) ≠ d_new` for every fork-recorded pair, so `d_new` provably did not allocate `a` itself. The indistinguishability of V9a thus ranges only over the acquisition paths that remain possible — fork and transclusion — not over a path V9b has ruled out."

**Problem**: V9a's core claim is that the acquisition path is not reconstructable from `R`. The trailing two sentences are a reconciliation between V9a and the later V9b — the shape of a prior finding's content folded back into the statement rather than the statement standing on its own. The carry of `origin(a) ≠ d_new` belongs in V9b (where it is proved); V9a only needs to name its quantifier domain.

**Required**: Reduce the carve-out to a single clause ("over the fork/transclusion paths, not direct allocation — see V9b") or drop it; let V9b own the `origin(a) ≠ d_new` fact without V9a re-narrating the interaction.

## OUT_OF_SCOPE

### Topic 1: Forking a transcludent source (`M(d_src)` references I-addresses with `origin ≠ d_src`)
**Why out of scope**: Correctly deferred to the Open Questions. V12(d) and V9b already behave correctly for such content (P4★ bounds containment regardless of origin), so no revision is needed here; the deeper invariants are future territory.

VERDICT: REVISE
