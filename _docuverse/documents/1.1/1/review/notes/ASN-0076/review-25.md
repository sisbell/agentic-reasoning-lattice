# Review of ASN-0076

## REVISE

### Issue 1: Citations to a non-existent foundation claim "SubAllocatorAxiom"
**ASN-0076, §E0 (and Foundation Recap, worked example)**: "SubAllocatorAxiom.FirstEmission (ASN-0047)", "SubAllocatorAxiom.T10aConformance", "SubAllocatorAxiom.Namespace", "SubAllocatorAxiom.Subspace".
**Problem**: ASN-0047 contains no claim named `SubAllocatorAxiom`, and no dotted sub-properties `.FirstEmission / .T10aConformance / .Namespace / .Subspace`. The relevant foundation item is `SubAllocatorBundle` (a LEMMA), whose body states the determinate first emission `[d.0.s_L.1]` with `origin = d`, `#E = 2`, `zeros = 3`, T4-validity, freshness, and the T10a `inc(·,0)` discipline — and which itself says these "are inherited from ASN-0093's sub-allocator lemmas." The K.λ first-emission/subsequent-emission *rule* the proof depends on (`ℓ_new = [d_new.0.s_L.1]`, `ℓ_sup = inc(max{…}, 0)`) is likewise attributed to a named axiom that the foundation does not expose under that name. As written, the load-bearing discharges of every K.λ precondition cite a dependency a reader cannot resolve.
**Required**: Retarget every `SubAllocatorAxiom.*` citation to the actual foundation claim(s) — `SubAllocatorBundle` and/or `AllocatorHierarchy` (ASN-0047) — and confirm each cited sub-fact (first-emission form, subsequent-emission `inc(max,0)` form, `zeros=3`, `subspace_I = s_L`, freshness) is genuinely supplied by the named claim. If the first/subsequent-emission *rule* of K.λ lives only in ASN-0093 (a non-foundation ASN), the construction cannot rest on it without restatement.

### Issue 2: E7 "LineageDiscoverability" diverges from the foundation's discoverability notion without reconciliation
**ASN-0076, §E7**: defines `covers(Σ, a)` and concludes "Any discovery operation that returns `covers(Σ, ·)` … will surface `ℓ_sup`."
**Problem**: ASN-0098 (a declared dependency) already fixes a precise discoverability framework: `discoverable_from(a, d, Σ)` holds iff `coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅` (LP12), and LP17 (GhostProjection) classifies a link whose coverage meets no arrangement range as *orphaned*. EDITLINK never places `ℓ_sup`, `ℓ_new`, or `ℓ_old` into any arrangement (E10: no K.μ⁺_L). Therefore, unless the referents are independently arranged, `ℓ_sup` is orphaned in the exact ASN-0098 sense and is **not** `discoverable_from` any document. E7 introduces a parallel, arrangement-independent `covers` predicate and labels the result "discoverability," which collides with the foundation's established (stricter) meaning. The prose hedge ("E7 establishes only that the structural witness is present") is correct but does not reconcile the term against the dependency.
**Required**: Either relate `covers` explicitly to ASN-0098's `project`/`discoverable_from` (noting that `covers` is the *inverse* lookup and that `ℓ_sup` is orphaned per LP17 absent arrangement of its referents), or rename the property to avoid asserting "discoverability" in a sense the cited foundation contradicts. State plainly that E7 is a structural-witness claim, not an ASN-0098 discoverability claim.

### Issue 3: Worked-example E4 verification conflates span-membership with coverage
**ASN-0076, Worked Example, E4 check**: "By PrefixSpanCoverage, coverage(…) = {t : ℓ_old ≼ t}, which includes ℓ_old by reflexivity. So (ℓ_old, δ(1, 8)) ∈ Σ'.L(ℓ_sup).e₁".
**Problem**: The conclusion is a span-membership fact (`(ℓ_old, δ(1,8))` is an element of the endset `E_from`); it follows directly from the construction `E_from = {(ℓ_old, δ(1,8))}`, **not** from the coverage equation. `ℓ_old ∈ coverage(span)` is a different statement and does not entail the span being a member of the endset. The "So" is a non-sequitur. The main E4 proof does this correctly (K.λ effect → `Σ' = Σ₂` → L6 slot accessor → singleton membership); the worked example should mirror it.
**Required**: Replace the coverage-based justification in the example with the singleton-membership / L6 chain used in the E4 proof. Keep the coverage remark only where it belongs (E7, where coverage of `ℓ_old` is the relevant fact).

## OUT_OF_SCOPE

### Topic 1: Supersession-type address convention and reader resolution policy
**Why out of scope**: The semantics that distinguish a "supersession-type" `τ_sup` from any other type address, the choice policy among divergent successors (E5), and termination of lineage navigation are explicitly deferred. The ASN is honest that E4/E7 are structural-only and that the Appendix is illustrative. These are genuinely new territory (a type-endset-convention ASN), not defects here.

### Topic 2: Authorization model behind E6
**Why out of scope**: E6's informal "Alice/Bob/Carol" ownership story presumes an authorization layer (who may fire K.λ on which document). The abstract K.λ has no executor field; the formal claim correctly reduces to `d_new ∈ E_doc`. The authorization model belongs to a future capabilities ASN.

META: not applicable — the ASN defines an operation as a composite of state-transition primitives and proves abstract invariant preservation and entity-relationship guarantees; it has not drifted into implementation mechanics.

VERDICT: REVISE
