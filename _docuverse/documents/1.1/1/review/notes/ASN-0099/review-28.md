# Review of ASN-0099

Reviewing this ASN carefully against the foundation ASNs and the standards in the brief.

## REVISE

### Issue 1: A1's load-bearing convention should be more sharply distinguished from substrate axiom inheritance

**ASN-0099, A1 (LinkStoreInertOfNonAllocatingOperations)**: A1 is labeled "derived structural lemma" with the conclusion `dom(Σ'.L) = dom(Σ.L) ∧ ...` for V ∖ {K.λ}.

**Problem**: For K.σ, K.α, K.δ, K.μ~, K.μ⁺_L the preservation follows directly from published `L' = L` frame clauses — this is genuine derivation from substrate axioms. For K.μ⁺, K.μ⁻, K.ρ the preservation rests entirely on the "closed-world reading" — a convention this ASN adopts. The substrate-published lemmas L12 (LinkImmutability) and L12a (LinkStoreMonotonicity) give only `dom(Σ.L) ⊆ dom(Σ'.L)` with value preservation conditional on `a ∈ dom(L)`; they permit `dom(Σ'.L) ⊋ dom(Σ.L)` at these three operations. The domain-equality conjunct of A1 at these operations is *not* derivable from substrate axioms alone — it requires the closed-world reading. The ASN is honest about this in A1's body text, but the single label "derived structural lemma" papers over the methodological distinction between cases (a) and (b). This matters because downstream claims (F9, F9-cor, F9★-cor, F17, F18) inherit A1 without each invocation surfacing that A1's reach at K.μ⁺/K.μ⁻/K.ρ depends on a non-axiomatic convention.

**Required**: Either split A1 into A1a (derived from published frames, case (a)) and A1b (convention-grounded, case (b)), or relabel A1 as "convention-grounded structural lemma" with the closed-world dependency marked at every downstream citation site. Alternatively, the cleanest fix is to lift the closed-world reading into ASN-0047 as an explicit substrate convention, after which A1 becomes a true derived lemma.

### Issue 2: F4's "unique match predicate" claim conflates definitional and operational uniqueness

**ASN-0099, F4 (MatchFormulaMinimality)**: "F1's slot-existential / singleton-overlap form is the unique match predicate."

**Problem**: The framing paragraph immediately following F4's statement adequately bounds the claim ("F4's uniqueness is stated *relative to the reader's promise*"), but the labeled claim itself reads as an absolute uniqueness theorem. The substantive content is meta-level: F1 is the unique fixed point of "the operation whose match predicate is F1." Any predicate P ≠ F1 defines a different operation, so trivially only F1 defines F1's operation. The non-trivial content is the realizability discharge — that the operational gap is observable at K.λ-realized states. The claims table entry repeats "unique match predicate" without the operational qualifier, so a reader scanning the table misses the framing.

**Required**: Carry the operational qualifier into F4's claim statement and the claims table entry. E.g., "F1's form is the unique match predicate up to operational distinguishability via F2 ∧ F3 conformance, with the operational gap realizable at K.λ-reachable states." This makes the claim's epistemic status visible at the citation surface.

### Issue 3: The case (ii)→case (i) lifting in F10's version-extension derivation deserves a citation handle

**ASN-0099, F10 (OrderedResult), "Verifying F10 across a version extension" paragraph**: The argument lifts T1 case (ii) on documents (`d_a ≺ d_v`) to T1 case (i) on anchors (`b_L(d_a) < b_L(d_v)` via component divergence at position #d_a + 1).

**Problem**: This lifting — "case (ii) on documents becomes case (i) on anchors because the appended `.0.s_L` introduces a divergence position" — is a recurring pattern in cross-document ordering arguments. The ASN walks through it explicitly for d_a/d_v but treats the general lifting as inline reasoning. Downstream derivations (the hypothetical n-document case, the iterated chain in the closing paragraph of F10) lean on the same lifting without citing a labeled lemma. The lifting is a discrete structural fact that warrants a citation handle to keep these chains auditable.

**Required**: Either name the lifting as a labeled lemma in the ASN (e.g., "F10a: AnchorLiftingOfDocumentOrdering — for any d_1 ≺ d_2 with `zeros(d_1) = zeros(d_2) = 2`, b_L(d_1) < b_L(d_2) via T1 case (i) at position #d_1 + 1"), or cite the version-extension paragraph explicitly when invoking the result in subsequent paragraphs.

### Issue 4: F2-V ∧ F3-V's derivation from F2 ∧ F3 conflates two conformance models

**ASN-0099, after F3-V**: "F2-V ∧ F3-V admits a one-line derivation from F2 ∧ F3 once the implementation's V-side output is taken to coincide with the abstract two-phase composite — that is, once `result_V(R, d, Σ) = result(image(R, d, Σ), Σ)` at every `(R, d, Σ)`..."

**Problem**: The derivation requires the implementation's `result_V` to factor through its `result`. But the ASN immediately notes: "an implementation may expose `findlinks_V` directly as its reader-facing surface — bypassing any internal `result` function — and would in that case be bound by F2-V ∧ F3-V without an intermediate `result` call to discharge." This leaves the conformance model ambiguous: is F2-V ∧ F3-V a *consequence* of F2 ∧ F3 (when implementations factor through `result`), or a *parallel obligation* (when they don't)? The two readings have different implications — if F2-V ∧ F3-V can hold independently, it can in principle disagree with F2 ∧ F3 evaluated at the same state. The ASN's text says "both are operationally equivalent under the definitional equality F12" but doesn't formalize what "operationally equivalent" means at the conformance level.

**Required**: State explicitly whether F2-V ∧ F3-V is an independent conformance pair (the implementation must satisfy both this and F2 ∧ F3 independently for the two surfaces) or a derived consequence (F2 ∧ F3 implies F2-V ∧ F3-V via F12). The intended reading appears to be "independent for implementations exposing findlinks_V directly, derived otherwise" — surface this disjunction at the claim level.

### Issue 5: F4's "any other refinement" universal closure leans on undischarged reachability

**ASN-0099, F4 strengthening direction, "Any other refinement (reachable exclusions)" paragraph**: "any predicate `P` that excludes a *reachable* F1-admitted pair `(a, I)` ... defines a different match predicate."

**Problem**: The argument enumerates three concrete strengthenings (coverage ⊆ I, I ⊆ coverage, cardinality ≥ k > 1) each with explicit witnesses, then closes with the universal "any other refinement." The closure relies on the claim that "the entire space of F1-admitted pairs is reachable" via K.λ allocation. The realizability discharge that follows is solid for endset-configuration realizability, but does not address whether *every* shape of P-exclusion (every conceivable predicate strengthening) is witnessed by *some* F1-admitted pair that the realizability machinery covers. For instance, a strengthening like "F1 ∧ #spans(eᵢ) ≥ 2" — requiring multi-span endsets — would exclude a pair F1 admits, and the realizability argument needs to exhibit a witness pair with single-span endsets (which it does, but only for the enumerated cases). The universal "any other refinement" implicitly claims the three enumerated witness *shapes* (single canonical spans at slot i with various I-set choices) suffice to defeat *every* strengthening, but this is not argued.

**Required**: Either supply an argument that the enumerated witness shapes are universally adequate (e.g., "any strengthening admitting at least one (a, I) pair not in F1's admission can be defeated by a single-canonical-span witness because…"), or weaken the closure to "any strengthening covered by the enumerated witness shapes" with an explicit boundary for what's not covered.

VERDICT: REVISE
