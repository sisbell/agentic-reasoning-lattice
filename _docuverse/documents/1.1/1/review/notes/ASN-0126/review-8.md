# Review of ASN-0126

## REVISE

### Issue 1: Registration-check decidability rests on an unstated finiteness condition

**ASN-0126, Registration entries / C0**: "`Σ_init.registry` is well-formed — i.e. it *is* a partial function `T_admissible/~ ⇀ (name, shape, idem)`."

**Problem**: The note's stated value proposition is "a finite shape catalog" and "a static shape-conformance check the substrate can apply at every emit." Precondition (i) of `K.λ_sh` is "*K is registered* — the registry records a shape for K," which at emit time requires deciding whether `coverage(K)` matches a registered coverage class. C0 formalizes the registry only as a *partial function over the infinite domain* `T_admissible/~`; it imposes no finiteness. A partial function over an infinite domain need not be finitely representable, and membership ("is `[K]` a key?") need not be decidable. So the central guarantee — that (i) is a static, applicable-at-every-emit check — is asserted but not grounded. The intro promises finiteness; the formalization drops it.

**Required**: Add registry finiteness to C0 / well-formedness (`|Σ_init.registry| < ∞`, paralleling L-fin), and state that the decidability of precondition (i) follows from finiteness together with CoverageEqualityDecidable (ASN-0086) — check `coverage(K)` against each of finitely many registered keys.

### Issue 2: The worked illustration never exercises the non-trivial wp case

**ASN-0126, The shape-gated emit / Worked illustration**: the note identifies the active-subset wp as "the proper depth artifact" and singles out the subtle separation — "the gate fires the emit … yet the tuple is born nullified and `(a, F, G) ∉ A_K^{Σ'}`."

**Problem**: The Worked illustration grounds only P4 (Sh-conf verdicts) and P5 (ghost state-independence). It never instantiates the analytically richest claim: a gate-enabled emit whose third wp conjunct fails, so the tuple lands in `L_K^{Σ'}` but not `A_K^{Σ'}`. That born-nullified scenario is the whole point of the gate-vs-landing distinction, and the note even argues such a covering tuple is *attainable* at a general `→_sh`-reachable state (because `→_sh` enforces only Binary, not unit-depth, on R). Asserting attainability without a concrete witness is exactly the gap the standards flag.

**Required**: Add a concrete instance — e.g. emit a Binary R-tuple with a non-unit `G` covering a range of link addresses, then emit a conforming non-R tuple whose fresh `a_emit` falls in that coverage; show all of (0),(i),(ii) hold (gate fires) yet `(a,F,G) ∉ A_K^{Σ'}` because the third inherited conjunct is false.

### Issue 3: Opening universal claim overclaims relative to the framework's scope

**ASN-0126, Single-source**: "Every typed relation has a single-span source — `|F| = 1`."

**Problem**: This is stated as a fact about *every* typed relation, but the framework only constrains `F` on *registered* types emitted via `→_sh`. The note itself later says "The link store underneath the substrate (ASN-0043) permits arbitrary higher arity, and an app needing multi-source relations can interact with the link store directly." A typed relation filed directly into the link store may have `|F| > 1`. So the universal opening sentence contradicts the later scoping clause.

**Required**: Scope the claim — e.g. "Every typed relation *the framework gates* (every registered relation emitted under `→_sh`) has `|F| = 1`."

## OUT_OF_SCOPE

### Topic 1: Static enforcement of the unit-depth retraction discipline

The note is candid that Binary registration of R is strictly weaker than ASN-0086's UnitDepthRetractionDiscipline, and that `→_sh` cannot enforce unit-depth at the gate — it remains an operational commitment on the Nullify *construction*. Whether the substrate should statically enforce unit-depth (or whether range-retraction tuples are legitimately admissible) is a layering/standardization question, already gestured at in Open Question #4. Not an error here.

### Topic 2: idem flag semantics

The flag is introduced with only structural presence + state-independence (P3). Its operational meaning (idempotent emit, nullification/re-emission interaction) is explicitly deferred to the successor. Minimal structural commitment is acceptable; the semantics belong in the successor note.

VERDICT: REVISE
