# Review of ASN-0047

## REVISE

### Issue 1: FrontierEquivalence mis-cited for k=2 spawns (and a node operand) in the entity-hierarchy worked example
**ASN-0047, *Worked example: entity hierarchy by K.δ*, Steps 2 and 3**: Step 2 — "`1.2.0.1 ∉ E₁` holds because this is the first `(1.2, 2)` spawn — freshness per the K.δ k = 2 at-most-once read (FrontierEquivalence)"; Step 3 — "`d ∉ E₂` holds because this is the first `(1.2.0.1, 2)` spawn — freshness per the K.δ k = 2 at-most-once read (FrontierEquivalence)".

**Problem**: FrontierEquivalence is stated *only* for the `(t,0)`-branch: "`inc(t, 0) ∉ Σ.E ⟺ t is the frontier of A's (t, 0)-branch`", and its hypotheses explicitly require `¬Node(t)`. Both cited steps are `k = 2` child-spawns, not `k = 0` sibling-advances, so the lemma does not apply. Worse, Step 2's operand is the node `1.2` (`Node(1.2)`), which violates FrontierEquivalence's `¬Node(t)` precondition outright. The K.δ box itself describes `k = 2` freshness differently — as a direct live-state read "logically equivalent to `inc(t, 2) ∈ Σ.E`" — not via FrontierEquivalence. (Step 4's `k = 0` citation, by contrast, is correct.)

**Required**: Replace the FrontierEquivalence citations in Steps 2 and 3 with the K.δ box's `k = 2` at-most-once live-state read (`inc(t, 2) ∉ Σ.E`), or with whatever lemma actually discharges child-spawn freshness (see Issue 2).

### Issue 2: child-spawn freshness equivalence (`k ∈ {1,2}`) asserted inline, never justified at FrontierEquivalence's standard
**ASN-0047, K.δ case (ii), k=1 and k=2 sub-cases**: "the case-level `e ∉ E` (with `e = inc(t, 1)`) *is* the enforcement of T10a's at-most-once-per-`(t, k')` discipline: it reads whether the spawn `(t, 1)` has already been performed, a fact logically equivalent to `inc(t, 1) ∈ Σ.E`" (and symmetrically for `k = 2`).

**Problem**: The biconditional "spawn `(t, k')` performed ⟺ `inc(t, k') ∈ Σ.E`" is asserted as "logically equivalent." Its forward direction is immediate (P1 persistence), but its reverse direction — that `inc(t, k')` could only have been produced by the `(t, k')` spawn and not by some other event — requires GlobalUniqueness / T10a.6, exactly the multi-step argument FrontierEquivalence proves for `k = 0`. The ASN invests a full lemma (with separate forward/reverse proofs) in the `k = 0` case but discharges the structurally identical `k ∈ {1,2}` cases with a one-sentence "logically equivalent." This is the gap that produced the Issue 1 mis-citation: there is no named lemma for child-spawn freshness to cite, so the worked example reached for the wrong one. "X is logically equivalent to Y" over a freshness predicate is a claim, not a derivation.

**Required**: Either generalise FrontierEquivalence to cover `inc(t, k') ∉ Σ.E` for `k' ∈ {1,2}` (the reverse direction reusing GlobalUniqueness/T10a.6 over the spawned child allocator's base), or add the one-line GlobalUniqueness justification inline so the equivalence is discharged rather than asserted — then cite that result, not FrontierEquivalence, in the worked example.

### Issue 3: duplicate deferral sentences for S3★ / S3★-aux preservation (anti-bloat)
**ASN-0047, *Generalized referential integrity*** — S3★: "Per-transition preservation of S3★ is discharged in the Class (a) verification matrix below (the joint *S3★ / S3★-aux* prose entry), the authoritative site for both invariants." S3★-aux: "Per-transition preservation is discharged jointly with S3★ in the Class (a) verification matrix below (the *S3★ / S3★-aux* prose entry), the authoritative site for both invariants."

**Problem**: Two adjacent definition boxes carry near-identical sentences that both defer to the same downstream location and both label it "the authoritative site for both invariants." This is the forward-reference accretion pattern flagged for this note ("multiple paragraphs in different sections defer to the same downstream location"; "two paragraphs say the same thing"). The reader is told twice, in the same words, where preservation lives — the second deferral advances nothing.

**Required**: State the joint-discharge pointer once (e.g., on S3★, with S3★-aux saying only "(preserved jointly with S3★)"), or drop both deferrals and let the matrix's `S3★ / S3★-aux` prose entry stand as the single authoritative site without advance announcement.

## OUT_OF_SCOPE

### Topic 1: renumbering-aware interior link withdrawal
**Why out of scope**: The ASN's K.μ⁻ models link-subspace contraction by suffix removal only; the implementation's interior `DELETEVSPAN` (compact-and-renumber) is a distinct operation. The ASN correctly confines this to an Open Question rather than specifying it. `DELETEVSPAN` and POOM mechanics are named OUT OF SCOPE; raising them in an open question to delimit the boundary is appropriate, not a defect.

### Topic 2: transitive transclusion-chain provenance
**Why out of scope**: Provenance guarantees across chains of transclusion are posed as an Open Question. This is new territory for a future ASN, not a gap in the transition taxonomy established here.

VERDICT: REVISE
