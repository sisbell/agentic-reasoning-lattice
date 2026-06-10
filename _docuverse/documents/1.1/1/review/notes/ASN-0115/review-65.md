# Review of ASN-0115

I worked the proofs, not just the prose. The hard cases check out: the Confinement lemma's T5 reduction is valid (`#p = m−1 ≥ 1` for `m ≥ 2`); the deep-case emptiness argument (`#s > m_S(d)`) correctly forces a proper-prefix contradiction with `v ≥ s`; R6's no-interior-hole guarantee is correctly *scoped to the bindable slice* (the full interval does contain unbound interior tumblers like `[S,1,1]`, and the ASN says so); R7's cross-state argument is airtight against the depth-discontinuity trap (a shared bound `v` pins `m_S` equal at both states, so depth-compatibility holds-or-fails identically, and the empty-restriction branch collapses to `∅` regardless); and R8's link-vacuity (CL-OWN forces `d = d'`, CL-UNIQ forces `v = v'`) is sound. The worked instances are arithmetically correct (`δ(5,2)=[0,5]`, `[1,2]⊕[0,5]=[1,7]`, terminal overrun at `k > n_1 = 4`). Cross-references are all to foundation ASNs. No foundation notation is reinvented (Confinement is a justified generalization of C0a with attribution).

I found no correctness or completeness defect. The one item below is anti-bloat polish, which this note is flagged for.

## REVISE

### Issue 1: Permanence essay-content and meta-framing inside R2's faithfulness proof

**ASN-0115, "Faithfulness, and where the invariant stops" (R2)**: "The justification is structural, and it is worth seeing exactly which invariants carry it." … "That cross-state permanence is the storage-layer invariant Nelson's design rests on — content lives permanently at its address, and 'you always know where you are, and can at once ascertain the home document of any specific word or character' (2/40)."

**Problem**: R2 is a single-state denotational equality, and its proof — S2 makes resolution single-valued, S3★ places `a` in the store, the `item` definition sets the value to exactly `Σ.C(a)`, "that is the whole of R2" — is complete and tight on its own. Two passages do not advance it. (a) The opener "it is worth seeing exactly which invariants carry it" is commentary *about* the proof, not the proof. (b) The closing sentence expounds *cross-state permanence* — content living permanently at its address, with a Nelson 2/40 quote about addressing — which is R11/S0/substrate territory, not R2's single-state faithfulness. Per the review guidance, the legitimate "what R2 does not do" clause ("permanence across states is a distinct guarantee R2 does not invoke; it is carried by S0") should stay; what is flaggable is the *placement* of the elaboration that follows it. The 2/40 quote is about location/permanence, supports R9/R11, and appears nowhere else in the note — it is essay content sitting in a proof slot.

**Required**: Keep the tight proof and the one-clause contrast with S0. Cut the meta-opener and the permanence elaboration (the "storage-layer invariant Nelson's design rests on" sentence and the 2/40 quote). If the addressing-permanence point is wanted, it belongs in R11's section, not R2's.

## OUT_OF_SCOPE

None. The ASN keeps to RETRIEVEV's guarantees and routes the adjacent operations (READLINK, FOLLOWLINK, RETRIEVEDOCVSPAN[SET], provenance reporting, straddling-span delivery) to its Open Questions and the stated scope list rather than defining claims for them.

VERDICT: REVISE
