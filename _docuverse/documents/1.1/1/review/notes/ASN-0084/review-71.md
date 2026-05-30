# Review of ASN-0084

## REVISE

### Issue 1: R-CS3 contains a rebuttal of a prior review rather than an argument

**ASN-0084, "Necessity of CS3" / R-CS3 proof, *CS3 is the sole rejecting clause***: "The previously-supposed redundancy of CS3 rested on R-PRE(iv) becoming *unsatisfiable* whenever a cut left subspace 1. That argument holds only when c₀ remains in subspace 1..."

**Problem**: This paragraph argues against a hypothesis ("the previously-supposed redundancy") that no reader of the note holds — it is a prior review finding's content relocated into the proof rather than removed. The lemma statement and the counterexample already establish that CS3 is load-bearing (the all-higher-subspace sequence satisfies CS1, CS2, CS4, R-PRE(i),(ii),(iv) vacuously and fails only CS3). The rebuttal adds no step to that argument; it defends a settled point against an absent interlocutor. This is exactly the reviser-drift pattern the anti-bloat classifier flags.

**Required**: Delete the "*CS3 is the sole rejecting clause*" rebuttal paragraph. The counterexample plus the region-collapse sentence (α = β = ∅, w_α = w_β = 0, non-degeneracy fails) already discharge the lemma. If the contrast with the c₀-in-subspace-1 case is genuinely informative, state it once as a positive observation, not as a refutation of a former claim.

### Issue 2: "Reduction of compound shifts" re-derives a fully general identity it already cites

**ASN-0084, "Reduction of compound shifts (R-P2, R-S2, R-S3)"**: "`c₀ + w_β + j = (c₀ + w_β) + j` (R-P2 and R-S2), by Extended Associativity with the outer pair (w_β, j)… The intermediate position `c₀ + w_β` has subspace S by OrdShiftHom (a), so the subsequent shift by j is again a valid OrdinalShift application…"

**Problem**: Extended Associativity is already stated as the general identity `(c + j) + k = c + (j + k)` for all `j, k ∈ ℕ`. The two bullets re-instantiate it at the specific destination expressions and wrap each instantiation in defensive subspace-validity prose. The header itself enumerates downstream consumers ("R-P2, R-S2, R-S3") — a use-site inventory rather than content that advances the identity. The R-S3 bullet's "first the outer pair… then the inner pair…" bookkeeping is a verbose unfolding of a one-line associativity instance.

**Required**: Collapse to a single sentence noting that the compound destinations `c₀ + w_β + j` and `c₀ + w_β + w_μ + j` are read left-associatively and equal the single-step shifts by Extended Associativity. Drop the per-bullet subspace-validity remarks (subspace preservation under shift is already a standing consequence under "Subspace confinement").

### Issue 3: Meta-commentary on derivation generality in Split/Merge

**ASN-0084, "Correspondence-Run Decomposition Transformation" / Split**: "The derivation quantifies over an arbitrary arrangement A, using only S8-cons of the original run and Extended Associativity; the same holds of the Merge derivation below."

**Problem**: This sentence describes the proof's own structure rather than advancing it, and forward-defers to the Merge derivation ("the same holds… below"). The Split and Merge derivations already exhibit their own quantification over A inline; the meta-summary is noise the reader must skip past.

**Required**: Remove the sentence. If parameterization over an arbitrary A is load-bearing for a later consumer, name that dependency at the consumer, not as a retrospective gloss here.

## OUT_OF_SCOPE

### Topic 1: Operational recovery of the canonical (maximal) partition

The note introduces Split and Merge and defers the actual confluent recovery of the S8-unique maximal partition to a future ASN (Open Question 6). This is correctly scoped: R-BLK only needs to produce a *valid* post-state partition B', and foundation S8 supplies the maximal partition's existence/uniqueness independently. The operational reduction is genuinely new territory.

### Topic 2: k-cut rearrangements for k > 4 and composition of rearrangements

Open Questions 1–2 (generalization beyond 4 cuts, closure of rearrangements under composition) are legitimate future work, not gaps in the depth-2, n ∈ {3,4} class this ASN defines.

VERDICT: REVISE
