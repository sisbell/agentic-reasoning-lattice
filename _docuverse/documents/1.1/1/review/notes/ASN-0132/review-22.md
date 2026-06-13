# Review of ASN-0132

I checked each claim against its cited foundations and verified the worked example by hand. The technical content is sound: CN-DEF's well-definedness (finite subset of `dom(Σ.L)`, L-fin ASN-0093) holds; CN-LOC correctly reduces the count to a function of `Σ.L` (since `home(a)` is a projection of the address-key and `nullified`/`addressable` are `Σ.L`-determined); CN-UNIT's four reductions are each grounded (anchoring by the existential structure of `touch`; transclusion/appearance/version-refraction by CN-LOC, with the version case correctly resting on J4's "no other elementary steps" leaving `Σ.L` untouched); CN-ENUM is the trivial cardinality-of-one-set identity; and the CN-MONO wp derivation matches FL-WP(a)/(b) of ASN-0121 in both the ordinary and retraction cases. The worked store checks out address by address (homes resolve to `d₁`, `nullified(Σ) = {a₂}`, count `= 2`, all-wildcard `= 4`, the `H₂` zero genuinely non-degenerate), and the three-transition "census in motion" correctly exhibits `2→3` (CN-MONO ordinary), `3→3` (CN-STAB), and `3→2` (collateral nullification falsifying CN-MONO's hypothesis). No drift into implementation mechanics — the Gregory notes are clearly marked deviations, not requirements. No cross-ASN references outside the foundation set.

The findings are confined to accumulated meta-prose, consistent with the active anti-bloat classifier.

## REVISE

### Issue 1: CN-MONO carries proof-narration that explains its own hypothesis rather than executing the derivation

**ASN-0132, "Retraction and permanence" (CN-MONO derivation)**: In the ordinary case — "The contributions of dom(Σ.L) therefore sum to the same total at both states. Note where that came from: the CN-MONO hypothesis that no currently-counted link is nullified is here automatic, falling out for free from L_R^{Σ'} = L_R^Σ; we never had to invoke it. **The retraction case below is where it earns its keep.**" — and the backward-pointing mirror in the retraction case: "**The step the ordinary case got for free** — every link counted at Σ is still addressable at Σ' — is therefore not automatic here, precisely because L_R^{Σ'} ⊋ L_R^Σ."

**Problem**: The two-case wp derivation is required (the standards demand a non-trivial wp case) and is correct. But the math itself already shows the hypothesis is vacuous when `L_R` is unchanged and load-bearing when `L_R` grows; the surrounding narration ("we never had to invoke it," "earns its keep," "got for free," "not automatic here") states this same observation twice — once forward in the ordinary case, once backward in the retraction case — and a reader tracing the logic must skip past it. This is the forward/backward-reference accretion the anti-bloat classifier targets: prose explaining *why* the precondition is needed rather than discharging the proof.

**Required**: Keep both wp cases. Replace the cross-referenced narration with at most one consolidated remark (e.g., a single sentence after the retraction case: "The hypothesis is vacuous for ordinary links — `L_R` is unchanged — and essential for retraction links, which may withdraw a counted link"). Delete the "earns its keep / got for free" pair.

### Issue 2: CN-OBT restates CN-DEF plus a delivery-scope disclaimer, promoted to theorem status

**ASN-0132, "Cost, and the meaning of asking for a number" (CN-OBT)**: "countlinks_FTT(q, Σ) = N asserts that |{a ∈ addressable(Σ) : sat(a, q, Σ)}| = N. It does not assert that those N links are deliverable on demand. Delivery is a separate concern across a separate boundary (out of scope here)... obtainability on demand is a promise the count does not make **and must not be read as making**."

**Problem**: The positive half (`= N` means `N` links satisfy) is CN-DEF restated. The negative half is a disclaimer about content delivery (RETRIEVEV), which the Scope section already places out of scope, phrased defensively ("must not be read as making"). As a numbered THM the claim introduces no derived guarantee of the operation — its "derivation" is the disclaimer itself.

**Required**: Either demote CN-OBT to a one-line remark (the existence-vs-retrieval boundary is worth noting once), or give it genuine derived content beyond CN-DEF; and drop the defensive "must not be read as making" phrasing.

## OUT_OF_SCOPE

The six Open Questions correctly defer the future territory this note touches — the V-spec/I-address agreement invariant, the count/enumeration concurrency discipline, count caching, the fragmentation-deduplication guarantee, count-vs-enumeration cost asymmetry, and federation. These are appropriately out of scope, not gaps in this ASN. The retraction-induced *decrement* of the count is not given a standalone claim, but it is adequately covered at the per-link level by CN-RETRACT (`a ∈ nullified ⟹` contributes `0`) combined with CN-LOC, and demonstrated in the worked example; no separate claim is required.

VERDICT: REVISE
