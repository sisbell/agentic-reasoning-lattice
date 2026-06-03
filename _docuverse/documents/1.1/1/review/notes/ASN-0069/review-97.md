# Review of ASN-0069

## REVISE

### Issue 1: Worked example re-derives V2 instead of citing it
**ASN-0069, §"Worked Example", "*Subsequent fork of `d_src`*" paragraph**: "By V2 applied at this second fork — whose inductive argument we walked through in §"Identity by Sub-Allocation" — `d_src ≼ d_new²`. We can verify directly: by TA5(c) `#d_new² = #d_new = #d_src + 1`; by TA5(b) at `k = 0`, `d_new²` agrees with `d_new` at every position except `sig(d_new) = #d_name`; ... The Prefix definition then gives `d_src ≼ d_new²`."

**Problem**: This first cites V2 for the conclusion `d_src ≼ d_new²`, then re-proves the same conclusion symbolically from TA5(b)/(c) and the Prefix definition. The re-derivation is V2's own argument (the inductive prefix derivation already given in §"Identity by Sub-Allocation"), not a check against a concrete scenario — `d_src` carries no concrete component values in this example, so nothing numeric is being verified. This is the "cite X, then re-establish X from primitives" duplication the anti-bloat pass targets: a worked example should exhibit the established property, not re-run the general proof. (Contrast the immediately following V10(a) check, which does use the concrete trailing-component values `2 ≠ 1` and is legitimate.)

**Required**: Delete the "We can verify directly: ..." symbolic re-derivation and let the V2 citation stand. If a concrete check is wanted, instantiate it with actual tumbler values rather than reproducing V2's abstract argument.

### Issue 2: §"Permanence Across Source and Fork" closing essay restates V12 without advancing it
**ASN-0069, §"Permanence Across Source and Fork", paragraph after V12**: "V12 underwrites Nelson's "lengthy due process" claim: published content stays published precisely because the permanence is structural, not policy. ... any withdrawal mechanism a deployment chooses to layer on top is a policy decision above the transition system, not an operation within it."

**Problem**: The load-bearing sentence ("There is no operation in the transition vocabulary that removes content from `C`...") is a legitimate statement of what the vocabulary does not do, but it is already the content of V12 and its derivation. The surrounding policy-vs-mechanism commentary is interpretive essay occupying a structural slot after a formal property — it does not advance the reasoning V12 already closed. Under the anti-bloat classifier this is essay content the precise reader must skip past.

**Required**: Reduce to the single substantive sentence (no removal operation exists in Σ), or fold it into V12's derivation; drop the policy/motivation framing.

## OUT_OF_SCOPE

### Topic 1: Concurrent-fork semantics, snapshot-vs-living forks, transcludent sources
**Why out of scope**: The Open Questions section correctly defers these to future ASNs; they are new territory (concurrency model, alternative inheritance disciplines, transclusion-chain forks), not errors in the present derivation.

VERDICT: REVISE
