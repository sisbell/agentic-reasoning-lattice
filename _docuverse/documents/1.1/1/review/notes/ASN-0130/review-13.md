# Review of ASN-0130

This is a careful, mostly rigorous note. PR3a's substitution induction is genuinely complete (WT-α / WT-W / iterated PC2, with capture- and interference-freedom both discharged), PR2's event-wise acyclicity argument correctly handles re-registration, and the wp analyses in PR0/PR5a are non-trivial and scope-honest. The findings below are real but localized.

## REVISE

### Issue 1: The parameter reading does not cover ℕ-sorted parameters in PD0's aggregate rule

**ASN-0130, PR5 (*Parameters*)**: "the checker runs PD0's rules with each parameter treated as a bound constant of its declared sort — the reading PD0's side conditions already give bound variables ('argument a literal or bound address'; step-constants 'reading no state beyond already-bound values'), a parameter counting as one more already-bound value"

**Problem**: This claims PD0's side conditions *already* accommodate bound variables, citing two of them. But PD0's aggregate rule (ASN-0129) reads: "*Aggregates*, over grow-only `D`, against **ℕ literals**: `count(D) ≥ c ∈ ST` and `count(D) ≤ c ∈ SF`." Its side condition is "ℕ literals," strictly narrower than "bound value." A bound ℕ *parameter* is not a literal, and neither cited side condition ("literal or bound address"; step-constant reads) covers the aggregate threshold position.

This is reachable in exactly the terms PR5 is built to certify. A view-independent, Boolean predicate `⟨x : ℕ⟩ → Bool` with body `count(L_W) ≥ x` (`L_W` a fixed-view, grow-only audit slice — admissible in a view-independent term) is intuitively ST: the count is non-decreasing, the threshold `x` is args-fixed. But PD0's aggregate rule, run literally, will not classify `count(L_W) ≥ x` as ST because `x` is not a literal — so check (iii) either silently refuses a term that ought to certify (incompleteness the "counting as one more already-bound value" framing implies it should *not* exhibit), or it extends "literal" to "bound ℕ value" without saying so.

The extension is sound — PD0's own ground ("a count over a growing set never decreases, so satisfied lower bounds persist and violated upper bounds stay violated") holds for any fixed threshold, literal or parameter — but the note neither invokes that ground for the aggregate rule nor restricts the parameter reading to exclude this case. The blanket claim "PD0's side conditions already give bound variables [this treatment]" is false at precisely the one rule whose side condition is "literals" rather than "bound values."

**Required**: Either (a) state explicitly that the parameter reading extends the aggregate rule's threshold from "ℕ literal" to "bound ℕ value of a parameter," sound by the count-monotone ground; or (b) restrict the parameter reading so ℕ-sorted parameters in aggregate comparison positions are not certified, and adjust the "counting as one more already-bound value" framing accordingly.

### Issue 2: The certification-coverage lint conflates non-predicate definitions, which it can never exclude

**ASN-0130, PR5**: "'every registered definition carries `pd_stable`' is the one-quantifier PL term `(A t ∈ M_pdef :: is_pd_stable(t))` — one term, view active … under PR0's discipline, exactly the registered definition addresses."

**Problem**: The note itself establishes (PR0, PR-ENC, and PR5a check (0)) that definitions of *any* result sort `C_D ∈ Codom` are registrable and referenceable — check (0)'s rationale is explicit: "a `℘_fin(T)`- or `ℕ`-valued definition, though a well-formed, registrable, referenceable artifact, has no stability to assert," rejected "*as a non-predicate*." Such non-predicate definitions can never carry `pd_stable` (check (0) rejects certification outright). Therefore `is_pd_stable(t)` is permanently false for every non-predicate `t ∈ M_pdef`, and the universal lint `(A t ∈ M_pdef :: is_pd_stable(t))` is unsatisfiable in any docuverse holding one — for a legitimate reason (a referenced `℘_fin(T)` helper), not a missing certificate.

Worse, the lint *cannot* be repaired within PL: restricting `M_pdef` to Boolean predicates requires reading each definition's result sort, which is `sig`/content-derived and outside PL's read surface (ASN-0129, *Structural reads only*; PC4 reads only `dom(Σ.M), Σ.L, Σ.registry`). So the only PL-expressible coverage lint is over *all* definitions — which conflates "uncertified predicate" with "legitimately non-predicate," the very distinction check (0) was added to draw. The note presents the lint as a clean structural-checkability win without reconciling it against its own non-predicate category.

**Required**: Qualify the claim. State that the universal lint checks *definition*-level certification (not *predicate*-level), that it is vacuously violated once a non-predicate definition is registered, and that PL cannot restrict the quantification domain to Boolean predicates (result sort being outside PL's read surface). The genuine win — the per-definition atom `is_pd_stable(t)` — should be the load-bearing claim; the universal form needs the caveat.

### Issue 3: Use-site inventory in PR-VIEW

**ASN-0130, PR-VIEW**: "PR5 and PR5a lean on this class."

**Problem**: This closing sentence enumerates downstream consumers and adds nothing to PR-VIEW's meaning — exactly the forward-reference accretion the note's `review-mode.anti-bloat` classifier flags. The view-independent class is fully defined by the preceding sentence; that PR5/PR5a use it is established at PR5/PR5a, where the dependency is stated again ("Certification therefore certifies only *view-independent* expansions (PR-VIEW)").

**Required**: Delete the sentence.

### Issue 4: The "substrate parameter" deferral is stated twice

**ASN-0130, PR-ENC**: "The concrete encoding is a substrate parameter, like the subspace identifiers and the designated standard classes (ASN-0128, Standard registrations); this note fixes the discipline, not the bytes."
**ASN-0130, What this note doesn't cover**: "**The concrete encoding.** PR-ENC fixes the discipline … the byte format is a substrate parameter for the implementation to fix, as with subspace identifiers."

**Problem**: Two passages carry the same "encoding is a substrate parameter, byte format deferred, like subspace identifiers" content. The scope section is the natural home (and adds the non-redundant typing-decidability point); the PR-ENC aside is the removable copy — it interrupts the definition of the artifact to announce a deferral.

**Required**: Drop the substrate-parameter aside from PR-ENC, leaving PR-ENC to define the discipline and the scope section to record the deferral.

## OUT_OF_SCOPE

The note's deferred topics — concrete byte format, activation/triggers, dangling live references (Open Q3), cross-substrate portability (Open Q2), naming (Open Q1), certificate classes beyond ST (Open Q4) — are correctly placed in its own Open Questions and scope section. Nothing additional belongs in a future ASN that this one fails to fence.

VERDICT: REVISE
