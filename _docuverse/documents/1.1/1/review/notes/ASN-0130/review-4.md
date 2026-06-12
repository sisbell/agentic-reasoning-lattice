# Review of ASN-0130

This is a strong note: the stratification of parse-layer (content-intrinsic) versus type-layer (registration-grounded) facts is exactly right, PR3a's substitution proof is genuinely worked rather than waved, the wp analyses are non-trivial and honest about the born-nullified boundary, and the worked composition exercises success, refusal, and the adversary case. I found two precision gaps, both fixable with localized text.

## REVISE

### Issue 1: The discipline-scope list omits PR-SIG, PR3, and PR3a, which consume discipline-dependent facts without carrying the qualifier

**ASN-0130, PR0 (Discipline and uniqueness)**: "The note's downstream claims — PR0's wp equivalence (…), PR1, PR2, PR5's lint reading, PS1's dedup reading — are scoped to derivations that are registration-disciplined and surface-disciplined (SD, ASN-0128)"

**Problem**: Three claims missing from this list depend on the same discipline and state no scope of their own:

- **PR-SIG's `sig` induction** asserts "At `a`'s first registration, PR0 (iv) has every referenced address `r` carrying an active tuple at the pre-state." That is guaranteed only when every `L_pdef`-growing step is a `register_pred` deposit — i.e., on registration-disciplined derivations. The entry-point seal does not close this: it seals the exposed `Emit_K` surface, but raw `K.λ_sh` steps remain in `→_sh` (which is precisely why the note defines discipline over derivations at all). A raw `pdef`-class deposit is admissible at the bare Multi gate — the static gate reads span counts, never content, as the note itself observes in the seal paragraph — and can deposit `F = enc({a})` over a run that never validated, leaving `sig(a)` ungrounded while the deposit counts as a "registration event."
- **PR3's evaluation precondition** spells "ever-registered" as the audit-slice fact "some `(b, F, G) ∈ L_pdef^Σ` with `addrs(F) = {a}`." That fact is a proxy for "the run validated at its deposit pre-state" only under registration discipline (PR3's own justification routes through PR1 and PR2(a), both explicitly discipline-scoped). Off-discipline, the audit fact can be true at an `a` whose run is not parse-valid, and PR3's resolution layer has no defined behavior there.
- **PR3a** inherits both: its hypothesis `sig(a) = (Γ_D, C_D)` consumes PR-SIG's induction, and its proof cites "the body's registration-state judgment … supplied by PR0 (iii) and permanent (PR1)" — PR1 being scoped.

Note the contrast: PR1 carries its qualifier in its own statement ("At any state Σ reached by a registration-disciplined derivation"); PR-SIG, PR3, and PR3a carry none, and the enumerated scope list reads as exhaustive.

**Required**: Either add PR-SIG's `sig` well-definedness, PR3, and PR3a to the scope list, or restate each with the registration-discipline qualifier (e.g., PR3's precondition as "ever-registered, where every `L_pdef`-growing step along the derivation is a `register_pred` deposit"). If the intent is instead that "registration" *means* a `register_pred` event by definition, then PR3's PL spelling of the precondition (`(E x ∈ L_pdef :: a ∈ addrs_F(x))`) must be flagged as equivalent to that meaning only under the discipline.

### Issue 2: "expand(a) ∈ ST" is undefined for parameterized expansions — PD0's classes are stated for state-predicates, and the certified object has free parameters

**ASN-0130, PR5a (iii)**: "*Class membership*: the checker's verdict `expand(a) ∈ ST` by PD0's rules." **PR5**: "asserting membership in PD0's **ST** class, the ⊤-stable spellings."

**Problem**: PD0's stability statement (ASN-0129) is about Boolean-valued state predicates — "Every ST term is *⊤-stable*: once true at a reachable Σ, true at every `→_sh*`-successor" — i.e., terms with a truth value at a state. For a definition with `k ≥ 1` parameters, `expand(a)` has free variables `Γ_D` and has no truth value until an environment binds them, so "expand(a) ∈ ST" and the stability it asserts are not well-posed as written. PD0's rules do classify quantifier-bound variables ("P(x, ·) ∈ ST" per binding, with side conditions like "argument a literal or bound address"), but a definition's *parameter* is a new kind of free variable that PD0 never confronts — named-parameter abstraction is exactly what this note adds. The note's own worked example exercises the gap: v2's certified body `(E x ∈ L_M :: t ∈ coverage_F(x))` has the free parameter `t` in the V-TUP test, which qualifies as a PD0 step-constant only if `t` counts among the "already-bound values" — a convention nowhere stated. The omission is conspicuous because the note polices the exactly analogous well-posedness for views at length (PR-VIEW: "'expand(a) ∈ ST' has a truth value only once a view is fixed" — restricting certification to view-independent expansions precisely so the asserted class is absolute). The parameter axis needs the same one-move treatment.

**Required**: State the certificate's meaning for open expansions: e.g., the syntactic check runs PD0's rules with parameters treated as bound constants of their declared sorts, and the certificate asserts that every `Γ_D`-instantiation of `expand(a)` is ⊤-stable (once true at a reachable Σ for given `args`, true at every `→_sh*`-successor for the same `args`). One or two sentences in PR5 or PR5a (iii), plus a clause noting the worked example's `t` is covered by this reading.

## OUT_OF_SCOPE

### Topic 1: Authorization — who may register, de-register, or certify
**Why out of scope**: The substrate has no principal model anywhere in the corpus — ASN-0086/0128's `Nullify` already lets any caller with a document retract any tuple, so "anyone can de-register anyone's definition" is the inherited stance, not a defect introduced here. An ownership/authorization layer over the validated surfaces is a future ASN. (Open Question 3 touches the adjacent policy question for dangling references.)

### Topic 2: Expansion cost and sharing
**Why out of scope**: Inlining at every reference node means `|expand(a)|` can grow exponentially in the stored reference DAG (a chain of definitions each applying its predecessor twice). Semantics are unaffected — PR3's determinacy pins the term, and PC5 termination holds — but memoized or DAG-shared evaluation is implementation territory, like the concrete encoding the note already fences off.

VERDICT: REVISE
