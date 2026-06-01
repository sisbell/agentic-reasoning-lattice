# Review of ASN-0047

## REVISE

### Issue 1: Meta-prose inventorying where a property is consumed

**ASN-0047, ExtendedReachableStateInvariants (TrackedEmission paragraph)**: "Established by the self-contained induction in its definition box ... That induction reaches every reachable state, so TrackedEmission holds wherever FrontierEquivalence consumes it."

**Problem**: The final clause advances no reasoning — it is a use-site pointer telling the reader that one lemma's domain covers another lemma's consumption point. TrackedEmission's own *Preservation* paragraph already establishes it holds at every reachable state; restating "wherever FrontierEquivalence consumes it" is the use-site-inventory pattern flagged for this note.

**Required**: Delete the "holds wherever FrontierEquivalence consumes it" clause. The preservation argument standing alone discharges the obligation; FrontierEquivalence cites TrackedEmission at its own consuming step.

### Issue 2: P3 / content-store-invariance restated in three locations

**ASN-0047, *Destruction confinement*, *ExtendedTransitionInvariants*, and the *Local extensions* table**: P3 is stated in *Destruction confinement* ("P3 is the synthesis of P0 ∧ P1 ∧ P2 ∧ L12"), re-explained in ExtendedTransitionInvariants ("P3 ... covers every per-transition monotonicity obligation ... P0 subsumes ASN-0036's S0 ... content-store invariance under arrangement mutation follows from P0 by the arrangement frames"), and restated again in the Properties table row.

**Problem**: The content-store-invariance derivation ("`C' = C` on every M-mutating transition leaves the content store untouched") appears verbatim-in-substance in both ExtendedTransitionInvariants prose and its table row, and the P0∧P1∧P2∧L12 synthesis appears three times. This is the "two paragraphs say the same thing in different words" pattern.

**Required**: State the content-store-invariance derivation once (in *Destruction confinement* alongside P3's definition); have ExtendedTransitionInvariants and the table cite it rather than re-derive.

### Issue 3: Orphan-link / tombstoning point repeated across four sites

**ASN-0047, D-CTG★ justification, *Orphan links and coupling flexibility*, link worked example Step 5, and Open Questions**: The same claim — links persist in `dom(L)` with fixed endsets under arrangement withdrawal, citing Nelson LM 4/9 "deleted links," with interior-withdrawal deferred to a separate mechanism — is made in the D-CTG★ justification ("interior link withdrawal ... catalogued in Open Questions"), in the dedicated *Orphan links* section, in worked example Step 5 ("This is the *orphan link* state Nelson identifies (LM 4/9)"), and as an Open Question.

**Problem**: Four restatements of one architectural fact. The worked-example occurrence and the dedicated-section occurrence are the legitimate ones (concrete instance + statement); the D-CTG★ justification's forward-deferral and the duplicate Nelson citation are accretion.

**Required**: Keep the *Orphan links* section as the canonical statement and the worked-example instance as the concrete verification. Reduce the D-CTG★ justification to a single cross-reference without re-citing LM 4/9 or re-arguing the cost.

### Issue 4: P4a mixes state quantification with transition-history quantification

**ASN-0047, P4a (Recorded-boundary witnessing)**: "`(A (a, d) ∈ R :: (E Σ_k in the transition history : (E v ∈ dom(M_k(d)) : subspace(v) = s_C ∧ M_k(d)(v) = a)))`"

**Problem**: P4a is listed among ExtendedReachableStateInvariants' composite-boundary *properties of a state*, yet its existential ranges over "the transition history," so it cannot be evaluated from a state Σ alone. The discharge compounds the dual character: new entries are witnessed by Σ' itself (state-local), while pre-existing entries appeal to "a prior witnessing state Σ_k" supplied by the inductive hypothesis (trace-local). A property that is sometimes state-local and sometimes trace-local is not well-typed as either a per-state invariant or a clean boundary property.

**Required**: Either (a) strengthen P4a to a fully state-local form whose witness lives in the *current* M (which the new-entry discharge already achieves and which J1'★ would maintain), or (b) explicitly classify P4a as a trace property distinct from the state-indexed invariant set and define what "the transition history" denotes formally. As written, the witnessing existential's domain is undefined.

## OUT_OF_SCOPE

### Topic 1: ASN-0093 M2 (EmptyArrangement) override
The ASN declares a foundation invariant (ASN-0093 M2) "not inherited" because K.μ⁺ populates arrangements. The Bridging-lemma note justifies this as ASN-0093 being a substrate whose population operations ASN-0047 supplies. This is a legitimate layering decision and is argued explicitly; reconciling the substrate/extension relationship is a foundation-scoping matter, not a defect in this ASN's transition model.

VERDICT: REVISE
