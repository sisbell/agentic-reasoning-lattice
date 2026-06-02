# Review of ASN-0047

## REVISE

### Issue 1: The k∈{1,2} freshness "structural guarantee" is overstated — it is contingent on a live-state fact

**ASN-0047, *Elementary transitions*, K.δ case (ii) precondition**: "At **k ∈ {1, 2}** (child-spawn) freshness is *structurally guaranteed*: T10a's at-most-once-per-`(t, k')` constraint together with GlobalUniqueness (ASN-0034) forces `inc(t, k)` to be a fresh address whenever the spawn `(t, k')` has not already been performed, so `e ∉ E` follows from the structural allocator discipline rather than from a live-state scan (this is the discharge the worked examples and S7d invoke)."

**Problem**: The guarantee is conditioned on "*whenever the spawn `(t, k')` has not already been performed*." But "the spawn `(t, k')` has not already been performed" is logically equivalent to `inc(t, k') ∉ E` — i.e., to the very conjunct `e ∉ E` being discharged. So the statement reduces to "`e ∉ E` follows structurally, given `e ∉ E`," which is circular. T10a's at-most-once rule is a *constraint the system must not violate*, not a free fact: the only mechanism that detects a repeated `(t, k')` spawn is checking whether its output already inhabits `E`. There is no escape from the live-state dependence the prose claims to avoid. GlobalUniqueness supplies distinctness *across distinct allocation events*; it does not establish that a given `(t, k')` spawn is a new event rather than a repeat.

Consequently the sharp asymmetry the box draws — k=0 a "dynamic frontier guard," k∈{1,2} "structural... rather than from a live-state scan" — does not hold. Both rest on the same `e ∉ E` conjunct against the current state; the genuine difference is only *which* state fact the guard encodes (current frontier index for k=0 vs. single-spawn occurrence for k∈{1,2}).

The same overstatement is instantiated in the worked example (*Worked example: entity hierarchy by K.δ*, Step 2): "`1.2.0.1 ∉ E₁` discharged by GlobalUniqueness (ASN-0034) ... (child-spawning at the live operand `t = 1.2`)." GlobalUniqueness alone does not discharge `1.2.0.1 ∉ E₁`; that holds only because this is the *first* `(1.2, 2)` spawn — a state fact, not a GU consequence.

**Required**: Either (a) identify a mechanism that enforces at-most-once independently of the `e ∉ E` check (and show it), or (b) weaken the claim: state that at k∈{1,2} the `e ∉ E` conjunct *is* the enforcement of T10a's at-most-once discipline (and at the worked-example Step 2, that `1.2.0.1 ∉ E₁` rests on this being the first `(1.2,2)` spawn, with GU supplying only cross-event distinctness once freshness is granted). The k=0 vs k∈{1,2} contrast should be reframed as "which state fact the guard reads," not "live-state scan vs. no scan."

## OUT_OF_SCOPE

### Topic 1: Interior link/content withdrawal with renumbering
The model's K.μ⁻ contracts only by suffix removal; interior withdrawal (compact-and-renumber, the implementation's `DELETEVSPAN`) is correctly deferred. This is already captured in the Open Questions and belongs to the named-operation layer, not this ASN.

VERDICT: REVISE
