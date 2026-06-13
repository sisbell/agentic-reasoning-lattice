# Review of ASN-0130

This is a rigorous note. I checked the operations (`register_pred`, `certify_pd_stable`, `evaluate`, plus de-registration via `Nullify_Binary` and supersession via S2) against the stated invariants (PR1, PR2, PR3a, the permanence claims), the boundary cases (empty run, single-address run, closed term `k=0`, self-reference, mutual reference, born-nullified deposit, forward reference, de-registered referent, non-Boolean / view-dependent / unknown certification), and the two wp analyses. I found no correctness defect. In particular the wp's `registration-disciplined` scoping is genuinely load-bearing — without discipline a non-canonical I0-equal tuple with `coverage(F') = subtree(a)` but `addrs(F') ⊋ {a}` would let a `VALID` call *hit* while leaving `POST-ref` (`addrs(F') = {a}`) false, and the note correctly identifies this as "the first use of the discipline." That is the kind of place these proofs usually break, and it holds.

The findings below are one precision issue about what the stability certificate actually asserts, and residual meta-prose (the note carries the anti-bloat classifier).

## REVISE

### Issue 1: The certificate's asserted class is not PD0's ST class
**ASN-0130, PS2 / PR5**: PS2 — "Asserts ST-class certification (PD0, ASN-0129) of the expansion"; PR5 — "asserting membership in PD0's ST class" and "The parameter reading extends that threshold position from 'ℕ literal' to any bound ℕ value."

**Problem**: Check (iii) does not run PD0's rules; it runs PD0's rules *lifted* — parameters as bound constants, and the aggregate-threshold case widened from "ℕ literals" to any bound ℕ value. The note's own worked motivation, `count(L_W) ≥ x` with `x : ℕ` a parameter, is precisely a term that is ⊤-stable yet is **not** in PD0's literal closed-term, ℕ-literal-threshold ST class — PD0's aggregate rule does not fire on a parameter threshold. So the property the certificate actually asserts is *per-instantiation ⊤-stability established under the extended rule*, a sound **superset** of PD0's literal ST. PR5 defines this lifted property correctly ("every `Γ_D`-instantiation … is ⊤-stable"), but then names it "PD0's ST class," and PS2 — the *registration declaration* an implementer reads for the class's meaning — reduces this to a bare "ST-class certification (PD0)" with no trace of the extension. The two labels coincide only at `k = 0`; for parametrized terms with a parameter-thresholded aggregate they diverge, and PS2 invites reading the certified class as literal PD0-ST.

**Required**: Name the certified property uniformly — per-instantiation ⊤-stability established by PD0's rules under the parameter reading (which extends PD0's aggregate-threshold case) — and state explicitly that this is a sound superset of PD0's literal closed-term ST. Fix PS2's one-line summary so it does not read as literal PD0-ST membership.

### Issue 2: PR-VIEW opens with motivation that precedes the load-bearing derivation
**ASN-0130, PR-VIEW**: "Xanadu's read side already puts scope in the reader's hands: in udanax-green every link query carries its own scope … with no backend-held 'current' substituted for the caller's choice — and link filtering is likewise front-end work, the reader's sieve. The definition layer inherits that published-artifact semantics."

**Problem**: The invariant's actual content — view-transparency — is derived from PC3 ("PC3 gives every PL term exactly one view, fixed at the top level; expansion yields one pure term; so the view binding every view-parameterized constituent … is the evaluating caller's") and stands without the udanax-green paragraph. The first two sentences are design motivation by precedent; a reader tracking the claim skips them to reach the derivation. The note carries `review-mode.anti-bloat`, which targets exactly this: essay/motivation sitting in front of the structural claim.

**Required**: Lead PR-VIEW with the PC3 derivation. If the udanax-green grounding is retained, mark it as a motivating aside rather than the invariant's opening — flag the placement, not the existence.

### Issue 3 (minor): The entry-point seal is deferred forward across several sections
**ASN-0130, PR-DISC / PR0 / "What this note commits"**: PR-DISC — "the entry-point seal (Standard registrations) discharges it for the shipped surfaces"; PR0 — "reachable only through this wrapper by the entry-point seal (Standard registrations below)"; summary bullet — "(the entry-point seal)".

**Problem**: Three sections defer to "Standard registrations" for the same downstream mechanism before it is defined. One forward reference is structurally forced (the seal must be defined with the class declarations it extends), but the discharge-by-seal claim is re-asserted in PR0 and the commitments summary beyond the PR-DISC statement that actually needs it. This is the "multiple paragraphs defer to the same downstream location" accretion pattern.

**Required**: State the discipline's discharge-by-seal once (at PR-DISC) with a single forward pointer; let PR0 and the summary rely on it rather than re-deferring.

## OUT_OF_SCOPE

### Topic 1: Validated supersession targets
PR4 reuses S2 unmodified, so nothing prevents a `supersedes` edge whose target is an unregistered (or never-allocated) address; `tip(a)` could then resolve to a non-evaluable head. PR4 is honestly scoped (it promises only that `tip` resolves the lineage and that branches surface ⊥), so this is not an error in the note. A validated-supersession surface that requires the successor registered is future territory — a sibling of Open Question 3's dangling-reference question.

VERDICT: REVISE
