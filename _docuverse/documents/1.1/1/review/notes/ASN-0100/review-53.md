# Review of ASN-0100

The operation is well-decomposed and the proofs are, in the main, complete: the three-region partition, the chain-shift identity (INS.chain-shift), the projection trace, and the per-state/boundary invariant split are all carried with real rigor. My findings are concentrated on accreted duplication and meta-prose — the patterns the `review-mode.anti-bloat` classifier targets.

## REVISE

### Issue 1: Functionality (S2) concluded twice in immediate succession
**ASN-0100, §Arrangement functionality (S2)**: "So `M'(d)` is a well-defined function." immediately followed by "The pairwise-disjoint, uniquely-defined regions just given establish that `M'(d)` is a function directly."
**Problem**: Two consecutive sentences assert the same conclusion from the same premise (pairwise-disjoint, uniquely-defined regions). The second adds nothing — it restates the first in different words. This is the "two paragraphs say the same thing" pattern at sentence granularity.
**Required**: Delete the second sentence (and the dangling "For other subspaces and other documents, `M'` equals `M`…" can attach to the first).

### Issue 2: M2-vs-C1a justification duplicated within §S8★
**ASN-0100, §Per-subspace span decomposition (S8★)**: The first paragraph already establishes "existence is supplied not by M2 (DecompositionExistence; ASN-0058) — which is stated for whole arrangements — but by C1a (RestrictionDecomposition; ASN-0058)". The third paragraph re-explains the same point: "Restricting to the content subspace is essential here: M2 carries the precondition S3 (ReferentialIntegrity, ASN-0036), `ran(M(d)) ⊆ dom(C)`, which the whole extended-state arrangement fails whenever `V_{s_L}(d') ≠ ∅`… C1a ranges over the single content subspace…".
**Problem**: The reader is told twice, in different sections of the same proof, why C1a rather than M2 is the existence vehicle. The third-paragraph restatement is essay-style rationale for a lemma choice already made.
**Required**: State the M2-vs-C1a distinction once (the first paragraph is the natural home, since that is where existence is discharged) and drop the re-explanation.

### Issue 3: S8a-for-`shift(p,k)` derived in full in two sections
**ASN-0100, §Effect One/Two (Placement)** derives S8a in full — "The shift's tail component `p_{m_C} + k ≥ 1` then transfers S8a to `shift(p, k)`: zeros remain zero…, depth is preserved at `m_C ≥ 2`, all components remain strictly positive." — and **§Post-state V-position well-formedness (S8a bullet)** derives the identical fact again with a `k = 0` / `k ≥ 1` split.
**Problem**: The same S8a derivation (with citations to OrdAddHom/TumblerAdd) appears twice. The "Discovering the Three Effects" section is supposed to reason from intent to the formal effect; a fully-cited invariant proof there is verification content placed in a discovery slot, then repeated in the verification section. (Note §Atomicity step 3 handles this correctly — it *defers* to §Post-state rather than re-deriving.)
**Required**: In §Placement, state the placement effect and assert well-formedness with a pointer to §Post-state; keep the single full derivation in the verification section.

### Issue 4: Meta-label and use-site forward-pointer in the worked example
**ASN-0100, §A Worked Example**: the bolded inline heading "**Tightness precondition of the trace below, grounded in the example's substrate state.**" and the trailing sentence "This is the load-bearing assumption that makes `N_I = ∅` concrete via LP19a (TightFreshness; ASN-0098); we trace the non-tight alternative at the end of this example."
**Problem**: The concrete construction of `Σ_{e_1}` is load-bearing and should stay, but the bolded structural-slot label and the closing narration (announcing what the assumption is for and forward-pointing to the non-tight trace later in the same example) are meta-prose around the reasoning rather than the reasoning. The reader must step past the label and the "we trace … at the end" pointer to follow the actual derivation.
**Required**: Drop the bold label and the forward-pointing sentence; let the constructed `Σ_{e_1}` and the `tight(e_1, Σ_{e_1})` conclusion stand on their own. The non-tight alternative already announces itself where it appears.

## OUT_OF_SCOPE

(none — the link-subspace insertion, COPY, DELETE, version derivation, and replication topics are correctly fenced in §Bounding the Scope and the Open Questions, with no claims asserted for them.)

VERDICT: REVISE
