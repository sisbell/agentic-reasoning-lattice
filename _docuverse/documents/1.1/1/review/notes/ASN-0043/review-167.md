# Review of ASN-0043

## REVISE

### Issue 1: Step 3 of the worked example re-motivates N ≥ 3 with a duplicate Nelson citation already carried by L3
**ASN-0043, Worked Example, Step 3**: "The standard triple (from, to, type) suffices for binary relational connections, but L3 admits `N ≥ 3` to support Nelson's 4-sets, 5-sets, and n-sets [LM 4/79]. We construct an arity-4 link to exercise L3, L6, and L8 in the higher-arity regime."
**Problem**: The N ≥ 3 / "4-sets, 5-sets ... n-sets" rationale with the [LM 4/79] citation already appears in L3's note ("Nelson [LM 4/79] explicitly calls for N-endset support beyond three: '4-sets, 5-sets ... n-sets ...'") and is foreshadowed in "The Endset Structure" ("Nelson's design does not stop at three"). An example step's job is verification; re-citing [LM 4/79] to re-motivate the design is essay content in a structural slot — the "two paragraphs say the same thing in different words" pattern the anti-bloat classifier targets.
**Required**: Drop the design re-motivation and the duplicate citation; state only what the step does ("Construct an arity-4 link `a₃`") and proceed to the checks.

### Issue 2: Step 6's intro restates L8's definition nearly verbatim
**ASN-0043, Worked Example, Step 6**: "L8 is defined on *coverage*, not span-set identity; its distinctive content is that two type endsets with different span decompositions but identical address coverage denote the same type."
**Problem**: L8 itself reads: "two type endsets with different span decompositions but identical address coverage denote the same type." Step 6's opening reproduces this sentence almost word-for-word. The non-vacuity signpost ("Steps 1–4 compare only same-singleton ... never the crux case") is enough to justify the step; the verbatim re-statement of L8's content adds no reasoning. Step 4's intro ("L8's substantive content is *discrimination* ...") is a milder instance of the same re-statement habit.
**Required**: Replace the re-statement with a one-line pointer to the gap being closed (prior steps used singleton/disjoint endsets only), and let the *L8 at Σ_6* check carry the content. Trim Step 4's "substantive content is discrimination" sentence likewise.

## OUT_OF_SCOPE

None. The open questions already route future topics (global content-subspace constant, transclusion/link-store consistency, compound-link well-formedness, allocation ordering, type-hierarchy constraints) to later ASNs; the body does not assert claims about them.

Notes on what I checked and found sound: the L1c chain construction and its `s = home(a)` derivation via CPP (two invocations correctly pin the third zero at `#s+1`); the FSP L1c bullet's zero-count derivation of `k₁ = 2` and `#tᵢ > #s`; FSE's terminal-position-only argument for `home(a') = home(a)` (resting correctly on `#home(a)+1 < #a` from L1b); the L9 Case A/B fresh-address constructions and ghost-disjointness transfer to `Σ'`; and the six-step worked example's arithmetic (PrefixSpanCoverage intervals, `δ(2,8)` vs split coverage `[g,g') ∪ [g',h) = [g,h)`, disjoint sibling prefix cones). These are correct.

VERDICT: REVISE
