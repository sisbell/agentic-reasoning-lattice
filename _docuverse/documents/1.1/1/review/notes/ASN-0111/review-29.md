# Review of ASN-0111

## REVISE

### Issue 1: Claim numbering has a gap — no RL4
**ASN-0111, Claims Introduced table and body**: the numbered sequence runs RL0, RL1, RL2, RL3, **RL-HOME**, RL5, RL6, RL7, RL8.
**Problem**: There is no RL4. The home claim sits in the RL4 slot (between RL3 and RL5) but is labeled RL-HOME, so the sequence jumps RL3 → RL-HOME → RL5. A reader cannot tell whether RL4 was dropped, renamed, or is missing. This reads as a renamed-claim artifact from a prior cycle.
**Required**: Either renumber the home claim as RL4, or renumber RL5–RL8 to close the gap. Mnemonic-named claims (RL-WF, RL-ARITY, etc.) are fine, but RL-HOME is wedged into the *numbered* run.

### Issue 2: "The read consults only Σ.L, never an arrangement" is asserted four times
**ASN-0111, intro / "Recorded relationship versus resolved position" / RL8 / worked orphaned instance**:
- Intro: "All three consult something beyond the link object… `readlink` consults nothing beyond the link itself."
- "Recorded relationship versus resolved position": "The direct read performs no such resolution; it returns the recorded spans as they stand."
- RL8: "`readlink(a, Σ)` depends only on `Σ.L`; it is independent of every document arrangement."
- Worked instance: "the read consults only `Σ.L`, never an arrangement (RL8)."
**Problem**: The same point is made in four sections. The "Recorded relationship versus resolved position" section in particular is a prose preamble whose first two sentences restate the intro distinction and whose content is fully captured by RL8 — it advances no reasoning RL8 doesn't already carry. This is exactly the cross-section repetition the anti-bloat pass targets.
**Required**: State the arrangement-independence once (RL8 is the natural home, with the worked orphaned instance as its check) and delete the redundant preamble prose. The intro's following/searching/counting distinction can stay as scope-setting, but should not also pre-argue RL8.

### Issue 3: RL-WF re-defers to the standing precondition already established
**ASN-0111, "Invariants governing the returned structure"**: "the guarantees a reader may assume of any value `readlink` produces, *under the standing precondition that `Σ` is reachable and invariant-satisfying* (established above)…"
**Problem**: The standing precondition is fully stated at the top of "Deriving the read." The parenthetical "(established above)" plus the re-statement here is a back-reference that restates rather than uses. It is the "defer to the same location" pattern.
**Required**: Drop the re-statement; the standing precondition governs the whole note and need not be re-cited per section.

### Issue 4: RL2 restates "model primitive" and cites L6 twice within one claim
**ASN-0111, RL2**: prose says "exposes each endset under its slot index as a model primitive (L6, ASN-0043)"; the formal line then repeats "the positional accessor `readlink(a, Σ).eᵢ` is a model primitive (L6, ASN-0043), with link equality componentwise."
**Problem**: The same proposition and the same citation appear twice in adjacent lines of one claim.
**Required**: State the slot-as-primitive fact and the L6 citation once.

### Issue 5: RL-GEN is near-vacuous
**ASN-0111, RL-GEN**: "By RL1 the read returns the recorded spans unmodified, and those spans are L4-general… so the read inherits that generality without adding any confinement."
**Problem**: Since `readlink(a, Σ) = Σ.L(a)` is an exact copy, "the read adds no confinement" is not a substantive read-side guarantee — it is an immediate restatement that the read changes nothing, already carried by RL1. It documents the absence of a restriction the operation never had.
**Required**: Either fold the L4-generality observation into RL1 as a one-line consequence, or drop RL-GEN. (RL-WF and RL-ARITY do carry reader-facing content — finiteness, well-formedness, mandatory non-empty type — so they should stay; RL-GEN does not clear that bar.)

## OUT_OF_SCOPE

### Topic 1: Continued-validity / distinguishability guarantees
The three Open Questions (validity from a read alone, empty-vs-unwitnessed distinction at FOLLOWLINK, distinguishing equal-structure links) correctly point to FOLLOWLINK and future ASNs rather than this one. No action needed; noted only to confirm they are appropriately deferred.

The note is correct throughout — every claim reduces faithfully to `readlink(a, Σ) = Σ.L(a)` and is properly grounded in foundation invariants (L2, L8, L9, L12, LP13, LP17, LP21). The worked example is concrete and checks RL1, RL2, RL5, RL6, RL8, RL-ARITY accurately. The findings above are prose-economy and labeling issues, not correctness gaps.

VERDICT: REVISE
