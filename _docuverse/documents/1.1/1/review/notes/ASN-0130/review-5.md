# Review of ASN-0130

I checked every numbered claim against the foundation extracts, with particular pressure on the four places a note like this usually breaks: the wp equivalences, the acyclicity argument under re-registration, the substitution-typing proof, and the well-posedness of certification. Summary of what was probed and held:

- **PR-ENC/PR-ENC-uniq**: the `shift(x,1) = inc(x,0)` identity is correctly grounded (TA5(c) + TA5-SigValid + OrdinalShift), and the uniqueness argument consumes only prefix-freeness plus S0 — it holds against every store, as claimed. The overlapping-suffix case is acknowledged and correctly disarmed by start-anchoring.
- **PR-SIG**: the parse/type stratification is sound; the mutual-reference example genuinely shows content-intrinsic typing would be ungrounded; `sig`'s induction on first-registration order is well-founded, and the re-derivation-identical claim at later deposit events follows from S0 + fixed referent signatures + determinism of the pass. The off-discipline failure mode (raw Multi-gate deposit minting a tuple with undefined `sig`) is stated rather than hidden.
- **PR0 wp**: I verified both directions. Hit ⇒ POST-ref needs canonical shaping (discipline); the note supplies the off-discipline counterexample (`addrs(F') = {a, a.x}` with equal coverage — I0a's separating pair). C3-necessity at the miss needs the miss-plus-shaping step "no active tuple denotes `a` at all," which I confirmed: under discipline, any active tuple denoting `a` would carry the unique run at `a` (PR-ENC-uniq) and so be I0-equal — a hit. Born-nullified deposits therefore falsify POST-ref exactly when ¬C3. The attainability convention is applied consistently with I6/DR.
- **PR1**: permanence is argued per step kind (K.σ/K.λ_sh frame C; K.α fresh-extends) plus induction, with L12 carried across genuine `→_sh` steps by B2's transition-invariant clause via RP-b — the correct citation chain, not a wholesale transfer.
- **PR2**: the event-wise formulation survives de-registration/re-registration. (a) holds because (iv)'s witness must be *active*, hence a prior deposit (born-nullified tuples never enter any active subset, R6a/R6c). (b) closes the self-reference loop by induction along the derivation, and the hit branch is independently excluded. The DAG and expansion termination follow; allocation order is correctly noted as irrelevant.
- **PR3/PR3a**: expansion is a function of content alone (no `sig` consulted; all renaming and order choices fixed), invoked only on ever-registered addresses where PR2's rank makes the recursion well-founded. The substitution induction is genuinely carried out: WT-α/WT-W identify the only two name-touching points of WT, the "surviving reference nodes sit under author binders only" observation (replacements are pure) is what makes the freshness bookkeeping close, and the simultaneous-to-sequential reduction plus last-parameter-first PC2 discharge is correct.
- **PR-VIEW/PR5/PR5a**: the view-independent class exactly complements PC3+UV's view-sensitive constituents (I checked the residuals: `is_filtered`, `is_in_chain`, `tip`, `target_of`, `age`, `targets_keyed` are admissible for view-independence but correctly fail PR5a(iii) since no PD0 rule admits them — the two gates compose without a leak). The parameter-as-bound-constant reading consumes only fixity, which PD0's ground already uses; Tup-sorted parameters are impossible (`Γ_D` is Codom-sorted). The lint's coverage-exactness argument at starts is correct in both cases (same-origin: equal lengths under sibling advance; cross-origin: prefix-incomparable anchors + length-ordering of prefixes).
- **Worked composition**: step 4's refusal of v1 (active slice not grow-only) and acceptance of v2 (∃ over grow-only `L_M` with step-constant body) are exactly PD0's rules applied; step 5's residence-vs-registration distinction is right.
- **Boundaries**: n = 1 runs, k = 0 closed terms, first-ever registration (empty `A_pdef` forces reference-free ground), born-nullified first registrations (later re-registration deposits afresh; `e₁` anchored correctly), supersession branches, certification of never-registered and de-registered targets — all covered in the text.

## REVISE

None. I found no claim whose proof is missing, no unstated case, and no foundation conflict. The two depth requirements most often skipped — non-trivial wp analysis and a concrete worked example — are both present and substantive (the wp counterexamples off-discipline are the strongest material in the note).

## OUT_OF_SCOPE

### Topic 1: Certification-time endorsement of de-registered referents
PR5a(i) demands an *active* target on the "no new endorsements against withdrawn registrations" principle, but `certify_pd_stable` will certify a definition whose *referents* have since been de-registered — the certificate is sound (the certified expansion is content-determined), yet the endorsement principle is applied non-transitively without comment.
**Why out of scope**: this is the same policy axis Open Question 3 already holds open for registration and evaluation; the surface's behavior is determinate and sound either way, so the resolution belongs to the note that settles OQ3, not to a revision here.

### Topic 2: Operational realization of `sig`
`sig(r)`'s sort component is derived, not stored; PR0(iii)'s "one finite signature lookup per reference node" is, operationally, a recursive recomputation down the reference DAG unless an implementation caches. The spec pins determinacy and termination, which is all correctness needs.
**Why out of scope**: recompute-vs-cache and validation cost are implementation strategy; the note correctly parameterizes them out, as it does the encoding bytes.

### Topic 3: Expansion size bounds
DAG-shared references unfold into a tree under `expand`, which can grow exponentially in the reference depth. Termination and purity are unaffected.
**Why out of scope**: complexity of evaluation-by-reference is new territory (a cost model for the predicate layer), not an error in the semantics committed here.

VERDICT: CONVERGED
