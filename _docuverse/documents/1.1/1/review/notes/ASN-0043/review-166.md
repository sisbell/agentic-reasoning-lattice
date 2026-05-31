# Review of ASN-0043

I checked the proof obligations (L1c via CPP, FSP's invariant discharge, FSE, the L9 ghost-type construction, PrefixSpanCoverage, and all six worked-example extension steps). The mathematics is sound — the L1c two-invocation CPP argument correctly pins the third zero at position `#s+1`, FSP discharges every enumerated state-local invariant, and the Step-6 coverage equality genuinely exercises L8's coverage-vs-decomposition crux. My findings are confined to the forward-reference / meta-prose accretion the `review-mode.anti-bloat` classifier flags.

## REVISE

### Issue 1: FSP's conclusion re-glosses an already-defined term, and the gloss is broader than the set it names
**ASN-0043, FSP statement**: "Then `Σ'` satisfies every state-local L- and S-invariant (the L- and S-invariants of this ASN and ASN-0036); and the `Σ → Σ'` transition satisfies the transition invariants L12 ... and L12a ..."
**Problem**: "state-local L- and S-invariants" is precisely defined one paragraph earlier as a specific enumerated list that *deliberately excludes* L2, L4, L7, L8–L13 (the META/derived/transition invariants). The parenthetical gloss "(the L- and S-invariants of this ASN and ASN-0036)" both restates the already-defined term (adding nothing) and is strictly broader than the intended set — it reads as *all* L-/S-invariants, which FSP does not and could not discharge (e.g. L9, L11b). A reader has to skip past the gloss and reconcile it against the real definition.
**Required**: Drop the parenthetical; the defined term carries the meaning.

### Issue 2: L11b re-explains the same defined term inline
**ASN-0043, L11b statement**: "— where 'the state-local L- and S-invariants' denotes the set named in *A Shared Conformance Lemma* above (preserved by FSP)."
**Problem**: This re-explains a term that is already defined in "A Shared Conformance Lemma," which L11b's proof then cites by name ("we appeal to FSP ..."). The dash-clause is a redundant definitional pointer; the "(preserved by FSP)" aside duplicates what the proof states two sentences later. This is the flagged pattern of a paragraph re-deferring to the same upstream location the proof already invokes.
**Required**: Delete the dash-clause; let the proof's FSP citation stand alone.

### Issue 3: FSP's ASN-0036 bullet closes with a summary exhaustiveness claim
**ASN-0043, FSP proof, "ASN-0036 invariants" bullet**: "`Σ'.C = Σ.C` discharges S0, S1, S7a, S7b verbatim; `Σ'.M = Σ.M` discharges S2, S3, S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ verbatim — every constraint on the content store and arrangement family is reproduced from `Σ`."
**Problem**: The two clauses already enumerate every discharged invariant by name and give the mechanism (stores unchanged). The trailing "— every constraint ... is reproduced from `Σ`" is a generalizing exhaustiveness restatement that advances no reasoning beyond the explicit list it follows.
**Required**: End the bullet after the two enumerated clauses.

## OUT_OF_SCOPE

None beyond what the Open Questions section already defers (global content-subspace constant, transclusion/link-store interaction, compound-link well-formedness).

VERDICT: REVISE
