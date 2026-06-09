# Review of ASN-0119

I checked the imported permutation equations (R-P1/R-P2, R-S1/R-S2/R-S3) and the induced π against the worked ordinals — pivot `A B C D E ↦ A C D E B` and swap `A B C D E F ↦ A E F C D B` both tile the affected interval exactly, and P0–P3, P5, P6, P8a/b, P9 all check out numerically. One claim about link-footprint fragmentation does not.

## REVISE

### Issue 1: P7a's necessity condition for fragmentation is false (and unproven)

**ASN-0119, Claims table, P7a (FootprintTransport)**: "...so fragmentation of a contiguous run occurs *only when* it straddles a cut covering a partial block — straddling alone does not force it."

**Problem**: The body proves only the weaker contrapositive of P7c: "a contiguous run that fragments... must therefore cross a cut." The table strengthens this to "cross a cut *covering a partial block*," which is never derived — and is false. Counterexample (your own worked pivot, cuts `ord2,3,6`, order `A C D E B`): take a link whose coverage is `{a₁, a₂}` — content bytes `A` and `B`. This is exactly Question 5's "running from a moved region into stationary content."

- Pre-footprint: `project = {ord1, ord2}` — a single contiguous run.
- `π(ord1) = ord1` (R-EXT), `π(ord2) = c₀ + w_β = ord5` (R-P2).
- Post-footprint: `{ord1, ord5}` — discontiguous, fragmented.

The run straddles cut `c₀`, but it covers the *complete* exterior touch `{A}` and the *complete* region `α = {B}`. No partial block is involved, yet it fragments — because the fixed exterior and the relocated `α` separate. Fragmentation here turns on whether the straddled blocks re-abut after relocation, not on partial coverage. The ASN explicitly raises this "stationary content" case in Question 5 but its stated characterization excludes it.

The companion sufficient-condition wording in the same entry and in the body ("runs that span complete relocated blocks" → contiguous) is also imprecise: a run spanning the complete exterior plus complete `α` (`{A,B}` above) "spans complete blocks" yet fragments. The condition holds only when the spanned blocks are *relocated* regions (excluding the fixed exterior) that re-tile contiguously — `α ∪ β` in the pivot re-abuts, but exterior `∪ α` does not.

**Required**: Either (a) weaken the table's necessity claim to match what the body proves — "fragmentation occurs only when the run straddles a cut" — or (b) state the correct geometric characterization the body already names ("survives as contiguous precisely when its π-image is again an interval") and drop the "covering a partial block" qualifier. Correspondingly, sharpen the sufficient condition so "complete relocated blocks" excludes the fixed exterior and requires the blocks to re-abut post-relocation. A stationary-content example (`{A,B}` fragmenting) should be exhibited alongside the existing `{B,C}` partial-block example, since Question 5 names exactly this case.

## OUT_OF_SCOPE

None beyond what the Open Questions already defer (shared-cut transclusion, unserialized concurrent rearrangement, index/footprint-fragmentation invariant, prior-arrangement recoverability). These are correctly held out of this ASN.

VERDICT: REVISE
