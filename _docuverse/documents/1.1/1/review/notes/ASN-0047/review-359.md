# Review of ASN-0047

## REVISE

### Issue 1: C1c / L1c chain discharge skips the k = 1 step's TA5a zero-count admissibility (a boundary check at zeros = 3)

**ASN-0047, *Extended reachable-state invariants*, C1c and L1c discharge prose**:
- C1c: "the structural inc-chain `t₀ = d, t₁ = inc(d, 2) = b_C(d) = [d.0.1], t₂ = inc(t₁, 1) = a` ... `k₁ = 2, k₂ = 1`, each in `{0, 1, 2}`; **the only `k = 2` step is `k₁` whose operand `t₀ = d` has `zeros(d) = 2 ≤ 2`**; and `#tᵢ > #d` at every step."
- L1c: analogous, with the `k₃ = 1` step `ℓ = inc(b_L(d), 1)`.

**Problem**: The formal C1c/L1c statement (inherited from ASN-0093) requires *each* step to satisfy "T10a's per-step admissibility constraints." For the `k = 1` step the relevant constraint is TA5a: `inc(t, 1)` preserves T4 only when `zeros(t) ≤ 3`. The operand of that step is `b_C(d)` (resp. `b_L(d)`), which has `zeros = zeros(d) + 1 = 3`. This sits *exactly* on the TA5a boundary (`k = 1 ∧ zeros ≤ 3`) — admissible, but only just. The prose explicitly discharges the `k = 2` step's zero bound (`zeros(d) = 2 ≤ 2`) and silently passes over the `k = 1` step's zero bound. A reader cannot confirm the chain is T10a-conforming without supplying the omitted check, and the boundary value (3, not 2) is precisely the kind of edge a "show your work" standard demands be made explicit.

**Required**: Add the `k = 1` admissibility check to both discharges: `zeros(b_C(d)) = 3 ≤ 3` (resp. `zeros(b_L(d)) = 3 ≤ 3`), licensing the `k = 1` step under TA5a's `k = 1 ∧ zeros(t) ≤ 3` clause. State that this is the boundary case so the tightness is visible.

### Issue 2: K.μ⁻ reverse-equivalence proof lists D-SEQ★ as both a hypothesis and a derived consequence, and invokes "preserved by restriction" on an object not yet shown to be a restriction

**ASN-0047, *K.μ⁻ admissible contraction shape*, reverse direction**: "hypothesise that `M_cand(d)` ... satisfies D-CTG★ + D-MIN★ + **D-SEQ★** at Σ' together with the elementary-preserved invariants (S2, S3★, S8a, S8-depth, S8-fin)" — then immediately "**D-SEQ★ at Σ' follows from** the candidate's D-CTG★/D-MIN★ ... together with S8-depth/S8-fin/S8a (**preserved by restriction**)."

**Problem**: Two defects in the same passage. (a) D-SEQ★ is named in the hypothesis set and then derived from the other hypotheses — it should not be assumed if it is being proved. (b) The phrase "preserved by restriction" presupposes `M_cand(d)` is a restriction of `M(d)`, which is the proof's *conclusion*, not an available premise at this point. The finiteness/depth facts the step needs actually follow from the genuine hypothesis `dom(M_cand(d)) ⊂ dom(M(d))` (a subset of a finite set is finite; every survivor is a pre-state V-position and keeps its pre-state depth), independent of the restriction conclusion.

**Required**: Drop D-SEQ★ from the hypothesis list (derive it), and re-justify S8-fin/S8-depth at the candidate from `dom(M_cand(d)) ⊂ dom(M(d))` plus value-preservation on survivors, not from "restriction."

### Issue 3: Defensive meta-prose in the K.μ~ necessity argument (anti-bloat)

**ASN-0047, *Necessity and sufficiency of the precondition***: "Necessity assumes π admissible, so subspace-preservation (iv) and link-fixity (v) both enter as hypotheses — (v) is derived in Step (A), Case `s_L`, from (iv), CL-UNIQ, and LRP; **it does not follow from (i)+(iv)+CL-UNIQ for an arbitrary π, as the link-swap transposition shows.**"

**Problem**: This carries the `review-mode.anti-bloat` reviser-drift signature: the clause defends *why* (v) is taken as a hypothesis rather than derived, by pointing back to a counterexample (the link-swap transposition) already constructed in *The conjuncts are mutually independent*. It explains the bookkeeping of the proof's hypothesis selection rather than advancing the necessity argument, and the reader must skip past it to follow the actual derivation. The substantive content (that (v) is established in Step (A)) is already stated; the "it does not follow from ..." rider is justification of a prior finding's resolution, not reasoning.

**Required**: Reduce to the load-bearing statement — that (v) is available as an admissibility hypothesis (established in Step (A)) — and drop the defensive "it does not follow from (i)+(iv)+CL-UNIQ ... as the link-swap transposition shows" clause; the independence of the clauses is already demonstrated in its own paragraph.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link/content withdrawal (compact-and-renumber DELETEVSPAN)
**Why out of scope**: The ASN's K.μ⁻ models suffix-removal only; interior compaction with V-position renumbering is the implementation's `DELETEVSPAN`, a named operation, and the ASN already routes it to an open question. New operation, not an error here.

### Topic 2: Concurrency/serialization of link and content allocation under a shared home document
**Why out of scope**: Atomicity beyond the single-event SequentialTransitionAxiom, and concurrent allocation coordination, are explicitly deferred (open questions) and fall under operation atomicity/concurrency, which is out of scope per the Scope block.

VERDICT: REVISE
