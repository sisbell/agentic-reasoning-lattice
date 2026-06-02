# Review of ASN-0086

## REVISE

### Issue 1: wp Case 2 is not delivered over the ASN's own working domain

**ASN-0086, Weakest-Precondition Analysis, Case 2 / Domain caveat**: "All results below are stated over states `→*`-reachable from `Σ_init`" (Working domain) versus "This formula is the weakest precondition **relative to the layer-reachable domain only**. It does *not* characterize `wp` over the strictly larger `→*`-reachable domain on which `Emit_K` is otherwise defined."

**Problem**: The ASN fixes its working domain as the `→*`-reachable states, and `Emit_K` is defined over exactly that domain. But the Case 2 wp is delivered only over the strictly smaller *layer-reachable* sub-domain. By the note's own admission, at a `→*`-reachable-but-undisciplined state "a pre-existing wide retraction to-span can already cover the fresh `a`, adding a further necessary [clause] that the formula above omits." So the wp claimed for Case 2 is incomplete with respect to the domain the ASN actually works over — the reader is given a wp for a restricted trajectory class, not for the operation as specified.

Worse, the missing clause — "no pre-existing `L_R^Σ` tuple has `a_emit(Σ, d)` in its to-coverage" — is itself a *state* predicate, finitely checkable over `L_R^Σ` (L-fin + CoverageEqualityDecidable). The full `→*`-reachable wp is therefore expressible directly as

`d ∈ dom(Σ.M) ∧ (K ≁ R ∨ a_emit(Σ,d) ∉ coverage(G)) ∧ ¬(∃(b,F',G') ∈ L_R^Σ : a_emit(Σ,d) ∈ coverage(G'))`

without any trajectory-bound "layer-reachable" apparatus. As written, the layer-reachable restriction substitutes a trajectory property for a clause that is a clean state predicate, and the genuine wp over the stated working domain is left uncharacterized.

**Required**: Either deliver the wp over the `→*`-reachable working domain with the third conjunct made explicit (preferred — it is a state predicate), or narrow the ASN's declared working domain so that "layer-reachable" is the domain of record for all results, not just this one. Do not leave the operation's actual-domain wp uncomputed while presenting a sub-domain formula as "the weakest precondition."

### Issue 2: Corollary R5.1 restates R5 without adding content

**ASN-0086, Corollary R5.1**: "For any `a ∈ A_rel^Σ`, either *content slot* — from-set (slot 1) or to-set (slot 2) — ... R0 emits at a fresh `A_rel` address a triple carrying the unit-depth span `(a, δ(1, #a))` in the chosen content slot (by Steps 3–4 ...)."

**Problem**: R5's own statement and proof already establish exactly the from-set (slot 1) and to-set (slot 2) emissions; R5 never touched slot 3 to begin with. The corollary's only added qualifier, "content slots only," excludes a case R5 never claimed. The corollary therefore re-derives Steps 3–4 of R5's proof as a separate numbered result, saying the same thing in different words.

**Required**: Either fold the slot-1/slot-2 emission directly into R5's postcondition and delete R5.1, or give R5.1 distinct content (e.g., the type-slot *impossibility* it gestures at) so it is not a restatement.

### Issue 3: R6c Consequence ends in prescriptive use-site guidance, not argument

**ASN-0086, *Consequence — `A_K` is not monotone***: "Predicates and observation views over `A_K` must therefore treat its evolution as non-monotone, not inherit monotonicity from `L_K`."

**Problem**: The paragraph's substantive content — `A_K` shrinks under retraction and grows under re-emission, so neither inclusion holds — is a real derived fact and belongs. The closing sentence, however, is advice to hypothetical downstream consumers about how they "must" treat `A_K`. It advances no claim about the present object; it is essay directed at future layers. This is the meta-prose pattern the anti-bloat classifier flags (use-site guidance in a structural slot).

**Required**: Drop the closing prescriptive sentence; the non-monotonicity fact stands on its own.

### Issue 4: Worked Sketch Step 1 inserts an unused alternative-caller excursion

**ASN-0086, Worked Sketch, Step 1**: "the retractor here happens to share `a₁`'s home document, so the caller supplies `d_retr = d`; a different caller homed at `d' ∈ dom(Σ_0.M)` with `d' ≠ d` would supply `Nullify(Σ_0, d', a₁)` instead, with identical effect on `nullified(Σ_1)`."

**Problem**: The worked example fixes `d_retr = d` and computes from there. The hypothetical "a different caller homed at `d'`" advances none of the Step 1 computation and exercises no property under demonstration; it is an aside imagining a configuration the example does not use. The home-independence of nullification is already implied by Nullify's signature taking an arbitrary `d_retr ∈ dom(Σ.M)`.

**Required**: Delete the parenthetical; if home-independence of nullification is worth stating, state it once at Nullify's definition, not inside an unrelated worked step.

## OUT_OF_SCOPE

### Topic 1: Arrangement/visibility interaction, multi-arity projections, concurrency, cardinality bounds
**Why out of scope**: The Open Questions section already isolates these (interaction of `L_K` with `Σ.M` visibility; binary projections of `|Σ.L(a)| > 3` links; Emit/Observe atomicity and consistency model; bound on `|nullified(Σ)|`). They are genuinely new territory layered on top of this note's relational vocabulary, correctly deferred rather than errors here.

### Topic 2: Elevating the unit-depth retraction discipline to a substrate K-operation
**Why out of scope**: Whether retraction should be a dedicated substrate operation with a unit-depth shape constraint (rather than a layer convention) is a substrate-design decision for a future ASN, as the note's own Open Questions acknowledge. Note, however, that resolving it is the cleanest path to closing Issue 1.

VERDICT: REVISE
