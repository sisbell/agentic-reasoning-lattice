# Review of ASN-0126

I checked the mathematics first. The wp formula itself is correct (it carries both inherited conjuncts), the projection bridge is sound, P5 and P6 are complete, and the worked illustration's arithmetic checks out — `a_R = ...2.3 ∉ coverage(G_rng) = [...2.4, ...2.7)`, the fresh citation address `a = inc(a_R,0) = ...2.4 = g` lands at the lower endpoint of the range, so the C3 born-nullified witness is genuine. The findings below are localized; none of them break P1–P6.

## REVISE

### Issue 1: the wp failure-mode prose claims only one landing conjunct can fail; in fact two can

**ASN-0126, Shape-conformance, "Weakest precondition of the shape-gated emit"**: "the two remaining inherited conjuncts `(K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))` and `¬(∃ (b, F', G') ∈ L_R^Σ :: a_emit(Σ, d) ∈ coverage(G'))` govern *landing* in the *active* subset `A_K^{Σ'}`, and of these the third — ... — is the one that can fail for a gate-clearing emit."

**Problem**: The second conjunct (C2) also fails for a gate-clearing emit. C2 fails precisely when `K ~ R ∧ a_emit(Σ, d) ∈ coverage(G)` — a *self-nullifying retraction*. This clears the gate: R is registered Binary (Single-source), so the emit needs only `|F| = 1, |G| = 1`, and the note's own unit-depth wrapper `G = {(a, δ(1,#a))}` is a single Binary-conformant span. Take `a = a_emit(Σ, d)` — exactly ASN-0086's supported Nullify self-emit branch (`P-tgt`: `a = a_emit(Σ, d_retr)`) — and then `a_emit ∈ coverage(G)`, so C2 is false, the tuple is deposited in `L_R^{Σ'}` (audit) and `a ∈ nullified(Σ')`, hence `(a,F,G) ∉ A_R^{Σ'}`. That is a second born-nullified mode, self-inflicted rather than inherited.

The note recognizes C2's failability in two other places and then contradicts itself here: the three-conjunct gloss earlier calls C2 "the emit is **not** a self-nullifying retraction," and the worked example's Step-1 R-emit explicitly checks it — "Note `a_R ∉ coverage(G_rng)` ... so **even this retraction lands active — it does not nullify itself**." If the note has to verify the R-emit doesn't self-nullify, then self-nullification is a failure mode the central wp characterization cannot call out as belonging to "the third" alone.

**Required**: State that *both* active-landing conjuncts can fail for a gate-clearing emit — C2 (self-nullifying retraction, `K ~ R ∧ a_emit ∈ coverage(G)`) and C3 (a prior retraction already covers `a_emit`). If the intent is to single out C3, the distinguishing property is not "the one that can fail" but "the one **newly** live under `→_sh`": C3 was vacuous under ASN-0086's unit-depth discipline (unit-depth + R0a), whereas C2's self-nullification is inherited and live in both. Say that.

### Issue 2: the third conjunct's meaning is restated three times before the substantive point

**ASN-0126, Shape-conformance, "Weakest precondition of the shape-gated emit"**: C3 ("no pre-existing retraction tuple covers the fresh address") is glossed in the three-conjunct summary ("no pre-existing retraction tuple already covers the fresh address"), again in the strictly-stronger sentence ("the third — no pre-existing `L_R` tuple already covers the fresh address `a_emit(Σ, d)`, independent of the gate"), and again in the born-nullified sentence ("whenever some prior retraction already covers its fresh address"), before the one sentence that actually advances the argument: "That third inherited conjunct stays live under `→_sh`: because R is gated by Binary alone ..."

**Problem**: A precise reader has to skip three equivalent restatements to reach the payload (why C3 stops being vacuous under this framework's Binary-only R gate). The restatements are "the same thing in different words" — the pattern the anti-bloat lens targets.

**Required**: State C3's content once, then deliver the live-under-`→_sh` argument. Fold the corrected failure-mode statement from Issue 1 into the same consolidated paragraph.

### Issue 3: the "K registered ⟹ K ∈ T_admissible" derivation is written out twice

**ASN-0126**: In the wp section — "`K registered` absorbs it: by C0 the registry stores a non-empty representative `K_j ∈ T_admissible` of K's coverage class, and `coverage(K) = coverage(K_j) ≠ ∅` forces `K ∈ T_admissible`." And again, at length, as the first step of the P5 proof — "First, `K ∈ T_admissible`. K is registered, so by C0 the registry stores a finite representative endset `K_j ∈ T_admissible` ... `coverage(K_j) ≠ ∅`; hence `coverage(K) = coverage(K_j) ≠ ∅`, so `K ≠ ∅`, i.e. `K ∈ T_admissible`."

**Problem**: The identical four-step chain (K registered → C0 gives non-empty `K_j` → coverage(K) = coverage(K_j) ≠ ∅ → K ∈ T_admissible) appears in both sections. This is duplicated derivation, not abstract-then-concrete.

**Required**: Prove it once (it is a small lemma — "registration of `[K]` forces `K ∈ T_admissible`") and cite it from both the wp absorption note and P5's proof.

## OUT_OF_SCOPE

### Topic 1: dynamic registration / deregistration

The registry is immutable by design (P1), so no type can be added, retyped, or removed after `Σ_init`. The consequence — an app that needs to register a type later, or retire one, is unserved — is real but is a different (or parallel) framework, as Open Question 6 already anticipates ("a supplemental note loosening the constraints here, or a parallel framework"). Not an error in this note.

**Why out of scope**: The note's thesis is an *immutable* registry; mutable-registry semantics is new territory, not a defect here.

### Topic 2: the operational-semantics layer

Idem semantics, the behavior catalog, default predicates, standard registrations, and predicate composition are explicitly deferred in Open Questions 1–5. That deferral is correctly placed — this note fixes the static shape vocabulary and gate; behaviors are a successor's job.

META: (none — the note defines state (the registry component), a refined transition relation with a static gate, and state invariants P1–P6, all stated abstractly enough that any implementation would owe the same guarantees; it has not drifted into implementation mechanics.)

VERDICT: REVISE
