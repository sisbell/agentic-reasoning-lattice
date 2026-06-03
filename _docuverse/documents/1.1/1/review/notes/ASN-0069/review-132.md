# Review of ASN-0069

## REVISE

### Issue 1: V8d carries accreted "what it does not claim" meta-prose that defers to a downstream location

**ASN-0069, §"Structural Correspondence", the two paragraphs following the V8d box**:

> "V8d concerns the *correspondence* ... The *store-persistence* of the shared content is a separate, unconditional matter, and we do not fold it into V8d. ... we let V12(b)/P0 carry it rather than restate it under V8d's hypothesis, where it would falsely appear contingent on non-targeting."

and

> "The whole-document non-targeting hypothesis is the cleanest condition V5a supports. A finer claim — that an individual position `v` survives even when *other* positions of `d_op` or `d_new` are edited — is available under K.μ⁻'s retention semantics ... but it requires the per-position frame rather than the whole-document one, so we do not fold it into V8d."

**Problem**: Both paragraphs are defensive justification about what V8d deliberately does *not* claim and why a related fact lives elsewhere (V12(b)/P0). This is the residue of the recent "split store-persistence out of perpetuity claim" revision: the split itself is sound, but the prose explaining the split — "we do not fold it into V8d," "we let V12(b)/P0 carry it rather than restate it," "where it would falsely appear contingent on non-targeting" — does not advance the reasoning. It is exactly the anti-bloat pattern of justifying document ordering and deferring to a downstream location. The opening sentence ("V8d concerns the *correspondence* ... which is precisely what the non-targeting hypothesis secures") also restates what the V8d box and its derivation already established. A reader following the correspondence argument must skip past this commentary to reach the next substantive claim.

**Required**: Replace the two paragraphs with at most one short sentence noting that store-persistence of the shared content is unconditional (V12(b)/P0) and independent of V8d's non-targeting hypothesis. Drop the "we do not fold it into V8d / would falsely appear contingent" structural commentary and the finer-claim-not-made paragraph entirely; the per-position retention claim, if wanted, belongs at K.μ⁻'s treatment, not in a negative aside here.

## OUT_OF_SCOPE

### Topic 1: Subsequent-fork content semantics (operand = prior version, not d_src)

J4's operand-tracking rule means a second fork of `d_src` snapshots the latest version's content rather than `d_src`'s. Whether that is the intended user-facing semantics of "fork d_src again" is a question about J4 (ASN-0047, foundation), not about this ASN, which faithfully applies the rule and flags the consequence in V10(b) and the worked example.

VERDICT: REVISE
