# Review of ASN-0133

This is a careful note. The termination theory (Q5/Q6) holds up under scrutiny: the real-fire/no-op decoupling is used consistently, the injection in Q5 is sound, Q-EXT correctly composes X-DEF with PD0 ⊥-stability, the regime form of H-SFAIR is derived correctly, and the non-grow-only obstruction analysis (1)/(2)/(3) maps correctly onto reached-vs-held with the right closing hypotheses. The two worked examples supply the concrete verification the standard demands and both check out. The findings below are localized.

## REVISE

### Issue 1: Q0's behavior-collection rebuild uses a single `is_filtered_J` where UV's `filtered` (a disjunction) is required

**ASN-0133, Q0 (heterogeneous-merge view analysis)**: "The three set-valued behavior atoms (`succs`, `sources_to`, `stale`) rebuild their default value as a QD filter over the atom's own raw active reading, its body the Boolean `is_filtered_J` — which UV never rewrites and is therefore view-stable — the filter being precisely UV's own default-view rewrite (ASN-0129) recast as a PL term."

**Problem**: UV's default-view rewrite drops `x` iff `filtered(x) = (∃ J ∈ Φ, J ≠ K_queried :: is_filtered_J(x))` — a disjunction over *every* BH1 type. A body of a single `is_filtered_J` is not "precisely UV's own default-view rewrite" once `|Φ| ≥ 2`. Concretely, with two BH1 types J₁, J₂ both distinct from the queried type, UV's default-view `succs` drops targets filtered by J₁ *or* J₂, whereas `{y ∈ succs(s) : ¬is_filtered_J₁(y)}` retains the J₂-filtered targets — a strictly larger set, hence the *wrong* default value. This breaks the value-preservation that is the entire point of the heterogeneous rebuild. The same paragraph treats `members`/`targets_of` correctly with `filtered` ("the UV filter `{· : ¬filtered(·)}` (UV's `filtered`, ASN-0129)"), so the two halves of the rebuild are inconsistent, and the worked example hides the slip because it stipulates `Φ = {retired}` (singleton), where `filtered = is_filtered_retired`.

**Required**: State the behavior-collection rebuild body as `¬filtered` (UV's full disjunction over `Φ ∖ {K_queried}`), uniformly with the `members`/`targets_of` rebuild, so Q0's "for *every* registry" claim survives multi-BH1 registries.

### Issue 2: RG states Post_ρ's meta-level nature redundantly

**ASN-0133, RG**: "The contract is meta-level, *not* a PL term: PL has no sort for emitted call sets (COD lists none, ASN-0129) and a PL term reads a single state, whereas the contract speaks of what a fire *emits* — so `Post_ρ` is written in the surface's emission forms, never evaluated as a PL verdict."

**Problem**: The proposition "Post_ρ is not PL" is asserted twice in one sentence ("*not* a PL term" / "never evaluated as a PL verdict"), and its justification is given twice ("PL has no sort for emitted call sets" / "the contract speaks of what a fire *emits*"). The following sentence ("What *is* PL is the trigger `T_ρ`…") then re-states the same distinction a third time. This is the meta-prose accretion the anti-bloat classifier targets: one statement of "Post_ρ is a meta-level emission contract, not a single-state PL term; the trigger T_ρ is the PL part" carries the whole load.

**Required**: Collapse to a single statement of the type distinction.

### Issue 3: Decorative capability list in the Triggers paragraph

**ASN-0133, Triggers**: "A trigger given as a `pdef` address (ASN-0130), evaluated by reference (PR3), makes the registry itself substrate content — its triggers linkable, versioned, and certified like any definition."

**Problem**: "linkable, versioned, and certified" advances no claim in the note — the note's only use of pdef-triggers is their evaluability and Q0-recognizability (correctly developed in the next sentence). The list is motivational decoration of a structural slot.

**Required**: Cut, or tie each named capability to a claim that uses it (none does here).

## OUT_OF_SCOPE

### Topic 1: Registering `quiescent_R` itself as substrate content
Q0 proves `quiescent_R ∈ PL`, but the recognizer is never registered (as a `pdef`) so that other agents could link or certify it. Shipping a "quiescence certificate" class is a natural extension — and shares the spirit of the note's own Open Question 1 (a `pd_extinct` certificate). New territory, not a defect here.

**Why out of scope**: The note's contribution is recognizability-as-PL-term; whether to materialize the recognizer as a certifiable class is a catalog-growth question for a later note, already gestured at by OQ1.

### Topic 2: Semantic adequacy of the audit-spelling trigger
The Marker pattern's audit-slice trigger falsifies even on a *born-nullified* deposit (Q3) — terminating soundly while the mark is not active. Whether the audit spelling matches an application's intended "the address is actively marked" semantics is an application concern; the note correctly scopes its claims to termination, not marking semantics.

**Why out of scope**: This is a property of how a coordination layer chooses its trigger spellings, not a guarantee the substrate owes; the note flags the audit/active tradeoff and stays on the termination side of it.

VERDICT: REVISE
