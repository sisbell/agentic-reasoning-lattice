# Review of ASN-0133

The logic here is sound. I worked the proofs and could not break them: Q0's view-classification is exhaustive (the four view-parameterized atoms, the six UV-rewritten collections, and the residual view-stable set partition `V_atom` correctly, and the `chain`/`elems`/`is_in_chain` corner is handled); Q6's reaching/holding taxonomy holds, including the satisfiability caveat that H-SFAIR's regime form is not free against an arbitrary environment; the cmt/res worked example computes `quiescent_R(Σ₂) = ⊤` correctly through the nested quantifier. No correctness REVISE.

What remains is residual meta-prose — the note carries the anti-bloat classifier, and two instances earn their flag.

## REVISE

### Issue 1: Worked composition re-asserts the heterogeneous-PL result for a case the example excludes
**ASN-0133, Worked composition (*Quiescence*)**: "By Q0, then, quiescent_R ∈ PL: decidable at every state, absorbing once reached (Q1) — and were a heterogeneous trigger added, the rewrite would keep it in PL regardless (worked concretely at the *Heterogeneous rewrite* illustration under Q0, where a default-view succs and an audit-slice trigger rebuild to one common-view term with value intact)."
**Problem**: The sentence just established this registry "is single-view *at the active view*… so… Q0's fixed-view-base rewrite is not even called on." The trailing clause then imagines a heterogeneous variant the worked registry does not instantiate and defers back to Q0's own worked illustration to cover it. This is the accreted pattern twice over — a paragraph imagining a case its own precondition has excluded, and a cross-deferral to material Q0 already owns (and demonstrates). A reader following "what is `quiescent_R` for *this* registry" must skip the counterfactual. The general heterogeneous result is Q0's; it does not need re-litigating inside the single-view example.
**Required**: End the claim at "(Q1)". The single-view registry's `quiescent_R ∈ PL` rests on Q0 directly; the counterfactual adds no value the worked example needs.

### Issue 2: H-SFAIR's regime-form derivation is wrapped in use-site narration
**ASN-0133, Conditional termination (*Read through Q-EXT…*)**: "This note invokes H-SFAIR in exactly one role: the all-SF, extinction-disciplined regime over a *non-grow-only* domain." … "That — not 'each recurring argument is fired infinitely often,' which Q-EXT forbids — is the content Q6 consumes."
**Problem**: The substantive content — Q-EXT caps real fires at one, so H-SFAIR's consequent is unsatisfiable and the implication collapses to "no `(ρ, x)` trigger-true at infinitely many indices" (the regime form) — is exactly what Q6 case (3) needs and stands on its own. The surrounding sentences narrate *where* the definition is consumed ("invokes H-SFAIR in exactly one role," "is the content Q6 consumes"), which is the "definition's introduction enumerates downstream consumers" pattern. The derivation does not need the use-site framing to be correct or readable.
**Required**: Keep the regime-form derivation; drop the "in exactly one role" / "is the content Q6 consumes" narration. Q6 can cite the regime form where it uses it.

## OUT_OF_SCOPE

None. The five open questions (a `pd_extinct`/SF certificate, a PL surrogate for H-W, per-scope vs. global work, cross-scope oscillation, contract necessity) are correctly deferred rather than half-answered, and the four "doesn't cover" items (scheduler, stochastic bodies, activation binding, environment model) are the right boundary — the note keeps rule bodies and scheduling at the implementation layer and holds `Post_ρ` meta-level, so it does not drift into mechanics.

VERDICT: REVISE
