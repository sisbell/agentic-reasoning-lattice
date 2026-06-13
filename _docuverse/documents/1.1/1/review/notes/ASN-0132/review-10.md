# Review of ASN-0132

The mathematics here is sound. I checked CN-DEF's well-definedness (finite computable subset of `dom(Σ.L)`, L-fin + FL-DEC), CN-ENUM's structural equality (both sides are the cardinality of one set), the CN-MONO weakest-precondition derivation (it reconstructs FL-WP(a) of ASN-0121 correctly — `sat(ℓ,q,Σ') ∧ ¬(E (b,F',G') ∈ L_R^Σ :: ℓ ∈ coverage(G'))`, with the second conjunct collapsing under the unit-depth discipline via R0a), the CN-UNIT(d) version-refraction argument against J4 (forking does K.δ/K.μ⁺/K.ρ and "no other elementary steps," so `Σ.L` is untouched), and the worked example arithmetic (`coverage(F) = [1.0.1.0.1.0.1.5, 1.0.1.0.1.0.1.13)`; `a₄`'s reference diverges at the document component `2>1`; `nullified(Σ)={a₂}` by equal-length prefix-incomparability; count = 2, all-wildcard = 4, `H₂` = genuine CN-ZERO). All of it holds. Depth, edge cases, and concrete grounding are present and strong.

The findings are prose, not correctness — which is what the `review-mode.anti-bloat` classifier asks me to look for. The note carries revision scars and a thrice-told side-point that a precise reader must work around.

## REVISE

### Issue 1: Revision scar and citation roadmap in CN-MONO
**ASN-0132, CN-MONO (wp derivation, first paragraph)**: "*(This is the substance an earlier draft mis-attributed to E-INV, ASN-0127 — which speaks of the slot-agnostic `matches(a, I, ·)` predicate, not the four-slot `sat`, and which says nothing of addressability at all, so it delivers neither half of what the step needs.)*"
**Problem**: This parenthetical establishes nothing in the proof. The pre-existing-link argument already stands on L12, LP13, CN-LOC, and the `L_R^{Σ'} = L_R^Σ` step; the note about which lemma a *prior draft* wrongly cited is pure scar — exactly the "prior finding's content relocated rather than removed" pattern. A correct proof does not footnote the citations it does *not* use. The same section carries a citation-roadmap filler: "**Each remaining fact is cited where it lives.**" — a meta-sentence announcing structure rather than advancing the argument.
**Required**: Delete the E-INV parenthetical outright. Drop "Each remaining fact is cited where it lives"; the per-fact citations that follow it stand on their own.

### Issue 2: The resolution-boundary separation is stated three times
**ASN-0132, intro / CN-ZERO / CN-STAB**: intro — "the discrepancy will live precisely in the resolution, never in the count"; CN-ZERO — "This is the same separation foreshadowed earlier: the instability lives in the resolution, not in the count"; CN-STAB — "The one caveat is the one already drawn at the resolution boundary, and CN-STAB makes it precise."
**Problem**: The general separation (a fixed resolved `q` is what the operation specifies; re-phrasing/re-resolving produces a *different* `q`) is asserted in the intro, re-asserted nearly verbatim in CN-ZERO, and re-opened in CN-STAB. The two *applications* are distinct and worth keeping — the empty-request zero (CN-ZERO) and the re-phrasing-after-edit caveat (CN-STAB) — but each re-derives the general point first, and the explicit back-pointers ("the same separation foreshadowed earlier," "already drawn at the resolution boundary") are the signature of redundancy. The intro's foreshadowing duplicates CN-STAB's content in advance.
**Required**: State the general separation once (the intro is the natural home, but trimmed to the setup, not the foreshadow of CN-STAB). At CN-ZERO and CN-STAB, keep only the specific application and drop the re-derivation and the "as foreshadowed / already drawn" framing.

### Issue 3: Defensive framing of the `nullified` clause in CN-STAB
**ASN-0132, CN-STAB (second paragraph)**: "**We state no separate clause fixing `nullified`, and one would be redundant**: `nullified(Σ)` is itself a function of `Σ.L` alone ... The equality of nullified sets is thus a *consequence* of the hypothesis, **not an extra demand on it** ..."
**Problem**: The load-bearing content here is correct and should stay (nullified is `Σ.L`-determined, so `Σ'.L = Σ.L` entails `nullified(Σ') = nullified(Σ)`, so F-PRES's single hypothesis suffices). But it is wrapped in a justification of a clause the ASN *declines to add* — "we state no separate clause... one would be redundant... not an extra demand." That is defensive prose answering an objection rather than proving the lemma.
**Required**: State the implication directly: "Since `nullified(Σ)` is selected from `L_R^Σ`, which `Σ.L` determines, the hypothesis `Σ'.L = Σ.L` entails `nullified(Σ') = nullified(Σ)`; hence F-PRES (link-store preservation alone) discharges the precondition." Drop the "we state no separate clause / not an extra demand" framing.

## OUT_OF_SCOPE

None. The note handles its boundaries cleanly: it cites ASN-0127's existence/discovery taxonomy (CN-ORPHAN via `discoverable_from`/FL-REACH/LP17/LP18) rather than rebuilding it; it defers delivery (CN-OBT), federation, caching, concurrency, and content-identity-vs-position counting to the Open Questions; and CN-OBT's deliverability disclaimer bounds the count's meaning without specifying delivery.

VERDICT: REVISE
