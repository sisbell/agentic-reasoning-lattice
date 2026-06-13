# Review of ASN-0133

This is careful, self-aware work — the foil structure for H-W, the checkable-vs-meta-level line in Q3, and the open/closed split are all genuine and mostly sound. The central recognizability/absorption results (Q0, Q1) and the extinction-bound machinery (Q-EXT, Q5, Q5a) check out. But the fairness hypothesis that the termination theorem stands on is mis-specified, and the load-bearing marker-pattern argument skips a step on exactly the class the worked example uses.

## REVISE

### Issue 1: H-FAIR's discharge condition omits in-domain trigger falsification

**ASN-0133, H-FAIR / Q6**: "σ is fair iff every (ρ, x) trigger-true at some Σ_k is eventually either fired or removed from its domain (x ∉ [D_ρ]_{Σ_m} …)" … "satisfiable by standard disciplines (round-robin, queue-fair, priority with aging)" … and Q6: "Thus past N every trigger-true argument is removed by the environment."

**Problem**: A trigger-true argument can stop being trigger-true *while staying in its domain* — falsified in place, not removed. This is precisely the case the note's own machinery turns on: the SF marker trigger `¬(∃ c ∈ L_K :: x ∈ coverage_G(c))` goes ⊥ the instant *any* actor deposits a covering K-tuple, and the environment "emits through the same surface." Concretely: a flagged target `t` is trigger-true (producer); the environment comments `t` itself (a `cmt` covering `t`), leaving `t` flagged and in-domain but `T_P(t) = ⊥`. H-FAIR's discharge — "fired or removed-from-domain" — has no slot for this third outcome. Three consequences:

- **(a) Unsatisfiability, not strength.** Q6 forces the reading `fired = real fire` ("a trigger-true fire is a real fire and would exceed H-RF's count"). Under that reading, the σ just described — `t` never real-fired (it went trigger-false first), never removed — is deemed *unfair*. A scheduler controls only fires, so it cannot stop the environment from falsifying `t` first; therefore **no** scheduler, round-robin included, satisfies H-FAIR in any falsifying environment. The satisfiability claim is stated unconditionally but holds only for environments that never falsify a trigger they didn't issue — gutting the open model the note built for.
- **(b) Incomplete case split.** Q6's "fired … or removed," and its conclusion "past N every trigger-true argument is removed by the environment," silently drop the falsified-in-domain alternative (for an SF trigger the environment's deposit, not a removal, is what settles it).
- **(c) The H-SFAIR comparison is wrong.** "H-SFAIR strictly stronger than H-FAIR" fails under the literal definition: an argument trigger-true at finitely many indices, then falsified-in-domain forever, satisfies H-SFAIR (no infinitely-often obligation) yet violates literal H-FAIR (trigger-true once, never fired/removed). They are incomparable, not ordered.

**Required**: Add in-domain falsification as a discharge — "eventually real-fired, removed from its domain, *or* `T_ρ(x, ·)` becomes ⊥" — and pin down "fired" (Q6 needs *real* fire; satisfiability needs the falsification escape). With the corrected discharge, Q6 becomes a clean three-way split (past N: real-fire impossible by H-RF, so removed *or* falsified, both environmental), the satisfiability claim holds, and H-SFAIR is genuinely stronger. The termination *conclusions* survive — both firing and falsification reach trigger-falsity, so quiescence is reached either way — so this is a hypothesis/proof correction, not a counterexample to Q6.

### Issue 2: marker-pattern extinction for idem=⊤ classes skips the dedup-miss step

**ASN-0133, Q3 / Worked composition**: "Post_ρ deposits exactly the witness the ∃ quantifies over — a K-tuple covering a — so the deposit grows L_K, the existential goes ⊤, the trigger goes ⊥" — and the worked example: "Post_R a res covering addr(c), growing L_res," with `res` declared **Binary, idem=⊤**.

**Problem**: For an idem=⊤ class `Emit_K` is a *no-op on a dedup hit* — it deposits nothing and `L_K` does not grow. So "the deposit grows L_K" is not immediate; it needs an argument that the fire never hits dedup, and the note asserts the growth without it — on the very rule (`ρ_R`, idem=⊤) the whole worked termination rests on. The missing step: the trigger reads the **audit** slice, so firing (`T_R(c) = ⊤`) means *no* `r ∈ L_res` has `addr(c) ∈ coverage_G(r)`; a dedup hit would be an *active* `res` carrying that same covering G (and active ⊆ audit), which would already have made `T_R(c) = ⊥` — so a fire and a hit cannot co-occur, and the emit is necessarily a miss. The same audit-slice reading is also what lets a *born-nullified* deposit count toward "the existential goes ⊤" (it enters `L_K` regardless of nullification) — a second unstated reliance.

**Required**: State, for the idem=⊤ marker case, that the audit-slice trigger precludes a dedup hit at firing time (hence the emit deposits and grows `L_K`), and that the audit reading makes a born-nullified deposit suffice. Without these, the pivotal "fire ⟹ trigger falsified" claim is asserted, not shown, for the class the worked example uses.

### Issue 3: regime (ii) calls a still-assumed bound "structure not assumption"

**ASN-0133, Q6 regime (ii)**: "all-SF bounds the real fires structurally (Q5a ⟹ H-RF, so N exists by structure not assumption)."

**Problem**: Q5a's derivation of H-RF *requires* bounded domain growth, which the note itself classifies as "reachability-quantified … as meta-level as H-W." So N's existence here rests on a meta-level assumption, not on structure alone. "By structure not assumption" conflates "not assumed directly as H-RF" with "not assumed at all" — exactly the checkable-vs-meta-level distinction the note is otherwise scrupulous about.

**Required**: Qualify to "by Q5a's structural route rather than by assuming H-RF directly — with Q5a's bounded-domain-growth hypothesis still in force."

## OUT_OF_SCOPE

### Topic 1: decidability of schema-level extinction checking
Q3 shows schema-level "strong enough" is a PL-validity question "not shown decidable here." Whether that validity is decidable beyond the negated-existential marker pattern is genuine future work, correctly left open (adjacent to OQ5).

### Topic 2: tuple-content scopes
SC scopes a tuple-domained rule by `addr(x)` — the tuple's own link address — so a comment is scoped by its address, not its target. A uniform "per-target" scope thus restricts the producer correctly (its domain elements *are* targets) but scopes the resolver per-comment, not per-target. Developing scope predicates over tuple endset content belongs to a future note; the present mechanism is consistently specified for what it claims.

VERDICT: REVISE
