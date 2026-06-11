# Review of ASN-0117

This ASN is in strong shape: the two-realisation split on `R = ∅` is correctly motivated by K.μ⁺'s strict-extension precondition, the coupling obligations J0/J1★/J1'★ are discharged explicitly rather than by gesture, the wp derivation's range identity `ran(M'(d)) = ran(M(d)) \ A_del^{excl}` checks out exactly (including the SD-based disjointness from link-subspace images), and the worked examples now cover the middle, leading, suffix, delete-everything, multi-position-shift, sharing, and transclusion cases. I verified the arithmetic in all six scenarios and the J1★ vacuity argument; they are sound. Two issues remain, one of them squarely in the anti-bloat category this note carries.

## REVISE

### Issue 1: The J2 self-sufficiency discharge is stated three times

**ASN-0117, "What shifts, and what the shift must preserve" (Case `R = ∅` paragraph and the coupling paragraph immediately following)**: The Case `R = ∅` paragraph ends: "As an *elementary* transition K.μ⁻ is self-sufficient — it requires no coupling and carries `Σ'.C = Σ.C ∧ Σ'.L = Σ.L ∧ Σ'.E = Σ.E ∧ Σ'.R = Σ.R` directly (J2, ContractionIsolation, ASN-0047) — so every coupling and frame obligation below holds for this single-step realisation outright, without recourse to a second step." The very next paragraph reopens: "For the `R = ∅` single step, J2 (ContractionIsolation) already supplies `Σ'.C = Σ.C ∧ Σ'.L = Σ.L ∧ Σ'.E = Σ.E ∧ Σ'.R = Σ.R` outright, so every obligation below holds trivially and the elementary K.μ⁻ carries no composite-coupling clause at all." The same conjunction is then quoted a third time later in the same paragraph ("together with J2's `Σ'.L = Σ.L ∧ Σ'.E = Σ.E ∧ Σ'.R = Σ.R` for the `R = ∅` single step").

**Problem**: Two adjacent paragraphs say the same thing in different words — the same J2 citation, the same four-way frame conjunction, the same "every obligation below holds outright" conclusion — and a third restatement follows within the paragraph. This is the accretion pattern this note is flagged for. Additionally, the coupling paragraph opens with "DELETE's coupling and frame obligations are discharged identically in both realisations," and then immediately describes two *different* discharge routes (trivially via J2 for the single step; explicit J0/J1★/J1'★ verification for the composite) — "identically" is the wrong word for what follows.

**Required**: State the J2 discharge once, in the coupling paragraph where it is consumed; reduce the Case `R = ∅` paragraph's closing sentence to the case definition plus a pointer ("coupling and frame discharge below"). Replace "discharged identically in both realisations" with wording that matches the actual structure (e.g., "discharged for both realisations — trivially via J2 for the single step, explicitly for the composite").

### Issue 2: S8★'s content and S8's preconditions are both misstated in the run-recut paragraph

**ASN-0117, "The document remains one coherent sequence"**: "But S8★ asserts only that *some* finite maximal-run partition exists, which S8 (ASN-0036) guarantees for any finite single-subspace arrangement; the contracted text arrangement `V_S(d') = {q_1, …, q_{N−c}}` is exactly such, so S8★ holds in the post-state notwithstanding the re-cut."

**Problem**: Two inaccuracies in one sentence. First, S8★ (ASN-0047) does not assert "only existence": on the content subspace — exactly the subspace this deletion re-cuts — S8★ retains S8's condition (c), *uniqueness* of the maximal-run decomposition. The paragraph's point (S8★ pins no particular decomposition *across* states, so a pre/post re-cut is not a violation) is correct, but the within-state obligation being discharged includes uniqueness, and the sentence as written denies that. Second, S8 is not guaranteed "for any finite single-subspace arrangement": its preconditions are S8-fin, S2, S3, S8a, and S8-depth. These all hold at the post-state (S2-post, S8-fin-post, S8a-post, S8-depth-post, and S3★ restricted to the text subspace), so the discharge goes through — but the loose gloss substitutes for the actual precondition inventory.

**Required**: Restate the sentence so that (i) the post-state obligation is existence *and uniqueness* of the maximal-run decomposition within the post-state, both delivered by S8, with the cross-state observation kept as the reason the re-cut is harmless; and (ii) S8's preconditions are named and matched to the post-state package conjuncts that supply them, rather than glossed as "finite single-subspace."

## OUT_OF_SCOPE

### Topic 1: Deletion in the link subspace
**Why out of scope**: The precondition fixes `S = subspace(p) = s_C`, so de-arranging link V-positions (withdrawing a link's entry from its home document's arrangement) is outside DELETE's domain. K.μ⁻ (ASN-0047) permits link-subspace contraction, so the substrate supports it, but specifying that operation — and its interaction with CL-OWN/CL-UNIQ and discoverability — is a separate operation for a future ASN, not an error here.

### Topic 2: Deletion at V-position depth m > 2
**Why out of scope**: The ASN inherits the depth-2 restriction (`#p = 2`) from the foundation contraction (ASN-0082), which is stated only at depth 2. Generalizing the left-shift displacement to deeper text subspaces is future foundation work, not a defect in this ASN.

VERDICT: REVISE
