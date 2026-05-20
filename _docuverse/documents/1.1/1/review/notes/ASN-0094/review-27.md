# Review of ASN-0094

## REVISE

### Issue 1: R6 cited as a single property
**ASN-0094, multiple sites**: "(R6 derivation in ASN-0086)", "consumed by R6 (ASN-0086) directly", "The active subset (R6, ASN-0086)"
**Problem**: ASN-0086's foundation has R6a (RetractionStability), R6b (SingleDepthRetraction), R6c (RestorationByReemission), and R6c-Corollary — no plain "R6". The catch-all R6 citations obscure which specific result is being consumed.
**Required**: Replace each R6 citation with the specific sub-claim. The "active-subset definition" reading should cite ASN-0086's `A_K^Σ` Definition or Definition (nullified) directly, not R6.

### Issue 2: Direct ASN-0093 citation in `→` definition
**ASN-0094, `→ — DomExtendingTransition` definition**: "ASN-0093's frame conditions on each K-op ensure the two non-affected stores are preserved pointwise..."
**Problem**: ASN-0093 is not in this review's foundation (ASN-0034, ASN-0043, ASN-0086). The ASN's stated discipline routes substrate facts through the substrate-conforming-layer scaffolding, but this site cites ASN-0093 directly.
**Required**: Route the frame-conditions claim through a named scaffolding clause (e.g., "the K-op frame-condition scaffolding clause") or attribute it via ASN-0086's SubstrateConformingLayer Definition.

### Issue 3: Missing Classifier walkthrough
**ASN-0094, "Per-Shape Template Walkthroughs / Classifier"**: section contains only the template definition (`is_K(d) ≡ (E τ ∈ A_K^Σ :: to₁(τ) = d)`) with no concrete state-evolution example.
**Problem**: Every other shape — Tuple-Classifier, DirectedPair (via FDD), Coverage (via SHCD), Comment, Resolution, Retraction, Provenance — has an emission/template-evaluation walkthrough. Classifier `(0, 1, -, A_doc, ⊤)` is the simplest shape and lacks one. The Tuple-Classifier walkthrough does not substitute because the target domain differs (`A_rel` vs `A_doc`), and the rejection cases that exercise Sh-conf clause (d) at `t_G = A_doc` are never demonstrated.
**Required**: Add a 5–10 line walkthrough at "### Classifier" with one `Emit_K(Σ, home_K, ∅, {(d, δ(1, #d))})` admission, one rejection (e.g., G targeting an `A_rel` address instead of `A_doc` to exercise the partition aspect of clause (d)), and one `is_K(d)` template evaluation.

### Issue 4: Resolution standalone walkthrough deferred
**ASN-0094, "Resolution base templates exercised directly"**: "this example threads `K_res` through Comment's parametric consumer in scope, rather than exhibiting a standalone Resolution registration; the framing in the Resolution walkthrough above flags this limitation and points to where a future standalone example would fit."
**Problem**: The catalog claims Resolution's base templates are mechanically generated per Sh5(b) and admissible standalone. The "worked example" exercises them only as part of Comment's `_via` consumption, so the standalone admissibility claim has no concrete witness in the ASN.
**Required**: Either add the missing standalone walkthrough (e.g., a hypothetical "ApprovedBy" layer relation registered at Resolution and consuming `pair_K`, `from_K`, `to_K`, `from_addrs_K`, `to_addrs_K` with no `_via` consumer in scope), or strengthen the prose to state explicitly that the standalone path is admissible by Sh5(b) without yet being exhibited (currently this is hedged across two paragraphs in different sections).

### Issue 5: Notational conflation in EffectiveWpSimplification walkthrough
**ASN-0094, "Walkthrough: EffectiveWpSimplification at Σ_2"**: "*ρ_1 (`b̂ = ρ_1`, `F' = F_{AR1}`, `G' = G_{AR1}`).*"
**Problem**: ASN-0086's `L_R^Σ` is defined as triples `(a, F, G)` where `a` is the *tuple-address*. The iterator binding `b̂` is the first component, so `b̂ = addr(ρ_1) = b_1`, not the tuple `ρ_1` itself. The walkthrough earlier introduced `b_1 := addr(ρ_1)` but then sets `b̂ = ρ_1`, conflating the object with its address.
**Required**: Change the binding to `b̂ = b_1` (or `b̂ = addr(ρ_1)`) in both bullets of Step 1.

### Issue 6: EffectiveWpSimplification statement under-qualified
**ASN-0094, Corollary statement**: "For every `K ∈ T_admissible`, every `d ∈ dom(Σ.M)`, and every `F, G ∈ Endset`, ASN-0086's `wp_086` for `Emit_K(Σ, d, F, G)` simplifies to `d ∈ dom(Σ.M) ∧ K ∈ T_admissible`..."
**Problem**: The "simplification" is a property of calls *that reach the substrate*. For K ∉ T_cat, Sh-conf rejects upstream of the substrate, so wp_086 is moot. The proof's Case B argument explicitly says "For the call to reach K.λ at all, Sh-conf must admit it." The statement of the corollary should make this conditional explicit so a reader doesn't take "wp_086 simplifies for every K ∈ T_admissible" as a substrate-level claim. (The K ≁ R automatic for K ∉ T_cat argument does close the universal, but the statement as written reads more strongly than what's actually proved.)
**Required**: Reword the statement to indicate that the simplification holds under the framework's *Emit_K routing commitment*, with the understanding that calls failing Sh-conf are short-circuited to `⊥` before wp_086 evaluation.

### Issue 7: Duplicate-Nullify compatibility argument is prose, not theorem
**ASN-0094, "Compatibility with ASN-0086's Nullify postcondition"**: The two-step argument (a) "Active-subset semantics are preserved" and (b) "Audit-slice semantics differ but in a way that does not affect downstream reads" is presented as prose.
**Problem**: This is a substantive interface claim: the framework changes ASN-0086's `Nullify` return type from `Σ' × A_rel^{Σ'}` to `(Σ' × A_rel^{Σ'}) ∪ {⊥}` and admits the `⊥`-branch at duplicate calls. The current prose argues operational compatibility but never states the preserved active-subset property as a formal corollary.
**Required**: Promote the argument to a labeled corollary, e.g., "**Corollary — NullifyActiveSubsetCompatibility.** Under the *Sh4 idempotency contract* with R registered, every `Nullify(Σ, d_retr, a)` call satisfying ASN-0086's P0/P1/P2 preconditions delivers ASN-0086's active-subset content of the Nullify postcondition (`{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` and `a ∈ nullified(Σ')` stable under R6a), whether the contract's clause (iii) admits a fresh `(Σ', _)` or clause (ii) suppresses to `⊥`". With derivation citing R6a + the audit-vs-active distinction.

### Issue 8: Sh4 Case B "no concurrent nullification" qualifier inherits depth gap
**ASN-0094, Sh4 Step Case B**: "a K.λ-step at type K with no concurrent nullification of any τ ∈ A_K^Σ"
**Problem**: For K ≁ R, the qualifier is trivially satisfied (an Emit_K with K ≁ R can't nullify K-tuples). For K ~ R, Case D absorbs the case. So Case B's qualifier is meaningful only at K ≁ R, where it's automatic. The qualifier reads as a substantive precondition but is in fact vacuous in its applicable scope, and the proof doesn't explicitly mark this. A reader trying to verify the case decomposition is exhaustive needs to walk through this reasoning unaided.
**Required**: Either add a one-sentence note at Case B's qualifier ("this qualifier is automatic for K ≁ R by the class-decomposition of `↦`; Case D handles K ~ R") or fold the qualifier into the Case D vs Case B split criterion explicitly.

## OUT_OF_SCOPE

### Topic 1: Multi-process substrate coordination
The Open Questions section already flags this as a scope boundary. Cross-process Sh4 consistency would require a coordination protocol; this is genuinely new territory.

### Topic 2: Ghost-targeting slot semantics
Open Questions flags this. Whether to admit `slot_addrs(F) ⊆ T \ A^Σ` is a substantive shape-language extension, not a gap in the current shape framework.

### Topic 3: Higher-arity links beyond standard-triple
The Scope section explicitly restricts to `L^Σ` (arity-3 slice). Extending to N > 3 would require additional per-slot shape components; out of scope for this ASN.

### Topic 4: Composite shapes (F or G constrained by another relation's content)
Open Questions item. Requires either decomposition into primitives or a new restriction axis; not an error in this ASN.

VERDICT: REVISE
