# Review of ASN-0094

I read this carefully — Sh-conf axiom, Sh0–Sh4 preservation theorems, the LinkAddressNotPrefixOfEmit lemma and its proof, the EffectiveWpSimplification corollary (with the new Π_K conjunct), the Sh4 idempotency proof with Case D's `+1,−1` structural bound, the AllocatedAddressAntichain lemma's three-case split with the cross-domain sub-cases written out, the catalog rows and per-shape walkthroughs, and the appendix's NAT-card/NAT-sub derivations. The proofs are substantially rigorous, edge cases are systematically exercised, and the stratification is honest and acyclic.

A few items worth tightening before this is built on.

## REVISE

### Issue 1: NAT-card additivity walkthrough mislabels a sub-case
**ASN-0094, Appendix, "Worked interleaved instance — `S₁ = {2, 7}`, `S₂ = {3, 5}`"**: "Sub-case A on `S₁'`, then base case on `S₁'' = ∅, S₂'' = {3}` collapsing through the symmetric ladder"

**Problem**: At the level where the partial union is `{2, 3}`, `max({2, 3}) = 3 ∈ S₂'' = {3}`, so *Sub-case B* fires on `S₂''` — not Sub-case A on `S₁'`. After that Sub-case B step the residual is `{2} ∪ ∅`, which is `|{2}| = 1`, not the base case; one more step (Sub-case A on the residual `{2}`) is needed to reach `|∅| = 0`. The recursion does terminate correctly (I traced it: levels 0 → 1 → 2 → 3 → base unwind to `4 = 2 + 2`), but the walkthrough's labeling does not match the actual recursion the formal proof prescribes.

**Required**: Either correct the labels ("Sub-case B on `S₂''`, then Sub-case A on the residual `{2}`, then base case at `|∅| = 0`") or expand the example to show each recursion level explicitly. This is the one example the appendix offers to demonstrate the additivity covers interleaved configurations the trichotomy-on-extremes route did not — readers checking it should see the case labels firing as the formal proof says they will.

### Issue 2: Generality witness counterfactual obscures what the general additivity argument actually buys
**ASN-0094, Lemma — LinkAddressNotPrefixOfEmit, "Generality witness (counterfactual) — Sub-case II.B at `#w ≥ 2`"**: The example exhibits Step II.1's additivity firing non-trivially against a hypothetical `a` with `zeros(a) = 4` — a value K.λ cannot emit. The "Why the general additivity argument is preserved" paragraph cites *citation purity* and *decoupling from substrate-reach assumptions* as the reasons to keep the general form.

**Problem**: Step II.1's contribution at every substrate-reachable case is the trivial `3 = 3 + 0` — `zeros(w)` is forced to 0 by the preamble's `zeros(a) = zeros(b) = 3`. The substantive contradiction at substrate-reachable inputs surfaces at Step II.2 or II.3, not at Step II.1. A careful reader following the proof to find where the *general* additivity is load-bearing concludes it is load-bearing only at hypothetical inputs the framework's hypothesis `a := a_emit(Σ, d)` rules out. The framing "the proof's `#w ≥ 2` case is *only* applicable in regimes the framework doesn't reach" is honest, but the *Generality witness* heading and the multi-page exposition risk suggesting the additivity does work the proof relies on.

**Required**: Either reduce the counterfactual to a sentence acknowledging the regime is unreachable (and Step II.1's additivity is trivial-but-cited for citation purity), or drop the counterfactual and replace it with a one-line note: "Step II.1's additivity is trivial under the current substrate scaffolding (it derives `zeros(w) = 0` from `zeros(a) = zeros(b) = 3`); the general form is retained so the proof closes against any future scaffolding admitting deeper K.λ emissions." Either compresses several pages to a paragraph and removes the misleading suggestion.

### Issue 3: Empty-`S_d` baseline computation buried in additional worked examples
**ASN-0094, "Additional Worked Examples — Coverage under SingleHomeCoverageDiscipline", "Empty-`S_d` baseline at Σ_0 (before any Coverage emission)"**

**Problem**: The `latest_K_for_addr(d) = ⊥` empty-baseline case is *the* path consumers must dispatch on every time the relation has not yet emitted at the target, but the worked computation sits in Additional Worked Examples — after the main Comment walkthrough — rather than at the template's definition in the NonIdempotentDirectedPair Coverage sub-section. A reader scanning the catalog row to see how to use `latest_K_for_addr` reaches the *Partiality propagation rule* prose but not the worked dispatch table until much later.

**Required**: Move the empty-`S_d` evaluation table (the one listing `latest_K_for_addr(d_subject) = ⊥`, `from₁(latest_K_for_addr(d_subject))` undefined, etc.) into the NonIdempotentDirectedPair section adjacent to the `latest_K_for_addr` template definition. The Coverage walkthrough can then reference it rather than re-walk it.

## OUT_OF_SCOPE

### Topic 1: Cross-process coordination protocol for the Sh4/FDD contracts
The Open Questions section flags this explicitly as a *scope boundary*. The single-process substrate commitment is correct for the current framework; characterizing the minimum cross-process protocol that preserves Sh4 belongs in a follow-on ASN that extends scope rather than fixes a gap here.

### Topic 2: Promoting the per-shape body-shape uniformity aspiration to a procedural recipe
The framework explicitly downgrades per-shape body-shape uniformity from a commitment to an aspiration, and records "Sharpening the aspiration to a procedural recipe... is recorded as an open work item; the present draft does not undertake it." That is the right call for this ASN — sharpening it would require introducing a body-shape derivation procedure, which is a separate piece of work.

VERDICT: REVISE
