# Review of ASN-0126

## REVISE

### Issue 1: "Binary" registration does not entail the unit-depth retraction discipline

**ASN-0126, Single-source**: "Registering R Binary therefore matches both authorities and keeps ASN-0086's UnitDepthRetractionDiscipline intact: every `L_R` tuple still carries a single unit-depth to-span `{(a, δ(1, #a))}`, exactly the discipline's requirement, so R-Scope's single-tuple-scope result ... continues to hold."

**Problem**: The Binary shape's conformance condition is `|F| = 1 ∧ |G| = 1` — *one span*, full stop. It does **not** require that the single G-span be unit-depth `δ(1, #a)`. A tuple with `G = {(t, ℓ)}` for any non-unit `ℓ` (e.g. covering a multi-address contiguous range, `ℓ = δ(2, #t)`) is `|G| = 1`, hence Binary-conformant, hence admitted by `Sh-conf(R, F, G)` and by `K.λ_sh`. The inference "R Binary ⟹ every `L_R` tuple carries a unit-depth to-span" is therefore invalid: Binary is strictly weaker than the unit-depth discipline. The unit-depth property in ASN-0086 comes from the *Nullify operation's construction* (`Emit_R(…, {(a, δ(1, #a))})`), which is a layer-level/operational commitment — not from any shape registration. Consequently R-Scope's `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` is **not** preserved by Binary registration either: R-Scope depends on the to-span being unit-depth (so that `coverage(G) = {t : a ≼ t}` and R0a's antichain forces the intersection to `{a}`); a Binary-but-non-unit-depth G covers more, and the single-tuple-scope conclusion fails.

**Required**: Either (a) add a unit-depth precondition to R's retraction emit at the framework level (a strictly stronger shape than generic Binary), or (b) explicitly state that the unit-depth discipline remains an ASN-0086 *layer commitment* not subsumed by Binary registration, and retract the claim that Binary registration alone "keeps the discipline intact." As written the note overclaims a structural guarantee that is actually operational.

### Issue 2: `K.λ_sh` has no arity precondition, but `Sh-conf` is defined only on triples

**ASN-0126, The shape-gated emit**: "`K.λ_sh` is `K.λ` with two added preconditions: (i) *K is registered* ... and (ii) `Sh-conf(K, F, G)`."

**Problem**: `K.λ` inherited from ASN-0086 admits any arity ≥ 3 (its only precondition is L3). `Sh-conf(K, F, G)` is defined over a *standard triple* `(F, G, K)` — it reads exactly two content slots. For a higher-arity emit `(e₁, e₂, e₃, e₄, K)` the predicate has no defined reading: does it test `(e₁, e₂)` and silently ignore `e₄`, or is the step inadmissible? The Single-source section's stated intent is that higher-arity goes through *direct link-store interaction*, i.e. outside `→_sh` — which means `K.λ_sh` should be restricted to arity 3. But no such precondition appears. This leaves P4's universal claim ("No `→_sh`-step extends `dom(Σ.L)` with a tuple ... for which `Sh-conf(K, F, G)` fails") ill-defined for arity > 3.

**Required**: Add an explicit `|value| = 3` (standard-triple) precondition to `K.λ_sh`, or define `Sh-conf` to return `⊥` on non-triples. Then P4 quantifies over a well-defined set.

### Issue 3: The disciplined-domain wp simplification relies on layer-reachability that `→_sh` does not establish

**ASN-0126, The shape-gated emit / Registry permanence**: "*Disciplined-domain simplification.* At a layer-reachable state ASN-0086's third conjunct holds vacuously (its unit-depth retraction discipline with R0a forces `a_emit(Σ, d) ∉ coverage(G')` ...)."

**Problem**: This simplification is invoked to reduce the framework's wp to `K registered ∧ Sh-conf(K, F, G) ∧ d ∈ dom(Σ.M) ...` at the states `→_sh` reaches. But ASN-0086's *layer-reachability* is strictly stronger than `→*`-reachability: it additionally requires every `→`-step that grows `L_R` be a `Nullify` (with unit-depth G). The projection argument `π` you give establishes only that every `→_sh`-reachable state projects to a `→*`-reachable state — **not** to a *layer-reachable* one. Combined with Issue 1, `→_sh`'s gate (Sh-conf at Binary) does not enforce the discipline commitment, so `→_sh`-reachable states are not known to be layer-reachable, and the vacuity of the third conjunct cannot be imported.

**Required**: Either prove that every `→_sh`-reachable state projects to a layer-reachable ASN-0086 state (which requires the unit-depth fix of Issue 1), or present the disciplined-domain simplification strictly as a conditional ("*if* at a layer-reachable state") and do not use it to characterize what `K.λ_sh` checks at general `→_sh`-reachable states.

## OUT_OF_SCOPE

### Topic 1: The "no fourth shape / single-source captures every pattern" claims
**Why out of scope**: These are empirical claims about the lattice's *usage* ("classifiers, citations, supersession chains, holdings"), not provable invariants of substrate state. They are appropriately framed as modest, and their validation belongs to usage/registration practice, not to a state-invariant proof in this ASN.

### Topic 2: Idem flag semantics, behavior catalog, default predicates, R standardization
**Why out of scope**: Explicitly deferred to the operational successor (Open questions #1–6). The note correctly commits only to the flag's structural presence and state-independence (P3).

VERDICT: REVISE
