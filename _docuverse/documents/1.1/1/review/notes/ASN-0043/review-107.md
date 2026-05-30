# Review of ASN-0043

## REVISE

### Issue 1: Defensive non-dependency meta-commentary in the L9 proof
**ASN-0043, L9 Case A**: "...any `b ∈ dom(Σ.L)` with `b = a` would have `home(b) = home(a) = d'`, contradicting the empty-set hypothesis. **No appeal to GlobalUniqueness is needed.**" and earlier "...the same construction yields the freshness `a ∉ dom(Σ.L)` (for L11a) and the producibility chain (for L1c)."
**Problem**: "No appeal to GlobalUniqueness is needed" is pure meta-commentary about what the proof does *not* depend on — it advances no reasoning; a clean proof simply does not invoke what it does not need. The parenthetical "(for L11a)...(for L1c)" is a use-site inventory annotating which downstream property each output serves. Both are exactly the reviser-drift patterns this note's anti-bloat classifier targets.
**Required**: Delete the non-dependency sentence and the "(for L11a)/(for L1c)" annotations; let the construction stand on its object-level content.

### Issue 2: L11a motivates S7d by imagining its absence rather than citing it
**ASN-0043, L11a**: "Per-chain conformance alone leaves the seeds unrelated — two links homed in different documents would otherwise yield two chains from two seeds that need not share a root. S7d (DocumentAllocationDiscipline, ASN-0036) closes this gap..."
**Problem**: This paragraph explains *why S7d is needed* (a counterfactual about what would happen without it) rather than stating what the proof uses. The load-bearing step is only "each seed `home(a)` is a node of 𝒯 by S7d, so each link chain is a subtree of 𝒯." The counterfactual setup is the "new prose explains why the premise is needed" pattern.
**Required**: Drop the counterfactual sentence; invoke S7d directly to place each seed in 𝒯.

### Issue 3: The fresh-sibling-existence argument is duplicated across L9 Case B and L11b
**ASN-0043, L9 Case B and L11b ("Construction of fresh `a'`")**: both run the identical argument — enumerate the `inc(·, 0)` sibling stream from an existing link, invoke L-fin (finiteness) + T10a.7 (injective/infinite enumeration) to extract the least fresh sibling, then establish `home`/`zeros`/`#E` invariance via CPP and TA5(c)/TA5-SigValid.
**Problem**: FSP already factors out the *conformance* half of these extensions but takes freshness (h1) and producibility (h2) as hypotheses, so the *existence of a fresh conforming sibling* is re-derived verbatim in two places. This is the "two paragraphs say the same thing in different words" pattern, and it will keep re-accreting on each cycle.
**Required**: Promote the fresh-sibling-existence construction to a companion local lemma (e.g., "FreshSiblingExistence": given a conforming `a ∈ dom(Σ.L)`, there exists `a' = incⁱ(a,0) ∉ dom(Σ.L)` with `home(a') = home(a)`, `subspace_I(a') = s_L`, `zeros(a') = 3`, `#E(a') = #E(a)`, T4-valid), and have L9 Case B and L11b cite it, discharging FSP's h1–h3 in one line each.

## OUT_OF_SCOPE

### Topic 1: Global content-subspace constant
**Why out of scope**: The first Open Question (extending content-side disjointness from the `s_C`-slice to all of `dom(Σ.C)`) is a genuine future-ASN concern; L0a's scoping to `dom(Σ.C)|_{s_C}` is a sound deliberate limitation of this ASN, not an error.

### Topic 2: Link/arrangement consistency under transclusion
**Why out of scope**: Whether `Σ.L` must stay consistent with `Σ.M` (Open Questions 2, 7, 8) concerns operations and cross-store invariants that belong to a later operations/arrangement ASN.

VERDICT: REVISE
