# Review of ASN-0133

This is a strong, careful note. The view-rebuild in Q0 is genuinely exhaustive (I checked every view-sensitive atom class against UV and PC3), the Q-EXT/Q5/Q5a/Q6 chain is sound, and the heterogeneous-rewrite worked example computes correctly end to end (I verified Σ* and the naive-merge contrast). The findings below are real but none is structural.

## REVISE

### Issue 1: H-W's load-bearing consequence is left underived — it *is* the termination conclusion

**ASN-0133, W/H-W and "The H-RF/H-W separation"**: "It implies the weaker H-RF (Q5's injection, below)." … "H-W is generically false under starvation, no usable route to H-RF though it formally implies it."

**Problem**: H-W is `|W(σ)| < ∞` for every σ, where `W(σ)` ranges over *all* indices (your own starvation example has the true argument's triple "recur at every index k"). But `|W(σ)| < ∞` means only finitely many `(ρ, x, k)` triples are trigger-true, hence only finitely many *indices* carry any trigger-true argument, hence past the maximum such index `quiescent_R(Σ_k)` holds at every `Σ_k`. So H-W entails: every σ reaches and *permanently holds* quiescence — with no fairness and no regime hypothesis. H-W is therefore strictly stronger than Q6's entire conclusion; it presupposes the termination it would be used to prove. The note derives only the weaker `H-W ⟹ H-RF` and attributes H-W's unusability to starvation-fragility ("generically false"), never naming the root cause: a hypothesis that is logically equivalent to "eventual held quiescence on every path" cannot serve as a hypothesis of a termination theorem. This is a one-step derivation from the definition, omitted.

**Required**: Add the derivation `H-W ⟹ eventual-and-held quiescence (unconditionally, every σ)`, and state that this — not merely starvation-fragility — is why H-W is "no usable route." It also sharpens the contrast with Q5a's bounded-domain-growth, which genuinely *does* sit strictly between H-RF and the conclusion (your "strictly stronger than H-RF … H-RF does not imply it" is correct there precisely because bounded growth does *not* imply quiescence).

### Issue 2: the worked-example divergence/stratification failure mode is precluded by the registry's own types

**ASN-0133, Worked composition / Bound (Q5a)**: "let the resolver's emissions also make fresh targets need attention (needs_attention true on addresses ρ_R creates, enlarging ⋃_k [D_{ρ_P}]_{Σ_k})" … "specialized to this all-SF producer, re-arm is vacuously excluded and the only divergence route left open is domain growth — which is exactly what the diagnosed failure exploits."

**Problem**: `ρ_R` emits `res`. The producer domain is `{t ∈ M_tgt : is_attn(t)}`, reading types `tgt` and `attn`. A `res` deposit is neither a `tgt`-tuple nor an `attn`-tuple nor a retraction, so it changes neither `M_tgt` nor `is_attn` — `ρ_R` *cannot* enlarge `[D_{ρ_P}]`. So the "classic failure mode" (resolver enlarging producer domain) is not realizable in this registry. Worse, the note then asserts domain growth is "the only divergence route left open" and "what the diagnosed failure exploits" — but that route is *also* closed by the type separation, not merely the re-arm route (which SF closes). Both divergence routes the paragraph discusses are structurally impossible here, so the illustration demonstrates nothing about the cmt/res registry — and the stratification "repair" guards a non-threat.

**Required**: Either make the coupling concrete (e.g., a `ρ_R` that *also* emits `attn`, or a `needs_attention` reading a type `ρ_R` writes) so the failure is genuinely instantiated, or state plainly that cmt/res is structurally non-divergent (its rules' domains and emissions are type-isolated) and illustrate Q4's "locally disciplined, globally divergent" with a separate construction rather than as a "let … also" perturbation of this registry.

### Issue 3: the "H-SFAIR = strong-scheduling form of regime (i)" identity is stated three times

**ASN-0133, H-SFAIR and Q6**:
- H-SFAIR: "H-SFAIR is the strong-scheduling form of regime (i), not a disjoint second route."
- Q6 (mid): "supplied directly, or by its strong-scheduling form, strong fairness (H-SFAIR)."
- Q6 (end): "only regime (i) — reached either by an eventually-idle environment directly or, equivalently, by its strong-scheduling form H-SFAIR — reaches and holds quiescence"

**Problem**: The same structural identity is asserted in three non-example locations. The same pattern recurs with the Q8/re-entry parenthetical, near-duplicated across adjacent claims (Q1: "a later environment step may re-arm a trigger — re-entry, Q8 — but that is fresh external input, not a fire") and reasserted in Q6 ("Cases (2) and (3) are Q8's re-entry at top level"). This is the "multiple paragraphs in different sections defer to the same downstream location" / "say the same thing in different words" accretion the anti-bloat classifier targets.

**Required**: State the H-SFAIR↔regime(i) identity once (at H-SFAIR, where it is defined) and let Q6 cite it; collapse the two Q6 restatements to a single reference. Keep one Q8/re-entry pointer.

### Issue 4: axiom-justification meta-prose on the hypotheses

**ASN-0133, The rule model**:
- H-FIN: "The demand is universal over the contract's admissible choices, not merely that some finite set exists: a body free to choose an infinite set would leave the fire with no post-state Σ'."
- H-ATOM: "environment steps fall between fires (H-FAIR), never within one, so the post-state extinction test (X-DEF) stays well-posed even for a non-monotone trigger."
- "Triggers: inline or by reference": "so recognizability is not unconditional relative to PR-DISC: PR3a delivers expand(a) ∈ PL exactly under PR-DISC, its acyclicity (PR2) itself proved under PR-DISC, and absent the discipline a raw pdef deposit may self-reference or cycle, leaving expand non-terminating and the trigger no PL term to evaluate."

**Problem**: The H-FIN and H-ATOM trailing clauses explain *why the hypothesis is needed* (forward-justifying against X-DEF, "would leave no post-state") rather than stating it. The Triggers paragraph re-derives the PR-DISC dependency chain (PR3a-under-PR-DISC, PR2-under-PR-DISC, raw-deposit-cycle) — substantive content buried in defensive restatement. These are the "new prose around an axiom explains why it is needed" pattern.

**Required**: H-FIN states the universal-over-admissible-choices demand (that is its content — keep that, drop "not merely … no post-state"); H-ATOM states no-interleaving (drop the X-DEF well-posedness rationale, or move it to X-DEF). Compress the PR-DISC conditionality to its claim: pdef-triggers require PR-DISC for expand-termination, so Q0's PL-membership is conditional for them; inline-triggers are unconditional. The dependency chain need not be re-walked.

## OUT_OF_SCOPE

### Topic 1: a fairness-realizing scheduler and the turn/serialization model H-SFAIR's satisfiability needs
**Why out of scope**: The note correctly identifies (in "What this note doesn't cover") that H-SFAIR is satisfiable only under a turn-fairness it neither states nor derives, and that the conditional theorems stand regardless. Constructing such a scheduler and proving its fairness is genuinely a future/implementation-layer ASN, not a gap here.

### Topic 2: the `pd_extinct` (SF) certificate class
**Why out of scope**: OQ1 flags that SF membership is the load-bearing *uncertified* check and proposes a designated certificate class. That is catalog growth for a future ASN (it depends on ASN-0130's certificate machinery), not a defect in this note's claims.

VERDICT: REVISE
