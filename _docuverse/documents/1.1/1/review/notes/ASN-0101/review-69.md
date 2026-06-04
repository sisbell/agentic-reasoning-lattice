# Review of ASN-0101

I checked the operation specification (D0), the gap-closure and preservation claims (D1–D9), the ValidComposite★ extension (D10), and the weakest-precondition calculations (D11), including the three worked examples. The mathematics is sound: the D0 containment reduction handles `m_S = 2` and `m_S ≥ 3` correctly, the `σ_d` bijection argument (D1) generalizes ASN-0082's D-BJ cleanly, D8's three-group coverage accounts for every ASN-0047 per-state invariant (S2, S3★, S3★-aux, S4, S7a/b/d, C1b/c, S8a, S8-fin, S8-depth, S8★, C-fin, D-CTG★/MIN★/SEQ★, P6/7/8, NodeLineage, ActivatedEmission, L0/1/1a/1b/1c/3, L14≡SD, L-fin, CL-OWN, CL-UNIQ), and the D10 single-DEL vacuity of J0/J1★/J1'★ plus the step-agnostic boundary induction for P4★/P7a are correct. The findings below concern accreted meta-prose in the D10 boundary derivation (this note carries `review-mode.anti-bloat`).

## REVISE

### Issue 1: Triplicated "step-agnostic closure" statement in the D10 boundary derivation
**ASN-0101, D10**: The same observation — that the boundary induction closes from the induction hypothesis and J0/J1★ regardless of whether the final step is DEL — is stated three times:

1. Preamble (*DEL-neutrality fact*): "DEL's effect on the other two composite-boundary properties, P4★ and P7a, needs no separate fact: the step-agnostic derivation below closes both from the induction hypothesis and the coupling constraints (J0, J1★) alone, whether or not the composite's final step is DEL."
2. Mid-step: "For a composite drawn entirely from the pre-DEL vocabulary, the derivation below reproves inductively, from coupling alone, what that theorem establishes for pre-DEL reachable states."
3. Closing: "The step-agnostic derivation above closes using only the induction hypothesis and the coupling constraints (J0, J1★), so it needs nothing further when the composite's final step is DEL."

**Problem**: Matches the flagged pattern "two paragraphs in the same document say the same thing in different words." The preamble sentence is a pure forward-pointer/use-site inventory ("needs no separate fact ... the derivation below closes both"), announcing what the derivation will do before it does it. The reader must skip past the preview to reach the actual derivation, then re-encounter the same claim at the close. Only N2 (the actual P4a fact) is load-bearing in the preamble.

**Required**: Keep N2 as the named fact. Delete the preamble's "needs no separate fact ..." sentence and the redundant mid-step restatement (item 2). The closing sentence (item 3) suffices to record that the derivation is step-agnostic — or drop it too, since the derivation visibly invokes only the IH and J0/J1★.

### Issue 2: Rationale-only sub-paragraph on why re-proof is required
**ASN-0101, D10, boundary derivation**: "P4★, P4a, and P7a are composite-boundary properties, not per-state invariants — ASN-0047's ExtendedReachableStateInvariants theorem lists them separately ... so we must re-establish these properties at every such boundary." followed later by "We cannot instead cite ASN-0047's ExtendedReachableStateInvariants at `B_{j+1}` for the non-DEL case: `B_j` may itself have been reached by an earlier DEL-containing composite ..."

**Problem**: Two separated paragraphs both justify *why the proof is necessary* rather than advancing it. The first establishes the scope distinction (legitimate context); the second re-litigates the same point against a specific shortcut. Combined with Issue 1's triplication, the boundary derivation spends more text justifying its own existence and generality than executing the induction.

**Required**: Consolidate to a single sentence stating that admitting DEL places DEL-terminated boundaries outside ExtendedReachableStateInvariants' scope, so P4★/P4a/P7a are re-proved by induction over composite boundaries. Remove the second "We cannot instead cite ..." paragraph as a restatement.

## OUT_OF_SCOPE

### Topic 1: Reconstruction / reversibility of pre-DELETE arrangements
The Open Questions correctly defer arrangement reconstruction, DELETE-then-INSERT round-trips, and orphaned-I-address enumeration to a versioning mechanism. These are future-ASN concerns, not gaps in D0–D11.

VERDICT: REVISE
