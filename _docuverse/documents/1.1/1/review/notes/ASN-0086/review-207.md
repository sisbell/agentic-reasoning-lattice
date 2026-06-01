# Review of ASN-0086

## REVISE

### Issue 1: Higher-arity caveat duplicated across three sites

**ASN-0086, "Definition — Partition" note vs. "Definition — AdmissibleTypes" final paragraph**:
- Partition: "*A_rel^Σ names the whole link store, not only the tuples.* … the store admits higher-arity links (`|Σ.L(a)| > 3`); such addresses inhabit `A_rel^Σ` but correspond to no tuple of any `L_K` … Where a result concerns tuples specifically we say so and restrict to `|Σ.L(a)| = 3`."
- AdmissibleTypes: "For the rest of this development we restrict attention to standard-triple links … Higher-arity links (L3 …) exist in `dom(Σ.L)` but are not members of any `L_K`; they admit an analogous construction with additional slot positions, which we do not pursue here."

**Problem**: The same content — higher-arity links live in `A_rel`, are excluded from every `L_K`, and their construction is not pursued — is stated twice in near-identical words, plus a third statement of the `|Σ.L(a)| = 3` restriction. This is the "two paragraphs say the same thing in different words" anti-bloat pattern, compounded by the Open Questions item already covering the future direction.

**Required**: State the higher-arity caveat once (the `L_K` definition's `|Σ.L(a)| = 3` conjunct plus a single one-line note), and delete the redundant restatement.

### Issue 2: Observe_K is defined as a core operation but never exercised concretely

**ASN-0086, "Worked Sketch"**: the five-step cycle invokes `Emit_K`/`K.λ` and `Nullify`, computing `L_K`, `L_R`, `nullified`, and `A_K` at each state — but never invokes `Observe_K`.

**Problem**: The note's headline contribution is the active/audit distinction, and `Observe_K` is the operation that surfaces it operationally via its `View ∈ {hist, oper}` selector and its pattern subset-match `F̂ ⊆ coverage(F) ∧ Ĝ ⊆ coverage(G)`. Neither the View selection nor the pattern-matching machinery receives any concrete verification. The standards require key operations to be checked against a specific scenario; one of the three core operations has zero worked instances.

**Required**: Add an `Observe_K` call to the sketch — e.g., at `Σ_1` or `Σ_2`, show `Observe_K(Σ, F̂, Ĝ, hist)` returns the retracted `(a₁, F₁, G₁)` while `Observe_K(…, oper)` omits it, and exercise a non-trivial pattern (`F̂` covering `c₁`) so the subset-match is verified, not just asserted decidable.

### Issue 3: "→*-reachability is closed under →" repeated as a standalone justification

**ASN-0086**: the parenthetical "(→*-reachability is closed under →)" / "the K.λ →-step carries this to Σ'" recurs in the Working-domain paragraph, R0's invariant-preservation paragraph, R-Scope, the wp Case 1 sufficiency paragraph, and the wp Case 2 derivation.

**Problem**: A trivial closure fact (RT-closure absorbs one more step) is re-justified five times. Each instance is short, but the recurrence is exactly the accreting-justification pattern the anti-bloat pass targets.

**Required**: Establish it once in the Working-domain paragraph and let later uses cite it without restating the reasoning.

## OUT_OF_SCOPE

### Topic 1: Concurrency/consistency model for Emit vs. Observe
**Why out of scope**: The atomicity of `Emit_K` relative to concurrent `Observe_K`, and the consistency model under which `A_K` transitions are observed, are genuinely new territory (a runtime semantics layer), correctly deferred to the Open Questions rather than forced into this structural note.

### Topic 2: Substrate-level elevation of the unit-depth retraction discipline
**Why out of scope**: Whether retraction should become a dedicated K-operation with a built-in unit-depth shape constraint (vs. remaining a layer convention) is a substrate-design decision for a future ASN; this note correctly treats it as a layer commitment and flags the tradeoff in Open Questions.

VERDICT: REVISE
