# Review of ASN-0126

## REVISE

### Issue 1: R-as-Multi contradicts the unit-depth retraction discipline the note claims to inherit unchanged

**ASN-0126, Single-source**: "To admit a variable number of targets under one registration, R must be registered **Multi**" and "ASN-0086's `nullified`/`L_R`/active-subset machinery, all of which read `coverage(G')`, carry over unchanged."

**Problem**: These two claims are inconsistent. ASN-0086's UnitDepthRetractionDiscipline requires *every* `(b, F', G') ∈ L_R^Σ` to have `G' = {(t, δ(1, #t))}` — a **single** unit-depth to-span. Registering R as Multi exists precisely "to admit a variable number of targets," i.e. to allow `|G| ≥ 2` in one retraction tuple. A multi-target R emit (`G = {(a₁,…), (a₂,…)}`, `|G| = 2`) violates ASN-0086's discipline, which is part of the very "machinery" the note says carries over unchanged. The discipline is load-bearing: it is what makes R-Scope's single-tuple-scope result `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` hold. With multi-span `G'`, R-Scope no longer applies and the note offers no multi-target replacement.

The note's own rationale is also muddled: it then says a single-target retraction "conforms ... because Multi subsumes `|G| = 1`." But if every retraction is single-target (which the discipline forces), R is exactly a Binary type and the stated reason for choosing Multi evaporates.

**Required**: Pick one and make it explicit. Either (a) keep ASN-0086's UnitDepthRetractionDiscipline — then `|G| = 1` always for R, register R as Binary, and drop the "variable number of targets" justification; or (b) deliberately relax the discipline to permit multi-target retraction — then state that ASN-0086's UnitDepthRetractionDiscipline does *not* carry over, and supply the replacement scope lemma (the per-to-span generalization of R-Scope) that establishes what `nullified` becomes for `|G| > 1`.

### Issue 2: No weakest-precondition derivation for the shape-gated emit

**ASN-0126, The shape-gated emit / Properties established (P4)**: "P4 ... *True by construction* of `→_sh`."

**Problem**: The whole point of this note is to refine the emit step, yet it derives no wp for that step. ASN-0086 — the direct parent — derives wp for both `Emit_K` (Case 2) and `Nullify` (Case 1), including a non-trivial state-dependent conjunct. The refinement here adds two preconditions (K registered; `Sh-conf(K, F, G)`) and a fourth state component, so the natural depth artifact is `wp(Emit under →_sh, (a, F, G) ∈ A_K^{Σ'})`, showing how shape-gating modifies ASN-0086's Case-2 wp. P4 ("by construction") asserts the conclusion but is not the analysis. The worked illustration checks postcondition *values* at fixed inputs; it does not compute a wp.

**Required**: Derive the wp for the shape-gated emit against a non-trivial postcondition (e.g. `(a, F, G) ∈ A_K^{Σ'}`), exhibiting the added `K registered ∧ Sh-conf(K, F, G)` conjuncts alongside the inherited `d ∈ dom(Σ.M)` and the ASN-0086 retraction-coverage conjunct, and confirm it coincides with `K.λ_sh`'s precondition.

## OUT_OF_SCOPE

### Topic 1: idem semantics, behavior/predicate catalog, standard registrations, N>3 extension
**Why out of scope**: These are explicitly deferred to the operational successor (Open questions 1–6). The structural commitments here — registry presence, `idem` state-independence (P3), shape vocabulary — stand without resolving them. Correctly left for a future note.

### Topic 2: Multi-target retraction scope lemma
**Why out of scope** *(conditional)*: If Issue 1 is resolved by choosing the multi-target relaxation (b), the generalized scope lemma is genuinely new territory and may live in the operational successor — but the *decision* to relax, and the resulting loss of R-Scope, must be stated in this note.

VERDICT: REVISE
