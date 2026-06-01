# Review of ASN-0086

I checked the proofs (R0, R0a, R-Scope, the wp analysis, CoverageEqualityDecidable), the worked sketch arithmetic, and the cross-references. The mathematics is sound: R0a's cross-home zero-counting argument is correct, R-Scope's antichain reduction holds, the wp Case 2 biconditional is established correctly within its stated domain, and the worked-sketch tumbler values (`a₁ = 1.0.1.0.1.0.2.1`, `b₁ = …2.2`, etc.) check out. The cross-references are all to foundation ASNs (0034/0036/0040/0043/0093), so no self-containment violation.

This note carries the `review-mode.anti-bloat` classifier. My findings are confined to meta-prose a precise reader must skip past.

## REVISE

### Issue 1: wp Case 2 — the self-nullification biconditional is derived twice, verbatim
**ASN-0086, Weakest-Precondition Analysis, Result paragraph**: "The fresh tuple `(a, F, G)` lands in the retraction slice `L_R^{Σ'}` only when `K ~ R`; once there, it nullifies its own address `a = a_emit(Σ, d)` only when its to-set covers `a` … The fresh emission therefore self-nullifies iff `K ~ R ∧ a_emit(Σ, d) ∈ coverage(G)`, and the disjunction is precisely the negation of that conjunction."

**ASN-0086, Derivation (both directions)**: "The fresh tuple lies in `L_R^{Σ'}` iff `K ~ R`, and — when it does — its to-coverage contains `a` iff `a = a_emit(Σ, d) ∈ coverage(G)`. Hence `a ∈ nullified(Σ') ⟺ (K ~ R ∧ a_emit(Σ, d) ∈ coverage(G))`. Negating both sides, `a ∉ nullified(Σ') ⟺ (K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))`."

**Problem**: The Result paragraph states the wp and then proves it inline; the Derivation paragraph re-proves the identical biconditional in nearly the same words. This is the "two paragraphs say the same thing in different words" pattern. The reader who reaches the Derivation has already seen the derivation.

**Required**: Let the Result paragraph *state* the wp and its interpretation ("captures the self-nullification boundary"); strip its inline derivation and let the Derivation paragraph carry the proof. One pass, not two.

### Issue 2: wp Case 1 — defensive parenthetical re-litigating the counterexample
**ASN-0086, Weakest-Precondition Analysis, Case 1 load-bearingness**: "(We do not assert `b ≠ a` as a generic fact: when P1 is dropped `a` is arbitrary, and nothing prevents `a = a_emit(Σ, d_retr)`; the counterexample simply selects an `a` for which they differ.)"

**Problem**: This is a defensive justification anticipating a misreading. The counterexample construction one sentence earlier already fixes the choice ("choose `a ∉ A_rel^Σ` distinct from the fresh emitter `a_emit(Σ, d_retr)`"), which makes `a ≠ a_emit` by selection. The parenthetical re-argues a point the construction already settled, and the reader must skip it to stay with the load-bearingness thread.

**Required**: Delete the parenthetical; the construction's "distinct from the fresh emitter" already carries the work.

### Issue 3: Worked Sketch — L-invariant discharge re-stated by deferral at each fresh address
**ASN-0086, Worked Sketch, Step 1**: "The remaining state-local L-invariants (L3, L4(c), L12, L12a, L14, L14a, L-fin) discharge by R0's generic argument applied with the concrete `b₁`." **Step 2**: "L-invariants at `a₂` discharge by R0 applied with substitutions of `a₂` for `b₁`". **Step 3**: "L-invariants at `b₂` discharge by R0's generic argument with the concrete `b₂` substituted (L0: …; L1: …; L1a: …; L1b: …; L1c: …)".

**Problem**: The sketch re-discharges the same invariant set at each fresh emission by appeal to R0's generic argument — three repetitions of "discharge by R0's generic argument." The concrete checks (which a worked example exists to show) are valuable once; the repeated deferral-to-R0 across steps is use-site meta-prose, not demonstration.

**Required**: Show the concrete per-component check at the first fresh emission (`b₁`), then for `a₂`/`b₂`/`a₃` note only the value that *changes* (the element-field ordinal) and state once that the invariant discharge is identical in form. Don't re-invoke "by R0's generic argument" per step.

## OUT_OF_SCOPE

### Topic 1: Tightening L1b to `#E = 2` at the substrate
L-ContiguousPrefix-Cor1 proves `#E(a) = 2` strictly for substrate-conforming states, while L1b (ASN-0043) admits `#E ≥ 2`. The note's own Open Question raises whether L1b should be tightened. That is a change to a foundation ASN, not a defect here.

### Topic 2: Concurrency / atomicity of Emit vs Observe
The Open Questions on observation ordering, Emit/Observe atomicity, and the consistency model under which `A_K` transitions are observed are genuinely new territory, correctly deferred.

VERDICT: REVISE
