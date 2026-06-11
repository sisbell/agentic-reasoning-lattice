# Review of ASN-0128

The note is technically strong — I checked the I0 minimal-elements identity (both directions hold), I1a's induction (all step kinds covered, including the K ~ R case), I6's wp (necessity and sufficiency both check out), DR's prefix-exclusion computation (the strict-prefix enumeration is complete), and the wrapper's hit-branch re-establishment of single-tuple scope (sound via R6b and R0a). The REVISE items below are two rigor gaps, three precision/specification gaps, and three accretion findings under the anti-bloat classifier.

## REVISE

### Issue 1: DR's central derivation rests on an uncited transfer, while the fully-cited alternative is disavowed
**ASN-0128, Standard registrations (DR)**: "The target `a`, being a link address at Θ, satisfies L1 and L1b there (ASN-0043's invariants, transferred)" — followed by "(The same conclusion follows by instantiating R0a — FlatLinkDomain, ASN-0086, via ASN-0126's B2 and RP-a — at the *post-state* of the prospective emit … We prefer the state-local computation above, which appeals to no prospective step.)"
**Problem**: Everywhere else the note names the exact carrier for every transferred fact — B2/B3, RP-a/RP-b/RP-c, with RP-a even inventorying R0a explicitly. Here, at the load-bearing step of the C3-vacuity proof, "transferred" names neither a per-state lemma asserting that every reachable state satisfies L1 and L1b nor the carrier chain; no such per-state result appears among the foundation claims, so the step is a hand-wave in the note's own citation discipline. Meanwhile the parenthetical alternative via R0a and RP-c is fully cited but explicitly disavowed — the note carries two proofs of one fact plus a preference remark, which is itself accretion.
**Required**: Pick one route. Either cite the precise per-state result delivering L1/L1b at reachable states and its carrier chain (as RP-a does for R0a), or adopt the R0a/RP-c derivation and delete the other. Drop the preference commentary either way.

### Issue 2: I1's irredundant-lists coincidence claim is asserted, not derived
**ASN-0128, Idem operational semantics (I1, hit clause)**: "where emitters present coverage-irredundant address lists — no listed address extending another — denoted-set equality and coverage equality coincide on the presented lists"
**Problem**: This rests on I0's minimal-elements identity (equal coverages force equal minimal denoted sets; for antichain lists, `addrs` equals its own minimal set, so the denotations coincide), but the identity sits unnamed in the middle of I0's long paragraph and the I1 claim cites nothing — the reader must reconstruct the chain. "X follows from Y" without the steps is a claim, not a proof.
**Required**: Label the minimal-elements identity in I0 (it is a real lemma with a two-direction proof) and cite it at I1's coincidence claim with the one-line derivation chain.

### Issue 3: retract_stale's counterfactual contradicts the wrapper's stated check discipline
**ASN-0128, BH4 (retract_stale)**: "were P0 re-evaluated per constituent, an invalid `d_retr` would void the batch only absent interleaving" — against DR: preconditions are "checked on every call, hits included, P0 first."
**Problem**: Under the actual design, P0 *is* evaluated per constituent — by the wrapper, on every call; the batch's entry evaluation is an additional check whose verdict the constituents' own checks then confirm by monotonicity. The counterfactual as phrased describes the factual design, so the front-truncation argument reads as the design refuting itself. The intended counterfactual is a batch whose admission is left *only* to the constituents' checks, with no entry evaluation.
**Required**: Rephrase the counterfactual ("were batch admission left to the constituents' own P0 checks alone…") and state explicitly that in the actual design both layers check and the per-call checks pass given the entry verdict.

### Issue 4: BH1's rewrite is underspecified under multiple read-filter registrations
**ASN-0128, BH1**: "the default view of `members(K')` is `{x ∈ members(K') : ¬is_filtered(x)}`" — against Denotation and views: "when some Unary type registered with BH1 has an active tuple whose F-coverage contains an address, that address is subtracted…"
**Problem**: `is_filtered` is defined per attaching type ("a membership predicate on the filter type's own active view"). Nothing forbids two or more BH1 registrations — `retired` ships with BH1 and an app may register another — and then BH1's equation does not say whose `is_filtered` applies, while the Views paragraph implies the union over all BH1 types. Also implicit but unstated: two BH1 types mutually filter each other's enumerations (each is an "other type" to the other).
**Required**: State the composition explicitly — subtract the union of all BH1-registered types' filtered sets (equivalently, conjoin `¬is_filtered` across them) — and say one sentence about mutual filtering between BH1 types.

### Issue 5: the example asserts BH3 predicates of a type never registered with BH3
**ASN-0128, An abstract registry example (Typed-reverse-lookup)**: "A separate emit of a different Binary type (say a hypothetical second `aux2`) at `F = a_p` with `G = [a_aux2]` gives `target_of(a_p, aux2) = a_aux2`, and `targets_keyed(a_p)` returns `{aux: a_aux1, aux2: a_aux2}`."
**Problem**: `target_of(·, K)` is BH3-unlocked, and `targets_keyed` joins "every Binary type K registered with BH3" — so the claimed output requires `aux2` to carry BH3, which the example never states. The example does not verify against the spec as written.
**Required**: Declare `aux2` Binary with BH3 attached, or drop it from the `targets_keyed` output.

### Issue 6: the same content stated twice — compatibility rationale, and is_in_chain semantics
**ASN-0128, R-C0 vs BH4; Denotation and views vs BH2**: R-C0: "every clause must be exercised by the machinery it conditions, and every clause is: BH1's `is_filtered` quantifies over Unary's `(a, F, ∅)` form, BH2's one-edge-per-tuple graph and BH3's `target_of` both read Binary's `|G| = 1`…"; BH4: "BH1–BH3 carry shape requirements because their machinery reads the shape's form — `is_filtered` quantifies over Unary's `(a, F, ∅)`, the walk and `target_of` read Binary's `|G| = 1`." Likewise Views: "`is_in_chain` is Boolean-valued but *enumeration-derived* … so an extension of a chain element does not satisfy it" against BH2: "membership in the walk's result list — exact denoted vertices, an enumeration-derived test, not a coverage test … so an extension of a chain element does not satisfy it."
**Problem**: Two pairs of passages in different sections saying the same thing in different words. R-C0's version is additionally a use-site inventory inside a well-formedness definition — the definition should state the compatibility table, not enumerate which machinery exercises each clause.
**Required**: One home per fact. Compatibility: the table/clauses in R-C0, the idem=⊥ derivation (which is real content) in BH4, no restatement of the shape-clause rationale in both. `is_in_chain`: define once in BH2; the Views section keeps at most the regime classification.

### Issue 7: deferral chain around the hit-clause "price"
**ASN-0128, I0 / AD / I1 / example**: I0: "priced where it bites, at I1's hit clause"; AD: "a divergence I0 argues and I1's hit clause prices"; I1: "The last exclusion bites exactly here, so here it is stated:"; example: "The second case pays I1's stated price."
**Problem**: Four sites narrate where one fact lives. This is the multiple-sections-deferring-to-one-downstream-location pattern plus document-ordering narration; the actual content — the suppressed-decomposition consequence and its `t`/`t.x` example — is correct and correctly placed in I1.
**Required**: Keep I1's statement. Reduce the other three to bare cross-references or delete them.

### Issue 8: recurring importance-announcement rhetoric
**ASN-0128, throughout**: "the scope is load-bearing" and "the choice is argued, not assumed" (I0); "The locus matters twice over" (I1); "an apparatus, not a remark … We follow the precedent" (The registration record); "RP-c is trivial for one reason worth stating" (RP); "The once-at-entry locus is load-bearing, not a convenience" (BH4); "Rejection is load-bearing, not a free error-convention choice" (S3); "We declare it because here it is load-bearing" (DR); "Two consequences of the wrapper's from-fill are worth naming" (S3).
**Problem**: Each sentence announces that the following argument matters rather than advancing it — defensive framing addressed to the reviewer, the kind that accretes across revision cycles. In every instance the argument that follows is real and stands without the preamble.
**Required**: Delete the announcements; keep the arguments.

## OUT_OF_SCOPE

### Topic 1: Operation result signatures and rejection algebra
The surface now has three outcomes — step taken with fresh address, no step with incumbent address, rejection with no address — but the operations carry no typed result signature, and whether a caller can discriminate a hit from a miss is unaddressed.
**Why out of scope**: The prose contracts (I6, DR) are complete on behavior; a formal result-type/API treatment is new territory for a successor, not an error here.

### Topic 2: Concurrency beyond the serialized reading
I4 explicitly inherits the sequential interleaved model ("concurrency has no semantics inside it") and analyzes the serialized race only.
**Why out of scope**: A genuine concurrent semantics — commutativity of independent emits, confluence of interleavings — is a deliberate non-commitment of the substrate model, not a gap in this note.

VERDICT: REVISE
