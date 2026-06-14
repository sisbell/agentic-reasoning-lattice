# Review of ASN-0131

This note is, on the whole, rigorous: the worked instance checks out under hand computation, the union/intersection laws are derived (not asserted) with the `⊇` failure exhibited by a concrete non-injective counterexample, RE-CWP is a genuine non-trivial weakest precondition, and RE-RET separates link-level permanence (R6a) from pair-value removal with care. The mathematics is sound. Two issues remain.

## REVISE

### Issue 1: RE-ADDR — "the only to-set that could cover ℓ_new is its own" omits the step that makes it true

**ASN-0131, "Composing regions" (the passage establishing RE-ADDR), and claims table RE-ADDR**: "every retraction to-set in `Σ'.L` is unit-depth at some link `t ∈ dom(Σ'.L)` … so any `t` distinct from `ℓ_new` is prefix-incomparable to it … and cannot cover it. **The only retraction to-set that could cover `ℓ_new` is its own — present only if `ℓ_new` is itself a retraction** — and it does so exactly when `ℓ_new` retracts its own emitter address."

**Problem**: The antichain (R0a) discharges the case `t ≠ ℓ_new`. For `t = ℓ_new`, the note jumps to "its own" — i.e. it silently identifies the tuple bearing that to-set with `ℓ_new` itself. But a *distinct* tuple `b ≠ ℓ_new` whose to-set targets `ℓ_new` would also place `ℓ_new ∈ nullified(Σ')`, and would directly falsify RE-ADDR: a non-self-retracting `ℓ_new` would then be non-addressable. The fact that no such `b` exists is real but unshown — it needs Nullify's P-tgt, not R0a: every pre-existing retraction's target lies in `dom(Σ.L)` (P1-target `∈ A_rel`, or self-emit-target `=` its own emitter address), hence differs from the fresh `ℓ_new ∉ dom(Σ.L)`, so the *only* tuple that can target `ℓ_new` is the freshly-emitted `ℓ_new` itself. The note cites R0a but neither P-tgt nor freshness-of-target for this step. RE-ADDR is load-bearing — invoked for the intersection counterexample's `(1, e) ∈ Avail(Σ)` and for the retraction emitter `b`'s addressability in RE-RET — so the unshown inference propagates.

**Required**: Add the missing clause — pre-existing retraction targets are confined to `dom(Σ.L)` (Nullify P-tgt) and so differ from the fresh `ℓ_new`; therefore any to-set targeting `ℓ_new` is borne by `ℓ_new` itself. This replaces an assertion with a derivation; it does not add bloat.

### Issue 2: anti-bloat — consumer-enumeration scope-note and bridge method-narration

**ASN-0131, "The unit of the answer: anchoring without names"**:

Quote 1: "The one ASN-0086 fact we consume at definition time is `nullified` itself — its well-definedness and computability — which the bridge carries here to ground `addressable` in RE-DEF and its decidability below."

Quote 2: "Coinciding steps do not by themselves transfer a lemma quantified over all reachable states, because the two vocabularies build `dom(Σ.M)` differently — ASN-0086 registers documents through `K.σ`, ASN-0047 through `K.δ` …"

**Problem**: Quote 1 is exactly the pattern the anti-bloat classifier enumerates — "a definition's introduction enumerates downstream consumers … rather than advancing the definition's meaning" ("addressable in RE-DEF and its decidability below"). It is also self-contradicting: R0a, R-Scope, R6a, R6c are each consumed downstream *through the same bridge*, so "the one ASN-0086 fact we consume" undercounts the bridge's actual job. Quote 2 narrates why a naive method fails before the real argument arrives; the load-bearing content is the one-sentence inclusion that follows it (ASN-0047 documents are `K.σ`-registrable by M0, so replay the identical `K.λ` sequence). The reader skips the "why coinciding steps fail" narration and the from-set consequence-enumeration ("adopting it excludes attributed retractions … which ASN-0086's Convention RetractionDirectionality would otherwise permit") to reach the operation's definition.

**Required**: Cut the consumer-enumeration sentence; compress the bridge to its inclusion (`K.σ`-registrability + `K.λ`-replay), dropping the "why coinciding steps fail" framing. State the empty-from-set fact once, at its use in RE-RET, not as preamble.

## OUT_OF_SCOPE

### Topic 1: image-union-distributivity is image-layer content
**ASN-0131, "Composing regions"** proves `image(W₁ ∪ W₂, d, Σ) = image(W₁, d, Σ) ∪ image(W₂, d, Σ)` inline. This is content-region image machinery; the scope directive places that layer in ASN-0127 ("cite, do not rebuild"). It is a genuinely-needed one-line fact that ASN-0127 happens not to state, so its natural home is there (alongside F-IMG-MONO/CONTR/SWING), cited here — not a defect in this note's reasoning, but image-layer content that drifted in. Non-blocking.

VERDICT: REVISE
