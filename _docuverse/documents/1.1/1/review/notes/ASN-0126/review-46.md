# Review of ASN-0126

## REVISE

### Issue 1: R's registration status is asserted in one section and re-opened in another

**ASN-0126, Single-source / Open questions §4**: Single-source states unconditionally "The framework registers R as **Binary**," and the entire retraction story — the wrapper `Emit_R(Σ, d_retr, {r}, {(a, δ(1, #a))})` as a `→_sh`-step — presupposes that `retract` is a *registered* key (precondition (i) of `K.λ_sh`). But Open question §4 lists "the retraction type R (Binary)" among *candidates* for pre-registration and asks whether `Σ_init.registry` is shipped with such types "or is composed entirely of app-declared entries."

**Problem**: These cannot both stand. If R-registration is a framework commitment, OQ4's question about R is already answered and must not be listed as open. If it is open (app-declared), then the retraction wrapper has a `→_sh` image *only when the app registers R as Binary* — an unstated precondition. As written, the retraction discussion treats a contingent fact as a framework guarantee.

**Required**: Either commit R to `Σ_init.registry` as a framework axiom (and remove R from OQ4), or condition every "the retraction wrapper is a `→_sh`-step" claim explicitly on "when R is registered as Binary," and state who is obligated to register it.

### Issue 2: P6's induction step names L12 but needs P1/P4 to carry the hypothesis

**ASN-0126, Properties established (P6)**: "every pre-existing tuple persists unchanged by L12 (LinkImmutability, ASN-0043) … preserving the hypothesis."

**Problem**: The induction hypothesis is "K registered ∧ `Sh-conf(K,F,G) = ⊤`," not merely "the value is unchanged." L12 preserves only the stored value `(F,G,K)`. To conclude that a pre-existing tuple's K is *still registered* at Σ' and that `Sh-conf` *still evaluates* ⊤ at Σ', you need registry invariance and conformance state-independence — P1 (registration status is P1-invariant) and P4 (`Sh-conf` verdict is state-independent). L12 alone establishes neither. The derivation cites the value-persistence premise and silently drops the two premises that actually preserve the predicate being inducted on.

**Required**: Add P1/P4 (or P2) to P6's step: value persists by L12, registration persists by P1, conformance verdict persists by P4. Name the chain.

### Issue 3: Duplicate and defensive meta-prose (anti-bloat)

**ASN-0126, Single-source**: Two sentences say the identical thing — "discontiguous multi-target retraction is the app's responsibility, outside `→_sh` — it is never a gated `→_sh`-step" and, a paragraph later, "Only *discontiguous* multi-target retraction is left to the app, outside `→_sh`." Collapse to one.

**ASN-0126, shape-gated emit (wp)**: "So 'the remaining three are inherited verbatim' is exact: the type-admissibility that enablement needs rides in on registration, not on a fourth landing conjunct." This is a defensive justification of a phrase three lines above, not a step in the derivation. The K∈T_admissible absorption is already proved; this sentence only re-asserts that the proof is correct. Remove.

**ASN-0126, Open questions §1**: The idem item pre-specifies an unborn registry field in detail ("a reserved `idem` registry field (value in `{⊤,⊥}`, frozen by P1 like every registry component)") and then poses four sub-questions about its semantics. An open question should name the gap, not draft the successor's state extension. Trim to the question.

**Required**: Delete the duplicate Single-source sentence, the defensive wp sentence, and the idem field's pre-specification.

## OUT_OF_SCOPE

### Topic 1: Semantics of the canonical from-fill `r = (d_retr, δ(1, #d_retr))`
The wrapper's from-fill has `coverage(r) = {t : d_retr ≼ t}` — the entire home-document subtree. As "attribution" this is degenerate (it attributes a retraction to the whole document, not to a specific attributor). Since `nullified` reads only G, this is not a correctness defect here. What an attribution from-set *should* carry, and whether a whole-subtree filler is acceptable, is a behavior-layer question for the successor note that defines retraction attribution semantics.

### Topic 2: Empty-registry boundary
If `Σ_init.registry = ∅`, precondition (i) fails for every emit, so `dom(Σ.L)` stays empty forever and `→_sh` reduces to `K.σ ∪ K.α`. C0 admits this (empty is a well-formed finite partial function). Whether a substrate with no registered types is intended/useful belongs to the standard-registrations question (OQ4), not to this note's structural commitments.

VERDICT: REVISE
