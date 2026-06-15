# Review of ASN-0133

I checked the technical core hard — Q0's heterogeneous-view merge (the rebuild equations, the completeness of the view-sensitivity enumeration, the `chain`/`elems` and `is_in_chain` handling), Q5/Q5a's bounds and their open-model behavior, Q6's full case analysis with H-SFAIR's regime form closing cases (2)/(3) and bounded growth excluding (1), Q-EXT/Q-FLIP's falsifier accounting, the SC anti-monotonicity proof, and the worked composition's SF/extinction/born-nullified arguments. **I found no correctness defect, no missing boundary case, no unsupported "by similar reasoning."** The reachability/firing logic is sound and the concrete examples (the two-fire reached-terminal-state sequence; the value-preservation check showing the naive merge computes the wrong verdict) genuinely exercise the postconditions.

The findings below are the anti-bloat targets the classifier asks for: removable duplicate content where a conclusion or definition is stated, then restated.

## REVISE

### Issue 1: The worked example restates its own conclusions

**ASN-0133, "Worked composition" (acyclic-coupling paragraph)**: the structural conclusion is stated three times —
- "it is an *acyclic coupling*, not a symmetric type-isolation: the two rules are coupled *one way only*."
- "The isolated return is what makes the forward feed acyclic: it closes no loop back to `ρ_P`'s domain."
- "the one live coupling is acyclic, its isolated return path closing no *mutual* cycle and its forward feed bounded by `ρ_P`'s environment-driven fires"

and "the crux" (no rule writes `attn`/`tgt`) is announced once ("Here is the crux the open model makes honest: no rule writes `attn` or `tgt`") then re-stated ("by the crux no rule writes `attn/tgt`") and referenced twice more.

**Problem**: The forward/backward analysis carries the whole point (forward feed = bounded one-way; backward = type-isolated); the two subsequent re-statements of "acyclic" and the re-statement of "the crux" add no content. This is the "two paragraphs say the same thing in different words" pattern.

**Required**: State the forward/backward analysis once; cut the "isolated return is what makes the forward feed acyclic" and the Q4-warning re-derivation down to a single reference; announce "the crux" once and reference it without re-stating it.

### Issue 2: Q6's preamble re-derives the Proof's opening step

**ASN-0133, Q6 ("Registry-side, unconditional" vs "Proof")**:
- Preamble: "σ has a last real fire (index N) or none, and past N every fire is a no-op. The registry moves the state no further — all state change past N is environment steps…"
- Proof: "σ has a last real fire — index N — or none … every fire past N is a no-op (RG): the registry moves the state no further, and all state change past N is environment steps."

**Problem**: The preamble does not merely *state* the registry-side result — it *derives* it (last fire N ⟹ past-N no-op tail ⟹ state-change-is-environment), and the Proof then derives the identical chain verbatim. The genuine value-add in the preamble is the conclusion ("Q1's absorption … is the registry's standing guarantee, holding whatever the environment does"); the derivation is duplicated.

**Required**: Let the preamble state the registry-side *conclusion* (finitely many real fires ⟹ registry-inert tail ⟹ Q1 absorption is the standing guarantee) and leave the N-and-no-op-tail derivation to the Proof.

### Issue 3: "Environment step" is fully defined in two places

**ASN-0133, RG vs H-FAIR**:
- RG: "interleaves the registry's own fires with **environment steps** — non-registry `→_sh` transitions the registry neither issues nor controls — and a *fire sequence* `σ` (made precise at H-FAIR) is an interleaving of the two from `Σ₀`."
- H-FAIR: "an *environment step* — any non-registry `→_sh*` transition (another agent or registry, or external input), which the scheduler neither issues nor constrains."

**Problem**: RG already gives a complete definition of environment steps and the fire-sequence interleaving (it is not merely a teaser — RG itself parenthesizes "made precise at H-FAIR"). H-FAIR then re-defines environment steps nearly verbatim. The only genuinely new content in H-FAIR is the `(Σ₀, s₁, Σ₁, …)` formalization and the fairness clause.

**Required**: Define "environment step" once — keep the formal `σ` tuple and fairness in H-FAIR, and have H-FAIR reference RG's environment-step definition rather than restating it (or move the definition to H-FAIR and drop RG's full statement to a forward pointer).

## OUT_OF_SCOPE

The note's Open Questions (SF certificate, runtime divergence detector, per-scope vs global work, cross-scope oscillation, contract necessity) and "What this note doesn't cover" (scheduler, stochastic bodies, activation binding, environment model) already enumerate the future territory comprehensively — including the de-registration-vs-firing lifecycle question, which is correctly deferred to the activation/protocol layer. I have no additional future-ASN topic to add.

One note in tension with the anti-bloat pass but *not* flagged as REVISE: the "Satisfiability is environment-conditional" block develops, through three distinct scenarios (counterfactual liveness, add-then-remove around turns, re-flag-forever), a satisfiability question the note explicitly declines to formalize and re-defers under "What this note doesn't cover." I considered flagging it, but each scenario establishes a *distinct* load-bearing point (liveness necessary; weak turn-fairness insufficient for the regime form; H-SFAIR distinct from regime (i)), and naming weak turn-fairness as H-FAIR's liveness premise is a precise, on-mission addition for a note whose thesis is "every hypothesis named." It earns its place.

VERDICT: REVISE
