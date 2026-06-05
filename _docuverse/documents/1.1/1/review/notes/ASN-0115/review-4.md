# Review of ASN-0115

## REVISE

### Issue 1: R7 Repeatability assumes comparability that the hypothesis does not supply

**ASN-0115, R7 (Repeatability)**: "Let `Σ`, `Σ'` be two states of one evolving docuverse — both reachable from a common initial state along the sequential transition order … Because both states lie on a common trace from the shared initial state, the sequential transition order makes them comparable, so without loss of generality `Σ` precedes `Σ'`."

**Problem**: "Reachable from a common initial state" does not entail "comparable." SequentialTransitionAxiom (ASN-0047) totally orders the transitions *within a single execution*, but two states reached from `Σ₀` by *different* operation choices are divergent branches of the reachability relation — neither need →*-precede the other. The proof's inference "lie on a common trace ⇒ comparable" silently re-reads "reachable from a common initial state" as "on one linear trace," which is exactly the missing hypothesis. The gap is load-bearing: across divergent branches a content address `a` may be allocated independently to *different* values (allocation is state-determined, so each branch can mint the same next address with a different `Σ.C(a)`), so `Σ.C(a) = Σ'.C(a)` fails and S0/L12 — which are per-transition along one trace — do not apply. The WLOG step is undischarged for the incomparable case.

**Required**: Either restrict R7's hypothesis to comparable states (state it as `Σ →* Σ'`, i.e. one is a reachability descendant of the other), or prove that a shared bound address carries the same value across divergent branches (which, given branch-local allocation, appears false and would itself need argument). As written the proof only covers the linear case it tacitly assumes.

### Issue 2: Finiteness of `act(ρ, Σ)` asserted without its premise

**ASN-0115, "What a spec-set is, and what delivery is"**: "Because `act(ρ, Σ)` is a finite subset of the totally ordered carrier `T` (ASN-0034, T1), it has a unique ascending enumeration `v₁ < v₂ < … < v_k`."

**Problem**: `⟦σ⟧` is an infinite tumbler interval and `T` is infinite, so finiteness of `act = dom(Σ.M(d)) ∩ ⟦σ⟧` does not follow from T1's total order alone. It follows only because `dom(Σ.M(d))` is finite (S8-fin, ASN-0036). The cited authority (T1) supplies the order, not the finiteness. The unique ascending enumeration — and hence the well-definedness of `deliver₁`'s order — rests on this unstated premise.

**Required**: Cite S8-fin (ASN-0036) as the source of finiteness; T1 then supplies the order. One clause fixes it.

## OUT_OF_SCOPE

### Topic 1: Single-span subspace straddling
**Why out of scope**: The V-spec definition confines `σ` to ordinal-level spans (`actionPoint(ℓ) ≥ 2`), and the ASN's own T5 argument correctly shows such spans cannot cross the subspace boundary. Delivery for a single boundary-crossing span is explicitly deferred to the Open Questions — that is genuinely new territory, not a defect here.

### Topic 2: Inline provenance inside delivered material
**Why out of scope**: R9 asserts only resolution-traceability of origin; whether origin must travel inside the delivered bytes is correctly identified as a separate (future) question, since the content item carries `Σ.C(a)`, not `a`.

VERDICT: REVISE
