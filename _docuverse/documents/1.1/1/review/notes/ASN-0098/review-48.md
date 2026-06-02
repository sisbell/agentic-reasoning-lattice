# Review of ASN-0098

I checked the projection algebra (LP4–LP11), the discoverability/wp claims (LP12–LP18), and the substrate-finitude machinery (LP-Sub, LP-Fin, LP19–LP21) against the foundations. The mathematics is largely sound and unusually thorough — the LP-Fin interval argument, the K.μ~ rebinding proof, and the worked trace all hold up under case-by-case checking. Two substantive items and one prose item remain.

## REVISE

### Issue 1: T4-validity of `F`-members is justified by a lemma that does not cover the unregistered documents `F` explicitly includes

**ASN-0098, "Boundary and Width Behaviour" (definition of `F`)**: "An address of the form `[d, 0, s, k]` with `d` T4-valid, `zeros(d) = 2`, `s ∈ {s_C, s_L}`, and `k ≥ 1` is exactly the structural form FirstEmission and ChainDiscipline (ASN-0093) fix for a chain element of the sub-allocator `A_C(d)` (resp. `A_L(d)`), so its T4-validity is delivered directly by ChainElementT4Validity (ASN-0093)."

**Problem**: `F` is defined to range over *all* T4-valid document tumblers `d` with `zeros(d) = 2`, and the prose is explicit that this includes documents "not yet registered, since future K.σ transitions can activate their chains." But `ChainElementT4Validity` (ASN-0093) is a statement about elements of `A_C(d)` / `A_L(d)` — sub-allocators that `SubAllocatorBundle` activates only "for each `d ∈ E_doc`," i.e. registered documents. For an unregistered `d`, `A_C(d)` is not an active chain, so the cited lemma does not apply to those members of `F`. The T4-validity conclusion is nonetheless true — but it follows *structurally* (`[d,0,s,k]` with `d` T4-valid having `zeros=2`, an isolated third zero at position `#d+1` flanked by non-zero `d_{#d}` and `s`, first component `d₁≠0`, last component `k≥1` ⇒ all four T4 clauses hold), not via the chain lemma.

**Required**: Replace the `ChainElementT4Validity` citation with the direct structural T4 check on the form `[d, 0, s, k]`, which covers registered and unregistered `d` uniformly. Reserve the chain-lemma citation for `LP-Sub`, where membership genuinely comes from active chains.

### Issue 2: `F`'s informal introduction names its downstream consumer instead of advancing the definition

**ASN-0098, "Boundary and Width Behaviour" (first paragraph)**: "The set `F` of *substrate-emittable addresses* is the domain against which the 'boundary insertion does not extend the link' property is formalised — the addresses the substrate could K.α/K.λ-emit within a span's reach, excluding the T4-invalid zero-extensions `s.0`, `s.0.0`, … that a raw span includes but no allocator chain can emit."

**Problem**: `F` is introduced twice — once here (a purpose-preview that defers to the LP19 property it will later serve) and once in the next paragraph as the formal set-builder. The first clause ("the domain against which the … property is formalised") is a use-site preview of a downstream consumer, not content that advances the definition's meaning. The reader must reach the formal `F = {…}` to learn what `F` is; the preview is skip-past prose.

**Required**: Fold the genuinely contentful part (the zero-extension exclusion intuition) into the formal definition paragraph and drop the downstream-consumer preview.

### Issue 3: LP6, LP7, LP14 triplicate one frame-template

**ASN-0098, LP6 / LP7 / LP14**: each paragraph reads, in different words, "operation X has frame `(A d :: M'(d) = M(d))`, preserves `dom(Σ.M)`, so by LP4 `project(e, d, Σ') = project(e, d, Σ)`."

**Problem**: The three are the same one-step argument instantiated at K.α, K.λ, K.ρ. The repetition is the "multiple paragraphs say the same thing in different words" pattern.

**Required**: State the template once ("any transition whose frame fixes every `M(d)` and preserves `dom(Σ.M)` leaves every projection fixed, by LP4") and list the three instances as a single sentence, retaining the LP6/LP7/LP14 labels for citation.

## OUT_OF_SCOPE

### Topic 1: Reverse-discovery, V-order/I-order correspondence, link-to-link induced discovery
These are correctly deferred to the Open Questions section as future ASNs; the per-state and per-operation projection algebra needed to formulate them is established here.

VERDICT: REVISE
