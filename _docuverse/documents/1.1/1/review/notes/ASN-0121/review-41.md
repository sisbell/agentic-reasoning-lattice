# Review of ASN-0121

## Verification performed

Before the verdict, the load-bearing derivations were checked independently:

- **FL-DEF forcing argument.** With soundness weakened to `sat` alone, both `R_min` and `R_max` satisfy the two demands; the addressability conjunct closes exactly that slack. The uniqueness argument is genuine, not decoration.
- **`nullified` locality and monotonicity.** `L_R^Σ` is selected from `dom(Σ.L)` by arity-3 and slot-3 coverage tests on stored values, so it is a function of `Σ.L`; F-PRES holds it fixed on every non-K.λ step, and R6a covers K.λ. The induction to `→*` is sound, and the vocabulary mismatch between ASN-0086's `→` and ASN-0047's is handled correctly — R6a is applied only at K.λ, the one operation the two vocabularies share with identical link-store contract.
- **FL-WP, all three cases.** Case (a)'s `L_R^{Σ'} = L_R^Σ` is established from the ordinariness cut (correctly on retraction-*relation* membership, not coverage class alone — the higher-arity retraction-typed link is routed to (a), consistent with ASN-0086's triple restriction). The ghost-pre-coverage conjunct is genuinely non-vacuous (freshness against `dom(Σ.L)` does not discharge it), and Trace 7(a) witnesses it. Case (b)'s existential split over `L_R^Σ ∪ {(b, F_b, G')}` is exact, the self-retraction term is live only there, and (a)/(b) exhaustively partition the fresh-link space. Case (c)'s membership equation is derived in both directions, which is what makes the wp weakest. The exhaustiveness argument for "K.λ is the unique result-changing transition" covers existing non-members (¬sat persists by L12; nullified persists by R6a) and exit under ordinary K.λ (barred by case (a)'s `L_R` fixity).
- **Tumbler arithmetic in the traces.** All checked concretely: the wide element-rooted home span `p ⊕ ℓ = [1,0,1,0,2,1,1,1]` is computed correctly and the document tumbler `[1,0,1,0,2]` does lie in the span (divergence at position 5 above `p`, proper prefix below the reach); all sibling addresses are equal-length and hence prefix-incomparable; the link sub-allocator frontiers in Traces 4, 6, 7 are contiguous (`[2,1]…[2,6]`, `[d'.0.2.1]`), so the worked stores are reachable on the link side; `H_node = ([1], δ(1,1))` covers exactly `{t : t₁ = 1}` per PrefixSpanCoverage; Trace 7's result `{r₁}` is right — `b` self-nullifies, `ℓ` fails the type slot and is independently born-nullified, `a₁–a₃` fail `Θ_ρ`.
- **FL-JUNK, FL-MON, FL-STB, FL-RET, FL-REACH.** Each proof consumes its hypotheses exactly: FL-JUNK's weaker `nullified(Σ') ∩ dom(Σ.L) = nullified(Σ)` is the right hypothesis (born-nullified junk is correctly admitted); FL-STB's routing through F-CIL satisfies F-CIL's predicate-locality condition since both `nullified` and `sat` read only `Σ.L` and query data; FL-REACH(d)'s restriction to *satisfying* links is what blocks the `q = (∗, ∅, ∗, ∗)` counterexample to the bare discoverable union, and the strictness witness (satisfying addressable orphan) is correct.
- **Boundary coverage.** Empty request component vs wildcard (zero vs unit), empty *stored* from/to endset (link-side zero, admitted only under the wildcard), ghost type addresses, higher arity, self-retraction, retraction-of-retraction non-restoration, residence at node/account/document granularity, and the element-rooted home-span edge case are all handled with explicit computations rather than gestures.
- **Cross-ASN citations** are confined to foundation ASNs (0034, 0043, 0047, 0086, 0093, 0098, 0127); the bare labels (S0, L3, L4, L9, L10, L12) resolve to foundation claims. No foundation notation is reinvented — `addressable` is correctly flagged as new over ASN-0086's `nullified`, and the `findlinks_FTT` subscript avoids colliding with F-FIND, with the non-restriction relationship witnessed in both directions.
- **Anti-bloat scan.** The candidate meta-prose sites (the FTT-subscript paragraph, the wp scope note, FL-JUNK's hypothesis-choice discussion, the FL-WP(c) directionality remark) were each examined; all carry content that is consumed later in the document (the slot-regime/range/dynamics differences ground FL-REACH and FL-WP; the scope note fixes what the displayed wp's mean; the hypothesis discussion bears on lemma strength). The single forward deferral ("derived below, once `→` is fixed") resolves two paragraphs later. No paragraph imagines a precondition-excluded case, no axiom is surrounded by why-it's-needed scaffolding, and no two paragraphs duplicate each other.

## REVISE

No REVISE items.

## OUT_OF_SCOPE

### Topic 1: Result ordering and enumeration order
Nelson's phrasing ("returns a list of all links") implies an ordering; FL-DEF specifies the answer as a set and leaves enumeration order unconstrained.
**Why out of scope**: Ordering and incremental delivery belong with the paginated variant FINDNEXTNLINKSFROMTOTHREE, which the scope list explicitly excludes; the set-level specification is the correct abstraction boundary for this ASN.

### Topic 2: Version- and federation-scoped inquiry
**Why out of scope**: Both are already recorded as Open Questions in the ASN itself — inquiry against prior states/versions and cross-store completeness are new territory, not gaps in the current-state operation specified here.

VERDICT: CONVERGED
