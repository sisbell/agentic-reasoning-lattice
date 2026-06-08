# Review of ASN-0099

## REVISE

### Issue 1: V conflates ASN-0047's atomic vocabulary with a non-atomic composite

**ASN-0099, "Link-Store-Inert Preservation"**: "the operative vocabulary is ASN-0047's extended-state vocabulary (ValidComposite★, V = {K.α, K.λ, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L, K.ρ})"

**Problem**: ASN-0047's ValidComposite★ defines its atomic vocabulary as exactly the seven operations `{K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ}` and states explicitly that "The named composite K.μ~ is not atomic; it may appear in the sequence as shorthand for its K.μ⁻ + K.μ⁺ decomposition." ASN-0099's `V` adds `K.μ~` as an eighth peer member and attributes the whole set to ValidComposite★, which misrepresents the cited definition. The ASN's own A1a contradicts this listing: it handles the atomic operations uniformly ("publish `L' = L` in their operative frame") but treats `K.μ~` as a special case ("the non-atomic K.μ⁻ + K.μ⁺ composite ... preserves Σ.L by transitive composition") — i.e., the ASN concedes `K.μ~` is *not* on equal footing with the atomic ops while simultaneously listing it as one. The tension also surfaces in F9, whose statement quantifies over a single-step "transition Σ → Σ' produced by an operation in V ∖ {K.λ}," yet `K.μ~ ∈ V ∖ {K.λ}` is a multi-step `Σ →* Σ'` composite (the proof's second sentence silently switches to a `Σ →* Σ'` framing to cover it).

**Required**: Either (a) define `V` as ASN-0047's seven atomic operations and let A1a/F9 handle `K.μ~` separately as the composite it already treats it to be, or (b) keep `K.μ~` in a clearly-labeled working set for this ASN that is distinguished from ValidComposite★'s atomic vocabulary, and align F9's "transition Σ → Σ'" wording with the `Σ →* Σ'` form required when a composite is admitted.

VERDICT: REVISE
