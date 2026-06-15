# Review of ASN-0131

I checked the new claims (RE-DEF, RE-NCD, RE-ADDR, RE-UDIST/-∩, RE-CWP, RE-RET) for correctness, case coverage, and — given the `review-mode.anti-bloat` classifier — for forward-reference accretion.

**Substance.** The mathematics is sound. I verified RE-NCD's separator-agreement argument (the third-zero position and the subspace-identifier component one past it both transfer under `s ≼ c`, forcing `E(c)₁ = E(s)₁ ≠ s_C` against L0's `E(c)₁ = s_C`); RE-ADDR's antichain/self-target case split (a fresh output is nullified in its post-state *iff* it retracts its own emitter); the RE-CWP weakest precondition (the `I_R`/`Δ` split is equivalent to "no available pair dropped," boundary `R = ∅` collapsing to `RE = ∅`); and RE-RET's sole-bearer biconditional (forward via permanent removal + emitter content-disjointness under the flagged `Θ` hypothesis; backward via R-Scope confining the fresh nullification to the named target). The worked instance correctly exercises RE-OVL, RE-CLIP, RE-WHOLE, per-endset surfacing, and RE-UNIT. RE-UDIST-∩'s two-obstruction analysis — including the injective counterexample showing no injectivity-style restriction recovers `⊇` — is correct. The transition enumeration in §Stability is exhaustive over the ASN-0047 vocabulary plus the ASN-0082 lift. No correctness or missing-case findings.

The findings below are all forward-reference accretion — minor, but they are the exact patterns the classifier asks to be surfaced.

## REVISE

### Issue 1: Open Question 4's target is fully characterized twice
**ASN-0131, §Composing regions (closing) and Open Questions**: the body closes with "The weakest *structurally-restricted sufficient* form — one that discharges the touch-implication without the per-endset quantifier — is what Open Question 4 takes up," and OQ4 restates the identical characterization: "the weakest *structurally-restricted sufficient* condition — phrased directly on the available endsets' coverages and the three region images …, with the per-endset `touch` quantifier eliminated."
**Problem**: The full open-problem statement (structural sufficient condition, on coverages and the three images, per-endset quantifier removed) appears in two slots. The body's "what it is not is *structural* …" sentences pre-state OQ4 rather than handing off to it.
**Required**: In the body, end the analysis at the exact necessary-and-sufficient touch-implication condition plus a bare pointer ("a structurally-checkable sufficient condition is left open, OQ4"); let OQ4 carry the characterization. Remove the duplicated framing from the body.

### Issue 2: the "membership-motion, spans-fixed" principle is re-tagged after a blanket statement
**ASN-0131, §Stability**: the intro establishes the blanket "By RE-IDENT each surfaced endset's coverage is permanent … never the spans of one that is. **Every motion catalogued below is a motion of membership.**" Subsequent bullets then re-assert it: the K.μ~ bullet — "the answer moving by membership alone (RE-IDENT)"; the insert/delete paragraph — "`RE` tracks the image's motion by membership, each surfaced endset's spans held fixed (RE-IDENT)."
**Problem**: Once the intro states all motion is membership-motion with spans fixed, the per-bullet re-tags restate the blanket without adding anything (the K.μ⁺/K.μ⁻ bullets correctly do *not* re-tag). This is the "two paragraphs say the same thing" pattern at the tag level.
**Required**: State the principle once in the intro; drop the per-bullet RE-IDENT re-tags except where a reader might genuinely suspect spans move.

### Issue 3: the union-distributivity rationale for OQ1 is stated in both §Extent and OQ1
**ASN-0131, §Extent and Open Questions**: §Extent argues "union-distributivity (RE-UDIST) holds for the adopted whole-endset value and would fail for the touching-spans reading," and OQ1 repeats it as "given that only whole-endset surfacing yields union-distributivity (RE-UDIST)."
**Problem**: The deciding fact is asserted in the analysis and again in the question. (Smallest of the three — the OQ1 occurrence functions partly as motivation.)
**Required**: Keep the argument in §Extent; reduce OQ1's clause to a pointer, or vice versa.

## OUT_OF_SCOPE

None. The Open Questions (rendered mode, multiplicity, link-subspace regions, type-slot semantics, non-co-resident stores, structural intersection condition) are correctly deferred rather than answered, and the note defines no claims for the listed out-of-scope operations.

VERDICT: REVISE
