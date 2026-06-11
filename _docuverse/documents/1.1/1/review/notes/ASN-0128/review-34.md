# Review of ASN-0128

## REVISE

### Issue 1: retract_stale establishes per-constituent admission but never states the batch's net postcondition
**ASN-0128, BH4 (age-staleness), `retract_stale`**: "P0 (`d_retr ∈ dom(Σ.M)`) is evaluated once at batch entry — the same state at which the stale set is evaluated — and on failure no constituent is issued. Once it holds there, it persists to every constituent pre-state by domain monotonicity … every constituent call is admitted."
**Problem**: The paragraph does the hard work — admission of every constituent under arbitrary interleaving, the hit/miss case split for already-retracted targets, the cannot-sterilize bound — and then stops one step short of saying what the batch *achieves*. The natural end-to-end postcondition is derivable from material already on the page: every `a` in the entry-state `stale(h)` is nullified at the batch's final state — a miss constituent nullifies its target outright (P-tgt enforced, S3's miss contract), a hit constituent finds its target already nullified (the hit branch's Nullification bullet via R6b), and R6a persists both to batch end across any permitted interleaving. Postconditions established but consequences not explored is a named gap; a batch operation whose contract never states the batch's outcome is the canonical instance.
**Required**: State the batch postcondition — `(A a ∈ stale(h) evaluated at batch entry :: a ∈ nullified(Σ_final))` — and derive it in one or two lines from the per-constituent contracts plus R6a.

### Issue 2: frontier-landing, a step-quantified claim, is cited under RP-a's single-state transfer
**ASN-0128, I2 (AuditSliceNotConsulted)**: "(FrontierUnification, ASN-0126, at extended-record states by RP-a; every `K.λ_sh` deposit lands at the frontier and advances it by one — frontier-landing)"
**Problem**: RP-a transfers claims whose conclusion is a predicate of one reachable state. `a_emit(Σ, d) = chain_d(f_d^Σ)` is such a claim; frontier-landing is not — it quantifies over deposits and constrains how the frontier moves across a step, so its transfer route is the step projection (RP(ii)/RP-b), not RP-a. The note knows this distinction precisely — the same sentence routes RangeSterilization "by RP-b's derivation projection, not by RP-a" — but the parenthetical as written places the step-quantified gloss inside the RP-a citation. The advance-by-one half is moreover not load-bearing in I2's argument, which needs only the frontier identification plus RangeSterilization.
**Required**: Scope the RP-a citation to the single-state equality, and either drop the frontier-landing gloss from I2 or transfer it explicitly via the step projection (RP(ii), with L-ContiguousPrefix at pre- and post-state).

### Issue 3: "does not even type-check" misstates why the inherited postcondition fails on a hit
**ASN-0128, I6 (IdemEmitSurfaceContract)**: "on a hit the returned address bears the incumbent's stored `(F', G')`, not the presented `(F, G)` — the inherited postcondition `(a, F, G) ∈ A_K^{Σ'}` does not even type-check against what the surface returns."
**Problem**: It type-checks fine. `A_K^{Σ'}` is a set of (address, endset, endset) triples and `(a★, F, G)` is such a triple; on a hit with incumbent decomposition `(F', G') ≠ (F, G)` the membership is simply *false*, because the stored value at `a★` is `(F', G')` and SliceUniqueness pins one triple per address. The move to a coverage-typed POST is right; the justification given for it is wrong, and a wrong justification for a correct definition is exactly the kind of hand-wave this note otherwise avoids.
**Required**: Replace the type-check claim with the accurate ground: the inherited postcondition is generally false on a hit (the stored decomposition need not be the presented one), so the caller-facing postcondition must be coverage-typed.

### Issue 4: the operation-set taxonomy misses `retract_stale`
**ASN-0128, Standard registrations, The operation set**: "`Observe_K` is ASN-0086's read unchanged, with the behavior and default predicates layered on it."
**Problem**: BH4 provides `retract_stale`, which is not a predicate and is not layered on `Observe_K` — it is state-changing batch tooling layered on `Nullify_Binary` (BH4: "a *sequence* of `→_sh` steps, one per target"). The closing paragraph's taxonomy — three primitives plus predicates over the read — silently omits the one behavior-provided surface that writes. A reader auditing the operation surface against this paragraph would conclude the behaviors are read-only, which BH4 contradicts.
**Required**: Account for `retract_stale` in the operation-set paragraph: behavior-provided write tooling reduces to `Nullify_Binary` step sequences and introduces no fourth primitive.

### Issue 5: SD defines a quantifier-phrase the note never uses
**ASN-0128, SD (SurfaceDiscipline)**: "a substrate is *surface-disciplined* when it admits only such derivations, and 'on a surface-disciplined substrate' quantifies below over the states surface-disciplined derivations reach — the analog of ASN-0086's LayerReachable."
**Problem**: The phrase "on a surface-disciplined substrate" occurs nowhere below. Every downstream use quantifies directly over derivations — "at every state a surface-disciplined derivation reaches" (DR, twice), "at states reached by surface-disciplined derivations" (I6), "extend a surface-disciplined derivation" (I4), "a derivation that is not surface-disciplined" (the example). A locution defined for downstream consumption that no downstream text consumes is dead setup — the accretion pattern this note is flagged for.
**Required**: Delete the substrate-level clause (the derivation-level definition and the LayerReachable analogy carry everything the note uses), or actually adopt the phrase at the use sites.

## OUT_OF_SCOPE

### Topic 1: Caller-visible rejection and branch signaling
The exposed `Emit_K` models rejection as partiality ("undefined there rather than total with an error value") and returns a bare address on both hit and miss — yet the branches differ observably (a hit ignores `d`; a miss consumes a chain slot). How a caller observes rejection, and whether the surface should signal which branch fired, is surface-protocol design.
**Why out of scope**: The note deliberately fixes the state semantics and leaves the result-channel protocol unmodeled; specifying error and branch observability is new machinery for a successor, not an error in this contract.

### Topic 2: Batch isolation beyond per-constituent contracts
`retract_stale` permits arbitrary interleaving and fixes only per-constituent semantics (plus the net postcondition Issue 1 asks to be stated). Whether batches need stronger isolation — e.g., a consistency statement about events that *become* stale mid-batch, or grouping of batches from concurrent retractors — is untreated.
**Why out of scope**: I4 already places concurrency ahead of the substrate relation; batch-level isolation guarantees would be a new commitment on the serializing authority, properly a successor's territory.

VERDICT: REVISE
