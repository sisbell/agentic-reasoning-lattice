# Review of ASN-0133

## REVISE

### Issue 1: The "stutter Σ →_sh* Σ" witness does not exist

**ASN-0133, W (Work)**: "The registry-level universal `|W(σ)| < ∞` for *every* σ from Σ₀ (H-W) holds iff every reachable state is quiescent — the contrapositive: any trigger-true prefix extends to an infinite σ by the stutter `Σ →_sh* Σ`, forcing `|W(σ)| = ∞`".

**Problem**: There is no stutter. Every `→_sh` step is `K.σ ∪ K.α ∪ K.λ_sh`, each of which *strictly grows* one of `dom(Σ.M)`, `dom(Σ.C)`, `dom(Σ.L)` (the foundation step effects). So `Σ →_sh* Σ` with one or more steps is impossible, and the reflexive (zero-step) reading does not extend a prefix to an *infinite* σ. The only other way to keep the state at Σ is a no-op fire (`Σ' = Σ`), but RG makes a no-op fire require an available *trigger-false* `(ρ', x')` with `x' ∈ [D_{ρ'}]` — which need not exist at a non-quiescent state (e.g. a single rule with a one-element domain that is trigger-true). For exactly the states the universal claim must cover, the stated construction produces no infinite σ. Since the circularity verdict ("H-W restates the conclusion") rests entirely on this construction, the stated proof of the load-bearing direction (∃ non-quiescent reachable Σ ⟹ ¬H-W) is unsupported.

**Required**: Replace the stutter with a construction that actually realizes `|W(σ)| = ∞`. The clean one: from a reachable non-quiescent Σ with `(ρ, x)` trigger-true, extend σ by environment `K.α` (content) deposits — *no* PL trigger reads `dom(Σ.C)` (it has no QD base and no membership atom, V-DOC/QD-audit, ASN-0129) — so `T_ρ(x, ·)` is preserved at every later index, giving `(ρ, x, k) ∈ W(σ)` for all `k` and hence `|W(σ)| = ∞`. State explicitly *why* the literal stutter fails (strict domain growth; no-op fires need a trigger-false argument).

### Issue 2: Forward-reference accretion around Q5a (anti-bloat)

**ASN-0133, W (closing clause) and the standalone "H-RF and bounded growth" paragraph**: W ends "...the load-bearing registry-level bound is Q5a's distinct-argument count `|⋃_k [D_ρ]|`, treated below." The next paragraph reopens the same orientation: "Bounded domain growth (Q5a) is strictly stronger ... it implies H-RF, not conversely ... so it sits strictly between H-RF and the conclusion and *is* the load-bearing registry-level strengthening".

**Problem**: Two consecutive paragraphs both forward-defer to Q5a as "the load-bearing registry-level bound/strengthening" and both pre-state the relation `bounded-growth ⟹ H-RF (not conversely)` that **Q5a then proves in full** (with its own counterexample: "a fair scheduler facing an environment that flags infinitely many distinct targets..."). The "H-RF and bounded growth" paragraph adds nothing reasoned — it is a map paragraph — and it forward-references **case (3)** ("case (3)'s out-of-phase cycling holds every state non-quiescent under bounded growth") two sections before case (3) is defined in Q6. This is precisely the forward-reference meta-prose the `anti-bloat` classifier targets: the reader must hold a not-yet-defined case and a not-yet-proven implication in suspension to parse an orientation already discharged downstream.

**Required**: Delete the standalone "H-RF and bounded growth" paragraph and the redundant closing clause of W; let Q5a establish the strict-strengthening (it already does) and let Q6 use H-RF where it needs it. If a one-line pointer is wanted, keep only "Q5a's domain bound implies H-RF strictly (proof there)," without the case-(3) forward reference.

### Issue 3: The "emissions, not bodies" principle is stated twice (anti-bloat)

**ASN-0133, RG and Q2**: RG asserts "two implementations producing the same emissions are indistinguishable." Q2 (ContractOnOutputs) asserts "any two bodies with the same outputs are equivalent under it."

**Problem**: Two paragraphs say the same thing in different words — the abstraction "bodies are identified by their emission sets" appears as a modeling aside in RG and again as the named claim Q2. Q2 is the home for it; the RG sentence is a preview that the precise reader must reconcile against the later claim.

**Required**: State the principle once. Either drop the RG aside and let Q2 carry it, or have RG cite Q2 forward without restating the equivalence.

### Issue 4: Mismatched foundation citation in the worked trace (precision/anti-bloat)

**ASN-0133, "A reached terminal state"**: "one `Emit_cmt` depositing `c` covering `t` — a single `→_sh` step, atomic by H-ATOM via I4."

**Problem**: I4 (ConcurrentEmitFirstCommit, ASN-0128) is about *concurrent* emits and serialization order; there is no concurrency here. The fact actually being cited — that an `idem=⊥` `Emit_cmt` is *one* `K.λ_sh` step — is I5 (IdemFalseAlwaysFresh) / I1's miss branch. Atomicity of a single step is then trivial under H-ATOM. "via I4" is a gratuitous, wrong-lemma citation.

**Required**: Cite I5 (or I1 miss) for "single `→_sh` step"; drop "via I4."

## OUT_OF_SCOPE

### Topic 1: Concrete scheduler, the SF (`pd_extinct`) certificate, runtime divergence detection, per-scope vs. global settling, cross-scope re-entry bounds

**Why out of scope**: These are correctly enumerated in "What this note doesn't cover" and the Open Questions. They are new territory (operational machinery and future certificate classes), not defects in this note's guarantees.

### Topic 2: Termination under composition of two cooperating registries

**Why out of scope**: The note subsumes other registries into the environment (whose bounded-input hypothesis Q5a names), so a genuine *compositional* termination theorem (A∘B terminates given A, B each do, without the over-approximation of treating one as adversarial environment) is a reasonable future ASN, not a gap here.

VERDICT: REVISE
