# Review of ASN-0133

This is a careful note, scrupulously honest about the meta-level/substrate boundary, and the core proofs (Q0, Q1, Q5, Q5a, Q-EXT, Q6) are sound. The H-W-as-foil narrative is genuinely illuminating, and the SF+extinction route (Q5a) is correctly shown to consume two load-bearing hypotheses with a counterexample for each. Three issues remain, one of them in the concrete verification.

## REVISE

### Issue 1: The worked example assigns two incompatible views to one QD filter

**ASN-0133, Worked composition**: "the base `M_tgt`, the members of a Unary target-marking type `tgt` (one of ASN-0129's QD bases `M_K`, read audit so the base itself is grow-only), with filter body `needs_attention(t) ≡ is_attn(t)` ... read at the *active* view."

**Problem**: The domain `{t ∈ M_tgt : is_attn(t)}` contains two view-parameterized constituents — `M_K` and `is_K` are *both* on PC3's view-parameterized list (ASN-0129). In a single PL term they read one top-level view (PC3 fixes the view at top level), so they cannot read audit and active respectively. The note's two annotations are therefore mutually unrealizable:

- The triggers `T_P`, `T_R` read `L_cmt`/`L_res`, which are *fixed-view* (audit by name), so they are view-independent and leave the top-level view free.
- The non-grow-only discussion the example turns on requires `is_attn` at **active** (PD1: active `is_K` flips both ways), forcing top-level view = active.
- But at view = active, `M_tgt` (= `members(tgt, active)`) reads the *active* members and is itself **not** grow-only (PD1/PD0: active `M_K` shrinks under retraction). So "M_tgt read audit so the base itself is grow-only" is false under the only assignment that makes the rest of the example coherent.

Consequently the supporting claim for `quiescent_R ∈ PL` — "single-view — both triggers read the audit slice" — is also incomplete: single-PL-term-ness needs *every* view-parameterized constituent (triggers **and** the view-parameterized parts of the domains) to agree on one view, not the triggers alone. The example is precisely the case where they don't.

(The *conclusion* `quiescent_R ∈ PL` survives — pick top-level view active and it is a well-typed term — but the stated justification and the M_tgt-grow-only remark are wrong as written.)

**Required**: Make the domain's views consistent, and correct Q0's single-view criterion to range over domains too. Either (a) commit to top-level view = active and drop the "M_tgt grow-only" claim (the domain is non-grow-only regardless; Q5a's union bound still absorbs it); or (b) keep members-at-audit by writing the base as PC3's view-independent fixed-slice rebuild `⋃(L_tgt, addrs_F)` (= `members(tgt, audit)`) rather than the view-parameterized `M_tgt`, leaving the top-level view free for `is_attn` to read active. In Q0/Q7, state that "single-view" must quantify over all view-parameterized constituents (triggers and domains/scopes alike).

### Issue 2: "names an empty case" is false for non-concurrent registries

**ASN-0133, Q6**: "but H-W is unsatisfiable for any registry doing concurrent work, so `H-W + H-FAIR` names an empty case — H-W's role is to locate H-RF, never to instantiate Q6."

**Problem**: The implication does not hold. H-W is unsatisfiable for registries *doing concurrent work* (your own H-W section correctly hedges: "essentially every registry that does concurrent work"), but it is perfectly satisfiable for trivial/sequential ones. A single-rule, single-argument registry whose argument starts trigger-true: it cannot be no-op-spammed while the argument stays true (firing it is the only available fire and it falsifies the trigger), so along *every* σ the argument is true at only one step, `|W(σ)| < ∞`, and H-FAIR holds (the argument is fired). That registry+σ witnesses `H-W + H-FAIR`. The conjunction is therefore not empty; the qualifier from the H-W section was silently dropped here.

**Required**: Qualify the claim — "empty among registries doing concurrent work," or better, "instantiates no case beyond `H-RF + H-FAIR` (since H-W ⟹ H-RF)." Note explicitly that trivial/sequential registries *do* satisfy `H-W + H-FAIR`, so H-W's redundancy is by subsumption under H-RF, not by emptiness.

### Issue 3: "each bounds real fires" is proven only for Q5a, and is false for acyclicity

**ASN-0133, W/H-W section**: "an all-SF, extinction-disciplined registry with bounded domain growth (Q5a); a *stratified* registry ... with per-stratum bounds; acyclicity of the emission/re-arm graph — each bounds *real fires* (and so supplies H-RF, below), but none bounds `W`."

**Problem**: The note states as fact that all three conditions bound real fires, but proves it only for Q5a. The universal claim is false for acyclicity: a single rule firing on an unboundedly growing domain has an acyclic emission/re-arm graph (nothing re-arms anything) yet unbounded real fires — exactly the divergence route Q5a's *separate* bounded-domain-growth clause is there to exclude. Acyclicity alone does not supply H-RF. The stratification case fares no better on its own terms: "with per-stratum bounds" silently smuggles in a per-stratum H-RF assumption, so it is a decomposition of the conclusion, not an independent structural condition that supplies it.

The note's headline conclusion (none of these bounds `W`) is unaffected, but the parenthetical over-credits two unproven foils.

**Required**: Either prove the real-fire bound for stratification and acyclicity, or downgrade the parenthetical to "best case." For acyclicity, add the domain-growth bound it actually needs; for stratification, surface that "per-stratum bounds" is a per-stratum H-RF hypothesis rather than a structural guarantee.

## OUT_OF_SCOPE

### Topic 1: The SF certificate (`pd_extinct`)
**Why out of scope**: Q-EXT/Q5a make SF membership the load-bearing uncertified registration check, but the property is syntactically decidable (PD0's scan) at registration today; shipping a substrate-recorded `pd_extinct` class so "every rule is at-most-once" becomes a queryable lint is correctly deferred to Open Question 1 (mirroring ASN-0130's OQ4), not a gap in this note.

### Topic 2: Termination for non-SF registries
**Why out of scope**: The full cross-rule re-arm analysis under the Q-FLIP falsifier inventory (the H-W route for triggers not in SF) is a different theorem; this note correctly scopes its quantitative payoff to the SF-plus-extinction design rule and leaves the general case unaddressed.

### Topic 3: A scheduler and fairness construction
**Why out of scope**: H-FAIR is stated as a named hypothesis; constructing a discipline that discharges it and proving the fairness property is operational machinery the note deliberately leaves at the implementation layer ("What this note doesn't cover").

VERDICT: REVISE
