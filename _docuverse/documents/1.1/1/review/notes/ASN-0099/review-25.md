# Review of ASN-0099

## REVISE

### Issue 1: Reused name `d_c` for two different hypothetical documents

**ASN-0099, worked example**: The F10 verification paragraph ("Verifying F10 across a version extension") defines `d_c = inc(d_a, 1)` — a version of `d_a` produced by K.δ at `k = 1`. Query 10 step (i) then defines `d_c = inc(d_b, 0)` — a sibling of `d_b` produced by K.δ at `k = 0`.

**Problem**: The same symbol `d_c` is used for two structurally different documents (version-extension descendant vs. sibling under same account). Even with the "this paragraph is local" qualifier in the F10 verification, the reuse creates confusion when readers move between sections. A reader reaching Query 10 may incorrectly attempt to import constraints from the F10 paragraph's `d_c`.

**Required**: Rename one of the two instances — for example, `d_v` for the F10 version-extension document, leaving `d_c` for Query 10's sibling document. Consistent naming is especially important in a worked example exercising both T1 case (i) and case (ii) ordering arguments, where the structural difference between sibling and version is the load-bearing distinction.

### Issue 2: F4 weakening-direction discharge has subtle self-reference that the framing only partially resolves

**ASN-0099, F4 (MatchFormulaMinimality)**: "An alternative implementation conforming to a weakening `P_w` of F1 ... would, by hypothesis, conform to F3 with `matches := P_w` — that is, satisfy F3's literal contract as parameterised by its own match predicate — and so return links satisfying `P_w` but not F1."

**Problem**: The argument requires F1 to be "fixed at the meta-level" while F3 is evaluated against the alternative `P_w`. The framing paragraph addresses this, but the discharge then asserts that "the alternative implementation fails the conformance test at the F1-non-admitted pair" — which is essentially restating that any predicate different from F1 differs from F1. The substantive content is the realizability discharge (links with the differing match status can be constructed via K.λ), but this content is presented as a downstream consequence rather than the load-bearing argument.

**Required**: Restructure F4's weakening direction to lead with realizability: "For any predicate `P_w` admitting strictly more pairs than F1, there exists a pair `(a, I)` admitted by `P_w` but not F1; K.λ realizability constructs a state where this pair is observable as an excluded link in F1-fixed F3." The meta-level framing then becomes incidental rather than load-bearing.

### Issue 3: A1's closed-world reading is grounded interpretively rather than directly

**ASN-0099, A1 (LinkStoreInertOfNonAllocatingOperations)**: The derivation for K.μ⁺, K.μ⁻, K.ρ rests on "the substrate's effect-clause convention" under a "closed-world reading," with the convention grounded on Nelson's design intent and Gregory's implementation evidence.

**Problem**: The closed-world reading is not stated as a convention anywhere in the substrate ASNs (ASN-0093, ASN-0047). A1 is load-bearing for F9-cor, F9★, F9★-cor and Query 10's verification, so the derivation chain leans on a meta-textual interpretation that the substrate does not explicitly endorse. The two converging sources (design intent + implementation evidence) are consultative rather than direct — they justify the convention without proving it from substrate axioms.

**Required**: Either (a) cite LP12a (LinkStoreMonotonicity, ASN-0093) which gives `dom(Σ.L) ⊆ dom(Σ'.L)`, then argue equality from the joint absence of L from both effect and frame clauses at K.μ⁺, K.μ⁻, K.ρ; or (b) explicitly acknowledge that the closed-world reading is a conventional interpretation that this ASN adopts and downstream consumers inherit. The current presentation conflates derivation with interpretation.

### Issue 4: F2/F3 verification in the worked example tests the spec against itself rather than against an implementation

**ASN-0099, worked example**: "Verifying F2 (Completeness) against the instance. ... The comprehension `{a ∈ dom(Σ.L) : matches(a, {α₂}, Σ)}` evaluates to `{ℓ}`. Completeness holds."

**Problem**: F2 and F3 are conformance contracts on a separate `result(·, ·)` implementation function. The verification only checks that the abstract `findlinks` comprehension produces `{ℓ}` — it doesn't engage with an actual implementation. The phrasing "Completeness holds" is a category error: completeness is a property of an implementation relative to the spec; what the verification actually shows is that F2 demands `{ℓ} ⊆ result({α₂}, Σ)`.

**Required**: Reframe the verification as "F2 obligates any conforming implementation to satisfy `result({α₂}, Σ) ⊇ {ℓ}`; F3 obligates `result({α₂}, Σ) ⊆ {ℓ}`; jointly, `result({α₂}, Σ) = {ℓ}`. The abstract specification produces `{ℓ}` for this instance." This makes the obligation/verification distinction explicit.

### Issue 5: F9★ is in the claims table but never explicitly verified in the worked example

**ASN-0099, claims table**: F9★ (EditOnlySurvivability) is listed as "introduced" — the multi-step closure of F9 within the K.μ-only fragment.

**Problem**: Query 10 verifies F9★-cor (the broader V ∖ {K.λ} closure) via a 5-step sequence interleaving K.δ, K.α, K.μ⁺, K.ρ, K.μ⁻. F9★ is the K.μ-only specialization, which is the "operationally salient sequence in the editing surface" per the ASN's own framing. The worked example never exhibits a K.μ-only chain. A reader wanting to see F9★ in action must construct one mentally.

**Required**: Either add a brief K.μ-only multi-step verification (e.g., a K.μ⁻ followed by K.μ⁺_L), or note explicitly in the claims table that F9★ is verified as the K.μ-only specialization of F9★-cor's Query 10 verification — making the relationship between F9★ and F9★-cor's worked exhibit explicit.

### Issue 6: F1's status in the claims table is "introduced" but it functions as a definition

**ASN-0099, claims table**: F1 (MatchPredicate) is listed with status "introduced" — distinct from F12, `matches(a, I, Σ)`, etc. listed as "definition."

**Problem**: F1's body is `matches(a, I, Σ) ≡ (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)` — this is the definitional equation introducing the `matches` predicate. F4 (MatchFormulaMinimality) then argues for its uniqueness. The "introduced" label is inconsistent with the table's own use of "definition" for analogous definitional equations.

**Required**: Relabel F1 as "definition" (matching `matches(a, I, Σ)` already listed as "definition" earlier in the table) or merge the two rows. The current table has both `matches(a, I, Σ)` and F1 (MatchPredicate) as separate entries pointing at the same predicate, which is redundant.

## OUT_OF_SCOPE

None — the ASN's "What We Have Not Specified" section appropriately defers procedure, multi-physical-instance protocols, caching, fine-grained access control, the inverse direction (FOLLOWLINK), and phantom-address semantics. None of these defer-to-future items are operationally captured by the prompt's explicit scope list (INSERT/DELETE/COPY/REARRANGE mechanics, version creation, BEBE).

VERDICT: REVISE
