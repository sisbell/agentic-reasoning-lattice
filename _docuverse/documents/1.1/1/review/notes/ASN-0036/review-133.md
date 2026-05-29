# Review of ASN-0036

The mathematical core is rigorous. I worked the S8 partition proof (coverage, within-subspace lemma both cases, across-subspace via T5/T10), the D-CTG-depth infinite-intermediate construction, the D-SEQ four-step assembly, and the worked-example shift computations at k=3 — they hold. The findings below are in the territory this note is explicitly flagged for (`review-mode.anti-bloat`): accreted meta-prose around the S8 existence/maximal-run distinction.

## REVISE

### Issue 1: The existence-vs-maximal-run distinction is stated three times across sections
**ASN-0036, S8 (post-statement paragraph) and Worked example (Σ₁ check)**: 
> "Conjunct (b) is what *defines* a correspondence run: when nⱼ > 1 it asserts a non-trivial ordinal-displacement identity, exercised at k ≥ 1 only on runs of length greater than one (the worked example below checks such a run at k = 3). The theorem proved here is the existence claim alone, and the witness it exhibits is the degenerate one..."

and again in the worked example:
> "(This length-5 run illustrates the *definition* of a correspondence run — conjunct (b) at nⱼ > 1 — not the output of S8's existence theorem, which guarantees only the singleton partition; the coalescing of singletons into maximal runs is the Open Question deferred below.)"

**Problem**: The same point — "the theorem only delivers singletons; non-trivial runs are illustrative and deferred to the Open Question" — appears in the S8 paragraph, forward-references the worked example, and is then restated in the worked example with a deferral pointing back to the Open Questions. This is the multi-section deferral-to-same-location pattern plus a defensive justification of the theorem's weakness. A reader must hold the same caveat in three places to follow what S8 actually proves.
**Required**: State once, at the theorem, that the exhibited witness is the singleton decomposition for which (b) reduces to the base case. Drop the forward reference and the worked-example parenthetical; the example can show a length-5 run without re-litigating what the theorem does not claim.

### Issue 2: D-CTG-depth's proof is previewed verbatim in prose before the claim
**ASN-0036, Arrangement contiguity (paragraph preceding D-CTG-depth)**:
> "The intuition — formalized as D-CTG-depth and proved below — is that if two positions diverged before the last component, then any choice of natural number n could be slotted into the next component to yield an intermediate; D-CTG would force all such intermediates into V_1(d), producing infinitely many positions and contradicting S8-fin."

**Problem**: This is the D-CTG-depth proof restated as "intuition" immediately before the formal claim, whose proof then walks the identical construction (slot n into the next component → infinitely many forced intermediates → contradict S8-fin). Two paragraphs saying the same thing; the preview advances no reasoning the proof doesn't supply.
**Required**: Either delete the preview or reduce it to a one-clause motivation ("at m ≥ 3, D-CTG + S8-fin force a shared prefix — see D-CTG-depth") without rehearsing the argument.

### Issue 3: S9 restates S0 with no formal content plus evidentiary prose
**ASN-0036, The separation theorem**: "S9 is S0 read directionally: arrangement-only transitions (`Σ'.M(d) ≠ Σ.M(d)`) cannot alter `C`, since S0 already holds for every transition unconditionally."
**Problem**: The Properties table itself records S9 as having "no formal content beyond S0." The section then adds a Nelson quote, a restatement of the S3 coupling already given in that section, and a Gregory note. As a named directional reading this is defensible, but the surrounding paragraph re-derives the one-directional coupling that S3's own frame clause already states.
**Required**: Keep the named corollary as a single sentence; remove the re-derivation of the coupling direction (it duplicates S3's frame clause) and trim to the directional statement.

## OUT_OF_SCOPE

### Topic 1: Maximal/unique-cardinality run decomposition
**Why out of scope**: The ASN proves only the singleton existence witness and already defers coalescing-into-maximal-runs and decomposition uniqueness to the Open Questions. This is correctly future territory, not an error — flagged here only to confirm it should *stay* deferred rather than be patched into S8.

### Topic 2: Whether editing operations preserve D-CTG/D-MIN/S2
**Why out of scope**: Operation frame/postconditions are explicitly out of scope and already listed in Open Questions; the ASN correctly states D-CTG/D-MIN as well-formedness constraints without proving operation preservation.

VERDICT: REVISE
