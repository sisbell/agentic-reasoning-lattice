# Review of ASN-0069

This ASN is thorough and largely correct: the V0–V12 derivation chain is well-grounded, the empty-source and fork-of-fork boundary cases are handled (V7, V11), and the ValidComposite★ verification discharges its preconditions in detail. My findings are confined to the anti-bloat residue the `review-mode.anti-bloat` classifier flags — meta-prose that defends or restates rather than advances the argument.

## REVISE

### Issue 1: Defensive "preservation alone does not establish" framing before the zeros induction
**ASN-0069, §"Identity by Sub-Allocation"**: "K.δ-ID.zeros-0/1 (ASN-0047) preserves zeros at both `k = 0` and `k = 1`, but preservation alone does not establish `zeros(d_new) = 2`; the induction supplies the input value `zeros(input) = 2` that K.δ-ID.zeros-0/1 then carries through."

**Problem**: This sentence explains *why* the following induction is needed (preservation is insufficient without an input value) rather than advancing the proof. It is immediately made self-evident by the base case, which states `zeros(d_src) = 2` and applies K.δ-ID.zeros-0/1 directly. This is the "new prose explaining why the technique is needed rather than what it does" pattern — defensive accretion a precise reader must skip past to reach the actual induction.

**Required**: Delete the sentence. The base case (`zeros(d_src) = 2 ... K.δ-ID.zeros-0/1 at k=1 gives zeros(d_new) = 2`) already supplies the input value and carries it through; no preamble justifying the induction is needed.

### Issue 2: Worked example restates the notation block's length/parent distinction
**ASN-0069, §"Worked Example", subsequent-fork paragraph**: "Here `d²_new` is *chain* notation — the second link in a fork chain, of length `#d_src + 2`." and "The sibling-notation `d_new²` distinguishes this second sibling fork of `d_src` ... in particular, `d_new² ≠ d²_new` of the prior paragraph (which has length `#d_src + 2` and parent `d_new` in its sub-allocator)."

**Problem**: The notation block (§"Independence Among Forks") already established this exact distinction: "the two are structurally distinct tumblers — `d_new²` has length `#d_src + 1` ... while `d²_new` has length `#d_src + 2`." The worked example re-derives the same length facts (`#d_src + 1` vs `#d_src + 2`) and parent assignments rather than simply *using* the convention. This is the "two paragraphs in the same document say the same thing in different words" pattern. (Distinct from the previously-declined Issue 4, which concerned the *position* of the notation block; this concerns the worked example *restating its content*.)

**Required**: In the worked example, use the notation without re-deriving the length/parent contrast — e.g., write `d_new² = p.2` (sibling) and reference `d²_new` (chain) by name, letting the notation block carry the structural distinction. Drop the parenthetical length/parent re-statement.

## OUT_OF_SCOPE

### Topic 1: Concurrent fork during source modification, snapshot-vs-living forks, transcludent sources
**Why out of scope**: These are raised correctly as Open Questions, not claims. They are new territory (concurrency semantics beyond the sequential atomic axiom, alternative inheritance models, transclusion chains) appropriate for future ASNs, not defects here.

VERDICT: REVISE
