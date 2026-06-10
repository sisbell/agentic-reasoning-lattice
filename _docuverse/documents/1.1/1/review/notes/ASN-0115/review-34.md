# Review of ASN-0115

The mathematics is sound. I checked each of R1–R11 against its proof sketch and the foundation contracts, and worked the R6/R8/R9/R10/R11 instances by hand: the Confinement lemma discharges correctly via TumblerAdd + T5, the R6 no-interior-hole property holds (it falls straight out of D-SEQ★'s contiguity of `[1, n_S]`), R7's link/content asymmetry is handled honestly, and R8's link-vacuity argument (CL-OWN forces `d = origin(a) = d'`, then CL-UNIQ forces `v = v'`) is airtight. No correctness or missing-conjunct defects.

The findings below are all the accretion patterns the `review-mode.anti-bloat` classifier asks for — and the git log (`tighten co-delivery non-disclosure prose in three sites`) confirms one of them is a live, partially-addressed concern.

## REVISE

### Issue 1: The Confinement lemma imports arrangement/C0a context into a purely geometric claim
**ASN-0115, "What a spec-set is, and what delivery is" (Confinement lemma)**: "For a populated named subspace (`V_{s₁}(d) ≠ ∅`) this is ASN-0058's C0a (PrefixConfinement), established there for a content reference; the proof below extends it to the case the V-spec definition also admits — `V_{s₁}(d) = ∅`, where C0a's `V_{u₁}(d_s) ≠ ∅` precondition fails — and rests only on the span's structure, not on which positions `d` binds."

**Problem**: The lemma statement names no document `d` — it is a fact about span geometry `(s, ℓ)` alone — and the three-line proof uses only TumblerAdd (reach copies the prefix below the action point) and T5 (ContiguousSubtrees). The proof is entirely case-independent in `V_{s₁}(d)`. So this sentence introduces `d`, `V_{s₁}(d)`, the `∅`/`≠∅` split, and C0a's precondition purely to narrate the lemma's provenance relative to a foundation result it does not use. The sentence even tells you the split is irrelevant ("rests only on the span's structure"). This is meta-prose around a self-contained geometric lemma — the reader must skip ~60 words of foundation-relationship before reaching a proof that ignores all of it.

**Required**: Delete the sentence; reduce any wish to acknowledge the kinship to a bare parenthetical citation (e.g. "(generalizes ASN-0058 C0a)"). The lemma statement and its proof stand alone.

### Issue 2: The transclusion non-disclosure guarantee is stated three times
**ASN-0115, R8 box / "Second" emphasis paragraph / Synthesis**:
- R8 box, clause (iii): "The sharing is a fact of *resolution*, not of the delivered output: each item carries the value `Σ.C(a)`, never the address `a` (R1), so the co-delivery is byte-indistinguishable from the delivery of two coincidentally-equal contents at distinct addresses (S4) and discloses nothing about the shared origin."
- "Second" emphasis point: "…The box already records the complementary half — that the output itself, carrying values not addresses (R1), is byte-indistinguishable from coincidental value-equality (S4) and so discloses nothing."
- Synthesis: "…but co-delivery discloses nothing about the sharing that two isolated single-span deliveries would not — the shared address is a fact of resolution, not of the output (R8)."

**Problem**: The same "fact of resolution, not of the output / byte-indistinguishable from coincidental value-equality (S4) / discloses nothing" point lands in all three sites. The "Second" paragraph self-incriminates — "The box already records the complementary half" — which is exactly the tell that a paragraph is restating content it has already cited. Its one genuinely new clause is "co-delivery … establishes nothing … that two separate single-span deliveries would not"; everything from "The box already records…" onward duplicates box clause (iii). (Within the same "Three points" structure, points 1 and 3 *do* add content — copy-vs-reference framing, the R3-forcing argument, the absent `consolidatespans` evidence — so they are not the problem; point 2 is.)

**Required**: State the non-disclosure guarantee once, in the R8 box. Trim the "Second" point to its new claim (co-delivery carries no more than two isolated deliveries) and drop its box-restating tail. Let the Synthesis carry at most a one-clause back-reference, not a re-derivation.

### Issue 3: R6 proof's `act = ∅` parenthetical over-splits a vacuous case
**ASN-0115, "Partial delivery: the gap is legal, not an error" (R6 proof)**: "(If instead `act = ∅` while `V_S(d) ≠ ∅`, … either the start's prefix differs from `[S, 1, …, 1]`, putting the slice wholly under an unrelated prefix, or the prefix is canonical but `s_{m_S} > n_S`, putting the slice past the frontier. Only the latter is a terminal overrun past the frontier in the stated sense; but in both the load-bearing negative property holds — the slice meets no bound position, so the span punches no interior hole within the active range.)"

**Problem**: The whole payload of this parenthetical is its last clause: when `act = ∅` the slice meets no bound position, hence no interior hole. The preceding two-way enumeration of *how* the slice misses `V_S(d)` ("prefix differs" vs "past frontier") changes no conclusion — both branches end at the same negative property — and imagines structure the case (`act = slice ∩ V_S(d) = ∅`) has already collapsed. It is defensive detail a reader must work past to reach the one-sentence conclusion.

**Required**: Replace the two-way split with the single observation that drives it — when `act = ∅` the depth-`m_S` slice is disjoint from `V_S(d)`, so it contains no bound position and punches no interior hole; the terminal-overrun half of R6 is then vacuously satisfied. (Minor: the no-interior-hole half for the substantive case is itself immediate from D-SEQ★'s contiguity of `[1, n_S]` — every `k ≤ n_S` is bound — so the canonical-start derivation is needed only for the *terminal-overrun* characterization, not the *no-hole* one. Worth noting if the proof is being trimmed anyway.)

## OUT_OF_SCOPE

The five Open Questions (inline content provenance, permitted outright failure, dangling resolved references, channel faithfulness, single straddling span) correctly defer the topics adjacent to this ASN's boundary, and the link-structure operations (READLINK/FOLLOWLINK) are properly deferred at R10. Nothing additional belongs here — the ASN delivers link *references* and stops, which is the right cut given the scope list.

VERDICT: REVISE
