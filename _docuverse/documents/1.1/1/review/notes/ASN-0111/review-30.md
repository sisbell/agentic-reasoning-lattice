# Review of ASN-0111

This note specifies READLINK as a pure lookup `readlink(a, Σ) ≡ Σ.L(a)`. The technical content is sound: the definedness condition (RL0), completeness (RL1), determinacy via LP13 (RL7), and the worked example (scattered cross-document from-set, ghost type, link→link nesting, orphaned read) all check out arithmetically and against the foundations. The address computations verify — `inc(a,0)` on the T4-valid `a=[1.0.1.0.1.0.2.1]` advancing position 8 to give `a'=[1.0.1.0.1.0.2.2]`, and `s ⊕ δ(2,8) = [1.0.1.0.1.0.1.3]` — and the coverage-is-subtree claims via PrefixSpanCoverage are correct.

The note carries the anti-bloat classifier; the one substantive finding concerns claim overlap.

## REVISE

### Issue 1: RL-REP restates a foundation lemma and duplicates RL5's principle
**ASN-0111, "Invariants governing the returned structure" (RL-REP) and "Type is interpreted by address" (RL5)**: RL-REP — "The relationship the read conveys is the *coverage* of each endset, not the particular span decomposition... interchangeable under every coverage-based use (projection independence, LP21); the type-by-address instance of this is RL5 above."

**Problem**: Three issues compound here.
1. **Self-acknowledged duplication.** RL-REP explicitly states "the type-by-address instance of this is RL5 above." RL5 already makes the coverage-is-meaning point ("the relationship... is fixed by `coverage(e₃)`... not by whatever is stored"). The principle "coverage, not decomposition, carries meaning" is thus asserted twice — once via L8 (RL5), once via LP21 (RL-REP). This is the "two paragraphs say the same thing in different words" pattern the anti-bloat pass targets.
2. **Foundation restatement.** RL-REP's content is LP21 (RepresentationInvariance) restated; the ASN may *use* LP21 without re-asserting it as a READLINK claim.
3. **Consumer-side, not a READLINK obligation.** READLINK returns the literal span decomposition verbatim (RL1, RL3) — it never reduces an endset to its coverage. "Interchangeability under coverage-based use" is a property exercised by projection/type-matching (downstream operations), not by this read. Stated alongside RL1's verbatim-decomposition guarantee, RL-REP invites confusion about what the read actually returns (spans, not coverage).

**Required**: Either drop RL-REP and fold the single needed clause ("a reader should interpret the result as address-sets-with-roles; equal-coverage endsets denote the same relationship") into RL5 as a one-line consequence, or restate RL-REP so it is unambiguously interpretation guidance for the reader (citing LP21) and explicitly does not weaken RL1's guarantee that the read returns the exact span decomposition.

## OUT_OF_SCOPE

### Topic 1: Distinguishing "unwitnessed" from "gone" at the FOLLOWLINK level
The second Open Question (an empty-at-read endset versus one referencing only unwitnessed content, collapsing under resolution) is correctly deferred — resolution against an arrangement is FOLLOWLINK territory.

### Topic 2: Reader-side identity of value-identical distinct links
The third Open Question (two distinct links with identical recorded structure yielding indistinguishable read *values*) is genuine future territory — READLINK returns the value only, and identity rides on the key `a` the reader supplies (RL4). A link-identity ASN, not this one, owns the guarantee.

VERDICT: REVISE
