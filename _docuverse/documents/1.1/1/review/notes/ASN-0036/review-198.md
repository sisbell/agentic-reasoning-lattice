# Review of ASN-0036

## REVISE

### Issue 1: S5 treats transition invariants S0/S1 as state predicates, and the rescue is misjustified
**ASN-0036, Sharing (S5), proof, "Shared facts"**: "S0 (content immutability) and S1 (store monotonicity) are transition invariants; a single-state witness satisfies them vacuously under the identity transition `Σ → Σ`, which preserves `dom(C)` and every stored value."

**Problem**: Two defects in one sentence.
1. The existential `(E Σ :: Σ satisfies S0–S3 ∧ …)` is not well-typed for S0 and S1. S2 and S3 are evaluable on a single state, but S0/S1 are quantified over *transitions* `Σ → Σ'`. "Σ satisfies S0" has no meaning without naming a transition.
2. "vacuously" is the wrong logical term. Under `Σ → Σ`, S0's antecedent `a ∈ dom(Σ.C)` is **true** for the constructed `a`, and the consequent holds because the value is unchanged — that is trivial/reflexive truth, not vacuous truth (which requires a false antecedent). Worse, the proof invokes "the identity transition `Σ → Σ`" without establishing that a no-op is in the system's transition vocabulary; if transitions are editing operations, identity need not be admissible.

**Required**: Either (a) state explicitly that S5 demonstrates only that the *state-level* invariants S2, S3 admit unbounded multiplicity, observing that S0/S1 are transition-level and impose no constraint on a standalone state; or (b) exhibit `Σ_N` as a reachable state and verify S0/S1 over a genuine admissible transition into it. In either case replace "vacuously."

### Issue 2: S7b carries "why the axiom is needed" prose in an axiom slot
**ASN-0036, Structural attribution (S7b)**: "This is a design requirement: content resides at the element level… **Node, user, and document-level tumblers identify containers, not content.** By T4's field correspondence, `zeros(a) = 3` means all four identifying fields…"

**Problem**: The note carries the `review-mode.anti-bloat` classifier. The bolded clause is rationale (why element-level was chosen), not a statement of what the axiom asserts. The axiom already says `zeros(a) = 3`; the container/content gloss is the kind of justify-the-axiom prose that accretes across cycles. A reader following the chain must skip past it.

**Required**: Drop the container/content sentence (or relegate it to the section's Nelson-intent prose). Keep only the axiom statement and the T4 field-correspondence consequence that is actually used.

## OUT_OF_SCOPE

### Topic 1: Operation-layer preservation of D-CTG/D-MIN/S2 under INSERT/DELETE/COPY/REARRANGE
**Why out of scope**: D-CTG, D-MIN, D-SEQ are imposed here as well-formedness *constraints*; whether each editing operation preserves them is explicitly deferred (Open Questions) and operation frame conditions are listed OUT OF SCOPE. The base (empty) case is correctly checked here.

### Topic 2: Contiguity for non-text subspaces (links, subspace 2)
**Why out of scope**: D-CTG/D-MIN/D-SEQ are deliberately scoped to `V_1(d)`; S8's run partition already covers all subspaces without contiguity. Links/endsets are out of scope.

VERDICT: REVISE
